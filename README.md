
<div class="as-grid m-t-md">
<div class="card-columns">
    
<div>
<h3>量化人如何用好Jupyter环境？（一）</h3>
<img src="https://source.unsplash.com/random/360x200?girls" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>网上有很多jupyter的使用技巧。但我相信，这篇文章会让你全面涨姿势。很多用法，你应该没见过。<br><br>- 显示多个对象值<br>- 魔法：%precision %psource %lsmagic %quickref等<br>- vscode中的interactive window<br>---<br><br>...</p>

<p><span style="margin-right:20px">发表于 2024-03-04 人气 198 </span><span><a href="https://www.jieyu.ai/blog/2024/03/04/how-to-use-jupyter-as-quant-researcher">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>为什么量化人应该使用duckdb？</h3>
<img src="https://source.unsplash.com/random/360x200?flower" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>上一篇笔记介绍了通过duckdb，使用SQL进行DataFrame的操作。我们还特别介绍了它独有的 **Asof Join** 功能，由于量化人常常处理跨周期行情对齐，这一功能因此格外实用。但是duckdb的好手段，不止如此。* 完全替代sqlite，但命令集甚至超过了Postgres<br>* 易用性极佳<br>* 性能怪兽作为又一款来自人烟稀少的荷兰的软件，北境这一苦寒之地，再一次让人惊喜。科技的事儿，真是堆人没用。</p>

<p><span style="margin-right:20px">发表于 2024-02-01 人气 780 </span><span><a href="https://www.jieyu.ai/blog/2024/02/01/why-should-you-use-duckdb">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>给Pandas找个搭子，用SQL玩转Dataframe!</h3>
<img src="https://images.jieyu.ai/images/2024/01/panda.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>对有一定SQL基础的人来说，pandas中的查询会有点繁琐。在这篇文章，我们将给Pandas找个搭子，在用SQL方便的地方，我们用SQL；在用原生查询方便的地方，我们就用原生查询。这个搭子会是谁呢？</p>

<p><span style="margin-right:20px">发表于 2024-01-29 人气 847 </span><span><a href="https://www.jieyu.ai/blog/2024/01/29/use-sql-query-with-pandas">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>改用十进制！点差如何影响策略</h3>
<img src="https://images.jieyu.ai/images/2024/01/switch-to-decimal.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>笔记[左数效应、整数关口与光折射](http://www.jieyu.ai/blog/2024/01/23/left-side-effect-integer-pressure/)中引用了南加州大学Lawrence Harris的[一篇论文](/assets/ebooks/Stock-price-clustering-and-price-discreteness.pdf)中，哈理斯研究了交易价格的聚类效应。聚类效应对我们确定压力位、完善下单算法都有一定的影响。但是，2001年，美股变更交易制度，由分数制切换为十进制。这个变化就导致了他的研究结论**作废**。</p>

<p><span style="margin-right:20px">发表于 2024-01-26 人气 992 </span><span><a href="https://www.jieyu.ai/blog/2024/01/26/switch-to-decimal">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>来自世坤！寻找Alpha 构建交易策略的量化方法</h3>
<img src="https://images.jieyu.ai/images/2024/01/kitty-in-basket.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>问：常常看到有人说Alpha seeking，这究竟是什么意思？自己回答不如推荐一本书：《Finding Alphas: A Quantitative Approach to Building Trading Strategies》，它的题目正好就是寻找Alpha。我拿到的PDF是2019年的第二版。来自WorldQuant（世坤）的Igor Tulchinshky等人，Igor Tulchinshky是世坤的创始人。</p>

<p><span style="margin-right:20px">发表于 2024-01-25 人气 363 </span><span><a href="https://www.jieyu.ai/blog/2024/01/25/finding-alphas-a-quantitative-approach">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>左数效应 整数关口与光折射</h3>
<img src="https://images.jieyu.ai/images/2024/01/pressure-of-price-integer-cat.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>常常有人问，新的因子/策略从哪里来？今天的笔记或许能启发你的思路。从1932年起，研究人员就注意到以9结尾的价格（比如\$3.99），在消费者的认知中，要远远小于邻近的整数价格（\$4.00）。后来这一效应被称为 left-digit effect。在证券交易中，类似的情况一样存在，不过它的表现形式是整数关口压力。</p>

