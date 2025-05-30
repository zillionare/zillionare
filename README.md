
<div class="as-grid m-t-md">
<div class="card-columns">
    
<div>
<h3>21天驯化AI打工仔 - SQEP与symbol编码性能测试</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>"007，我们需要讨论一个重要的性能优化问题，"我一边敲击键盘一边对我的 AI 助手说道。"什么问题？我已经准备好了，"007 回应道，它的语音合成器发出了一种几乎可以称为热情的声音。"在量化交易系统中，数据查询性能至关重要。我们需要测试一下股票代码编码方式对查询速度的影响。"</p>

<p><span style="margin-right:20px">发表于 2025-05-18 人气 934 </span><span><a href="https://www.jieyu.ai/blog/2025/05/18/Taming-the-AI-Worker-in-21-Days-5">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Augment随手记</h3>
<img src="https://images.jieyu.ai/images/hot/gallery/banner/IMG_20250510_112543.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>Duckdb是一个年轻而迷人的数据库。它的备份可以简单到通过拷贝文件来完成 -- 但前提是，没有其它进程独占她。如果你的服务使用了duckdb，而且还在不停地读写她，你该怎么给她一个备份呢？<br><br>我们把这个问题抛给了Augment.<br><br><br>To Augment:<br><br>> 增加一个后台任...</p>

<p><span style="margin-right:20px">发表于 2025-05-17 人气 292 </span><span><a href="https://www.jieyu.ai/blog/2025/05/17/augment-daily-dose-1">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>致命的 ID -- DuckDB 中的 Returning 子句之谜</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514210946.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>Duckdb是一个年轻但非常有潜力的数据库。但它也有桀骜不驯的一面：在一个普通的update语句执行时，出现了罕见的违反外键约束的问题。最终，依靠Augment这个强大的AI工具，我们找到了根本原因，并且通过坚实的实验验证了结论。<br><br>『华生，你是否曾思考过，在数据库的深处，隐藏着...</p>

<p><span style="margin-right:20px">发表于 2025-05-14 人气 198 </span><span><a href="https://www.jieyu.ai/blog/2025/05/14/IDENTITY-The-Mystery-of-the-Returning-Clause">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 如何存储10亿个Symbol?</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>现在，我们需要设计一种通用的数据交换格式（Standard Quotes Exchange Protocol, SQEP）。这种格式的工作原理是：由数据生产者（因为只有生产者才了解原始数据的具体格式）将数据转换为这种标准格式，然后再将其推送到Redis中供消费者使用。</p>

<p><span style="margin-right:20px">发表于 2025-05-14 人气 407 </span><span><a href="https://www.jieyu.ai/blog/2025/05/14/Taming-the-AI-Worker-in-21-Days-4">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 数据库的优化</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>五一小长假之前，我在搭档 007 的帮助下已经成功实现了从 Tushare 获取 OHLC 数据，并通过 Redis 消息队列将数据存储到 ClickHouse 数据库。为了进一步完善量化交易系统的数据支持，今天我们将聚焦于数据库的优化设计，主要涉及获取日线复权因子、获取分钟线数据以及计算分钟线数据（例如 15 分钟）三个方面。五一结束之后，我们计划通过这些优化，能够为量化交易策略提供更丰富、更精细的数据，从而提升系统的性能和决策能力。</p>

<p><span style="margin-right:20px">发表于 2025-05-13 人气 780 </span><span><a href="https://www.jieyu.ai/blog/2025/05/13/Taming-the-AI-Worker-in-21-Days-3">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 开发量化交易系统</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>今天是第二天，我计划实现如下任务：<br>1. 安装 ClickHouse 和 DBeaver<br>2. 创建 ClickHouse 数据表<br>3. 修改 Redis 消息队列代码以支持 ClickHouse 存储我唤醒了 007，它今天是要陪我一起战斗代码的。</p>

<p><span style="margin-right:20px">发表于 2025-05-11 人气 847 </span><span><a href="https://www.jieyu.ai/blog/2025/05/11/Taming-the-AI-Worker-in-21-Days-2">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 我如何获取量化数据</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>IDEA：本人和本人的 AI黑奴 的相互协作，能不能在短短 21 天内开发出一套量化交易系统？这么有意思的挑战，不如就从今天开始吧！“数据是一切开始的基础”，我打算先安排 AI黑奴 从数据获取开始做起。（感觉叫 AI黑奴 不太好听，那就给它取个名字叫：007号打码机，希望007号“牛码”可以“码力全开”）好！下面我们正式准备开发工作！</p>

<p><span style="margin-right:20px">发表于 2025-05-10 人气 992 </span><span><a href="https://www.jieyu.ai/blog/2025/05/10/Taming-the-AI-Worker-in-21-Days-1">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>试过 Cursor 和 Trae 之后，我如何用 Augment 完成了一个复杂项目</h3>
<img src="https://images.jieyu.ai/images/2025/04/20250423201107.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>常常有人问，真有人用 AI 完成过一个复杂的项目吗？我！在这个过程中，我感受到 Augment （也许不只是 Augment，而是 AI 辅助编程）强大的力量。它帮我省下很多个小时。如果你是一位秀发飘逸的美女程序员，你更是应该用它 -- 它指定能保住你的头发 -- 不过这一点对我来说已经无关紧要了。</p>

<p><span style="margin-right:20px">发表于 2025-04-21 人气 363 </span><span><a href="https://www.jieyu.ai/blog/2025/04/21/how-do-i-workout-a-complex-project-using-augment">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>20 - Pandas应用案例[3]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“Modin 通过多核并行加速 Pandas 操作，读取 10GB CSV 文件比 Pandas 快 4-8 倍；Polars 基于 Rust 架构，内存占用仅为 Pandas 的 1/3；Dask 则支持分布式计算，轻松处理 TB 级数据。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 861 </span><span><a href="/articles/python/numpy&pandas/numpy-pandas-for-quant-trader-20">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>19 - Pandas应用案例[2]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/poster-on-wall.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“通过将字符串列转换为 category 类型，内存占用可减少 90% 以上；使用 itertuples 替代 iterrows，遍历速度提升 6 倍；结合 Numba 的 JIT 编译，数值计算性能可媲美 C 语言。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 537 </span><span><a href="/articles/python/numpy&pandas/numpy-pandas-for-quant-trader-19">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas应用案例[3]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“Modin 通过多核并行加速 Pandas 操作，读取 10GB CSV 文件比 Pandas 快 4-8 倍；Polars 基于 Rust 架构，内存占用仅为 Pandas 的 1/3；Dask 则支持分布式计算，轻松处理 TB 级数据。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 134 </span><span><a href="https://www.jieyu.ai/blog/2025/04/05/numpy-pandas-for-quant-trader-20">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas应用案例[2]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/poster-on-wall.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“通过将字符串列转换为 category 类型，内存占用可减少 90% 以上；使用 itertuples 替代 iterrows，遍历速度提升 6 倍；结合 Numba 的 JIT 编译，数值计算性能可媲美 C 语言。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 771 </span><span><a href="https://www.jieyu.ai/blog/2025/04/05/numpy-pandas-for-quant-trader-19">点击阅读</a></span></p>

</div><!--end-article-->

</div>
</div>


