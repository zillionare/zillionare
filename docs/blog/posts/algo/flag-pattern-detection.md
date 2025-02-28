---
title: 烛台密码 三角形整理如何提示玄机
date: 2025-02-25
category: algo
slug: flag-pattern-detection
motto: 
img: https://images.jieyu.ai/images/2025/02/daniel-thomas.jpg
stamp_width: 60%
stamp_height: 60%
tags: [算法,模式识别]
---

<!--PAID CONTENT START-->
本文是几个月前《三角形整理检测》的后续篇，改进了算法，增加了应用场景的讨论。
<!--PAID CONTENT END-->

《匡醍.因子分析与机器学习策略》课程的最后一课是关于深度学习框架在量化交易中的应用的。考虑很多技术交易者都会看图操作，比如艾略特浪型、头肩顶、三角形整理等等。正好CNN在图像模式识别能力上超越了人类，所以，就打算拿三角形整理的检测作为例子。

要通过CNN网络来实现三角形整理检测，首先需要做到数据标注。我们在课程中已经实作出来一个标注工具。不过，我更希望能够使用算法自动检测到三角形整理模式。这篇文章就将介绍我的算法。

<!-- BEGIN IPYNB STRIPOUT -->

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/hot/logo/zsxq.png'>
<span style='font-size:0.6rem'></span>
</div>

如果你希望拿到本文源码，可以加入我们的星球。加入星球三天后，更可以获得我们研究平台的账号。在平台中提供了可以运行、验证notebook版本，你可以完全复现本文的结果。
<!-- END IPYNB STRIPOUT -->

!!! note
    <div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
    <img src='https://images.jieyu.ai/images/2025/02/matryoshka-doll.jpg'>
    <span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
    </div>
    先通过算法对k线图进行标注，再通过CNN网络进行识别，感觉这个有点Matryoshka doll了。于是我在课程中换了另一个例子，通过4 channel的一维卷积，实现了预测误差1%的准确率。这篇文章算是课程的边脚料重新加工了。

算法的示意图如下：

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/resist-support.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>三角形检测示意图</span>
</div>

首先，我们得找到k线图中的波峰和波谷。在图中，波峰是点1和2，波谷则是点3和4。然后我们作通过点1和2的直线，得到压力线；作通过点3和4的直线，得到支撑线。

在Python中，计算两点之间的直线可以通过np.polyfit来实现。通过该函数，将获得直线的斜率。通过两条直线之间的斜率关系，我们可以进一步得到三角形的形态。

如果记Sr为压力线的斜率，记Ss为支撑线的斜率，那么，三角形的形态可以由以下表格来定义：

| 压力线方向 | 支撑线方向 | 角度对比          | 标记 | 说明           |
| ---------- | ---------- | ----------------- | ---- | -------------- |
| Sr>0       | Ss>0       | abs(sr) > abs(ss) | 1    | 上升且发散三角 |
| Sr>0       | Ss>0       | abs(sr) < abs(ss) | 2    | 上升且收敛三角 |
| Sr>0       | Ss<0       | abs(sr) > abs(ss) | 3    | 发散偏上升三角 |
| Sr>0       | Ss<0       | abs(sr) < abs(ss) | 4    | 发散偏下降三角 |
| Sr<0       | Ss>0       | abs(sr) > abs(ss) | 5    | 下降且收敛三角 |
| Sr<0       | Ss>0       | abs(sr) < abs(ss) | 6    | 上升且收敛三角 |
| Sr<0       | Ss<0       | abs(sr) > abs(ss) | 7    | 下降且收敛三角 |
| Sr<0       | Ss<0       | abs(sr) < abs(ss) | 8    | 下降且发散三角 |

部分形态如下图所示：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/all-triangles.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

识别算法的实现代码如下：

```python
from zigzag import peak_valley_pivots

def triangle_flag(df, lock_date=None):
    if lock_date is not None:
        peroid_bars = df.loc[:lock_date]
    else:
        peroid_bars = df
        
    thresh = peroid_bars.close[-120:].pct_change().std() * 3
    
    pvs = peak_valley_pivots(peroid_bars.close.astype(np.float64), thresh, -1 * thresh)
    
    if len(pvs) == 0:
        return 0, None, None

    pvs[0] = pvs[-1] = 0
    pos_peaks = np.argwhere(pvs == 1).flatten()[-2:]
    pos_valleys = np.argwhere(pvs == -1).flatten()[-2:]

    if len(pos_peaks) < 2 or len(pos_valleys) < 2:
        return 0, None, None

    minx = min(pos_peaks[0], pos_valleys[0])
    y = df.close[pos_peaks].values
    p = np.polyfit(x=pos_peaks, y=y, deg=1)
    upper_trendline = np.poly1d(p)(np.arange(0, len(df)))

    y = df.close[pos_valleys].values
    v = np.polyfit(x=pos_valleys, y=y, deg=1)
    lower_trendline = np.poly1d(v)(np.arange(0, len(df)))

    sr, ss = p[0], v[0]

    flags = {
        (True, True, True): 1,
        (True, True, False): 2,
        (True, False, True): 3,
        (True, False, False): 4,
        (False, True, True): 5,
        (False, True, False): 6,
        (False, False, True): 7,
        (False, False, False): 8,
    }

    flag = flags[(sr > 0, ss > 0, abs(sr) > abs(ss))]

    return flag, upper_trendline, lower_trendline
```

