"""pdf2md_vlm.py — PDF → 高保真 Markdown（视觉转写驱动）。

核心思想
--------
不解析 PDF 的字形编码（数学字体各家不同，CM/AdvGulliver/MathTime/
自定义单字母字族…），而是：
  1) 版面几何  -> 切出「段落块 / display 公式块 / 表格 / 图」区域（字体无关）
  2) 区域渲染  -> 高分辨率位图（模型看得见真实字形与上下标关系）
  3) local VLM -> 逐块转写为 Markdown（含 $...$ / $$...$$）
  4. 校验      -> 与 PDF 字符清单交叉核对（词精确率/召回率 + 公式幻觉）
  5. smart复核 -> 校验失败的块，附带疑点描述交由强模型重做

这样既避免字形映射的过拟合，又用可验证的方式压制静默错误。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import fitz

# 表格/图抽取走几何抽取（与字体无关），实现在同目录的 tables_figures.py。
# 该模块缺失时 extract_media 会显式报错，不静默返回空——否则调用方
# 会以为"这篇论文没有表/图"，而实际是没装依赖。
if __package__:
    from . import tables_figures as geometry
    _GEOMETRY_ERR = None
else:                                  # 直接以脚本方式运行
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import tables_figures as geometry
        _GEOMETRY_ERR = None
    except ImportError as e:           # pragma: no cover
        geometry = None
        _GEOMETRY_ERR = e

# ---------------- 环境 ----------------

def load_env(path: str = '.env') -> dict:
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, _, v = line.partition('=')
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


# ---------------- LLM 客户端 ----------------

class LLM:
    def __init__(self, url: str, key: str, model: str, name: str):
        self.url, self.key, self.model, self.name = url.rstrip('/'), key, model, name

    def chat(self, system: str, user: str, image_b64: str | None = None,
             max_tokens: int = 1500, temperature: float = 0.0,
             retries: int = 3) -> tuple[str, float]:
        content = [{'type': 'text', 'text': user}]
        if image_b64:
            content.append({'type': 'image_url',
                            'image_url': {'url': 'data:image/png;base64,' + image_b64}})
        body = {'model': self.model, 'temperature': temperature,
                'max_tokens': max_tokens,
                'messages': [{'role': 'system', 'content': system},
                             {'role': 'user', 'content': content}]}
        data = json.dumps(body).encode()
        last = None
        for attempt in range(retries + 1):
            req = urllib.request.Request(
                self.url + '/chat/completions', data=data,
                headers={'Authorization': 'Bearer ' + self.key,
                         'Content-Type': 'application/json'})
            try:
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=300) as r:
                    out = json.load(r)
                return out['choices'][0]['message']['content'], time.time() - t0
            except urllib.error.HTTPError as e:
                detail = ''
                try:
                    detail = e.read().decode()
                except Exception:
                    pass
                # 部分模型强制 temperature=1
                if 'temperature' in detail.lower() and 'only 1' in detail.lower():
                    body['temperature'] = 1.0
                    data = json.dumps(body).encode()
                    last = e
                    continue
                last = e
                if attempt == retries - 1:
                    break
                time.sleep(1.5 * (attempt + 1))
            except Exception as e:
                last = e
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f'[{self.name}] LLM 调用失败: {last}')


# ---------------- PDF 渲染 ----------------

def render_box(page: fitz.Page, box: fitz.Rect, dpi: int = 280) -> tuple[str, int, int]:
    r = (fitz.Rect(box.x0 - 5, box.y0 - 5, box.x1 + 5, box.y1 + 5)) & page.rect
    pix = page.get_pixmap(clip=r, dpi=dpi)
    return base64.b64encode(pix.tobytes('png')).decode(), pix.width, pix.height


def text_in_box(page: fitz.Page, box: fitz.Rect, pad: float = 5) -> str:
    r = (fitz.Rect(box.x0 - pad, box.y0 - pad, box.x1 + pad, box.y1 + pad)) & page.rect
    return re.sub(r'\s+', ' ', page.get_text('text', clip=r)).strip()


# ---------------- 脚注/页眉隔离（字体无关） ----------------

def body_band(page: fitz.Page) -> tuple[float, float]:
    """返回正文区的 (y_top, y_bottom)。用页眉页脚的水平分隔线切出正文。"""
    H, W = page.rect.height, page.rect.width
    ys = []
    for dr in page.get_drawings():
        r = dr['rect']
        # 脚注/页眉分隔线有两个稳定特征：横跨 >=45% 页宽，且位置固定
        # （页眉在页顶 16% 内，页脚线在页底 12% 内）。图内的框线/图例线
        # 虽然也可能很宽，但位置随机——TimeSeriesMomentum p7 的
        # Figure 1 有两条 206pt（页宽 544，38%）的线位于页面中部，
        # 若只看宽度会误判成脚注线，导致 y>466 的正文被整片丢弃。
        if (0.2 <= r.height <= 2.6 and r.width >= W * 0.45
                and r.y0 > 50):
            ys.append(r.y0)
    try:
        for img in page.get_image_info():
            b = fitz.Rect(img['bbox'])
            if (0.3 <= b.height <= 3.2 and b.width >= W * 0.45
                    and b.y0 > 50):
                ys.append(b.y0)
    except Exception:
        pass
    top = 0.0
    bottom = H
    if ys:
        top = max([y for y in ys if y < H * 0.16] or [0.0])
        # 脚注分隔线只出现在页底 12% 内——这一条约束能挡掉图内框线
        bottom = min([y for y in ys if y > H * 0.86] or [H])

    # 页底成片小字号 = 脚注区。Elsevier 双栏页底**没有分隔线**，
    # 但脚注字号明显小于正文（实测 turning_points p2：正文 9.7pt、
    # 脚注 7.3pt），靠字号可以可靠切出。
    from collections import Counter
    sized = []
    for b in page.get_text('dict').get('blocks', []):
        if b.get('type') != 0:
            continue
        for ln in b.get('lines', []):
            sp = ln.get('spans', [])
            if not sp:
                continue
            t = ''.join(s.get('text', '') for s in sp).strip()
            if len(t) > 25:
                sized.append((ln['bbox'][1],
                              max(s.get('size', 0) for s in sp)))
    if len(sized) >= 8:
        body_sz = Counter(round(s[1], 1) for s in sized).most_common(1)[0][0]
        # 排除图形区域：与矢量图形/图片重叠的行是图表标签，不能当脚注
        gfx = []
        try:
            for dr in page.get_drawings():
                r = dr['rect']
                if r.height > 12 and r.width > 12:
                    gfx.append(r)
            for img in page.get_image_info():
                gfx.append(fitz.Rect(img['bbox']))
        except Exception:
            pass

        def in_gfx(y, x0=0.0, x1=page.rect.width):
            rc = fitz.Rect(x0, y - 1, x1, y + 12)
            ra = max((rc.x1 - rc.x0) * (rc.y1 - rc.y0), 1e-6)
            for g in gfx:
                inter = g & rc
                if inter.is_empty:
                    continue
                if (inter.x1 - inter.x0) * (inter.y1 - inter.y0) > 0.5 * ra:
                    return True
            return False

        cands = []
        run_texts = []
        for b in page.get_text('dict').get('blocks', []):
            if b.get('type') != 0:
                continue
            for ln in b.get('lines', []):
                sp = ln.get('spans', [])
                if not sp:
                    continue
                t = ''.join(s.get('text', '') for s in sp).strip()
                y, sz = ln['bbox'][1], max(s.get('size', 0) for s in sp)
                if (len(t) > 25 and sz < body_sz - 0.45
                        and y > H * 0.55 and not in_gfx(y, ln['bbox'][0],
                                                       ln['bbox'][2])):
                    cands.append(y)
                    run_texts.append(t)
        cands.sort()
        # 连续成片小字号的**首行**若是图/表注（Fig. N. / Table N. / Panel A），
        # 那不是脚注而是图表说明——TimeSeriesMomentum p7 的正文就是这样
        # 被误切的（正文 8.1pt 占多数，6.5pt 的 Fig.1 图注反被判为脚注）。
        if run_texts:
            first = re.sub(r'^\s*', '', run_texts[0])
            if re.match(r'^(Fig\.?|Figure|Table|Panel|Notes?\b|Chart)\b',
                        first, re.I):
                cands = []
        # 图表里的坐标轴标签也是小字号，但它们零散分布；
        # 脚注是**页底连续成片**的小字号行。要求候选区间连续覆盖
        # >=6 行且起点低于页高 78%（图表区通常在页面上半部）。
        best = None
        if cands:
            # 必须是**近似连续成片**的小字号行：相邻候选 y 间距
            # <= 该段行距的 1.6 倍。Elsevier 双栏里图注紧跟正文下方，
            # 正文与图注字号交错（实测 turning_points p14：8.0pt 正文
            # 与 6.4pt 图注在 y=662/667/673/676 交替），交错不算成片。
            gaps = [b - a for a, b in zip(cands, cands[1:])]
            if gaps:
                step = sorted(gaps)[len(gaps) // 2]
                run_start, run_len = cands[0], 1
                for a, b, g in zip(cands, cands[1:], gaps):
                    if g <= max(step * 1.6, 14):
                        run_len += 1
                    else:
                        if run_len >= 6:
                            best = run_start
                            break
                        run_start, run_len = b, 1
                if best is None and run_len >= 6:
                    best = run_start
            if best is not None and best > H * 0.78:
                # 字号启发式容易误伤：Elsevier 双栏里正文段落也可能是
                # 页底唯一的小字号块（实测 turning_points p14：末段正文
                # "23 Recent studies focus on..." 6 行连续、含文献引用，
                # 与脚注特征几乎一样）。
                # 区分点：脚注是**注**，通常 1-9 行、<900 字符，且首字符
                # 是紧贴正文的标号数字；正文段落即使首词是数字也会有
                # 完整的句子结构与更长篇幅。
                zone_raw = page.get_text('text', clip=fitz.Rect(
                    0, best - 4, page.rect.width, page.rect.height))
                zone = ' '.join(zone_raw.split())
                n_lines = len([x for x in zone_raw.splitlines() if x.strip()])
                starts_num = bool(re.match(r'^\d{1,2}\s*[A-Z(]', zone))
                # 页脚（页码等）在分隔线更下方，这里只看第一条分隔线
                if starts_num and n_lines <= 9 and len(zone) < 900:
                    bottom = min(bottom, best - 4)
    return top + 2, bottom - 2


# ---------------- 段落切分（字体无关） ----------------

_WATERMARK_RE = re.compile(
    r'electronic copy available at|ssrn\.com/abstract'
    r'|this article is published by|download from|\bopen access\b',
    re.I)


def _is_page_watermark(t: str) -> bool:
    """出版社加在每页的固定水印/版权行（与正文内容无关）。"""
    return bool(_WATERMARK_RE.search(t))


def page_lines(page: fitz.Page, band: tuple[float, float]) -> list[dict]:
    top, bot = band
    lines = []
    for b in page.get_text('dict').get('blocks', []):
        if b.get('type') != 0:
            continue
        for ln in b.get('lines', []):
            t = ''.join(s.get('text', '') for s in ln.get('spans', []))
            if not t.strip():
                continue
            x0, y0, x1, y1 = ln['bbox']
            if y0 < top or y1 > bot:
                continue
            sizes = [s.get('size', 0) for s in ln.get('spans', [])]
            lines.append({'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                          't': t, 'minS': min(sizes) if sizes else 0,
                          'maxS': max(sizes) if sizes else 0})
    lines.sort(key=lambda l: (l['y0'], l['x0']))
    # 页脚水印：Elsevier 每页重复的
    # 'Electronic copy available at: https://ssrn.com/abstract=...'。
    # 按内容判定而非位置——按位置会误删页眉行号和页底表格
    # （实测 'This table presents the results of...' 在页底）。
    #
    # 注：**不做**栏宽裁剪。尝试过按行宽分位数定栏界，结果会误删
    # 跨栏正文（mhim p14 的 'where rWML,t is the unscaled...'）和
    # 表格内短行。侧栏水印已由内容判定覆盖，无需几何过滤。
    lines = [l for l in lines if not _is_page_watermark(l['t'])]
    return lines


def to_rows(lines: list[dict]) -> list[dict]:
    """按 y 重叠聚成 row；行内碎片按 x 拼接。"""
    rows, cur = [], []
    for l in lines:
        if cur:
            p = cur[-1]
            overlap = l['y0'] <= p['y1'] + 2 and l['y1'] >= p['y0'] - 2
            if overlap:
                cur.append(l)
                continue
            rows.append(cur)
            cur = [l]
        else:
            cur = [l]
    if cur:
        rows.append(cur)
    out = []
    for r in rows:
        r.sort(key=lambda l: l['x0'])
        out.append({'x0': min(l['x0'] for l in r), 'x1': max(l['x1'] for l in r),
                    'y0': min(l['y0'] for l in r), 'y1': max(l['y1'] for l in r),
                    't': ''.join(l['t'] for l in r).strip(),
                    'maxS': max(l['maxS'] for l in r),
                    'minS': min(l['minS'] for l in r)})
    out.sort(key=lambda r: r['y0'])
    return out


def _column_xs(rows: list[dict], page_w: float) -> tuple[float, float]:
    """探测本页所有行的栏左边距集合（1 或 2 个）。

    次峰必须有**实质行数**才认作第二栏。真双栏的每一栏都有成百行
    起始于相同的 x；而单个行尾碎片（行内公式/分句被 PDF 拆出的独立
    line，如 "An autoregression of monthly" x0=347.9）也会形成一个
    x0 峰，若不加质量门槛，单栏页会被误判成双栏：
    实测 mhim p4 因此把 1 行碎片当成"右栏"，单独聚段转写，
    产出与正文重复的垃圾块（'An autoregression of monthly ...'）。
    """
    from collections import Counter
    cnt = Counter(round(r['x0']) for r in rows if len(r['t']) > 20)
    if not cnt:
        return 0.0, 0.0
    main_x, main_n = cnt.most_common(1)[0]
    # 第二栏的行数门槛：实测（5 篇 30 页统计）真第二栏最少 5 行
    # （turning_points p13 的右栏只剩 5 行），而行尾碎片堆最多 2 行。
    # 取 max(5, 15%) 落在这两者之间。
    min_mass = max(5, int(main_n * 0.15))
    # 找出与主峰相距 >= 页宽*0.35 的众数峰，且行数达标
    cands = [(x, n) for x, n in cnt.items()
             if abs(x - main_x) >= page_w * 0.35 and n >= min_mass]
    if cands:
        second_x = max(cands, key=lambda kv: kv[1])[0]
        return float(min(main_x, second_x)), float(max(main_x, second_x))
    return float(main_x), 0.0


def rows_to_paras(rows: list[dict], page_w: float = 600.0) -> list[dict]:
    """rows（或 lines）-> 段落。

    段首判定用「相对**栏左边距**的缩进」，而不是「相对上一行的 x 偏移」——
    后者会被行内公式碎片的 x 偏移误触发，把段落从中间切断
    （实测：'crash of -73.42% in' / 'three months.' 被切成两段）。

    双栏必须**先分栏再聚行**：to_rows 会把左右栏同一 y 的行并成一行，
    之后再判断栏就晚了（x0 众数只剩左栏，右栏被吞进左栏段落，
    实测 TimeSeriesMomentum p2 出现 3255 字符的"段落"）。
    因此这里接收原始 lines，先按 x 簇分栏，各栏内独立聚行聚段。
    """
    # 若传入的是已按 y 合并的 rows（缺少逐行 x 分布），退回原行为
    paras: list[list[dict]] = []
    col_a, col_b = _column_xs(rows, page_w)
    if col_b and col_b - col_a >= page_w * 0.35:
        mid = (col_a + col_b) / 2
        left = [r for r in rows if r['x0'] < mid]
        right = [r for r in rows if r['x0'] >= mid]
        paras = _split_one_col(to_rows(left)) + _split_one_col(to_rows(right))
    else:
        paras = _split_one_col(to_rows(rows))
    out = []
    for p in paras:
        box = fitz.Rect(min(x['x0'] for x in p), min(x['y0'] for x in p),
                        max(x['x1'] for x in p), max(x['y1'] for x in p))
        text = ' '.join(x['t'] for x in p).strip()
        sizes = [x['maxS'] for x in p]
        out.append({'box': box, 'text': text, 'size': max(sizes) if sizes else 0})
    return out


def _split_one_col(rows: list[dict]) -> list[list[dict]]:
    from collections import Counter
    paras, cur, prev = [], [], None
    xs = Counter(round(r['x0']) for r in rows if len(r['t']) > 20)
    col_x = max(xs.items(), key=lambda kv: kv[1])[0] if xs else 0.0
    for r in rows:
        brk = prev is None
        if prev is not None:
            long_enough = len(prev['t']) > 20
            indented = r['x0'] > col_x + 7 and len(r['t']) > 20
            if abs(r['maxS'] - prev['maxS']) > 1.2:
                brk = True
            elif r['y0'] - prev['y1'] > 13:
                brk = True
            elif indented and long_enough:
                brk = True
        if brk and cur:
            paras.append(cur)
            cur = []
        cur.append(r)
        prev = r
    if cur:
        paras.append(cur)
    return paras


# ---------------- display 公式定位（字体无关） ----------------

GREEK = re.compile('[\u0370-\u03ff\u2200-\u22ff\u2211\u2210\u220f\u2202'
                   '\u2207\u221a\u221e\u2264\u2265\u2260\u2192\u00d7\u00f7'
                   '\u00b1\u2212]')
EQNO = re.compile(r'\(\s*\d{1,2}[a-z]?\s*\)\s*[,.;]?\s*$')
EQOP = re.compile(r'[=≈≡≤≥≠]')
CAPT = re.compile(r'^\s*(Table|Figure|Fig\.|Tableau|Panel|Chart|Scheme|图|表)\b', re.I)
URLISH = re.compile(r'(@|https?://|www\.|\.com|\.edu|\.org)')


def is_display_equation(row: dict, colw: float) -> bool:
    """独占窄带 + 数学信号 + 右端式号。字体无关。

    「独占」才是关键判据，不是「窄」：display 公式必然整行独占排版，
    而行内公式总与正文左右并排。接近栏宽的 display 公式很常见
    （如 eq1 的 rWML,t = 1.752 - 0.378 rRMRF,t ... 占 353pt），
    只用宽度阈值会把它漏掉。
    """
    t = row['t']
    if URLISH.search(t) or CAPT.match(t):
        return False
    w = row['x1'] - row['x0']
    has_eqno = bool(EQNO.search(t))
    has_greek = bool(GREEK.search(t))
    has_eq = False
    for m in EQOP.finditer(t):
        i = m.start()
        if re.search(r'[A-Za-z0-9)\]}α-ωΑ-ΩΣ]', t[max(0, i - 2):i] + t[i + 1:i + 3]):
            has_eq = True
            break
    narrow = w < colw * 0.90
    wide_eq = has_eq and has_eqno        # 近栏宽但带式号 -> 仍是 display
    if has_eqno and (narrow or wide_eq):
        return True
    if (has_eq or has_greek) and narrow:
        # 排除纯散文行
        words = [x for x in re.split(r'\s+', t) if x]
        common = set('the of and is in to for that with are this from which has '
                     'have their they its return risk strategy market stock '
                     'portfolio month monthly we our not but all can data '
                     'model results figure table period sample time'.split())
        if len(words) >= 6 and not has_eq:
            low = sum(1 for x in words if x.strip('.,;:()').lower() in common)
            if low / len(words) >= 0.5:
                return False
        return True
    return False


_PROSE_WORD = re.compile(r'[A-Za-z]{3,}')
_PROSE_COMMON = set(
    'the and for with that this from which are was were has have their they '
    'its not but all can our may such when where while bear bull equal over '
    'under both each also more most than then into out about after before'
    .split())


NUMCELL = re.compile(r'^\s*[-(]?\s*[\d.,]+\s*[%)]?\s*$')


def _is_math_continuation(t: str) -> bool:
    """是否公式的续行（t 值行 / 限位行 / 纯符号行），而非正文散文或表格。"""
    words = _PROSE_WORD.findall(t)
    if len(words) > 6:
        return False
    if any(w.lower() in _PROSE_COMMON for w in words):
        return False
    # 表格数值行：`(1) (2) (3)` 或 `1.955 2.428 (6.6)` —— 大量独立数字/括号数字
    num_cells = re.findall(r'\(\s*-?\d[\d.,]*\s*\)', t)
    if len(num_cells) >= 3:
        return False
    toks_n = re.findall(r'(?<![A-Za-z])[\d.,]+(?![A-Za-z])', t)
    if len(toks_n) >= 5 and len(words) <= 2:
        return False
    if len(NUMCELL.findall(t)) >= 3:
        return False
    return bool(re.search(r'[=<>≈≤≥∑∫√()\[\]0-9,.]', t))


def _table_row_indices(page: fitz.Page, band, rows: list[dict]) -> set:
    """表格行索引（整片多列数值行）。用于把表格从公式候选中排除。
    表格的共性是「成片的等距数值 + 常有 booktabs 横线」，与字体无关。

    注意：不能用「单行数字个数>=3」当表格判据——正文里
    `a = 0, w = 0, 1/2` 这类含多个数字的行会中招，进而把后续正文
    整片误标为表格、把真公式排除掉。必须要求：连续 >=4 行数字密集，
    且这些行的 x 起点/行宽高度一致（真表格才会这样排）。
    """
    import re
    if len(rows) < 6:
        return set()
    W = page.rect.width
    top, bot = band

    def numeric_count(t):
        # 独立数字 token：前后不是字母
        return len(re.findall(r'(?<![\w.])\(?-?\d[\d.,]*\)?\s*%?', t))

    numeric_idx = [i for i, r in enumerate(rows) if numeric_count(r['t']) >= 4]
    hlines = []
    for dr in page.get_drawings():
        rc = dr['rect']
        if 0.2 <= rc.height <= 2.6 and rc.width >= W * 0.35 and rc.y0 > top:
            hlines.append(rc.y0)
    try:
        for img in page.get_image_info():
            b = fitz.Rect(img['bbox'])
            if 0.3 <= b.height <= 3.2 and b.width >= W * 0.35 and b.y0 > top:
                hlines.append(b.y0)
    except Exception:
        pass

    marked = set()
    i = 0
    while i < len(numeric_idx):
        run = [numeric_idx[i]]
        j = i + 1
        while j < len(numeric_idx) and numeric_idx[j] - numeric_idx[j - 1] <= 1:
            run.append(numeric_idx[j])
            j += 1
        if len(run) >= 4:
            rs = [rows[k] for k in run]
            # 行宽一致性：真表格各行右边界对齐（方差小）
            rights = [r['x1'] for r in rs]
            lefts = [r['x0'] for r in rs]
            right_spread = max(rights) - min(rights)
            left_spread = max(lefts) - min(lefts)
            near_line = any(abs(h - rows[run[0]]['y0']) < 40 for h in hlines)
            aligned = (right_spread < 18 or left_spread < 18)
            if aligned or near_line:
                marked.update(run)
        i = j
    return marked


def locate_display_eqs(page: fitz.Page, band: tuple[float, float]) -> list[fitz.Rect]:
    """定位 display 公式块的 bbox。

    一个 display 公式常被排版器拆成多行（公式主体行 + t 值行 + 式号行），
    例如 eq1 的 `rWML,t = 1.752 - 0.378 rRMRF,t ...` 与
    `(7.93) (-8.72) ... (1)` 是相邻两行。只标主行会让 t 值行被并进
    段落，或让整块被当作段落转写。这里对命中的窄带向下做贪心扩展，
    把紧邻的窄带行/纯数值行并入同一公式块。
    """
    lines = page_lines(page, band)
    if not lines:
        return []
    xs = sorted(l['x0'] for l in lines)
    clusters, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] < 25:
            cur.append(x)
        else:
            clusters.append(cur)
            cur = [x]
    clusters.append(cur)
    best = max(clusters, key=len)
    colw = max(l['x1'] - l['x0'] for l in lines if l['x0'] in best) or page.rect.width
    rows = to_rows(lines)
    table_rows = _table_row_indices(page, band, rows)

    seeds = [i for i, r in enumerate(rows)
             if is_display_equation(r, colw) and i not in table_rows]
    merged: list[list[int]] = []
    used: set[int] = set(table_rows)
    for i in seeds:
        if i in used:
            continue
        grp = [i]
        used.add(i)
        j = i + 1
        while j < len(rows):
            cur_r, nxt = rows[j - 1], rows[j]
            gap = nxt['y0'] - cur_r['y1']
            h = max(cur_r['y1'] - cur_r['y0'], 6)
            if (gap <= h * 0.9
                    and nxt['x1'] - nxt['x0'] < colw * 0.97
                    and not CAPT.match(nxt['t'])
                    and not URLISH.search(nxt['t'])
                    and _is_math_continuation(nxt['t'])):
                grp.append(j)
                used.add(j)
                j += 1
            else:
                break
        merged.append(grp)

    eqs = []
    for grp in merged:
        rs = [rows[i] for i in grp]
        x0 = min(r['x0'] for r in rs) - 3
        x1 = max(r['x1'] for r in rs) + 3
        y0 = min(r['y0'] for r in rs) - 3
        y1 = max(r['y1'] for r in rs) + 3
        eqs.append(fitz.Rect(x0, y0, x1, y1))
    return eqs

# ---------------- 校验（与字体无关，仅用 PDF 字符） ----------------

_NOISE = {'\x00': '', '\ufffd': '', '\u0001': '', '\u0002': '',
          'þ': '+', 'ð': '(', 'ł': 'l', 'Ł': 'L',
          'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi',
          'ﬄ': 'ffl', 'ı': 'i', '\u00ad': '', '\u200b': '', '\ufeff': ''}


def normalize_pdf_text(s: str) -> str:
    for k, v in _NOISE.items():
        s = s.replace(k, v)
    s = re.sub(r'[^\x20-\x7E\u00A0-\uFFFF]', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def _split_md(text: str) -> list[tuple[str, str]]:
    parts, buf, pos = [], [], 0
    for m in re.finditer(r'\$\$.+?\$\$|\$.+?\$|\\\[.+?\\\]|\\\(.*?\\\)',
                         text, re.S):
        seg = text[pos:m.start()]
        if seg.strip():
            buf.append(seg)
        parts.append(('math', m.group(0)))
        pos = m.end()
    tail = text[pos:]
    if tail.strip():
        buf.append(tail)
    if buf:
        parts.insert(0, ('prose', ' '.join(buf)))
    return parts


def _detect_repeat(md: str, size: int = 12) -> int:
    """检测复读：连续 size 个词以上的片段重复出现。"""
    words = re.findall(r"[A-Za-z']+", md.lower())
    n = len(words)
    if n < size * 2:
        return 0
    seen = set()
    rep = 0
    for i in range(0, n - size):
        k = tuple(words[i:i + size])
        if k in seen:
            rep += 1
        seen.add(k)
    return rep


def verify_block(pdf_text: str, md_text: str, is_display: bool = False,
                 trunc_len: int = 1400,
                 exclude_texts: list | None = None) -> dict:
    """块级校验：散文精确率/召回率 + 公式幻觉字母 + 漏公式。
    阈值经注入式灵敏度对照标定（12/12 注入错误全部捕获）。

    trunc_len：截断判定的长度阈值。块级默认 1400；整页/整栏转写要放大
    （页级输出本来就有 2000-7000 字，沿用 1400 会把每页都判成截断，
    导致散文校验被整体跳过）。
    """
    from collections import Counter
    issues = []
    parts = _split_md(md_text)
    md_prose = ' '.join(t for k, t in parts if k == 'prose')
    math_raw = ' '.join(t for k, t in parts if k == 'math')
    n_math = sum(1 for k, _ in parts if k == 'math')
    # URL 里的 = 不是数学信号（"https://ssrn.com/abstract=2041429"）
    scrub = re.sub(r'https?://\S+', ' ', pdf_text)
    scrub = re.sub(r'\S+@\S+', ' ', scrub)

    truncated = (len(md_text) > trunc_len or md_text.count('$') % 2 == 1)
    def toks(s):
        return [w.lower() for w in re.findall(r'[A-Za-z]{2,}', s)]
    pdf_w, md_w = Counter(toks(pdf_text)), Counter(toks(md_prose))
    # 剔除被涂白/截图的图表区域文字：那些内容不进正文（以图片保留），
    # 若不剔除会把含图页判成大面积漏写。
    for et in exclude_texts or []:
        for w, c in Counter(toks(et)).items():
            if pdf_w.get(w, 0) > 0:
                pdf_w[w] = max(0, pdf_w[w] - c)
    inter = sum((pdf_w & md_w).values())
    precision = inter / max(sum(md_w.values()), 1) if md_w else 0.0
    recall = inter / max(sum(pdf_w.values()), 1) if pdf_w else 0.0

    if is_display:
        # display 公式块：不应有散文。只查两件事——
        #  (a) 确实产出了公式
        #  (b) 公式里的字母都能在原文里找到
        # 散文精确率/召回率在此无意义（块内本就没有散文词），
        # 若沿用会把每个正确公式都误判为 NO_PROSE。
        if n_math == 0:
            issues.append({'kind': 'MISSING_DISPLAY',
                           'detail': 'display 公式块未转写出公式'})
        elif not _is_reasoning_leak(md_text):
            stripped = re.sub(r'\\[a-zA-Z]+', ' ', math_raw)
            stripped = re.sub(r'[{}_^$&\\]', ' ', stripped)
            got = Counter(re.findall(r'[A-Za-z]', stripped.lower()))
            have = Counter(re.findall(r'[A-Za-z]', pdf_text.lower()))
            extra = {w: c for w, c in got.items() if c > have.get(w, 0)}
            if extra:
                detail = ', '.join(f'{w}x{c}(原文{have.get(w,0)})'
                                   for w, c in sorted(extra.items())[:6])
                issues.append({'kind': 'HALLUCINATED_SYMBOL',
                               'detail': f'公式含原文没有的字母: {detail}',
                               'math': math_raw[:160]})
        precision = recall = None
        return {'ok': not issues, 'issues': issues,
                'precision': precision, 'recall': recall,
                'n_math': n_math, 'truncated': truncated}
    if truncated:
        precision = recall = None
    else:
        # 短块（标题/关键词/标签，如 'ARTICLE INFO' / 'ABSTRACT'）
        # 不做散文比对：参照文本只有几个词，词频统计噪声极大，
        # 正确转写也会被判 PROSE_MISMATCH。
        short_block = len(pdf_w) < 8
        if not md_w:
            issues.append({'kind': 'NO_PROSE',
                           'detail': '模型输出无任何散文'})
        elif precision < 0.80 and not short_block:
            issues.append({'kind': 'PROSE_HALLUCINATION',
                           'detail': f'模型写了原文没有的词（精确率{precision:.0%}）'})
        # 双栏切分后，栏底/栏顶的段落本来就是被切断的（首词是残词，
        # 尾词在另一栏）。这类块召回率天然偏低，用更宽松的阈值。
        chopped = bool(re.match(r'^[a-z]{2,}\b', pdf_text.strip()))
        need_recall = 0.55 if chopped else 0.72
        if short_block:
            need_recall = 0.0
        if recall < (0.0 if is_display else need_recall):
            lost = sorted(w for w in pdf_w if pdf_w[w] > md_w.get(w, 0))[:12]
            # 保留不足一半且不是栏边残段 -> 内容大量丢失（实测 mhim p3
            # 脚注块只转写了 46%，脚注 4 的正文整段没了）。这类必须
            # 以 critical 报出，不能混在普通召回率提示里。
            severe = (recall < 0.5 and not chopped)
            issues.append({
                'kind': 'PROSE_LOSS' if severe else 'PROSE_MISMATCH',
                'detail': (f'原文词仅保留{recall:.0%}——内容大量漏写'
                           if severe else f'原文词仅保留{recall:.0%}（漏写）'),
                'lost_sample': lost})

    # 公式幻觉：公式里的字母必须在原文出现
    stripped = re.sub(r'\\[a-zA-Z]+', ' ', math_raw)
    stripped = re.sub(r'[{}_^$&\\]', ' ', stripped)
    got = Counter(re.findall(r'[A-Za-z]', stripped.lower()))
    have = Counter(re.findall(r'[A-Za-z]', pdf_text.lower()))
    extra = {w: c for w, c in got.items() if c > have.get(w, 0)}
    if extra:
        detail = ', '.join(f'{w}x{c}(原文{have.get(w,0)})'
                           for w, c in sorted(extra.items())[:6])
        issues.append({'kind': 'HALLUCINATED_SYMBOL',
                       'detail': f'公式含原文没有的字母: {detail}',
                       'math': math_raw[:160]})

    # 思考泄漏优先判定：本地模型有时不直接给转写，而是输出
    # "1. **Analyze the text:** ..." 这类推理过程。推理里会反复引用
    # 同一段原文，若先做复读检测就会被误标成 REPETITION，掩盖真实
    # 根因（输出根本不是转写结果）。
    if _is_reasoning_leak(md_text):
        issues.append({'kind': 'REASONING_LEAK',
                       'detail': '模型输出的是推理过程而非转写结果'})

    # 复读检测：local 模型在长段落上偶发自我复读（实测：
    # 'In uptrend or downtrend phases, such strategies will tend' 连续出现两次）
    rep = 0 if _is_reasoning_leak(md_text) else _detect_repeat(md_text)
    if rep:
        issues.append({'kind': 'REPETITION',
                       'detail': f'输出含 {rep} 处 ≥12 词重复片段（模型复读）'})

    # 漏公式（用去掉 URL 后的文本，避免网址里的 = 造成误报）
    #
    # 「看起来有公式」的判据必须紧。实测过宽的判据会把
    # 'values of 0.13 and 2.00, reaching ... in 2000-02' 这类纯散文
    # 误判成含公式（`s, in 2` 匹配了「字母+逗号+字母+数字」），
    # 每次误报都要占掉一次人工核对。因此要求：
    #   1) 真正的运算符（= ≤ ∑ …），且不是连字符/破折号
    #   2) 或 紧邻的下标记号 r_{i,t} / x_1 / RV_i,t 形态
    # 排除 and/or、he/she 这类普通英文词里的斜杠
    scrub_nw = re.sub(r'\b(?:and|or|he|she|they|we|it)\s*/\s*'
                      r'(?:or|and|he|she|they|we|it)\b', ' ', scrub,
                      flags=re.I)
    looks_math = bool(re.search(r'[=≤≥≈⇒∫∑√∂]|</?[a-z]+>', scrub_nw)) or \
        bool(re.search(
            # 斜杠分数线：记号/记号 或 记号/(表达式)，
            # 两侧都要求短（<=4 字符），避免普通词误中
            r'[A-Za-z]{1,3}[₀-₉a-z,]{1,3}\s*/\s*'
            r'(?:\(?\s*[A-Za-zσ]{1,3}[₀-₉a-z,]{0,3})',
            scrub_nw))
    if is_display and n_math == 0:
        issues.append({'kind': 'MISSING_DISPLAY', 'detail': 'display 公式块未转写出公式'})
    elif not is_display and looks_math and n_math == 0:
        issues.append({'kind': 'MISSING_MATH', 'detail': '原文含数学结构但未转写公式'})

    return {'ok': not issues, 'issues': issues,
            'precision': precision, 'recall': recall,
            'n_math': n_math, 'truncated': truncated}


# ---------------- 转写提示词 ----------------

PARA_SYS = (
    'You are a Markdown transcriber, not a chatbot.\n'
    'You see one image of a paragraph from an academic paper. Reply with '
    'that paragraph in Markdown and nothing else.\n\n'
    'STRICT OUTPUT CONTRACT:\n'
    '- Reproduce ALL prose exactly as printed. Do not summarise, do not '
    'translate, do not add or drop words.\n'
    '- Convert every mathematical expression to LaTeX: inline math in '
    '$...$, display equations in $$...$$.\n'
    '- Preserve all subscripts, superscripts, hats, tildes, fraction bars, '
    'summation limits. Never invent a symbol absent from the image.\n'
    '- Never write words like "the image", "transcribe", "let me", '
    '"I need to", "step 1", "analyze". No preamble, no commentary, '
    'no code fence.\n'
    '- Keep equation numbers as plain text outside the math.')

EQ_SYS = (
    'You are a LaTeX OCR engine, not a chatbot.\n'
    'You see one image containing one displayed equation.\n'
    'Reply with the equation and nothing else.\n\n'
    'STRICT OUTPUT CONTRACT:\n'
    '- First and only line: $$<latex>$$\n'
    '- Never write words like "the image", "the equation", "transcribe", '
    '"let me", "I need to", "step 1", "analyze", "re-examine".\n'
    '- Never explain, never reason, never restate the prompt.\n'
    '- Do not include the equation number inside the math.\n'
    '- Preserve every subscript, superscript, hat, tilde, fraction '
    '(numerator over denominator), summation lower/upper limit, matrix.\n'
    '- If you are unsure of a glyph, still output your best LaTeX guess; '
    'never invent a symbol that is not visible in the image.\n\n'
    'Example input: an image of  a_i = b/c + d\n'
    'Example reply: $$a_i = \\frac{b}{c} + d$$')

REVIEW_SYS = (
    'A previous transcription of this image failed automated verification. '
    'Re-transcribe the image correctly, fixing the listed problems.\n'
    'Never invent symbols absent from the image. Reproduce prose exactly. '
    'Output only the Markdown.')

PAGE_SYS = (
    'You convert one region image of an academic paper into Markdown.\n'
    'The region may be a whole page, one column of a two-column page, '
    'or the footnote area at the bottom of a page.\n'
    'RULES:\n'
    '1. Reproduce ALL text exactly as printed. Do not summarise, do not '
    'translate, do not add or drop words.\n'
    '2. Ignore page headers, footers, page numbers and publisher watermarks.\n'
    '3. If text is rotated 90 degrees, read it as normal text.\n'
    '4. Math: inline in $...$, display in $$...$$. Preserve sub/superscripts, '
    'fractions, summation limits, hats, matrices.\n'
    '5. Figures and tables are blanked out in the image and replaced by '
    'short tokens like [[FIG-1]] or [[TAB-1]] printed in their place. '
    'Reproduce each token EXACTLY as-is, on its own line, at its '
    'position in the text. Do NOT describe or transcribe the '
    'blanked-out content.\n'
    '6. Output ONLY the Markdown. No analysis, no comments, no code fence.')


def _clean_md(s: str) -> str:
    s = s.strip()
    s = re.sub(r'^```(?:markdown|md)?\s*', '', s)
    s = re.sub(r'\s*```$', '', s)
    return s.strip()


_THINK_RE = re.compile(
    r'(the (?:user|image|previous)\b.{0,60}(?:wants|contains|transcribe|transcribed)'
    r'|i need to\b|^let me\b|^first,? i\b|re-?examine|re-?consider'
    r'|the equation is:|step \d'
    r'|extracted text|the image has been rotated)', re.I | re.M)


def _is_reasoning_leak(s: str) -> bool:
    """模型把思考过程当成答案输出（本地模型关不掉思考时会这样）。

    **不要**按长度放行。旧实现有 `if len(s) > 1200: return False`，
    假设"长输出=完整转写"；实测 mhim 附录 B 的泄漏块有 5357 字
    （推理 + 答案混杂），被该守卫放行、以 ok=True 写进了交付物。
    现在的短语集精度足够高（论文正文不会出现"the user wants"这类话）。
    """
    return bool(_THINK_RE.search(s))


def _salvage_math(s: str) -> str:
    """从思考泄漏文本里抢救出仍然定形的 $$...$$（模型常在推理末尾给出结果）。"""
    m = re.findall(r'\$\$(.+?)\$\$', s, re.S)
    if m:
        return '$$' + max(m, key=len).strip() + '$$'
    return ''


_TABLE_MD = re.compile(
    r'\\begin\{(array|tabular|longtable|matrix|bmatrix|pmatrix|'
    r'align|aligned|equation)\*?\}'
    r'|(?:^|\n)\s*\|.*\|\s*$|^\|[\s:|-]{6,}\|')


def _looks_like_table_md(s: str) -> bool:
    """VLM 输出是否是表格（定位器误把表格送进 eq/para 通道时的识别）。
    覆盖三种形态：LaTeX array、markdown 管道行、以及多列数字块。"""
    if _TABLE_MD.search(s):
        return True
    # 连续两行以上以 | 开头 = markdown 表格
    lines = [l for l in s.splitlines() if l.strip()]
    pipe = sum(1 for l in lines if l.strip().startswith('|'))
    if pipe >= 2:
        return True
    return False


# ---------------- 转写引擎（带缓存 + 复核） ----------------

class Transcriber:
    def __init__(self, local: LLM, smart, cache_dir: Path,
                 use_review: bool = True, max_retry: int = 2,
                 local_retry: int = 1):
        self.local = local
        self.smart_pool = smart if isinstance(smart, list) else [smart]
        self.smart_idx = 0
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_review = use_review
        self.max_retry = max_retry
        self.local_retry = local_retry
        self.stats = {'local': 0, 'review': 0, 'cached': 0,
                      'fail': 0, 'llm_seconds': 0.0,
                      'review_failed': 0, 'block_error': 0}

    def _cache_key(self, pdf: str, page: int, kind: str,
                   box: tuple, sys_prompt: str) -> str:
        h = hashlib.sha256()
        h.update(f'{pdf}|{page}|{kind}|{box}|{sys_prompt}'.encode())
        return h.hexdigest()[:24]

    def _cache_get(self, key: str):
        f = self.cache_dir / f'{key}.json'
        if f.exists():
            try:
                return json.loads(f.read_text(encoding='utf-8'))
            except Exception:
                return None
        return None

    def _cache_put(self, key: str, payload: dict):
        (self.cache_dir / f'{key}.json').write_text(
            json.dumps(payload, ensure_ascii=False), encoding='utf-8')

    def review(self, prompt, b64):
        """在复核模型池里轮换调用；全池不可用时抛异常。"""
        last = None
        for _ in range(len(self.smart_pool)):
            llm = self.smart_pool[self.smart_idx % len(self.smart_pool)]
            try:
                txt, dt = llm.chat(prompt[0], prompt[1], b64,
                                   max_tokens=4000, temperature=1.0)
                self.stats['llm_seconds'] += dt
                self.stats['review'] += 1
                self.smart_idx += 1
                return _clean_md(txt), llm.name
            except Exception as e:
                last = e
                self.smart_idx += 1
                self.stats['review_failed'] += 1
        raise RuntimeError(f'复核模型池全部不可用: {last}')

    def transcribe(self, page: fitz.Page, box: fitz.Rect, kind: str,
                   pdf_name: str, page_no: int, dpi: int = 280,
                   salt: str = '', exclude_rects: list | None = None) -> dict:
        """kind ∈ {para, eq, page}。返回 {'md', 'verify', 'source'}。

        page：整页或整栏（页级管线用）。输出长（2-7k 字），
        对应放宽 token 上限与截断判定阈值。
        salt：并入缓存键——页面被涂白/标记后，同一区域的渲染内容会变，
        必须让旧缓存失效。
        exclude_rects：图表区域（已涂白、以图片保留）。其文字从校验
        参照中剔除，否则含图页会被判成大面积漏写。
        """
        if kind == 'eq':
            sys_prompt = EQ_SYS
        elif kind == 'page':
            sys_prompt = PAGE_SYS
        else:
            sys_prompt = PARA_SYS
        mt = 4000 if kind == 'page' else 1600
        tl = 7000 if kind == 'page' else 1400
        b64, _, _ = render_box(page, box, dpi=dpi)
        key = self._cache_key(pdf_name, page_no, kind,
                              (round(box.x0), round(box.y0),
                               round(box.x1), round(box.y1)),
                              sys_prompt + ('|' + salt if salt else ''))
        hit = self._cache_get(key)
        if hit is not None:
            self.stats['cached'] += 1
            return hit
        pdf_text = normalize_pdf_text(text_in_box(page, box))
        excl = [normalize_pdf_text(page.get_text('text', clip=r))
                for r in (exclude_rects or [])]
        is_display = (kind == 'eq')
        # 定位器把独立成行的公式归到了 para 通道（宽度接近栏宽时
        # 达不到"窄带"阈值）。这类块本来就只有公式、没有散文，
        # 若按 para 校验会误报 NO_PROSE。用「参照文本里几乎全是
        # 符号数字」来识别它们。page 类型不做此改判——整页契约里
        # 公式与散文混排是常态。
        if not is_display and kind == 'para':
            letters = sum(c.isalpha() for c in pdf_text)
            if len(pdf_text) >= 8 and letters / len(pdf_text) < 0.55 \
                    and re.search(r'[=∑∫<>≤≥]|\$\s*$', pdf_text):
                is_display = True

        def do(llm: LLM, prompt: tuple, temp: float):
            txt, dt = llm.chat(prompt[0], prompt[1], b64,
                               max_tokens=mt, temperature=temp)
            self.stats['llm_seconds'] += dt
            if llm is self.local:
                self.stats['local'] += 1
            else:
                self.stats['review'] += 1
            return _clean_md(txt)

        md = do(self.local, (sys_prompt, 'Transcribe this to Markdown.'), 0.0)

        # VLM 输出表格结构（array/tabular/markdown 管道行）说明这块其实是
        # 表格而非公式——定位器把表格送进了 eq 通道。这不是错误，
        # 改判为表格、不做公式校验，内容仍以表格形式保留。
        if _looks_like_table_md(md):
            payload = {'md': md, 'verify': {'ok': True, 'issues': [],
                                            'precision': None, 'recall': None,
                                            'n_math': 0, 'truncated': False,
                                            'kind': 'table'},
                       'source': 'local', 'is_table': True}
            self._cache_put(key, payload)
            self.stats['table_blocks'] = self.stats.get('table_blocks', 0) + 1
            return payload

        v = verify_block(pdf_text, md, is_display=is_display, trunc_len=tl,
                         exclude_texts=excl)

        # 本地模型重试：思考泄漏或明显空输出时先自己再试一次
        for _ in range(self.local_retry):
            bad = (not v['ok'] and _is_reasoning_leak(md)) or not md.strip()
            if not bad:
                break
            md = do(self.local, (sys_prompt,
                                 'Output ONLY the transcription. '
                                 'No reasoning, no explanation.'), 0.0)
            v = verify_block(pdf_text, md, is_display=is_display, trunc_len=tl,
                         exclude_texts=excl)

        # 思考泄漏但推理末尾已给出 $$...$$ 结果 -> 抢救
        salvaged_out = False
        if is_display and _is_reasoning_leak(md):
            salvaged = _salvage_math(md)
            if salvaged:
                vs = verify_block(pdf_text, salvaged, is_display=True)
                if vs['ok']:
                    md, v = salvaged, vs
                    salvaged_out = True
                    self.stats['salvaged'] = self.stats.get('salvaged', 0) + 1

        # 本地模型思考泄漏：直接判为需要复核
        leaked = _is_reasoning_leak(md)
        if leaked:
            v['ok'] = False
            v['issues'].append({'kind': 'REASONING_LEAK',
                                'detail': '模型输出了推理过程而非转写结果'})

        # 校验失败 -> smart LLM 带疑点复核
        smart_adopted = False
        if not v['ok'] and self.use_review:
            for attempt in range(self.max_retry):
                hint = '\n'.join(f"- {i['kind']}: {i['detail']}"
                                 for i in v['issues'])
                if v['truncated']:
                    hint += ('\n- TRUNCATED: 你的上一次输出被截断了，'
                             '请只转写图片内容，不要重复或补充任何文字')
                review_prompt = (
                    f'自动校验发现以下问题：\n{hint}\n\n'
                    f'你之前的转写（不可信，仅供对照）：\n{md[:700]}\n\n'
                    f'请依据图片重新完整转写。只输出转写结果本身，'
                    f'不要输出任何思考或解释。')
                # smart 端点可能 500/超时；失败时保留 local 结果并标记，
                # 单块失败绝不能中断整篇转换
                try:
                    md2, who = self.review((REVIEW_SYS, review_prompt), b64)
                except Exception as e:
                    v['issues'].append({'kind': 'REVIEW_FAILED',
                                        'detail': f'复核未完成: {str(e)[:80]}'})
                    break
                v2 = verify_block(pdf_text, md2, is_display=is_display, trunc_len=tl,
                          exclude_texts=excl)
                if _is_reasoning_leak(md2):
                    v2['ok'] = False
                    v2['issues'].append({'kind': 'REASONING_LEAK',
                                         'detail': '复核模型同样输出了推理过程'})
                # 取校验更好的那个
                if _score(v2) > _score(v):
                    md, v = md2, v2
                    smart_adopted = True
                    self.stats['review_by'] = who
                if v['ok']:
                    break

        if not v['ok']:
            self.stats['fail'] += 1
        # source 记录实际被采用的来源（smart 复核成功才用 smart 的）
        if smart_adopted:
            source = 'smart'
        elif salvaged_out:
            source = 'local+salvage'
        else:
            source = 'local'
        payload = {'md': md, 'verify': v, 'source': source}
        self._cache_put(key, payload)
        return payload


def _score(v: dict) -> tuple:
    """校验打分：通过的排前面，其次散文指标高者胜。"""
    p = v.get('precision') if v.get('precision') is not None else 0.5
    r = v.get('recall') if v.get('recall') is not None else 0.5
    return (0 if v['ok'] else 1, -len(v['issues']), p + r, v['n_math'])


# ---------------- 页面编排：段落 + display 公式按 y 交错 ----------------

def _split_long_para(page: fitz.Page, box: fitz.Rect,
                     max_h: float = 185.0, min_h: float = 62.0) -> list[fitz.Rect]:
    """过长的段落按行间隙递归切半。

    local 模型在超长段落上会偶发自我复读，且输出易被 max_tokens 截断。
    阈值取 ~14 行正文高度（实测 190pt 以上的段落开始出现复读/截断）。
    切分必须**均衡**：在最大行间隙处切，若任一半仍超长则递归；
    下限 min_h 防止切出只有一两行的小碎片（那会让每块的召回率校验失真）。
    """
    if box.height <= max_h:
        return [box]
    lines = [l for l in page_lines(page, body_band(page))
             if box.y0 - 2 <= l['y0'] and l['y1'] <= box.y1 + 2]
    if len(lines) < 12:
        return [box]
    best_gap, cut_y = 0.0, None
    for a, b in zip(lines, lines[1:]):
        g = b['y0'] - a['y1']
        # 只在中段附近找切点，避免切出不均衡的两半
        if g > best_gap and box.y0 + box.height * 0.3 < (a['y1'] + b['y0']) / 2 \
                < box.y1 - box.height * 0.3:
            best_gap, cut_y = g, (a['y1'] + b['y0']) / 2
    if cut_y is None:
        return [box]
    # 两个子块之间留 6pt 空隙，**不能重叠**：渲染时两侧各加 5pt padding
    # （见 render_box/text_in_box），若子块边界重叠 4pt（旧实现是
    # cut+2 / cut-2），渲染出的两张图会重叠 14pt——超过一行文字的高度，
    # 边界行在两图中都完整可见，被 VLM 转写两次，产出跨块重复
    # （实测 mhim p1 的致谢脚注因此重复了 25 词）。
    # 留 6pt 空隙后渲染重叠仅 4pt，不足一个字高，边界行只会出现在一侧。
    top = fitz.Rect(box.x0, box.y0, box.x1, cut_y - 3)
    bot = fitz.Rect(box.x0, cut_y + 3, box.x1, box.y1)
    out = []
    for b in (top, bot):
        if b.height < min_h:
            return [box]          # 切出来太小 -> 不切
        out.extend(_split_long_para(page, b, max_h, min_h))
    return out or [box]


def _is_noise_block(page: fitz.Page, box: fitz.Rect, text: str) -> bool:
    """纯页码/页眉页脚残片不值得送 VLM。"""
    t = text.strip()
    if re.fullmatch(r'[\divxlcIVXLC\-–—\s]{1,6}', t):      # 1 / iv / -
        return True
    if len(t) < 12 and not re.search(r'[=<∑∫]', t):      # 极短且无数学
        return True
    # 落在页眉/页脚带
    top, bot = body_band(page)
    if box.y1 <= top + 6 or box.y0 >= bot - 6:
        return True
    return False


def _annotate_overlaps(blocks: list[dict]) -> int:
    """同页内两个转写区域的框显著重叠 -> 内容可能重复。就地标记并返回命中数。

    正常流程下各块区域不会显著重叠：公式区域的行已从段落流中剔除，
    长段落切分产生的子块之间也只在边界共享 ~2pt。若两块重叠超过小框
    面积的一半，说明定位或分栏出了错——实测 mhim p4 曾因单栏页被误判
    为双栏，把行尾碎片聚成"右栏"段落，与正文块重叠并产出重复内容。
    这里是安全网：先修根因，再保证万一其它路径出错也能被报出来。
    """
    n = 0
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            a, b = blocks[i].get('box'), blocks[j].get('box')
            if not a or not b:
                continue
            ra, rb = fitz.Rect(a), fitz.Rect(b)
            inter = ra & rb
            if inter.is_empty:
                continue
            ia = (ra.x1 - ra.x0) * (ra.y1 - ra.y0)
            ib = (rb.x1 - rb.x0) * (rb.y1 - rb.y0)
            si = (inter.x1 - inter.x0) * (inter.y1 - inter.y0)
            small = min(ia, ib)
            if small <= 0 or si / small < 0.5:
                continue
            for me, other in ((blocks[i], blocks[j]), (blocks[j], blocks[i])):
                if 'OVERLAPPING_REGION' in me.get('issues', []):
                    continue
                me.setdefault('issues', []).append('OVERLAPPING_REGION')
                me['ok'] = False
                prev = me.get('detail', '')
                add = (f'转写区域与块 idx{other.get("index", "?")} 重叠 '
                       f'{si / small:.0%}（内容可能重复）')
                me['detail'] = f'{prev}；{add}' if prev else add
                n += 1
    return n


def _dup_words(s: str) -> list[str]:
    """重复检测用的词序列。

    注意**不要**用 `\\$[^$]*\\$` 剥除数学内容：行内公式的定界符在
    跨块拼接后可能不配对，该正则会把第一个 `$` 到很远的下一个 `$`
    之间整段吞掉，导致真实重复被漏检（实测 TimeSeriesMomentum 的
    重复因此计为 0 次）。数学内容里的数字/符号本就不会进入
    `[A-Za-z']+` 词表，只需先去掉 LaTeX 命令名即可。
    """
    s = re.sub(r'\\[a-zA-Z]+', ' ', s or '')
    return re.findall(r"[A-Za-z']+", s.lower())


def _find_duplicate_blocks(blocks: list[dict], min_words: int = 12,
                           pdf_words: list[str] | None = None) -> list[dict]:
    """跨块重复文本检测：同一段 >=N 词的文字出现在多个块里。

    块内复读由 verify_block 的 REPETITION 覆盖；这里抓**跨块**重复——
    区域重叠、切分边界双读、定位错误都可能让同一段文字出现两次
    （实测 mhim p4 的重复块：同段文字既在完整段落里、又单独成块）。
    返回文档级问题列表，进 meta['doc_issues'] 与复核清单。

    为什么用「滑动窗口」而不是「块文本互相包含」：重复往往只是
    其中一段，且两侧还各有独有内容，包含关系抓不到。12 词窗口
    在论文语料里足够罕见，实测无误报。

    pdf_words 给定时用它区分错误类型：论文学术写作本身会重复
    同样的表述（实测 mhim p13 与 p10 两处定义用了同一句话），
    若原文就有 >=2 次，这是**原文特征**不是转换错误，报为
    REPEATED_IN_SOURCE（warn）并说明，避免误导人删掉合法内容。
    """
    from collections import defaultdict
    win: dict[tuple, set] = defaultdict(set)
    for i, b in enumerate(blocks):
        ws = _dup_words(b.get('md') or '')
        for k in range(0, max(0, len(ws) - min_words + 1)):
            win[tuple(ws[k:k + min_words])].add(i)
    pairs: dict[tuple, tuple] = {}
    for w, idxs in win.items():
        if len(idxs) < 2:
            continue
        lst = sorted(idxs)
        for a in range(len(lst)):
            for c in range(a + 1, len(lst)):
                pairs.setdefault((lst[a], lst[c]), w)

    def count_in_pdf(w: tuple) -> int:
        if not pdf_words:
            return 0
        n = len(w)
        return sum(1 for k in range(0, len(pdf_words) - n + 1)
                   if tuple(pdf_words[k:k + n]) == w)

    issues = []
    for (i, j), w in pairs.items():
        bi, bj = blocks[i], blocks[j]
        sample = ' '.join(w)
        bj_ref = f'p{bj.get("page", "?")}/idx{bj.get("index", "?")}'
        from_source = count_in_pdf(w) >= 2
        issues.append({
            'kind': 'REPEATED_IN_SOURCE' if from_source
                    else 'DUPLICATE_CONTENT',
            'detail': (f'与块 {bj_ref} 有 {min_words} 词以上重复，'
                       f'但原文本身即如此（非转换错误，无需删除）'
                       if from_source else
                       f'与块 {bj_ref} 有 {min_words} 词'
                       f'以上重复（两处需人工比对，删除多余的一份）'),
            'pages': [bi.get('page'), bj.get('page')],
            'block': [f'p{bi.get("page", "?")}/idx{bi.get("index", "?")}',
                      bj_ref],
            'sample': sample[:160],
        })
    return issues


def transcribe_page(page: fitz.Page, page_no: int, pdf_name: str,
                    tr: Transcriber, dpi: int = 280) -> list[dict]:
    band = body_band(page)
    lines = page_lines(page, band)
    eqs = locate_display_eqs(page, band)

    # 把 display 公式**行**从段落流中剔除——它们由 VLM 单独转写为 $$ 块。
    # 若不剔除，VLM 会在同一次输出里混合正文与公式，重排时难以对齐。
    # 必须在线->row 之前剔除：双栏论文左右栏同行 y 重叠，若先 to_rows
    # 再剔除，公式行会与另一栏的正文行粘在一起，剔除不干净。
    def covered(line):
        return any(e.y0 - 2 <= line['y0'] and line['y1'] <= e.y1 + 2
                   for e in eqs)
    kept_lines = [l for l in lines if not covered(l)]
    # rows_to_paras 内部会先分栏再聚行（双栏必需）
    paras = rows_to_paras(kept_lines, page.rect.width)

    items = []
    for p in paras:
        txt = normalize_pdf_text(text_in_box(page, p['box']))
        if _is_noise_block(page, p['box'], txt):
            continue
        subs = _split_long_para(page, p['box'])
        for si, sub in enumerate(subs):
            items.append({'y': sub.y0, 'kind': 'para', 'box': sub,
                          'split': (si > 0)})
    items += [{'y': e.y0, 'kind': 'eq', 'box': e, 'split': False}
              for e in eqs]
    items.sort(key=lambda it: it['y'])

    out = []
    for idx, it in enumerate(items):
        try:
            res = tr.transcribe(page, it['box'], it['kind'], pdf_name, page_no,
                               dpi=dpi)
        except Exception as e:
            # 端点故障/渲染异常：记占位，整篇继续
            tr.stats['block_error'] += 1
            out.append({'kind': it['kind'], 'md': '', 'ok': False,
                        'page': page_no + 1, 'source': 'error', 'index': idx,
                        'box': tuple(round(v, 1) for v in it['box']),
                        'detail': f'{type(e).__name__}: {e}'[:200],
                        'issues': ['ERROR']})
            continue
        out.append({'kind': it['kind'], 'md': res['md'],
                    'ok': res['verify']['ok'], 'page': page_no + 1,
                    'source': res['source'],
                    'index': idx,
                    'box': tuple(round(v, 1) for v in it['box']),
                    'split_cont': it.get('split_cont', False),
                    'is_table': res.get('is_table', False),
                    'detail': '; '.join(i.get('detail', '')
                                         for i in res['verify']['issues']),
                    'issues': [i['kind'] for i in res['verify']['issues']]})
    _annotate_overlaps(out)
    return out


# ---------------- 正文范围 / 参考文献 ----------------

BODY_END_RE = re.compile(r'^\s*(references|bibliography)\s*$', re.I)


def detect_body_end(doc: fitz.Document) -> int:
    for pno in range(len(doc)):
        for line in doc[pno].get_text().splitlines():
            if BODY_END_RE.match(line.strip()):
                return pno
    return len(doc)


# ---------------- 人工复核清单 ----------------

# 疑点分级。公式错是不可接受的，散文瑕疵可容忍，所以分级而非一刀切。
#   critical : 公式内容可能错 -> 必须人工看
#   warn     : 内容多半是对的但判为不可信（切分导致的召回率不足等）
#   info     : 已自动处理，不需人工介入
# 分级依据「错了会不会误导读者」：
#   critical — 内容本身可能是错的（公式幻觉、漏公式、模型没给出转写）
#   warn     — 内容多半可用但有瑕疵（复读冗余、召回率不足、截断）
# 公式错不可接受，所以凡涉及公式的疑点一律 critical。
SEVERITY = {
    'HALLUCINATED_SYMBOL': ('critical', '公式含原文没有的字母——可能是幻觉符号'),
    'MISSING_DISPLAY': ('critical', 'display 公式块没转写出公式'),
    'MISSING_MATH': ('critical', '原文有数学结构，模型未输出公式'),
    'PROSE_HALLUCINATION': ('critical', '模型写了原文没有的词'),
    'REASONING_LEAK': ('critical', '模型输出的是推理过程而非转写结果'),
    'ERROR': ('critical', '转写调用失败'),
    'OVERLAPPING_REGION': ('critical', '两个转写区域框重叠，内容可能重复'),
    'DUPLICATE_CONTENT': ('critical', '同一段文字出现在多个块中（内容重复）'),
    'REPETITION': ('warn', '输出含长片段重复（模型复读，内容冗余）'),
    'REVIEW_FAILED': ('warn', '复核未完成（端点限流/故障）'),
    'TRUNCATED_OUTPUT': ('warn', '输出被 max_tokens 截断'),
    'PROSE_MISMATCH': ('warn', '原文词召回率偏低，可能漏写'),
    'PROSE_LOSS': ('critical', '原文词保留不足一半——内容大量漏写'),
    'REPEATED_IN_SOURCE': ('warn', '原文本身即重复该片段（非转换错误）'),
    'NO_PROSE': ('warn', '输出中没有散文'),
    'SPURIOUS_MATH': ('warn', '原文无数学结构却输出了公式'),
}
SEVERITY_ORDER = {'critical': 0, 'warn': 1, 'info': 2}


def build_review_report(pdf_path: Path, out_dir: Path, meta: dict,
                       page_boxes: dict) -> Path | None:
    """生成 review.md：逐块列出存疑项，含原图裁切 + 模型输出 + 疑点。

    人只在两种情况下需要看它：
      1. critical 项——公式可能错，必须人工核对
      2. 想知道某块为什么被判不可信
    因此报告要能让人**不打开原 PDF 就完成核对**：裁切图与模型输出并排。

    返回 None 表示没有存疑项也没有文档级异常，不产出报告。
    """
    flagged = []
    for p in meta.get('pages_detail', []):
        for it in p.get('items', []):
            if it.get('ok'):
                continue
            flagged.append((p['page'], it))
    doc_issues = meta.get('doc_issues') or []
    if not flagged and not doc_issues:
        return None

    doc = fitz.open(pdf_path)
    shots_dir = out_dir / 'review_shots'
    shots_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f'# 人工复核清单 — {pdf_path.name}',
        '',
        f'- 正文页数：{meta.get("body_end_page")}',
        f'- 总块数：{sum(len(p["items"]) for p in meta["pages_detail"])}',
        f'- 存疑块：{len(flagged)}',
        f'- 文档级异常：{len(doc_issues)}',
        '',
    ]
    n_crit = sum(1 for _, it in flagged
                 if any(SEVERITY.get(i, ('warn', ''))[0] == 'critical'
                        for i in it.get('issues', [])))
    n_doc_crit = sum(1 for d in doc_issues
                     if SEVERITY.get(d.get('kind', ''), ('warn', ''))[0]
                     == 'critical')
    lines += [
        f'**其中 {n_crit + n_doc_crit} 项涉及内容正确性（critical），必须人工核对；**',
        f'其余 {len(flagged) - n_crit} 块多为切分导致的召回率不足，内容多半无误。',
        '',
    ]
    # 文档级异常（跨块重复等）优先展示：它们不绑定单个块，
    # 但会直接影响最终 md 的正确性（重复内容）。
    if doc_issues:
        lines += ['## 文档级异常', '']
        for d in doc_issues:
            lvl, desc = SEVERITY.get(d.get('kind', ''), ('warn', ''))
            lines.append(f'- **{d.get("kind")}**（{lvl}）{desc}')
            lines.append(f'  - {d.get("detail", "")}')
            if d.get('sample'):
                lines.append(f'  - 重复片段：`{d["sample"]}`')
        lines += ['', '---', '']
    lines += [
        '每项给出：原图裁切（`review_shots/`）、模型实际输出、自动检出的疑点。',
        '核对方法：看图里的公式，与下方 LaTeX 逐项对照。',
        '',
    ]

    order = {'critical': 0, 'warn': 1}
    flagged.sort(key=lambda t: (
        order.get(max((SEVERITY.get(i, ('warn', ''))[0]
                       for i in t[1].get('issues', [])), default='warn')),
        t[0]))

    for n, (page, it) in enumerate(flagged, 1):
        box = page_boxes.get((page, it['index']))
        shot = ''
        if box is not None:
            try:
                p = doc[page - 1]
                pix = p.get_pixmap(clip=fitz.Rect(box) & p.rect, dpi=200)
                fn = f'review_shots/p{page:03d}_{it["index"]:03d}.png'
                pix.save(str(out_dir / fn))
                shot = fn
            except Exception:
                shot = ''
        crit = any(SEVERITY.get(i, ('warn', ''))[0] == 'critical'
                   for i in it.get('issues', []))
        lines += [
            f'## {n}. p{page} · {"`" + it["kind"] + "`"} · '
            f'{"**CRITICAL**" if crit else "warn"}',
            '',
        ]
        if shot:
            lines += [f'![p{page} 块{it["index"]}]({shot})', '']
        for iss in it.get('issues', []):
            lvl, desc = SEVERITY.get(iss, ('warn', iss))
            lines.append(f'- `{iss}`（{lvl}）{desc}')
        if it.get('detail'):
            lines.append(f'- 详情：{it["detail"]}')
        lines += [
            f'- 复核来源：{it.get("source", "?")}',
            '',
            '模型输出：',
            '',
            '```markdown',
            (it.get('md') or '(空)').strip()[:1200],
            '```',
            '',
            '---',
            '',
        ]

    rep = out_dir / 'review.md'
    rep.write_text('\n'.join(lines), encoding='utf-8')
    return rep


# ---------------- 主入口 ----------------

def extract_media(doc: fitz.Document, body_end: int,
                  out_dir: Path) -> dict:
    """表格 + 图 + 链接清单。

    表格与图走几何抽取（`tables_figures.py`）。该模块缺失时**显式报错**，
    不静默返回空——否则调用方会误以为「这篇论文没有表/图」，
    而实际是没装依赖，会静默丢内容。
    """
    res = {'tables': {}, 'figures': {}, 'links': []}
    if geometry is None:
        raise RuntimeError(
            '缺少 tables_figures.py，无法抽取表格/图。'
            '请确保它与 pdf2md.py 在同一目录。'
            f'（原始错误：{_GEOMETRY_ERR}）')
    # 表格：逐页抽取（表格可能内联在正文中）
    for pno in range(len(doc)):
        try:
            for t in geometry.extract_tables_page(doc[pno]):
                res['tables'].setdefault(f"T{t['num']}", {**t, 'page': pno + 1})
        except Exception:
            continue
    # 图：整页渲染 caption 上方区域
    assets = out_dir / 'assets'
    fig_pages = []
    for pno in range(len(doc)):
        page = doc[pno]
        has_cap = any(geometry.CAPTION_RE.match(l.strip())
                      and re.match(r'\s*Fig', l.strip(), re.I)
                      for l in page.get_text().splitlines())
        if has_cap and (page.get_images() or page.get_drawings()):
            fig_pages.append(pno)
    try:
        res['figures'] = geometry.extract_figures(doc, fig_pages, assets)
    except Exception:
        pass
    # 链接
    seen = set()
    for pno in range(len(doc)):
        for l in doc[pno].get_links():
            uri = l.get('uri')
            if uri and uri not in seen:
                seen.add(uri)
                res['links'].append(uri)
    return res


def inline_media(text: str, media: dict) -> str:
    """把文末汇总的表/图以 markdown 形式附在正文后，并给出链接清单。"""
    tail: list[str] = ['', '---', '', '## Tables and Figures', '']
    any_media = False
    for k in sorted(media['tables'], key=lambda s: int(s[1:])):
        try:
            tail.append(geometry.table_to_markdown(media['tables'][k]))
            tail.append('')
            any_media = True
        except Exception:
            continue
    for k in sorted(media['figures'], key=lambda s: int(s[1:])):
        f = media['figures'][k]
        tail.append(f"![Fig. {k[1:]}](assets/{f['file']})")
        tail.append('')
        tail.append(f"*{f.get('caption', '')}*")
        tail.append('')
        any_media = True
    if media['links']:
        tail.append('')
        tail.append('## Links')
        tail.append('')
        for u in media['links']:
            tail.append(f'- <{u}>')
        tail.append('')
    if not any_media and not media['links']:
        return text
    return text + '\n' + '\n'.join(tail).rstrip() + '\n'


def convert(pdf_path: Path, out_dir: Path, local: LLM, smart,
            max_pages: int | None = None, dpi: int = 280,
            use_review: bool = True, quiet: bool = False) -> dict:
    doc = fitz.open(pdf_path)
    body_end = detect_body_end(doc)
    if max_pages:
        body_end = min(body_end, max_pages)
    cache = out_dir / '.vlm_cache'
    tr = Transcriber(local, smart, cache, use_review=use_review)

    md_parts: list[str] = []
    kinds: list[str] = []
    per_page = []
    for pno in range(body_end):
        page = doc[pno]
        items = transcribe_page(page, pno, pdf_path.name, tr, dpi=dpi)
        per_page.append({'page': pno + 1, 'items': items})
        # 同一段被纵向切开的连续块：直接首尾相接（不加空行），
        # 否则会引入原文不存在的段落边界。误判为表格的块转写为
        # markdown 表格并保留（它仍是有价值的内容）。
        buf = None
        for it in items:
            if not it['md'].strip():
                buf = None
                continue
            if it.get('split_cont'):
                if buf is not None:
                    buf['md'] = buf['md'].rstrip() + ' ' + it['md'].lstrip()
                    buf['split_cont'] = it.get('split_cont', False)
                    continue
            if buf is not None:
                md_parts.append(buf['md'])
                kinds.append(buf['kind'])
            buf = {'md': it['md'], 'kind': it['kind'],
                   'split_cont': it.get('split_cont', False)}
        if buf is not None:
            md_parts.append(buf['md'])
            kinds.append(buf['kind'])
        if not quiet:
            ok = sum(1 for x in items if x['ok'])
            print(f'  p{pno+1}: {len(items)} 块, 校验通过 {ok}')

    text = '\n\n'.join(md_parts)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 跨页续接：上一页末块未以句末标点结束、下一页首块非标题/非公式时，
    # 两块实为同一段被分页切断，合并（否则读者看到断裂的句子）
    text = _join_page_breaks(text, kinds)
    out_dir.mkdir(parents=True, exist_ok=True)
    media = extract_media(doc, body_end, out_dir)
    text = inline_media(text, media)
    (out_dir / 'paper.md').write_text(text + '\n', encoding='utf-8')

    meta = {'source': pdf_path.name, 'pages': len(doc),
            'body_end_page': body_end, 'dpi': dpi,
            'stats': tr.stats,
            'media': {'tables': sorted(media['tables']),
                      'figures': sorted(media['figures']),
                      'links': len(media['links'])},
            'pages_detail': per_page}
    # 文档级检测：跨块重复文本（区域重叠、切分边界双读、定位错误都会导致）。
    # 这类错误直接反映在最终 md 里，必须在交付前报出来。
    # 同时用 PDF 原文词表区分「原文本身重复」与「转换产生的重复」。
    all_blocks = [it for p in per_page for it in p['items']]
    pdf_all = ' '.join(doc[p].get_text() for p in range(body_end))
    meta['doc_issues'] = _find_duplicate_blocks(
        all_blocks, pdf_words=_dup_words(pdf_all))
    n_conv = sum(1 for d in meta['doc_issues']
                 if d['kind'] == 'DUPLICATE_CONTENT')
    n_src = len(meta['doc_issues']) - n_conv
    if meta['doc_issues'] and not quiet:
        print(f'[warn] 文档级重复检查：{n_conv} 处转换产生（需处理），'
              f'{n_src} 处原文本身重复（无需处理）')
    (out_dir / 'meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    # 人工复核清单：只列存疑块，并按严重程度排序。
    # 公式错不可接受，所以 critical 项必须在报告最前面。
    page_boxes = {(p['page'], it['index']): it.get('box')
                  for p in per_page for it in p['items']
                  if it.get('box')}
    meta['review_report'] = None
    try:
        rep = build_review_report(pdf_path, out_dir, meta, page_boxes)
        if rep:
            n_crit = sum(1 for p in per_page for it in p['items']
                         if not it['ok'] and any(
                             SEVERITY.get(i, ('warn', ''))[0] == 'critical'
                             for i in it['issues']))
            n_warn = sum(1 for p in per_page for it in p['items']
                         if not it['ok']) - n_crit
            doc_issues = meta['doc_issues']
            n_doc_crit = sum(1 for d in doc_issues
                             if SEVERITY.get(d.get('kind', ''),
                                             ('warn', ''))[0] == 'critical')
            n_doc_warn = len(doc_issues) - n_doc_crit
            meta['review_report'] = str(rep)
            meta['review_counts'] = {'critical': n_crit + n_doc_crit,
                                     'warn': n_warn + n_doc_warn,
                                     'doc': len(doc_issues)}
            (out_dir / 'meta.json').write_text(
                json.dumps(meta, ensure_ascii=False, indent=2),
                encoding='utf-8')
            if not quiet:
                print(f'[review] {rep.name}: {n_crit + n_doc_crit} 项需人工核对'
                      f'（critical）, {n_warn + n_doc_warn} 项提示')
    except Exception as e:
        if not quiet:
            print(f'[warn] 复核清单生成失败: {type(e).__name__}: {e}')
    return meta


_HEAD_RE = re.compile(r'^(\|?\s*(#|Table|Figure|Fig\.|Panel)|\d+\.\s|Notes?:)')


def _join_page_breaks(text: str, kinds: list[str]) -> str:
    """合并被分页切断的同一段落。只合并 段落↔段落，公式块不参与。

    脚注块不参与合并：页底脚注常常未完（输出截断在标记处，如 `<sup>4</sup`），
    若按「未完句 + 下段小写开头」规则合并，会把它与下一页正文缝在一起
    （实测 mhim：`<sup>4</sup three months. Even the large returns...`）。
    """
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    pkinds = [k for k, p in zip(kinds, paras) if p]
    out, out_kind = [], []
    for i, p in enumerate(paras):
        kind = pkinds[i] if i < len(pkinds) else 'para'
        if out and kind == 'para' and out_kind[-1] == 'para':
            prev = out[-1]
            prev_unfinished = not prev.rstrip().endswith(
                ('.', '!', '?', ':', ';', ')', ']', '}', '"', '’'))
            cur_starts_mid = (p[0].islower() or p[0] in ',;)' or
                              bool(re.match(r'^[a-z]\b', p)))
            # 上一块是脚注（以 <sup>N</sup> / ^N / "N 文本" 开头）则不合并
            prev_is_footnote = bool(re.match(
                r'^\s*(<sup>|\^|\[\^|\d{1,3}\s+[A-Z(])', prev))
            if (prev_unfinished and cur_starts_mid
                    and not prev_is_footnote and not _HEAD_RE.match(p)):
                out[-1] = prev + ' ' + p
                continue
        out.append(p)
        out_kind.append(kind)
    return '\n\n'.join(out)


def build_clients(env: dict, local_model: str | None = None,
                  smart_model: str | None = None) -> tuple[LLM, LLM]:
    local = LLM(env['LLM_LOCAL_URL'], env['LLM_LOCAL_API_KEY'],
                local_model or env.get('LLM_LOCAL', ''), 'local')
    smart = LLM(env['LLM_SMART_URL'], env['LLM_SMART_API_KEY'],
                smart_model or env.get('LLM_SMART', ''), 'smart')
    return local, smart


def build_smart_pool(env: dict, primary: str | None = None) -> list[LLM]:
    """复核模型池。主模型被限流（429）时自动换用备选。

    实测：deepseek-v4.1-flash / kimi-k3 在连续调用后返回 429，
    mimo-v2.6-flash / space-bunny 仍可用——复核链路不能因单点限流而失效。

    备选顺序取自配置 SMART_FALLBACKS（逗号分隔）；未配置时用内置默认值，
    那些是实测可用的模型名，换环境时按需覆盖。
    """
    url = env['LLM_SMART_URL']
    key = env['LLM_SMART_API_KEY']
    fb = env.get('SMART_FALLBACKS', '').strip()
    if fb:
        extra = [x.strip() for x in fb.split(',') if x.strip()]
    else:
        extra = ['mimo-v2.6-flash', 'space-bunny', 'kimi-k3']
    names = [primary or env.get('LLM_SMART', '')] + extra
    seen, out = set(), []
    for n in names:
        if n and n not in seen:
            seen.add(n)
            out.append(LLM(url, key, n, f'smart:{n}'))
    return out


def find_env_file(explicit: Path | None = None) -> Path:
    """定位配置文件：显式指定 > 同目录 `pdf2md.env` > 同目录 `.env`。

    只认本目录，不向上遍历仓库根——那会让配置来源变得不可预测
    （同一份代码在不同 cwd 下读到不同的 .env）。
    要用别的配置就显式传 --env 或设 PDF2MD_ENV。
    """
    if explicit:
        return explicit
    from_env = os.environ.get('PDF2MD_ENV')
    if from_env:
        return Path(from_env)
    here = Path(__file__).resolve().parent
    for name in ('pdf2md.env', '.env'):
        cand = here / name
        if cand.exists():
            return cand
    return here / '.env'


def review_from_meta(pdf_path: Path, out_dir: Path) -> int:
    """仅从已有 meta.json 重新生成复核清单（不调用任何 LLM）。

    用于：改了 SEVERITY 分级或报告格式后重出报告；或者事后想再核对一遍。
    """
    mf = out_dir / 'meta.json'
    if not mf.exists():
        print(f'[error] 找不到 {mf}，请先跑一次转换')
        return 2
    meta = json.loads(mf.read_text(encoding='utf-8'))
    page_boxes = {(p['page'], it['index']): it.get('box')
                  for p in meta.get('pages_detail', [])
                  for it in p['items'] if it.get('box')}
    rep = build_review_report(pdf_path, out_dir, meta, page_boxes)
    if not rep:
        print('  ✓ 无存疑块')
        return 0
    n_crit = sum(1 for p in meta.get('pages_detail', [])
                 for it in p['items'] if not it['ok'] and any(
                     SEVERITY.get(i, ('warn', ''))[0] == 'critical'
                     for i in it['issues']))
    print(f'[ok] {rep}  (critical {n_crit})')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description='PDF -> 高保真 Markdown（视觉转写 + 校验 + 复核）')
    ap.add_argument('pdf', type=Path)
    ap.add_argument('-o', '--out', type=Path, required=True)
    ap.add_argument('--max-pages', type=int, default=None)
    ap.add_argument('--dpi', type=int, default=280)
    ap.add_argument('--local-model', default=None)
    ap.add_argument('--smart-model', default=None)
    ap.add_argument('--no-review', action='store_true',
                    help='禁用 smart LLM 复核（仅用 local）')
    ap.add_argument('--env', type=Path, default=None,
                    help='配置文件路径（默认读同目录的 pdf2md.env 或 .env，'
                         '也可用环境变量 PDF2MD_ENV 指定）')
    ap.add_argument('--review-only', action='store_true',
                    help='不跑转换，仅从已有 meta.json 重新生成复核清单')
    args = ap.parse_args()

    if args.review_only:
        # 不需要任何配置或端点
        if geometry is None:
            print('[error] 缺少 tables_figures.py，无法裁切原图。')
            return 3
        return review_from_meta(args.pdf, args.out)

    env_path = find_env_file(args.env)
    env = load_env(str(env_path))
    if not env:
        print(f'[error] 未读到配置：{env_path}')
        print('        可放同目录的 pdf2md.env，或用 --env / PDF2MD_ENV 指定')
        print('        需要 LLM_LOCAL_URL / LLM_LOCAL_API_KEY / LLM_LOCAL /')
        print('        LLM_SMART_URL / LLM_SMART_API_KEY / LLM_SMART')
        return 2
    for k in ('LLM_LOCAL_URL', 'LLM_LOCAL_API_KEY', 'LLM_LOCAL',
              'LLM_SMART_URL', 'LLM_SMART_API_KEY', 'LLM_SMART'):
        if k not in env:
            print(f'[warn] .env 缺少 {k}')
    # 前置检查依赖：正文转写要跑十几分钟，不能等全部做完才发现
    # 表格/图模块缺失——那样白转一遍且没有产物落盘。
    if geometry is None:
        print('[error] 缺少 tables_figures.py（表格/图抽取依赖）。')
        print(f'        请把它与 pdf2md.py 放在同一目录。'
              f'（原始错误：{_GEOMETRY_ERR}）')
        return 3
    local, smart = build_clients(env, args.local_model, args.smart_model)
    smart_pool = build_smart_pool(env, args.smart_model)
    print(f'[cfg] local={local.model} dpi={args.dpi}')
    print('[cfg] 复核池: ' + ', '.join(m.model for m in smart_pool))
    meta = convert(args.pdf, args.out, local, smart_pool,
                   max_pages=args.max_pages, dpi=args.dpi,
                   use_review=not args.no_review)
    s = meta['stats']
    n_blocks = sum(len(p['items']) for p in meta['pages_detail'])
    print(f'[ok] {args.out / "paper.md"}')
    print(f'  正文页 {meta["body_end_page"]} 页, 共 {n_blocks} 块')
    print(f'  local={s["local"]} smart复核={s["review"]} '
          f'缓存命中={s["cached"]} 校验未过={s["fail"]}')
    print(f'  LLM 累计 {s["llm_seconds"] / 60:.1f} 分钟')

    rc = meta.get('review_counts')
    if meta.get('review_report'):
        rep = Path(meta['review_report'])
        print()
        print(f'  ⚠ 需人工复核：{rc["critical"]} 项涉及内容正确性（必须核对）'
              f' + {rc["warn"]} 项提示')
        print(f'    {rep}')
        print('    报告内每项都附了原图裁切，逐项对照即可，无需打开原 PDF。')
        if rc['critical']:
            print('    ⚠ 公式/内容不能错——请优先核对 critical 项。')
    else:
        print('  ✓ 无存疑块，未生成复核清单')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
