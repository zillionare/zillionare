---
title: "[0901] QuanTide Weekly"
date: 2024-09-01
category: others
slug: quantide-weekly-0901
img: 
stamp_width: 60%
stamp_height: 60%
tags: [others, weekly, numpy, pandas]
seq: 第 7 期
---

### 本周要闻

* 市场传闻存量房贷利率下调，房地产 ETF 大涨，但尾盘多股炸板
* 中国 8 月官方制造业 PMI 为 49.1% 比上月下降 0.3 个百分点
* 国家市监总局宣布阿里整改完成
* 半年报第一股！桐昆股份同比增长 911.35%，为已发布半年报公司中净利润增速最高。

### 下周看点
* 下调存量房贷利率传闻能否兑现？
* 周一财新制造业 PMI 发布
* 周五，2024 低空经济发展大会将于 9 月 6 日至 8 日在芜湖举行

### 本周精选

* 主力正在进场？快速傅里叶变换与股价预测研究
* 连载！量化人必会的 Numpy 编程 (1)

---

## 本周要闻

* 市场传出的信息，有关方面正在考虑进一步下调存量房贷利率，允许规模高达 38 万亿元人民币的存量房贷寻求转按揭，以降低居民债务负担、提振消费。<remark>截至周六，上述传闻并未获得官方证实。</remark>
* 8 月份，PMI 为 **49.1%**，环比下降 0.3 个百分点。从企业规模看，大型企业 PMI 为 50.4%，仍高于临界点；中、小型企业 PMI 分别为 48.7%和 46.4%，环比下降 **0.7** 和 0.3 个百分点。<remark>8 月 PMI 受高温天气影响，并未显著超预期</remark>
* 8 月 30 日下午，国家市场监督管理总局宣布阿里巴巴完成三年整改，取得良好成效。阿里巴巴股价从 2020 年峰值以来，跌去七成。
* 美东时间周五，美股三大指数集体收涨，道指收涨 0.55%，报 41563.08 点，**创历史新高**。标普 500 上涨 1.01%，纳斯达克上涨 1.13%。美联储青睐的 7 月份 PCE 通胀数据基本符合预期，市场押注 9 月美联储大幅降息的可能性减少，但市场仍然预计 11 月或 12 月可能会有大幅降息。
* 易方达纳斯达克 100ETF 发布 2024 年中期报告，常州投资集团持有 5.92%份额，成为第一大持有人。该 ETF 在去掉净值上涨 49.21%的情况下，今年仍上涨 14.91%。该 ETF2017 年发行，现净值 3.16。
* 半年报第一股！桐昆股份发布半年报，公司实现净利润 10.65 亿元，同比增长 911.35%，为已发布半年报公司中净利润增速最高。报告期内，涤纶长丝行业下游需求较去年同期边际改善显著，产品销量与价差有所增大，**行业整体处于复苏状态**。整体看，电子行业成大赢家，与上年同期相比，电子行业营收增速高居首位，上半年整体营收为 1.59 万亿元，同比增长 17.3%。

<claimer>信息来源：东方财富网站</claimer>

---

## 下周看点
* 周五市场传闻，下调存量房贷利率正在考虑中，随即房地产 ETF 大涨，银行股大跌以回应传闻，但尾盘回落，涨停个股纷纷炸板。下周，此传闻是被证实还是被证伪？或将对市场有重要影响。
* 周一财新制造业 PMI 发布
* 周五，2024 低空经济发展大会将于 9 月 6 日至 8 日在芜湖举办
* 周五，美国 8 月失业率和非农报告公布

---

# 主力正在进场？快速傅里叶变换与股价预测研究

一个不证自明的事实：经济活动是有周期的。但是，这个事实似乎长久以来被量化界所忽略。无论是在资产定价理论，还是在趋势交易理论中我们几乎都找不到周期研究的位置 -- 在后者语境中，大家宁可使用“摆动”这样的术语，也不愿说破“周期”这个概念。

这篇文章里，我们就来探索股市中的周期。我们将运用快速傅里叶变换把时序信号分解成频域信号，通过信号的能量来识别主力资金，并且根据它们的操作周期进行一些预测。最后，我们给出三个猜想，其中一个已经得到了证明。

## FFT - 时频互转

（取数据部分略）。

我们已经取得了过去一年来的沪指。显然，它是一个时间序列信号。傅里叶变换正好可以将时间序列信号转换为频域信号。换句话说，傅里叶变换能将沪指分解成若干个正弦波的组合。

```python
# 应用傅里叶变换
fft_result = np.fft.fft(close)
freqs = np.fft.fftfreq(len(close))

# 逆傅里叶变换
filtered = fft_result.copy()
filtered[20:] = 0
inverse_fft = np.fft.ifft(filtered)
```

---

```python
# 绘制原始信号和分解后的信号
plt.figure(figsize=(14, 7))
plt.plot(close, label='Original Close')
plt.plot(np.real(inverse_fft), label='Reconstructed from Sine Waves')
plt.legend()
```

