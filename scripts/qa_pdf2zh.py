#!/usr/bin/env python3
"""pdf2zh 译文质检：归属、完整性、真实性。

背景：手工核对发现 translations/Momentum-Has-Its-Moments/ 里的 zh.pdf
实际是另一篇论文（Momentum Crashes）的译文——批量翻译时文件错位并不
罕见，而且不看内容很难察觉。本脚本用机器可查的信号自动发现这类问题：

  1. 归属：mono 版页数应与 original-en 一致（±2 页）；
     dual 版约为 2 倍。页数明显不符 = 大概率装错了论文。
  2. 真实性：页面文本中 CJK 字符占比应显著（>15%），否则可能
     是未翻译/翻译失败后回退的原文。
  3. 完整性：逐页检查是否有空白页（文本量骤降为 0）。
  4. 公式保全：抽查含公式的页——pdf2zh 保留原字形，正文应仍能抽到
     数学符号（∑ ∫ √ 或希腊字母），全无 = 可疑。

用法：
    python scripts/qa_pdf2zh.py <translations_dir> [--orig-dir <originals_dir>]

translations_dir 结构假定：
    <dir>/<PaperName>/original-en.pdf   （该文件夹对应的英文原文）
    <dir>/<PaperName>/zh.pdf            （mono，可选）
    <dir>/<PaperName>/zh-dual.pdf       （dual，可选）
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import fitz

# pdf2zh 输出的部分汉字落在 CJK 兼容表意区（U+F900-FAFF，如 量→U+F97E）
# 与扩展 A 区（U+3400-4DBF），不算进来会低估中文占比/漏检术语。
# 统一先做 NFC 归一化（兼容表意字符有规范分解，会被折叠回统一汉字），
# 再统计，双保险。
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
MATH_SYM = re.compile(r'[\u2211\u222b\u221a\u03b1-\u03c9\u0391-\u03a9\u2264\u2265\u2260]')


def norm_text(s: str) -> str:
    return unicodedata.normalize('NFC', s)


def page_stats(doc: fitz.Document) -> dict:
    n_cjk = n_ascii = n_math = 0
    empty = []
    for i in range(len(doc)):
        t = norm_text(doc[i].get_text())
        c = len(CJK.findall(t))
        n_cjk += c
        n_ascii += len(re.findall(r'[A-Za-z]', t))
        n_math += len(MATH_SYM.findall(t))
        if i > 0 and len(t.strip()) < 20:
            empty.append(i + 1)
    return {'pages': len(doc), 'cjk': n_cjk, 'ascii': n_ascii,
            'math': n_math, 'empty': empty}


def check_paper(folder: Path, results: list):
    name = folder.name
    # 原文优先取本目录 original-en.pdf，缺失时回退到同级 originals/ 共享目录
    # （translations/<Paper>/original-en.pdf 是 originals/<Paper>.pdf 的副本，
    #   已按去重原则删除，QA 通过相对路径寻址）。
    orig = folder / 'original-en.pdf'
    if not orig.exists():
        alt = folder.parent.parent / 'originals' / f'{name}.pdf'
        if alt.exists():
            orig = alt
    if not orig.exists():
        results.append((name, 'FAIL', '找不到原文（original-en.pdf / originals/），无法核对'))
        return
    d_orig = fitz.open(orig)
    n_orig = len(d_orig)
    s_orig = page_stats(d_orig)
    d_orig.close()

    if not (folder / 'zh.pdf').exists() and \
            not (folder / 'zh-dual.pdf').exists():
        results.append((name, 'TODO', f'{n_orig} 页，尚未翻译'))
        return

    for fname, kind in (('zh.pdf', 'mono'), ('zh-dual.pdf', 'dual')):
        f = folder / fname
        if not f.exists():
            continue
        d = fitz.open(f)
        s = page_stats(d)
        d.close()
        notes = []
        ok = True

        # 1) 归属：页数
        expect = n_orig if kind == 'mono' else n_orig * 2
        tol = 2 if kind == 'mono' else 4
        if abs(s['pages'] - expect) > tol:
            ok = False
            notes.append(f"页数 {s['pages']} ≠ 预期 {expect}(±{tol})"
                         f"，疑似装错论文")
        # 2) 真实性：CJK 占比
        total_letters = s['cjk'] + s['ascii']
        ratio = s['cjk'] / max(total_letters, 1)
        if ratio < 0.15:
            ok = False
            notes.append(f'中文字符占比仅 {ratio:.0%}，疑似未翻译')
        # 3) 完整性：空白页
        if s['empty']:
            ok = False
            notes.append(f"空白页 {s['empty'][:6]}"
                         f"{'...' if len(s['empty']) > 6 else ''}")
        # 4) 公式保全：与原文对比数学符号量级
        if s_orig['math'] > 50 and s['math'] < s_orig['math'] * 0.2:
            ok = False
            notes.append(f"数学符号骤减 {s_orig['math']}→{s['math']}，"
                         f"公式可能丢失")
        tag = 'OK  ' if ok else 'FAIL'
        detail = '; '.join(notes) if notes else \
            f"{s['pages']}页 中文{ratio:.0%} 公式符{s['math']}"
        results.append((f'{name}/{fname}', tag, detail))


def main() -> int:
    ap = argparse.ArgumentParser(description='pdf2zh 译文质检')
    ap.add_argument('dir', type=Path)
    args = ap.parse_args()
    if not args.dir.exists():
        print(f'[error] 目录不存在: {args.dir}')
        return 2

    results = []
    folders = [d for d in sorted(args.dir.iterdir())
               if d.is_dir() and not d.name.startswith('.')]
    for folder in folders:
        check_paper(folder, results)

    width = max((len(r[0]) for r in results), default=10)
    n_bad = n_todo = 0
    for name, tag, detail in results:
        if tag == 'FAIL':
            n_bad += 1
        elif tag == 'TODO':
            n_todo += 1
        print(f'{tag} {name:<{width}}  {detail}')
    print(f'\n共 {len(results)} 份：OK {len(results) - n_bad - n_todo}，'
          f'FAIL {n_bad}，待翻译 {n_todo}')
    return 1 if n_bad else 0


if __name__ == '__main__':
    raise SystemExit(main())