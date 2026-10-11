"""页级转写原型（v2）。

思路：把"版面语义"交给模型，几何只保留两件必要的事。
  - 几何：正文带切分（页眉/页脚/脚注隔离）+ 双栏切分 → 每个区域一张图
  - 模型：区域转写为 Markdown（忽略页眉页脚、处理旋转文本、
          公式转 LaTeX、图/表用占位符）
  - 几何：smart 模型定位表格/图的 bbox → 程序裁切为图片资产
          （表格不翻译，截图无损保留，规避数字转写风险）
  - 校验：页级词召回/精确率（剔除图表区域）+ 泄漏 + 复读 + 占位符配对

与 pdf2md.py 的关系：并存。pdf2md.py 是块级管线（精细、补丁多）；
本文件是页级原型（粗粒度、语义交给模型）。人工检验通过后再决定主路径。

用法：
  python pdf2md_page.py <pdf> -o <outdir> [--max-pages N] [--dpi 170]
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf2md as M


# ---------------- 区域规划 ----------------

def plan_regions(page: fitz.Page) -> list:
    """把页面切成待转写的区域：正文（整幅或按栏切分）+ 脚注带。

    正文带由 body_band 给出（页眉/页脚/脚注分隔，已实测 171 页 0 误伤）。

    双栏切分要过两道关，否则会把文字切坏（实测 p1 标题页被切）：
      1. 栏界取「左栏右缘与右栏左缘的中点」（约 270pt），**不是**两个
         栏左边距的中点（约 160pt——那落在左栏内部，会把左栏文字砍半）。
         左缘用中位数抗通栏行。
      2. 页面若存在**通栏行**（标题、跨栏作者行等），不切栏，整幅转写。
         通栏检测只看页面中段 80% 高（页眉/页脚区排除，否则每个页眉
         都会触发）。
    """
    band = M.body_band(page)
    lines = M.page_lines(page, band)
    if not lines:
        return []
    H = page.rect.height
    min_x0 = min(l['x0'] for l in lines)
    max_x1 = max(l['x1'] for l in lines)
    col_a, col_b = M._column_xs(lines, page.rect.width)
    double = bool(col_b and col_b - col_a >= page.rect.width * 0.35)

    regions = []
    split_x = None
    if double:
        mid0 = (col_a + col_b) / 2
        left_x1 = sorted(l['x1'] for l in lines
                         if l['x0'] < mid0 and l['x1'] < col_b - 2)
        if left_x1:
            left_edge = left_x1[len(left_x1) // 2]      # 中位数抗通栏行
            if left_edge < col_b - 6:                    # 栏界须确实在栏间
                gutter = (left_edge + col_b) / 2
                top_ex = band[0] + H * 0.10
                bot_ex = band[1] - H * 0.10
                crossing = [l for l in lines
                            if top_ex < l['y0'] < bot_ex
                            and l['x0'] < gutter - 4 and l['x1'] > gutter + 4]
                if not crossing:
                    split_x = gutter

    if split_x is not None:
        regions.append(('colL', fitz.Rect(min_x0 - 6, band[0], split_x, band[1]),
                        'the LEFT column of a two-column page'))
        regions.append(('colR', fitz.Rect(split_x, band[0], max_x1 + 6, band[1]),
                        'the RIGHT column of a two-column page'))
    else:
        regions.append(('body', fitz.Rect(min_x0 - 6, band[0],
                                          max_x1 + 6, band[1]),
                        'the body of a page (may contain two-column text, '
                        'read left column fully before right)'))

    # 脚注带：body_band 的底界若明显高于页底，说明其下还有内容
    # （脚注、页脚水印、页码）。去掉最底部 18pt 的页码区。
    if band[1] < H - 26:
        regions.append(('fn', fitz.Rect(min_x0 - 6, band[1] + 2,
                                        max_x1 + 6, H - 18),
                        'the footnote area at the bottom of a page'))
    return regions


# ---------------- 图表定位（smart） ----------------

BBOX_SYS = (
    'You locate tables and figures on a page image.\n'
    'Return ONLY a JSON object, no prose, no code fence:\n'
    '{"tables": [{"bbox": [x0,y0,x1,y1]}], "figures": [{"bbox": [x0,y0,x1,y1]}]}\n'
    'bbox = pixel coordinates in THIS image (origin top-left). '
    'Include the caption inside the bbox. If there are none, use empty lists.')

BBOX_DPI = 190


def locate_assets(pool, page: fitz.Page, dpi: int = BBOX_DPI) -> dict:
    """让 smart 模型返回表格/图的 bbox（页面坐标 pt）。

    返回 {'tables': [Rect], 'figures': [Rect], 'model': str}；全部失败返回 {}。
    bbox 做合理性过滤：面积占比 0.5%~90%、越界裁剪、IoU>0.5 去重。
    """
    pix = page.get_pixmap(dpi=dpi)
    b64 = base64.b64encode(pix.tobytes('png')).decode()
    W, H = pix.width, pix.height
    data = None
    used = ''
    for llm in pool:
        try:
            txt, _ = llm.chat(
                BBOX_SYS,
                f'Image size: {W} x {H} pixels. Locate tables and figures.',
                b64, max_tokens=800, temperature=0.0)
            m = re.search(r'\{.*\}', M._clean_md(txt), re.S)
            if not m:
                raise ValueError('no JSON')
            data = json.loads(m.group(0))
            used = llm.name
            break
        except Exception:
            continue
    if data is None:
        return {}

    page_area = page.rect.width * page.rect.height

    def clean(seq):
        out = []
        for item in seq or []:
            try:
                px = item['bbox'] if isinstance(item, dict) else item
                r = fitz.Rect(px[0] * 72 / dpi, px[1] * 72 / dpi,
                              px[2] * 72 / dpi, px[3] * 72 / dpi)
            except Exception:
                continue
            r = r & page.rect
            if r.is_empty:
                continue
            a = (r.x1 - r.x0) * (r.y1 - r.y0)
            if a < page_area * 0.005 or a > page_area * 0.9:
                continue
            out.append(r)
        ded = []
        for r in out:
            dup = False
            for i, s in enumerate(ded):
                it = r & s
                if it.is_empty:
                    continue
                ia = (it.x1 - it.x0) * (it.y1 - it.y0)
                ua = ((r.x1 - r.x0) * (r.y1 - r.y0)
                      + (s.x1 - s.x0) * (s.y1 - s.y0)) - ia
                if ua > 0 and ia / ua > 0.5:
                    if ((r.x1 - r.x0) * (r.y1 - r.y0)
                            > (s.x1 - s.x0) * (s.y1 - s.y0)):
                        ded[i] = r
                    dup = True
                    break
            if not dup:
                ded.append(r)
        return ded

    return {'tables': clean(data.get('tables')),
            'figures': clean(data.get('figures')),
            'model': used}


def page_number_rects(page: fitz.Page) -> list:
    """页码：页顶/页底的孤立纯数字行。各页数字不同，跨页重复检测抓不到，
    单独按"位置 + 纯数字"判定，涂白即可（无 token，不属于正文）。"""
    H = page.rect.height
    out = []
    for l in M.page_lines(page, M.body_band(page)):
        t = l['t'].strip()
        if re.fullmatch(r'\d{1,4}', t) and (l['y0'] < H * 0.08
                                            or l['y1'] > H * 0.90):
            out.append(fitz.Rect(l['x0'], l['y0'], l['x1'], l['y1']))
    return out


def detect_running_bands(doc, body_end: int, min_frac: float = 0.3) -> dict:
    """找出跨页重复出现的页眉/页脚行 -> {pno: [Rect]}，之后涂白。

    running head（如 "C.L. Goulding, C.R. Harvey and M.G. Mazzoleni"、
    "Journal of Financial Economics 149 (2023) 378–406"）在页顶重复出现，
    若只依赖提示词"忽略页眉"容易被模型当正文转写（实测 p2 两栏各抄了
    一段）。做法：归一化前 6 词计数，出现于 >=30% 页面的判为重复行；
    只看页面顶部 12% / 底部 8%（正文不会在那里重复整句）。
    """
    from collections import Counter, defaultdict
    counts = Counter()
    occ = defaultdict(list)
    for pno in range(body_end):
        page = doc[pno]
        H = page.rect.height
        lines = M.page_lines(page, M.body_band(page))
        seen = set()
        for l in lines:
            if not (l['y0'] < H * 0.12 or l['y1'] > H * 0.92):
                continue
            ws = M._dup_words(l['t'])[:6]
            if len(ws) < 3:
                continue
            key = ' '.join(ws)
            if key in seen:
                continue
            seen.add(key)
            counts[key] += 1
            occ[key].append((pno, fitz.Rect(l['x0'], l['y0'],
                                            l['x1'], l['y1'])))
    out = defaultdict(list)
    thresh = max(2, int(body_end * min_frac))
    for key, c in counts.items():
        if c >= thresh:
            for pno, r in occ[key]:
                out[pno].append(r)
    return dict(out)


def crop_assets(page: fitz.Page, assets: dict, out_dir: Path,
                counters: dict, dpi: int = 200) -> list:
    """把 bbox 裁成 PNG 资产。返回 [(kind, clip, filename, token)]。

    编号为**文档级**（[[FIG-1]]、[[TAB-1]]…），token 会被印到页面上
    供转写模型照抄，展开时再替换成真实的图片链接。
    """
    assets_dir = out_dir / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for kind, key, prefix in (('table', 'tables', 'TAB'),
                              ('figure', 'figures', 'FIG')):
        for r in assets.get(key, []):
            counters[kind] = counters.get(kind, 0) + 1
            n = counters[kind]
            pad = 8
            clip = fitz.Rect(r.x0 - pad, r.y0 - pad,
                             r.x1 + pad, r.y1 + pad) & page.rect
            pix = page.get_pixmap(clip=clip, dpi=dpi)
            fn = f'{kind}-{n}.png'
            pix.save(str(assets_dir / fn))
            saved.append((kind, clip, fn, f'[[{prefix}-{n}]]'))
    return saved


def mask_assets(page: fitz.Page, saved: list) -> dict:
    """把图表区域涂白，并在原位置印上短 token（[[FIG-1]] 等）。

    这是"表格截图替代 + 程序控制位置"的关键：模型不需要理解
    "这里是图还是表"——它只需要照抄看到的 token（这是它的强项），
    位置信息由 token 在页面上的物理位置天然携带。展开时程序把
    token 替换成 ![kind](assets/xxx.png)，位置和资产都精确对应。

    涂白用 overlay=True 追加到内容流末尾，渲染时覆盖原文字；
    文本层不动，校验参照照旧可提取（再由 exclude_rects 剔除）。
    """
    tokens = {}
    for kind, rect, fn, token in saved:
        page.draw_rect(rect, color=None, fill=(1, 1, 1), overlay=True)
        page.insert_text((rect.x0 + 3, rect.y0 + 11), token,
                         fontsize=10, color=(0.45, 0.45, 0.45),
                         overlay=True)
        tokens[token] = (kind, fn)
    return tokens


# ---------------- 页级校验 ----------------

def verify_page(pdf_text: str, md: str, asset_rects: list,
                tokens: dict) -> dict:
    """页级校验。

    - 词召回/精确率：参照词表**剔除图表 bbox 内的词**——图表以图片形式
      保留、正文里只有 token，若不剔除会把每页都判成漏写。
    - 泄漏/复读：整页文本直接判。
    - token 配对：每个 [[FIG-n]]/[[TAB-n]] 都应出现在转写结果里
      （模型只需照抄它看到的 token）。缺失 = 该资产在正文中无位置，
      会被标记并在页尾兜底，人可复核。
    """
    from collections import Counter
    issues = []

    def words(s):
        return M._dup_words(s)

    ref = Counter(words(pdf_text))
    for r in asset_rects:
        inside = r.get('text') or ''
        for w, c in Counter(words(inside)).items():
            if ref.get(w, 0) > 0:
                ref[w] = max(0, ref[w] - c)
    md_wo = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', md)
    md_wo = re.sub(r'\[\[(?:FIG|TAB)-\d+\]\]', ' ', md_wo)
    out = Counter(words(md_wo))

    inter = sum((ref & out).values())
    recall = inter / max(sum(ref.values()), 1)
    precision = inter / max(sum(out.values()), 1)

    if recall < 0.80:
        issues.append({
            'kind': 'PROSE_LOSS' if recall < 0.55 else 'PROSE_MISMATCH',
            'detail': f'页级词召回 {recall:.0%}'})
    if precision < 0.85:
        issues.append({'kind': 'PROSE_HALLUCINATION',
                       'detail': f'页级精确率 {precision:.0%}'})
    if M._is_reasoning_leak(md):
        issues.append({'kind': 'REASONING_LEAK', 'detail': '输出含推理残留'})
    rep = M._detect_repeat(md)
    if rep:
        issues.append({'kind': 'REPETITION',
                       'detail': f'{rep} 处 ≥12 词重复（双栏串读/复读）'})
    if tokens:
        missing = [t for t in tokens if t not in md]
        if missing:
            issues.append({
                'kind': 'PLACEHOLDER_MISMATCH',
                'detail': f'{len(missing)} 个 token 未出现在转写中：'
                          f'{", ".join(missing[:6])}（资产已裁切，'
                          f'将在页尾兜底）'})
    return {'ok': not issues, 'issues': issues,
            'recall': round(recall, 3), 'precision': round(precision, 3)}


# ---------------- 主流程 ----------------

SEVERITY = {
    'PROSE_LOSS': 'critical', 'PROSE_HALLUCINATION': 'critical',
    'REASONING_LEAK': 'critical', 'PLACEHOLDER_MISMATCH': 'critical',
    'PROSE_MISMATCH': 'warn', 'REPETITION': 'warn',
}


def convert(pdf_path: Path, out_dir: Path, local, smart_pool,
            max_pages: int | None = None, dpi: int = 170,
            use_bbox: bool = True, quiet: bool = False) -> dict:
    doc = fitz.open(pdf_path)
    body_end = M.detect_body_end(doc)
    if max_pages:
        body_end = min(body_end, max_pages)
    cache = out_dir / '.vlm_cache'
    tr = M.Transcriber(local, smart_pool, cache)
    pages_dir = out_dir / 'pages'
    pages_dir.mkdir(parents=True, exist_ok=True)

    md_parts, per_page = [], []
    counters: dict = {}
    running = detect_running_bands(doc, body_end)
    for pno in range(body_end):
        page = doc[pno]
        t0 = time.time()
        # 顺序很重要：先按原始页面做区域规划与图表定位（涂白会改渲染），
        # 然后裁图、涂白+印 token，最后才送转写。
        regions = plan_regions(page)
        assets = locate_assets(smart_pool, page) if use_bbox else {}
        saved = crop_assets(page, assets, out_dir, counters)
        tokens = mask_assets(page, saved)
        # 跨页重复的页眉/页脚：涂白（无 token），并从校验参照剔除
        run_rects = running.get(pno, []) + page_number_rects(page)
        for r in run_rects:
            page.draw_rect(r, color=None, fill=(1, 1, 1), overlay=True)
        excl_rects = [clip for _, clip, _, _ in saved] + run_rects
        salt = ','.join(sorted(tokens)) + f'|dpi{dpi}|run{len(run_rects)}'

        region_md = []
        for tag, rect, hint in regions:
            try:
                res = tr.transcribe(page, rect, 'page', pdf_path.name,
                                    pno, dpi=dpi, salt=salt,
                                    exclude_rects=excl_rects)
                region_md.append(res['md'])
            except Exception as e:
                region_md.append('')
                per_page.append({'page': pno + 1, 'fatal': str(e)[:120]})

        asset_only = []
        for kind, clip, fn, tok in saved:
            asset_only.append({'rect': tuple(round(v, 1) for v in clip),
                               'text': M.normalize_pdf_text(
                                   page.get_text('text', clip=clip))})
        for r in run_rects:
            asset_only.append({'rect': tuple(round(v, 1) for v in r),
                               'text': M.normalize_pdf_text(
                                   page.get_text('text', clip=r))})
        md_page = '\n\n'.join(x for x in region_md if x.strip())
        v = verify_page(M.normalize_pdf_text(page.get_text()),
                        md_page, asset_only, tokens)

        # 展开 token -> 图片链接；缺失的页尾兜底
        missing = []
        for tok, (kind, fn) in tokens.items():
            if tok in md_page:
                md_page = md_page.replace(tok, f'![{kind}](assets/{fn})')
            else:
                missing.append((tok, kind, fn))
        if missing:
            md_page += '\n\n' + '\n\n'.join(
                f'<!-- {tok} 未在正文定位 -->\n![{kind}](assets/{fn})'
                for tok, kind, fn in missing)
        md_parts.append(md_page)
        per_page.append({
            'page': pno + 1,
            'regions': [t for t, _, _ in regions],
            'ok': v['ok'], 'issues': v['issues'],
            'recall': v['recall'], 'precision': v['precision'],
            'assets': [(k, fn) for k, _, fn, _ in saved],
            'tokens_missing': [t for t, _, _ in missing],
            'bbox_model': assets.get('model', ''),
            'secs': round(time.time() - t0, 1),
        })
        # 页面预览（供人工核对；含涂白效果）
        pix = page.get_pixmap(dpi=90)
        pix.save(str(pages_dir / f'p{pno + 1:02d}.png'))
        if not quiet:
            flag = 'OK ' if v['ok'] else '!! '
            print(f'  [{flag}] p{pno + 1:2d}: regions={len(regions)} '
                  f'recall={v["recall"]:.0%} prec={v["precision"]:.0%} '
                  f'assets={len(saved)} '
                  f'{v["issues"] and [i["kind"] for i in v["issues"]] or ""}',
                  flush=True)

    # ---- 组装 ----
    text = '\n\n'.join(x for x in md_parts if x.strip())
    text = re.sub(r'\n{3,}', '\n\n', text)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'paper.md').write_text(text + '\n', encoding='utf-8')

    meta = {'source': pdf_path.name, 'pages': len(doc),
            'body_end_page': body_end, 'dpi': dpi,
            'stats': tr.stats, 'pages_detail': per_page}
    (out_dir / 'meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    # ---- 复核清单 ----
    flagged = [p for p in per_page if not p.get('ok', True)
               or p.get('fatal')]
    if flagged:
        lines = [f'# 页级复核清单 — {pdf_path.name}', '',
                 f'- 正文页数：{body_end}',
                 f'- 存疑页：{len(flagged)} / {body_end}', '',
                 '每页预览图在 `pages/`，裁切的表格/图在 `assets/`。',
                 '']
        for p in flagged:
            lines.append(f'## p{p["page"]}')
            lines.append('')
            lines.append(f'![p{p["page"]}](pages/p{p["page"]:02d}.png)')
            lines.append('')
            if p.get('fatal'):
                lines.append(f'- 致命错误：{p["fatal"]}')
            for it in p.get('issues', []):
                lvl = SEVERITY.get(it['kind'], 'warn')
                lines.append(f'- `{it["kind"]}`（{lvl}）{it["detail"]}')
            lines.append(f'- 召回 {p.get("recall")} / 精确 {p.get("precision")}')
            lines.append('')
        rep = out_dir / 'review.md'
        rep.write_text('\n'.join(lines), encoding='utf-8')
        meta['review_report'] = str(rep)
    return meta


def assets_saved_any(per_page) -> bool:
    return any(p.get('assets') for p in per_page)


def main() -> int:
    ap = argparse.ArgumentParser(description='页级转写原型（v2）')
    ap.add_argument('pdf', type=Path)
    ap.add_argument('-o', '--out', type=Path, required=True)
    ap.add_argument('--max-pages', type=int, default=None)
    ap.add_argument('--dpi', type=int, default=170)
    ap.add_argument('--no-bbox', action='store_true',
                    help='跳过表格/图定位（不裁切资产）')
    ap.add_argument('--env', type=Path, default=None)
    args = ap.parse_args()

    env_path = M.find_env_file(args.env)
    env = M.load_env(str(env_path))
    if not env:
        print(f'[error] 未读到配置：{env_path}')
        return 2
    local = M.LLM(env['LLM_LOCAL_URL'], env['LLM_LOCAL_API_KEY'],
                  env.get('LLM_LOCAL', ''), 'local')
    pool = M.build_smart_pool(env)
    print(f'[cfg] local={local.model} bbox池={[m.model for m in pool]}')
    t0 = time.time()
    meta = convert(args.pdf, args.out, local, pool,
                   max_pages=args.max_pages, dpi=args.dpi,
                   use_bbox=not args.no_bbox)
    s = meta['stats']
    pages = meta['pages_detail']
    n_bad = sum(1 for p in pages if not p.get('ok', True) or p.get('fatal'))
    print(f'[ok] {args.out / "paper.md"}')
    print(f'  正文页 {meta["body_end_page"]}, 存疑页 {n_bad}')
    print(f'  local={s.get("local", 0)} 复核={s.get("review", 0)} '
          f'缓存={s.get("cached", 0)}')
    print(f'  总耗时 {(time.time() - t0) / 60:.1f} 分钟')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())