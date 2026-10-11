#!/usr/bin/env python3
"""生成图表截图的联络图（contact sheet），用于人工目检裁剪质量。

用法:
  python3 tools/contact_sheet.py --figures extracted/<论文名>/figures -o /tmp/check.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="图表截图联络图")
    ap.add_argument("--figures", required=True, type=Path, help="figures 目录或 png 文件")
    ap.add_argument("-o", "--output", required=True, type=Path)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--cell", nargs=2, type=int, default=[470, 330], metavar=("W", "H"))
    ap.add_argument("--limit", type=int, default=0, help="最多放几张，0=全部")
    args = ap.parse_args()

    from PIL import Image, ImageDraw

    if args.figures.is_dir():
        imgs = sorted(args.figures.glob("*.png"))
    else:
        imgs = [args.figures]
    if args.limit:
        imgs = imgs[: args.limit]
    if not imgs:
        raise SystemExit(f"未找到 png: {args.figures}")

    cw, ch = args.cell
    cols = max(1, args.cols)
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cw * cols, ch * rows), "white")
    dr = ImageDraw.Draw(sheet)
    for i, p in enumerate(imgs):
        im = Image.open(p)
        w0, h0 = im.size
        im.thumbnail((cw - 10, ch - 22))
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(im, (x + 5, y + 18))
        dr.text((x + 6, y + 4), f"{p.name} {w0}x{h0}", fill="red")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"[ok] {len(imgs)} 张 -> {args.output} ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
