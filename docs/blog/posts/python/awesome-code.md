---
title: 只廖廖数行，但很惊艳的代码
slug: awesome-code
date: 2023-12-19
categories:
    - python
tags:
    - quant
    - algorithm
    - python
---

既然c/java/python等语言的索引都从零开始，因此我们的盘点也从一行代码也没有的项目开始

## 0行: No Code

这个项目只有零行代码，具有轻量级、跨平台、全自动不可描述之美，一举斩获github 50k :star:

<!--more-->

!!! tip
    在 github 上有一个高达 50k stars 的项目，名为 [nocode](https://github.com/kelseyhightower/nocode)。它确实做到了不产生任何 bug：
    
    _No code is the best way to write secure and reliable applications. Write nothing; deploy nowhere._

    不写代码，就不会产生 bug，这真是极高的佛家智慧：菩提本无树，明镜亦非台，本来无一物，何处惹尘埃？不过，就是这样一个项目，还是被人提交了超过 3k 的 issues（当我们认为项目中存在 bug，或者有新的功能需求，就可以提出一个 issue），远超平均水平，这也算是程序员的幽默吧？

    <div style="text-align:right"> - 摘自《Python能做大项目》</div>

要评论这样的项目，也必须儒释道兼修之：

!!! quote
    空即是色 色即是空
    道可道 非常道 名可名 非常名
    道本无言 言说是妄
    阅尽天下码，心中已无码！


## 1行：雷神之锤

这行代码出现在游戏雷神之锤中，它是一个平方根倒数速算法，即求：

$$x^{\frac{-1}{2}}$$

这个函数一般人不大用得到，但在游戏中做光影跟踪是必备。具体来说，大家还是看图吧：

![](https://images.jieyu.ai/images/2023/12/quake-vector.png)

我也不想多解释了。看着这图，不像是做游戏，这简直就是程序员的头发。再研究多了，头发就更少了。

总之，这行牛x的代码是这样的：

```c
i  = 0x5f3759df - ( i >> 1 );
```

代码作者是约翰.卡马克。它的牛x之处，在于作者以近科拉马努金似的直觉，发现了 0x5f3759df 这个常数。这个算法后来还被chatGPT抄走了。


不过，既然咱们是讲量化的号，我们也讲一个量化中会用到的一行代码的例子。这个例子，在我们讲MPT那部分时提过。

## 1行：狄利克雷分布

在使用蒙特卡洛方法求解MPT的有效前沿时，我们需要生成无数权重向量。如果有n个资产，我们需要这样生成：

```python
import numpy as np

weights = np.array(np.random.random(len(stocks)))
weights = weights/np.sum(weights)  
```

第2行是必须的，因为我们要确保各项资产权重之和加起来为1。但我们可以使用狄利克雷分布一行代码搞定：

```python
from numpy.random import dirichlet

w = dirichlet(np.ones(n), n)
```

## 2行： shuffle

对于给定的 n 个元素，生成一个排列，使得每一个元素都能等概率地出现在每一个位置。这就是shuffle算法的魔力。

```java
for(int i = n - 1; i >= 0 ; i -- )
    // rand(0, i) 生成 [0, i] 之间的随机整数
    swap(arr[i], arr[rand(0, i)]) 
```

不过，相对于0和1行而言，这个算法朴素太多了。随机数生成、抽样在量化中使用得非常普遍。这里我们举一个偏应用一点的例子，


两行代码求出maxdrawdown的区间：

```python
import numpy as np
# close是收盘价序列
# 最大回撤结束的位置 最低的那个位置
i = np.argmax((np.maximum.accumulate(close) - close))
# 回撤开始的位置 最高的那个点
j = np.argmax(data['close'][:i])  
```

## ~~4行~~

发挥空间太大了，我们就不讲例子了。不过，这里给一个量化中常用的时间算法。我们在做特征提取、回测时常常要指定周期。在提取行情数据时，又需要知道起始时间，那么，在知道结束日期，要算出n个周期以前是哪个时间，怎么计算？

如果要求计算的是日线，这个计算不算复杂，但你必须有交易日历，这样才能排除掉休市日。

如果要求计算的是分钟线别的线，比如30分钟线，这个计算就比较复杂。我们不仅要考虑到休市日，还要考虑到跨天的情况。zillionare量化框架提供了一个空间换时间的算法。它先根据周期n，将30分钟的tick展开，并与日期合并，这样计算就变成了线性的：

```python
tm = moment.hour * 60 + moment.minute

new_tick_pos = cls.ticks[frame_type].index(tm) + n
days = new_tick_pos // len(cls.ticks[frame_type])
min_part = new_tick_pos % len(cls.ticks[frame_type])

```
---
---
```python
date_part = cls.day_shift(moment.date(), days)
minutes = cls.ticks[frame_type][min_part]
h, m = minutes // 60, minutes % 60

```

代码使用的ticks数组，在30分钟级别是这样的：

```
ticks = [600, 630, ..., 900]
```
600即早上10点。这里用了一个day_shift函数，它就是简单地使用交易日历进行搜索。最终我们还做了一个优化，通过求模运算代替了实际上的ticks数组展开，从而把空间也省了下来。这在`n`比较大的时候，还是非常有用的。

做量化会有不少底层工具函数要写，如果自己没时间，也可以参考zillionare量化框架的代码。





