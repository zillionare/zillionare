
<div class="as-grid m-t-md">
<div class="card-columns">
    
<div>
<h3>21天驯化AI打工仔 - SQEP与symbol编码性能测试</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span> 前言"007，我们需要讨论一个重要的性能优化问题，"我一边敲击键盘一边对我的 AI 助手说道。"什么问题？我已经准备好了，"007 回应道，它的语音合成器发出了一种几乎可以称为热情的声音。"在量化交易系统中，数据查询性能至关重要。我们需要测试一下股票代码编码方式对查询速度的影响。"前三天，我们讨论了如何从 Tushare 获取 OHLC (开盘价、最高价、最低价、收盘价) 数据和调整因子 (adj_factor)。当时我们存储的数据结构如下：```python<br>{<br>    "timestamp": "时间戳",<br>    "ts_code": "股票代码",<br>    "ohlc": {<br>        "ts_code": "股票代码",<br>        "open": "开盘价",<br>        "high": "最高价",<br>        "low": "最低价",<br>        "close": "收盘价",<br>        "vol": "成交量"<br>    },<br>    "adj_factor": {<br>        "ts_code": "股票代码",<br>        "trade_date": "交易日期",<br>        "adj_factor": "复权因子"<br>    }<br>}<br>```现在，我们需要设计一种通用的数据交换格式（Standard Quotes Exchange Protocol, SQEP）。这种格式的工作原理是：由数据生产者（因为只有生产者才了解原始数据的具体格式）将数据转换为这种标准格式，然后再将其推送到 Redis 中供消费者使用。"在金融数据处理中，毫秒级的延迟可能意味着巨大的差异，"007 解释道，"特别是在高频交易场景下，查询性能的优化至关重要。"我点点头："没错，其中一个关键问题是股票代码 symbol 的数据类型选择。理论上，整数类型的查询和比较操作应该比字符串更高效，但我们需要实际测试来验证这一点。""我可以帮你设计一个严谨的实验，"007 建议道，"我们可以生成足够大的数据集，然后在相同条件下比较 string 和 int64 类型的查询性能。"于是，我和 007 决定生成 1 亿条股票数据，对 string 类型和 int64 类型的 symbol 进行严谨公平的性能测试，以量化分析不同编码方式对查询效率的实际影响。这个实验将帮助我们在构建高性能量化交易系统时做出更明智的技术选择。 1. SQEP-BAR-DAY 日线场景下的数据交换格式"设计一个好的数据交换格式需要考虑多方面因素，"007 分析道，"包括数据完整性、传输效率、存储空间和查询性能。"SQEP-BAR-DAY 是标准行情交换协议 (Standard Quotes Exchange Protocol) 中用于日线数据的格式规范。该格式设计用于在不同系统组件间高效传输和处理股票日线数据，确保数据的一致性和互操作性。这种标准化的数据格式解决了量化交易系统中一个常见的痛点：不同数据源提供的数据格式各不相同，导致系统需要为每个数据源编写特定的处理逻辑。通过 SQEP，我们可以将这种复杂性隔离在数据生产者端，让消费者端的代码更加简洁和通用。 1.1. 字段定义SQEP-BAR-DAY 包含以下标准字段：| 字段名     | 数据类型      | 说明                                 |<br>| </p>

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
<p><span>内容摘要:<br></span> 前言<br>第一天，我们讨论了如何从Tushare获取OHLC(开盘价、最高价、最低价、收盘价)数据和调整因子(adj_factor)。当时我们存储的数据结构如下：```python<br>{<br>    "timestamp": "时间戳",<br>    "ts_code": "股票代码",<br>    "ohlc": {<br>        "ts_code": "股票代码",<br>        "open": "开盘价",<br>        "high": "最高价",<br>        "low": "最低价",<br>        "close": "收盘价",<br>        "vol": "成交量"<br>    }, <br>    "adj_factor": {<br>        "ts_code": "股票代码",<br>        "trade_date": "交易日期",<br>        "adj_factor": "复权因子"<br>    }<br>}<br>```现在，我们需要设计一种通用的数据交换格式（Standard Quotes Exchange Protocol, SQEP）。这种格式的工作原理是：由数据生产者（因为只有生产者才了解原始数据的具体格式）将数据转换为这种标准格式，然后再将其推送到Redis中供消费者使用。 1. SQEP-BAR-DAY 日线场景下的数据交换格式SQEP-BAR-DAY 是标准行情交换协议(Standard Quotes Exchange Protocol)中用于日线数据的格式规范。该格式设计用于在不同系统组件间高效传输和处理股票日线数据，确保数据的一致性和互操作性。 1.1. 字段定义SQEP-BAR-DAY 包含以下标准字段：| 字段名     | 数据类型      | 说明                                 |<br>| </p>

