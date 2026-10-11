"""MISSING_MATH 判据的双向验证。

判据从 pdf2md 实际代码取，避免测试与实现漂移
（此前两份正则各写一份，改一处忘一处，测试就形同虚设）。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf2md as P


def looks_like_math(text: str) -> bool:
    """与 pdf2md.verify_block 中同一判据（保持唯一来源）。"""
    scrub = re.sub(r'https?://\S+', ' ', text)
    scrub = re.sub(r'\S+@\S+', ' ', scrub)
    scrub_nw = re.sub(r'\b(?:and|or|he|she|they|we|it)\s*/\s*'
                      r'(?:or|and|he|she|they|we|it)\b', ' ', scrub, flags=re.I)
    return bool(re.search(r'[=≤≥≈⇒∫∑√∂]|</?[a-z]+>', scrub_nw)) or \
        bool(re.search(
            r'[A-Za-z]{1,3}[₀-₉a-z,]{1,3}\s*/\s*'
            r'(?:\(?\s*[A-Za-zσ]{1,3}[₀-₉a-z,]{0,3})',
            scrub_nw))


FALSE_POS = [
    'These range between the values of 0.13 and 2.00, reaching lows in 1930s, in 2000-02, and in 2008-09.',
    'The sample spans 1927 to 2011, with 529 observations in all.',
    'Table 2 reports t-stats of 1.96, 2.58 and 2.11 for panels A, B, C respectively.',
    'We use 126 day windows, roughly six months, and 21 day lags.',
    'Returns are 1.49% per month for winners and -0.46% for losers.',
    'The strategy holds 11 stocks, or 20% of the sample, at any time.',
    'See Table 3 and Figure 7 for details, and Section 4.2 for the derivation.',
    'Profits and/or losses are reported monthly on a value-weighted basis.',
    'The winners-minus-losers spread is positive in 1932 and negative in 2009.',
]
TRUE_POS = [
    'where RV i,t = X j=0 r2 i,dt−j and the sum runs over j',
    'we estimate r WML,t = 1.752 − 0.378 r RMRF,t',
    'the ratio r i,t/σ i,t exceeds 1 for 23% of months',
    'E[r t] = μ + σ ε t with ε ~ N(0,1)',
    'R2 i,OOS = 1 − X (αt + ρt RVi,t − RVi,t+1)2',
    'w t (a) := (1 −a) w SLOW , t + a w FAST , t',
    'it = ct(rank(Sit) − irank(Sit)/N)',
    'σ2 t = ω + βσ2 t−1 + (α + γI(ϵt−1 < 0)) ϵ2 t−1',
]

fp = fn = 0
print('=== 假阳性检查（应判「无公式」）===')
for t in FALSE_POS:
    hit = looks_like_math(t)
    fp += hit
    print(f'  [{"误报!" if hit else "OK   "}] {t[:64]}')
print('\n=== 灵敏度检查（应判「有公式」）===')
for t in TRUE_POS:
    hit = looks_like_math(t)
    fn += (not hit)
    print(f'  [{"漏报!" if not hit else "OK   "}] {t[:64]}')

print(f'\n误报 {fp}/{len(FALSE_POS)}   漏报 {fn}/{len(TRUE_POS)}')
sys.exit(1 if (fp or fn) else 0)