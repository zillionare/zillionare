<head>
<link href="assets/css/bootstrap.min.4.0.css" rel="stylesheet" />
<link href="assets/css/font-awesome-4.7.0/css/font-awesome.min.css" rel="stylesheet" />
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
.md-typeset h1,
.md-content__button {
    display: none;
}

.md-typeset hr {
    display: none;
}

.md-sidebar--primary {
    display: none;
}
.md-sidebar--secondary {
    display: none important!;
}

.as-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
}



@media (min-width: 768px) { 
    .card-columns {
        column-count: 2;
    }
 }

@media (min-width: 1200px) { 
    .card-columns {
        column-count: 3;
    }
 }

a .card-title {
    color: rgb(55, 58, 60);
}

a .card-text {
    color: rgb(55, 58, 60);
}

a:hover {
    color: inherit;
    text-decoration: inherit;
}

nav a {
    font-size: 0.8rem !important;
    color: white;
}
</style>
</head>

<div class="as-grid m-t-md">
<div class="card-columns">
    
<div class="card">
    <a href="blog/2024/01/12/low-turnover-factor-3">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?food"/>
    <div class="card-body">
        <h4 class="card-title">Alphalens因子分析(4) - Information Coefficient方法</h4>
        <p class="card-text">在前面的笔记中，无论是回报分析，还是因子Alpha，它们都受到交易成本的影响。信息分析 (Information Analysis)则是一种不受这种影响的评估方法，主要研究方法就是信息系数(Information Coefficient)。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-12</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="blog/2024/01/11/low-turnover-factor-3">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cloud"/>
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
    <a href="/articles/coursea/24lectures/detail">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?room"/>
    <div class="card-body">
        <h4 class="card-title">二十四课内容详情</h4>
        <p class="card-text">共40万字，461段超过7000行代码（另有若干策略代码作为福利赠送，未计入），这门课用一句话介绍：涵盖了量化交易全流程、学完就能进入实战的课程。<br><br>这门课程共分六个部分，24个章节。下面是各个部分及章节主要内容介绍，也透露出我们在选题与课程编排方面的考虑：<br><br> 一、 数据从...</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-04</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="/articles/coursea/24lectures/how-the-course-are-composed">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?girls"/>
    <div class="card-body">
        <h4 class="card-title">大富翁量化24课编排说明</h4>
        <p class="card-text"> 01 课程内容<br>本课程涵盖了从获得数据，到数据预处理、因子提取与分析、回测、可视化到实盘的全流程，介绍了众多量化必备库的用法，包括：<br> 如何获取数据<br>我们会介绍akshare, tushare, jqdatasdk这些常用库，也会介绍机构在用什么数据库<br> Pyt...</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-04</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="/articles/coursea/24lectures/faq">
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?cats"/>
    <div class="card-body">
        <h4 class="card-title">常见问题</h4>
        <p class="card-text"> 报名流程和学习环境<br><br>!!! abstract "课程怎么学？"<br>    课程以视频、notebook和答疑方式提供。视频在荔枝微课上，notebook由我们提供的服务器host。每周提供一次集中答疑，时间是周日晚8点，形式为腾讯会议。<br><br><br>    购买后，加宽...</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2024-01-04</small></p>
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
    <img class="card-img-top img-responsive" src="https://source.unsplash.com/random/360x200?food"/>
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

</div>
</div>


