#!/usr/bin/env python3
"""从论文 PDF 提取翻译所需的素材。

产出（每篇论文一个子目录）:
  pages/page_001.md     分页纯文本（供翻译）
  figures/*.png         图表区域截图（不翻译，直接嵌入）
  figures/index.json    图表索引（编号、标题、页码、裁剪框）
  meta.json             论文元信息

图表为矢量绘制，无法提取内嵌图片。策略：
1. 识别真实图表标题行（Figure/Table/Fig./Exhibit + 编号），过滤正文假阳性
2. 按方向启发式取区域（图在标题上方、表在标题下方），并并入相交的矢量图形簇
3. 高分辨率渲染后按像素自动裁掉空白边，得到紧凑截图
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import fitz

CAPTION_RE = re.compile(
    r"^\s*(Figure|Fig\.|Table|Exhibit)\s+([0-9]+[.:]?|[IVX]+[.:]?)\s*(.*)$",
    re.IGNORECASE,
)
# 出现在正文句子里的动词/短语——命中则说明整行是正文引用而非标题
SENTENCE_HINTS = re.compile(
    r"\b(illustrat\w*|examin\w*|map\w*|show\w*|include\w*|present\w*|report\w*|"
    r"display\w*|indicat\w*|summariz\w*|summaris\w*|contain\w*|provid\w*|depict\w*|"
    r"plot\w*|list\w*|document\w*|confirm\w*|reveal\w*|compar\w*|measur\w*|"
    r"tabulate\w*|plot\w*|plot\w*|we|our|us\b|which|that|from the|of the|in the|"
    r"is|are|was|were|can be)\b",
    re.IGNORECASE,
)
CONT_MAX_GAP = 14


def _lines_of(page: fitz.Page) -> list[tuple[dict, str]]:
    rows: list[tuple[dict, str]] = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for line in b["lines"]:
            rows.append((line, "".join(s["text"] for s in line["spans"]).strip()))
    rows.sort(key=lambda r: (r[0]["bbox"][1], r[0]["bbox"][0]))
    return rows


def find_captions(page: fitz.Page) -> list[dict]:
    """真实图表标题行：Figure/Table + 编号，且整行不构成正文句子。"""
    rows = _lines_of(page)
    captions = []
    for i, (line, text) in enumerate(rows):
        m = CAPTION_RE.match(text)
        if not m:
            continue
        rest = m.group(3) or ""
        # 真标题形如 "Fig. 1. U.S. stock market cycles."（编号后 . 或 : 加大写/数字）
        looks_like_title = bool(re.match(r"^[.:]\s+[A-Z0-9]", rest))
        if not looks_like_title and re.match(r"^[a-z]", rest):
            continue  # 编号后直接跟小写单词 = 正文句，如 "Table 3 decomposes..."
        if not looks_like_title and SENTENCE_HINTS.search(text):
            continue  # 正文引用，如 "Figure 1 presents the cumulative..."
        full = text
        j = i + 1
        while j < len(rows) and rows[j][0]["bbox"][1] - line["bbox"][3] < CONT_MAX_GAP:
            nxt = rows[j][1]
            if not nxt or CAPTION_RE.match(nxt) or len(nxt) > 90:
                break
            if "%" in nxt or re.search(r"\(\s*-?\d", nxt) or re.match(r"^\(?\d", nxt):
                break  # 数据行，不是标题续行
            full += " " + nxt
            j += 1
        if len(full) > 300:
            continue
        if re.search(r"\b(continued|cont\.)\b", full, re.IGNORECASE):
            continue  # 跨页续表并入首页截图，不单独出图
        kind = "table" if m.group(1).lower().startswith("table") else "figure"
        captions.append({"bbox": list(line["bbox"]), "text": full, "kind": kind})
    return captions


def graphic_bands(page: fitz.Page) -> list[fitz.Rect]:
    """页面上成规模的矢量图形并集（用于并入图表区域）。"""
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 15 or r.height < 10:
            continue
        if r.width > page.rect.width * 0.85 and r.height < 3:
            continue
        rects.append(r)
    if not rects:
        return []
    rects.sort(key=lambda x: (x.y0, x.x0))
    clusters: list[fitz.Rect] = []
    for r in rects:
        for c in clusters:
            if r.x0 < c.x1 + 45 and r.x1 > c.x0 - 45 and r.y0 < c.y1 + 45 and r.y1 > c.y0 - 45:
                c |= r
                break
        else:
            clusters.append(fitz.Rect(r))
    return [c for c in clusters if c.width * c.height > 1500]


def column_bounds(page: fitz.Page, y0: float, y1: float, cb: fitz.Rect) -> tuple[float, float]:
    """估计标题行所在栏的水平范围，用于给无矢量图形的纯文本表格定宽。"""
    mid = page.rect.width / 2
    cb_mid = (cb.x0 + cb.x1) / 2
    left_col = cb_mid < mid
    xs0, xs1 = [], []
    for line, _ in _lines_of(page):
        x0, ly0, x1, ly1 = line["bbox"]
        if ly1 < y0 - 5 or ly0 > y1 + 5:
            continue
        if left_col and x0 >= mid - 10:
            continue
        if not left_col and x1 <= mid + 10:
            continue
        xs0.append(x0)
        xs1.append(x1)
    if not xs0:
        return max(0.0, cb.x0 - 8), min(page.rect.width, cb.x1 + 8)
    return max(0.0, min(xs0) - 6), min(page.rect.width, max(xs1) + 6)


def caption_region(page: fitz.Page, cap: dict, bands: list[fitz.Rect]) -> fitz.Rect:
    """图标题 → 从标题向上"贴着"图形逐个并入（在断档处停止）；
    表标题 → 向下同样处理。无图形则按栏宽 + 固定高度取框。"""
    cb = fitz.Rect(cap["bbox"])
    upward = cap["kind"] == "figure"
    band_h = 330 if upward else 460
    lo, hi = (cb.y0 - band_h, cb.y0) if upward else (cb.y1, cb.y1 + band_h)
    region = fitz.Rect(cb)

    # 只保留正确一侧、水平有重叠的图形带
    cand = []
    for b in bands:
        if b.x1 < cb.x0 - 10 or b.x0 > cb.x1 + 10:
            continue
        if upward and b.y1 <= cb.y0 + 5 and b.y0 >= lo - 30:
            cand.append(b)
        elif not upward and b.y0 >= cb.y1 - 5 and b.y1 <= hi + 30:
            cand.append(b)

    if cand:
        # 从离标题最近的带开始向外逐个贴合扩张，断档 >40pt 即停
        used: set[int] = set()
        while True:
            best, best_gap = None, 41.0
            for i, b in enumerate(cand):
                if i in used:
                    continue
                gap = (region.y0 - b.y1) if upward else (b.y0 - region.y1)
                if gap < best_gap:  # 负间隙=已重叠，直接并入
                    best, best_gap = i, gap
            if best is None:
                break
            region |= cand[best]
            used.add(best)
    else:
        x0, x1 = column_bounds(page, lo, hi, cb)
        region = fitz.Rect(x0, lo if upward else cb.y0, x1, cb.y1 if upward else hi)

    # 水平方向兜底：按栏宽补全，防止矢量带不完整导致右侧截断
    cx0, cx1 = column_bounds(page, region.y0, region.y1, cb)
    region = fitz.Rect(min(region.x0, cx0), region.y0, max(region.x1, cx1), region.y1)

    # 排除页脚区域（页码、脚注线）
    footer_y = page.rect.y1 - 34
    if region.y1 > footer_y:
        region = fitz.Rect(region.x0, region.y0, region.x1, footer_y)
    return region & page.rect


def tighten(page: fitz.Page, region: fitz.Rect, threshold: int = 245, margin: float = 4.0) -> fitz.Rect:
    """在低分辨率预览上找非白像素范围，换算回 PDF 坐标得到紧凑裁剪框。

    避免依赖 Pixmap 裁剪 API（该版本构造重载不可用）。
    """
    try:
        import numpy as np
    except ImportError:
        return region
    if region.width < 60 or region.height < 50:
        return region
    preview = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=region)
    if preview.width < 2 or preview.height < 2:
        return region
    arr = np.frombuffer(preview.samples, dtype=np.uint8)
    arr = arr.reshape(preview.height, preview.width, preview.n)[:, :, :3]
    ink = (arr < threshold).any(axis=2)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return region
    # 预览为 1pt/px，直接以像素偏移换算 PDF 坐标
    x0 = region.x0 + max(0, cols[0] - margin)
    x1 = region.x0 + min(preview.width, cols[-1] + 1 + margin)
    y0 = region.y0 + max(0, rows[0] - margin)
    y1 = region.y0 + min(preview.height, rows[-1] + 1 + margin)
    return fitz.Rect(x0, y0, x1, y1) & page.rect


def is_rotated(page: fitz.Page) -> bool:
    """大跨页表格常整页旋转 90°。以主要文本方向判定。"""
    dirs: dict[tuple, int] = {}
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            dirs[ln["dir"]] = dirs.get(ln["dir"], 0) + len(ln["spans"])
    if not dirs:
        return False
    main = max(dirs, key=dirs.get)
    return abs(main[1]) > 0.7


def render_rotated_group(doc: fitz.Document, pages: list[int], path: Path, scale: float = 2.2) -> tuple[int, int]:
    """把连续的旋转页整页渲染、转正后横向拼接成一张图。

    两类情况需区分：
    - 页面自带 /Rotate=90：PyMuPDF 渲染出来已是横向正立，不再旋转
    - /Rotate=0 但内容竖排：渲染结果为纵向，需逆时针转 90°

    正立后按页序左右并排（竖排页面的"下一页在下方"对应横排的"下一块在右侧"）。
    """
    from PIL import Image

    ims = []
    for pno in pages:
        pix = doc[pno].get_pixmap(matrix=fitz.Matrix(scale, scale))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if im.height > im.width:  # 纵向渲染 = 内容竖排（文字自下而上），顺时针转正
            im = im.rotate(-90, expand=True)
        ims.append(im)
    gap = 14
    w = max(i.width for i in ims)
    h = sum(i.height for i in ims) + gap * (len(ims) - 1)
    sheet = Image.new("RGB", (w, h), "white")
    y = 0
    for i in ims:
        sheet.paste(i, (0, y))
        y += i.height + gap
    sheet.save(path)
    return sheet.width, sheet.height


def extract(pdf_path: Path, out_root: Path) -> dict:
    doc = fitz.open(pdf_path)
    out = out_root / pdf_path.stem
    (out / "pages").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)

    index = []
    fig_seq = 0
    pno = 0
    while pno < len(doc):
        page = doc[pno]
        (out / "pages" / f"page_{pno + 1:03d}.md").write_text(
            page.get_text("text").strip() + "\n", encoding="utf-8"
        )

        # 旋转页：连续的跨页大表整体渲染为一张图
        if is_rotated(page):
            group = [pno]
            pno += 1
            while pno < len(doc) and is_rotated(doc[pno]):
                (out / "pages" / f"page_{pno + 1:03d}.md").write_text(
                    doc[pno].get_text("text").strip() + "\n", encoding="utf-8"
                )
                group.append(pno)
                pno += 1
            fig_seq += 1
            first = group[0] + 1
            last = group[-1] + 1
            suffix = f"p{first:03d}" if first == last else f"p{first:03d}-{last:03d}"
            name = f"t{fig_seq:02d}_{suffix}.png"
            render_rotated_group(doc, group, out / "figures" / name)
            index.append({"kind": "table", "text": f"(横贯 {len(group)} 页的大表，已转正)",
                          "page": first, "pages": [g + 1 for g in group], "file": name})
            continue

        bands = graphic_bands(page)
        prev_region: fitz.Rect | None = None  # 去重仅在同一页内有效
        for cap in find_captions(page):
            region = caption_region(page, cap, bands)
            if prev_region is not None:
                inter = region & prev_region
                inter_a = 0.0 if inter.is_empty else inter.width * inter.height
                min_a = min(region.width * region.height, prev_region.width * prev_region.height)
                if inter_a > 0.5 * min_a:
                    continue
            if region.width < 60 or region.height < 50:
                continue
            fig_seq += 1
            kind = cap["kind"]
            name = f"{kind[0]}{fig_seq:02d}_p{pno + 1:03d}.png"
            tight = tighten(page, region)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=tight)
            pix.save(out / "figures" / name)
            index.append({"kind": kind, "text": cap["text"], "page": pno + 1,
                          "bbox": [round(v, 1) for v in tight], "file": name})
            prev_region = region
        pno += 1

    meta = {"source_pdf": pdf_path.name, "pages": len(doc), "figures": len(index)}
    (out / "figures" / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    for pdf in args.pdfs:
        meta = extract(pdf, args.out)
        print(f"{pdf.name}: {meta['pages']}页, 提取图表 {meta['figures']} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())