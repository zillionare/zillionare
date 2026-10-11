#!/usr/bin/env python3
"""译文 PDF 质量核查：对比原文与译文的页数、矢量绘图数、图表占位符。

用法:
  python3 tools/verify_translation.py <原文.pdf> <译文.pdf>

退出码 0 = 通过，1 = 有差异。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

PLACEHOLDER_RE = re.compile(
    r'[\[【](?=[^\]】]*(?:Fig\.?|Table|图|表)\s*[0-9]+)'
    r'[^\]】]*(?:插入|放入|Insert|附近|将)[^\]】]*'
    r'(?:Fig\.?|Table|图|表)\s*([0-9]+)[^\]】]*[\]】]',
    re.IGNORECASE,
)


def check(orig_path: Path, zh_path: Path) -> int:
    orig = fitz.open(orig_path)
    zh = fitz.open(zh_path)
    errors = []

    # 1. 页数
    if len(orig) != len(zh):
        errors.append(f'页数不一致: 原文 {len(orig)} vs 译文 {len(zh)}')
    else:
        print(f'[ok] 页数一致: {len(orig)} 页')

    # 2. 每页矢量绘图数（图表是否保留）
    lost = []
    for pno in range(min(len(orig), len(zh))):
        a = len(orig[pno].get_drawings())
        b = len(zh[pno].get_drawings())
        if a > 0 and b == 0:
            lost.append(pno + 1)
        elif abs(a - b) > max(5, a * 0.1):
            lost.append(f'{pno + 1}(原{a}/译{b})')
    if lost:
        errors.append(f'矢量绘图疑似丢失的页: {lost}')
    else:
        print('[ok] 矢量绘图数一致（图表保留）')

    # 3. 占位符数量（正文引用图表的完整性）
    def placeholders(doc):
        out = []
        for pno in range(len(doc)):
            for m in PLACEHOLDER_RE.finditer(doc[pno].get_text()):
                out.append((pno + 1, m.group(0)[:40]))
        return out

    po, pz = placeholders(orig), placeholders(zh)
    if len(po) != len(pz):
        errors.append(f'图表占位符数量不一致: 原文 {len(po)} vs 译文 {len(pz)}')
    else:
        print(f'[ok] 图表占位符数量一致: {len(po)} 个')

    # 4. 译文是否还有未翻译的大段英文（抽查：连续 200+ 英文字符的行）
    long_en = 0
    for pno in range(len(zh)):
        for line in zh[pno].get_text().splitlines():
            s = line.strip()
            if len(s) > 200 and re.fullmatch(r'[A-Za-z0-9\s\.,;:\(\)\[\]\-\'\"/%$&]+', s):
                long_en += 1
    if long_en > 5:
        errors.append(f'译文中有 {long_en} 行疑似未翻译的长英文')
    else:
        print(f'[ok] 未翻译长英文行数: {long_en}')

    if errors:
        print('\n[FAIL]')
        for e in errors:
            print('  -', e)
        return 1
    print('\n[PASS] 全部检查通过')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'用法: {sys.argv[0]} <原文.pdf> <译文.pdf>', file=sys.stderr)
        sys.exit(2)
    sys.exit(check(Path(sys.argv[1]), Path(sys.argv[2])))
