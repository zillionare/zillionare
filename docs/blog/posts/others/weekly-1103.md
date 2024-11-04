---
title: "[1103] QuanTide Weekly"
date: 2024-11-03
category: others
slug: quantide-weekly-1103
img: https://images.jieyu.ai/images/2024/10/larry-willimans-card.jpg
stamp_width: 60%
stamp_height: 60%
tags: [others, weekly, factor]
seq: 第 15 期
fonts:
    sans: 'ZhuqueFangsong, sans-serif'
---

### 本周要闻
* 英伟达和宣伟公司纳入道指
* 制造业PMI时隔5个月重返景气区间
* 三季报收官，8成上市公司实现盈利


### 下周看点
* 周二：美国大选投票日（美东时间）
* 周二：财新发布10月服务业PMI
* 4日-8日，人常会：增量政策工具或将揭晓
* 周六：统计局发布10月PPI/CPI

### 本周精选

1. 一门三杰！一年翻十倍的男人发明了 UO 指标
2. 世界就是一个波函数：直流分量差分因子获得15.%年化

---

* 道琼斯指数发布公告，将英伟达和全球涂料供应商宣伟公司纳入道琼斯工业平均指数。英伟达将取代英特尔，宣伟将取代陶氏化学。
* 统计局发布，10月份制造业PMI 50.1%，环比上升0.3。这是制造业PMI连续5个月运行在临界点以下后重新回到景气区间。
* 统计数据显示，近八成上市公司前三季度实现盈利，近五成实现净利润正增长。消费品行业呈现明显修复态势，高技术制造业经营具有韧性，农林牧渔、非银金融、电子、社会服务等行业净利润增幅居前，同比增速达507%、42%、37%、30%。

* 人大常会会11月4日至8日在北京举行，前期财政部提及的一次性新增债务额度和“不仅于此”的增量政策工具，或者将在本次会议上揭晓答案。

<claimer>根据财联社、东方财富、证券时报等资讯汇编</claimer>

---

# 一年十倍男发明了UO

