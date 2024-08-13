---
title: "[0811] QuanTide Weekly"
date: 2024-08-11
seq: 第 4 期
category: others
slug: quantide-weekly-0811
img: https://images.jieyu.ai/images/2024/08/kenneth-griffin.jpg
stamp_width: 60%
stamp_height: 60%
tags: [others, weekly, career]
---

## 本周要闻

* 央行表示，将在公开市场操作中增加国债买卖。坚决防范汇率超调风险。
* 统计局：七月 CPI 同比上涨 0.5%，PPI 同比下降 0.8%
* 美最新初请失业金人数明显下降，市场对经济衰退的担忧稍解，美股震荡回升

## 下周看点

* 周二晚美国PPI，周三晚美国核心CPI和周四零售销售数据
* 周五（8 月 16 日）股指期货交割日
* 周一马斯克连线特朗普

## 本周精选

* Datathon-我的 Citadel 量化岗之路！附历年比赛资料
* 视频通话也不能相信了！ Deep-Live-Cam 一夜爆火，伪造直播只要一张照片！
* 介绍一个量化库之 tsfresh

---

<remark>上期<b>本周要闻</b>中提到巴斯夫爆炸，维生素价格飙涨。本周维生素板块上涨 3.6%，最高上涨 6.7%。</remark>

* 周末央行密集发声，完善住房租赁金融支持体系，支持存量商品房去库存。研究适度收窄利率走廊宽度。做好跨境资金流动的监测分析，防止形成单边一致性预期并自我强化，坚决防范汇率超调风险。<remark>利率走廊是指中央银行设定的短期资金市场利率波动范围。它通常由三个利率构成：<br>政策利率：通常是央行的基准利率，如再贴现率或存款准备金利率。<br>超额准备金利率（上限）：银行存放在央行的超额准备金所获得的利息。<br>隔夜拆借利率（下限）：银行间市场的最低借贷成本。</remark>
* 7 月 CPI 同比上涨 0.5%，前值 0.3%。其中猪肉上涨 20.4%，影响 CPI 上涨 0.24%。畜肉类价格上涨 4.9%，影响 CPI 上涨约 0.14%。受市场需求不足及部分国际大宗商品价格下行等因素影响，PPI 下降 0.8%，环比下降 0.2%。<br><remark>猪肉以一己之力拉升 CPI 涨幅近一半。猪肉短期上涨过快，涨势恐难持续，将对下月 CPI 环比构成压力。</remark>
* 此前因 7 月失业率上升、巴菲特大幅减仓、日央行加息等多重导致全球股市巨幅震荡，美股经历2024年以来市场波动最大的一周。但在 8 日，美公布上周初请失业救济人数为 23.3 万，前值 25 万，预期 24 万。数据大幅好于前值和预期之后，市场担忧减弱，美股、日经等上周先跌后涨，基本收复失地。这一事件表明，近期市场对数据报告格外敏感。

---

* 周五消息，嘉实基金董事长赵学军因个人问题配合有关部门调查。方正证券研究所所长刘章明被调整至副所长，不再担任研究所行政负责人。刘今年一月因违规荐股被出具警示函。

## 下周看点

* 下周二、周三和周四，事关美联储降息的几大重要数据，如PPI, CPI和零售销售数据都将出炉。美联储鹰派人物表示，通胀率仍远高于委员会2%的目标，且存在上行风险。财报方面，家得宝、沃尔玛值得关注，身处商品供应链末端的大卖场们可能对于通胀在加速还是降速有更切身的体会。
* 周五（8 月 16 日）股指期货交割日。今年以来，股指期货交割日上证指数表现比较平稳，甚至以上涨为主。

<claimer>根据财联社、东方财富、证券时报等资讯汇编</claimer>

---

# DATATHON-我的 CITADEL 量化岗之路！附历年比赛资料

