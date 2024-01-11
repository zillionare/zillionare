
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.4.0/animate.min.css">
<style>
.md-sidebar--primary {
    width: 0%;
}
</style>

<div class="container m-t-md">
    
<div class="row">

<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInLeft">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cloud"/>
    <div class="card-block">
        <h4 class="card-title">因子分析（3）- 都是坑！这么简单的Alpha计算，竟然错了？！</h4>
        <h6 class="text-muted">2024-01-11</h6>
        <p class="card-text">我们继续 Alphalens 因子分析报告的解读。在过去的两篇笔记中，我们都提到，运用 Alphalens 进行因子分析步骤很简单，但是如果不了解它背后的机制与逻辑，很容易得到似是而非的结论。<!--数据精度问题： akshare 是爬虫机制。它的数据来自于财经网站的网页。这些网页是供人阅读用的。因此，它在一些数据显示上，都要进行人性化处理。比如，对换手率，它只保留两位百分数点。对于大市值的沪深 300 而言，它们的换手率平常本来也就在 1%~5%之间波动，这样就引起了数据碰撞 (clash)。它对因子分析究竟有多大的影响不得而知。但是，可以肯定的是，当我们用不同的数据源来进行研究时，得到的结果会有不同。 --><br></p>
        <a href="low-turnover-factor-3" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInUp">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/kaiyun.jpg"/>
    <div class="card-block">
        <h4 class="card-title">Alphalens因子分析(2) - low turnover秒杀98%的基金经理!</h4>
        <h6 class="text-muted">2024-01-10</h6>
        <p class="card-text"><br>上一篇笔记，我们已经为因子分析准备好了数据。这一篇笔记，我们就进行因子分析。分析过程在 Alphalens 中非常简单，核心是读懂它的报告。</p>
        <a href="alphalens-and-low-turnover-factor-2" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>



<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInRight">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/alphalens.jpg?2"/>
    <div class="card-block">
        <h4 class="card-title">Alphalens 因子分析 - 以低换手率因子为例(1)</h4>
        <h6 class="text-muted">2024-01-09</h6>
        <p class="card-text"><br>因子分析是量化研究的基本技能之一。通过因子分析，找出有效的因子，通过相关性去重后，就可以通过机器学习、线性回归等方法把因子组合起来，构成交易策略。这一篇笔记我们就介绍如何使用 Alphalens 来进行单因子分析。我们使用的因子是低换手率因子。</p>
        <a href="alphalens-and-low-turnover-factor-1" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInDown">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2024/01/normal-dist.jpg"/>
    <div class="card-block">
        <h4 class="card-title">Z-score 因子的深入思考</h4>
        <h6 class="text-muted">2024-01-04</h6>
        <p class="card-text">最新（2024 年 1 月）出版的 SC 技术分析（Techical Analysis of Stock & Commodities）的第 4 条文章给到了 Z-score，原文标题为《Z-score: How to use it in Trading》。今天的笔记，就借此机会，同步推出我们对通过Z-score来构建量化因子的一些观点。</p>
        <a href="z-score-as-a-factor" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>



<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInLeft">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2023/12/hdf5-book.jpg"/>
    <div class="card-block">
        <h4 class="card-title">200倍速！基于 HDF5 的证券数据存储</h4>
        <h6 class="text-muted">2024-01-02</h6>
        <p class="card-text">去年 15 日的笔记挖了个坑，给出了量化数据和因子的存储方案技术导图。这一篇笔记就开始填坑。即使我们购买了在线数据服务，比如 tushare, 聚宽的账号，我们仍然要构建自己的本地存储，为什么？</p>
        <a href="save-quote-data-with-hdf5" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInUp">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?girls"/>
    <div class="card-block">
        <h4 class="card-title">年终特稿：这个指标我愿称之为年度最强发现</h4>
        <h6 class="text-muted">2023-12-29</h6>
        <p class="card-text">如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，这个因子就是不二之选。</p>
        <a href="connor-rsi-the-best" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>



