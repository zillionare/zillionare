---
title: 常见问题
slug: faq
date: 2024-01-04
category: 课程
tags: 
    - 课程
---

## 报名流程和学习环境

!!! abstract "课程怎么学？"
    课程以视频、notebook和答疑方式提供。视频在荔枝微课上，notebook由我们提供的服务器host。每周提供一次集中答疑，时间是周日晚8点，形式为腾讯会议。<br><br>
    购买后，加宽粉（quantfans_99）账号，开通课件服务器账号，即可开始学习。宽粉还将为您和老师建立课程小群。
    购买请点击[链接](http://weike.fm/EqeEq4d411)

!!! abstract "学这门课需要多久？"
    课程共有24章，约40万字节，视频时长（精剪和1.2倍加速）约30小时。建议2个月学完，但取决于您的背景和能分配的时间。<br><br>
    课程视频会永久免费收看。课件服务器使用期限一般为4个月，如果4个月内没有学完，可向我们提出申请，合理使用。也可以按我们提供的软件，自行部署大富翁量化研究环境，下载课件自行部署。<br><br>课件服务器仅供学习使用，不能用作云服务器。

!!! abstract "哪些人适合学习这门课/前置条件？"
    任何人，只要具有**基本的Python编程知识**，和**大学水平的数学知识**，都可以报名学习这门课。具体情况可以咨询宽粉（quantfans_99），请她帮你评估是否达到了入门条件。<br><br>如果您有一定编程基础，正在学习Python，也可以先报名课程，老师可以提供免费辅导。

!!! abstract "你们提供学习环境吗？"
    我们提供一个由192CPU核、256GB内存构成的服务器集群为学员服务，学员通过浏览器登录后，即可在线学习和运行我们的示例代码。在该环境中，我们有超过30亿条商用数据（2024年起由聚宽赞助），仅这些数据的订阅费就超过2万元。

!!! abstract "你们的学习环境有何优势，自己搭环境可以吗？"
    这个环境最大的优势就是我们提供了回测功能（不是基于bactrader的回测）及商用数据。我们的回测是在分钟线基础上进行撮合的，并且自动实现了T+1限制、涨跌停交易限制，能最大程度真实还原交易现场。这些数据量特别巨大，无法复制。因此，您自己搭建的环境，还需要购买数据，才能真实还原交易现场。**只有基于真实的数据，您进行策略调优才有意义**。

## 职业规划相关问题

!!! tip "你们有哪些学员在学习这门课？"
    据不完全统计（并非每位学员都愿意跟我们分享其背景），有2名以上藤校博士、3名以上基金经理（含私募总）在学习本课程，并有一家私募采购我们的课程供员工/实习生学习。其它学员还有香港投行员工、私募员工、互联网大厂工程师、在校学生等。
    
!!! tip "为什么要学习量化交易？"
    只有学会理财，才能拥有睡后收入。学会量化交易，不再为金钱工作，而是让金钱为你工作！

!!! tip "学完这门课，是不是就能赚钱了？"
    Yes And No. 这门课是一门综合性课程，重点在于解决有策略思路的情况下，如何将其程序化、科学化。学完这门课程，如果您是经验丰富的交易者，那么您将能运用本门课程所讲授的方法，重新梳理自己的交易经验，去伪存真，将其中有效的经验以程序的方式固化下来，从而避免情绪波动、人脑计算能力不足、无法洞悉和分析市场全景的困扰；如果您没有交易经验，您也将掌握科学的量化理论和研究方法，获得打开策略宝库的钥匙。<br><br>总之，学完这门课，无论是跟自己比，还是跟其它交易者比，您都将获得明显的进步。但是，能否赚钱不仅仅跟自己的能力提升有关，还跟市场密切相关。如果市场在下行，并且不能做空，那么赚也难。

!!! tip "你们有认识的猎头可以帮忙推荐工作吗？"
    当然有！我们的账号[量化风云](https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c)是小红书上量化赛道第一名，猎头公司都会主动与我们合作。

## 量化框架相关问题

!!! tip "你们的课程有backtrader的详细介绍，为什么还要介绍大富翁量化的回测功能？"
    backtrader有以下几个重要不足：
    1. 它无法对接A股的实盘交易。您必须自己开发适合国内的行情接收和实盘接口才能将策略转入实盘。
   
    2. backtrader不能提供动态前复权。但这是惟一正确的复权机制。

    3. backtrader理论上可以基于1分钟线进行撮合，但考虑到数据拷贝问题，实际上无法实现。基于日线进行撮合会导致虚假成交。比如当天标的最低价下探到10.2元，如果你在10.3元处进行委买1万手，backtrader就会让你成交。但有可能在10.3及以下，当天就只成交了一手，因此回测时，最大成交量也应该就是1手，但backtrader会以全天成交量为限，让其成交。基于分钟线进行拟合，就可以基本避免这种虚假成交。

    4. backtrader不知道A股的交易制度，因此它不限制T+1卖出和涨跌停交易。这会导致回测与实盘策略表现差异太大。

!!! tip "大富翁量化框架有何优势？"
    1. 优秀的回测和策略系统。策略转实盘无须进行代码修改，替换回测服务器地址为实盘服务器地址即可。免于修改就会减少错误。此外，动态前复权、基于分钟数据的撮合都是领先优势。

    2. 海量数据处理能力。我们是国内率先使用时序数据库保存行情数据的开发者。

    3. 优秀的代码质量和文档质量。文档质量确实很重要。

    4. 提供了许多算法和量化交易常用函数。比如我们的日历运算库、绘图库、形态识别等都是独家功能。

!!! tip "学完后我能用你们的大富翁量化软件吗？"
    可以，这正是我们的优势之一。学完课程后，就可以使用我们的量化软件在本地部署，立即开始交易。<br><br>
    大富翁量化软件2.0是开源软件，但我们只对学员提供安装包和指导。部署2.0需要购买聚宽数据。

!!! tip "大富翁量化软件未来规划？"
    我们正在开发2.1版本，预计今年6月前交付。这一版本将使用clickhouse作为数据库，以便能支持tick级数据存储并仍然保持很好的性能。在实盘接口和行情方面，我们将接入QMT。

## 其它问题

!!! tip "我有一块GPU，在量化中能用上吗？"
    如果直接从价格数据入手的话，这样端到端的AI技术现在还没有成熟，也有可能永远不会成熟。价格数据包含了相当大的噪声，或者说，它是一个多对多的映射，因此无法从中进行有效地学习。<br><br>
    目前最成熟的量化策略与AI结合的方案是人工提取因子，通过机器学习，特别是XGBoost这类算法来进行因子组合。XGBoost无法利用GPU。如果使用lightGBM,能在部分阶段中利用CPU。NLP在量人交易中的作用是显而易见的，但是大模型需要的运行环境是多数人无法承受的。

!!! tip "我该如何申请量化交易权限？有哪些门槛？"
    一般新开户可以同时申请量化交易权限。可以跟宽粉（quantfans_99）咨询，帮您找到门槛最低、资费最优的券商。

!!! tip "可以介绍下老师吗?"
    <div style="width:150px; position: relative;float:right">
        <img src="https://images.jieyu.ai/images/hot/me.png" style="width: 120px; display:inline-block"/>
        <p style="text-align:center;width:120px"> Aaron </p>
    </div>

    -   IBM/Oracle高级软件研发经理

    -   海豚浏览器（红杉资本投资）副总裁

    -   格物致知（量化投资）联创

    -   Zillionare开源量化框架发起人

    -   《Python高效编程实践指南》作者（机械工业出版社出版）。

