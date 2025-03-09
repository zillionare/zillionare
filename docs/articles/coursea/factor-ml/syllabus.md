---
slug: factor-machine-learning-syllabus
---

<style>

.cols {
    column-count: 2;
    column-gap: 2em;
}

h1 {
    font-weight: 400 !important;
}

h2 {
    margin-top: 2em;
}

h3 {
    color: #303030 !important;
    font-weight: 200 !important;
    font-size: 1.2em;
}

h4 {
    color: #808080 !important;
    font-weight: 100 !important;
    font-size: 1em;
    margin-left: 1em;
}

h5 {
    display: none;
}

.module {
    text-align: center;
    font-size: 2em;
    margin: 2em 0;
}

more {
    font-size: 0.75em;
    color: #808080;
    /* border: 1px solid #ccc; */
    margin: 2.5em 0 -1em 0;
    position: relative;
    cursor: pointer;
    /* min-height: 2em; */
    display: inline-block;
}

more::before {
    content: '课程要点 >';
    position: absolute;
    /* top: 50%; */
    /* left: 100%; */
    transform: translate(0, -50%);
    width: 5em;
    height: 3em;
    /* background-color: #ccc; */
    transition: transform 0.3s ease;
}

more.expanded::before {
    content: '';
}

more > p {
    display: none;
    transition: height 0.5s ease; /* 平滑过渡效果 */
}

more.expanded > p {
    display: block;
}

hr {
    height: 1px !important;
    color: #ddd !important;
    border: none;
    background-image: linear-gradient(to right, 
                    rgba(0, 0, 0, 0.2), 
                    rgba(0,0,0,0));
    background-repeat: no-repeat;
    width: 80%;
}

@media only screen and (max-width: 1024px) {
  .md-sidebar-toc {
    display:none;
    width: 0;
  }
  
  .cols {
      column-count: 1;
    }
    
  .markdown-preview {
      left: 0px !important;
      width: 100% !important;
  }
}

</style>
<script>
var sidebarTOCBtn = document.getElementById('sidebar-toc-btn');
document.body.setAttribute('html-show-sidebar-toc', true);

document.addEventListener('DOMContentLoaded', function() {
    const moreElements = document.querySelectorAll('more');

    moreElements.forEach(element => {
        element.addEventListener('click', function() {
            element.classList.toggle('expanded');
        });
    });
});
</script>

<p>§ 因子投资与机器学习策略</p>
<h1 style="text-align:center">课程大纲 </h1>
<div class="cols">

<a href="#declaration">大纲说明</a>

## 1. 导论

### 1.1. 因子投资的起源
### 1.2. 寻找 Alpha
### 1.3. 从 CAPM 拓展到多因子
### 1.4. 从因子分析到因子投资
### 1.5. 从因子模型到交易策略
### 1.6. 关于课程编排

<more>

这门课面向的对象是专业的量化研究员、或者打算向这个方向转岗求职、或者尽管是其它职业，但决心以专业、严谨的态度探索量化研究的学习者。

学完这门课程并完全掌握其内容，你将具有熟练的因子分析能力、掌握领先的机器学习策略构建方法，成为有创新研究能力和比较竞争优势的量化研究员。

课程内容涵盖了因子挖掘、因子检验到构建机器学习模型的过程。如果要独立从事交易，还需要补充学习《量化 24 课》。

</more>

---

## 2. 因子预处理流程
### 2.1. 因子数据的来源
### 2.2. 因子生成
### 2.3. 因子预处理
#### 2.3.1. 异常值处理
#### 2.3.2. 缺失值处理
#### 2.3.3. 分布调整
#### 2.3.4. 标准化
#### 2.3.5. 中性化

<more>

这一章及下一章是因子检验的基础。我们将结合大量的示例代码，介绍因子检验的基本原理与技术实现细节，为后面理解Alphalens因子分析框架打下坚实基础。

</more>

---

## 3. 因子检验方法
### 3.1. 回归法
### 3.2. IC 分析法
### 3.3. 分层回溯法
### 3.4. 因子检验的代码实现
#### 3.4.1. 生成因子：进一步模块化
#### 3.4.2. 因子预处理：接入真实的数据
#### 3.4.3. 计算远期收益
#### 3.4.4. 回归分析的实现
#### 3.4.5. IC 分析法实现
#### 3.4.6. 分层回溯法实现
### 3.5. 三种方法的区别与联系

<more>

