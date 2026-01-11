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

    .md-sidebar--primary {
    display: none;
    }
 }

a .card-title {
    color: rgb(55, 58, 60);
    font-size: 17px;
}

a .card-text {
    color: rgb(55, 58, 60);
    font-size: 14px;
}

a:hover {
    color: inherit;
    text-decoration: inherit;
}

nav a {
    font-size: 0.8rem !important;
    color: white;
    mix-blend-mode: difference;
}
</style>

<div class="as-grid m-t-md">
<div class="card-columns">
    
<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/tools/2026十大量化技术/fasthtml/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260110212357.png"/>
    <div class="card-body">
        <h4 class="card-title">量化新基建(三) - FastHTML：Python 全栈开发的终极答案</h4>
        <p class="card-text">这是2026量化新基建的第三篇文章了。我们的目标是介绍2026年，要打造一个量化交易系统，你可能（应该）使用的那些技术。今天我们要介绍的是，在2026年，你该使用什么样的技术来构建量化交易系统的前端。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2026-01-11</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/tools/2026十大量化技术/sqlite/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/153f985ba06d4a909bd17e097d904b20_3_with_two_logo.jpg"/>
    <div class="card-body">
        <h4 class="card-title">2026量化新基建(二) - sqlite 与 sqlite-utils</h4>
        <p class="card-text">对量化人来说，有一个场景，非常适合使用 sqlite： 无须安装和设置、以 pythonic 的方式进行开发，并且具有非常好的性能。但是，一直以来，我是直接使用 python 内置的 sqlite3 模块来操作 sqlite 数据库的。直到最近，我发现了 sqlite-utils 这个库，它让我以最简洁的方式，获得了全所未有的表达力。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2026-01-01</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/tools/2026十大量化技术/uv&pydantic/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251224163832.png"/>
    <div class="card-body">
        <h4 class="card-title">UV & Pydantic：重塑 2026 Python 工程化基石</h4>
        <p class="card-text">本文将探讨两项彻底改变 Python 开发体验的技术：Astral 的 UV —— 一个旨在替代 pip、poetry、pyenv 的全能包管理器；以及 Pydantic 2.0 —— 由 Rust 驱动的数据验证与解析库。它们的结合，构成了 2026 年高性能量化系统的标准地基。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-12-23</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/factor-strategy/打新不中，买新当如何/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251218114139.png"/>
    <div class="card-body">
        <h4 class="card-title">打新不中，买新当如何？lightgbm 打新模型如何构建？</h4>
        <p class="card-text">摩尔线程和沐曦股份这两天彻底激发了打新市场。前者中一签至少赚27万，后者中一签至少赚40万。如果中签，应该在什么价位卖出？如果不中，是否还有上车机会？机器学习模型来告诉你答案。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-12-18</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/algo/data-normalization/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/11/dmytro-yarish-yNTrQwvYjno-unsplash.jpg"/>
    <div class="card-body">
        <h4 class="card-title">夏普大于4的策略有多恐怖？但它为什么好得不真实？</h4>
        <p class="card-text">本文通过一个回测收益异常的案例，揭示了数据标准化中常见的“前视偏差”陷阱。全局Z-score或Min-Max归一化会引入未来数据，导致模型表现虚高。文章强调了使用滚动窗口等Point-in-Time方法进行正确归一化的重要性，以避免自我欺骗，获得真实收益。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-11-28</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/algo/昨天应该涨多少？Tushare和东财还没商量好/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/square/food/24.jpg"/>
    <div class="card-body">
        <h4 class="card-title">关于昨天应该涨多少这件事，Tushare 和 东财还没商量好</h4>
        <p class="card-text">最近在整一个适合个人使用的量化框架，数据源选择了 tushare，实时数据和交易 API 使用 QMT。在尝试一个策略时，发现该发出信号的时候，没有发出信号，于是就开始了排错之旅。这一查不要紧，发现就连最基本的每日涨跌幅数据也算不『对』了。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-11-24</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/tools/关于复权那些事儿/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/4x3/IMG_20251007_201839.jpg"/>
    <div class="card-body">
        <h4 class="card-title">前后复权都不对，动态复权又太贵！一文揭示策略失败的根本原因</h4>
        <p class="card-text">这是所有的量化课程都不会告诉你的，基于静态复权计算出来的因子，很可能不具有时间平稳性，这意味着我们无法基于它来发现统计规律。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-11-21</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/tools/moonshot/moonshot-is-all-you-need-5/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/4x3/IMG_20251007_193043.jpg"/>
    <div class="card-body">
        <h4 class="card-title">Moonshot is all you need - 红利策略完结篇</h4>
        <p class="card-text">本篇是本系列的最后一篇,运用之前的Moonshot回测框架，我们将最终完成红利策略的构建。5年回测结果表明，本策略年化达到11.6%，sharpe 高达4.55，远远超过同期沪深300.</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-11-09</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/factor-strategy/跟着国会山股神去炒股/">
    <img class="card-img-top img-responsive" src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/4x3/IMG_20251007_180707.jpg"/>
    <div class="card-body">
        <h4 class="card-title">Political Alpha，跟着国会山股神去炒股</h4>
        <p class="card-text">通过分析公开的国会议员交易记录，我们发现了令人惊讶的投资模式，这些数据背后隐藏着怎样的市场洞察？</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-11-03</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/factor-strategy/ESG策略初探-02/">
    <img class="card-img-top img-responsive" src="https://fastly.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/4x3/IMG_20251007_180707.jpg"/>
    <div class="card-body">
        <h4 class="card-title">ESG评分多空投资策略：买ESG评分高的公司真的能赚钱吗？（附分层回测通用代码）</h4>
        <p class="card-text">本文对华证与 Wind 的 ESG 评分分别构建“按披露日横截面分层、T+1 生效、前向填充到日频、等权持有到下一次披露”的策略框架，在最长可追溯样本期内进行系统回测.</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-10-26</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/career&figure/successfully-starting-a-career-in-quant-research/">
    <img class="card-img-top img-responsive" src="https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/23.jpg"/>
    <div class="card-body">
        <h4 class="card-title">如何选择量化交易基金，Max Dama 给你的7个建议</h4>
        <p class="card-text">对于想要在量化交易行业发展的新人，可能并不知道该如何挑选一家公司。因此，他们很容易在选择第一份工作时犯错。这个错误可能会导致你日后放弃这个行业，而事实上，你可能非常适合这个行业并取得成功。没有经验的人很容易犯错；但我想提供一些指导，帮助你避免一些常见的陷阱。</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-10-23</small></p>
    </div>
    </a>
</div><!--end-card-->


<div class="card">
    <a href="https://blog.quantide.cn/blog/posts/factor-strategy/ESG策略初探-01/">
    <img class="card-img-top img-responsive" src="https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/22.jpg"/>
    <div class="card-body">
        <h4 class="card-title">ESG策略初探-01</h4>
        <p class="card-text">从化石燃料到金融市场，绿色转型已不可逆。到2024年，151个国家宣布碳中和目标，120个将其纳入法律，86个给出清晰路线图。资本正在用估值与资金流向表态：可持续发展是新的共识。而在资本对“可持续价值”的抉择中，**ESG**正成为衡量企业与经济体可持续竞争力的核心标尺</p>
        <p class="card-text"><small class="text-muted"><i class="fa fa-calendar"></i>2025-10-22</small></p>
    </div>
    </a>
</div><!--end-card-->

</div>
</div>