<!--PAID CONTENT START-->
```python
def show_trendline(asset, df, resist, support, flag, width=600, height=400):
    desc = {
        1: "上升且发散三角",
        2: "上升且收敛三角",
        3: "发散偏上升三角",
        4: "发散偏下降三角",
        5: "下降且收敛三角",
        6: "上升且收敛三角",
        7: "下降且收敛三角",
        8: "下降且发散三角",
    }

    if isinstance(df, pd.DataFrame):
        df = df.reset_index().to_records(index=False)

    title = f"flag: {flag} - {desc[flag]}"
    cs = Candlestick(df, title=title, show_volume=False, show_rsi=False, width=width, height=height)
    cs.add_line("support", np.arange(len(df)), support)
    cs.add_line("resist", np.arange(len(df)), resist)
    cs.plot()


np.random.seed(78)
start = datetime.date(2023, 1, 1)
end = datetime.date(2023, 12, 29)
barss = load_bars(start, end, 4)

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df)
    if flag != 0:
        show_trendline(key, df, resist, support, flag)
```
<!--PAID CONTENT END-->

最后，我们来研究一支个股的情况，看看这个算法可能有哪些用途：

<!--PAID CONTENT START-->
```python
start = datetime.date(2023, 1, 1)
end = datetime.date(2023, 12, 29)
barss = load_bars(start, end, ("300814.XSHE", ))

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df, datetime.date(2023, 9, 11))
    if flag != 0:
        show_trendline(key, df, resist, support, flag, width=800, height=600)
```
<!--PAID CONTENT END-->


<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/300814.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

标的从23年4月19日以来，先后出现4次波峰。随着时间的推移，整理形态也不断变化。

7月12，突破之前的形态是发散偏上升三角。

<!--PAID CONTENT START-->
```python
start = datetime.date(2022, 12, 1)
end = datetime.date(2023, 10, 29)
barss = load_bars(start, end, ("300814.XSHE", ))

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df, datetime.date(2023, 7,19))
    if flag != 0:
        show_trendline(key, df, resist, support, flag, width=800, height=600)
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/300814-break-out.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

7月12日突破之后，支撑和压力线发生变化。此时可以计算出9月7日的压力位是48元。但当天只冲击到45.6，随后收了上影线。

<!--PAID CONTENT START-->
```python
start = datetime.date(2022, 12, 1)
end = datetime.date(2023, 10, 29)
barss = load_bars(start, end, ("300814.XSHE", ))

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df, datetime.date(2023, 8,19))
    if flag != 0:
        show_trendline(key, df, resist, support, flag, width=800, height=600)
```
<!--PAID CONTENT END-->


<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/300814-sep-6.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

此时仍然是上升三角，但9月7日未破压力位后，压力线应该使用最新的两个波峰连线。此时的压力线的斜率比之前的要小，显示后续走势会弱一些。

<!--PAID CONTENT START-->
```python
start = datetime.date(2022, 12, 1)
end = datetime.date(2023, 12,29)
barss = load_bars(start, end, ("300814.XSHE", ))

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df, datetime.date(2023, 9,15))
    if flag != 0:
        show_trendline(key, df, resist, support, flag, width=800, height=600)
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/300814-nov-20.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

在9月7日新的波峰形成后，新的压力线在11月20日的值为48.5，当天的最高点为46.4，再次未破压力位。此后压力线需要重新计算。新的压力线的斜率进一步减小。形态也由此前的上升且发散三角形，转换为上升且收敛三角形，表明已经到了退出的时间。

<!--PAID CONTENT START-->
```python
start = datetime.date(2022, 12, 1)
end = datetime.date(2023, 12,29)
barss = load_bars(start, end, ("300814.XSHE", ))

for key, df in barss.groupby("asset"):
    df = df.reset_index().set_index("date")
    flag, resist, support = triangle_flag(df)
    if flag != 0:
        show_trendline(key, df, resist, support, flag, width=800, height=600)
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/300814-dec-29.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

上述压力线斜率的变化能够表明价格上升是打开了新的通道，还是预期在走弱，这对我们中短线操作很有帮助。

在通过机器学习构建策略时，我们可以把压力线和支撑线斜率的变化($\delta{Sr}$, $\delta{Ss}$)、压力线和支撑线预测出来的值($P_{t+1}$, $V_{t_1}$)等作为特征，那么，我们就可能更精确地预测未来走势。