本章介绍了回归法、IC法和分层回溯法的原理及实现代码。这一章完成后，你已经可以自己实现一个简单的因子分析框架了。这对理解Alphalens的实现非常有帮助。

</more>

---

## 4. 初识 Alphalens
### 4.1. 斜率因子：定义和实现
### 4.2. 如何为 Alphalens 计算因子和收集价格数据
### 4.3. Alphalens 如何实现数据预处理
### 4.4. 因子分析与报表生成
### 4.5. 参考文献

<more>

Alphalens将因子检验过程进行了高度的抽象，把我们在前面两章讲到的步骤封装成两个函数，而大量的定制则是通过参数来实现。我们将介绍Alphalens要求的输入数据格式、它是如何通过参数来控制分层、缺失值处理、远期回报计算等行为的。

通过这一章的学习，你将掌握Alphalens最基本的用法。

</more>

---

## 5. Alphalens 报表分析
### 5.1. 收益分析
#### 5.1.1. Alpha 和 Beta
#### 5.1.2. 分层收益均值图
#### 5.1.3. 分层收益 Violin 图
#### 5.1.4. 因子加权多空组合累计收益图
#### 5.1.5. 收益的分层驱动
#### 5.1.6. 多空组合收益的稳健性
### 5.2. 事件分析
### 5.3. IC 分析
### 5.4. 换手率分析
### 5.5. 参考文献

<more>

Alphalens的报告并非不言自明。比如，它没有告诉你Alpha和beta各是什么单位，bps单位又是多少；它更不会告诉你，什么样的Alpha是好的，什么样的Alpha则是好到不能相信；有一些报表，它的计算方式与你想像的、或者曾听说的不太一样。

为了准确地理解这些报告，我们使用了三种方式：1. 阅读、调试源码的方式。通过这种方式，我们发现bps是万分之一，定义在plotting.py这个文件中；2. 使用合成数据，这样我们理解了最好的因子理论上应该产生什么样的图表报告；3. 通过Github issues, Quantopian社区Archive的文档，从其它用户的问题中找到答案。

这将是现阶段全网惟一一个真正讲透了Alphalens的教程。

</more>

---

## 6. Alphalens 高级技巧（1）
### 6.1. 排除功能性错误
#### 6.1.1. 过时的 Alphalens 版本
#### 6.1.2. MaxLossExceedError
#### 6.1.3. 时区问题
### 6.2. 因子的单调性
### 6.3. 再谈收集价格数据
### 6.4. 该如何分析日线以上级别的因子？
### 6.5. 深入因子分层
#### 6.5.1. 有确定交易信号的因子
#### 6.5.2. 离散值因子

<more>

这一章我们将介绍如何排除Alphalens在使用中可能遇到的错误，既有程序性的，也有逻辑性的。我们还介绍了如何进行日线以上级别的因子分析。很多网上教程甚至都没意识到这里会存在问题，因为他们从来没有做过这个级别的分析。

我们还深入探讨了Alphalens的分层机制，包括如何处理因子值是离散值的情况。

</more>

---

## 7. Alphalens 高级技巧（2）
### 7.1. 重构因子检验过程
### 7.2. 参数调优：拯救你的因子
#### 7.2.1. 修正因子方向
#### 7.2.2. 过滤非线性分层
#### 7.2.3. 使用最佳分层方式
#### 7.2.4. Grid Search
### 7.3. 过拟合检测方法
#### 7.3.1. 样本外检测
#### 7.3.2. 绘制参数高原
### 7.4. 关于多空组合的思考

<more>

使用Alphalens进行因子检验，就像做一场面试一样，你得尽可能暴露因子的潜能，然后才能评估它的好坏。这一章我们将介绍如何想尽办法把因子的潜能挖掘出来，同时，又不要受过拟合的欺骗。除了样本外检测之外，我们还会教你通过绘制参数高原来评估因子的过拟合程度。

可视化很重要。尤其是你的工作，需要与他人合作时。

</more>

---

## 8. Alpha101 因子介绍
### 8.1. Alpha101 因子中的数据和算子
### 8.2. Alpha101 因子解读
### 8.3. 如何实现 Alpha101 因子？

<more>

Alpha101因子库是World Quant发表于2015年的一个因子库。其中有80%的因子是在世坤正式使用（发布时间）的。我们将介绍如何读懂Alpha101因子的公式，实现它的算子。