<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInRight">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?drink"/>
    <div class="card-block">
        <h4 class="card-title">05 Poetry: 项目管理的诗和远方</h4>
        <h6 class="text-muted">2023-12-26</h6>
        <p class="card-text">上一章里，我们通过 ppw 生成了一个规范的 python 项目，对初学者来说，许多闻所未闻、见所未见的概念和名词扑面而来，不免让人一时眼花缭乱，目不暇接。然而，如果我们不从头讲起，可能读者也无从理解，ppw 为何要应用这些技术，又倒底解决了哪些问题。<br><br>在 2021 年 3 月...</p>
        <a href="poetry-for-project-management" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInDown">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cats"/>
    <div class="card-block">
        <h4 class="card-title">Sharpe 5.5!遗憾规避因子</h4>
        <h6 class="text-muted">2023-12-26</h6>
        <p class="card-text">如果在你买入之后，股价下跌，你会在第二天急着抛吗？反之，如果在你卖出之后，股价上涨，你会反手追入吗？先别急着回答，我们来看看科学研究的结论是怎样的。关于这类问题，都是行为金融学研究的范畴。具体到这个场景，我们可以运用遗憾理论来解释。遗憾理论，又称遗憾规避理论（ Fear of Regret Theory），是行为金融学的重要理论之一，该理论认为，非理性的投资者在做决策时，会倾向于避免产生后悔情绪并追求自豪感，避免承认之前的决策失误。</p>
        <a href="how-regret-factor-get-5.5-sharpe-ratio" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInLeft">
    <img class="card-img-top img-responsive" src="https://images.jieyu.ai/images/2023/12/santa-claus.png"/>
    <div class="card-block">
        <h4 class="card-title">Santa Claus Rally</h4>
        <h6 class="text-muted">2023-12-25</h6>
        <p class="card-text"><!--  --><br>每天坚持发贴 。千字左右，图文并茂。声明：这一天我们也没有漏发。<br>---Santa Claus Rally 是指 12 月 25 日圣诞节前后股市的持续上涨这样一个现象。《股票交易员年鉴》的创始人 Yale Hirsch 于 1972 年创造了这个定义，他将当年最后五个交易日和次年前两个交易日的时间范围定义为反弹日期。</p>
        <a href="santa-claus-rally" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInUp">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?light"/>
    <div class="card-block">
        <h4 class="card-title">净新高占比因子</h4>
        <h6 class="text-muted">2023-12-24</h6>
        <p class="card-text">个股的顶底强弱比较难以把握，它们的偶然性太强。董事长有可能跑路，个股也可能遇到突发利好（比如竞争对手仓库失火）。在个股的顶底处，**情绪占据主导地位，理性退避次席，技术指标出现钝化**，进入<red>现状不可描述，一切皆有可能</red>的状态。但是，行业指数作为多个随机变量的叠加，就会出现一定的规律性（受A4系统性影响的偶然性我们先排除在外，毕竟也不是天天有A4）。这是因子分析和技术分析可以一展身手的地方。</p>
        <a href="net-high-net-low-factor" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>



<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInRight">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?dogs"/>
    <div class="card-block">
        <h4 class="card-title">QMT/XtQuant 之开发环境篇</h4>
        <h6 class="text-muted">2023-12-22</h6>
        <p class="card-text">!!! tip 笔记要点<br>    1. XtQuant 获取及安装<br>    2. XtQuant 工作原理 （图2）<br>    3. 版本和文档一致性问题 （图3）<br>    4. 使用 VsCode 远程开发</p>
        <a href="how-to-setup-xtquatn-development-env" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>


<div class="col-xs-12 col-md-6">
    <article class="card animated fadeInDown">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?room"/>
    <div class="card-block">
        <h4 class="card-title">量化数据免费方案之 QMT</h4>
        <h6 class="text-muted">2023-12-21</h6>
        <p class="card-text">!!! tip "学习要点"<br>    - xtquant 提供了数据和交易接口<br>    - xtquant 可以独立于 QMT 之外运行<br>    - download_history_data<br>    - download_history_data2<br>    - get_market_data</p>
        <a href="qmt-get-stock-price" class="btn btn-primary">Read more</a>
    </div>
    </article><!-- .end Card -->
</div>

</div>

</div>
