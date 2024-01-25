---
title: 来自世坤！寻找Alpha 构建交易策略的量化方法
slug: finding-alphas-a-quantitative-approach
date: 2024-01-24
categories: 
    - books
motto: 谁终将声震人间，必长久深自缄默；谁终将点燃闪电，必长久如云漂泊
lunar:
img: https://images.jieyu.ai/images/2024/01/kitty-in-basket.jpg
tags: 
    - books
    - quant
---

问：常常看到有人说Alpha seeking，这究竟是什么意思？

推荐这本《Finding Alphas: A Quantitative Approach to Building Trading Strategies》。我拿到的PDF是2019年的第二版。来自WorldQuant（世坤）的Igor Tulchinshky。

<!--more-->
---

Alpha起源于60年代的资本资产定价模型（CAPM）理论。该理论认为，股票的预期回报由无风险利率，alpha回报以及市场风险暴露（即beta回报）共同构成。Alpha是股票回报的驱动因素。

关于Alpha的起源及定义，还有其它一些说法。比如今天推荐的这本书认为，Alpha起源于芝加哥大学的经济学博士Michael Jensen于1968年发表的一篇论文。在该论文中他使用了Jensen's Alpha一词，用以描述组合的风险调整收益，并确定其是否优于市场预期。实际上，这似乎与CAPM的Alpha并无不同。

世坤定义的Alpha，则是一种可以为投资组合增值的交易信号，甚至是算法、源代码及配置参数的组合！QuantPian的因子分析框架Alphalens，也包含了寻找Alpha、即寻找交易信号的含义。

这本书不到300页，比较适合入门。它介绍了如何设计Alpha因子，如何评估因子（IR,IC,换手率等）。在第15章和第16章介绍了如何使用机器学习，自动搜索因子。

从18章开始，具体介绍了各种场景下的因子设计，比如基本面的、动量因子、日内、事件驱动因子等等。

这本书谈方法比较多，比较适合入门，有了一个全貌之后，再看Zura Kakushadze的《101 Formulaic Alphas》，它的代码会多一点（伪代码）。

这本书没有中文版。如果像我一样习惯看中文，可以在firefox中安装一个名为“沉浸式翻译”的扩展。它可以翻译PDF文档，并且分两列对照展示。

---

<div style="display:flex;">
<div style="flex:50%; ">
<img src="https://images.jieyu.ai/images/2024/01/finding-alphas.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://images.jieyu.ai/images/2024/01/finding-alphas-toc-1.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://images.jieyu.ai/images/2024/01/finding-alphas-toc-2.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://images.jieyu.ai/images/2024/01/finding-alphas-toc-3.jpg" style="height:200px"/>
</div>
</div>

[下载 PDF](/assets/ebooks/finding-alphas-a-quantitative-approach-to-building-trading-strategies.pdf)
