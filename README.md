---
title: 大富翁量化编程实战课
---


<style>
.module {
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .14), 0 1px 5px 0 rgba(0, 0, 0, .12), 0 3px 1px -2px rgba(0, 0, 0, .2);
  margin: 1em 0;
  border-radius: .3rem;
  overflow: auto;
  background-color: rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: start;
  padding: 0;
}

.module >.left {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 5vw;
    writing-mode: vertical-rl;
}

.module >.right {
    display: flex;
    flex-flow: column;
    justify-content: space-around;
    align-items: center;
    padding: 0 1vw;
    flex: 1;
}

.row {
    display: flex;
    width: 100%;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
}

.row > * {
    flex: 1;
    overflow: hidden;
}

.box {
    box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .14), 0 1px 5px 0 rgba(0, 0, 0, .12), 0 3px 1px -2px rgba(0, 0, 0, .2);
    border-radius: 2px;
    margin: 0.5vw;
    display: flex;
    flex-flow: column;
}

.box > .title {
    font-size: 2vw;
    font-weight: 500;
    padding: 0 1.5vw;
}

.box > .content {
    padding: 1vw 0.2vw;
}

.item {
    border-radius: 3px;
    text-align: center;
    margin: 0.5px;
    padding: 0 0.5vw;
    white-space: nowrap;
}

/* primer */
.primer {
    border: 1px solid rgba(0, 184, 212, .8);
    padding: 0;
}

.module.primer > .left {
    background-color:rgba(0, 184, 212, .8);
}

.primer .box {
    background-color: rgba(0, 184, 212, .1);
    width: 40vw;
    height: 10vw;
}

.primer .title {
    background-color: rgba(0, 184, 212, .2);
}

.primer .item {
    border: 1px solid  rgba(0, 184, 212, .8);
    font-size: 1.2vw;
}

/* course */
.course {
    border: 1px solid rgba(183, 150, 217, .8);
    padding: 0;
}

.module.course > .left {
    background-color: rgba(183, 150, 217, .8);
}

.course .box {
    background-color: rgba(242, 189, 199, .1);
    height: 17vw;
}

.course .title {
    background-color: rgba(183, 150, 217, .2);
}

.course .item {
    border: 1px solid rgba(183, 150, 217, .8);
    font-size: 1.1vw;
}

.course .alpha2 > .item {
    background-color: rgba(183, 150, 217, .2);
}

.course .alpha4 > .item {
    background-color: rgba(183, 150, 217, .4);
}

.course .alpha6 > .item {
    background-color:rgba(183, 150, 217, .6);
}

.course .alpha8 > .item {
    background-color: rgba(183, 150, 217, .8);
}

/* advanced */
.advanced .title {
    background-color: rgba(0, 191, 165, .2);
    font-size: 1.5vw;
}
.advanced {
    border: 1px solid rgba(0, 191, 165, .8);;
    padding: 0;
}

.module.advanced > .left {
    background-color: rgba(0, 191, 165, .8););
}

.advanced .box {
    background-color:rgba(0, 191, 165, .1);
}

.advanced .item {
    border: 1px solid rgba(0, 191, 165, .8);
    font-size: 1.1vw;
}

.advanced .alpha2 > .item {
    background-color: rgba(0, 191, 165, .2);
}


.advanced .alpha4 > .item {
    background-color: rgba(0, 191, 165, .4);
}

.advanced .alpha6 > .item {
    background-color: rgba(0, 191, 165, .6);
}

.advanced .alpha8 > .item {
    background-color: rgba(0, 191, 165, .8);
}

/* watermark */
.wartermark{
    /* transform: rotate(331deg); */
    font-size: 2vw;
    color: rgba(5, 5, 5, 0.1);
    position: absolute;
    padding-left: 40%;
    padding-top: 25.5%;
}
</style>


## 1. 大富翁和大富翁量化课程

大富翁是可以本地部署的开源量化框架，自2019年起开发，2022年底2.0基本完成，功能齐全，能容纳超大规模数据（目前在生产环境已存储超30亿条行情数据）。

