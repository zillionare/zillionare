#!/usr/bin/env python3
"""图文合流：将工作论文版译文中的占位符替换为文末对应图表的截图。

原理：
  工作论文版（SSRN/NBER）在正文留 [Insert Fig.X here] 占位符，图表集中在文末。
  本脚本按图表编号配对，把文末图表渲染成图片，插入到占位符所在页，
  生成一份"图文合流版" PDF（zh-flow.pdf），阅读体验接近正式出版版。

  译文 zh.pdf 保持原样（忠实原文）；合流版是增值交付物。

用法:
  python3 tools/merge_figures.py <译文zh.pdf> <原文en.pdf> -o <输出.pdf>

  原文用于定位文末图表的精确区域（矢量绘图边界），译文用于定位占位符。
  要求原文与译文页数一致（pdf2zh 保证）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import fitz
from PIL import Image

# 占位符：方括号内同时含"图/表/Fig/Table+数字"与"插入/放入/Insert/附近/将"即认定
# 覆盖 [在此处插入图4] [将表3插入此处] 【请在此处插入图1】 [Insert Fig. 2 here]
PLACEHOLDER_RE = re.compile(
    r'[\[【](?=[^\]】]*(?:Fig\.?|Table|图|表)\s*[0-9]+)'
    r'[^\]】]*(?:插入|放入|Insert|附近|将)[^\]】]*'
    r'(?:Fig\.?|Table|图|表)\s*([0-9]+)[^\]】]*[\]】]',
    re.IGNORECASE,
)
# 文末图表标题：Fig. 4. / Table 3 / 图4 / 表3（行首）
CAPTION_RE = re.compile(r'^\s*(Fig\.?|Table|图|表)\s*([0-9]+)\b', re.IGNORECASE)


def find_placeholders(doc: fitz.Document) -> dict[str, list[int]]:
    """返回 {图表编号: [页码...]}，编号形如 F4 / T3。"""
    out: dict[str, list[int]] = {}
    for pno in range(len(doc)):
        for m in PLACEHOLDER_RE.finditer(doc[pno].get_text()):
            kind = 'F' if m.group(0).lower().find('fig') >= 0 or '图' in m.group(0) else 'T'
            # 更稳：看编号前的词
            pre = m.group(0)
            if re.search(r'Fig|图', pre, re.IGNORECASE):
                kind = 'F'
            else:
                kind = 'T'
            key = f'{kind}{m.group(1)}'
            out.setdefault(key, []).append(pno)
    return out


def find_figure_pages(doc: fitz.Document) -> dict[str, int]:
    """在文末区域找图表标题，返回 {编号: 页码}。只看后 1/3 页面。"""
    out: dict[str, int] = {}
    start = len(doc) * 2 // 3
    for pno in range(start, len(doc)):
        for line in doc[pno].get_text().splitlines():
            m = CAPTION_RE.match(line.strip())
            if m:
                kind = 'F' if m.group(1).lower().startswith('fig') or m.group(1) == '图' else 'T'
                key = f'{kind}{m.group(2)}'
                out.setdefault(key, pno)
    return out


def figure_clip(page: fitz.Page) -> fitz.Rect:
    """取页面矢量绘图的并集作为图表区域；无绘图则取整页。"""
    rect = None
    for d in page.get_drawings():
        r = d['rect']
        if r.width < 15 or r.height < 10:
            continue
        rect = r if rect is None else rect | r
    if rect is None:
        return page.rect
    # 排除页眉页脚
    rect.y0 = max(rect.y0 - 6, 0)
    rect.y1 = min(rect.y1 + 6, page.rect.y1 - 30)
    return rect & page.rect


def render_clip(page: fitz.Page, clip: fitz.Rect, scale: float = 2.0) -> Image.Image:
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def main() -> int:
    ap = argparse.ArgumentParser(description='图文合流：占位符处插入文末图表')
    ap.add_argument('zh_pdf', type=Path, help='译文 PDF')
    ap.add_argument('en_pdf', type=Path, help='原文 PDF（定位图表区域）')
    ap.add_argument('-o', '--output', type=Path, required=True)
    ap.add_argument('--scale', type=float, default=2.0)
    args = ap.parse_args()

    zh = fitz.open(args.zh_pdf)
    en = fitz.open(args.en_pdf)
    if len(zh) != len(en):
        print(f'[warn] 页数不一致: 译文 {len(zh)} vs 原文 {len(en)}，按译文页码处理')

    placeholders = find_placeholders(zh)
    fig_pages = find_figure_pages(en)
    print(f'占位符: {sorted(placeholders)}')
    print(f'文末图表: {sorted(fig_pages)}')

    # 配对
    pairs = []
    for key, pages in sorted(placeholders.items()):
        if key in fig_pages:
            pairs.append((key, pages[0], fig_pages[key]))
        else:
            print(f'[warn] {key} 在文末未找到对应图表，跳过')
    if not pairs:
        print('[fail] 无配对，退出')
        return 1

    # 渲染文末图表
    inserts: dict[int, list[Image.Image]] = {}
    for key, ph_page, fig_page in pairs:
        clip = figure_clip(en[fig_page])
        img = render_clip(en[fig_page], clip, args.scale)
        inserts.setdefault(ph_page, []).append((key, img))
        print(f'  {key}: 占位符p{ph_page + 1} <- 文末p{fig_page + 1} ({img.width}x{img.height})')

    # 生成合流版：在占位符页后插入图表页
    out = fitz.open()
    for pno in range(len(zh)):
        out.insert_pdf(zh, from_page=pno, to_page=pno)
        if pno in inserts:
            for key, img in inserts[pno]:
                # 按图片比例建新页（A4 宽 595pt）
                w_pt = 595.0
                h_pt = w_pt * img.height / img.width
                page = out.new_page(width=w_pt, height=h_pt + 36)
                page.insert_text((36, 24), f'[{key[0] == "F" and "图" or "表"} {int(key[1:])}（原文文末图表，移至此处）]',
                                 fontsize=9, color=(0.5, 0.5, 0.5))
                import io
                buf = io.BytesIO()
                # 图表多为线条图，JPEG quality 85 体积小且清晰
                img.convert('RGB').save(buf, format='JPEG', quality=85)
                page.insert_image(fitz.Rect(24, 30, w_pt - 24, 30 + h_pt - 12), stream=buf.getvalue())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output)
    print(f'[ok] {args.output} 共 {len(out)} 页（原文 {len(zh)} 页 + {len(out) - len(zh)} 页图表）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
