---
title: "简街印度风波：量化巨头为何从算法竞争转向规则套利？"
description: "全球顶级量化交易公司简街因在印度市场操纵指数被罚，引发行业震动。本期节目深入剖析简街如何利用Pump and Dump与Marking the Close手法操纵市场，探讨为何拥有顶尖人才的技术公司会选择钻规则空子而非突破算法。我们揭示了量化交易正从技术竞争转向规则竞争的行业趋势，以及IEX与城堡投资在规则制定权上的博弈。这一切背后，是否隐藏着量化交易Alpha衰减的残酷现实？"
date: 2024-07-07
audio: https://cdn.jsdelivr.net/gh/zillionare/podcast@main/2024/07/11-final.mp3

<style>
.bg-light {
    background-color: #fcfefe;
    padding: 10px 15px;
    margin-bottom: 5px;
    border-radius: 5px;
}
.bg-dark {
    background-color: #f8f9fa;
    padding: 10px 15px;
    margin-bottom: 5px;
    border-radius: 5px;
}
</style>

<div class="bg-light"><p># 房间里的大象：Alpha衰减下的量化巨头困局</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 量化好声音，睡前听一听。我是Flora。</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 我是Aaron。今天我们要聊一个非常有意思的话题——简街这家量化交易巨头最近在印度市场被指控操纵指数的事件。</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 对，这个事件真的很有意思。Aaron，你看过那份关于简街的报告吗？他们被指控在印度市场进行「日内指数操纵」和「延长版尾盘操纵」。</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 看过了，说实话挺震惊的。简街作为全球最大的做市商之一，2020年证券交易额超过17万亿美元，居然会用这种看起来很「原始」的手法来赚钱。</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 这就是我想说的重点！Aaron，你不觉得很奇怪吗？简街可是以技术见长的公司，他们雇佣的都是顶尖人才。为什么不去突破算法，而是去钻规则的空子？</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 这个问题很尖锐。对于简街，大家可能已经了解到他们公司的面试题，还有就是在他们官网上的puzzles，确实每一期的谜题都出得很有意思，我自己也常常看。感觉很高大上。关于简街的技术路线，Flora，需要我介绍一下吗？</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 对，如果有同学打算去简街，或者去一家简街出来的人开的量化投资公司，那么了解它们的tech stack会是一个好主意。所以，Aaron你能不能跟大家介绍一下。</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 好的。简街主要以高频交易为主。为了构建他们的高频交易系统，他们使用了一种比较小众的编程语言，叫做OCaml。他们95%以上的系统代码，都是通过这种语言来开发的。简街还向Ocaml社区贡献了core, async等好几个重要的库。</p></div>
<div class="bg-dark"><p>Ocaml是一种函数式、指令式、模块化和面向对象的通用编程语言。现在主要由法国国家信息与自动化研究所维护。这种语言在自动定理证明、静态分析和形式方法软件中都超有存在感。它是一种看上去像动态类型语言，写起来像写数学公式，但运行起来却有静态语言一样的安全性和高性能。</p></div>
<div class="bg-light"><p>**Flora**： 听起来确实很酷，也很适应于量化交易行业，因为我们要处理大量的数学计算。所以被简街这样的高频量化投资公司选中也不奇怪。都在说简街这次被罚是因为不合规的操作，那他们具体是怎么做的呢？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 根据报道，简街主要有两个策略，一个是通过Pump and Dump手法操纵日内指数; 另一个是Marking the Close，是在期权到期日收盘前进行大量交易，人为推高或压低指数价格。所有这些操作，都是通过现货与期货的联动来完成获利的。</p></div>
<div class="bg-light"><p>根据印度管理当局的一个认定，他们的Pump and Dump手法是这样的操作的：上午，他们在现货与期货市场上，大量且激进地买入BANKNIFTY指数的成分股，拉高股价。</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 我跟大家解释一下，BANKNIFTY指数是印度银行业的一个指数。相当于A股的中证银行指数。</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 对，他们通过这种拉抬，就会使得对应股票价格虚高，于是，此时他们就会在流动性极高的指数期权市场上，建立巨大的看跌头寸，完成布局。然后就在当天剩下的时间里，对成份股价格进行打压，这样尽管他们会在现货和期货市场上有比较严重的亏损，但在指数期权上会获得巨大的利润。</p></div>
<div class="bg-dark"><p>这只是其中的一个策略。另一个被称为Marking the close的策略，就是我们俗称的拉尾盘，不过，这个策略只是在期权交割日当天尾盘才实施。当采取这个策略时，他们可能在全天多数时间不怎么交易，但会在最后30分钟，在指数成份股和期货市场上，发动了大规模、集中的卖出攻击，这样就可以从早就持有的看跌期权中获利。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 有的朋友可能会疑惑，这样的操作为什么会被算是是违规？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 印度管理当局认为简街的操作违规，并不是因为他们高频交易，主要是因为他们操纵市场。量化机构可以进行高频交易，但是不能利用自己的资金和交易速度优势，去人为地放大市场波动。就是你可以利用速度优势来对冲和避险，但不能制造出波动。我想这才是核心。类似的案例在A股的2023年底也发生过。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 对，当时是小盘股上的DMA策略，也就是所谓的多空收益互换，听起来跟 简街这次被罚的手法很像。那次一些明星私募公司受到了监管处罚。我记得，更早一点，2015年也有一起类似的案子，犯事的是伊士顿，他们利用「不正当的交易优势和额外交易速度优势」，大量操纵中金所股指期货交易。所以，太阳底下没有新鲜事，这些钻空子的玩法，看起来一直打不绝、禁不完。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 不过A股正在加大监管力度。今天是7月7号，从今天起，国内也出了一个量化交易新规，开始实施了。就是对每秒申报/撤单≥300笔，或单日≥2万笔的高频交易进行监管。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 这个新规颁布得非常及时。希望新规对防止像简街这样操纵市场的行为起到防范和震慑作用。那回到我最初的问题，简街雇佣了全球顶尖的人才，为什么不去突破算法，而是选择去钻规则的空子，甚至是去做违规操作？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 我觉得可能有几个原因。首先，算法的突破需要长期的投入，而规则套利是立竿见影的。其次，可能是因为纯算法的alpha已经越来越难获得了，并且Alpha的持续性变短了。量化交易已经从「技术竞赛」变成了「规则竞赛」。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 某种程度上是的。简街有强大的人才优势，但他们选择去研究监管规则，而不是去开发更先进的算法。这可能反映了整个行业的一个趋势。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 但这样做的风险也很大。你看简街在印度被罚了，伊世顿的人都被判刑了。这种「聪明钱」的做法真的值得吗？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 这就是风险收益的权衡了。对于简街来说，即使在印度被罚，他们在全球其他市场的收益可能早就覆盖了这些损失。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 这让我想到一个更深层的问题 —— 这种行为对市场公平性的影响。如果大家都去钻规则的空子，而不是提高市场效率，那金融市场的意义又何在？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 你说得对。这也是为什么监管机构要严厉打击这种行为。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 所以我们看到的可能是一个博弈过程。技术公司在寻找规则漏洞，监管机构在不断完善规则。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 对，而且这个博弈可能永远不会结束。简街们会继续寻找新的套利机会，监管机构会继续堵漏洞， 就像打地鼠一样。说到规则博弈，我想到最近还有一个很有意思的案例——城堡投资，也就是城堡投资和IEX的争议。IEX是投资者交易所，这是一家比较新的公司。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 哦？这又是什么情况？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: IEX想要推出期权交易所，但城堡强烈反对，称IEX的提案是「自私自利的」，对市场有害。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 具体争议在哪里？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 核心争议是IEX计划引入一个「速度缓冲」机制，对每一笔订单设置一个350微秒的延迟，以消除高频交易者的速度优势，同时允许算法在这个延迟期间取消或重新定价报价。城堡投资认为这会让做市商发布他们不打算兑现的报价。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 所以，国外已经从利用规则发展到争夺制定规则的话语权的阶段了。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 没错！这个案例完美地说明了我们今天讨论的主题。IEX声称这是为了减少延迟套利，保护投资者；但城堡投资认为这实际上会创造「虚幻的报价」，误导市场参与者。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 有意思的是，这次是两个技术公司在争夺规则制定权，而不是简单地利用现有规则。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 对！这说明规则套利已经进化了。现在不仅仅是利用现有规则的漏洞，还要试图影响规则的制定过程。谁能影响规则，谁就能获得竞争优势。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 这让我想到一个问题——在这种环境下，技术创新的意义是什么？是为了更好地服务市场，还是为了获得监管优势？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 这就是问题的核心。IEX说他们的机制是为了「促进更多人参与做市竞争」，但城堡投资认为这会「剥夺投资者保护」。双方都声称是为了投资者利益，但实际上可能都是为了自己的商业利益。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 这个案例和简街的印度事件有什么共同点？</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 共同点是都体现了量化交易公司从纯技术竞争转向规则竞争的趋势。简街在印度利用现有规则漏洞，IEX试图创造新的规则优势，城堡投资则试图阻止对手获得规则优势。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 所以我们看到的是一个三层博弈：利用现有规则、影响新规则制定、阻止对手获得规则优势。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 完全正确！这也解释了为什么这些公司要雇佣大量的合规和政府关系人员，而不仅仅是技术人员。在某种程度上，律师和说客变得和程序员一样重要。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 但这种乱象，也可能有另外一种解释，就是量化投资的房间太小，但却闯进来一头大象，大象在小房间里无法生存，它就总想闹出点事儿来。最终，要解决这个问题，还得把大象请出房间。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 也就是，如果你的资金体量太大，就应该去做价值投资，去帮助行业和社会的发展与进步。量化本质上是一种投机，有实力、有资金的机构不应该把投机当成一种事业。这片天地，应该让给中小投资者。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 好的，今天的量化好声音就到这里。感谢大家的收听，我们下期再见！</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 再见！</p></div>
