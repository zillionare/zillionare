---
title: "[1020] QuanTide Weekly"
date: 2024-10-20
category: others
slug: quantide-weekly-1020
img: https://images.jieyu.ai/images/university/toronto.webp
stamp_width: 60%
stamp_height: 60%
tags: [others, weekly, numpy, pandas]
seq: 第 13 期
fonts:
    sans: 'ZhuqueFangsong, sans-serif'
---

### 本周要闻
* 幻方量化宣布降低对冲全系产品投资仓位至0
* 9月CPI、PPI及前三季度GDP数据出炉
* 潘功胜发声，宏观经济政策应更加重视消费


### 下周看点
* 周一：最新LPR报价
* 周二：华为原生鸿蒙之夜新品发布会
* 周五：多家银行存量房贷利率调整
* 周日：全球低空经济论坛年会

### 本周精选

* 连载！量化人必会的 Numpy 编程(7)

---

* 宁波幻方量化公告，将逐步把对冲全系产品投资仓位降低至0，同时自10月28日起免除对冲系列产品后期的管理费。作出改变的原因是，市场环境变化，对冲系列产品难以同时取得收益和缩小风险敞口，潜在收益风险比明显下降，未来收益将明显低于投资人预期。建议投资者适时调整投资组合，市场低位较适合配置指数增强产品，在风险能力匹配前提下，对冲产品可转至多头。（财联社）
* 10月13日，国家统计局数据显示，9月份全国居民消费价格（CPI）环比持平，同比上涨0.4%，涨幅回落；工业生产者出厂价格（PPI）环比降幅收窄，同比降幅扩大。CPI、PPI同比表现均弱于市场预期。（证券时报网）
* 10月18日，统计局公布2024年9月经济数据，9月社零当月同比3.2%，固定资产投资累计同比3.4%，工增当月同比5.4%，三季度GDP同比4.6%。前三季度GDP累计同比4.8%。（财联社）
* 在10月18日的2024金融街论坛上，央行行长潘功胜重磅发声。谈及实现经济的动态平衡，需要把握好几个重点时，他提到宏观经济政策的作用方向应从过去的更多偏向投资，转向消费与投资并重，并更加重视消费。(财联社)


---


## Numpy量化应用案例[4]

### 突破旗形整理

最近和一位做量化的私募大佬聊了一下行情，他给我发了这张图片。

