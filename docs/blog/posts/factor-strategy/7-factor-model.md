---
title: 7因子模型，除了规模、市场、动量和价值，还有哪些？
slug: what-is-7-factor-model
date: 2024-03-26
category: strategy
motto: Hope is wishing something would happen. Faith is believing something will happen. Courage is making something happen.
lunar:
lineNumbers: true
img: https://images.jieyu.ai/images/2024/03/duke.jpg
tags: 
    - 因子
---

这篇文章的源起是有读者问，七因子模型除了规模、市场、动量和价值之外，还包括哪几个因子？就这个题目，正好介绍一下Fung & Hsieh的七因子模型。

七因子模型一般是指David Hsieh和William Fung于2004年在一篇题为《Hedge Fund Benchmarks: A Risk Based Approach》中提出的7 factor model。

![L50](https://images.jieyu.ai/images/2024/03/david-hsieh.jpg)
作者David Hsieh 出生于香港，是Duke大学教授，在对冲基金和另类beta上有着深入而广泛的研究。William Fung则是伦敦商学院对冲基金教育研究中心的客座教授。

这篇论文发表以来，共获得了1300多次引用。作者也以此论文获得了由CFA颁发的格雷厄姆和多德杰出贡献奖及费雪.布莱克纪念基金会奖等几个奖励。因此，这篇论文在量化史上还是有一定地位的，值得我们学习。

在[这篇论文](/assets/ebooks/Hedge-Fund-Benchmarks-A-Risk-Based-Approach.pdf)中，7因子模型指的是以下7个：

1. Bond Trend-Following Factor 债券趋势跟随因子
2. Currency Trend-Following Factor 货币趋势跟随因子
3. Commodity Trend-Following Factor 商品趋势跟踪因子
4. Equity Market Factor 股票市场因子
5. The Equity Size Spread Factor 股票规模利差因子
6. The Bond Market Factor 债券市场因子
7. The Bond Size Spread Factor 债券规模利差因子

这几个因子中，股票市场因子、规模利差因子本质上就是市场因子和规模因子。


前三个因子来自Fung和Hsieh另一篇论文：《The Risk in Hedge Fund Strategies: Theory and Evidence from Trend Followers》。
这篇论文发表几年后， Fung和Hsieh又增加了第8个因子，即MSCI新兴市场指数。

这篇论文中还介绍了对冲基金研究中几个常见的偏差（bias），这里也重点介绍下。

!!! tip
    在投资中了解什么是错的、怎么错的，可能比了解什么是对的更重要，毕竟，投资中，只有正确的方法和方法论是持久发作用的，而所谓“正确的结论”，都只是一时一地的产物。

研究对冲基金时，第一个容易出现的偏差是选择偏差。共同基金（即公募基金）需要公开批露他们的投资活动，但对冲基金则不需要。对冲基金的数据一般由数据供应商收集，在这种收集过程中，就可能出现选择偏差，从而使得数据库中的基金样本不是整个基金样本的代表性样本。

第二是幸存者偏差。这是所有基金研究中的一个常见问题。我们在课程中讲过，股票的上市和退市都比较严格，公司即使退市，它的历史数据也能很容易获取到；但已停止运营的基金则会从数据库中剔除掉。这一点除了本文有提到，在其它许多论文中也有提到。


第三个偏差是即时历史偏差(instant history bias)。当基金进入数据库时，它会把过去的业绩历史记录也带入进来，尽管这些业绩记录是在孵化期创建的。并且，如果一支基金在孵化期的业绩不够好，他们也往往会停止运营。显然，这样的业绩记录并不完全真实可靠。

在量化研究中如何避免各种系统偏差是很重要的经验和技巧。这些经验并不来自于学术研究，掌握这些经验需要我们了解数据加工处理的过程 -- 很多人无法直接了解到数据收集到加工的全过程，因此行业交流是十分重要的。

回到正题。读者的提问是，在七因子模型中，除了市场、规模、价值和动量，其它几个因子是什么。这个问题可能来源于国内私募在用的一个8因子模型。

![](https://images.jieyu.ai/images/2024/03/20240326193718.png)


这个模型由清华大学国家金融研究院在2017年3月的一个简报（[中国私募基金8因子模型](/assets/ebooks/中国私募基金风险因子分析.pdf)）中作出批露。它参考了Fung和Hsieh的7因子模型，提出了8个因子，分别是：

1. 股票市场风险因子（MKT）
2. 规模因子（SMB）
3. 价值因子（HML)
4. 动量因子（MOM）
5. 债券因子（BOND10)
6. 信用风险因子（CBMB10)
7. 债券市场综合因子（BOND_RET）
8. 商品市场风险因子

不难看出，这个8因子模型是在经典的FF三因子（规模、市场、价值）基础上，增加了动量因子（Titman和Jegadesh），再结合Fung和Hsieh的七因子中的一些因子构成的。

在这个模型中，股票市场风险因子定义为：

![](https://images.jieyu.ai/images/2024/03/mkt-factor.png)

$RET_HS300_t$为第$t$月的沪深300指数的月收益率， $RF_t$为第$t$月1年期定期存款利率的月利率。这点比较意外，一般来说，国债的风险比存款还要低（大额存款有50万的止付额），但收益要高一些，一般多会使用国债利率作为无风险收益率。


它的规模因子构建方法是，以一年为期进行一次换手。在每年6月底构建一次投资组合，将A股按流通市值将样本股票等分为小盘组和大盘组，再根据T-1期年报中的账面市值比和A股流通市值（ME）计算出账面市值比后，将股票按30%, 40%, 30%的比例划分为成长组、平衡组和价值组。最后，将两种分组方式所得的结果，按笛卡尔积的方式组成为六组，再计算各组的月收益率。

它的价值因子、动量因子构建方法与规模因子类似。

债券因子公式为：

![75%](https://images.jieyu.ai/images/2024/03/bond10.jpg)

信用风险因子为：

![75%](https://images.jieyu.ai/images/2024/03/cbmb10.jpg)

债券市场综合因子公式为：

![75%](https://images.jieyu.ai/images/2024/03/bond_ret.jpg)

数据使用的是中债综合全价指数。文章虽然只有10页的篇幅，但在因子构建方面讲解得比较详细，感兴趣的同学可以找来一读。

题图是杜克大学的地标 - Duke Chapel（杜克教堂）。我曾经开车路过杜克大学，当时心想，哈，这就是杜克大学了，可惜事前没有安排，没能进去参观。

从CAPM、APT以来，各种因子被源源不断地提出，形成了所谓的因子动物园一说。这么多因子，如何进行学习？如何梳理它们的脉络？对初学者而言，可能会一时没有头绪。我们准备了一个系统的量化课程（《量化二十四课》），并且即将开设新的因子分析及机器学习策略课程，欢迎咨询。现在报名《量化二十四课》，还可以免费升级到《因子分析及机器学习策略》课程。

文中提及的两篇论文，可以在[这里](http://www.jieyu.ai/blog/2024/03/26/what-is-7-factor-model/)找到链接下载。