大富翁的起名有两重寓意，一是希望这个框架的使用者们，都能实现财富自由。另一方面，大富翁也是一款投资游戏的名字 -- 财富终究只是一场大富翁游戏。在这场游戏中，**努力和才能固然重要，但运气始终是不可或缺的**。

每一个从事金钱游戏的人，最终都将明白，个人在经济周期面前，是多么的渺小。这也正是达利欧在投资上取得了巨大的成功之后，仍要深入历史，探索大周期（见《原则：应对变化中的世界秩序》 - 瑞.达利欧著）的原因。因此，无论我们采用什么样的方法进行投资，都需要顺势而为，不可逆流而上。


## 2. 课程简介

本课程是一门**中高级**课程，它面向打算进入量化交易领域的学生、程序员和正在从事主观交易的机构投资者和个人投资者。

课程涵盖了量化交易的全流程，即如何获取数据，如何考察数据的分布、关联性，因子和模式的发现和提取，如何编写策略、进行回测和评估，最终将策略接入实盘。

学习完成本课程的内容之后，您将会对量化交易有全面和系统的了解，能够独立实施量化策略的开发、调试、回测及实盘交易，并且能评估和改进自己的策略。您将有能力复现论文、经典量化交易策略或者实现策略思想。如果自己已经有了成功的交易经验，则将有如虎添翼之感。

!!! tip
    本课程并非面试指南。完成本课程后，您将有能力在任何一家投资机构开展工作，但要获得这些机构的offer，从我们的跟踪情况来看，您还需要刷一些面试宝典，补充部分数学知识、基础算法题和了解一些 brain teaser的应对技巧。

    相关资料在我们的课程和社群中都有推荐。

