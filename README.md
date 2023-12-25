大富翁 (Zillionare)是开源量化框架，提供数据本地化、回测、交易接入和量化分析底层库支持等一站式服务。<br><br>大富翁的起名有两重寓意，一是希望她的使用者们都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏，以示提醒大家，不要忽视运气的因素。<br><br>在投资中的运气，其实就是周期。千万不要做逆周期的投资。<br><br>Zillionare 最新版本是2.0，提供了海量数据存储（在我们的生产环境下，存储超过30亿条记录）和高性能访问能力。Zillionare是开源框架，您可以自行研究、拓展该框架。我们也提供付费服务。比如，2.0的Docker-compse 安装版本我们目前只对学员提供。<br><br>关于Zillionare的更多细节请访问[链接](articles/products/)

---

## 近期文章

!!! info "Sharpe 5.5!遗憾规避因子"
    如果在你买入之后，股价下跌，你会在第二天急着抛吗？反之，如果在你卖出之后，股价上涨，你会反手追入吗？先别急着回答，我们来看看科学研究的结论是怎样的。关于这类问题，都是行为金融学研究的范畴。具体到这个场景，我们可以运用遗憾理论来解释。遗憾理论，又称遗憾规避理论（ Fear of Regret Theory），是行为金融学的重要理论之一，该理论认为，非理性的投资者在做决策时，会倾向于避免产生后悔情绪并追求自豪感，避免承认之前的决策失误。<br><text-right>发表于 2023-12-26 [阅读](./docs/blog/posts/regret.md)</text-right>

!!! info "Santa Claus Rally"
    Santa Claus Rally 是指 12 月 25 日圣诞节前后股市的持续上涨这样一个现象。《股票交易员年鉴》的创始人 Yale Hirsch 于 1972 年创造了这个定义，他将当年最后五个交易日和次年前两个交易日的时间范围定义为反弹日期。<br><text-right>发表于 2023-12-25 [阅读](./docs/blog/posts/santa-clause.md)</text-right>

!!! info "净新高占比因子"
    个股的顶底强弱比较难以把握，它们的偶然性太强。董事长有可能跑路，个股也可能遇到突发利好（比如竞争对手仓库失火）。在个股的顶底处，**情绪占据主导地位，理性退避次席，技术指标出现钝化**，进入<red>现状不可描述，一切皆有可能</red>的状态。但是，行业指数作为多个随机变量的叠加，就会出现一定的规律性（受A4系统性影响的偶然性我们先排除在外，毕竟也不是天天有A4）。这是因子分析和技术分析可以一展身手的地方。<br><text-right>发表于 2023-12-24 [阅读](./docs/blog/posts/nh-nl.md)</text-right>

!!! info "球队和硬币因子"
    <br><br>球队和硬币因子最初来自于耶鲁大学 Tobias Moskowitz 的发表于 2021 年 9 月的一篇论文，发布以来，得到了超过 14 次以...<br><text-right>发表于 2023-12-23 [阅读](./docs/blog/posts/hockey-and-coin.md)</text-right>

!!! info "Connor's RSI 我愿称之为年度最强指标"
    人们发明了各种技术指标。这些技术指标中，以价格因子居多，比如均线、ATR、MACD， RSI, JDK等。由于拥挤效应的存在，多数因子的有效性也越来越弱，或者说，它们的使用范围也越来越局限。但有一个因子，是基于著名的RSI的改进版。如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，它是不二之选。<br><text-right>发表于 2023-12-22 [阅读](./docs/blog/posts/connors-rsi.md)</text-right>

!!! info "QMT/XtQuant 之开发环境篇"
    !!! tip 笔记要点<br>    1. XtQuant 获取及安装<br>    2. XtQuant 工作原理 （图2）<br>    3. 版本和文档一致性问题 （图3）<br>    4. 使用 VsCode 远程开发<br><text-right>发表于 2023-12-22 [阅读](./docs/blog/posts/work-with-xtquant.md)</text-right>

!!! info "量化数据免费方案之 QMT"
    !!! tip "学习要点"<br>    - xtquant 提供了数据和交易接口<br>    - xtquant 可以独立于 QMT 之外运行<br>    - download_history_data<br>    - download_history_data2<br>    - get_market_data<br><text-right>发表于 2023-12-21 [阅读](./docs/blog/posts/qmt-get-stock-price.md)</text-right>

!!! info "量化交易中的遗传算法"
     什么是遗传算法？- 遗传算法利用自然选择的概念来确定问题的最佳解决方案。<br>- 遗传算法通常用作优化器，调整参数使得目标最优<br>- 遗传算法可以独立 | 在人工神经网络的构建中使用。<br><text-right>发表于 2023-12-20 [阅读](./docs/blog/posts/genetic-algorithms.md)</text-right>

!!! info "只廖廖数行，但很惊艳的代码"
    既然c/java/python等语言的索引都从零开始，因此我们的盘点也从一行代码也没有的项目开始 0行: No Code这个项目只有零行代码，具有轻量级、跨平台、全自动不可描述之美，一举斩获github 50k :star:<br><text-right>发表于 2023-12-19 [阅读](./docs/blog/posts/awesome-code.md)</text-right>

!!! info "基于深度学习的量化策略如何实现归一化？"
    基于深度学习的量化策略如何实现归一化？本文首先辨析了归一化、标准化与正则化三个术语，然后分析了min-max, sin, sigmoid等归一化函数在量化中使用时常犯的错误，讲解了如何制作一个好的归一化函数。最后，以一些量化因子归一化示例作为结束。<br><br><text-right>发表于 2023-12-16 [阅读](./docs/blog/posts/normalization.md)</text-right>