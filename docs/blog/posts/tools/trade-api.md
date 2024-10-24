---
title: 量化实盘接口
slug: trader-api
date: 2024-10-22
category: tools
motto: Storms make people stronger and never last forever
img: 
lunar:
tags: 
    - 实盘
    - quantlib
---

## Easytrader
Easytrader是一个通过模拟键鼠事件，操作券商客户端来实现交易功能的交易代理。这种方式中，easytrader提供了buy, sell等交易API，策略调用这些API，easytrader把它转化成对券商交易客户端的鼠标点击事件，最终完成交易。
特点是接入不需要申请，支持的券商较多（除华泰、海通、国金外，其它的可以通过同花顺来接入）。但由于是模拟键鼠事件来操作GUI，所以存在稳定性较差、响应速度慢的问题。
如果一定要通过它来进行实盘，需要找一台性能较好的独立的物理机，只安装券商的交易客户端和Easytrader, Easytrader以服务器模式运行，再在策略端，使用easytrader的remote client连接过去，平时不操作这台物理机，以名对easytrader的操作造成干扰。
此外，还应该关闭该机器上的自动更新等功能。
## 恒生电子Ptrade
Ptrade是恒生电子开发的量化平台。官方有一个视频教程，免费注册后可收看。在我的《大富翁量化编程实战》课程中也有介绍。
它的运行方式是券商托管式。券商采购Ptrade软件，进行一些定制化后，提供给自己的客户使用。
用户使用Ptrade策略编辑器生成自己的策略，回测通过后，上传到券商机房运行。这种接入方式中，券商提供python版本的sdk，通过sdk中的交易API来进行下单。
托管模式下，一般不能访问互联网、无法更新Python及依赖库的版本，不能自行安装软件。量化策略与交易API、数据获取API等紧密耦合，如果后期想更换券商，成本较高。因为不能自行安装软件和库，因此难以利用较新的第三方算法。如果使用了机器学习、强化学习等人工智能算法，这些库不一定在券商提供的环境下有，即使有的话，版本很可能跟我们常用的不一致，并且可能没有GPU可用。
优点是行情速度更快，省去了机房维护工作。
Ptrade软件网上无法下载，需要找券商工作人员开户后获取，并且一般要满足30万资金门槛才能开通实盘。目前可以向国金、国盛、国元、安信、东莞等券商申请开通Ptrade。如果有调佣（可以做到万一免五）和资金门槛要求（可以做到最低两万）的，也可以找我。
## QMT
讯投QMT由北京睿智融科开发。与Ptrade一样，它也是由券商采购定制后，提供给自己的客户使用的。不一样的是，它是本地运行模式，策略安全性更好一点。
QMT提供了两种交易接入方式，一种是文件扫单模式，一种是API式。后者需要在QMT平台里编写策略并运行，对Python版本和可运行库有一定限制（但可以通过白名单增加新的第三方库）。
文件扫单模式则没有上述限制。
QMT软件网上无法下载，需要找券商工作人员开户后获取，目前可以向国金、国盛、国元、安信、东莞等券商申请开通。如果有调佣（可以做到万一免五）和资金门槛要求（可以做到最低两万）的，也可以找我。
## 东财EMC
东方财富EMC，开户门槛为100万资金。需要加入它的官方量化技术支持群申请开通。它提供API交易和本地文件扫单两种方式。
本地文件扫单方式响应速度在10ms以内。与量化程序没有耦合，因此量化程序可以运行在任何一台机器上，可以使用任意的Python版本和第三方库。
但是用户需要自己将交易指令（比如buy, sell等）转换成为文件单格式，并且EMC对委托的结果也是以csv方式返回，也需要用户自己解析。
gmadaptor提供了这种封装。不仅如此，它还将自己封装成一个服务器，因此量化策略可以运行在不同的机器和操作系统上（EMC只能运行在Windows上）。
## 其它接入方式
其它还有华泰MATIC，需要找华泰证券开通，这个资金门槛比较高，需要1000万，我可以帮忙申请到500万门槛的。
一创聚宽也提供了量化交易接入，采用的是托管模式。
## 参考资源
如果有需要学习Easytrader, Ptrade, QMT和东财EMC的，我这里有相关的学习资料，可以留言获取。