整个因子库的实现已经有较好的开源库，我们也将介绍。这会成为你的兵器库中的宝贝之一。

</more>

---

## 9. Talib 技术因子
<!--时序因子几乎是 CTA、加密货币中的惟一因子类型。同时，在 A 股也有非常重要的地位-->

<!-- Percentage Price Oscillator https://github.com/stefan-jansen/machine-learning-for-trading/blob/main/24_alpha_factor_library/02_common_alpha_factors.ipynb-->
### 9.1. Ta-lib 函数分组
### 9.2. 冷启动期 (unstable periods)
<!--不是仅仅去掉 NAN 就稳定了。RSI 大概在 3 * win 之后才稳定-->
### 9.3. 震荡类指标
#### 9.3.1. RSI
<!-- RSI 翻新应用, intelli RSI, Connor's RSI -->
#### 9.3.2. ADX - 平均方向运动指数
#### 9.3.3. APO - 绝对价格震荡指标
#### 9.3.4. PPO - 百分比价格震荡指标
#### 9.3.5. Aroon 振荡器
#### 9.3.6. Money Flow Index
#### 9.3.7. Balance of Power
#### 9.3.8. William's R
#### 9.3.9. Stochastic 随机振荡指标
### 9.4. 成交量指标
#### 9.4.1. Chaikin A/D Line
#### 9.4.2. OBV
### 9.5. 波动性指标
#### 9.5.1. ATR 与 NATR - 平均真实波幅
### 9.6. 8 种移动平均线
### 9.7. Overlap 研究
#### 9.7.1. 布林带
#### 9.7.2. Hilbert 趋势线和 Sine Wave Indicator
#### 9.7.3. Parabolic Sar
### 9.8. Momentum 指标
<more>

Alpha101因子多数是量价因子，由于可以想到的原因，它没有重复早已存在多年的经典技术因子，但这些因子仍然有它的Alpha存在。这一节我们会简单介绍下talib库，讲解技术指标的冷启动期 -- 可能是一个比较冷的知识，冷启动期不止是NaN，比如，RSI的冷启动期就比较长，是win参数的3倍。

Talib的技术指标很多，我们会每类介绍几个，重点介绍在新的技术条件下，如何翻新这些因子。以RSI为例，我们会讲intelli-RSI，Connor's RSI。这样你不仅得到了一些新因子，还提升了自己创新研究的能力。

即使是一些有经验的人，也可能是初次听说我们讲要介绍的一些因子。比如像Hilbert Sine Wave，这可是在Trading View等平台上比较好卖的付费技术指标之一。

</more>


---

## 10. 其它量价因子
### 10.1. 小概率事件
<!-- 单个极值事件，比如沪指单日最大跌幅、最大连续跌幅，背后是小概率事件发生后的回归 -->
### 10.2. 最大回撤
### 10.3. pct_rank
### 10.4. 波动率
### 10.5. z-score
### 10.6. 夏普率
### 10.7. 一阶导因子
### 10.8. 二阶导因子
### 10.9. 频域因子
### 10.10. TSFresh 因子库
### 10.11. 行为金融学因子
#### 10.11.1. 整数关口因子
#### 10.11.2. 冲压失败因子
<!--冲击前高、前低失败-->
#### 10.11.3. 缺口因子
<!--逢缺必补-->
#### 10.11.4. 遗憾规避理论因子
<!-- 日内成交均线冲击、日间密集成交区冲击因子 -->

<more>

有一些小概率因子很容易做出来。也许正因为是这样的原因，它们没有名字，也没有上论文的机会。但是它们的Alpha真实存在。比如指数单日最大跌幅、最大连续跌幅等等。其背后的原理是极端事件之后的概率回归。

总之，这是比较炫技和创新的一章。我们会介绍二阶导因子、频域因子、行为金融学因子。比如，频域因子是通过快速傅里叶变换或者小波变换，找出主力资金的操作周期来进行预测的因子。在其他人还停留在使用小波平滑噪声的阶段，我们已经开始使用它来探索主力资金的规律了！

</more>

---

## 11. 基本面因子和另类因子
### 11.1. Famma 五因子
#### 11.1.1. 市场因子
#### 11.1.2. 规模因子
<!--
小市值效应中的幸存者偏差：The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect" (by Tyler Shumway and Vincent Warther) 

rolf banz如何错过了低波动因子 https://www.rolfbanz.ch/2012/09/low-beta-anomaly-some-early-evidence/

