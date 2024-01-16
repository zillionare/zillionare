
<div class="as-grid m-t-md">
<div class="card-columns">
    
<div>
<h3>2024 年，如何打造惊艳的个人博客/出版系统并且赚点小钱？</h3>
<img src="http://www.jieyu.ai/articles/python/best-practice-python/chap01/" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>几年前，我就推荐过用 Markdown 写作静态博客。静态博客几乎是零托管成本，比较适合个人博客起步。Markdown 便于本地搜索，也可当作是个人知识库方案。现在有了新的进展。我不仅构建了一个视觉上相当不错的个人网站，还美化了 github、构建了个人出版系统 -- 将文章导出为排版精美的图片和 pdf 的能力。<!--more-->这一方案的核心是 Mkdocs 和 Mkdocs-material。前者是 Python 技术文档构建系统，后者是与之适配的主题。我在 [《Python 能做大项目》](http://www.jieyu.ai/articles/python/best-practice-python/chap01/) 这本书中，深入介绍过这两种技术。现在，基于这两种技术，我们可以走得更远：不仅可以撰写技术文档，更可以打造博客和门户网站。下图就是截取的 [大富翁量化](https://www.jieyu.ai) 的网站界面： 这本书的第 10 章中了，这里我们只介绍如何开通博客功能，以及定制首页。Material 自带了博客插件，我们只需要在配置中启用它（以及其它相关插件）:```yaml<br>plugins:<br>  - awesome-pages:<br>      collapse_single_pages: true<br>  - blog:<br>      post_excerpt_separator: </p>

<p><span style="margin-right:20px">发表于 2024-01-15</span><span><a href="https://www.jieyu.ai/blog/2024/01/15/static-site-in-2024">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>私募量化策略大盘点-2024年初</h3>
<img src="https://source.unsplash.com/random/360x200?tiddy" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>看了十几家私募路演报告，总结出2023年最有效的策略！因子挖掘还是以手工为主，最有效的因子（策略）仍然是技术类的趋势+反转，无论是CTA还是量化多头都是如此。模型构成基本上都是机器学习。其中树模型比神经网络占比更大一些，有的机构中使用率高达90%。</p>

<p><span style="margin-right:20px">发表于 2024-01-14</span><span><a href="https://www.jieyu.ai/blog/2024/01/14/review-of-private-equity-quantitative-strategies-in-2024">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Jupyter Notebook中如何设置环境变量？</h3>
<img src="https://source.unsplash.com/random/360x200?cats" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>我们常常通过Jupyter Notebook来分享代码和演示分析结果。有时候，我们需要在代码中使用账号和密码，如果它们也被分享出去，可就大不妙了。正确的做法是把密码设置在环境变量中，在代码中读取环境变量。但是，Jupyter Notebook默认设置下，并不能读取到主机的环境变量。</p>

<p><span style="margin-right:20px">发表于 2024-01-14</span><span><a href="https://www.jieyu.ai/blog/2024/01/14/how-to-set-env-in-jupyter-notebook">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Alphalens因子分析(4) - Information Coefficient方法</h3>
<img src="https://source.unsplash.com/random/360x200?room" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>在前面的笔记中，无论是回报分析，还是因子Alpha，它们都受到交易成本的影响。信息分析 (Information Analysis)则是一种不受这种影响的评估方法，主要研究方法就是信息系数(Information Coefficient)。</p>

<p><span style="margin-right:20px">发表于 2024-01-12</span><span><a href="https://www.jieyu.ai/blog/2024/01/12/low-turnover-factor-3">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>因子分析（3）- 都是坑！这么简单的Alpha计算，竟然错了？！</h3>
<img src="https://source.unsplash.com/random/360x200?dogs" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>我们继续 Alphalens 因子分析报告的解读。在过去的两篇笔记中，我们都提到，运用 Alphalens 进行因子分析步骤很简单，但是如果不了解它背后的机制与逻辑，很容易得到似是而非的结论。<!--数据精度问题： akshare 是爬虫机制。它的数据来自于财经网站的网页。这些网页是供人阅读用的。因此，它在一些数据显示上，都要进行人性化处理。比如，对换手率，它只保留两位百分数点。对于大市值的沪深 300 而言，它们的换手率平常本来也就在 1%~5%之间波动，这样就引起了数据碰撞 (clash)。它对因子分析究竟有多大的影响不得而知。但是，可以肯定的是，当我们用不同的数据源来进行研究时，得到的结果会有不同。 --><br></p>

<p><span style="margin-right:20px">发表于 2024-01-11</span><span><a href="https://www.jieyu.ai/blog/2024/01/11/low-turnover-factor-3">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Alphalens因子分析(2) - low turnover秒杀98%的基金经理!</h3>
<img src="https://images.jieyu.ai/images/2024/01/kaiyun.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span><br>上一篇笔记，我们已经为因子分析准备好了数据。这一篇笔记，我们就进行因子分析。分析过程在 Alphalens 中非常简单，核心是读懂它的报告。</p>

<p><span style="margin-right:20px">发表于 2024-01-10</span><span><a href="https://www.jieyu.ai/blog/2024/01/10/alphalens-and-low-turnover-factor-2">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Alphalens 因子分析 - 以低换手率因子为例(1)</h3>
<img src="https://images.jieyu.ai/images/2024/01/alphalens.jpg?2" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span><br>因子分析是量化研究的基本技能之一。通过因子分析，找出有效的因子，通过相关性去重后，就可以通过机器学习、线性回归等方法把因子组合起来，构成交易策略。这一篇笔记我们就介绍如何使用 Alphalens 来进行单因子分析。我们使用的因子是低换手率因子。</p>

<p><span style="margin-right:20px">发表于 2024-01-09</span><span><a href="https://www.jieyu.ai/blog/2024/01/09/alphalens-and-low-turnover-factor-1">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Z-score 因子的深入思考</h3>
<img src="https://images.jieyu.ai/images/2024/01/normal-dist.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>最新（2024 年 1 月）出版的 SC 技术分析（Techical Analysis of Stock & Commodities）的第 4 条文章给到了 Z-score，原文标题为《Z-score: How to use it in Trading》。今天的笔记，就借此机会，同步推出我们对通过Z-score来构建量化因子的一些观点。</p>

<p><span style="margin-right:20px">发表于 2024-01-04</span><span><a href="https://www.jieyu.ai/blog/2024/01/04/z-score-as-a-factor">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>存了50TB！pyarrow + parquet</h3>
<img src="https://images.jieyu.ai/images/2024/01/apache-arrow.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span><br>在上一篇笔记中，我们指出，如果我们只在日线级别上存储行情数据和因子，HDF5 无论如何都是够用了。即使是在存储了 40 年分钟线的单个股数据集上，查询时间也只花了 0.2 秒 -- 这个速度已经足够快了，如果我们不需要在分钟级别上进行横截面数据查询的话。<br></p>

<p><span style="margin-right:20px">发表于 2024-01-03</span><span><a href="https://www.jieyu.ai/blog/2024/01/03/pyarrow-plus-parquet">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>200倍速！基于 HDF5 的证券数据存储</h3>
<img src="https://images.jieyu.ai/images/2023/12/hdf5-book.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>去年 15 日的笔记挖了个坑，给出了量化数据和因子的存储方案技术导图。这一篇笔记就开始填坑。即使我们购买了在线数据服务，比如 tushare, 聚宽的账号，我们仍然要构建自己的本地存储，为什么？</p>

<p><span style="margin-right:20px">发表于 2024-01-02</span><span><a href="https://www.jieyu.ai/blog/2024/01/02/save-quote-data-with-hdf5">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>年终特稿：这个指标我愿称之为年度最强发现</h3>
<img src="https://source.unsplash.com/random/360x200?drink" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>如果说在多因子时代，我们可以仅凭一个因子就构建出策略，并且还很有可能跑赢市场的话，这个因子就是不二之选。</p>

<p><span style="margin-right:20px">发表于 2023-12-29</span><span><a href="https://www.jieyu.ai/blog/2023/12/29/connor-rsi-the-best">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>xtquant 中的板块数据</h3>
<img src="https://images.jieyu.ai/images/2023/12/sector-cloud.jpg?4" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>!!! tip 笔记要点1. xtquant 中有哪些板块和板块分类？<br>    1. 如何获取板块的成份股？<br>    2. 如何获取指数的行情数据？</p>

<p><span style="margin-right:20px">发表于 2023-12-27</span><span><a href="https://www.jieyu.ai/blog/2023/12/27/qmt-set-sector">点击阅读</a></span></p>

</div><!--end-article-->

</div>
</div>