![](https://www.citadel.com/wp-content/uploads/2024/07/Citadel_Intenship_KenSpeakstoInterns_YT_v2.jpg)
<cap>Kenneth Griffin Speak to Interns</cap>

Citadel 是一家顶级的全球性对冲基金管理公司，由肯尼斯. 格里芬 (Kenneth Griffin) 创建于 1990 年，是许多量化人的梦中情司。

Citadel 为应届生提供多个岗位，但往往需要先进行一段实习。

Citadel 的实习资格也是比较有难度，这篇文章就介绍一些通关技巧。

---

我们会对主要的三类岗位，即**投资**、**量化研究**和**软件研发**都进行一些介绍，但是重点会在量化研究岗位上。

我们将介绍获得量化研究职位的一条捷径，并提供一些重要的准备资料。

<!--
## wonderlic 测试

Citadel 在线评估测试，也称为 Citadel Wonderlic 测试，基本上是一种心理测量评估，旨在衡量各种技能，否则无法通过查看候选人的简历或在工作中所做的事情来衡量各种技能。 - 人物访谈。这些技能包括；决策、解决问题、学习新信息的能力以及适应不断变化的工作环境的能力。

Citadel 还使用此测试来简化招聘过程。这是因为作为一家具有这种能力的公司，它每年都会收到数千份为其提供建议的所有职位的申请。因此，使用 Wonderlic 这样的工具从一开始就淘汰掉不合格的候选人，而不是花费大量的时间和资源进行面对面的面试，这是很有意义的。

50 个问题，12 分钟，每个问题 14 秒。可以在网上找一些备考课程。一般在 500 到 1000 之间

Wonderlic Select 并不是唯一的 Citadel 评估。如果您正在尝试 Citadel 软件工程师实习，您可能会面临 HackerRank 编码评估。如果您申请成为 Citadel 交易实习生，您将被要求参加 Citadel 金融概念评估休息 (Citadel FCAT)。

-->

---

## 投资类岗位

投资类岗位可能是最难申请的，但待遇十分优渥。

2025 年的本科或者硕士实习生将拿到 5300 美元的周薪，并且头一周都是住在四季酒店里，方便新人快速适应自己的同伴和进行社交。

在应聘条件上面，现在的专业和学校背景并不重要，你甚至可以不是经济学或者金融专业的，但需要对股票的估值感兴趣。

但他们的要求是“非凡 (Extraordianry)” -- 这个非凡的标准实际上比哈佛的录取标准还要高一些。Citadel 自称录用比是 1%，哈佛是 4%。如果要对非凡举个例子的话，Citadel 会介绍说，他们招过 NASA 宇航员。

所以，关于这个岗位，我很难给出建议，但是 Citadel 在面试筛选上，是和 Wonderlic 合作的，如果你确实很想申这个岗位，建议先报一个 Wonderlic 的培训，大约$50 左右。Wonderlic Select 会有认知、心理、文化和逻辑方面的测试，参加此类培训，将帮你刷掉一批没有准备的人。

![](https://images.jieyu.ai/images/2024/08/11-weeks-of-extraordianry-growth.jpg)
<cap>11 weeks of extraordinary growth program</cap>

---

一旦入选为实习生，Citadel 将提供一个 11 周的在岗实训，实训内容可以帮助你快速成长。通过实训后，留用的概率很大。

## 软件研发类

这个岗位比较容易投递，Citadel 在做一个很基本的筛选后，很快就会邀请你参加 HackerRank 测试。由于 HackerRank 是自动化的，所以，几乎只要申请，都会得到邀请。

HackerRank 有可能遇到 LeetCode 上困难级的题目，但也有人反映会意外地遇到 Easy 级别的题目。总的来说，平时多刷 Leetcode 是会有帮助的。并且准备越充分，胜出的机会就越大。

你可以在 glassdoor 或者一亩三分地（1point3acres）上看到 Citadel 泄漏出来的面试题，不过，多数信息需要付费。

## 量化研究和 Datathon

参加 Datathon 并争取好的名次，是获得**量化研究岗位**实习的捷径。从历年比赛数据来看，竞争人数并不会很多（从有效提交编号分析），一年有两次机会。

这个比赛是由 correlation one 承办的。c1 是由原对冲基金经理 Rasheed Sabar 发起的，专注于通过培训解决方案帮助企业和发展人才。

它的合作对象有 DoD, Amazon, Citadel, Point 72 等著名公司。可能正是因为创始人之前的职业人脉，所以它拿到了为 Citadel, Point 72 举办竞赛和招募的机会。在它的网站上有一些培训和招募项目，也可以看一看。

---

![75%](https://images.jieyu.ai/images/2024/08/correlation-one.jpg)
<cap>Correlation One</cap>

Datathon 只针对在校生举办，你得使用学校邮箱来申请。通过官网在线报名后，你需要先进行一个**90 分钟**的在线评估。这个评估有心理和价值观的、也有部分技术的。

评估结果会在**比赛前三天**通知。然后进入一个社交网络阶段（network session），在此阶段，你需要组队，或者加入别人的队伍。Datathon 是协作性项目，一般要求**4 人一队**参赛。

正式开始后，你会收到举办方发来的问题和数据集（**我们已搜集历年测试问题、数据集及参赛团队提交的答案到网站，地址见文末**），需要从中选择一个问题进行研究，并在 7 天内提交一个报告，阐明你们所进行的研究。

这个过程可能对内地的学生来讲生疏一些，但对海外留学生来讲，类似的协作和作为团队进行 presentation 是很平常的任务了。所以，内地的学生如果想参加的话，更需要这方面的练习，不然，会觉得 7 天时间太赶。

---

## 女生福利

女生除可以参加普通的 Datathon 之外，还有专属的 Women's Datathon，最近的一次是明年的 1 月 10 日，现在开始准备正是好时机。

不过，这次 Women's Datathon 是线下的，仅限美国和加拿大在读学生参加。

## Datathon 通关技巧

Datathon 看起来比赛的是数据分析能力，是硬技巧，但实际上，熟悉它的规则，做好团队协作也非常重要。而且从公司文化上讲，Citadel 很注重协作。

1. 组队时，一定要确保团队成员使用相同的编程语言，否则工作结果是没有办法聚合的。
2. 尽管 Citadel 没有限制编程语言和工具软件，但最终提供的报告必须是 PDF, PPT 或者 HTML。并且，如果你提交的 PDF 包含公式的话，还必须提供 latex 源码。考虑到比赛只有 7 天，所以你平时就必须很熟悉这些工具软件。或者，当你组队时，就需要考虑，团队中必须包含一个有类似技能的人。
3. Datathon 是在线的虚拟竞赛，所以，并没有现场的 presentation 环境。因此，一定要完全熟悉和遵循它的提交规范。
4. 也正是因为上一条，Report 一定要条理清晰，一定要从局外人的身份多读几次，看看项目之外的人读了这份报告，能否得到清晰的印象。
5. 尽可能熟悉 Jupyter Notebook 和 pandas（如果你使用 Python 的话）。这也是官方推荐，通过 Notebook 可以快速浏览竞赛所提供的数据集。

---

6. 补充数据是有益的，这能反映你跳出框架自己解决问题的能力。所以平常要多熟悉一些数据集。如果一些数据要现爬的话，那需要非常熟悉爬虫。因为爬虫与后面的数据分析是串行的。在数据拿下来之前，其它工作都只能等待。
7. Visualization 非常重要。如果你习惯使用 Python，平时可以多练习 matplotlib 和 seaborn 这两个库。
   
我们已经搜集了 2017 年以来所有的竞赛题目，包括数据、问题，以及一些团队提交的报告和代码。如果你需要准备 Datathon，这会是一个非常好的参考。

在这里，我们对 2024 年夏的 Datathon 做一个简单介绍。

## 2024 年 Summer Datathon

![](https://images.jieyu.ai/images/2024/08/datathon-2024-summer-ps.jpg)
<cap>Problem Statement of 2024 Summer Datathon</cap>

2024 年的 Datathon 于 8 月 5 日刚刚结束。这次的题目是关于垃圾食品的，要求从提供的数据集中，得出关于美国食品加工的一些结论。除了指定数据集之外，也允许根据需要自行添加新的数据集。不过，这些数据集也提交给评委，并且不得超过 2G。

论题可以从以下三个之中选择，也可以自行拟定：

---

1. 能够从肉类生产来预测餐馆的股价吗？
2. 糖的价格会影响年青人对含糖饮料的消费吗？如果存在影响，这种影响会有地区差异吗？
3. 肉制品生产低谷与失业人数相关吗？

有的团队已经将竞赛数据集、问题及他们的答案上传到 github，下表是我们搜集的部分 repo 列表。其中包含了一些当年夺得过名次的 solution，非常值得研究。如果你在练习中能达到此标准，那么就有较大概率在自己的比赛中取得名次。

| year                                                                         | rank | files              | 说明                   |
| ---------------------------------------------------------------------------- | ---- | ------------------ | ---------------------- |
| [2024 summer](https://github.com/arjashok/2024-Summer-Datathon)              | NA   | data, code, report | 两个团队的报告，可运行 |
| [2024 spring](https://github.com/chtang-hmc/Spring-Invitation-Datathon-2024) | NA   | data, code, report | 目录清晰，报告质量高   |
| [2023](https://github.com/redders7/datathon2023)                             | NA   | report, code       |                        |
| [2022](https://github.com/Bennyoooo/citadel_datathon_2022)                   | 3rd  | report, code       | 报告质量高，可视化效果 |
| [2021 summer](https://github.com/joshuali99/Citadel-Summer-Datathon-2021)    | 1st  | data, src, report  | 包含 airbnb 数据       |
| [2021 spring](https://github.com/evilpegasus/datathon-spring-2021)           | NA   | data,code,report   |                        |
| [2020]                                                                       | 3rd  | report             |                        |
| [2018](https://github.com/wlong0827/citadel-datathon-2018)                   | 1st  | data,code,report   | 两个团队的报告         |
| [2017]                                                                       | NA   | report,code,data   |                        |

这些竞赛的资料也都上传到了我们的 Jupyter Lab 服务器，只需要付很小的费用就可以使用。无须下载和安装，你就可以运行和调试其他人提交的答案。

![75%](https://images.jieyu.ai/images/2024/08/datathon-screenshot.jpg)
<cap>Datathon 历年资料</cap>

---

如果你想立即开始练习，可以[申请使用我们的课程环境](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662263140&idx=1&sn=e0e0f226e385d2f3866a016b5886c2c7&chksm=f1e5aa3dc692232bcad109555676aed1cd86e6af4ca117f1cb9b195ae82a6addeb2e1b1bb9f7&payreadticket=HGygwRghkKW2urwKdqW4GaeGTsLWib7U82M8r7Pj7Sw9-POZVrrNC5iMskYZQYG_UM2u5BM#rd)，这样可以节省你下载数据、安装环境的时间。我们已帮你调通了 2024 年夏季比赛的代码，可以边运行边学习他人的代码。

---

# 视频通话也不能相信了！ DEEP-LIVE-CAM 一夜爆火，伪造直播只要一张照片！

![L50](https://images.jieyu.ai/images/2024/08/deep-live-cam.png)

让马斯克为你带货！

AI 换脸已不是什么大新闻，视频换脸也早就被实现，最早出现的就是 Deep Fake。但是，如果说直播和视频通话也能被实时换脸呢？

发布数月之久的 Deep Live Cam 最近一夜爆火，很多人注意到它伪造直播只要一张照片。

最近，博主 MatthewBerman 进行了一次测试。 他正戴着眼镜在镜头前直播，当给模型一张马斯克的照片之后，直播流立马换脸成了马斯克！就连眼镜也几乎很好地还原了！

他还测试了暗光条件和点光源的条件——常规情况下较难处理的场景，但是 Deep-Live-Cam 的表现都非常丝滑，暗光条件下的甚至更像马斯克了！

这个项目已在 Github 上开源，目前星标接近 8k。对硬件要求不高，只用 CPU 也可以运行。

---

**快快提醒家里的老人**，如果接到孩子的电话，特别是要钱的，一定要先问密码验证问题。如果老人记不住密码验证问题，也可以教老人使用先挂断，再主动拨回去的方法。

这个版本支持 Windows 和 MacOS。需要使用 Python 3.10， git，visual studio 2022 运行时（Windows）或者 onnxruntimes-silicon（MacOS Arm）和 ffmpeg。第一次运行会下载一些模型，大约 300M。

---

# 介绍一个量化库之 TSFRESH

TsFresh 是一个 Python 库，用于识别时间序列数据中的模式。tsfresh 这个词来自于 Time Series Feature extraction based on scalable hypothesis tests"。

![50%](https://images.jieyu.ai/images/2024/08/tsfresh.png)

为什么要使用 tsfresh 呢？

实际上，tsfresh 并不专门为量化设计的。但由于 k 线数据具有时间序列特征，因此可以利用 tsfresh 进行一部分特征提取。在量化场景下使用 tsfresh，主要收益有：

1. 在机器学习场景下，可能需要大量的 feature。如果这些 featrue 都通过手工来构造，不光时间成本很高，正确性也难以保证。从其文档来看，tsfresh 在算法和代码质量上应该是很优秀的。它的算法有专门的白皮书进行描述，代码也有单元测试来覆盖。所以，即使一个算法自己能实现，我也愿意依赖 tsfresh（当然要多读文档和源码）。毕竟，在 feature 阶段出了错，策略一定失败并且无处查起。
2. 如果要提取时间序列的多个特征，手工提取就很难避免串行化执行，从而导致速度很慢。而 tsfresh 已经实现了并行化。

---

当然，我们也要认识到，尽管很多 awesome-quant list 列入了 tsfresh，但 tsfresh 并不是特别适合量化场景，因为金融时间序列充满了噪声。数据不是没有规律，而是这些规律隐藏在大量的随机信号中，而很多时间序列特征库，都是基于时间序列是有比较强的规律这一事实设计出来的。

所以，tsfresh 中许多 feature，实际上并没有 ta-lib 中的特征来得有效。

但如果你要运用机器学习方法，并且有大量标注数据的话（这实际上是比较有难度、很花钱的一件事），那么可以参考下面的示例，快速上手 tsfresh 加机器学习。

在 [Medium](https://medium.com/@francode77/using-tsfresh-to-predict-the-price-of-a-crypto-asset-9227438884db) 上有一篇文章，介绍了如何使用 tsfresh 提取特征，并使用 ARDRegression （sklearn 中的一种线性回归）来预测加密货币价格。文章附有 [代码](https://github.com/Francode77/TSFRESH_price_prediction)，正在探索加密货币的读者可以尝试一下。

如果你愿意看视频的话，Nils Braun在 PyCon 2017 上以tsfresh进行股票预测为例做了一次 [presentation](https://www.youtube.com/watch?v=Fm8zcOMJ-9E)，也很有趣，注意看到最后的Q&A session。

![50%](https://images.jieyu.ai/images/2024/08/tsfresh-on-pycon-2017.jpg)

<about/>