毕业论文被大佬狂怼： http://www.jieyu.ai/blog/2024/09/12/rolf-banz/
-->

#### 11.1.3. 价值因子
#### 11.1.4. 盈利因子
#### 11.1.5. 投资因子
### 11.2. 另类因子
<!-- 掘金冷门数据 https://pdf.dfcfw.com/pdf/H3_AP202204011556464427_1.pdf -->

#### 11.2.1. 社交媒体情绪因子
<!--股吧排名、热搜-->
#### 11.2.2. 网络流量因子
#### 11.2.3. 卫星图像因子
<!--这是 CNN 网络得以应用的地方-->
#### 11.2.4. 专利申请因子
<!--包括专利申请通过、药品上市批准等，再向前挖就是药品中期试验数据-->
### 11.3. 爬虫的技术路线
<!-- request > scrapy > selenium > playright > extension -->

<more>

这一部分我们讲思路会比较多。因为另类因子要么去买，要么去爬。但我们不想讲爬虫。

</more>

---

## 12. 因子挖掘方法
<!-- 新的技术发展、跨界融合 
时装轮回 -- 很多因子是风格因子。一段时间不好，过一段时间就好了
进入到不同的交易品种。不是所有的因子都在所有的市场和交易品种上被认真的尝试过
进入不同的频率。有一些因子在宏观上不行，但在高频中就可能有效。
因子不是一切

从其它领域借用名词： 信息断食 https://www.wenxuecity.com/news/2024/09/15/125777979.html
-->
### 12.1. 新因子从哪里来
<!-- 改造传统技术指标、论文、同行、路演交流--》
<!-- 从哪里找论文 金融顶刊-->
<!-- 从自己或者别人的交易经验中来 -->
<!-- 从涨停、强势个股中来。对非常强的个股，前面介绍的因子往往都是不能用的，有它们自己的技术局限。要构建自己的市场指标，比如涨停家数、上涨家数-->

<!-- 

创新来自于边缘地带。创新来自于“混搭”。罗素选择的是如何用逻辑解释数学，这一独特的角度才使他最终成为一代宗师。我们讲到，从来就没有什么新技术，创新来自于继承和综合。很多学哲学的朋友觉得罗素的学生维特根斯坦更牛，也有人觉得另一位哲学家弗雷格比罗素的思想更早。的确，罗素就像一块海绵，一直在从别人那里吸取知识，随时准备改变自己的想法，罗素后期受维特根斯坦影响很大。但是，罗素的特点是集大成，他的整合能力更强，所以，综合来看，我们应该承认，罗素对哲学的影响更大。

尤其要熟悉罗素开创的数理逻辑。

罗素认为，我们的日常语言很混乱，容易误导，吵了半天，其实大家说的不是一回事，这很容易产生坏的哲学，逻辑则可以澄清和消除这些误解，更好地处理抽象的概念。

其次著名心理学家卡尼曼指出，我们的大脑中有系统一和系统二。系统二就包括了逻辑推理，但这不是我们天生就熟悉的，所以特别需要后天去学习和锻炼。

新的技术指标：

Awesome Oscillator https://www.ifcmarkets.hk/en/ntx-indicators/awesome-oscillator
Relative Volatility Index https://www.tradingview.com/support/solutions/43000594684-relative-volatility-index/ RVI 指标首次出现在 1993 年的《Technical Analysis of Stocks & Commodities》杂志上。
Relative Vigor Index: https://www.investopedia.com/terms/r/relative_vigor_index.asp
Average Daily Range: https://tw.tradingview.com/scripts/adr/
Williams Alligator: https://www.investopedia.com/articles/trading/072115/exploring-williams-alligator-indicator.asp
Connors RSI: 
Smoothed Moving Average: https://trendspider.com/learning-center/what-is-the-smoothed-moving-average-sma/
PVT: https://www.tradingview.com/support/solutions/43000502345-price-volume-trend-pvt/

```python https://github.com/TA-Lib/ta-lib-python/issues/622
def PVT(c, v):
    return np.cumsum(v[1:] * np.diff(c) / c[:-1])
```