<p><span style="margin-right:20px">发表于 2025-05-14 人气 407 </span><span><a href="https://www.jieyu.ai/blog/2025/05/14/Taming-the-AI-Worker-in-21-Days-4">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 数据库的优化</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span> 前言<br>五一小长假之前，我在搭档 007 的帮助下已经成功实现了从 Tushare 获取 OHLC 数据，并通过 Redis 消息队列将数据存储到 ClickHouse 数据库。为了进一步完善量化交易系统的数据支持，今天我们将聚焦于数据库的优化设计，主要涉及获取日线复权因子、获取分钟线数据以及计算分钟线数据（例如 15 分钟）三个方面。五一结束之后，我们计划通过这些优化，能够为量化交易策略提供更丰富、更精细的数据，从而提升系统的性能和决策能力。 1. 获取日线的复权因子<br>> 我：007！帮我在 `data_producer.py` 和 `data_consumer.py` 中添加获取日线因子的代码。<br>> <br>> 007：🫡收到请求，正在处理...为了在 `data_consumer.py` 和 `data_producer.py` 中补充因子的数据，我们需要对原代码进行一些修改。主要思路是在生产者代码中获取因子数据并封装到数据结构中，然后在消费者代码中处理这些因子数据。因为后续我们要收集分钟级的数据，所以我新建了一张表，命名为 `daily_data`，用于存储日线因子数据。<br>;<br>``` 2.2. 修改生产者代码，添加分钟线数据获取功能<br>007 还是采用 tushare 来获取分钟线数据，并添加到数据表中。但是，这里获取分钟线数据我并不打算用 tushare 作为数据源，而是打算采用 qmt 提供的 API 接口来获取分钟级的数据。<!--<br>!!! note 改用 qmt 的一些理由<br>    QMT（迅投极速策略交易系统）相较于 Tushare 在获取分钟线数据方面有一些优势，以下是具体原因：    | 比较维度           | QMT                                                                                                                                                                                                                          | Tushare                                                                                                                                                                                  |<br>    | </p>

<p><span style="margin-right:20px">发表于 2025-05-13 人气 780 </span><span><a href="https://www.jieyu.ai/blog/2025/05/13/Taming-the-AI-Worker-in-21-Days-3">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 开发量化交易系统</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span> （二）实现 ClickHome 数据库<br><br>今天是第二天，我计划实现如下任务：<br>1. 安装 ClickHouse 和 DBeaver<br>2. 创建 ClickHouse 数据表<br>3. 修改 Redis 消息队列代码以支持 ClickHouse 存储<br><br>我唤醒了 007，它今天是...</p>

<p><span style="margin-right:20px">发表于 2025-05-11 人气 847 </span><span><a href="https://www.jieyu.ai/blog/2025/05/11/Taming-the-AI-Worker-in-21-Days-2">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>21天驯化AI打工仔 - 我如何获取量化数据</h3>
<img src="https://images.jieyu.ai/images/2025/05/20250514202750.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>IDEA：本人和本人的 AI黑奴 的相互协作，能不能在短短 21 天内开发出一套量化交易系统？<br><br>这么有意思的挑战，不如就从今天开始吧！“数据是一切开始的基础”，我打算先安排 AI黑奴 从数据获取开始做起。（感觉叫 AI黑奴 不太好听，那就给它取个名字叫：007号打码机，希望00...</p>

<p><span style="margin-right:20px">发表于 2025-05-10 人气 992 </span><span><a href="https://www.jieyu.ai/blog/2025/05/10/Taming-the-AI-Worker-in-21-Days-1">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>试过 Cursor 和 Trae 之后，我如何用 Augment 完成了一个复杂项目</h3>
<img src="https://images.jieyu.ai/images/2025/04/20250423201107.png" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>常常有人问，真有人用 AI 完成过一个复杂的项目吗？我！在这个过程中，我感受到 Augment （也许不只是 Augment，而是 AI 辅助编程）强大的力量。它帮我省下很多个小时。如果你是一位秀发飘逸的美女程序员，你更是应该用它 -- 它指定能保住你的头发 -- 不过这一点对我来说已经无关紧要了。</p>

<p><span style="margin-right:20px">发表于 2025-04-21 人气 363 </span><span><a href="https://www.jieyu.ai/blog/2025/04/21/how-do-i-workout-a-complex-project-using-augment">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas应用案例[3]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“Modin 通过多核并行加速 Pandas 操作，读取 10GB CSV 文件比 Pandas 快 4-8 倍；Polars 基于 Rust 架构，内存占用仅为 Pandas 的 1/3；Dask 则支持分布式计算，轻松处理 TB 级数据。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 861 </span><span><a href="https://www.jieyu.ai/blog/2025/04/05/numpy-pandas-for-quant-trader-20">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas应用案例[2]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/poster-on-wall.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“通过将字符串列转换为 category 类型，内存占用可减少 90% 以上；使用 itertuples 替代 iterrows，遍历速度提升 6 倍；结合 Numba 的 JIT 编译，数值计算性能可媲美 C 语言。”</p>

<p><span style="margin-right:20px">发表于 2025-04-05 人气 537 </span><span><a href="https://www.jieyu.ai/blog/2025/04/05/numpy-pandas-for-quant-trader-19">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas应用案例[1]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/christmas.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“Alphalens 要求因子数据是双重索引的 Series，价格数据是日期为索引、资产代码为列的 DataFrame。通过 Pandas 的 pivot_table 和 set_index，可以轻松完成格式转换，为因子分析奠定基础。”</p>

<p><span style="margin-right:20px">发表于 2025-04-04 人气 134 </span><span><a href="https://www.jieyu.ai/blog/2025/04/04/numpy-pandas-for-quant-trader-18">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Pandas核心语法[7]</h3>
<img src="https://images.jieyu.ai/images/hot/mybook/women-sweatshirt-indoor.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>“Pandas 的 DataFrame 提供了强大的样式功能，可以通过 Styler 对象实现类似 Excel 的条件着色效果。此外，Pandas 内置的绘图方法支持多种图表类型，轻松满足数据可视化需求。”</p>

<p><span style="margin-right:20px">发表于 2025-04-03 人气 771 </span><span><a href="https://www.jieyu.ai/blog/2025/04/03/numpy-pandas-for-quant-trader-17">点击阅读</a></span></p>

</div><!--end-article-->

</div>
</div>


