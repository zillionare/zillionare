<style>

.cols {
    column-count: 2;
    column-gap: 2em;
}

h1, h2, h3, h4 {
    font-weight: 400 !important;
}
h4 {
    color: #808080 !important;
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
    margin: 10px 0;
    position: relative;
    cursor: pointer;
    min-height: 2em;
    display: inline-block;
}

more::before {
    content: 'More >';
    position: absolute;
    top: 50%;
    /* left: 100%; */
    transform: translate(0, -50%);
    width: 4em;
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

<p>§ 因子分析与机器学习策略</p>
<h1 style="text-align:center">课程大纲 </h1>
<div class="cols">

## 1. 导论
### 1.1. 因子投资的起源
### 1.2. 寻找 Alpha
### 1.3. 从 CAPM 拓展到多因子
### 1.4. 从因子分析到因子投资
### 1.5. 从因子模型到交易策略
### 1.6. 关于课程编排

<more>

这门课面向的对象是专业的量化研究员、或者打算向这个方向转岗求职、或者尽管是其它职业，但决心以专业、严谨的态度探索量化研究的学习者。课程内容涵盖了因子挖掘、因子检验到构建机器学习模型的过程。如果要独立从事交易，还需要补充学习《量化 24 课》。

</more>

## 2. 因子预处理流程
### 2.1. 因子数据的来源
### 2.2. 因子生成
### 2.3. 因子预处理
#### 2.3.1. 异常值处理
#### 2.3.2. 缺失值处理
#### 2.3.3. 分布调整
#### 2.3.4. 标准化
#### 2.3.5. 中性化
### 2.4. 延伸阅读

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

## 4. 初识 Alphalens
### 4.1. 斜率因子：定义和实现
### 4.2. 如何为 Alphalens 计算因子和收集价格数据
### 4.3. Alphalens 如何实现数据预处理
### 4.4. 因子分析与报表生成
### 4.5. 参考文献

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

---

## 8. Alpha101 因子介绍
### 8.1. Alpha101 因子中的数据和算子
### 8.2. Alpha101 因子解读
### 8.3. 如何实现 Alpha101 因子？

---

## 9. Talib 技术因子
<!--时序因子几乎是 CTA、加密货币中的惟一因子类型。同时，在 A 股也有非常重要的地位-->

<!-- Percentage Price Oscillator https://github.com/stefan-jansen/machine-learning-for-trading/blob/main/24_alpha_factor_library/02_common_alpha_factors.ipynb-->
### 9.1. Ta-lib 函数分组
### 9.2. 冷启动期 (unstable periods)
<!--不是仅仅去掉 NAN 就稳定了。RSI 大概在 3 * win 之后才稳定-->
### 9.3. 8 种移动平均线
### 9.4. Overlap 研究
#### 9.4.1. 布林带
#### 9.4.2. Hilbert 趋势线和 Sine Wave Indicator
#### 9.4.3. Parabolic Sar
### 9.5. Momentum 指标
#### 9.5.1. RSI
<!-- RSI 翻新应用-->
#### 9.5.2. ADX - 平均方向运动指数
#### 9.5.3. APO - 绝对价格震荡指标
#### 9.5.4. PPO - 百分比价格震荡指标
#### 9.5.5. Aroon 振荡器
#### 9.5.6. Money Flow Index
#### 9.5.7. Balance of Power
#### 9.5.8. William's R
#### 9.5.9. Stochastic 随机振荡指标
### 9.6. 成交量指标
#### 9.6.1. Chaikin A/D Line
#### 9.6.2. OBV
### 9.7. 波动性指标
#### 9.7.1. ATR 与 NATR - 平均真实波幅

## 10. 其它因子
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

## 11. 基本面因子和另类因子
### 11.1. Famma 五因子
#### 11.1.1. 市场因子
#### 11.1.2. 规模因子
#### 11.1.3. 价值因子
#### 11.1.4. 盈利因子
#### 11.1.5. 投资因子
### 11.2. 另类因子
#### 11.2.1. 社交媒体情绪因子
<!--股吧排名、热搜-->
#### 11.2.2. 网络流量因子
#### 11.2.3. 卫星图像因子
<!--这是 CNN 网络得以应用的地方-->
#### 11.2.4. 专利申请因子
<!--包括专利申请通过、药品上市批准等，再向前挖就是药品中期试验数据-->

## 12. 因子挖掘方法
<!-- 新的技术发展、跨界融合 
时装轮回 -- 很多因子是风格因子。一段时间不好，过一段时间就好了
进入到不同的交易品种。不是所有的因子都在所有的市场和交易品种上被认真的尝试过
进入不同的频率。有一些因子在宏观上不行，但在高频中就可能有效。
因子不是一切
-->
### 12.1. 改造传统技术指标
### 12.2. 论文
### 12.3. 同行、路演交流
<!-- 2023 年的 DMA 策略 -->
### 12.4. 网络资源
<!--聚宽因子看板-->
### 12.5. 因子正交性检测
<!-- https://github.com/stefan-jansen/machine-learning-for-trading/blob/f652d79ab2f137d75d554af2cc437a5512b16069/24_alpha_factor_library/04_factor_evaluation.ipynb -->
### 12.6. 因子不是一切！谈谈因子动物园

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
## 15. sk-learn 通用工具包
### 15.1. 数据预处理：preprocessing
<!-- 标准化工具、归一化工具、缺失值处理、独一码编码 -->
### 15.2. metrics
<!-- 其它前面已经介绍过一部分，这里介绍一下 sklearn 中的位置，以及没有介绍的部分 -->
### 15.3. 模型解释与可视化
### 15.4. 内置数据集
<!-- load_iris, fetch_openml, make_classification-->

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

## 18. 从决策树到 XGBoost
<!-- 决策树、随机森森、GBDT、XGBoost\LightGBM -->
### 18.1. 决策树
<!-- https://github.com/edyoda/data-science-complete-tutorial/blob/master/6.%20Decision%20Tree.ipynb -->
#### 18.1.1. 决策树分类 <!-- https://scikit-learn.org/stable/modules/tree.html#classification -->
#### 18.1.2. 决策树回归
### 18.2. XGBoost
<!-- https://github.com/datacamp/Machine-Learning-With-XGboost-live-training/blob/master/notebooks/Machine-Learning-with-XGBoost-solution.ipynb -->
#### 18.2.1. 熟悉训练数据
#### 18.2.2. 构建第一个分类器
#### 18.2.3. 可视化特征重要性
#### 18.2.4. 查看模型树
#### 18.2.5. 交叉验证
#### 18.2.6. 调优
<!-- 我们将探索 max depth, colsample_bytree, subsample, min_child_weight, gamma, alpha, learning_rat 等参数的作用，并使用 grid_search_cv 和 RandomizedSearchCV 来进行超参数调优。-->

<!-- LightGBM 与 XGBOOST 的比较 https://www.showmeai.tech/article-detail/195 -->
---

## 19. 基于 XGBoost 回归模型的价格预测
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

## 20. 基于 XGBoost 分类模型的交易策略
<!--顶底预测模型-->
### 20.1. 策略原理
### 20.2. 策略实现
#### 20.2.1. 数据标注工具
#### 20.2.2. 模型实现代码
#### 20.2.3. 模型评估与优化

## 21. XGBoost 再思考
### 21.1. 更好的 XGBoost: LightGBM?
### 21.2. 如何构建组合？
### 21.3. 资产定价模型还是交易模型？
### 21.5. 为什么是 XGBoost，而不是神经网络？ <!-- 标注数据量决定 -->

<!-- [Predicting Chinese stock market using XGBoost multi-objective optimization with optimal weighting](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10936758/)
-->

<!-- 我们构建的是一个选股模型，还是交易模型？实际上，我们应该构建两个模型，第一个是买入模型，它同时具有选股和择时能力；第二个是卖出模型，它有择时能力，只负责判断何时卖出 -->

## 22. 结语与展望
### 22.1. CNN 网络识别 K 线模式
#### 22.1.1. 如何获得免费 GPU 资源
#### 22.1.2. 示例
#### 22.1.3. CNN 模式识别的问题
##### 22.1.3.1. 数据集增广
##### 22.1.3.2. 错放的容错能力
<!--CNN 有容错能力，对关键点的识别有误差，这与人脸识别不一样-->
### 22.2. Reinforcement Learning
#### 22.2.1. 强化学习基础
#### 22.2.2. 为什么强化学习适合量化交易？ <!-- 商品和加密货币 -->
#### 22.2.3. 强化学习资源
### 22.3. 其它重要智能算法
#### 22.3.1. kalman filter
#### 22.3.2. Genentic Algo

</div>

<!--机器学习相关 https://github.com/aialgorithm/Blog-->
<!--机器学习 metrics 中的 average https://stackoverflow.com/questions/52269187/facing-valueerror-target-is-multiclass-but-average-binary-->
<!-- confusion matrix: https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62-->
<!--
傅立叶与小波分析： https://cseweb.ucsd.edu/~baden/Doc/wavelets/polikar_wavelets.pdf

-->