-->
### 12.2. 网络资源
<!--聚宽因子看板
[^yzkb]:  [聚宽的因子看板](https://www.joinquant.com/view/factorlib/list)。在这里我们可以浏览一些常见的因子分类，及各类因子在当前市场环境下的表现。
-->
### 12.3. 因子正交性检测
<!-- https://github.com/stefan-jansen/machine-learning-for-trading/blob/f652d79ab2f137d75d554af2cc437a5512b16069/24_alpha_factor_library/04_factor_evaluation.ipynb -->
### 12.4. 谈谈因子动物园

<more>

这也是谈天谈地比较务虚的一章，但依然干货满满。我们会谈一些找资源的方法，比如怎么找论文、数据等。到现在为止，我们已经介绍了好几百个因子（不算参数和周期），所以，我们也需要看看究竟有多少因子是独立的。所以，我们会介绍正交性检测方法。

</more>

---

## 13. 机器学习概述
### 13.1. 机器学习分类
#### 13.1.1. 机器学习、深度学习、强化学习
<!--https://www.showmeai.tech/article-detail/185-->
#### 13.1.2. 监督无监督和强化学习
#### 13.1.3. 回归与分类
### 13.2. 机器学习模型简介
### 13.3. 机器学习三要素
### 13.4. 机器学习基本流程
<!-- https://scikit-learn.org/1.4/tutorial/basic/tutorial.html -->
### 13.5. 机器学习应用场景
<!--
线性回归、广义加性（决策树）、集成模型（梯度增强）、神经网络、强化学习、遗传算法、Bayesian 网络、高斯过程
-->
<!-- 回归与分类的本质是一个经典哲学问题，世界是连续的，还是量子化的？这个问题之所以经典，是因为它无所不在。当我们要用机器学习来解决一个问题是，首先就会遇到它：这是回归回题，还是分类问题？-->

<!--弄懂这些概念，帮助我们了解机器学习的局限在哪里，以及通用人工智能难在哪里。-->

<more>

机器学习快速入门。世界是连续的，还是量子？这是一个古老的哲学问题，也决定了机器学习的基本模型 -- 回归还是分类？

</more>

---

## 14. 机器学习核心概念
<!-- 线性代数、梯度优化、反向传播、激活函数 -->
### 14.1. 偏差、方差
### 14.2. 过拟合与正则化惩罚
### 14.3. 损失函数、目标函数和度量函数和距离函数
#### 14.3.1. 损失函数和目标函数
#### 14.3.2. 度量函数
#### 14.3.3. 距离函数

<!--通义千问，损失函数与距离函数的区别-->
<!-- https://stackoverflow.com/a/47306502/13395693 -->
<!-- 欧氏距离与 MSE 的区别-->

<more>

这门课程是一门应用课程，不想涉及太多理论，但如果一点原理都不懂，就只能照搬照抄示例，无法进行任何拓展。因此，我们决定选择跟应用层密切相关的基本概念进行讲解 -- 只有了解了这些概念，我们才懂得如何选择目标函数，如何评估策略，如何防止过拟合等等。

</more>

---

## 15. SKLearn 通用工具包
### 15.1. 数据预处理：preprocessing
<!-- 标准化工具、归一化工具、缺失值处理、独一码编码 -->
### 15.2. metrics
<!-- 其它前面已经介绍过一部分，这里介绍一下 sklearn 中的位置，以及没有介绍的部分 -->
### 15.3. 模型解释与可视化
### 15.4. 内置数据集
<!-- load_iris, fetch_openml, make_classification-->
<!-- https://github.com/stefan-jansen/machine-learning-for-trading/tree/main/06_machine_learning_process -->
<more>

<!--如何阅读困惑矩阵-->
<!--1. https://www.v7labs.com/blog/confusion-matrix-guide-->
<!-- 2. 三分类困惑矩阵：https://digitalcommons.aaru.edu.jo/cgi/viewcontent.cgi?article=1115&context=erjeng-->
sklearn 是一个非常强大的机器学习库，以丰富的模型和简单易用的接口赢得大家的喜爱。在这一章，我们先向大家介绍 sklearn 的通用工具包 -- 用来处理无论我们采用什么样的算法模型，都要遇到的那些共同问题，比如数据预处理、模型评估、模型解释与可视化和内置数据集。


</more>

---

## 16. 模型优化
### 16.1. 优化概述
<!-- 目标和分类：
        一阶优化：SGD, Momentum, AdaGrad
        二阶优化：梯度和二阶导
        零阶优化方法： 粒子群、遗传算法 GA
    -->
### 16.2. k-fold cross validation
### 16.3. 参数搜索
#### 16.3.1. 网格搜索
#### 16.3.2. 随机搜索
#### 16.3.3. 贝叶斯优化

### 16.4. Rolling Forecasting
<!-- 用于模型的解释工具， inspection & visualization-->
<!-- knn 预测 https://github.com/sammanthp007/Stock-Price-Prediction-Using-KNN-Algorithm -->
<more>

量化领域的机器学习有它自己的特殊性，比如在交叉验证方面，我们实际上要使用的是一种称为 Rolling Forecasting（也称为 Walk-Forward Optimization 的方法）。

</more>

---

## 17. 聚类：寻找 Pair Trading 标的
### 17.1. 聚类算法概述
<!-- kmeans vs DBSCAN vs HDBSCAN -->
<!--如果特征太多，先降维-->
### 17.2. HDBSCAN 算法原理
<!-- https://scikit-learn.org/stable/modules/clustering.html#hdbscan -->
### 17.3. 寻找 Pair Trading 标的
#### 17.3.1. HDBSCAN 示例
<!-- https://towardsdatascience.com/dbscan-clustering-for-trading-4c48e5ebffc8 -->
#### 17.3.2. 结果评估
<!-- 将股价走势绘制出来-->
<!-- ADF 测试 -->
#### 17.3.3. 配对选择
<!-- https://github.com/quantrocket-codeload/quant-finance-lectures/blob/master/quant_finance_lectures/Lecture42-Introduction-to-Pairs-Trading.ipynb-->

<more>

在量化交易中，Pair Trading 是一类重要的套利策略，它的先决条件是找出能够配对的两个标的。这一章我们将介绍先进的 HDBSCAN 聚类方法，演示如何通过它来实现聚类，然后通过 statsmodels 中的相关方法来执行协整对检验，找到能够配对的标的。最后，我们还将演示如何将这一切组成一个完整的交易策略。

这将是你学会的第一个有效的机器学习策略。

</more>

---

## 18. 从决策树到 LightGBM
<!-- 决策树、随机森森、GBDT、XGBoost\LightGBM -->
### 18.1. 决策树
<!-- https://github.com/edyoda/data-science-complete-tutorial/blob/master/6.%20Decision%20Tree.ipynb -->
#### 18.1.1. 决策树分类 <!-- https://scikit-learn.org/stable/modules/tree.html#classification -->
#### 18.1.2. 决策树回归
### 18.2. LightGBM
<!-- https://github.com/datacamp/Machine-Learning-With-XGboost-live-training/blob/master/notebooks/Machine-Learning-with-XGBoost-solution.ipynb -->
#### 18.2.1. 熟悉训练数据
#### 18.2.2. 构建第一个分类器
#### 18.2.3. 可视化特征重要性
#### 18.2.4. 查看模型树
#### 18.2.5. 交叉验证
#### 18.2.6. 调优
<!-- 我们将探索 max depth, colsample_bytree, subsample, min_child_weight, gamma, alpha, learning_rat 等参数的作用，并使用 grid_search_cv 和 RandomizedSearchCV 来进行超参数调优。-->

<!-- LightGBM 与 XGBOOST 的比较 https://www.showmeai.tech/article-detail/195 -->

<more>

受限于金融数据的高噪声，现阶段端到端的交易策略还不太可行；又受限于标注数据的大小，深度学习等人工智能模型也不适用于交易策略的构建。在机器学习模型当中，目前最优秀的模型就是梯度提升决策树模型。代表实现是XGBoost和LightGBM。

由于LightGBM在多数任务上，无论是速度还是准确率都超越了XGBoost，所以，我们的课程将重点介绍LightGBM。

这一章将完整地介绍LightGBM模型，并且通过示例来演示如何使用、如何inspect和visualize生成的模型，如何执行交叉验证和参数调优。

</more>

---

## 19. 基于 LightGBM 回归模型的价格预测
### 19.1. 策略原理
<!-- 
均线与价格之间的线性变换
如果均线具有稳定性，则价格会向均线回归
-->
### 19.2. 策略实现
### 19.3. 策略优化思路
<!--
1. 使用成本均线，而不是 MA 来进行预测
2. 什么情况下均线才是稳定的？要增加哪些指标？
-->

<more>

资产定价是量化研究的核心问题之一，如果能够给出资产的合理定价，那么就能给出交易信号。

定价是个回归问题。尽管很难实现端到端的价格预测模型，我们还是以巧妙的构思，做出来一个可以预测未来价格的回归模型（理论上能自洽）。

我们不能保证这个模型总是有效的，有许多改进方案我们还没来得及探索，但是，以此为出发点，你在机器学习交易模型构建上，已经占据了领先优势。

</more>

---

## 20. 基于 LightGBM 分类模型的交易策略
<!--顶底预测模型-->
### 20.1. 策略实现
#### 20.1.1. 顶底查找算法
#### 20.1.2. 标注工具
##### 20.1.2.1. 基本布局
##### 20.1.2.2. 初始化
##### 20.1.2.3. 部件更新
#### 20.1.3. 构建模型
##### 20.1.3.1. 模型基类
##### 20.1.3.2. V2
##### 20.1.3.3. V3
### 20.2. 算法优化
#### 20.2.1. 样本平衡
#### 20.2.2. 多周期及微观数据
#### 20.2.3. 市场氛围
#### 20.2.4. id作为特征

<more>

在这一章，我们将构建一个基于 LightGBM 分类模型的交易模型。换句话说，它不负责预测价格，但能告诉你应该买入、还是卖出信号。学完这一章，你一定会认同，模型肯定就该这么构建，剩下的都是工作量而已：你需要构建系统、标注数据、构建特征，然后训练模型。

</more>

---

## 21. 未来新世界
<!-- 参考视频： https://www.3blue1brown.com/lessons/mlp -->
### 21.1. 如何获得免费算力 <!-- 标注数据量决定 -->

<!-- [Predicting Chinese stock market using XGBoost multi-objective optimization with optimal weighting](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10936758/)
-->

<!-- 我们构建的是一个选股模型，还是交易模型？实际上，我们应该构建两个模型，第一个是买入模型，它同时具有选股和择时能力；第二个是卖出模型，它有择时能力，只负责判断何时卖出
XGBoost很好，但LightGBM可能在内存占用、某些场景下的训练速度上会更优。这一章将介绍LightGBM如何使用。我们会给一个完整的例子，但不会涉及太多细节。这就是你常常在其它课程中会看到的那种内容。
-->

### 21.2. CNN 价格预测
#### 21.2.1. 如何为训练提供数据
#### 21.2.2. 如何构建特征数据
#### 21.2.3. 如何定义模型
#### 21.2.4. 训练
#### 21.2.5. 生产部署
#### 21.2.6. CNN的原理与性能优化
### 21.3. Transformer
<!--CNN 有容错能力，对关键点的识别有误差，这与人脸识别不一样-->
### 21.4. Reinforcement Learning
### 21.5. 其它重要智能算法
#### 21.5.1. kalman filter
#### 21.5.2. Genentic Algo

<more>

前面讲过为什么深度学习还不太适合构建量化交易模型。这一章前面部分，我们会通过一个CNN预测价格的例子，来说明为什么。了解了这些局限之后，也许你能够发明一种新颖的模型，适合量化交易。这一部分没能教你可带走的工具和经验。但是如果你是研究型、创新型的人，你也会觉得这一部分内容也非常有价值。

强化学习是我们比较看好的一个方向，特别是用在商品期货和加密货币交易中。我们会介绍一些入门知识和学习资源。

还有两个重要的智能算法，既不是机器学习，也不是深度学习或者强化学习，但在量化中确实也比较常用，就是kalman filter和genetic algo，不过，这一部分我们没有代码，把更多的探索空间留给了你。。

</more>

</div>

<!--机器学习相关 https://github.com/aialgorithm/Blog-->
<!--机器学习 metrics 中的 average https://stackoverflow.com/questions/52269187/facing-valueerror-target-is-multiclass-but-average-binary-->
<!-- confusion matrix: https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62-->
<!--
傅立叶与小波分析： https://cseweb.ucsd.edu/~baden/Doc/wavelets/polikar_wavelets.pdf
-->

<!-- 重写本课开场白，可以参考罗闻全： https://open.163.com/newview/movie/free?pid=SHK5ITQ33&mid=KHK5ITSBB -->
<hr>

<h2 id="declaration">说明</h2>
<p>1. 本大纲并非课程教材目录，比如，课程中许多章节有《延伸阅读》小节，未在此显示。</p>
<p>2. 课程内容还包括习题，未在此显示</p>
<p>3. 课程内容还包括补充材料，比如完整的 Alpha101因子实现代码（从数据获取、因子提取、因子检验到回测）及其它示例代码，未在此显示</p>