![Larry Williams，1987 年世界期货交易大赛冠军](https://images.jieyu.ai/images/2024/10/larry-willimans-card.jpg)

指标 Ultimate Oscillator（终极振荡器）是由 Larry Williams 在 1976 年发表的技术分析因子。

Larry 是个牛人，不打嘴炮的那种。他发明了 William's R（即 WR）和 ultimate ocsillator 这样两个指标。著有《我如何在去年的期货交易中赢得百万美元》一书。他还是 1987 年世界期货交易大赛的冠军。在这场比赛中，他以 11.37 倍回报获得冠军。

更牛的是，在交易上，他们家可谓是一门三杰。

---

<div style='width:50%;float:right;padding: 0.5rem 0rem 0 1rem;text-align:center'>
<img src='https://images.jieyu.ai/images/2024/10/michell-williams.jpg'>
<span style='font-size:0.6rem'>Michelle Williams</span>
</div>

这是他女儿，michelle williams。她是知名女演员，出演过《断臂山》等名片，前后拿了 4 个奥斯卡最佳女配提名。更厉害的是，她在 1997 年也获得了世界期货交易大赛的冠军，同样斩获了 10 倍收益。在这个大赛的历史上，有这样收益的，总共只有三人，他们家占了俩。

这件事说明，老 williams 的一些交易技巧，历经 10 年仍然非常有效。

<div style='width:72%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/worldcupchanpion-michelle-larry.jpg'>
<span style='font-size:0.6rem'></span>
</div>

Larry Williams 的儿子是位心理医生，著有《交易中的心理优势》一书。近水楼台先得月，身边有两位世界冠军，确实不愁写作素材。

---

这是指标的计算公式。

$$
\text{True Low} = \min(\text{Low}, \text{Previous Close}) \\
\text{True High} = \max(\text{High}, \text{Previous Close}) \\
\text{BP} = \text{Close} - \text{True Low} \\
\text{True Range} = \text{True High} - \text{True Low} \\
\text{Average BP}_n = \frac{\sum_{i=1}^{n} BP_i}{\sum_{i=1}^nTR_i} \\
ULTOSC_t=\frac{4Avg_t(7) + 2Avg_t(14) + Avg_t(28)}{4+2+1} \times 100
$$


它旨在通过结合不同时间周期的买入压力来减少虚假信号，从而提供更可靠的超买和超卖信号。Ultimate Oscillator 考虑了三个不同的时间周期，通常为 7 天、14 天和 28 天，以捕捉短期、中期和长期的市场动量。

这个公式计算步骤比较多，主要有 true low, true high 和 true ange, bull power 等概念。

用这个图来解释会更清楚。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/ultimate-oscillator.jpg'>
<span style='font-size:0.6rem'></span>
</div>


---

所谓的 true range，就是把前收也考虑进行，与当天的最高价、最低价一起，来求一个最大振幅。然后计算从 true low 到现价的一个涨幅，作为看涨力道（Bull Power）。

最后，用**看涨力道**除以**真实波幅**，再在一定窗口期内做平均，这样就得到了归一化的看涨力道均值。

最后，它结合长中短三个周期平均，生成最终的指标。

从构造方法来讲，它与 RSI 最重要的区别是，加入了 high 和 low 两个序列的数据。

做过交易的人知道，关键时刻最高价和最低价，都是多空博弈出来的，它是隐含了重要信息的。如果实时盯过盘口的人，可能感受更深。

像最高点，它是主力一口气向上吃掉多少筹码才拿到的这个最高点。**上面的筹码吃不掉，最高价就定在这个地方。吃不掉的筹码是更大的资金的成本或者其它什么心理价位，就是未来的压力位**。

因此，ultimate oscillator 与 RSI 相比，是包含了更多的信息量的。希望这部分解读，能对大家今后探索因子起到一定的启迪作用。

这个图演示了实际中的 uo 指标，看起来是什么样的。从视觉上看起来，它跟 RSI 差不多，都是在一定区间震荡的。

---

![](https://images.jieyu.ai/images/2024/10/ultimate-oscillator-visualize.jpg)


这个因子在回测中的表现如何？在回测中，从 2018 年到 2023 年的 6 年中，它的 alpha 年化达到了 13.7%，表现还是很优秀的。

![](https://images.jieyu.ai/images/2024/10/uo-alpha.jpg)

不过因子收益主要由做空贡献。大家看这张分层收益图，收益主要由第 1 层做空时贡献。在纯多的情况下，alpha 并不高，只有 1.6%，收益主要由 beta 贡献，所以组合收益的波动比较大。

<div style='width:90%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/uo-quantile-returns.jpg'>
<span style='font-size:0.6rem'></span>
</div>

---

所以，这个指标在期货上会更好使。

在多空组合下，6 年的收益达到了 2.2 倍。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/uo-cumulative-returns.jpg'>
<span style='font-size:0.6rem'></span>
</div>


最后我们看一下因子密度分布图。看上去很符合正态分布，尽显对称之美。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/uo-factor-distplot.jpg'>
<span style='font-size:0.6rem'></span>
</div>


从分层均值收益图来看，我们在交易中还可以做一点小小的优化，就是淘汰第8层之上的因子。这样调优之后，在2018年到2022年间，年化Alpha达到了24%，5年累计收益达到了2.75倍。

---

我们保留了2023年的数据作为带外数据供测试。在这一年的回测中，年化Alpha达到了13%，表明并没有出现过拟合。2023年的累计收益曲线如下：

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/ultimate-oscillator-2023-cum-returns.jpg'>
<span style='font-size:0.6rem'></span>
</div>


同期沪指是以下跌为主。8月底开启的上涨，在时间上与DMA策略上涨巧合了。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/sh-2023-plot.jpg'>
<span style='font-size:0.6rem'></span>
</div>


---

# 世界就是一个波函数

从直觉上看，使用波谱分析的方法来构建因子非常自然。因为经济是有周期的，交易更是有周期的。不过在量化交易中运用波谱分析，有它的难度。

以人声的波谱分析来说，它的频率有着固定的范围，能量也有固定的范围，换句话说，它们是平稳序列。但证券价格不是。我们多次讲过这个观点，股票价格是震荡向上的随机序列，只要国家经济还在发展，因此它不是平稳的。

但我们总能找到一种方法来分析问题。

## 波谱变换

我们先简单地介绍波谱变换。

```python
fft_result = np.fft.fft(close)
freqs = np.fft.fftfreq(len(close))

# 逆傅里叶变换
filtered = fft_result.copy()
filtered[20:] = 0
inverse_fft = np.fft.ifft(filtered)
inversed = pd.Series(inverse_fft.real, index=close.index)
```

---

```python
# 绘制原始信号和分解后的信号
plt.figure(figsize=(14, 7))
plt.plot(close, label='Original Close')
plt.plot(inversed, label='Reconstructed from Sine Waves')
plt.legend()
```


第一行代码是将时间序列变换成频谱，也就是所谓的时频变换。变换后的结果是一个复数数组，其中实部是频谱，虚部是频谱的偏移。

该数组是按频率由小大到排列的，也就是数组的开始部分是低频信号，结尾部分是高频信号。元素的取值是该信号的能量。一般我们把高频信号当成时噪声。 在这个数组当中零号元素有特殊的含义，它的频率是零赫兹，也就是它是一种直流分量。

第一行是生成频率的代码。注意它只与时间序列本身的长度有关系。也就是一个序列如果长度为30个时间单位，那么我们认为它的最高频率是30次。至于该频率实际上有没有信号，要看前一个数组对应位置的数值，如果是非零，就认为该频率的波存在。

第6~第8行是对转换后的频率信号进行简单处理。我们将20号以后的数组元素置为零。这样就实现了滤波。

然后我们通过ifft将处理后的信号逆变换回来，再重建时间序列。

---

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/10/fft-and-revert-it-back.jpg'>
<span style='font-size:0.6rem'></span>
</div>

我们看到图像更平滑了。所以这也是一种均线平滑的方法。好，关于FFT我们就介绍到这里。

## 直流分量的解释

现在我们思考一个问题，将价格序列进行时频变换后，得到的直流分量，意味着什么？

这里有一个猜想，如果我们把一次振动看成一次交易 -- 买入时导致股价上升，卖出时导致股价下跌回到起点 -- 这就是一种振动，对吧？

那么，高频振动就对应着高频交易，低频振动就对应着低频交易。如果在该窗口期没有做任何交易的资金，它们就是长线资金，是信号中的直流分量。直流分量的能量越大，高频振动的能量越小，股价就越稳定。

现在，我们再进一步思考，如果在t0期直流分量的能量为e0，在t1期的能量变为e1，那么，两者的差值意味着什么？

---

这就意味着有新的长线资金（超过窗口期）进来了。那么，股价就应该看涨。

## 直流分量差分因子

这个因子的原理是把股价当成一种波动，对它按30天为滑动窗口，进行波谱分析，提取直流分量（即频率为0的分量）的差分作为因子。

```python
def calc_wave_energy(df, win):
    close = df.close / df.close[0]
    dc = close.rolling(win).apply(lambda x: np.fft.fft(x)[0])
    return-1 * dc.diff()

np.random.seed(78)
_ = alphatest(2000, start, end, calc_factor=calc_wave_energy, args=(30,), top=9)
```


这是年化Alpha，很意外我们就得到了17%的年化：

|                                               | 1D     | 5D     | 10D    |
| --------------------------------------------- | ------ | ------ | ------ |
| Ann. alpha                                    | 0.170  | 0.144  | 0.114  |
| beta                                          | 0.022  | 0.030  | 0.040  |
| Mean Period Wise Return Top Quantile (bps)    | 2.742  | 2.512  | 2.042  |
| Mean Period Wise Return Bottom Quantile (bps) | -9.614 | -8.516 | -7.270 |
| Mean Period Wise Spread (bps)                 | 12.355 | 11.178 | 9.473  |


我们再来看分层收益均值图。我们从未得到过如此完美的图形。它简直就像是合成出来的。

---

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/11/fft-mean-wise-quantile.png'>
<span style='font-size:0.6rem'></span>
</div>

近20年累计收益17.5倍。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/11/fft-cumlative-returns.png'>
<span style='font-size:0.6rem'></span>
</div>

在《因子分析与机器学习》课程中，我们批露了更多高效率因子，并且深入浅出地讲解了因子分析和机器学习构建量化交易策略的原理，快来一起学习吧。

