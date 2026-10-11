"""版面/重复检测的回归测试（纯合成数据，不依赖任何 PDF）。

覆盖两个曾产生实际缺陷的判据：
  1. 栏探测：单栏页不能被单个行尾碎片误判成双栏
     （mhim p4 曾因此产出与正文重复的垃圾块）
  2. 重复/重叠检测：跨块重复与区域重叠必须被检出，正常内容不得误报

运行：python test_layout_rules.py   退出码非 0 = 有退化
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdf2md as M

PAGE_W = 595.0
fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    if not ok:
        fails += 1
    print(f'  [{"OK  " if ok else "FAIL"}] {name}: got={got} want={want}')


def mk_line(x0, y0, text, w=None):
    return {'x0': x0, 'x1': x0 + (w or PAGE_W * 0.7), 'y0': y0,
            'y1': y0 + 12, 't': text, 'minS': 9, 'maxS': 12}


print('=== 1) 栏探测（单栏页 + 行尾碎片）===')
# 主栏 25 行 + 1 行行尾碎片（len>20 且 x0 远离主栏）——不得判为双栏
lines = [mk_line(89, 100 + i * 24, 'main body line number ' + str(i) * 3)
         for i in range(25)]
lines.append(mk_line(347.9, 400, 'An autoregression of monthly'))
a, b = M._column_xs(lines, PAGE_W)
check('单栏+1碎片 -> 无第二栏', b, 0.0)

# 碎片堆（4 行）仍不得判双栏（实测碎片堆最多 2 行，真栏最少 5 行）
lines2 = [mk_line(89, 100 + i * 24, 'main body line number ' + str(i) * 3)
          for i in range(25)]
lines2 += [mk_line(347.9, 300 + i * 24, 'fragment line long enough xx')
           for i in range(4)]
a2, b2 = M._column_xs(lines2, PAGE_W)
check('单栏+4行碎片 -> 仍无第二栏', b2, 0.0)

# 真稀疏右栏（5 行，仿 turning_points p13）-> 必须识别
lines3 = [mk_line(38, 100 + i * 24, 'main body line number ' + str(i) * 3)
          for i in range(17)]
lines3 += [mk_line(283, 300 + i * 24, 'right column sparse line text')
           for i in range(5)]
a3, b3 = M._column_xs(lines3, PAGE_W)
check('稀疏右栏5行 -> 识别双栏', b3, 283.0)

print('\n=== 2) 栏探测（真双栏）===')
dl = [mk_line(38, 100 + i * 24, 'left column text line ' + str(i) * 3)
      for i in range(20)]
dl += [mk_line(283, 100 + i * 24, 'right column text line ' + str(i) * 3)
       for i in range(20)]
da, db = M._column_xs(dl, PAGE_W)
check('真双栏两栏均被识别', (da, db), (38.0, 283.0))

print('\n=== 3) 区域重叠检测 ===')
A = {'index': 0, 'page': 5, 'box': (89, 100, 515, 475), 'md': 'x' * 50,
     'ok': True, 'issues': []}
B = {'index': 3, 'page': 5, 'box': (348, 391, 506, 427), 'md': 'y' * 50,
     'ok': True, 'issues': []}          # 完全嵌在 A 内
C = {'index': 4, 'page': 5, 'box': (89, 487, 508, 618), 'md': 'z' * 50,
     'ok': True, 'issues': []}          # 与 A 不重叠
n = M._annotate_overlaps([A, B, C])
check('嵌套块被标记', (n, A['ok'], B['ok'], C['ok']), (2, False, False, True))
D = {'index': 0, 'page': 1, 'box': (89, 100, 515, 200), 'md': 'x', 'ok': True,
     'issues': []}
E = {'index': 1, 'page': 1, 'box': (89, 199, 515, 300), 'md': 'y', 'ok': True,
     'issues': []}
check('边界共享2pt不标记', M._annotate_overlaps([D, E]), 0)

print('\n=== 4) 跨块重复检测 ===')
dup_sent = ('an autoregression of monthly realized variances yields an '
            'out of sample r square of')
blocks = [
    {'index': 0, 'page': 4, 'md': f'prefix text before. {dup_sent} 57.82 done'},
    {'index': 1, 'page': 4, 'md': f'{dup_sent} 57.82 this is'},
    {'index': 2, 'page': 5, 'md': 'unrelated content about momentum returns'},
]
issues = M._find_duplicate_blocks(blocks)
check('重复被检出', len(issues), 1)
check('类型正确', issues[0]['kind'] if issues else '', 'DUPLICATE_CONTENT')
ok2 = M._find_duplicate_blocks([
    {'index': 0, 'page': 1, 'md': 'The quick brown fox jumps over the lazy '
                                 'dog and runs into the deep forest'},
    {'index': 1, 'page': 1, 'md': 'Momentum premia are high across all the '
                                 'asset classes in this long sample period'},
])
check('无关内容不误报', ok2, [])
# 不配对 $ 不得吞掉文字（TimeSeriesMomentum 曾因该缺陷漏检）
unbalanced = [
    {'index': 0, 'page': 1, 'md': 'we estimate $alpha and beta is consistent '
                                 'with the theories mentioned above in '
                                 'addition we find that momentum captures'},
    {'index': 1, 'page': 2, 'md': 'is consistent with the theories mentioned '
                                 'above in addition we find that momentum '
                                 'captures individual stock returns'},
]
check('不配对$仍能检出重复', len(M._find_duplicate_blocks(unbalanced)), 1)

# 原文本身重复（PDF 侧也能找到 >=2 次）-> 报 REPEATED_IN_SOURCE，勿误导删除
pdf_w = M._dup_words(blocks[0]['md'] + ' ' + blocks[1]['md'])
issues_src = M._find_duplicate_blocks(blocks, pdf_words=pdf_w)
check('原文重复 -> REPEATED_IN_SOURCE',
      issues_src[0]['kind'] if issues_src else '', 'REPEATED_IN_SOURCE')
issues_conv = M._find_duplicate_blocks(blocks, pdf_words=M._dup_words('nothing'))
check('PDF 侧无重复 -> DUPLICATE_CONTENT', issues_conv[0]['kind'], 'DUPLICATE_CONTENT')

print(f'\n{"全部通过" if fails == 0 else f"{fails} 项失败"}')
sys.exit(1 if fails else 0)