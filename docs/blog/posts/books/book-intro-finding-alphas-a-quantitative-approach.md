---
title: 来自世坤！寻找Alpha 构建交易策略的量化方法
slug: finding-alphas-a-quantitative-approach
date: 2024-01-25
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

自己回答不如推荐一本书：《Finding Alphas: A Quantitative Approach to Building Trading Strategies》，它的题目正好就是寻找Alpha。我拿到的PDF是2019年的第二版。来自WorldQuant（世坤）的Igor Tulchinshky等人，Igor Tulchinshky是世坤的创始人。

<!--more-->
---

Alpha起源于60年代的资本资产定价模型（CAPM）理论。该理论认为，股票的预期回报由无风险利率，alpha回报以及市场风险暴露（即beta回报）共同构成。Alpha是股票回报的驱动因素。

关于Alpha的起源及定义，还有其它一些说法。比如今天推荐的这本书认为，Alpha起源于芝加哥大学的经济学博士Michael Jensen于1968年发表的一篇论文。在该论文中他使用了Jensen's Alpha一词，用以描述组合的风险调整收益，并确定其是否优于市场预期。实际上，这似乎与CAPM的Alpha并无不同。

世坤定义的Alpha，则是一种可以为投资组合增值的交易信号，甚至是算法、源代码及配置参数的组合！QuantPian的因子分析框架Alphalens，也包含了寻找Alpha、即寻找交易信号的含义。

以上是我个人对Alpha的一些看法。这些知识点在我们的《量化24课》及最新的《因子分析与机器学习模型》中都有介绍。

下面就介绍下这本书。

这本书不到300页，比较适合入门。在前两章中介绍了Alpha和量化投资的简短历史。考虑到关于量化投资有很多以讹传讹的信息在广泛流传（正如我们已经看到的，什么是Alpha，就有好几种说法 -- 这还不包括所谓的Alpha策略），由Igor Tulchinshky作的序，无疑可以起到正本清源的作用。

在这两章中，EMH又一次被拿出来批判。他还实际上引用了格罗斯曼–斯蒂格利茨悖论来进行批判，但没有指出来这一观点实际上来自于格罗斯曼–斯蒂格利茨。在《量化24课》的导论中，我们可能对量化的历史发展进程发掘得更充分一些，在那里，我们是明确指出这个悖论直接导致了现代微观金融理论向行为金融学过渡的二次创业。这个导论是免费下载的，感兴趣的同学可以在我们网站上下载。

第一章介绍了如何设计Alpha的关键概念。比如如何评价一个好的Alpha：

- 简洁之美：alpha隐含的idea和数学表达都是简单的
- 样本内高夏普比率
- 对数据/参数的微小改变不敏感。注：这就是所谓的参数平原
- 在不同的universe都有效
- 在不同的股票市场都有效

这些提法比较抽象。在具体实践中，因子分析框架会用各种指标，比如IC, IR, 换手率等等从不现的方面来揭示Alpha的特质。

这一章还给出了挖掘Alpha的步骤：

1. 探索数据的分布
2. 获取一个idea
3. 用数学把idea变成股票持仓
4. 测试这个数学表达

在《因子分析与机器学习模型》中，我们是这样划分步骤的：

1. 获取原始数据
2. 提取因子
3. 因子预处理
4. 单因子检验

由因子到策略，还有一个因子组装问题，不过这已经是因子分析的手续步骤了。

第二章内容主要是回顾量化历史，讨论了Alpha是否存在，来源等等。这一章提到一个重要观点，是值得大家注意的。就是我们应该如何看待学术文献在量化中的作用。在寻找资产价格之间的合理关系时，学术文献一直并将继续是思想的重要来源。但是为了处理上的方便，论文常常基于不完整、或者与实际市场不一致的假设。简言之，尽信书不如无书。

第二部分从第4章开始，到第17章结束，讨论了寻找Alpha过程中的方方面面，比如如何处理数据、评估Alpha因子，控制偏差等等。第15章和第16章介绍了如何使用机器学习，自动搜索因子。

从18章开始，具体介绍了各种场景下的因子应该设计，比如基本面的、动量因子、日内、事件驱动因子等等，这一部分对拓宽知识面比较有帮助。

这本书谈方法比较多，比较适合入门，有了一个全貌之后，再看Zura Kakushadze的《101 Formulaic Alphas》，它的代码会多一点（伪代码）。看完这两本书，你可能仍然无法下手实作一个因子分析和实现一个策略。如果是这样，你可以来报名我们的《因子分析与机器学习交易策略》课，课程以Notebook呈现，可以边看解说边运行代码。需要的数据也无须另外准备，都在环境中提供了。

此外，我们还有更全面的《量化24课》。

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