我们得到的输出如下：

![](https://images.jieyu.ai/images/2024/08/real-vs-synthetic.jpg)

在数字信号处理的领域，时间序列被称为时域信号，经过傅里叶变换后，我们得到的是频域信号。时域信号与频域信号可以相互转换。Numpy 中的 fft 库提供了 fft 和 ifft 这两个函数帮我们实现这两种转换。

np.fft.fft 将时域信号变换为频域信号，转换的结果是一个复数数组，代表信号分解出的各个频率的振幅 -- 也就是能量。频率由低到高排列，其中第 0 号元素的频率为 0，是直流分量，它是信号的均值的某个线性函数。

np.ff.ifft 则是 fft 的逆变换，将频域信号变换为时域信号。

将时域信号变换到频域，就能揭示出信号的周期性等基本特征。我们也可以对 fft 变换出来的频域信号进行一些操作之后，再变换回去，这就是数字信号处理。

---

## 高频滤波和压缩

如果我们把高频信号的能量置为零，再将信号逆变换回去，我们就会得到一个与原始序列相似的新序列，但它更平滑 -- 这就是我们常常所说的低通滤波的含义 -- 你熟悉的各种移动平均也都是低通滤波器。

![](https://images.jieyu.ai/images/hot/course/factor-ml-promotion.png)

在上面的代码中，我们只保留了前 20 个低频信号的能量，就得到了与原始序列相似的一个新序列。如果把这种方法运用在图像领域，这就实现了有损压缩 -- 压缩比是 250/20。

在上世纪 90 年代，最领先的图像压缩算法都是基于这样的原理 -- 保留图像的中低频部分，把高频部分当成噪声去掉，这样既保留了图像的主要特征，又大大减少了要保存的数据量。

---

当时做此类压缩算法的人都认识这位漂亮的小姐姐 -- Lena，这张照片是图像算法的标准测试样本。在漫长的进化中，出于生存的压力，人类在识别他人表情方面进化出超强的能力。所以相对于其它样本，一旦压缩造成图像质量下降，肉眼更容易检测到人脸和表情上发生的变化，于是人脸图像就成了最好的测试样本。

<div style='width:50%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://images.jieyu.ai/images/2024/08/lena.jpg'>
<span style='font-size:0.6rem'>Lena </span>
</div>

Lena 小姐姐是花花公子杂志的模特，这张照片是她为花花公子 1972 年 11 月那一期拍摄的诱人照片的一小部分 -- 在原始的照片中，Lena 大胆展现了她诱人的臀部曲线，但那些不正经的科学家们只与我们分享了她的微笑 -- 从科研的角度来讲，这也是信息比率最高的部分。

无独有偶，在 Lena 成为数字图像处理的标准测试样本之前，科学家们一直使用的是另一位小姐姐的照片，也出自花花公子。

好，言归正传。我们刚刚分享了一种方法，去掉信号中的高频噪声，使得信号本身的意义更加突显出来。我们也希望在证券分析中使用类似的技法，使得隐藏在 K 线中的信号显露出来。

但如果我们照搬其它领域这一方法，这几乎就不算研究，也很难获得好的结果。实际上，在证券信号中，与频率相比，我们更应该关注信号的能量，毕竟，我们要与最有力量的人站在一边。

---

<div style='text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2024/08/may-the-force-be-with-you.jpg'>
<span style='font-size:0.6rem'>愿原力与你同在 -- 星球大战</span>
</div>

所以，我们换一个思路，把分解后的频域信号中，能量最强的部分保留下来，看看它们长什么样。

## 过滤低能量信号

```python
# 保留能量最强的前 5 个信号
amp_threshold = np.sort(np.abs(fft_result))[-11]

# 绘制各个正弦波分量
plt.figure(figsize=(14, 7))

theforce = []
for freq in freqs:
    if freq == 0:  # 处理直流分量
        continue
    elif freq < 0:
        continue
    else:
        amp = np.abs(fft_result[np.where(freqs == freq)])
        if amp < amp_threshold:
            continue
```

---

```python

        sine_wave = amp * np.sin(2 * np.pi * freq * np.arange(len(close)))
        theforce.append(sine_wave)
        plt.plot(dates, sine_wave, label=f'Frequency={freq:.2f}')

plt.legend()
plt.title('Individual Sine Wave Components')
ticks = np.arange(0, len(dates), 20)
labels_to_show = [dates[i] for i in ticks]
plt.xticks(ticks=ticks, labels=labels_to_show, rotation=45)
plt.show()
```

FFT 给出的频率总是一正一负，我们可以简单地认为，负的频率对我们没有意义，那是一种我们看不到、也无须关心的暗能量。所以，在代码中，我们就忽略了这一部分。

![](https://images.jieyu.ai/images/2024/08/individual-sine-wave.jpg)

我们看到，对沪指走势影响最强的波（橙色）的周期是 7 个月左右：从峰到底要走 3 个半月，从底到峰也要走 3 个半月。由于它的能量几乎是其它波的一倍，所以它是主导整个叠加波的走势的：如果其它波与它同相，叠加的结果就会使得趋势加强；反之，则是趋势抵消。其它几个波的能量相仿，但频率不同。

---

这些波倒底是什么呢？它可以是一种经济周期，但是说到底，经济周期是人推动的，或者反应了人的判断。因此，我们可以把波动的周期，看成**资金的操作周期**。

从这个分解图中，我们可以猜想，有一个长线资金（对应蓝色波段），它一年多调仓一次。有一个中线资金（对应橙色波段），它半年左右调一次仓。其它的资金则是短线资金，三个月左右就会做一次仓位变更。还有无数被我们过滤掉的高频波段，它们操作频繁，可能对应着散户，但是能量很小，一般都可以忽略；只有在极个别的时候，才能形成同方向的叠加，进而影响到走势。

现在，我们把这几路资金的操作合成起来，并与真实的走势进行对比，看看情况如何：

![](https://images.jieyu.ai/images/2024/08/real-vs-5-waves-synthetic.jpg)

在大的周期上都基本吻合，也就是这些资金基本上左右了市场的走势。而且，我们还似乎可以断言，在 3 月 15 到 5 月 17 这段时间，出现了股价与主力资金的背离趋势：主力资金在撤退了，但散户还在操作，于是，尽管股价还在上涨，但最终的方向，由主力资金来决定。

---

!!! tip
    黑色线是通过主力资金波段合成出来的（对未来有预测性），在市场没有发生根本性变化之前，主力的操作风格是相对固定的，因此，它可能有一定的短时预测能力。如果我们认可这个结论的话。那么就应该注意到，末端部分还存在另一个背离 -- 散户还在离场，但主力已经进场。当然，关于这一点，请千万不要太当真。

## 关于直流分量的解释

我过去一直以为直流分量表明资产价格的趋势，但实际上所有的波都是水平走向的 -- 但只有商品市场才是水平走向的，股票市场本质上是向上的。所以，直流分量无法表明资产价格的趋势。

直到今天我突然涌现一个想法：如果你把一个较长的时序信号分段进行 FFT 分解，这样会得到若干个直流分量。这些直流分量的回归线才是资产价格的趋势。

这里给出三个猜想：

1. 如果分段分解后，各个频率上的能量分布没有显著变化，说明投资者的构成及操作风格也没有显著变化，我们可以用 FFT 来预测未来短期走势，直到条件不再满足为止。
   

2. 沪指 30 年来直流分量应该可以比较完美地拟合成趋势线，它的斜率就等于沪指 20 年回归线的斜率。
3. 证券价格是直流分量趋势线与一系列正弦波的组合。

---

下面我们来证明第二个猜想（过程略）。最终，我们将直流分量及趋势线绘制成下图：

![75%](https://images.jieyu.ai/images/2024/08/dc-regression.jpg)

而 2005 年以来的 A 股年线及趋势线是这样的：

![75%](https://images.jieyu.ai/images/2024/08/a-share-yearly.jpg)

不能说十分相似，只能说几乎完全一致。

趋势线拟合的 p 值是 0.055 左右，也基本满足 0.05 的置信度要求。

---

这篇文章是我们《因子投资与机器学习策略》中的内容，出现在如何探索新的因子方法论那一部分。对 FFT 变换得到的一些重要结果，将成为机器学习策略中用以训练的特征。更多内容，我们课堂上见！

![](https://images.jieyu.ai/images/hot/course/factor-ml-promotion.png)

<!-- 如果不是读过达. 利欧的《原则》，我也几乎就要相信股价的波动与经济周期无关了。但是，一直有种微弱的信念，既然经济活动存在周期，证券价格的波动也必然存在周期 -->

---

# 量化人必会的 NUMPY 编程 (1) - 核心语法

## 1. 基本数据结构

NumPy 的核心数据结构是 ndarray（即 n-dimensional array，多维数组）数据结构。这是一个表示多维度、同质并且大小固定的数组对象。

ndarray 只能存放同质的数组对象，这样使得它无法表达记录类型的数据。因此，numpy 又拓展出了名为 structured array 的数据结构。它用一个 void 类型的元组来表示一条记录，从而使得 numpy 也可以用来表达记录型的数据。因此，在 Numpy 中，实际上跟数组有关的数据类型主要是两种。

前一种数组格式广为人知，我们将以它为例介绍多数 Numpy 操作。而后一种数据格式，在量化中也常常用到，比如，通过聚宽 [^聚宽] 的 jqdatasdk 获得的行情数据，就允许返回这种数据类型，与 DataFrame 相比，在存取上有不少简便之处。我们将在后面专门用一个章节来介绍。

在使用 Numpy 之前，我们要先安装和导入 Numpy 库：

```bash
# 安装 NUMPY
pip install numpy
```

---

一般地，我们通过别名`np`来导入和使用 numpy：

```python
import numpy as np
```

为了在 Notebook 中运行这些示例时，能更加醒目地显示结果，我们首先定义一个 cprint 函数，它将原样输出提示信息，但对变量使用红色字体来输出，以示区别：

```python
from termcolor import colored

def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", 'red') for item in args]
    print(formatter.format(*colorful))

# 测试一下 CPRINT
cprint("这是提示信息，后接红色字体输出的变量值：{}", "hello!")
```

接下来，我们将介绍基本的增删改查操作。

### 1.1. 创建数组

#### 1.1.1. 通过 Python List 创建
我们可以通过`np.array`的语法来创建一个简单的数组：

```python
arr = np.array([1, 2, 3])
cprint("create a simple numpy array: {}", arr)
```

在这个语法中，我们可以提供 Python 列表，或者任何具有 Iterable 接口的对象，比如元组。

#### 1.1.2. 预置特殊数组
很多时候，我们希望 Numpy 为我们创建一些具有特殊值的数组。Numpy 也的确提供了这样的支持，比如：

---

| 函数                | 描述                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| zeros<br>zeros_like | 创建全 0 的数。zeros_like 接受另一个数组，并生成相同形状和数据类型的 zeros 数组。常用于初始化。以下*_like 类推。 |
| ones<br>ones_like   | 创建全 1 的数组                                                                                                  |
| full<br>full_like   | 创建一个所有元素都填充为`n`的数组                                                                                |
| empty<br>empty_like | 创建一个空数组                                                                                                   |
| eye<br>identity     | 创建单位矩阵                                                                                                     |
| random.random       | 创建一个随机数组                                                                                                 |
| random.normal       | 创建一个符合正态分布的随机数组                                                                                   |
| random.dirichlet    | 创建一个符合狄利克雷分布的随机数组                                                                               |
| arange              | 创建一个递增数组                                                                                                 |
| linspace            | 创建一个线性增长数组。与 arange 的区别在于，此方法默认生成全闭区间数组。并且，它的元素之间的间隔可以为浮点数。   |

<!--还有一些比较小众的预置函数，比如 np.indices-->

```python
# 创建特殊类型的数组
cprint("全 0 数组：\n{}", np.zeros(3))
cprint("全 1 数组：\n{}", np.ones((2, 3)))
cprint("单位矩阵：\n{}", np.eye(3))
cprint("由数字 5 填充的矩阵：\n{}", np.full((3,2), 5))

cprint("空矩阵：\n{}", np.empty((2, 3)))
cprint("随机矩阵：\n{}",np.random.random(10))
cprint("正态分布的数组：\n{}",np.random.normal(10))
cprint("狄利克雷分布的数组：\n{}",np.random.dirichlet(np.ones(10)))
cprint("顺序增长的数组：\n{}", np.arange(10))
cprint("线性增长数组：\n{}", np.linspace(0, 2, 9))
```

!!! warning
    尽管 empty 函数的名字暗示它应该生成一个空数组，但实际上生成的数组，每个元素都是有值的，只不过这些值既不是 np.nan，也不是 None，而是随机值。我们在使用 empty 生成的数组之前，一定要对它进行初始化，处理掉这些随机值。
<!--
在这里，注意 empty 数组在打印时是有值的，这些值都是随机的。Numpy 提供 empty 函数主要是出于性能考虑。它使得我们可以快速构建一个数组，但可以在后面再来填充它的数值。但我们毕竟 empty 创建的数据存在随机值，所以，我们使用 empty 时一定要小心，很多情况下，我们会宁可使用 zeros，也不是 empty。
-->

---

生成正态分布数组很有用。我们在做一些研究时，常常需要生成满足某种条件的价格序列，再进一步研究和比较它的特性。

比如，如果我们想研究上升趋势和下降趋势下的某些指标，就需要有能力先构建出符合趋势的价格序列出来。下面的例子就演示了如何生成这样的序列，并且绘制成图形：

```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    axes[i].plot(close)
```

绘制的图形如下：

![](https://images.jieyu.ai/images/2024/04/same-vol-different-trend.jpg)

<!--
很多情况下我们需要生成正态分布数组。比如，我们想研究股价涨跌幅与波动率之间的关系，比如，股价持续上涨与持续下跌，会有同样的波动率吗？此时，我们可以从下跌-0.1，到上涨 0.1，中间以 0.05 为一档，造出若干个回报序列，再来求它们的波动率。此时就可以用：

```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    vol = round(np.std(r), 3)
    axes[i].set_title(f"vol={vol}")
    axes[i].plot(close)
```

这个例子就演示了如何通过收益数组生成价格序列。

结论是，持续上涨、持续下跌和横盘整理的序列，可以有同样的波动率。它的意义是什么呢？我们知道，绩优股常常是低波动率的。这给了我们一个比较好的起点，再加上其它的指标，我们就可以筛选出绩优股出来。当然，知道了波动率与涨跌的关系之后，我们就知道，反过来，低波动率的，不一定是绩优股。
-->

示例中还提到了 Dirichlet（狄利克雷）分布数组。这个数组具有这样的特点，它的所有元素加起来会等于 1。比如，在现代投资组合理论中的有效前沿优化中，我们首先需要初始化各个资产的权重（随机值），并且满足资产权重之和等于 1 的约束（显然！），此时我们就可以使用 Dirichlet[^dirichlet] 分布。

---

!!! info
    狄利克雷，德国数学家。他对数论、傅里叶级数理论和其他数学分析学领域有杰出贡献，并被认为是最早给出现代函数定义的数学家之一和解析数论创始人之一。
<!--当然我们也可以使用高斯分布，再将其正则化。-->

<!--
arange 数组类似 range 语法，将生成一个整数数组，而 linspace 将生成步幅为浮点数的数组。此外，一个是左闭右开区间，一个是两端闭合区间。linspace 有什么用？

这里举一个例子，判断均线走势。假设均线数组为 ma, 共 10 个数据，则 linspace(ma[0], ma[-1], 10) 为连接两端的弦。用 ma 数组减去弦数组，如果值为正，则均线在向下拐头，否则，均线为凹曲线，是向上拐头，处在加速上涨中。
-->
#### 1.1.3. 通过已有数组转换

我们还可以从已有的数组中，通过复制、切片、重复等方法，创建新的数组
```python
# 复制一个数组
cprint("通过 np.copy 创建：{}", np.copy(np.arange(5)))

# 复制数组的另一种方法
cprint("通过 arr.copy: {}", np.arange(5).copy())

# 使用切片，提取原数组的一部分
cprint("通过切片：{}", np.arange(5)[:2])

# 合并两个数组
arr = np.concatenate((np.arange(3), np.arange(2)))
cprint("通过 concatenate 合并：{}", arr)

# 重复一个数组
arr = np.repeat(np.arange(3), 2)
cprint("通过 repeat 重复原数组：{}", arr)

# 重复一个数组，注意与 NP.REPEAT 的差异
# NP.TILE 的语义类似于 PYTHON 的 LIST 乘法
arr = np.tile(np.arange(3), 2)
cprint("通过 tile 重复原数组：{}", arr)
```

!!! question
    np.copy 与 arr.copy 有何不同？在 Numpy 中还有哪些类似函数对，有何规律？

<!--
我们在数组复制时，使用了两种方法。一种是 np.copy，另一种，则是数组对象自身的 copy。这两种方法有何不同？
-->
---

注意在 concatenate 函数中，axis 的作用：

```python
arr = np.arange(6).reshape((3,2))

# 在 ROW 方向上拼接，相当于增加行，默认行为
cprint("按 axis=0 拼接：\n{}", np.concatenate((arr, arr), axis=0))
# 在 COL 方向上拼接，相当于扩展列
cprint("按 axis=1 拼接：\n{}", np.concatenate((arr, arr), axis=1))
```

### 1.2. 增加/删除和修改元素
Numpy 数组是固定大小的，一般我们不推荐频繁地往数组中增加或者删除元素。但如果确实有这种需求，我们可以使用下面的方法来实现增加或者删除：
<!--
如果要频繁地执行增加和删除数组元素这种会改变数组大小的操作，一般我们会使用 Python 的 list 作为数据结构，而不是使用 numpy 的 array.
-->

| 函数   | 使用说明                                                                                |
| ------ | --------------------------------------------------------------------------------------- |
| append | 将`values`添加到`arr`的末尾。                                                           |
| insert | 向`obj`（可以是下标、slicing）指定的位置处，插入数值`value`（可以是标量，也可以是数组） |
| delete | 删除指定下标处的元素                                                                    |

示例如下：

```python
arr = np.arange(6).reshape((3,2))
np.append(arr, [[7,8]], axis=0)
cprint("指定在行的方向上操作、n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr.reshape((3,2)), 1, -10)
cprint("不指定 axis，数组被扁平化：\n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr, 1, (-10, -10), axis=0)
cprint("np.insert:\n{}", arr)

arr = np.delete(arr, [1], axis=1)
cprint("deleting col 1:\n{}", arr)
```

<!--
append 默认就是在行的方向上进行操作，这里的 axis=0 可以省略
-->

---

!!! tip
    请一定运行一下这里的代码，特别是关于 insert 的部分，了解所谓的扁平化是怎么回事。
<!--
第 5~11 行代码对比了 insert 在指定 axis 和不指定 axis 下的不同行为。特别要注意，如果不指定 axis，则执行此操作后，数组将会被扁平化为一维数组，无论之前数组的维度如何。
-->

<!--
第 13 行演示了如何删除一个数组元素。注意第二个参数是要被删除的元素的坐标，它可以是标量、也可以是一个坐标数组或者切片
-->

<!--
注意在 numpy 中，多数操作都不会直接修改原数组，而是返回一个新的数组
-->

有时候我们需要修改个别元素的值，应该这样操作：

```python
arr = np.arange(6).reshape(2,3)

arr[0,2] = 3
```

这里涉及到如何定位一个数组元素的问题，也正是我们下一节的内容。

<!--
!!! warning
    在 Numpy 中，多数操作并不会在原数组上执行，而是会拷贝并返回一个新的数组。下面的例子提醒我们注意由此可能产生的问题：

    ```python
    data = np.array([("aaron", "label")], 
                    dtype=[("name", "O"), ("label", "O")])
    filter = data["name"] == "aaron"

    # AFTER THIS: AARON -> 100
    data["label"][filter] = 100

    # THIS WON'T CHANGE
    data[filter]["label"] = "blogger"
    ```
-->
### 1.3. 定位、读取和搜索

#### 1.3.1. 索引和切片

Numpy 中的索引和切片语法大致类似于 Python，主要区别在于对多维数组的支持：

```python
arr = np.arange(6).reshape((3,2))
cprint("原始数组：\n{}", arr)

# 切片语法
cprint("按行切片：{}", arr[1, :])
cprint("按列切片：{}", arr[:, -1])
cprint("逆排数组：\n {}", arr[: : -1])

# FANCY INDEXING
cprint("fancy index: 使用下标数组：\n {}", arr[[2, 1, 0]])

```

上述切片语法在 Python 中也存在，但只能支持到一维，因此，对下面的 Python 数组，类似操作会出错：

---

```python
arr = np.arange(6).reshape((3,2)).tolist()

arr[1, :]
```

提示 list indices must be integers or slices, not tuple。

<!--
在上面的代码中，我们还通过 tolist() 将 numpy 数组转换成为 Python list。在 Numpy 对象与 Python 对象之间的转换会经常发生，特别是时间对象之间的转换，需要熟练掌握。
-->

#### 1.3.2. 查找、筛选和替换

在上一节中，我们是通过索引来定位一个数组元素。但很多时候，我们得先通过条件运算把符合要求的索引找出来。这一节将介绍相关方法。

| 函数            | 使用说明                                                   |
| --------------- | ---------------------------------------------------------- |
| np.searchsorted | 在有序数组中搜索指定的数值，返回索引。                     |
| np.nonzero      | 返回非零元素的索引，用以查找数组中满足条件的元素。         |
| np.flatnonzero  | 同 nonzero，但返回输入数组的展平版本中非零的索引。         |
| np.argwere      | 返回满足条件的元素的索引，相当于 nonzero 的转置版本        |
| np.argmin       | 返回数组中最小元素的索引（注意不是返回满足条件的最小索引） |
| np.argmax       | 返回数组中最大元素的索引                                   |

```python

# 查找
arr = [0, 2, 2, 2, 3]
pos = np.searchsorted(arr, 2, 'right')
cprint("在数组 {} 中寻找等于 2 的位置，返回 {}, 数值是 {}", 
        arr, pos, arr[pos - 1])

arr = np.arange(6).reshape((2, 3))
cprint("arr[arr > 1]: {}", arr[arr > 1])

# NONZERO 的用法
mask = np.nonzero(arr > 1)
cprint("nonzero 返回结果是：{}", mask)
cprint("筛选后的数组是：{}", arr[mask])

# ARGWHERE 的用法
mask = np.argwhere(arr > 1)
cprint("argwere 返回的结果是：{}", mask)
```

---

```python
# 多维数组不能直接使用 ARGWHERE 结果来筛选
# 下面的语句不能得到正确结果，一般会出现 INDEXERROR
arr[mask]

# 但对一维数组筛选我们可以用：
arr = np.arange(6)
mask = np.argwhere(arr > 1)
arr[mask.flatten()[0]]

# 寻找最大值的索引
arr = [1, 2, 2, 1, 0]
cprint("最大值索引是：{}", np.argmax(arr))
```

使用 searchsorted 要注意，数组本身一定是有序的，不然不会得出正确结果。
<!--
为什么我们要讲这个函数？在熟悉了 Numpy 之后，大家可能会想把所有的数据都使用 numpy 数组来表示。我们通过这个例子提醒大家，numpy 中的搜索，由于没有索引，实际上会比较慢。只有在数据已经有序的情况下，它才能加快。因此，我们也不能把所有数据都用 Numpy 来表示。
-->

第 10 行到第 21 行代码，显示了如何查找一个数组中符合条件的数据，并且返回它的索引。

<!--
很多场景下，我们要关心的是符合条件的数据的位置，而不是它的取值。比如，在通达信公司中，有一个 barssince，就是要求自满足条件以来，经过了多少个 bar。这就是我们只关心索引位置的一例。
-->

argwhere 返回值相当于 nonzero 的转置，在多维数组的情况下，它不能直接用作数组的索引。请自行对比 nonzero 与 argwhere 的用法。

<!--
以 arg 开头的函数，不完全是为了返回索引值。比如 argsort 是用来进行排序的，但它返回的是排序后的索引，类似于 rank。但 rank 返回的是排名，argsort 返回的是索引

```python
import numpy as np

# 创建一个数组
arr = np.array([3, 1, 2])

# 使用 ARGSORT 获取排序后的索引
sorted_indices = np.argsort(arr)

# 再次使用 ARGSORT 获取排名
ranks = np.argsort(sorted_indices) + 1

print("Ranks:", ranks)
```
-->

在量化中，有很多情况需要实现筛选功能。比如，在计算上下影线时，我们是用公式$(high - max(open, close))/(high - low)$来进行计算的。如果我们要一次性地计算过去 n 个周期的所有上影线，并且不使用循环的话，那么我们就要使用 np.where, np.select 等筛选功能。

<!--单就这一功能而言，还有更高效地实现方式-->

下面的例子显示了如何使用 np.select 来计算上影线：

```python
import pandas as pd
import numpy as np

bars = pd.DataFrame({
    "open": [10, 10.2, 10.1],
    "high": [11, 10.5, 9.3],
    "low": [9.8, 9.8, 9.25],
    "close": [10.1, 10.2, 10.05]
})
```

---

```python
max_oc = np.select([bars.close > bars.open, 
                    bars.close <= bars.open], 
                    [bars.close, bars.open])
print(max_oc)

shadow = (bars.high - max_oc)/(bars.high - bars.low)
print(shadow)

```

np.where 是与 np.select 相近的一个函数，不过它只接受一个条件。

```python
arr = np.arange(6)
cprint("np.where: {}", np.where(arr > 3, 3, arr))
```

这段代码实现了将 3 以上的数字截断为 3 的功能。这种功能被称为 clip，在因子预处理中是非常常用的一个技巧，用来处理异常值 (outlier)。

但它没有办法实现两端截断。此时，但 np.select 能做到，这是 np.where 与 np.select 的主要区别：

```python
arr = np.arange(6)
cprint("np.select: {}", np.select([arr<2, arr>4], [2, 4], arr))
```
其结果是，生成的数组，小于 2 的被替换成 2，大于 4 的被替换成 4，其它的保持不变。

<!--
还有一种筛选，是从一个集合中随机筛选出若干样本，我们将在随机数一节中讲到。
-->

<!--
以上介绍的方法，无论是 indexing, slicing，最终都引导我们定位到数组的元素。显然，有了这个定位，我们就能修改数组元素。但是，这里也必须强调视图 (view) 和副本 (copy) 的概念。因为根据我们定位元素的方法的不同，我们得到的结果，可能是原数组的一个视图，也可能是原数组的一个副本。前者可以修改到原数组元素，后者的修改只能修改副本。

#### 视图和副本

Numpy 数组实际上是由两部分组成的，一个是包含实际数据元素的连续数据缓冲区；另一个则是关于数组的元数据。元数据包括数据类型、步幅和其他更容易操作 ndarray 的重要信息，比如 shape。

这种组织方式带来了一个好处，即有可能只更改某些元数据（比如数据类型和 shape），而不更改数据缓冲区，就可以以不同的方式访问和操作原数组，但看起来象是一个新的数组。这些新数组称为视图。

Numpy 中的多数定位操作会返回视图，但有一些则会返回原数组的 copy。规则是，基本索引总是创建视图。所以，我们可以这样修改一个数组：

```python
x = np.arange(10)

# 创建了一个视图
y = x[1:3]
x[1:3] = [10, 11]
```

现在 y 和 x[1:3] 持有相同的值。因此修改是改在原数据缓冲区上。

另一方面，高级索引总是创建副本，比如：

```python
x = np.arange(9).reshape(3,3)
cprint("原始数组、n{}", x)

y = x[[1, 2]]
cprint("高级索引创建了副本、n{}", y)

# 现在我们修改高级索引副本值
x[[1,2]] = [[10, 11, 12], [13, 14, 15]]
cprint("就地赋值改变了 x\n{}", x)

cprint("但 y 是副本、n{}", y)
cprint("副本的 base 属性{}", y.base)
cprint("视图的 base 属性{}", x[1:2].base)
```

上述示例中，比较难以理解的是第 8 行。我们要记住，这是所谓的 in-place 分配的一种情况，此时不会创建任何视图或副本。

示例中还给出了判断一个数组究竟是副本还是视图的标准。如果一个数组是视图，那么它的 base 会指向原数组。而副本的 base 会指向 None。

我们还会在介绍完 Structured array 之后，再介绍一个常见、但更容易犯错的例子。
-->

### 1.4. 审视 (inspecting) 数组
<!--了解 numpy 的 dtype 类型，shape、ndim、size 和 len 的用法。-->

当我们调用其它人的库时，往往需要与它们交换数据。这时就可能出现数据格式不兼容的问题。为了有能力进行查错，我们必须掌握查看 Numpy 数组特性的一些方法。

我们先如下生成一个简单的数组，再查看它的各种特性：

```python

arr = np.ones((3,2))
cprint("dtype is: {}", arr.dtype)
cprint("shape is: {}", arr.shape)
cprint("ndim is: {}", arr.ndim)
```

---

```python
cprint("size is: {}", arr.size)
cprint("'len' is also available: {}", len(arr))

# DTYPE
dt = np.dtype('>i4')
cprint("byteorder is: {}", dt.byteorder)
cprint("name of the type is: {}", dt.name)
cprint('is ">i4" a np.int32?: {}', dt.type is np.int32)

# 复杂的 DTYPE
complex = np.dtype([('name', 'U8'), ('score', 'f4')])
arr = np.array([('Aaron', 85), ('Zoe', 90)], dtype=complex)
cprint("A structured Array: {}", arr)
cprint("Dtype of structured array: {}", arr.dtype)
```

正如 Python 对象都有自己的数据类型一样，Numpy 数组也有自己的数据类型。我们可以通过`arr.dtype`来查看数组的数据类型。

<!--
这里我们是通过 np.ones 生成的数组，数组的各元素都是 1。注意我们得到的 dtype 是 np.float64，这也是 Numpy 中最常见的数据类型。
-->

从第 3 行到第 6 行，我们分别输出了数组的 shape, ndim, size 和 len 等属性。ndim 告诉我们数组的维度。shape 告诉我们每个维度的 size 是多少。shape 本身是一个 tuple, 这个 tuple 的 size，也等于 ndim。

size 在不带参数时，返回的是 shape 各元素取值的乘积。len 返回的是第一维的长度。

### 1.5. 数组操作
<!--介绍引起数组形状、size 等改变的相关操作-->

我们在前面的例子中，已经看到过一些引起数组形状改变的例子。比如，要生成一个$3×2$的数组，我们先用 np.arange(6) 来生成一个一维数组，再将它的形状改变为 (2, 3)。

另一个例子是使用 np.concatenate，从而改变了数组的行或者列。

#### 1.5.1. 升维
我们可以通过 reshape, hstack, vstack 来改变数组的维度：

---

```python

cprint("increase ndim with reshape:\n{}", 
        np.arange(6).reshape((3,2)))

# 将两个一维数组，堆叠为 2*3 的二维数组
cprint("createing from stack: {}", 
        np.vstack((np.arange(3), np.arange(4,7))))

# 将两个 （3，1）数组，堆叠为（3，2）数组
np.hstack((np.array([[1],[2],[3]]), np.array([[4], [5], [6]])))
```

#### 1.5.2. 降维

通过 ravel, flatten, reshape, *split 等操作对数组进行降维。
<!--很多操作，比如像 argwhere，会返回升维的结果，此时我们可能需要在使用前，对其降维-->

```python

cprint("ravel: {}", arr.ravel())

cprint("flatten: {}", arr.flatten())

# RESHAPE 也可以用做扁平化
cprint("flatten by reshape: {}", arr.reshape(-1,))

# 使用 HSPLIT, VSPLIT 进行降维
x = np.arange(6).reshape((3, 2))
cprint("split:\n{}", np.hsplit(x, 2))

# RAVEL 与 FLATTEN 的区别：RAVEL 可以操作 PYTHON 的 LIST
np.ravel([[1,2,3],[4, 5, 6]])
```

这里一共介绍了 4 种方法。ravel 与 flatten 用法比较接近。ravel 的行为与 flatten 类似，只不过 ravel 是 np 的一个函数，可作用于 ArrayLike 的数组。

通过 reshape 来进行扁平化也是常用操作。此外，还介绍了 vsplit, hsplit 函数，它们的作用刚好与 vstack，hstack 相反。

#### 1.5.3. 转置

此外，对数组进行转置也是此类例子中的一个。

---

比如，在前面我们提到，np.argwhere 的结果，实际上是 np.nonzero 的转置，我们来验证一下：

```python
x = np.arange(6).reshape(2,3)
cprint("argwhere: {}", np.argwhere(x > 1))

# 我们再来看 NP.NONZERO 的转置
cprint("nonzero: {}", np.array(np.nonzero(x > 1)).T)
```

两次输出结果完全一样。在这里，我们是通过`.T`来实现的转置，它是一个语法糖，正式的函数是`transpose`。

当然，由于 reshape 函数极其强大，我们也可以使用它来完成转置：

```python
cprint("transposing array from \n{} to \n{}", 
    np.arange(6).reshape((2,3)),
    np.arange(6).reshape((3,2)))
```

<about/>