<p><span style="margin-right:20px">发表于 2024-01-24 人气 861 </span><span><a href="https://www.jieyu.ai/blog/2024/01/24/left-side-effect-integer-pressure">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>龙凤呈祥：这种无底限炒作，如何用量化方法发现它？</h3>
<img src="https://images.jieyu.ai/images/2024/01/dragon-and-phoenix.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>作为量化人，我们敏锐地观察市场，不放过任何一个可能产生利润的机会。一旦发现这样的机会，我们决不会在乎其它人怎么看怎么想，书上有没有这么讲。**但是，大胆假设，小心求证。**今天带来的因子，挺魔幻的，我把它叫做魔性汉字。如果你难以接受这种无底线的炒作，那么，我们换一个名字：另类因子。</p>

<p><span style="margin-right:20px">发表于 2024-01-23 人气 537 </span><span><a href="https://www.jieyu.ai/blog/2024/01/23/magic-hot-word-factor">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>量化研究员如何写一手好代码</h3>
<img src="https://images.jieyu.ai/images/2024/01/thesus.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>即使是Quant Research， 写一手高质量的代码也是非常重要的。再好的思路，如果不能正确地实现，都是没有意义的。只有正确实现了、通过回测检验过了，才能算是真正做出来了策略。写一手高质量的代码的意义，对Quant developer来讲就更是自不待言了。这篇notebook笔记就介绍一些python best practice。<br></p>

<p><span style="margin-right:20px">发表于 2024-01-18 人气 134 </span><span><a href="https://www.jieyu.ai/blog/2024/01/18/how-to-manage-python-project-as-quanter">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>ClickHouse: One table to rule them all!</h3>
<img src="https://images.jieyu.ai/images/2024/01/query-buillion-rows-in-ms.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>前面几篇笔记我们讨论了存储海量行情数据的个人技术方案。它们之所以被称之为个人方案，并不是因为性能弱，而是指在这些方案中，数据都存储在本地，也只适合单机查询。数据源很贵 -- 在这个冬天，我们已经听说，某些上了规模的机构，也在让员工共享万得账号了。所以，共享网络存储，从而只需要一个数据账号，就成为合理的需求。更不必说，集中管理才可能让 IT 来进行数据维护，而分析师只需要专注于策略就好。</p>

<p><span style="margin-right:20px">发表于 2024-01-17 人气 771 </span><span><a href="https://www.jieyu.ai/blog/2024/01/17/one-table-to-rule-them-all-with-clickhouse">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>找校友！起底百亿私募创始人</h3>
<img src="https://images.jieyu.ai/images/2024/01/routouline.jpg" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>国内百亿私募创始人的毕业学校新鲜出炉，有没有你的校友？从专业上看，数学（包括统计、金融数学）、计算机（含电子信息、软件）、物理是分布最多的专业。但也出现了文科专业（政治经济学）和商学专业。从地域分布上看，京、沪、浙领先，中部地区仅有江西财经大学为代表，西部地区仅有四川大学和西安交大两所高校入围。</p>

<p><span style="margin-right:20px">发表于 2024-01-16 人气 250 </span><span><a href="/articles/investment/量化杂谈/founders-of-private-equity">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>私募量化策略大盘点-2024年初</h3>
<img src="https://source.unsplash.com/random/360x200?breakfast" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>看了十几家私募路演报告，总结出2023年最有效的策略！因子挖掘还是以手工为主，最有效的因子（策略）仍然是技术类的趋势+反转，无论是CTA还是量化多头都是如此。模型构成基本上都是机器学习。其中树模型比神经网络占比更大一些，有的机构中使用率高达90%。</p>

<p><span style="margin-right:20px">发表于 2024-01-14 人气 890 </span><span><a href="https://www.jieyu.ai/blog/2024/01/14/review-of-private-equity-quantitative-strategies-in-2024">点击阅读</a></span></p>

</div><!--end-article-->


<div>
<h3>Jupyter Notebook中如何设置环境变量？</h3>
<img src="https://source.unsplash.com/random/360x200?girls" style="width: 300px" align="right"/>
<p><span>内容摘要:<br></span>我们常常通过Jupyter Notebook来分享代码和演示分析结果。有时候，我们需要在代码中使用账号和密码，如果它们也被分享出去，可就大不妙了。正确的做法是把密码设置在环境变量中，在代码中读取环境变量。但是，Jupyter Notebook默认设置下，并不能读取到主机的环境变量。</p>

<p><span style="margin-right:20px">发表于 2024-01-14 人气 813 </span><span><a href="https://www.jieyu.ai/blog/2024/01/14/how-to-set-env-in-jupyter-notebook">点击阅读</a></span></p>

</div><!--end-article-->

</div>
</div>


