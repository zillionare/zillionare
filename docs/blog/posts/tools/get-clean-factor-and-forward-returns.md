---
title: 12个参数，48个组合，这么复杂的函数怎么学？
slug: get-clean-factor-and-forward-returns
date: 2024-07-26
category: tools
motto: Learning how to fall teaches you how to land.
img: https://images.jieyu.ai/images/hot/mybook/girl-on-sofa.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - 工具
    - quantlib
---

在Alphalens中，get_clean_factor_and_forward_returns函数自动实现了收益计算、分层、缺失值处理和标准化，大大简化了因子分析的工作。

但是，这个函数有12个参数， 48个参数组合，复杂度量指数远超McCabe博士提出的高风险区域50。加上不太懂因子分析的原理，初学者很容易在这一步就犯错，但却茫然无知。


这十二个参数可以归类为5组。factor与price参数作为数据输入，前面已经介绍过了。这里就不再显示了。


![](https://images.jieyu.ai/images/2024/07/get-clean-factor-and-forward-returns-group-params.jpg)


通过这些参数的控制，就可以让Alphalens帮我们完成收益计算、分层、缺失值处理和标准化。

这些功能在整个因子分析体系中的位置如下：


![](https://images.jieyu.ai/images/2024/07/gcfafr-in-factor-analysis.png)
<cap>函数在体系中的位置与作用。计算前向收益等功能未绘出</cap>


<!-- draw group plot
<div class="text-2xl">

<v-drag pos="40,550,98,98">

<Ellipse/>
</v-drag>


<v-drag pos="180,400,120,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4 > 分组</Box>
</v-drag>

<v-drag pos="180,510,120,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > 缺失值</Box>
</v-drag>

<v-drag pos="180,620,120,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > 收益计算</Box>
</v-drag>

<v-drag pos="180,730,120,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > 分层</Box>
</v-drag>

<v-drag pos="620,280,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4 > zeroaware</Box>
</v-drag>

<v-drag pos="620,370,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4  > quantiles</Box>
</v-drag>

<v-drag pos="620,460,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4  > bins</Box>
</v-drag>

<v-drag pos="620,660,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > groupby</Box>
</v-drag>

<v-drag pos="620,750,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > groupby_labels</Box>
</v-drag>

<v-drag pos="620,840,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > binning_by_group</Box>
</v-drag>


<v-drag pos="350,370,230,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > max_loss</Box>
</v-drag>

<v-drag pos="350,480,230,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > filter_zscore</Box>
</v-drag>


<v-drag pos="350,640,230,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > periods</Box>
</v-drag>

<v-drag pos="350,750,230,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > cumulative_returns</Box>
</v-drag>
</div>

-->

分层行为由参数quantiles, bins和zeroaware来控制。quantiles与bins是互斥的参数，当我们指定bins时，需要把quantiles显著地置为None，才能使bins生效。

这篇文章主要讲解这两个参数，请看视频。

<iframe src="https://www.bilibili.com/video/BV1zJe9ebETH/?spm_id_from=333.999.0.0" class="w-800px h-400px"/>

<!--
zeroware用在这样的场合，如果因子是以零为中心并且分出多空信号的，我们一般就应该声明zeroware为True，以避免Alphalens把本该属于两种信号的因子归到一类中。

在分层的时候，我们还可通过分组参数，来控制分层是在组内进行，还是在整个Universe中进行。

收益计算主要由参数periods和cumulative_returns控制。

缺失值是这些参数中最容易理解的部分。max_loss决定了抛弃掉多少缺失值（比率）后，因子分析仍可继续进行。它的默认值是35%。filter_zscore是指因子值中，超过多个少标准差以外的值会被当成异常值抛弃掉。它的缺省值是20。看上去这个值设置得挺大的，这是因为一些财务数据之间的离差常常会很大。-->
