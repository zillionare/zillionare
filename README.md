
<div class="as-grid m-t-md">
<div class="card-columns">
    
<div class="card">
    <a href="blog/2024/01/12/low-turnover-factor-3">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?girls"/>
    <div class="card-body">
        <h4 class="card-title">Alphalens因子分析(4) - Information Coefficient方法</h4>
        <p class="card-text">在前面的笔记中，无论是回报分析，还是因子Alpha，它们都受到交易成本的影响。信息分析 (Information Analysis)则是一种不受这种影响的评估方法，主要研究方法就是信息系数(Information Coefficient)。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-12</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/11/low-turnover-factor-3">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cats"/>
    <div class="card-body">
        <h4 class="card-title">因子分析（3）- 都是坑！这么简单的Alpha计算，竟然错了？！</h4>
        <p class="card-text">我们继续 Alphalens 因子分析报告的解读。在过去的两篇笔记中，我们都提到，运用 Alphalens 进行因子分析步骤很简单，但是如果不了解它背后的机制与逻辑，很容易得到似是而非的结论。<!--数据精度问题： akshare 是爬虫机制。它的数据来自于财经网站的网页。这些网页是供人阅读用的。因此，它在一些数据显示上，都要进行人性化处理。比如，对换手率，它只保留两位百分数点。对于大市值的沪深 300 而言，它们的换手率平常本来也就在 1%~5%之间波动，这样就引起了数据碰撞 (clash)。它对因子分析究竟有多大的影响不得而知。但是，可以肯定的是，当我们用不同的数据源来进行研究时，得到的结果会有不同。 --><br></p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-11</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/10/alphalens-and-low-turnover-factor-2">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/kaiyun.jpg"/>
    <div class="card-body">
        <h4 class="card-title">Alphalens因子分析(2) - low turnover秒杀98%的基金经理!</h4>
        <p class="card-text"><br>上一篇笔记，我们已经为因子分析准备好了数据。这一篇笔记，我们就进行因子分析。分析过程在 Alphalens 中非常简单，核心是读懂它的报告。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-10</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/09/alphalens-and-low-turnover-factor-1">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/alphalens.jpg?2"/>
    <div class="card-body">
        <h4 class="card-title">Alphalens 因子分析 - 以低换手率因子为例(1)</h4>
        <p class="card-text"><br>因子分析是量化研究的基本技能之一。通过因子分析，找出有效的因子，通过相关性去重后，就可以通过机器学习、线性回归等方法把因子组合起来，构成交易策略。这一篇笔记我们就介绍如何使用 Alphalens 来进行单因子分析。我们使用的因子是低换手率因子。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-09</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/04/z-score-as-a-factor">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/normal-dist.jpg"/>
    <div class="card-body">
        <h4 class="card-title">Z-score 因子的深入思考</h4>
        <p class="card-text">最新（2024 年 1 月）出版的 SC 技术分析（Techical Analysis of Stock & Commodities）的第 4 条文章给到了 Z-score，原文标题为《Z-score: How to use it in Trading》。今天的笔记，就借此机会，同步推出我们对通过Z-score来构建量化因子的一些观点。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-04</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/03/pyarrow-plus-parquet">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/apache-arrow.jpg"/>
    <div class="card-body">
        <h4 class="card-title">存了50TB！pyarrow + parquet</h4>
        <p class="card-text"><br>在上一篇笔记中，我们指出，如果我们只在日线级别上存储行情数据和因子，HDF5 无论如何都是够用了。即使是在存储了 40 年分钟线的单个股数据集上，查询时间也只花了 0.2 秒 -- 这个速度已经足够快了，如果我们不需要在分钟级别上进行横截面数据查询的话。<br></p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-03</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/02/save-quote-data-with-hdf5">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2023/12/hdf5-book.jpg"/>
    <div class="card-body">
        <h4 class="card-title">200倍速！基于 HDF5 的证券数据存储</h4>
        <p class="card-text">去年 15 日的笔记挖了个坑，给出了量化数据和因子的存储方案技术导图。这一篇笔记就开始填坑。即使我们购买了在线数据服务，比如 tushare, 聚宽的账号，我们仍然要构建自己的本地存储，为什么？</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-02</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2023/12/29/connor-rsi-the-best">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?room"/>
    <div class="card-body">
        <h4 class="card-title">年终特稿：这个指标我愿称之为年度最强发现</h4>
        <p class="card-text">如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，这个因子就是不二之选。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2023-12-29</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2023/12/27/qmt-set-sector">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2023/12/sector-cloud.jpg?4"/>
    <div class="card-body">
        <h4 class="card-title">xtquant 中的板块数据</h4>
        <p class="card-text">!!! tip 笔记要点1. xtquant 中有哪些板块和板块分类？<br>    1. 如何获取板块的成份股？<br>    2. 如何获取指数的行情数据？</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2023-12-27</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2023/12/26/how-regret-factor-get-5.5-sharpe-ratio">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?room"/>
    <div class="card-body">
        <h4 class="card-title">Sharpe 5.5!遗憾规避因子</h4>
        <p class="card-text">如果在你买入之后，股价下跌，你会在第二天急着抛吗？反之，如果在你卖出之后，股价上涨，你会反手追入吗？先别急着回答，我们来看看科学研究的结论是怎样的。关于这类问题，都是行为金融学研究的范畴。具体到这个场景，我们可以运用遗憾理论来解释。遗憾理论，又称遗憾规避理论（ Fear of Regret Theory），是行为金融学的重要理论之一，该理论认为，非理性的投资者在做决策时，会倾向于避免产生后悔情绪并追求自豪感，避免承认之前的决策失误。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2023-12-26</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2023/12/25/santa-claus-rally">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2023/12/santa-claus.png"/>
    <div class="card-body">
        <h4 class="card-title">Santa Claus Rally</h4>
        <p class="card-text"><!--  --><br>每天坚持发贴 。千字左右，图文并茂。声明：这一天我们也没有漏发。<br>---Santa Claus Rally 是指 12 月 25 日圣诞节前后股市的持续上涨这样一个现象。《股票交易员年鉴》的创始人 Yale Hirsch 于 1972 年创造了这个定义，他将当年最后五个交易日和次年前两个交易日的时间范围定义为反弹日期。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2023-12-25</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2023/12/24/net-high-net-low-factor">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cloud"/>
    <div class="card-body">
        <h4 class="card-title">净新高占比因子</h4>
        <p class="card-text">个股的顶底强弱比较难以把握，它们的偶然性太强。董事长有可能跑路，个股也可能遇到突发利好（比如竞争对手仓库失火）。在个股的顶底处，**情绪占据主导地位，理性退避次席，技术指标出现钝化**，进入<red>现状不可描述，一切皆有可能</red>的状态。但是，行业指数作为多个随机变量的叠加，就会出现一定的规律性（受A4系统性影响的偶然性我们先排除在外，毕竟也不是天天有A4）。这是因子分析和技术分析可以一展身手的地方。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2023-12-24</small></p>
    </div>
    </a>
</div><!--end-card-->

</div>
</div>


