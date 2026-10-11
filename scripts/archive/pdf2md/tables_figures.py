#!/usr/bin/env python3
"""表格 / 图 / 外链 的几何抽取库（scripts/pdf2md/pdf2md.py 的依赖）。

本模块只做**几何抽取**，不碰数学字体，因此对任意排版都适用：
  - 表格：词坐标聚类 -> 列对齐 -> markdown 表
  - 图：整页渲染 caption 上方区域 -> PNG + caption 文本
  - 外链：get_links()

正文段落与公式由 pdf2md.py 走视觉转写链路处理（见该文件 README）。

早期版本这里还包含公式的字符几何装配（is_formula_char / BIG_OPS /
assemble_region），绑定 Computer Modern 字族，实测在非 CM 论文上
识别率为 0（5 篇里 4 篇公式全丢），已迁至视觉链路。

本文件保留独立的 __main__ 便于单独调试：
  python tables_figures.py <pdf> -o <outdir>

注意：本文件里的 `extract_body_pages()` 仍含基于 CM 字族的公式装配，
那是早期方案的遗留，**只有独立运行本文件时才会走到**。
pdf2md.py 只调用 `extract_tables_page` / `extract_figures` /
`table_to_markdown` / `CAPTION_RE`，不经过那段代码。

独立运行（调试用）：
  python tables_figures.py <原文.pdf> -o <输出目录>
  产出 <输出目录>/paper.md, assets/fig-N.png, meta.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import fitz

PLACEHOLDER_RE = re.compile(
    r"\[(Insert\s+(Fig\.?|Table)\s*([0-9]+)[^\]]*)\]", re.IGNORECASE
)
CAPTION_RE = re.compile(r"^\s*(Fig\.?|Table)\s*([0-9]+)\b[.:]?\s*(.*)$", re.IGNORECASE)
FOOTER_RE = re.compile(r"Electronic copy available at|ssrn\.com", re.IGNORECASE)

LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}

# CM 数学字体 -> LaTeX
MATH_FONTS = ("CMMI", "CMSY", "CMEX", "MSBM")
MATH_SYMBOL_CHARS = set("()+-=,./|")
GREEK = {"α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
         "ε": r"\varepsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
         "λ": r"\lambda", "μ": r"\mu", "ν": r"\nu", "ξ": r"\xi",
         "π": r"\pi", "ρ": r"\rho", "σ": r"\sigma", "τ": r"\tau",
         "φ": r"\phi", "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
         "Γ": r"\Gamma", "Δ": r"\Delta", "Θ": r"\Theta", "Λ": r"\Lambda",
         "Σ": r"\Sigma", "Φ": r"\Phi", "Ψ": r"\Psi", "Ω": r"\Omega"}
# CMEX10 glyph 映射（由字体 charset 直接验证：vextendsingle / summationtext /
# summationdisplay / hatwide）
#   'X' = summationdisplay (∑ display), 'P' = summationtext (∑ text)
#   'b' = hatwide（宽帽号，作为 accent 修饰后继符号）
#   '\x0c' = vextendsingle（竖线延伸件，堆叠成 | ）
BIG_OPS = {"X": r"\sum", "P": r"\sum", "S": r"\sum", "R": r"\int",
           "Q": r"\prod"}
HAT_ACCENTS = {"ˆ", "b"}          # CMR 帽号 / CMEX 宽帽
BAR_EXTS = {"\x0c"}               # vextendsingle
BIN_OPS = {"−": "-", "–": "-", "·": r"\cdot", "×": r"\times",
           "≤": r"\leq", "≥": r"\geq", "≠": r"\neq", "≈": r"\approx",
           "∈": r"\in", "∞": r"\infty", "∂": r"\partial",
           "˜": r"\tilde{}", "˘": r"\tilde{}", "\u02dc": r"\tilde{}"}


def clean(s: str) -> str:
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    return s


def is_math_span(s: dict) -> bool:
    return any(k in s.get("font", "") for k in MATH_FONTS)


def tex_token(text: str, font: str) -> str:
    """单个 span 文本 -> LaTeX 片段。"""
    out = []
    for ch in text:
        if ch in GREEK:
            out.append(GREEK[ch])
        elif ch in BIN_OPS:
            out.append(BIN_OPS[ch])
        elif ch == "∗":
            out.append("*")
        elif ch in "_^$%&#{}~\\":
            out.append("\\" + ch)
        else:
            out.append(ch)
    t = "".join(out)
    if "CMEX" in font and t.strip() in BIG_OPS:
        return BIG_OPS[t.strip()]
    return t


def line_to_tex(spans: list[dict], base_size: float = 12.0) -> tuple[str, bool]:
    """一行 spans -> (markdown文本, 是否含公式)。

    char 级装配（替代旧 span 级逻辑）：
    - span 拆成 char，按 x 排序
    - hat：'ˆ' / CMEX 'b' + 后继主符号 -> \\hat{X}
    - 上下标：8/6pt 按 origin_y 相对基线判 ^/_；同类相邻合并
    - 数字粘连：'1 . 752' -> '1.752'；行尾 '.^{11}' 脚注剥离
    数学 span 前后自动包 $...$（连续数学 span 合并为一段）。

    整行数学占比高（公式行）时：整行按 char 统一装配，避免 CMR 数字与
    CMMI 符号被切成多段而在 run 之间插入空格（1 | . | 752 -> '1 . 752'）。
    """
    # 行基线
    base_oy = [s.get("origin", (0, 0))[1] for s in spans
               if abs(s.get("size", 0) - base_size) < 1.5]
    ref_oy = sum(base_oy) / len(base_oy) if base_oy else None
    ref = ref_oy if ref_oy is not None else base_size * 33.5

    # ---- 公式行：整行统一装配 ----
    math_chars = sum(len(s.get("text", "")) for s in spans if is_math_span(s))
    all_chars = sum(len(s.get("text", "")) for s in spans)
    if all_chars and math_chars / all_chars > 0.3:
        chars: list[dict] = []
        for s in spans:
            font = s.get("font", "")
            size = s.get("size", base_size)
            oy = s.get("origin", (0, 0))[1]
            bx0, _, bx1, _ = s.get("bbox", (0, 0, 0, 0))
            txt = clean(s.get("text", ""))
            n = max(len(txt), 1)
            for k, ch in enumerate(txt):
                if ord(ch) < 32:
                    continue
                # span 内按字符均分 x，保证装配顺序与视觉顺序一致
                xc = bx0 + (bx1 - bx0) * (k + 0.5) / n
                chars.append({"ch": ch, "font": font, "size": size, "oy": oy,
                              "xc": xc, "x0": xc, "x1": xc, "y0": oy, "y1": oy})
        chars.sort(key=lambda c: c["xc"])
        tex = assemble_line(chars, ref, base_size=base_size)
        return (f"${tex}$" if tex else ""), bool(tex)

    parts: list[tuple[str, tuple]] = []
    for s in spans:
        font = s.get("font", "")
        size = s.get("size", base_size)
        oy = s.get("origin", (0, 0))[1]
        txt = clean(s.get("text", ""))
        if not txt.strip():
            parts.append(("text", txt))
            continue
        stripped = txt.strip()
        accents = HAT_ACCENTS | set("\u02dc\u02d9")
        only_accents = all(ch in accents for ch in stripped)
        if is_math_span(s) or only_accents:
            parts.append(("math", (txt, font, size, oy)))
            continue
        # 组合记号可能粘在正文 span 末尾（"…low because ˆ" + 后续 CMMI σ）。
        # 把记号单独拆成 math run，避免整句被吞进公式，也避免 'ˆ' 残留。
        m = re.search("[" + re.escape("".join(accents)) + "]$", stripped)
        if m:
            cut = len(txt) - len(stripped) + m.start()
            if cut > 0:
                parts.append(("text", txt[:cut]))
            parts.append(("math", (txt[cut:], font, size, oy)))
        else:
            parts.append(("text", txt))
    # 收集连续 math span 的 char，重走 token 装配
    out: list[str] = []
    has_math = False
    i = 0
    while i < len(parts):
        kind, val = parts[i]
        if kind == "text":
            out.append(val)
            i += 1
            continue
        run_chars: list[dict] = []
        while i < len(parts) and parts[i][0] == "math":
            t, f, sz, oy = parts[i][1]
            for ch in t:
                run_chars.append({"ch": ch, "font": f, "size": sz, "oy": oy,
                                  "xc": 0, "x0": 0, "x1": 0, "y0": oy, "y1": oy})
            i += 1
        tex = assemble_line(run_chars, ref, base_size=base_size)
        if tex.strip():
            has_math = True
            out.append(f"${tex.strip()}$")
    return "".join(out), has_math


def base_tex(ch: str, font: str) -> str:
    """单个字符 -> TeX（不做上下标判定）。"""
    if ch in GREEK:
        return GREEK[ch]
    if ch in BIN_OPS:
        return BIN_OPS[ch]
    if ch == "∗":
        return "*"
    if ch in BAR_EXTS or ch in HAT_ACCENTS:
        return ""          # 由 assemble_line 单独处理
    if ch in "_^$%&#{}~\\":
        return "\\" + ch
    if "CMEX" in font and ch.strip() in BIG_OPS:
        return BIG_OPS[ch.strip()]
    return ch


def _hat_target(chars: list[dict], i: int, has_x: bool) -> int | None:
    """返回帽号 chars[i] 应修饰的字符下标。

    CMEX 'b'(hatwide) 的 x 区间几乎完全覆盖被修饰符号（α 的 [282.1,289.6] vs
    hatwide 的 [282.8,289.5]），故按 x 重叠度绑定；rawdict 里 hatwide 常常
    排在目标之后，不能按前后顺序。无 x 信息时退化为就近字符。
    """
    if has_x:
        hx0, hx1 = chars[i]["x0"], chars[i]["x1"]
        best, best_ov = None, 0.0
        for j in (i - 1, i + 1):
            if not (0 <= j < len(chars)):
                continue
            c = chars[j]
            if c["font"].startswith("CMEX") and c["ch"].strip() in BIG_OPS:
                continue
            ov = min(hx1, c["x1"]) - max(hx0, c["x0"])
            if ov > 0 and ov > best_ov:
                best, best_ov = j, ov
        if best is not None:
            return best
    for j in (i + 1, i - 1):
        if 0 <= j < len(chars):
            return j
    return None


def assemble_line(chars: list[dict], ref_oy: float,
                  base_size: float = 12.0) -> str:
    """char 序列（按 x 排好）-> TeX。

    处理：\\hat{}（CMR 'ˆ' 与 CMEX 'b' 宽帽，按 x 重叠绑定目标）、
    vextendsingle 竖线堆叠（|…|）、上下标合并（同类相邻合并，异类不合并）、
    数字粘连、脚注剥离。
    """
    # 帽号绑定：CMEX 'b'(hatwide) 的 x 区间几乎完全覆盖被修饰符号（如 α 的
    # [282.1,289.6] vs hatwide 的 [282.8,289.5]），因此按 x 重叠度绑定目标，
    # 不能按前后顺序——hatwide 在 rawdict 里常排在目标之后。
    # 部分调用路径（line_to_tex 的 run 合成）没有真实 x，退化为按顺序。
    has_x = all(c.get("x1", 0) != c.get("x0", 0) for c in chars)
    toks: list[tuple[str, str]] = []
    bar_xs: list[float] = []
    i, n = 0, len(chars)
    while i < n:
        c = chars[i]
        ch, font, size, oy = c["ch"], c["font"], c["size"], c["oy"]
        # CMEX vextendsingle：竖线延伸件，按 x 位置堆叠 -> 单个 '|'
        if ch in BAR_EXTS and "CMEX" in font:
            if not any(abs(c["xc"] - bx) < 6 for bx in bar_xs):
                bar_xs.append(c["xc"])
                toks.append(("base", "|", size, c["x0"], c["x1"], c["oy"]))
            i += 1
            continue
        # 帽号：CMR 'ˆ' 或 CMEX 'b'(hatwide) -> \hat{目标符号}
        if ch in HAT_ACCENTS and (ch == "ˆ" or "CMEX" in font):
            tgt = _hat_target(chars, i, has_x)
            if tgt is not None:
                tc = chars[tgt]
                tex = f"\\hat{{{base_tex(tc['ch'], tc['font'])}}}"
                if tgt == i + 1:
                    toks.append(("base", tex, size, c["x0"], c["x1"], c["oy"]))
                    i = tgt + 1
                else:
                    # 目标在前：把最近一个 base token 替换为带帽形式。
                    # 不能按字符串长度判断（\alpha 长 6 但仍是单个符号），
                    # 改为按「是否已经是复合式」判断：含 {} 或 \ 的说明
                    # 前面已拼了多个符号或已有修饰，不该再被帽号吃掉。
                    if toks and toks[-1][0] == "base" and not re.search(
                            r"[{}]|\s|\\\\", toks[-1][1]):
                        toks[-1] = ("base", tex, toks[-1][2], toks[-1][3], toks[-1][4], toks[-1][5])
                    else:
                        toks.append(("base", tex, size, c["x0"], c["x1"], c["oy"]))
                    i += 1
            else:
                toks.append(("base", r"\hat{}", size, c["x0"], c["x1"], c["oy"]))
                i += 1
            continue
        if ch == " ":
            toks.append(("gap", " ", size, c["x0"], c["x1"], c["oy"]))
            i += 1
            continue
        t = base_tex(ch, font)
        if size < base_size - 1.5:
            # 上下标判定三级：相对区域基线
            #   oy < base-1  -> 上标
            #   oy > base+1  -> 下标
            #   介于两者之间且字号更小 -> 附着于上一个同类脚本（二级下标，
            #   如上限 N_t 的 t：oy 196.1 与 N 的 195.1 几乎相同但字号 6<8）
            if oy < ref_oy - 1:
                op = "sup"
            elif oy > ref_oy + 1:
                op = "sub"
            else:
                op = None
            toks.append((op, t, size, c["x0"], c["x1"], c["oy"]))
        else:
            toks.append(("base", t, size, c["x0"], c["x1"], c["oy"]))
        i += 1
    merged: list[tuple[str, str]] = []
    # 同类脚本平级合并。实测 N_t 的 t(oy 196.10) 与 d_{t-j} 的 t(oy 405.22)
    # 相对各自前字符的 oy 差分别为 1.00 / 0.96pt——纯几何无法可靠区分
    # 「二级下标」与「平级下标」，故不猜嵌套层级，统一平级合并。
    # ^{Nt} 虽不如 ^{N_{t}} 精确，但不会像错误嵌套那样改变语义。
    for kind, tex, sz, chx0, chx1, choy in toks:
        if kind is None:
            if merged and merged[-1][0] in ("sub", "sup"):
                merged[-1] = (merged[-1][0], merged[-1][1] + tex)
            else:
                merged.append(("sub", tex))
            continue
        if merged and kind in ("sub", "sup") and merged[-1][0] == kind:
            merged[-1] = (kind, merged[-1][1] + tex)
        elif merged and kind == "gap" and merged[-1][0] in ("sub", "sup"):
            merged.append((kind, tex))
        elif (merged and kind in ("sub", "sup") and merged[-1][0] == "gap"
                and len(merged) >= 2 and merged[-2][0] == kind):
            merged.pop()
            merged[-1] = (kind, merged[-1][1] + tex)
        else:
            merged.append((kind, tex))
    out = []
    for kind, tex in merged:
        if kind == "sub":
            out.append(f"_{{{tex.strip()}}}")
        elif kind == "sup":
            out.append(f"^{{{tex.strip()}}}")
        else:
            out.append(tex)
    s = "".join(out)
    # 上下标内部不留空格：_{ i,t } -> _{i,t}，| \alpha -\beta | -> |\alpha-\beta|
    s = re.sub(r"([_^])\{\s+", r"\1{", s)
    s = re.sub(r"\s*([_^])\{", r"\1{", s)
    s = re.sub(r"([_^])\{([^}]*?)\s+\}", r"\1{\2}", s)
    s = re.sub(r"\s*,\s*", ",", s)
    s = re.sub(r"(_\{[^}]*?)\s*-\s*", r"\1-", s)
    s = re.sub(r"([_^])\{([^}]*)\}",
               lambda m: m.group(1) + "{" + m.group(2).strip() + "}", s)
    # 数字粘连：'1 . 752' -> '1.752'
    s = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", s)
    # 行尾脚注上标剥离：'.^{11}'
    s = re.sub(r"\.\s*[_^]\{\d+\}\s*$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def strip_outer_tex(s: str) -> str:
    """去一层外层 _{..} / ^{..} 包裹。"""
    s = s.strip()
    m = re.fullmatch(r"[_^]\{(.*)\}", s, re.S)
    return m.group(1) if m else s


def page_frac_bars(doc: fitz.Document, pno: int) -> list[tuple[float, float, float]]:
    """页内 inline-image 横条 [(x0, y, x1)]，y 为 top-origin pt。"""
    def mm(M, N):
        a, b, c, d, e, f = M
        a2, b2, c2, d2, e2, f2 = N
        return [a * a2 + b * c2, a * b2 + b * d2, c * a2 + d * c2,
                c * b2 + d * d2, e * a2 + f * c2 + e2, e * b2 + f * d2 + f2]

    G = [0.1, 0, 0, 0.1, 0, 0]
    H = doc[pno].rect.height
    out = []
    for x in doc[pno].get_contents():
        raw = doc.xref_stream(x).decode("latin-1")
        for m in re.finditer(
                r"(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) "
                r"(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) cm\s*\nBI", raw):
            C = mm(list(map(float, m.groups())), G)
            x0, y0 = C[4], C[5]
            x1, y1 = C[0] + C[4], C[3] + C[5]
            out.append((round(min(x0, x1), 1), round(H - max(y0, y1), 1),
                        round(max(x0, x1), 1)))
    return out


def region_ref_oy(chars: list[dict], fallback: float = 600.0) -> float:
    """区域自身的基线：取最大字号字符的 origin_y 中位数。

    必须用区域基线而非全页均值——下标与基线常只差 1~2pt（如 eq6 的
    σ_target：σ 基线 128.9，target 下标 130.7），用全页均值会误判成上标。
    也不能混用不同字号（上限 N_t 与下限 i 都是 8/6pt，若按中位数会把 N_t
    的下标判成上标），故先按最大字号过滤。
    """
    if not chars:
        return fallback
    top = max(c["size"] for c in chars)
    full = [c["oy"] for c in chars if c["size"] >= top - 0.5]
    if not full:
        full = [c["oy"] for c in chars]
    full.sort()
    return full[len(full) // 2]


def is_formula_char(font: str, size: float, ch: str) -> bool:
    """公式本体判据：数学字体 / 小字 / 公式符号 / 组合记号（帽号等）。"""
    if any(k in font for k in ("CMMI", "CMSY", "CMEX")):
        return True
    if size < 10:
        return True
    if ch in MATH_SYMBOL_CHARS or ch in HAT_ACCENTS or ch in BAR_EXTS:
        return True
    if ch in "\u02dc\u02d9":          # 波浪号（tilde / breve）
        return True
    if "CMR" in font and len(ch.strip()) <= 2 and not ch.strip().isalpha():
        return True
    return False


def page_formula_chars(page: fitz.Page) -> list[dict]:
    """页内 char 级记录（含 bbox/font/size/origin）。"""
    recs = []
    d = page.get_text("rawdict")
    for b in d["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            for s in ln["spans"]:
                for c in s["chars"]:
                    ch = c["c"]
                    if ord(ch) < 32 and ch != "\x0c":
                        continue
                    x0, y0, x1, y1 = c["bbox"]
                    recs.append({"x0": x0, "x1": x1, "y0": y0, "y1": y1,
                                 "xc": (x0 + x1) / 2, "yc": (y0 + y1) / 2,
                                 "font": s["font"], "size": s["size"],
                                 "oy": s["origin"][1], "ch": ch})
    return recs


def assemble_sum_block(rows: list[list], ref_oy: float) -> str | None:
    """含 CMEX 大运算符的行组 -> \\sum_{lo}^{up} 左部 右部；无大符返回 None。"""
    big = None
    for r in rows:
        for c in r:
            if "CMEX" in c["font"] and c["ch"].strip() in BIG_OPS:
                big = c
                break
        if big:
            break
    if big is None:
        return None
    op = BIG_OPS[big["ch"].strip()]
    bcx = (big["x0"] + big["x1"]) / 2
    bcy = (big["y0"] + big["y1"]) / 2
    upper, lower, left, right = [], [], [], []

    def route(c: dict) -> None:
        if c["y1"] < bcy - 2 and abs(c["xc"] - bcx) < 14:
            upper.append(c)
        elif c["y0"] > bcy + 2 and abs(c["xc"] - bcx) < 14:
            lower.append(c)
        elif c["xc"] > bcx:
            right.append(c)
        else:
            left.append(c)

    for r in rows:
        if any(c is big for c in r):
            for c in r:
                if c is big:
                    continue
                route(c)
            continue
        strip = [c for c in r if abs(c["xc"] - bcx) < 10]
        rest = [c for c in r if abs(c["xc"] - bcx) >= 10]
        ys = sum(c["y0"] for c in strip) / len(strip) if strip else None
        if (strip and ys is not None
                and max(c["xc"] for c in strip) - min(c["xc"] for c in strip) < 30):
            if ys < bcy:
                upper.extend(strip)
            else:
                lower.extend(strip)
        else:
            rest = list(r)
        for c in rest:
            route(c)
    u = assemble_line(sorted(upper, key=lambda c: c["xc"]),
                      region_ref_oy([c for r in rows for c in r], ref_oy)) if upper else ""
    lo = assemble_line(sorted(lower, key=lambda c: c["xc"]),
                       region_ref_oy([c for r in rows for c in r], ref_oy)) if lower else ""
    ls = assemble_line(sorted(left, key=lambda c: c["xc"]),
                       region_ref_oy(left, ref_oy)) if left else ""
    rs = assemble_line(sorted(right, key=lambda c: c["xc"]),
                       region_ref_oy(right, ref_oy)) if right else ""
    tex = (ls + " " if ls else "") + op
    if lo:
        tex += f"_{{{strip_outer_tex(lo)}}}"
    if u:
        tex += f"^{{{strip_outer_tex(u)}}}"
    if rs:
        tex += f" {rs}"
    return tex.strip()


def assemble_frac_block(chars: list[dict], bar: tuple[float, float, float],
                        ref_oy: float) -> str | None:
    """横条 + 上下字符 -> \\frac{num}{den}；不匹配返回 None。

    显示型分数的横条位于主基线高度，bbox 切分会混进主行字符，
    必须按基线 oy 相对 bar_y 的偏移划分：
      分子  bar_y-34 < oy < bar_y-6
      分母  bar_y+6  < oy < bar_y+36
    分子/分母各自用自己的区域基线，否则 σ_target 会被误判成上标。
    """
    x0, y, x1 = bar
    inx = [c for c in chars if x0 - 8 < c["xc"] < x1 + 8]
    num = [c for c in inx if y - 34 < c["oy"] < y - 6]
    den = [c for c in inx if y + 6 < c["oy"] < y + 36]
    if not num or not den:
        return None
    ntex = assemble_line(sorted(num, key=lambda c: c["xc"]),
                         region_ref_oy(num, ref_oy))
    dtex = assemble_line(sorted(den, key=lambda c: c["xc"]),
                         region_ref_oy(den, ref_oy))
    return f"\\frac{{{ntex}}}{{{dtex}}}"


def row_cluster(chars: list[dict]) -> list[list[dict]]:
    """按 y 区间重叠把字符切成行组。"""
    rows: list[list[dict]] = []
    for c in sorted(chars, key=lambda c: (c["oy"], c["xc"])):
        placed = False
        for r in rows:
            if r[0]["oy"] - 4 <= c["oy"] <= r[-1]["oy"] + 4:
                r.append(c)
                placed = True
                break
        if placed:
            continue
        rows.append([c])
    for r in rows:
        r.sort(key=lambda c: c["oy"])
    rows.sort(key=lambda r: r[0]["oy"])
    return rows


def bar_children(bar: tuple[float, float, float],
                 bars: list[tuple[float, float, float]],
                 lo: float, hi: float) -> list[tuple[float, float, float]]:
    """落在 bar 的 (lo, hi) 带内且 x 范围被 bar 包含的横条（嵌套子式）。"""
    x0, y, x1 = bar
    out = []
    for nb in bars:
        if nb is bar:
            continue
        if not (lo < nb[1] - y < hi):
            continue
        if nb[0] >= x0 - 5 and nb[2] <= x1 + 5:
            out.append(nb)
    return out


def assemble_region(chars: list[dict], bars: list[tuple[float, float, float]],
                    ref_oy: float, depth: int = 0) -> str:
    """递归装配一个公式区域。

    同一个显示公式内可以有多条横条（eq4 的外层分数 + 内嵌分数），
    逐条独立处理会互相抢字符，因此这里按 x 包含关系判定嵌套：
    最外层横条决定分子/分母，每个分子/分母内部再递归装配
    （内部可能又是分数，求和，或普通行）。
    """
    if not chars:
        return ""
    # 1) 区域内含大运算符 -> 求和结构优先
    bigs = [c for c in chars
            if "CMEX" in c["font"] and c["ch"].strip() in BIG_OPS]
    if bigs and len(bigs) == 1:
        rows = row_cluster(chars)
        if len(rows) > 1:
            tex = assemble_sum_block(rows, ref_oy)
            if tex and ("\\sum" in tex or "\\prod" in tex):
                return tex

    # 2) 区域内含横条 -> 分数结构
    if bars and depth < 4:
        # 找最外层横条：没有被同区域其他横条包含的那条
        outer = bars[0]
        for b in bars:
            if any(o is not b and o[0] <= b[0] + 1 and o[2] >= b[2] - 1
                   and abs(o[1] - b[1]) < 90 for o in bars):
                continue
            outer = b
        x0, y, x1 = outer
        # 子式判定：y 在上下 90pt 内 **且** x 范围被 outer 包含。
        # x 包含是主要判据（同一公式的嵌套分数不会横向溢出），
        # y 窗口要放宽，否则内层分数（eq4 偏移 +43.7pt）会被漏掉。
        kids = [b for b in bars
                if b is not outer
                and abs(b[1] - y) < 90
                and b[0] >= x0 - 5 and b[2] <= x1 + 5]
        num_bars = [b for b in kids if b[1] < y]
        den_bars = [b for b in kids if b[1] > y]
        # 区域上下界由子式撑开（子式自己还可能更深，递归时再算）
        lo = min([-40.0] + [b[1] - y - 40 for b in num_bars])
        hi = max([40.0] + [b[1] - y + 40 for b in den_bars])

        inx = [c for c in chars if x0 - 2 < c["xc"] < x1 + 2]
        num = [c for c in inx if y + lo < c["oy"] < y - 1]
        den = [c for c in inx if y + 1 < c["oy"] < y + hi]
        if num and den:
            ntex = assemble_region(num, num_bars, ref_oy, depth + 1)
            dtex = assemble_region(den, den_bars, ref_oy, depth + 1)
            # 主基线上、分数左右两侧的字符 -> 前缀/后缀
            head = [c for c in chars
                    if c["xc"] < x0 - 2 and abs(c["oy"] - y) <= 7]
            tail = [c for c in chars
                    if c["xc"] > x1 + 2 and abs(c["oy"] - y) <= 7]
            ht = assemble_line(sorted(head, key=lambda c: c["xc"]),
                               y) if head else ""
            tt = assemble_line(sorted(tail, key=lambda c: c["xc"]),
                               y) if tail else ""
            core = f"\\frac{{{ntex}}}{{{dtex}}}"
            return (ht + " " if ht else "") + core + (" " + tt if tt else "")

    # 3) 退化为单行
    return assemble_line(sorted(chars, key=lambda c: c["xc"]),
                         region_ref_oy(chars, ref_oy))


def extract_body_pages(doc: fitz.Document, body_end: int) -> tuple[list[str], list[dict]]:
    """正文页转段落流。返回 (markdown行, 占位符记录)。

    该 PDF 每行一个 block，且同行可能拆成多个 dict-line：
    1. 先按 y0 合并同行碎片（保留 spans 供公式转换）
    2. 每行经 line_to_tex 转为含 $...$ 的 markdown
    3. 再按规则切段：y 间隙 > 16pt，或字号跳变（正文/脚注），或段首缩进
    4. 独立公式行（数学占比高 + 短行/公式编号）转为 $$...$$ 块
    """
    md: list[str] = []
    placeholders: list[dict] = []
    for pno in range(min(body_end, len(doc))):
        page = doc[pno]
        # ---- 公式块预处理：锚点聚类（sum/frac），先占位 ----
        fchars = page_formula_chars(page)
        base_all = [c["oy"] for c in fchars if abs(c["size"] - 12) < 1.5]
        page_ref = sum(base_all) / len(base_all) if base_all else 600.0
        # 宽度下限放宽到 12pt：内层分数条（如 eq4 的分母内嵌套分数）本身很窄，
        # 用 >20 会把它们全滤掉，导致外层分数的分子/分母内容缺失。
        bars = [b for b in page_frac_bars(doc, pno) if b[2] - b[0] > 12]
        # 宽横条若落在表格区则跳过（表格线也是 inline-image）
        if pno + 1 >= 29 - 5:  # 样板表格始于 p29；正文页无需过滤
            pass
        consumed: set[int] = set()  # 已装配 char 的 id
        formulas: list[tuple[float, str]] = []  # (y, tex)

        def claim(sel: list[dict]) -> None:
            for c in sel:
                consumed.add(id(c))

        def near_chars(yc: float, xc: float, dy: float, dx: float) -> list[dict]:
            """锚点邻域内的公式字符。窗口按公式实测几何取值：
            求和号高约 26pt，限位在其上下 8pt 内，操作数在其左右 55pt 内。
            """
            sel = []
            for c in fchars:
                if id(c) in consumed:
                    continue
                if abs((c["y0"] + c["y1"]) / 2 - yc) < dy and abs(c["xc"] - xc) < dx \
                        and is_formula_char(c["font"], c["size"], c["ch"]):
                    sel.append(c)
            return sel

        # 1) 分数锚点优先——分子/分母内部可能再嵌求和（eq4）。
        #    先处理分数可避免求和把分数的字符抢走。
        def assemble_sum_at(b: dict) -> str | None:
            """装配单个大运算符锚点，返回 TeX（成功时同时 claim）。"""
            xc = (b["x0"] + b["x1"]) / 2
            yc = (b["y0"] + b["y1"]) / 2
            sel = near_chars(yc, xc, 30.0, 55.0)
            if not sel:
                return None
            rows: list[list] = []
            for c in sorted(sel, key=lambda c: (c["y0"], c["xc"])):
                placed = False
                for r in rows:
                    ys0 = min(x["y0"] for x in r)
                    ys1 = max(x["y1"] for x in r)
                    if c["y0"] <= ys1 + 3 and c["y1"] >= ys0 - 3:
                        r.append(c)
                        placed = True
                        break
                if not placed:
                    rows.append([c])
            tex = assemble_sum_block(rows, page_ref)
            if tex and ("\\sum" in tex or "\\prod" in tex) and len(tex) > 8:
                claim(sel)
                return tex
            return None

        def all_anchors() -> list[dict]:
            return [c for c in fchars
                    if "CMEX" in c["font"] and c["ch"].strip() in BIG_OPS]

        # 1) 分数簇优先——分子/分母内部可能再嵌分数或求和（eq4/eq9）。
        #    按 x 包含 + y 邻近把横条聚成簇，同簇交给 assemble_region 递归处理；
        #    逐条独立处理会让多条横条互相抢字符，把一个公式拆成碎片。
        H = page.rect.height
        live = [b for b in bars
                if not (b[2] < 100 and b[1] > 700) and 60 <= b[1] <= H - 40]
        seen_bars: set = set()
        for bar in live:
            if bar in seen_bars:
                continue
            cluster = [b for b in live
                       if b is bar
                       or (b[0] >= bar[0] - 12 and b[2] <= bar[2] + 12
                           and abs(b[1] - bar[1]) < 90)
                       or (bar[0] >= b[0] - 12 and bar[2] <= b[2] + 12
                           and abs(b[1] - bar[1]) < 90)]
            seen_bars.update(cluster)
            cx0 = min(b[0] for b in cluster)
            cx1 = max(b[2] for b in cluster)
            cy0 = min(b[1] for b in cluster) - 40
            cy1 = max(b[1] for b in cluster) + 40
            # x 窗口要够宽：显示公式的前缀（如 R²_{i,OOS} = 1 −）在横条左侧
            # 几十 pt 处，不收进来会被切成两段并与公式块重复。
            sel = [c for c in fchars
                   if id(c) not in consumed
                   and cy0 <= c["oy"] <= cy1
                   and cx0 - 95 <= c["xc"] <= cx1 + 70
                   and is_formula_char(c["font"], c["size"], c["ch"])]
            if len(sel) < 3:
                continue
            tex = assemble_region(sel, cluster, page_ref)
            math_n = sum(1 for c in sel
                         if any(k in c["font"] for k in ("CMMI", "CMSY", "CMEX")))
            if tex and "\\frac" in tex and math_n >= max(3, len(sel) // 4):
                claim(sel)
                formulas.append((sum(b[1] for b in cluster) / len(cluster), tex))

        # 2) 剩余的独立求和锚点（未被分数吸收的）
        for b in all_anchors():
            if id(b) in consumed:
                continue
            xc = (b["x0"] + b["x1"]) / 2
            yc = (b["y0"] + b["y1"]) / 2
            sel = [c for c in fchars
                   if id(c) not in consumed
                   and abs((c["y0"] + c["y1"]) / 2 - yc) < 30
                   and abs(c["xc"] - xc) < 55
                   and is_formula_char(c["font"], c["size"], c["ch"])]
            if not sel:
                continue
            tex = assemble_sum_block(row_cluster(sel), page_ref)
            if tex and ("\\sum" in tex or "\\prod" in tex) and len(tex) > 8:
                claim(sel)
                formulas.append((yc, tex))

        formulas.sort()
        # 已消费 char 的几何包络：frags 中落入包络的 span 行剔除
        # （sum/frac 块由 formulas 接管，避免旧逻辑拆散）
        consumed_boxes = [(c["x0"], c["y0"], c["x1"], c["y1"])
                          for c in fchars if id(c) in consumed]

        def span_consumed(spans: list[dict]) -> bool:
            """span 行多数 char 已被公式块消费 -> 整行剔除。"""
            if not consumed_boxes:
                return False
            n_hit = 0
            n_all = 0
            for s in spans:
                for ch in s.get("text", ""):
                    n_all += 1
                    x0, _, x1, _ = s.get("bbox", (0, 0, 0, 0))
                    xc = (x0 + x1) / 2
                    oy = s.get("origin", (0, 0))[1]
                    for bx0, by0, bx1, by1 in consumed_boxes:
                        if bx0 - 2 <= xc <= bx1 + 2 and by0 - 2 <= oy <= by1 + 2:
                            n_hit += 1
                            break
            return n_all > 0 and n_hit / n_all > 0.5

        d = page.get_text("dict")
        # frags 保留 spans：(y0, y1, x0, size, spans)
        frags: list[tuple[float, float, float, float, list]] = []
        for b in d["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b["lines"]:
                spans = ln.get("spans", [])
                if not spans:
                    continue
                if span_consumed(spans):
                    continue
                txt = clean("".join(s.get("text", "") for s in spans)).strip()
                if not txt or FOOTER_RE.search(txt):
                    continue
                if re.fullmatch(r"\d{1,3}", txt):
                    continue
                size = max(s.get("size", 0) for s in spans)
                x0, y0, _, y1 = ln["bbox"]
                frags.append((round(y0, 1), round(y1, 1), round(x0, 1),
                              round(size, 1), spans))
        frags.sort(key=lambda f: (f[0], f[2]))
        # 合并同行碎片（y0 相近 + 字号相近），spans 按 x0 排序拼接
        merged: list[tuple[float, float, float, float, list]] = []
        for y0, y1, x0, size, spans in frags:
            if merged and abs(y0 - merged[-1][0]) < 2 and abs(size - merged[-1][3]) < 1:
                py0, py1, px0, psize, pspans = merged[-1]
                merged[-1] = (py0, max(py1, y1), min(px0, x0), psize, pspans + spans)
            else:
                merged.append((y0, y1, x0, size, list(spans)))
        # 每行转 tex（含 $...$），同时记录数学占比
        lines: list[tuple[float, float, float, float, str, float]] = []
        for y0, y1, x0, size, spans in merged:
            spans_sorted = sorted(spans, key=lambda s: s["bbox"][0])
            base = size if size >= 10 else 12.0
            tex, has_math = line_to_tex(spans_sorted, base_size=base)
            tex = tex.strip()
            if not tex:
                continue
            math_chars = sum(len(s.get("text", "")) for s in spans_sorted if is_math_span(s))
            all_chars = sum(len(s.get("text", "")) for s in spans_sorted)
            ratio = math_chars / max(all_chars, 1)
            lines.append((y0, y1, x0, size, tex, ratio))
        # 公式块按 y 插入 lines（独占行，ratio=1.0 触发 $$ 块逻辑）
        for fy, ftex in formulas:
            fx = 200.0
            lines.append((fy - 2, fy + 2, fx, 12.0, f"${ftex}$", 1.0))
        lines.sort(key=lambda L: (L[0], L[2]))
        xs = sorted(x0 for _, _, x0, size, _, _ in lines if size >= 11)
        body_x = xs[len(xs) // 2] if xs else 89.0
        paras: list[list[tuple[float, float, float, str, float]]] = []
        cur: list[tuple[float, float, float, str, float]] = []
        prev_y1: float | None = None
        prev_size: float | None = None
        for y0, y1, x0, size, tex, ratio in lines:
            if size >= 15:  # 章节标题
                if cur:
                    paras.append(cur)
                    cur = []
                title = re.sub(r"^(\d+)\.\s*", r"\1. ", tex)
                # 标题不含公式， strip 残留 $（误判时）
                paras.append([(y0, x0, size, f"## {title}", 0.0)])
                prev_y1, prev_size = None, None
                continue
            # 独立公式行：数学占比 > 0.5 且（短行或带公式编号），独占一段
            if ratio > 0.5 and (len(tex) < 120 or re.search(r"\(\d+\)\s*$", tex)):
                if cur:
                    paras.append(cur)
                    cur = []
                paras.append([(y0, x0, size, tex, ratio)])
                prev_y1, prev_size = None, None
                continue
            brk = False
            if cur and prev_y1 is not None:
                gap = y0 - prev_y1
                if gap > 16:
                    brk = True
                elif prev_size is not None and abs(size - prev_size) > 1:
                    brk = True  # 正文/脚注切换
                elif x0 > body_x + 10 and gap > 6:
                    brk = True  # 段首缩进
            if brk:
                paras.append(cur)
                cur = []
            cur.append((y0, x0, size, tex, ratio))
            prev_y1, prev_size = y1, size
        if cur:
            paras.append(cur)
        for para in paras:
            if len(para) == 1 and para[0][2] >= 15:
                md += ["", para[0][3], ""]
                continue
            # 独立公式段 -> $$...$$ 块
            if len(para) == 1 and para[0][4] > 0.5:
                tex = para[0][3]
                # 剥离公式编号 (N)，转为 \tag
                m = re.search(r"\((\d+)\)\s*$", tex)
                tag = ""
                if m:
                    tag = f" \\tag{{{m.group(1)}}}"
                    tex = tex[: m.start()].strip()
                # 把 $...$ 内联转为块级：去外层 $，包 $$...$$
                inner = re.sub(r"^\$(.*)\$$", r"\1", tex.strip())
                # 多个 $...$ 片段合并
                inner = re.sub(r"\$\s*", " ", inner)
                inner = re.sub(r"\s*\$", " ", inner)
                inner = re.sub(r"\s+", " ", inner).strip()
                md += ["", f"$${inner}{tag}$$", ""]
                continue
            texts = [t for _, _, _, t, _ in para]
            # 占位符独占段时转标记
            if len(texts) == 1:
                m = PLACEHOLDER_RE.search(texts[0])
                if m and len(texts[0].strip()) < 60:
                    kind = "F" if m.group(2).lower().startswith("fig") else "T"
                    key = f"{kind}{m.group(3)}"
                    placeholders.append({"key": key, "page": pno + 1})
                    md.append(f"\n<!-- PLACEHOLDER:{key} -->\n")
                    continue
            md.append(reflow(texts))
            md.append("")
    return md, placeholders


def reflow(lines: list[str]) -> str:
    """行合并为段：连字符续行直连，否则空格连接；段内空行分段启发式略去（原型从简）。"""
    out = ""
    for ln in lines:
        if out.endswith("-"):
            out = out[:-1] + ln.lstrip()
        elif not out:
            out = ln
        else:
            out += " " + ln
    return clean(out)


# ---------------- 表格 ----------------

def cluster_columns(words: list[tuple], tol: float = 18.0) -> list[float]:
    xs = sorted(w[0] for w in words)
    clusters: list[list[float]] = []
    for x in xs:
        if clusters and x - clusters[-1][-1] <= tol:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    return [sum(c) / len(c) for c in clusters]


def _is_num_cell(s: str) -> bool:
    s = s.strip().strip("()")
    if s in ("—", "–", "-", "--"):
        return True  # 缺失值占位也算数据格
    return bool(re.fullmatch(r"-?[\d.]+%?", s))


def _is_panel_label(s: str) -> bool:
    return bool(re.match(r"\s*Panel\s+[A-Z]\s*:", s))


def _looks_like_header_line(s: str) -> bool:
    """短行、无句号结尾。Panel 标签行由调用方跳过（不阻断回溯）。"""
    s = s.strip()
    if not s or len(s) > 85:
        return False
    if s.endswith("."):
        return False
    if len(s.split()) > 10:
        return False
    return True


def extract_tables_page(page: fitz.Page) -> list[dict]:
    """一页提多表。每表 -> {num, title, subtitle, header, rows, notes}。

    无边框文本流按坐标重建：
    - 标题行（Table N）定位各表起点，下一标题为终点（严格开区间）
    - 表头 = 首个数据行上方连续的短行（描述段落是长句，自动排除）
    - t 值括号行向后并入；单标签行（如 WML*）向前并入下一数据行
    - y 间隙 > 60pt 即判定表结束（页码等孤立行自动排除）
    """
    words = page.get_text("words")
    words = [w for w in words if not FOOTER_RE.search(w[4])]
    if not words:
        return []
    rows_y: dict[int, list] = defaultdict(list)
    for w in words:
        rows_y[round(w[1])].append(w)
    sorted_y = sorted(rows_y)

    def raw_text(y: int) -> str:
        return clean(" ".join(w[4] for w in sorted(rows_y[y], key=lambda w: w[0])))

    # 所有 Table N 标题行
    titles: list[tuple[int, str]] = []
    for y in sorted_y:
        m = re.match(r"\s*Table\s+([0-9]+)\b", raw_text(y))
        if m and len(raw_text(y)) < 60:
            titles.append((y, m.group(1)))
    if not titles:
        return []
    titles.append((10**9, ""))  # 哨兵

    tables = []
    for ti in range(len(titles) - 1):
        y0, num = titles[ti]
        y1 = titles[ti + 1][0]
        ys = [y for y in sorted_y
              if y0 < y < y1 and y < page.rect.y1 - 40 and raw_text(y)]
        if not ys:
            continue
        texts = [(y, raw_text(y)) for y in ys]

        def is_data_line(t: str) -> bool:
            return sum(1 for w in t.split() if _is_num_cell(w)) >= 2

        di = next((i for i, (_, t) in enumerate(texts) if is_data_line(t)), None)
        if di is None:
            continue
        # 表头：向上连续短行，最多 5 行；Panel 标签行跳过但不阻断
        hi = di
        while hi - 1 >= 0 and di - (hi - 1) <= 5:
            prev = texts[hi - 1][1]
            if _is_panel_label(prev):
                hi -= 1
                continue
            if not _looks_like_header_line(prev):
                break
            hi -= 1
        subtitle = clean(" ".join(t for _, t in texts[:hi]
                                  if len(t) > 40))[:400]
        # 该表列聚类：表区数字词 x0
        region_words = [w for y, _ in texts[hi:] for w in rows_y[y]]
        num_xs = sorted(w[0] for w in region_words if _is_num_cell(w[4]))
        if len(num_xs) >= 4:
            cols = cluster_columns([(x,) for x in num_xs])
        else:
            cols = cluster_columns([(w[0],) for w in region_words])
        # 表头按列分配（直接用表头区词坐标；Panel 标签行跳过）
        header = [""] * len(cols)
        for y, t in texts[hi:di]:
            if _is_panel_label(t):
                continue
            for w in rows_y[y]:
                idx = min(range(len(cols)), key=lambda i: abs(cols[i] - w[0]))
                header[idx] = (header[idx] + " " + w[4]).strip() if header[idx] else w[4]
        header = [clean(h) for h in header]

        def assign(y: int) -> list[str]:
            cells = [""] * len(cols)
            for w in sorted(rows_y[y], key=lambda w: w[0]):
                idx = min(range(len(cols)), key=lambda i: abs(cols[i] - w[0]))
                cells[idx] = (cells[idx] + " " + w[4]).strip() if cells[idx] else w[4]
            return [clean(c) for c in cells]

        # 数据行
        body: list[list[str]] = []
        notes_parts: list[str] = []
        prev_y = texts[di][0]
        i = di
        pending_label = ""  # 单标签行暂存，向前并入
        ended = False
        while i < len(texts):
            y, t = texts[i]
            if y - prev_y > 60 and body:
                notes_parts.extend(x[1] for x in texts[i:])
                break
            prev_y = y
            cells = assign(y)
            non_empty = [c for c in cells if c]
            if not non_empty:
                i += 1
                continue
            if re.fullmatch(r"\d{1,3}", t.strip()):
                i += 1  # 页码孤行
                continue
            if _is_panel_label(t):
                # Panel 分节行：独占一行（首列），不参与数据
                row = [""] * len(cols)
                row[0] = f"**{t.strip()}**"
                body.append(row)
                i += 1
                continue
            if len(non_empty) == 1 and not _is_num_cell(non_empty[0]):
                # 单标签：暂存，拼到下一数据行首格
                pending_label = (pending_label + " " + non_empty[0]).strip() \
                    if pending_label else non_empty[0]
                i += 1
                continue
            if all(re.fullmatch(r"\(.*\)", c) or not c for c in cells):
                # t 值行：向后并入上一行
                if body:
                    for j, c in enumerate(cells):
                        if c and j < len(body[-1]):
                            body[-1][j] = (body[-1][j] + " " + c).strip()
                i += 1
                continue
            if not is_data_line(t) and body and len(t) > 40:
                # 尾部描述 -> notes
                notes_parts.extend(x[1] for x in texts[i:])
                break
            if pending_label:
                cells[0] = (pending_label + " " + cells[0]).strip()
                pending_label = ""
            body.append(cells)
            i += 1
        if pending_label and body:
            body[-1][0] = (body[-1][0] + " " + pending_label).strip()

        title_line = raw_text(y0)
        tables.append({"num": num, "title": title_line, "subtitle": subtitle,
                       "header": header, "rows": body,
                       "notes": clean(" ".join(notes_parts))[:600],
                       "ncol": len(cols)})
    return tables


def extract_table_page(page: fitz.Page) -> dict | None:
    ts = extract_tables_page(page)
    return ts[0] if ts else None


def table_to_markdown(t: dict) -> str:
    h = t["header"]
    lines = [f"**Table {t['num']}: {clean(t['title'])}**", "",
             "| " + " | ".join(h) + " |",
             "| " + " | ".join(["---"] * len(h)) + " |"]
    for r in t["rows"]:
        # 补齐列数
        if len(r) < len(h):
            r = r + [""] * (len(h) - len(r))
        lines.append("| " + " | ".join(r[: len(h)]) + " |")
    if t["notes"]:
        lines += ["", f"*{t['notes'][:600]}*"]
    return "\n".join(lines)


# ---------------- 图 ----------------

def extract_figures(doc: fitz.Document, fig_pages: list[int], out_assets: Path) -> dict:
    """矢量图页渲染为 PNG（caption 上方区域），返回 {F1: {file, caption, page}}。"""
    out_assets.mkdir(parents=True, exist_ok=True)
    figs: dict[str, dict] = {}
    for pno in fig_pages:
        page = doc[pno]
        txt = page.get_text()
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        cap_text, cap_y0 = "", None
        for i, l in enumerate(lines):
            m = CAPTION_RE.match(l)
            if m:
                # caption 可能跨多行：续接后续非空行直到空行或 Panel 开头
                cap_text = l
                # 在页面坐标中定位 caption 起始 y
                for b in page.get_text("dict")["blocks"]:
                    if b.get("type") != 0:
                        continue
                    for ln in b["lines"]:
                        s = clean("".join(s.get("text", "") for s in ln["spans"])).strip()
                        if s.startswith(l[:30]):
                            cap_y0 = ln["bbox"][1]
                            break
                    if cap_y0 is not None:
                        break
                # 续行
                j = i + 1
                while j < len(lines) and len(cap_text) < 600:
                    nxt = lines[j]
                    if CAPTION_RE.match(nxt) or nxt.startswith("Panel") or FOOTER_RE.search(nxt):
                        break
                    if re.fullmatch(r"\d{1,3}", nxt):
                        break
                    cap_text += " " + nxt
                    j += 1
                num = m.group(2)
                key = f"F{num}"
                # clip：整页宽，顶部留 30pt，底部到 caption 上方
                y1 = (cap_y0 - 8) if cap_y0 else page.rect.y1 - 60
                clip = fitz.Rect(20, 20, page.rect.width - 20, max(y1, 100))
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), clip=clip)
                fname = f"fig-{num}.png"
                pix.save(out_assets / fname)
                figs[key] = {"file": fname, "caption": clean(cap_text[:800]),
                             "page": pno + 1}
                break
    return figs


# ---------------- 主流程 ----------------

BODY_END_RE = re.compile(r"^\s*(references|bibliography|参考文献)\s*$", re.I)


def detect_body_end(doc: fitz.Document) -> int:
    """正文结束页：参考文献标题所在页（不含）。找不到就返回末页。"""
    for pno in range(len(doc)):
        for line in doc[pno].get_text().splitlines():
            if BODY_END_RE.match(line.strip()):
                return pno
    return len(doc)


def detect_table_pages(doc: fitz.Document, start: int = 0) -> list[int]:
    """含表格的页：对每页跑一次表格抽取，有结果即收录。

    必须扫全文而非只扫 body_end 之后：部分论文（TimeSeriesMomentum）
    的表格/图内联在正文中，位于参考文献之前。
    """
    return [p for p in range(start, len(doc)) if extract_tables_page(doc[p])]


def detect_fig_pages(doc: fitz.Document, start: int = 0) -> list[int]:
    """含图caption 的页。CAPTION_RE 用 ^ 锚定行首，必须逐行匹配
    （对整页文本 search 永远不中）。另要求页面确有图形内容。
    同样扫全文——图既可能在文末也可能内联在正文中。"""
    out = []
    for p in range(start, len(doc)):
        page = doc[p]
        # 纯图表页也可能被 Table 命中，这里只认 Fig.
        has_cap = any(CAPTION_RE.match(l.strip())
                      and re.match(r"\s*Fig", l.strip(), re.I)
                      for l in page.get_text().splitlines())
        if not has_cap:
            continue
        if page.get_images() or page.get_drawings():
            out.append(p)
    return out


def convert(pdf_path: Path, out_dir: Path,
            body_end: int | None = None, table_pages: list[int] | None = None,
            fig_pages: list[int] | None = None) -> dict:
    doc = fitz.open(pdf_path)
    n = len(doc)
    # 全部自动探测：不同论文的正文长度、表格页、图页都不同，
    # 不能沿用样板的硬编码页码。表格/图要扫全文——
    # 部分论文（TimeSeriesMomentum）的表格内联在正文中、在参考文献之前。
    if body_end is None:
        body_end = detect_body_end(doc)
    if table_pages is None:
        table_pages = detect_table_pages(doc)
    if fig_pages is None:
        fig_pages = detect_fig_pages(doc)
    table_pages = [p for p in table_pages if p < n]
    fig_pages = [p for p in fig_pages if p < n]

    md_lines, placeholders = extract_body_pages(doc, body_end)

    tables: dict[str, dict] = {}
    for pno in table_pages:
        for t in extract_tables_page(doc[pno]):
            tables[f"T{t['num']}"] = t

    assets = out_dir / "assets"
    figs = extract_figures(doc, fig_pages, assets)

    # 内联：占位符 -> 图表 markdown
    out: list[str] = []
    used = set()
    for ln in md_lines:
        m = re.search(r"<!-- PLACEHOLDER:(F\d+|T\d+) -->", ln)
        if m:
            key = m.group(1)
            used.add(key)
            out.append("")
            if key.startswith("T") and key in tables:
                out.append(table_to_markdown(tables[key]))
            elif key.startswith("F") and key in figs:
                f = figs[key]
                out.append(f"![Fig. {key[1:]}](assets/{f['file']})")
                out.append("")
                out.append(f"*{f['caption']}*")
            else:
                out.append(f"> [图表 {key} 未在文末定位，见原文 p{next((p['page'] for p in placeholders if p['key']==key), '?')}]")
            out.append("")
        else:
            out.append(ln)
    # 文末未被占位符消费的图表，附录兜底
    rest = [k for k in list(tables) + list(figs) if k not in used]
    if rest:
        out += ["", "---", "", "## 文末图表（占位符未覆盖）", ""]
        for k in sorted(rest):
            if k.startswith("T"):
                out += [table_to_markdown(tables[k]), ""]
            else:
                f = figs[k]
                out += [f"![Fig. {k[1:]}](assets/{f['file']})", "", f"*{f['caption']}*", ""]

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "paper.md").write_text("\n".join(out).strip() + "\n", encoding="utf-8")
    meta = {"source": pdf_path.name, "pages": n,
            "placeholders": placeholders,
            "tables": {k: {"page": None, "title": v["title"]} for k, v in tables.items()},
            "figures": figs}
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="PDF -> 图表内联 Markdown 原型")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    meta = convert(args.pdf, args.out)
    print(f"[ok] {args.out / 'paper.md'}")
    print(f"  placeholders: {len(meta['placeholders'])}")
    print(f"  tables: {sorted(meta['tables'])}")
    print(f"  figures: {sorted(meta['figures'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
