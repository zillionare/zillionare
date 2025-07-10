---
title: "高频变高危：监管新规下的市场变局"
description: "深入解析高频交易的技术原理与监管挑战。从每秒300笔申报的新规定义出发，探讨套利、做市、延迟套利等30多种高频策略，揭示报价填充、spoofing等争议操作的市场影响。分析减速带等技术创新如何抑制过度投机，展望量化交易从拼速度向拼策略的转型趋势"
date: 2025-07-10
audio: https://cdn.jsdelivr.net/gh/zillionare/podcast@main/2025/07/14-final.mp3
---

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


<div class="bg-light"><p>Flora：量化好声音 每晚都要听。大家好，我是Flora，欢迎回来。</p></div>
<div class="bg-dark"><p>Aaron：大家好，我是Aaron，欢迎收听我们这一期播客</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 今天咱们要聊一聊高频交易的那些事，包括它的定义，它的策略，它一些比较有争议的地方</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 好，不过我先歪个楼，因为今天有一个非常大的事儿，得跟大家播报一下。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 跟马斯克有关吧</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 对，就是Grok 4的发布。发布到现在不到4小时。据说这个模型在HLE的考试中，得到到了45%的高分。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: HLE这个词展开来讲，其实挺唬人的，它是Humanities Last Exam，人类最后的考试。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 没错。人类最后的考试。在这场考试中，Grok 4领先，之前最强的是Gemini Pro，这次领先了接近一倍的分数。马斯克今天还在凡尔赛，后面就没有题可以训练了，因为这个Grok，已经超过多数博士生水平了。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 真是人类最后的考试没错了。不过，马斯克也常常跳票。Grok 4是否真的这么强，我们让子弹先飞一会儿。我们先回到今天的主题。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 我们先从高频交易的定义开始。这次交易新规，也是明确地给出了定义。</p></div>
<div class="bg-light"><p>Flora：根据新规，每秒300笔上以的申报，或者单账户、单日申报达到2万笔就属于高频交易啦。那我们先从一个比较hot的问题开始，为什么高频交易需要被特别监管呢？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 其实高频交易一直是市场中不安分的那个坏孩子。这些年来，在全球市场上，频频被罚。机构利用速度和资金优势，操纵市场，放大了市场波动，损害他人特别是散户的利益，也确实应该被监管。最近的事儿就是大家都知道了，简街，在印度市场上，因为操纵市场被罚了。</p></div>
<div class="bg-light"><p><strong>Flora</strong>: Aaron，那高频交易到底能快到什么速度？</p></div>
<div class="bg-dark"><p>Aaron：高频交易速度的演进真的很惊人。在21世纪初，高频交易的执行时间还是以秒为单位，但到了2010年，这个时间已经缩短到毫秒甚至微秒级别。现在的高频交易系统追求的是纳秒级的优势。为了达到这么高的速度，很多公司会甚至把服务器直接放在交易所旁边，这叫做"co-location"。</p></div>
<div class="bg-light"><p>Flora：所以这真是军备竞赛啊。那对散户来讲，是不是很不公平？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 对，正是这样，不光是对散户，对市场上其它资金，比如像养老基金，也很不公平。另外，过度投机很容易放大市场波动，造成踩踏事故，所以，加强监管真的是必须的。</p></div>
<div class="bg-light"><p>Flora：所以，高频交易究竟是谁在做，有哪些策略呢？这个Aaron能不能帮我们梳理一下？</p></div>
<div class="bg-dark"><p>Aaron：做高频交易的公司吧，一般来说可以可以分为三类吧。一类是套利者，然后是自营交易商，还有一类是做市商。他们的策略，据不完全统计，大约有30多种。主要是一些套利策略，还有一些是利用市场微观结构来进行的一些策略等等。</p></div>
<div class="bg-light"><p>Flora：高频交易里面的这些套利的策略到底是怎么操作的，然后他们会面临一些什么样的监管的问题呢？</p></div>
<div class="bg-dark"><p>Aaron：套利其实是高频交易里面最基础的一个策略。它其实就是利用同一个资产，在不同的市场或者说不同的时间，它的价格是不一样的，然后你通过这种价格差来获利。比如说某一个资产，它可能在纽交所的交易价格是150美元，同时它在另一个交易所的价格是150.01美元，这个时候你就可以通过非常快速的操作，在低价的地方买入，在高价的地方卖出，就赚取这0.01美元的差价。这个东西看起来很少，但是如果你有非常大的交易量的话，这个收益也是很可观的。</p></div>
<div class="bg-light"><p>Flora：哇 这个真的是要快。看起来也只是一些很朴素的算法，不是那么高大上哈。</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 没错</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 然后这个完全是靠速度和规则来玩的。还有一些套利的策略，比如说统计套利，它可能就要用到一些数学模型，来预测。比如说有两只资产，它的价格走势本来是很相关的，但是突然之间，它们两个之间出现了一个偏离，这个时候你可能就会买入，被低估的那一只，同时卖出被高估的那一只，等到它们的价格回归之后再进行平仓。</p></div>
<div class="bg-dark"><p>这些策略的话其实频率不一定很高，但是它可能在短期内会有大量的交易，所以同样它也会触及到监管的红线</p></div>
<div class="bg-light"><p><strong>Flora</strong>: 那高频交易里面的这种利用时间差，来获利的这种策略到底是怎么操作的？</p></div>
<div class="bg-dark"><p><strong>Aaron</strong>: 这种策略其实就是利用,信息传播的速度差来获利。比如说有一个养老基金，它要在纽交所买入大量的资产，这个订单信息从纽约传到芝加哥，是需要16毫秒的，高频交易者他们就在纽约提前得知了这个消息，然后他们就会抢先在芝加哥买入这些资产，等养老基金的订单到了之后，他们再以一个更高的价格卖给他们</p></div>
<div class="bg-light"><p>为了能够更快的获得这个信息，有一些公司甚至在纽约和芝加哥之间，铺设了微波的通讯线路，因为微波它的传输速度要比光纤快大概30%左右，所以他们就可以快4毫秒拿到这个信息</p></div>
<div class="bg-dark"><p>Flora：所以这个也是为什么大家会说，它是一种掠夺性的交易，就是你并没有创造任何价值，你只是在利用这种速度和信息差来获利，所以它对于市场的公平性是有损害的</p></div>
<div class="bg-light"><p>Aaron：另外一个跟这个很像的就是做市，做市的话其实是你要提供流动性，然后自己是要通过买卖价差来获利。所以做市商他一般是要承诺持续的提供双边的报价，所以他不会说像这种延迟套利一样，我可以随时就退出市场，所以这是他们一个很本质的区别</p></div>
<div class="bg-dark"><p>Flora：听说高频交易中有一些颇有争议的策略，比如报价填充和spoofing？</p></div>
<div class="bg-light"><p>Aaron：对，报价填充是一种市场操纵形式，就是虚假申报并撤销。当你虚假申报之后，这个价格就开始在网上传播，然后你又快速撤销它，那其它投资者可能刚刚拿到未撤销的报价，做了一个决定，从而就上当受骗了。spoofing则是在此基础上更进一步，加上了反向操作。</p></div>
<div class="bg-dark"><p>Flora：这种做法合法吗？</p></div>
<div class="bg-light"><p>Aaron：在多数市场上都是不合法的。城堡投资在2014年就因为报价填充被罚款过。涛合投资2019年被罚了接近7000万美金。但是有一些市场，特别是加密货币市场是没有监管的，所以，这些高频策略很可能在这些市场上还非常流行。</p></div>
<div class="bg-dark"><p>Flora：看起来高频交易确实很容易走偏啊。那有没有利用高频数据，但又是比较合规的操作呢？</p></div>
<div class="bg-light"><p>Aaron：有许多被动操作，一般认为是合规的。比如，tick trading，订单流等等。拿Tick trading来说，它通常旨在识别市场中大订单的开始。例如，养老基金的大额买单会在几小时甚至几天内执行，由于需求增加会导致价格上涨。套利者可以尝试发现这种情况，买入证券，再卖给养老基金，从中获利。这个过程基本上是被动的，目前来看，算是合规的。</p></div>
<div class="bg-dark"><p>Flora：在限制高频交易方面，除了利用法规方法外，有没有一些技术创新可以解决这些问题？</p></div>
<div class="bg-light"><p>Aaron：这方面也有的。比如IEX就推出了减速带产品，强行给订单增加一个350微秒的延时。这个做法尽管遭到了象城堡投资这样的基金公司，甚至是纳斯达克的反对，但最终还是得到了普遍认可，现在纳斯达克，以及一些著名的现货外汇交易平台，都推出了自己的减速带产品，用来抑制过度投机。</p></div>
<div class="bg-dark"><p>Flora：抑制过度投机，倡导公平交易正是监管的目标，也是这次量化交易新规推出的初衷。所以，你认为量化交易新规推出后，各投资机构在策略上会有哪些转变？</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 在对高频交易有了明确的定义之后，很显然大家在高频交易上面的竞赛会得到降级。之后大家可能应该从拼速度，转向拼策略，转向中低频策略。对于高频数据的利用，也会从直接利用，转向降频使用。</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 这个怎么说？</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 就是从高频数据，比如订单流、level 2数据当中，发现其中的交易模式，进而识别出交易对手和对手意图。比如，如果你能识别养老基金在买入的话，那么可以象之前提到的高频交易一样，选择做它的对手盘，但也可以做它的朋友，一起加仓。现在有了机器学习、强化学习等技术的加持，现在做这个事儿，应该难度是降低了。</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: Aaron, 你在开头提到了有超过30多种高频交易策略。但我们今天只介绍了其中的一小部分。如果想了解其它交易策略，有没有什么参考资料？</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 这方面的参考资料不少。链接太长，就请参考我们的文字稿，或者公众号文章吧</p></div>
<div class="bg-dark"><p><strong>Flora</strong>: 好的，那今天的节目就是这样。量化好声音，每晚都要听。我们下期再见</p></div>
<div class="bg-light"><p><strong>Aaron</strong>: 再见！</p></div>
<div class="bg-dark"><p>https://www.daytrading.com/hft-strategies</p></div>