本课程讲授的内容，远非量化交易的全部。在学完本课程后，您可沿着我们给出的学习[路线图](#roadmap)继续深造，成为领域专家。

课程媒介为录播视频、Notebook文稿和每周一次答疑辅导。文字稿部分约40万字节。本课程将为学员提供可运行这些Notebook的实验环境，在该实验环境中：

* 192核CPU和256GB内存（学员共享）
* Jupyter Lab策略开发环境
* 超过30亿条分钟级行情数据，并提供盘中实时数据
* 回测服务。您可以立即编写策略并运行回测
* 仿真交易。本环境中可提供仿真交易，供您检验自己的策略

这是一门比较硬核的课程，我们在内容编排上做到了顺序讲述、层层递进、前后照应、取舍得当。在内容上，还有许多其它地方难得一见的知识点，我们列举一二：

!!! question
    1. A股报价的最小单位是分。很多情况下，我们需要将小数四舍五入到百分位。2元以下的个股出现舍入误差时，我们将承受0.5%的损失。如果每天进行一次这样的交易，年化损失会达到惊人的247%！可是，您使用的四舍五入方法，它是正确的吗？
    2. 有人说回测中要使用后复权，这个结论是正确的吗？你将如何证明？
    3. 除了min, max, 还有哪些函数可能是未来函数，您能给出一个清单吗？
    4. 如果您的策略在回测中得到夏普是2，一般而言，这是个不错的策略。但在实盘中，它开始回撤了，夏普也在变差。当回撤达到多少时，可以断定，策略的运行环境已不存在，必须中止实盘（其它人可能告诉您，量化程序一旦运行，就必须扛过去）？


在难度取舍上，有一些课程实现了从小学生到研究生阶段的难度覆盖，比如从Python的基础语法开始，讲到Python高性能编程，或者需要高深数学技巧（比如BS公式，伊滕引理或者维纳过程等）的衍生品策略。这是不恰当的。这门课以A股为实践材料，因此几乎所有人都具有一定的领域知识，并且不需要过于高深的数学知识（衍生品对数学要求高一些）。


## 3. 课程大纲及编排说明

<div class="admon_green" title="导论">
💡 课时安排：1课时

💡 介绍什么是量化交易，量化金融的知识体系，本课程的目标和定位，如何学习本课程（环境、参考书和辅导）

</div>

<div class="admon_blue" title="Module 1. 获取数据">

💡 课时安排：5课时

💡 课程目录

* 第1课 证券基础知识与Akshare
* 第2课 Tushare
* 第3课 Jqdatasdk
* 第4课 Zillionare
* 第5课 习题

💡 介绍如何稳定和高性价比地获取证券数据及本地化存储的问题。我们将主要介绍akshare, tushare, Jqdatasdk和Zillionare，顺带涉及Baostock和YFinance。

这一模块中，我们将介绍证券和交易所编码方案，除权和复权的概念，几种复权方式的推导关系。您将在后面的课程中（回测和实盘）了解到，复权会是量化交易中根本性的问题之一。

我们还将通过两个示例，来揭示数据的力量。其中之一是市盈率与大盘择时的关系，另一个则是投资者人数与市场走势的关系。

</div>

<div class="admon_purple" title="Module 2. 初识策略">

💡 课时安排：3课时

💡 课程目录

* 第6课 小市值策略
* 第7课 布林带策略
* 第8课 网格交易法

💡 小市值策略是著名的Famma三因子之一，在全球各个市场，多年来一直有较好的表现。尽管短期内它可能面临周期性失效，但小市值公司优异的成长性是它的逻辑支撑，因此无论何时，它都是量化兵器库中的必备策略。在2023年7月华泰金工发布的因子评测中，小市值因子表现排名第三。

布林带策略有坚实的统计学理论支撑，是80年代最有效的技术指标类策略。在本课程中，我们指出了布林带策略的优化改进方向，而实现这些改进所需要的技术，我们将在第13课介绍。

网格交易法由信息论大师香农提出。它以其简洁易懂，不判断趋势的特点深受大家喜爱，成为各券商向客户提供的必备交易工具之一。我们在这一节课中，先是实现了一个朴素的算法，只获得0.71%的年化回报，然后一步步将其优化到接近30%的年化回报。

在本模块中，我们从基本面、技术面和交易维度带大家认识策略编写的一般流程，并且从零开手，逐步抽象出来自己的策略编写框架。在掌握策略编写的原理之后，后面学习和理解庞大精深的回测框架就易如反掌。这里我们将接触到OOP编程概念，最终将实现一个抽象的策略基类，从而简化每一次具体的策略子类的编写。
</div>

<div class="admon_green" title="Module 3. 量化分析方法和技术">

💡 课时安排：7课时

💡 课程目录

* 第9课 Numpy和Pandas
* 第10课 经典技术指标库 Ta-lib
* 第11课 数据分析与Python实现（1）
* 第12课 数据分析与Python实现（2）
* 第13课 技术分析实战
* 第14课 因子分析
* 第15课 Alphalens及其它
  
💡 这个模块中，我们首先介绍了Numpy和Pandas。它们在证券分析领域，既作为基础数据结构使用，也提供了常用算法比如移动均值等。这一节课展示了大量金融领域里使用numpy函数的例子，比如计算最大回撤 (max drawdown)等等。

ta-lib是经典的技术指标库，也是我们提取时序因子的重要来源。

在第11、12课，我们主要介绍基础的概率与统计原理及应用：一阶矩到四阶矩， PDF/CDF， 统计推断方法，残差，相关性，相似性和距离，归一化等。如果不从事金融衍生品交易，这里学习的数学知识将能覆盖大部分量化策略研究领域。

动量、趋势跟踪、反转策略是一直市场上最有效的策略。经典的Alpha 101因子中，主要是以收益因子为基础来构建更复杂的动量、趋势和反转因子。我们将在第13课，以我们已经掌握的概率和统计知识为基础，通过复杂的技术形态分析，实现构建前述因子和策略的基本组件。我们相信，通过这些技术以及技术的组合，将会更好地发现趋势和反转。

第14、15课我们将介绍因子分析流程，我们将学习到异常值、缺失值处理、分布调整、标准化(zscore)、中性化处理，以及如何通过IC法、回归法和分层法实现单因子的评测。

这一模块中我们将学习到Python量化生态中最重要的那些库，比如 **Numpy**, Pandas, **ta-lib**, **Scipy**, **Sklearn**, Statistics, **Statmodels**, **Alphalens**, **Sympy**, **Ckwraps**, **Zigzag**, jqfactor等（黑体字部分是重点讲述）。

</div>

<div class="admon_blue" title="Module 4. 高级数据可视化">

💡 课时安排：3课时
💡 课程目录

* 第16课 Matplotlib与图的构成原理
* 第17课 交互式绘图Plotly及Plotly Dash
* 第18课 语义关系图Seaborn及PyEcharts
  
💡 量化交易一般不需要人工干预，但我们在策略研究中，特别是在早期的策略探索阶段，往往需要借助绘图来揭示数据之间的关系，或者它们内在的分布特性。或者，我们需要就策略的各项评估指标，生成图文并茂，清晰易懂的报告，向客户传达策略的价值。在每一次回测运行结束之后，我们还很可能需要借助叠加了交易详情的k线图来进行调优。因此，我们必须熟练掌握数据可视化技巧，这就是Module 4的主要内容。

我们在第16课，我们以matplotlib为例，介绍了一张图是由哪些元素顶底向上构成的，这包括标注、标记、图例、轴、子图、图，以及色彩和主题。掌握了绘图的领域知识，再来学习框架，就会豁然开朗。

第17课，我们介绍了Plotly，用来在notebook或者网页上绘制交互式图。我们还介绍了如何绘制复杂的K线图，包括如何处理日期之间的gap，拖动式数据加载，如何绘制十字光标等。这节课我们还介绍了Plotly Dash，通过它我们可以仅凭Python就完成简单的交互式网页应用，从而可以制作一个售卖我们策略的网站。

第18课，seaborn为我们带来了基于语义的图形绘制，提供了快速探索数据内在的关系和分布的可能。我们还介绍了PyEcharts，这是国内团队常用的绘图框架，它还提供了一些更高级的绘图结构。

</div>

<div class="admon_purple" title="Module 5. 回测和回测框架">

💡 课时安排：4课时
💡 课程目录

* 第19课 Backtrader (一)
* 第20课 Backtrader (二)
* 第21课 策略评估与可视化
* 第22课 回测陷阱与大富翁回测框架的答案

💡 回测是检验量化策略最重要的方式，Backtrader则是当下最流行的本地化回测框架之一。我们从Backtrader最基础的时间线概念及语法糖讲起，逐步介绍DataFeeds, 多周期数据，指标，编写策略及评估，并在第20课以讲解驱动引擎、订单、交易代理、可视化和优化作为结束。

在评估策略这节课，我们介绍了回报率5大指标，风险调整收益类6大指标，基准对照类两大指标及各指标应用场景、关联度。这节课我们还将介绍一个制作策略回测报告的工具 -- quantstats库。

即使是有了一定工作经验的人，也很容易编写出来一个跑分很高的策略，却对已经深陷的危险茫然不知。这里有数据的问题、有框架的问题、也有编码熟练度的问题。您可能对未来数据、前视偏差这些概念烂熟于心，但只有有着丰富实战经验的人，才知道什么情况下，我们已浑然不觉地引入了这些偏差。学完这一课，相信会省掉您无数个焦灼的夜晚。这一课介绍的回测陷阱范围非常之广，包括了函数库的、数据编制发布时机引起的、复权引起的、模拟撮合机制引起的、实盘差异等。

最后，我们还介绍了大富翁回测框架是如何解决这些问题的。

在这一部分，我们将学习到这些重要的库： **backtrader**, **empyrical**,**quantstats**等，以及大富翁开源框架中的zillionare-backtesting, zillionare-trader-client.

</div>

<div class="admon_green" title="Module 6. 实盘接口">

💡 课时安排：2课时
💡 课程目录

* 第23课 EasyTrader、东财EMC和Trader-gm-adaptor
* 第24课 Ptrade和QMT
  
💡 策略最终都要接入实盘。我们首先介绍了基于键鼠模拟的交易接口。我们可以通过它来运行模拟盘，对我们的策略进行实盘前的最后测试。我们介绍了如何通过easytrader来进行雪球组合的模拟交易，以及如何跟踪网络上其它高手的交易。

掘金量化开发的量化终端包含了交易接口，被许多券商采购，比如东方财富采购后，最终提供给用户的产品称为东财EMC。它使用文件扫单的方式监视用户策略的输出。在这一课，我们介绍了如何将文件扫单接口封装成网络服务，从而更容易为量化策略使用。

第24课介绍另外两个流派的实盘接口，即PTrade和QMT。前者是券商机房托管方式，后者则可以在本地运行，并且提供了方便的API接口。

这一部分介绍的重要库（软件）有**Easy-Trader**, **Zillionare-Trader-gm-Adaptor**, **PTrade**, **qmt**,和**xtquant**。

</div>

!!! tip
    更详细的课程大纲（具体到三级标题），可联系助教索取。
## 4. 量化知识体系与本课程定位

量化交易不仅在国内是新生事物，就连直到在华尔街点据主流地位，也不过20多年历史。因此，关于量化交易，很少看到体系化的知识结构梳理。

我们根据自己的经验，结合国内外同类课程、同行交流的结果，通过对主流量化框架、量化常用库的梳理和对重要论文的阅读梳理，总结出如下学习<span id="roadmap">路线图</span>：

<div>
<div class="wartermark">大富翁量化编程</div>
<div class="module advanced">
    <div class="left">
    <div>进阶研究方向</div>
    </div>
    <div class="right">
        <div class="row">
            <div>
            <div class="box" style="height: 12vw">
                <div class="title">策略探索方法论</div>
                <div class="content">
                    <div class="item">证券市场与交易规则</div>
                    <div class="item">研报论文复现</div>
                    <div class="item">另类数据/因子挖掘</div>
                    <div class="item">情报学与社会工程</div>
                </div>
            </div>
            <div class="box" style="height: 12vw">
                <div class="title">拓展品种</div>
                <div class="content">
                    <div class="item">商品期货</div>
                    <div class="item">股指期货</div>
                    <div class="item">期权</div>
                    <div class="row">
                    <div class="item">可转债</div>
                    <div class="item">ETF</div>
                    <div class="item">数字货币</div>
                    <div class="item">外汇</div>
                    </div>
                </div>
            </div>
            </div>
            <div>
            <div class="box" style="height: 10vw">
                <div class="title">现代金融理论</div>
                <div class="content">
                    <div class="row">
                        <div class="item">EMH</div>
                        <div class="item">APT</div>
                        <div class="item">PT</div>
                        <div class="item">伊藤引理</div>
                    </div>
                    <div class="row">
                        <div class="item">CAPM</div>
                        <div class="item">BS公式</div>
                        <div class="item">MM定理</div>
                    </div>
                    <div class="row">
                        <div class="item">行为金融学</div>
                        <div class="item">财务报表</div>
                    </div>
                </div>
            </div>
            <div class="box" style="height: 14.2vw">
                <div class="title">数学与算法</div>
                <div class="content">
                    <div class="row">
                        <div class="item">贝叶斯</div>
                        <div class="item">马尔可夫</div>
                        <div class="item">蒙特卡洛</div>
                        <div class="item">凸优化</div>
                        <div class="item">PCA</div>
                    </div>
                    <div class="row alpha1">
                        <div class="item">人工智能</div>
                        <div class="item">增强学习</div>
                        <div class="item">NLP</div>
                        <div class="item">RNN</div>
                    </div>
                    <div class="row alpha2">
                        <div class="item">机器学习</div>
                        <div class="item">knn</div>
                        <div class="item">svm</div>
                        <div class="item">xgboost</div>
                    </div>
                    <div class="row alpha4">
                        <div class="item">时间序列</div>
                        <div class="item">ARIMA</div>
                        <div class="item">ARCH</div>
                        <div class="item">Kalman</div>
                    </div>
                    <div class="row alpha6">
                        <div class="item">时频变换</div>
                        <div class="item">FFT</div>
                        <div class="item">wavelet</div>
                    </div>
                </div>
            </div>
            </div>
            <div class="box" style="height:24.5vw">
                <div class="title">策略和模型</div>
                <div class="content">
                    <div class="row">
                        <div class="item">微观结构 & HFT</div>
                        <div class="item">order flow trading</div>
                    </div>
                    <div class="row">
                        <div class="item">Guerilla Algorithm</div>
                        <div class="item">PTP/FIFO</div>
                    </div>
                    <div class="row">
                        <div class="item">Scalping</div>
                        <div class="item">VWAP</div>
                    </div>
                    <div class="row alpha2">
                        <div class="item">动量策略</div>
                        <div class="item">时序动量</div>
                        <div class="item">行业动量</div>
                    </div>
                    <div class="row alpha2">
                        <div class="item">趋势跟踪</div>
                        <div class="item">Dual Thrust</div>
                        <div class="item">海龟交易法</div>
                    </div>
                    <div class="row alpha4">
                        <div class="item">主力模式识别</div>
                        <div class="item">情绪分析</div>
                    </div>
                    <div class="row alpha4">
                        <div class="item">统计套利</div>
                        <div class="item">ETF套利</div>
                        <div class="item">指数增强</div>
                        <div class="item">跨品种套利</div>
                    </div>
                    <div class="row alpha6">
                        <div class="item">均值回归</div>
                        <div class="item">跨期套利</div>
                        <div class="item">alpha套利</div>
                    </div>
                    <div class="row alpha8">
                        <div class="item">基本面</div>
                        <div class="item">行业轮动</div>
                        <div class="item">Alpha对冲</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="module course">
    <div class="left">
    <div>本课程</div>
    </div>
    <div class="right">
        <div class="row">
        <div class="box" style="height:18vw">
            <div class="title">
            高级数据可视化
            </div>
            <div class="content">
                <div class="row">
                <div class="item">图的构成</div>
                <div class="item">坐标轴</div>
                <div class="item">Axes/Fig</div>
                <div class="item">双轴</div>
                </div>
                <div class="row alpha2">
                <div class="item">Bar</div>
                <div class="item">Line</div>
                <div class="item">Scatter</div>
                <div class="item">Hist</div>
                <div class="item">积分图</div>
                </div>
                <div class="row alpha2">
                <div class="item">分面图</div>
                <div class="item">热力图</div>
                <div class="item">Image</div>
                <div class="item">联合分布图</div>
                </div>
                <div class="row alpha4">
                <div class="item">样式和主题</div>
                <div class="item">调色板</div>
                <div class="item">语义化</div>
                <div class="item">交互式K线</div>
                </div>
                <div class="row alpha6">
                <div class="item">matplotlib</div>
                <div class="item">plotly</div>
                <div class="item">Plotly Dash</div>
                </div>
                <div class="row alpha6">
                <div class="item">seaborn</div>
                <div class="item">PyEcharts</div>
                </div>
            </div>
        </div>
        <div class="box" style="height:18vw">
            <div class="title">
            回测和回测框架
            </div>
            <div class="content">
                <div class="row">
                <div class="item">backtrader</div>
                <div class="item">语法糖</div>
                <div class="item">时间线</div>
                <div class="item">指标</div>
                </div>
                <div class="row">
                <div class="item">DataFeeds</div>
                <div class="item">多周期</div>
                <div class="item">驱动引擎</div>
                <div class="item">订单</div>
                </div>
                <div class="row">
                <div class="item">交易代理</div>
                <div class="item">可视化</div>
                <div class="item">优化</div>
                </div>
                <div class="row alpha2">
                <div class="item">Metric</div>
                <div class="item">收益率</div>
                <div class="item">夏普</div>
                <div class="item">Sortino</div>
                <div class="item">𝛼 𝛽</div>
                <div class="item">Omega</div>
                </div>
                <div class="row alpha4">
                <div class="item">可视化</div>
                <div class="item">Quant Stats</div>
                </div>
                <div class="row alpha4">
                <div class="item">回测陷阱</div>
                <div class="item">大富翁回测框架</div>
                </div>
            </div>
        </div>
        <div class="box" style="height:18vw">
            <div class="title">
            实盘接口
            </div>
            <div class="content">
                <div class="row">
                <div class="item">键鼠模拟</div>
                <div class="item">EasyTrader</div>
                <div class="item">策略跟踪</div>
                </div>
                <div class="row">
                <div class="item">东财EMC</div>
                <div class="item">文件单</div>
                <div class="item">网络封装</div>
                </div>
                <div class="row">
                <div class="item">Ptrade</div>
                </div>
                <div class="row">
                <div class="item">QMT</div>
                </div>
                <div class="row">
                <div class="item">Mini-QMT</div>
                <div class="item">XtData</div>
                <div class="item">XtTrade</div>
                </div>
            </div>
        </div>
        </div>
        <div class="row">
        <div class="box"  style="height:18vw">
            <div class="title">
            获取数据
            </div>
            <div class="content">
                <div class="row">
                <div class="item">证券常识</div>
                <div class="item">证券列表</div>
                </div>
                <div class="row">
                <div class="item">交易日历</div>
                <div class="item">行情数据</div>
                </div>
                <div class="row">
                <div class="item">财务数据</div>
                <div class="item">ST 停牌 涨跌停价</div>
                </div>
                <div class="row">
                <div class="item">其它</div>
                <div class="item">ETF</div>
                <div class="item">债券</div>
                <div class="item">新闻</div>
                <div class="item">空单</div>
                <div class="item">北向</div>
                </div>
            </div>
        </div>
        <div class="box"  style="height:18vw">
            <div class="title">
            初识策略
            </div>
            <div class="content">
                <div class="row">
                <div class="item">基本面策略.规模因子</div>
                </div>
                <div class="row">
                <div class="item">基本面策略.规模因子</div>
                </div>
                <div class="row">
                <div class="item">技术面策略.布林带</div>
                </div>
                <div class="row">
                <div class="item">手写策略框架</div>
                <div class="item">OOP与封装</div>
                <div class="item">抽象类</div>
                </div>
            </div>
        </div>
        <div class="box" style="height:18vw">
            <div class="title">
            量化分析技术
            </div>
            <div class="content">
                <div class="row">
                <div class="item">概率统计</div>
                <div class="item">矩</div>
                <div class="item">分布</div>
                <div class="item">PDF/CDF</div>
                <div class="item">假设检验</div>
                </div>
                <div class="row alpha2">
                <div class="item">因子分析</div>
                <div class="item">预处理</div>
                <div class="item">IC</div>
                <div class="item">分层</div>
                <div class="item">评测框架</div>
                </div>
                <div class="row alpha4">
                <div class="item">形态检测</div>
                <div class="item">顶底检测</div>
                <div class="item">平台整理</div>
                <div class="item">模式识别</div>
                </div>
                <div class="row alpha8">
                <div class="item">scipy</div>
                <div class="item">statmodels</div>
                <div class="item">ckwraps</div>
                <div class="item">zigzag</div>
                </div>
                <div class="row alpha6">
                <div class="item">sympy</div>
                <div class="item">alphalens</div>
                <div class="item">sklearn</div>
                <div class="item">statistics</div>
                </div>
                <div class="row alpha6">
                <div class="item">Numpy</div>
                <div class="item">Pandas</div>
                <div class="item">Ta-Lib</div>
                </div>
            </div>
        </div>
        </div> <!--row-->
    </div>
</div>
<div class="module primer">
    <div class="left">
    <div>Primer</div>
    </div>
    <div class="right">
        <div class="row">
            <div class="box">
                <div class="title">
                Python 基础
                </div>
                <div class="content">
                    <div class="row">
                    <div class="item">基本语法</div>
                    <div class="item">Pip</div>
                    <div class="item">Conda</div>
                    </div>
                    <div class="row">
                    <div class="item">Testing</div>
                    <div class="item">Debug</div>
                    </div>
                </div>
            </div>
            <div class="box">
                <div class="title">
                数学基础（大学水平）
                </div>
                <div class="content">
                    <div class="row">
                    <div class="item">高等数学</div>
                    <div class="item">概率与统计</div>
                    <div class="item">线性代数</div>
                    </div>
                </div>
            </div>
            <div class="box">
                <div class="title">
                编程工具
                </div>
                <div class="content">
                    <div class="row">
                    <div class="item">Git</div>
                    <div class="item">VsCode</div>
                    </div>
                    <div class="row">
                    <div class="item">PyCharm</div>
                    <div class="item">Jupyter Notebook</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div style="color: gray;font-size:x-small;font-style:italic;text-align:center">The Pilgram's Progress to Zillionare</div>
</div>
<br>
在这个路线图中，最下面一层可以看作是学习量化的前置条件。如果您还不具备其中某些知识，也不必过份担心，经过一小段时间认真地自学，就应该能达到入门标准。在交易中，最重要的并不是数学或者什么别的技能，而是我们对规律的发现和洞察能力：
<br>
<br>

<div style="font-style:italic;color:grey;text-align:right">Algebra is like sheet music. The important thing is not can you read it, it's can you hear it.<br>-- Movie 'Oppenheimer'</div>

<br>

关于量化交易所需要的Python基础，我们有较好的英文教材可以提供。该教材比较简练，不需要花很多时间就能学完，并且与我们的课程能很好衔接。

## 5. 讲师和助教

<div class="admon_blue" title="👨🏻 Aaron">

985名校计算机专业硕士，曾任职于 IBM/Oracle等多家知名外企，后创业与人合伙，成立公司专注量化投资。5年量化开发经验，10年以上A股操作经验。

开源量化框架Zillionare、Python工程模板Python Project Wizard及多个开源软件开发者。

Python布道者，著有《Python能做大项目》，宣传Python开发最佳工程和质量管理实践。

爱好围棋而不精，初段水平。
</div>

<div class="admon_purple" title="👩🏻 Belva">

海外名校硕士，人工智能专业。协助完成了课程设计及部分示例代码。
</div>

<div class="admon_purple" title="👩🏻‍💼 Cindy">

海外名校硕士，金融专业，曾在头部券商实习及银行投行部门任职。协助完成了部分视频剪辑。
</div>

<div class="admon_purple" title="👩🏻‍🎓 Stacey">

某211硕士，金融专业在读，协助完成部分教辅工作。
</div>

### 5.1. 鸣谢
<div class="admon_blue" title="👨🏻‍💻 Babt">

985名校计算机专业硕士，现任某头部券商量化开发部门。协助完成了部分课程设计和视频剪辑。
</div>

## 6. 课程注册流程

每月一日开启新一期学习营。第一周到第三周都将获得早鸟价折扣。

* 联系 quantfans_99 (宽粉) 确定优惠价格，获取购买链接和用户协议
* 通过平台购买课程
* 购买完成当日，助教开通实验账号，将课程登录网址、账号密码发送给学员
* 助教将学员加入当期学员微信群，以便接受会议通知
* 学员开始学习，并在开营后的每周日晚，参加课程答疑
* 4个月后，学员结束课程学习。此时可根据我们提示的路线图，进一步深造

课程实验环境如下：

 ![75%](https://images.jieyu.ai/images/2023/10/welcome-to-zillionare-course.png) 
 ![50%](https://images.jieyu.ai/images/2023/10/cheese-course-lab.png)

近期参考优惠价：

<div class="hat" title="Batch 04, Start Date: 1th Nov, 2023">

| Tier       | Applicable till | Fee(￥) |
| ---------- | --------------- | ------ |
| 超级早鸟价 | 2023年10月9日   | 4500   |
| 早鸟价     | 2023年10月16日  | 4550   |
| 标准价     | 2023年10月31日  | 4600   |

</div>

<div class="hat" title="Batch 05, Start Date: 1th Dec, 2023">

| Tier       | Applicable till | Fee(￥) |
| ---------- | --------------- | ------ |
| 超级早鸟价 | 2023年11月6日   | 4600   |
| 早鸟价     | 2023年11月13日  | 4650   |
| 标准价     | 2023年11月30日  | 4700   |

</div>

<div class="hat" title="Batch 06, Start Date: 1th Jan, 2024">

| Tier       | Applicable till | Fee(￥) |
| ---------- | --------------- | ------ |
| 超级早鸟价 | 2023年12月4日   | 4700   |
| 早鸟价     | 2023年12月11日  | 4750   |
| 标准价     | 2023年12月30日  | 4800   |

</div>


<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

<div class="admon_purple" title="👩🏻 联系我们" style="overflow:hidden">
<div style="display:flex;justify-content:space-evenly;align-items:center;height:150px;">
<div>
    <img src="https://images.jieyu.ai/images/hot/quantfans.png" width="150px">
    <div style="position:absolute;top:170px;left:28%">宽粉</div>
</div>
<div style="margin-top:-20px">
    <img src="https://images.jieyu.ai/images/hot/gzh_258.jpg" width="125px">
    <div style="position:absolute;top:170px;left:68%">公众号</div>
</div>
</div>
</div>
