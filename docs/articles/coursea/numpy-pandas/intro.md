---
hide:
    - title
title: 课程简介
slug: numpy-pandas-in-quant-trade
category: 课程
tags: 
    - 课程
    - 因子投资
    - 机器学习
---

正如死亡和税收不可避免，Numpy和Pandas对量化人而言，也具有同样的地位 -- 每个量化人都不可避免地要与这两个库打交道。

如果你去研究一些非常重要的量化库，比如alphalens, empyrical, backtrader, tushare, akshare, jqdatasdk等，或者一些非常优秀的量化框架比如quantaxis, zillionare, vnpy等等，你就会发现它们都依赖于numpy和pandas。实际上，一个库只要依赖于pandas，它也必将传递依赖到numpy。

具体地说，Numpy和Pandas不仅为量化人提供了类似于表格的数据结构 -- Numpy Structured Array和Pandas DataFrame -- 这对于包括行情数据在内的诸多数据的中间存储是必不可少的；它还提供了许多基础算法，比如：

- 在配对交易(pair trade)中，相关性计算是非常重要的一环。无论是Numpy还是Pandas都提供了相关性计算函数。
- 在Alpha 101因子计算中，排序操作是一个基础函数 -- 这是分层回测的基础 -- Pandas通过rank方法来提供这一功能。
- Maxdrawdown(最大回测)是衡量策略的重要指标。Numpy通过numpy.maximum.accumulate提供了支持。

类似常用的算法非常多，我们将在本课程中一一介绍它们。

## 课程定价

为了惠及更多读者，我们采取了分级定价策略：

=== "Plan A"
    !!! tip "免费"
        您可以通过在[匡醍量化](https://blog.quantide.cn/articles/python/numpy%26pandas/01-introduction/)这里免费阅读课程文本。
=== "Plan B"
    !!! tip "仅99元!"
        我们提供了可在线运行的 notebook。它与 Plan A的内容几乎一样，但是每一段代码都可以运行（如果你熟悉 notebook，就能理解）。你可以修改它，运行它，而不用对着我们的课程文本复制、粘贴以及担心依赖库和数据从哪儿来。

        您可以在[小红书](https://www.xiaohongshu.com/goods-detail/67f4d677ab6a3e0001e5bb84?t=1762062506298&xsec_token=ABstLThUDfUaYjgAOEyrahdZ7G6MeNK3ln85SXgObCR88%3D&xsec_source=pc_arkselfshare)上购买。

## 课程编排说明

紧扣量化场景来介绍Numpy和Pandas是本课的一大特点。我们通过分析重要的、流行度较高的量化库源码，找出其中使用numpy和pandas的地方，再进行归类的提炼，并结合一些量化社区中常问的相关问题 -- 这些往往是量化人在使用numpy/pandas时遇到的困难所在 -- 来进行课程编排，确保既能系统地讲解这两个重要的库，又保证学员在学习后，能立即将学习到的方法与技巧运用到工作中，迅速提高自己的生产力。

全部课程共分11个章节。

无论是演示代码、还是练习，我们都尽可能安排在量化场景下完成，这样会增强您的代入感。但是，这往往也要求您能理解这些场景和数据。

在编写本课程时，作者阅读了大量书籍、博文、论文和开源项目代码。其中一部分与教材关联度较高的，我们以延伸阅读、脚注的方式提供参考链接。如果学员有时间，也可以阅读这部分内容，以获得跟作者同样的视野景深。但如果你时间紧张，也完全可以跳过这些内容，只关注我们课程内容的主线就好。

本课程是专门为量化交易从业者，比如quant developer, quant researcher和quant pm等人设计。如果您有基础的金融知识，这门课也适用于其它需要学习Numpy和Pandas的人。课程内容在丰度和深度上都是市面上少见的。