![75%](https://images.jieyu.ai/images/2024/10/roger-trend.jpg)

这个底部点位，他**又一次**精准命中了（3143那个点，不是3066。周五上证实际下探到3152点）。不过，我更好奇的是他的研究方法，也就图的下半部分。知道大致的底之后，再结合缺口、前低等一些信息，确实有可能比较精准地预测底部点位。

---

我当时就回了一句，最近忙着上课，等有时间了，把这个三角形检测写出来。

这个检测并不难，写一个教学示例，一个小时的时间足够了。

在分享我的算法之前，先推荐一个外网的[方案](https://www.youtube.com/watch?v=b5m7BZAHysk)。同样是教学代码，显然不如我随手写的优雅，先小小自得一下。不过，这样的好处就是，他的代码可能更容易读懂。

所谓旗形整理（或者说三角形检测），就是下面这张图：


![](https://images.jieyu.ai/images/2024/10/flag-pattern-1.jpg)


在这张图，每次上涨的局部高点连接起来，构成压力线；而下跌的局部低点连起来，构成支撑线。

如果我们再在开始的位置画一条竖线，就构成了一个小旗帜，这就是旗形的来由。

---

旗形整理的特别之处是，整理何时结束似乎是可以预测的，因为这两条线之间的交易空间会越来越窄。

**当它小于一个ATR时**，就是整理必须结束，即将选择方向的时候。

下图显示了随时间推移，震荡幅度越来越小的情况。

![75%](https://images.jieyu.ai/images/2024/10/flag-pattern-2.jpg)

最终，股价会选择方向。一旦选择方向，就往往会有一波较大的行情（或者下跌）：

![75%](https://images.jieyu.ai/images/2024/10/flag-pattern-3.jpg)

---

所以，能够自动化检测旗形整理，有以下作用：



1. 如果当前处理在旗形整理中，可以设定合理的波段期望。
2. 检测临近整理结束，可以减仓等待方向。
3. 一旦方向确定，立即加仓。

现在，我们就来看如何实现。首先，我们有这样一个标的：

![75%](https://images.jieyu.ai/images/2024/10/605158-1.png)

这是已经上涨后的。我们再来看它上涨前的：

![75%](https://images.jieyu.ai/images/2024/10/605158.png)


---

肉眼来看，一个旗形整理似有若无。

我们的算法分这样几步：

1. 找到每阶段的峰和谷的坐标
2. 通过这些坐标及它们的收盘价，进行趋势线拟合
3. 通过np.poly1d生成趋势线
4. 将趋势线和k线图画在一张图上

```python
def find_peak_pivots(df, win):
    local_high = (df.close.rolling(win)
                    .apply(lambda x: x.argmax()== win-1))
    local_high[:win] = 0
    
    # find_runs函数是量化24课内容
    v,s,l = find_runs(local_high)

    peaks = []
    i = 0
    while i < len(v):
        if l[i] >= win // 2:
            if s[i] > 0:
                peaks.append(s[i] - 1)
        for j in range(i+1, len(v)):
            if l[j] >= win // 2:
                peaks.append(s[j] - 1)
                i = j
        if j == len(v)-1:
            break

    return peaks
```

---

```python
def find_valley_pivots(df, win):
    local_min = (df.close.rolling(win)
                .apply(lambda x: x.argmin()== win-1))
    local_min[:win] = 0
    
    v,s,l = find_runs(local_min)

    valleys = []
    i = 0
    while i < len(v):
        if l[i] >= win // 2:
            if s[i] > 0:
                valleys.append(s[i] - 1)
        for j in range(i+1, len(v)):
            if l[j] >= win // 2:
                valleys.append(s[j] - 1)
                i = j
        if j == len(v)-1:
            break

    return valleys

def trendline(df):
    peaks = find_peak_pivots(df, 20)
    valleys = find_valley_pivots(df, 20)

    y = df.close[peaks].values
    p = np.polyfit(x=peaks, y = y, deg=1)
    upper_trendline = np.poly1d(p)(np.arange(0, len(df)))

    y = df.close[valleys].values
    v = np.polyfit(x=valleys, y = y, deg=1)
    lower_trendline = np.poly1d(v)(np.arange(0, len(df)))
```

---

```python
    candle = go.Candlestick(x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    line=dict({"width": 1}),
                    name="K 线",
                    increasing = {
                        "fillcolor":"rgba(255,255,255,0.9)",
                        "line": dict({"color": RED})
                    },
                    decreasing = {
                        "fillcolor": GREEN, 
                        "line": dict(color =  GREEN)
                    })
    upper_trace = go.Scatter(x=df.index, 
                             y=upper_trendline, 
                             mode='lines', 
                             name='压力线')

    lower_trace = go.Scatter(x=df.index, 
                             y=lower_trendline, 
                             mode='lines', 
                             name='支撑线')

    fig = go.Figure(data=[candle,lower_trace, upper_trace])

    fig.show()
```



最后，我们对该标的在上涨之前的形态进行检测，得到以下结果：

<img src="https://images.jieyu.ai/images/2024/10/flag-pattern-605148.png" style="position:relative;margin-top:-100px;z-index:-1; width:90%"/>

---

这个结果说明，旗形整理结束时，方向选择受大盘影响，仍有一定不确定性，但没有跌破前低，这是此后能凝聚共识、返身上涨的关键。

我们再来看一个最近一个月翻了7倍的标的：

<img src="https://images.jieyu.ai/images/2024/10/flag-pattern-830799-full-period.png" style="position:relative;margin-top:-100px;z-index:-1"/>

这是未上涨前的形态：

<img src="https://images.jieyu.ai/images/2024/10/flag-pattern-830179-before-advance.png" style="position:relative;margin-top:-100px;z-index:-1"/>

这是检测出来的旗形整理：

---

![](https://images.jieyu.ai/images/2024/10/flag-pattern-830179-detection.jpg)

完美捕捉！

当然，这里只是示例代码，在实际运用中，由于我们使用了小样本线性回归，回归结果具有不稳定性，要作为生产代码，还需要辅以其它方法让其预测更稳定。无论如何，我们已经迈出了关键一步。

代码(可运行的ipynb文件)放在知识星球里。正在建设，所以目前是最低价格。

![](https://images.jieyu.ai/images/hot/logo/zsxq.png)

如果有一些代码和术语看不明白（比如为何以ATR来决定整理结束），这些都是我们量化24课的内容，欢迎报名！

---

## 好课开讲！

![](https://images.jieyu.ai/images/hot/course/factor-ml/1.png)

---

## 目标清晰 获得感强

![](https://images.jieyu.ai/images/hot/course/factor-ml/2.png)

---

## 为什么选择QuanTide的课程？

![](https://images.jieyu.ai/images/hot/course/factor-ml/3.png)


