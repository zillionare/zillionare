---
title: 玩转XtQuant量化交易
slug: quant-trade-with-qmt
---

QMT是迅投公司推出的量化交易软件，它是券端采购软件，因此具有量化实盘接口。当前定制采购了QMT的券商约50家左右，开通量化权限的门槛从数万元到数十万元不等，开通量化权限除仍然能享受到万一（甚至免五）的费率优惠外，还将免费获得历史和实时交易行情数据，是目前性价比较高的一种实盘接入方案。

## 课程选题
作为量化软件，QMT提供了两种使用方式。一种是内置量化交易平台。通过内置Python环境，实现策略开发、回测和实盘交易。另一种方式是使用QMT提供的XtQuant库，通过第三方量化框架驱动，来实现策略开发、回测和实盘交易。

通过XtQuant+第三方量化框架实现量化交易，有许多突出的优点：

---

1. 更好的策略开发编辑工具。使用第三方量化框架，您将可以使用Vs Code或者PyCharm来进行策略开发与调试，这两种开发工具的效率远超QMT内置的编程界面。
2. 更快的回测速度。多名用户反馈，在QMT内部进行回测，速度还是比较慢的。
3. 不受限制地回测时间。部分券商提供的QMT在周末会进行维护，此时无法进行策略开发与回测。此外，一些券商提供的QMT，模拟盘交易时间又必须是在盘后才能进行。
4. 避免锁定效应。使用QMT内置的量化功能，不可避免地产生锁定效应，这将包括：
   1. 技术锁定。内置QMT不能任意安装Python库。这将导致您无法使用先进的技术，在量化竞赛中，输在起跑线上。
   2. 数据锁定。使用内置QMT时，遇到QMT未提供的数据，但第三方数据源可提供，此时能否获取，如何获取，目前还未看到文档和示例。量化人都有自己的因子库，如何在内置环境下，提取、储存和读取因子库，这也是官方文档未提及的一个方面。
   3. 迁移锁定。一旦大量软件资产锁定在QMT内置平台上，未来迁移的成本将很高。触发量化平台的事件很多，比如，其它券商提供了更优惠的费率；或者您需要在多个券商处开多个户头；或者某个必须的数据只在其它平台上提供等等。此外还有一些外在因素，比如2023年就发生了聚宽和一创终止合作，从而导致用户不得不把策略往QMT上迁移的情况。

基于以上原因，本课程将主要讲授如何实现第三方量化框架下，集成XtQuant以实现量化交易。

---

主要内容有：

1. 开通和安装QMT及XtQuant
2. XtQuant的数据功能
3. XtQuant的交易接口
4. 将XtQuant封装成服务
5. 与大富翁量化框架集成

!!! info 大富翁量化框架
    大富翁框架2.1版本将集成XtData的数据和交易接口，成为支持QMT量化交易的完整三方平台。数据存储基于Click House构建，可在容纳少量数据的同时，提供极低的查询响应时间。




