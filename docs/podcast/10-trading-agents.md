>[!tip]Flora: 量化好声音，睡前听一听！
> hello大家好！欢迎收听今天的量化好声音，我是Flora

> [!note]我是Aaron

>[!tip]Flora: 今天我们要来聊一聊一个非常有趣的话题
> 如何用大语言模型 来做一个
> 多智能体的金融交易框架

>[!note]Aaron: 
> 今天我们要介绍一个全网热搜的框架，叫TradingAgents
> 是不是听起来有点兴奋？这听起来就很硬核啊

>[!tip]
> Flora: Trading Agents
> 会交易的代理？

>[!note]Aaron: 对, Trading Agents
> 最近一个月，它很火啊，在github上新增了7k的赞

>[!tip]
> Flora: 对，我看了一下github的历史
> 这个库是今年2月创建的，但最近一个月势头很猛啊
> 看上去是不是实现了什么技术上的突破？

>[!note]Aaron: 也可能是因为它现在完全开源了

>[!tip]
> Flora: 这也就解释了为什么最近这么火了。
> Aaron，在介绍这个框架之前，是不是先给大家介绍下
> 之前大语言模型在量化交易方面的进展？

>[!note]Aaron: 
好的。在这个模型出来之前，其实市场上已经有一些大模型做量化交易的例子了。
比如bloombergGPT, XuanYuan 2.0, PIXIU, FinGPT等等
这里面像bloombergGPT，XuanYuan 2.0, PIXIU,它们主要是金融语料相关的一些NLP任务
比如数据结构化处理、情绪分析、金融知识问答等等
不涉及到量化模型和交易

>[!tip]Flora: 所以，你还没有介绍的FinGPT，应该是一个量化交易模型了？

> [!note]Aaron: 
> 对 FinGPT可视为与交易相关的模型
> 它基于情绪分析自动生成交易信号
> 信号体现为买卖时点

>[!tip]Flora: 这个实际上就是听消息炒股了
> 我们前几天还做了一期节目
> 介绍了the crystal ball trading challenge
> 根据Victor Haghani等人的实证研究
> 看起来听消息炒股是不太聪明的样子啊

> [!note]Aaron: 根据那个实验
> 就算你提前一天知道了消息
> 然后自己分析进行操作
> 最后还是反而会赔得更多
> 关键原因在于，
> 我们根据自己的认知来进行分析
> 常常会有很多误区，非常主观
> 我们自己得到的结论
> 就算是对的
> 也不见得就是世界的共识
> 所以，光知道消息不行
> 还得看看社交媒体上其它人的观点
> 而且还要从正反两方面看

>[!tip]Flora: 听到这里，我感觉好像明白什么了
> Aaron,你今天要介绍的trading agents
> 是不是正好针对这些方面做了改进？

>[!note]Aaron: 被你预判到了！
> 今天我们要介绍的这个框架啊
> 它其实是模拟了一个高水平的、真实的交易团队的这种协作
> 然后它里面有很多的
> 用大语言模型驱动的这种智能体，也就是Agent
> 每个智能体都有自己特定的角色,比如说
> 有做基本面分析的,有做情绪分析的
> 有做这种风险评估的 还有专门做交易的
> 它们会 通过这种 类似于辩论 来交换信息
> 最终结合历史数据来做出一个交易决策。

>[!tip]Flora: 作为一个技术派，我比较好奇
> 这些Agent里，应该也有做技术分析的吧？
> 就是看K线图指标那些

> [!note]Aaron: 
> 确实如此。还有看消息炒股的。
> 它有专门的分析新闻和社交媒体的Agent。

>[!tip]Flora: 这个虚拟团队，会有像真实团队一样的组织架构吗？

> [!note]Aaron: 它就是一个真实的团队
> 这个团队里，有我们刚刚说的这些Agent
> 相当于最前端的分析师
> 他们搜集资料、清洗数据
> 包括生成一些技术指标

>[!tip]Flora: 在真实的团队中，分析师处在前线
> 他们搜集市场情报
> 然后交给团队的专家，也就是研究团队

> [!note]Aaron: 正是如此
> trading agents也模拟了这样一个团队
> 而且最有意思的是，它把研究团队分为两派
> 一派是乐观派，总认为现在是牛市
> 另一派则是悲观派，总把现在当成熊市

>[!tip]Flora: 确实有点东西
> 我知道，在真实的团队中
> 这两派其实很难共存
> 即使一个团队中有这样两派
> 也很难进行理性的讨论
> 常常是相互看不起
> 尽管理想状态是兼听则明
> 实际上是一拍两散

> [!note]Aaron: 所以，这确实是人工智能带来的颠覆性机会
> 那我们继续介绍它的架构
> 这两派会分别出具买方证据和卖方证据
> 把这些证据交给交易员

>[!tip]Flora: 你这里说的交易员
> 应该还是系统中的Agent，而不是真实的交易员吧

> [!note]Aaron: 对 没错没错没错
> 交易员会结合这两种意见
> 形成自己的交易建议
> 然后再交给风控团队

>[!tip]Flora: 不用说，这仍然是一些Agent

> [!note]Aaron: 对，就是另外一些Agents
> 在最后面就是基金经理的角色了
> 所以，整个系统就是由一些
> 分工很细、很明确的Agent组成的
> 看起来，如果我们自己在本地搭建出这样一个系统
> 不仅可以节省成本，更重要的是
> 能获得更全面、综合、深入的思考
> 以及人类无法想像的思维速度！

>[!tip]Flora: 听上去确实是很赞的样子
> 那它的效果怎么样 有做过回测吗？

>[!note]Aaron: 有的
> 这个框架实际上是Uc berkeley，MIT等几个大学的中国学者提出来的
> 他们进行了比较深入的研究
> 在apple, google和Amazon等标的上进行了回测
> 结论是年化收益会大幅提升近30%左右
> 而最大回撤非常惊人
> 在amazone上回撤最大，也只有2.11%

>[!tip]Flora: 这些数据确实是非常优秀了！
> 大家可以去github上面玩一玩，自己动手试一试
> 大模型做金融的
> 我们见过的也不少了
> 那你认为这个模型有什么优势之处？

>[!note]Aaron: 之前的很多模型吧 它要么就是
> 只是专注在一个单一的任务上面 像做个分析呀 或者搜搜数据什么的
> 要么就是说 它没有去很好的模拟
> 真实的交易团队里面的这种复杂的互动

>[!tip]Flora: 对，交易不是一个人说了算，需要团队协作

>[!note]Aaron: 
> 所以这是这个项目最大的优势是它模拟了一个真实的交易团队
> 各个角色之间既分工、又协作，还会相互争吵

>[!tip]Flora: 所以这有点像之前比较流行的GPT里面
> 让多个分析师之间对话讨论
> 反复讨论、思辨，最后接近最正确的答案？

>[!note]Aaron: 对，很有点真理越辩越明的意思。

>[!tip]Flora: 恩。这也让我想到一个问题
> 毕竟我们知道，大模型是生成模型
> 它会自己加戏，会有幻觉，会编故事
> 那这样的话，各个Agent之间的讨论，还能做到基于事实
> 基于逻辑推理，
> 确保严谨吗？

>[!note]Aaron: 确实！如果让AI之间，用我们说话的这种自然语言沟通，
> 效率其实不高
> 而且信息传着传着 就容易跑偏
> 就像我们小时候玩那个
> 传话游戏 最后意思可能全拧了

>[!tip]Flora: 哈哈 对传话游戏那个比喻很形象
> 那这个TradingAgents是怎么解决这些问题的?

>[!note]Aaron: 它是设计了一种结构化的通讯协议
> 这个是非常重要的
> 因为传统的这种基于自然语言的通讯,
> 它很容易出现问题,比如它会遗忘一些信息
> 或者说它会扭曲一些信息 特别是在这种复杂任务的情况下
> 那在trading agents中，智能体之间的交流 主要是
> 通过这种结构化的文档和图表
> 比如说 分析师团队他们会输出一个分析报告
> 然后这个报告里面会有一些
> 非常明确的这种指标和他的建议
> 交易员会根据这个分析报告
> 再输出一个决策的信号
> 同样也是有他的理由和证据
> 它们只有在辩论的时候 才会使用自然语言对话
> 所以整个这个通讯是非常高效的,也避免了这种信息的丢失

>[!tip]Flora: 所以既利用大语言模型的优势
> 又利用结构化数据来限制它的缺点
> 所以它的改进从原理上就是不证自明的了
> 好的！今天我们聊了这个Tradingagents
> 那么这一切对我们听众朋友来说
> 可能意味着什么呢

> [!note]Aaron: 这里可能有一个值得我们再次思考的问题
> 当人工智能不再仅仅是一个个独立的分析工具
> 而是能够像人类团队一样
> 进行协作辩论 权衡利弊的时候
> 未来我们人类要怎么和这些
> 越来越聪明的AI同事一起工作
> 尤其是在金融这种高风险高回报
> 决策压力巨大的行业里
> 这种变化长远来看
> 会怎么改变我们对于专业知识
> 团队价值 甚至是角色过程的理解呢？

>[!tip]Flora: 这个问题可能值得我们个量化人都想一想
> 以上就是这期播客的全部内容了 非常感谢大家的收听 这里也提醒大家别忘了订阅我们的量化好声音

>[!note]Aaron: 对的，如果你想了解更多的量化资讯或者想要学习量化，欢迎大家订阅Quantide Research platform
> 这在里，我们提供了百余篇优质的文章和研报策略复现，并配有相关资料和可运行代码的notebook文件

>[!tip]Flora: 
> 此外，我们还开设有 量化24课和因子分析与机器学习策略 这两门课程
> 分别针对量化新手和专业的量化策略开发交易员，欢迎大家报名！

>[!note]Aaron: 好的 那咱们下期再见啦

>[!tip]Flora: 拜拜
