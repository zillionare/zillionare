---
slug: 24-lectures-syllabus
---

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
    color: #a0a0a0 !important;
}

.module {
    text-align: center;
    font-size: 2em;
    margin: 2em 0;
}

em {
    font-size: 0.75em;
    font-style: italic;
    color: #808080;
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
var sidebarTOCBtn = document.getElementById('sidebar-toc-btn')
document.body.setAttribute('html-show-sidebar-toc', true)
</script>
<p>§ 量化二十四课</p>
<h1 style="text-align:center">课程大纲 </h1>

## 1. 导论
### 1.1. 证券投资和量化交易的发展
### 1.2. 量化交易知识体系
### 1.3. 什么样的人适合做量化？
### 1.4. 量化策略浅探
#### 1.4.1. Alpha 策略
#### 1.4.2. 市场中性策略
#### 1.4.3. 高频套利策略
#### 1.4.4. 技术分析类策略
#### 1.4.5. 策略研究方法
### 1.5. 课程内容简介
### 1.6. 如何学习本课程
#### 1.6.1. 预备知识
#### 1.6.2. 在线量化环境介绍
  
<div class="module">I. 证券常识与数据源</div>

<em>这一部分介绍最量化交易必须掌握的证券常识，比如复权。复权是量化交易中不可回避的问题，将贯穿我们课程始终，但我们在网上看到的答案，很多是错的。这一节还会告诉你一个意想不到的问题，Python在四舍五入上也有问题</em>

## 2. 证券常识及数据源之 Akshare
### 2.1. 交易所及证券代码
### 2.2. 复权知识
### 2.3. Akshare
#### 2.3.1. 在课件环境下安装 akshare
#### 2.3.2. 实时股票数据
#### 2.3.3. 股票历史数据
#### 2.3.4. 证券列表
#### 2.3.5. 交易日历
#### 2.3.6. 封装和改进建议
#### 2.3.7. 练习

## 3. 数据源之 Tushare、JqDataSdk
### 3.1. TUSHARE
#### 3.1.1. 在课件环境下安装和设置 token
#### 3.1.2. 股票历史数据
#### 3.1.3. 证券列表
#### 3.1.4. 交易日历
### 3.2. 聚宽本地数据
#### 3.2.1. 在课件环境下安装和设置账号
#### 3.2.2. 股票历史数据
#### 3.2.3. 证券列表
#### 3.2.4. 交易日历
### 3.3. BAOSTOCK
#### 3.3.1. 股票历史数据
#### 3.3.2. 证券列表
### 3.4. YFINANCE
<em>这一节的习题，将提示前后复权之间的线性变换关系</em>
  
## 4. 使用Zillionare来获取数据
### 4.1. Omicron
#### 4.1.1. 初始化 omicron
#### 4.1.2. 实时股票数据
#### 4.1.3. 股票历史数据
#### 4.1.4. 证券列表
#### 4.1.5. 交易日历
#### 4.1.6. 板块数据
### 4.2. 数据解读 A 股: 投资者人数与市场走势关系

## 5. 习题讲解（仅视频）

<div class="module">
II. 初识策略
</div>
<em>6~8课构成课程的第二部分。我们从基本面、技术面和交易执行等三个维度介绍了三种类型的策略，以及如何编写策略回测和构建一个简单的回测框架。在示例中，我们还提供了更多的策略，比如Connor's RSI策略</em>

## 6. 小市值策略
### 6.1. 小市值策略简介
### 6.2. 策略实现 - 手动实现最简单的回测
#### 6.2.1. 初始化
#### 6.2.2. 绘图
#### 6.2.3. 策略主体代码
### 6.3. 策略优化
#### 6.3.1. 择时优化
#### 6.3.2. 规则优化
#### 6.3.3. 参数优化
  
## 7. 布林带策略
### 7.1. 使用coursea的初始化
### 7.2. 基于基类的布林带策略 - 回测框架化
### 7.3. 策略优化方向讨论
#### 7.3.1. 参数优化
#### 7.3.2. 趋势判断
  
## 8. 网格交易
### 8.1. 网格交易 - 无需择时的策略
### 8.2. 代码实现
#### 8.2.1. 初始化
#### 8.2.2. 评估函数
#### 8.2.3. 策略行为分析
### 8.3. 技术实现问题
#### 8.3.1. 委托价格和交易时机
#### 8.3.2. 送转问题
#### 8.3.3. 交易单位
### 8.4. 策略优化: 从1.37%到79.8%!
#### 8.4.1. 选择有“界”的标的
##### 8.4.1.1. 大市值股票
##### 8.4.1.2. 超跌股票
##### 8.4.1.3. 可转债
#### 8.4.2. 基于历史数据，确定网格参数
#### 8.4.3. 提高资金利用率
### 8.5. 趋势跟踪网格
  
<div class="module">III. 量化交易中的数据分析：理论与实现</div>
<em>9~13是量化分析的基本功，重点介绍Numpy、Pandas、Talib等库的用法。第9章的习题提供了很多富有技巧、且在量化中常用的Numpy练习题</em>

## 9. Numpy 和 Pandas
### 9.1. Numpy
#### 9.1.1. 创建数组
##### 9.1.1.1. vanilla version
##### 9.1.1.2. 预置特殊数组
##### 9.1.1.3. 通过已有数组转换
#### 9.1.2. 查看 (inspecting) 数组特性
#### 9.1.3. 数组操作
##### 9.1.3.1. 升维
##### 9.1.3.2. 降维
##### 9.1.3.3. 转置
##### 9.1.3.4. 增加/删除元素
#### 9.1.4. 逻辑运算和比较
#### 9.1.5. 集合运算
#### 9.1.6. 数学运算
##### 9.1.6.1. 点乘
##### 9.1.6.2. 聚合运算和统计函数
#### 9.1.7. 读取、查找和搜索
##### 9.1.7.1. 索引和切片
##### 9.1.7.2. 查找、替换、筛选
#### 9.1.8. 类型转换和 typing module
#### 9.1.9. Structured Array
#### 9.1.10. IO
#### 9.1.11. 量化交易中常用函数示例
##### 9.1.11.1. REF(close, n)
##### 9.1.11.2. EVERY(cond, n)
##### 9.1.11.3. LAST(cond_list, n, m)
##### 9.1.11.4. BARSLAST
##### 9.1.11.5. CROSS
### 9.2. Pandas
#### 9.2.1. creation
#### 9.2.2. 数据访问
#### 9.2.3. 遍历 dataframe
### 9.3. pandas vs numpy
  
## 10. Ta-Lib
### 10.1. 安装talib
#### 10.1.1. 原生库的安装
##### 10.1.1.1. Macos
##### 10.1.1.2. Linux
##### 10.1.1.3. Windows
##### 10.1.1.4. 使用conda
##### 10.1.1.5. 第三方构建的wheel包
#### 10.1.2. 安装python wrapper
### 10.2. ta-lib概览
#### 10.2.1. 关于帮助文档
#### 10.2.2. 两类接口
#### 10.2.3. 方法概览
### 10.3. 常用指标函数
#### 10.3.1. ATR
#### 10.3.2. 移动平均线
##### 10.3.2.1. SMA
##### 10.3.2.2. EMA
##### 10.3.2.3. WMA
#### 10.3.3. 布林带
#### 10.3.4. MACD
#### 10.3.5. RSI
#### 10.3.6. OBV （on-balance volume)
### 10.4. 模式识别函数
#### 10.4.1. CDL3LINESTRIKE
#### 10.4.2. CDL3WHITESOLDIERS
  
<em>统计与概率在量化分析中占有重要地位。第11~12课梳理了量化中最常用的统计与概率知识，包括一阶矩到四阶矩、PDF/CDF，协方差等。这一章的示例中，就会解决沪指下跌4%了，此时能不能抄底这样的问题</em>

## 11. 数据分析与Python实现（1）
### 11.1. 考察数据分布
#### 11.1.1. 寻找数据的中心
##### 11.1.1.1. 均值和质心
##### 11.1.1.2. 中位数
##### 11.1.1.3. 众数
#### 11.1.2. 量化数据的分散程度
##### 11.1.2.1. 分位数
##### 11.1.2.2. 方差和标准差
##### 11.1.2.3. 频数、PMF、PDF、CDF、PPF和直方图
##### 11.1.2.4. 概率密度和概率密度函数
##### 11.1.2.5. 累积概率和累积概率函数CDF
##### 11.1.2.6. CDF估计及其应用
##### 11.1.2.7. 几个概念之间的关系
#### 11.1.3. 数据的分布形态
#### 11.1.4. 中心矩的概念
#### 11.1.5. 偏度、峰度在投资中的解释与应用
  
## 12. 数据分析与Python实现（2）
### 12.1. 统计推断方法
#### 12.1.1. 分位图
#### 12.1.2. 假设检验方法
### 12.2. 拟合、回归和残差
#### 12.2.1. 残差及其度量
##### 12.2.1.1. max_error
##### 12.2.1.2. mean_absolute_error
##### 12.2.1.3. mean_absolute_percentage_error
##### 12.2.1.4. mean_squared_error
##### 12.2.1.5. rooted mean squared error
#### 12.2.2. 回归分析
### 12.3. 相关性
#### 12.3.1. 协方差和相关系数
#### 12.3.2. 皮尔逊相关性和斯皮尔曼相关性
#### 12.3.3. 相关性分析示例
### 12.4. 距离和相似性
#### 12.4.1. 常见距离定义列举
#### 12.4.2. 如何计算距离
### 12.5. 归一化
  

## 13. 技术分析实战

<em>传统的技术分析并没有太多的理论支撑，但它基于交易者的经验，自然有它的道理。在学习了第11~12课后，我们把学到的知识用以技术分析，发现峰回路转、别有洞天。传统的技术分析，在统计理论知识加持下，通过自适应参数，大大提高了算法的鲁棒性和择时能力</em>

### 13.1. 箱体的检测
#### 13.1.1. 基于统计的方法
#### 13.1.2. 基于聚类的算法
### 13.2. 寻找山峰与波谷
#### 13.2.1. scipy中的实现
#### 13.2.2. 第三方库：zigzag
#### 13.2.3. 如何平滑曲线
#### 13.2.4. 双顶模式的检测
#### 13.2.5. 圆弧底的检测
### 13.3. 凹凸性检测

## 14. 因子分析

<em>因子是能具有预测能力的特征。因子分析与检验是一种快速筛选其特征的方法，这也是进入量化机构的必考知识点。我们通过手动分步实现因子分析各个步骤，然后介绍Alphalens这一常用因子检验框架</em>

### 14.1. 因子分类
### 14.2. 因子分析
#### 14.2.1. 预处理
##### 14.2.1.1. 异常值处理
##### 14.2.1.2. 缺失值处理
##### 14.2.1.3. 分布调整
##### 14.2.1.4. 标准化
##### 14.2.1.5. 中性化
### 14.3. 单因子测试
#### 14.3.1. 回归法
##### 14.3.1.1. 回归法的因子评价
#### 14.3.2. IC分析法
##### 14.3.2.1. IC分析法的因子评价
#### 14.3.3. 分层回测法
#### 14.3.4. 三种方法的区别与联系
### 14.4. 因子评价体系
  
## 15. Alphalens及其它
### 15.1. Alphalens
#### 15.1.1. Alphalens调用流程
#### 15.1.2. 数据预处理
#### 15.1.3. 因子分析
#### 15.1.4. Alphalens常见错误和警告
##### 15.1.4.1. 时区问题
##### 15.1.4.2. MaxLossExceedError
##### 15.1.4.3. FutureWarning
### 15.2. JQFactor和jqfactor-analyzer
### 15.3. sympy
### 15.4. statistics
### 15.5. statsmodels
#### 15.5.1. OLS（普通最小二乘法）估计
#### 15.5.2. 比较OLS与RLM
#### 15.5.3. ARIMA模型与时间序列预测
### 15.6. zipline
### 15.7. pyfolio
### 15.8. ta

<div class="module">IV. 数据可视化</div>

<em>绘图不仅仅为了创造美丽的可视化效果，更是为了释放数据的全部潜力，并揭示原本隐藏的insights。这一点在量化中也不例外。我们需要有能力绘制k线图、并且叠加回测信号以供我们调优策略，也需要绘制回测报告等。</em>

## 16. Matplotlib 绘图
### 16.1. matplot 简介
### 16.2. 图是如何构成的
#### 16.2.1. 最顶层的概念
#### 16.2.2. pyplot, Figure与Axes之间的关系
#### 16.2.3. layout
#### 16.2.4. Figure Anatomy
### 16.3. 高频使用对象
#### 16.3.1. Axis
##### 16.3.1.1. spine定位与隐藏
##### 16.3.1.2. 共享x轴
##### 16.3.1.3. 刻度
#### 16.3.2. 文本和中文
#### 16.3.3. 样式和颜色
##### 16.3.3.1. colormap
  
## 17. Plotly 绘图
### 17.1. Plotly 中的基本概念
### 17.2. Plotly 模块结构
#### 17.2.1. Plotly Express
#### 17.2.2. Graph Objects
#### 17.2.3. 其它
### 17.3. 比较 plotly express 与 go.Figure
### 17.4. Plotly 股票分析图绘制
#### 17.4.1. K 线图绘制
#### 17.4.2. 叠加技术指标
#### 17.4.3. 子图
#### 17.4.4. 显示区域
#### 17.4.5. 交互式提示
### 17.5. 色彩
#### 17.5.1. 离散色彩序列
#### 17.5.2. 连续色阶
### 17.6. 主题和模板
### 17.7. Dash 简介
#### 17.7.1. Hellow World
#### 17.7.2. 连接到数据
#### 17.7.3. 增加交互式控件
#### 17.7.4. 美化应用程序
#### 17.7.5. 深入Dash
  
## 18. Seaborn 与 PyEcharts 绘图
### 18.1. Seaborn
#### 18.1.1. Seaborn 绘图概览
##### 18.1.1.1. 统计关系的可视化
##### 18.1.1.2. 数据分布的可视化
##### 18.1.1.3. 二元分布的可视化
##### 18.1.1.4. 联合分布和边缘分布
##### 18.1.1.5. 回归拟合
#### 18.1.2. 主题
#### 18.1.3. 调色板的使用
##### 18.1.3.1. 定性调色板
##### 18.1.3.2. 连续调色板
##### 18.1.3.3. 发散调色板
### 18.2. PyEcharts
#### 18.2.1. 在 Notebook/Jupyterlab 中运行
#### 18.2.2. 调用习惯
#### 18.2.3. 使用选项
#### 18.2.4. 子图和布局
##### 18.2.4.1. Grid 布局
##### 18.2.4.2. Page 布局
##### 18.2.4.3. tab 布局
##### 18.2.4.4. Timeline
### 18.3. 关于颜色和美学

<div class="module">V. 回测框架</div>

<em>backtrader是最著名的开源回测框架，很多机构并没有量化投研系统的研发能力，在内部就常常使用backtrader做回测。我们用两个课时，深入讲解了backtrader的用法。</em>

## 19. backtrader 回测框架（1）
### 19.1. 快速开始
### 19.2. backtrader 语法糖
#### 19.2.1. 时间线 (Line)
#### 19.2.2. 运算符重载
### 19.3. Data Feeds
#### 19.3.1. GenericCSVData
#### 19.3.2. Pandas Feed
#### 19.3.3. 自定义一个 Feed
#### 19.3.4. 增加新的数据列
### 19.4. 多周期数据
#### 19.4.1. 多周期技术指标比较
### 19.5. 指标
#### 19.5.1. 内置指标库
#### 19.5.2. 自定义指标
##### 19.5.2.1. 最小周期
  
## 20. backtrader 回测框架（2）
### 20.1. Cerebro
#### 20.1.1. 增加记录器（日志）
#### 20.1.2. 增加观察者
#### 20.1.3. 执行与绘图
### 20.2. Order
#### 20.2.1. notify_order
### 20.3. 交易代理
#### 20.3.1. 资产与持仓查询
#### 20.3.2. 成交量限制
##### 20.3.2.1. FixedSize
##### 20.3.2.2. FixedBarPerc
##### 20.3.2.3. BarPointPerc
#### 20.3.3. 交易时机 - Cheat-On-Open
#### 20.3.4. 交易时机 - Cheat-on-Close
#### 20.3.5. 交易函数
##### 20.3.5.1. 普通交易函数
##### 20.3.5.2. order_target 系列
#### 20.3.6. 组合交易
#### 20.3.7. OCO 订单
#### 20.3.8. 滑点、交易费用
##### 20.3.8.1. 固定滑点
##### 20.3.8.2. 百分比滑点
#### 20.3.9. 交易费用
### 20.4. 可视化
#### 20.4.1. 观察器
##### 20.4.1.1. Broker 观察器
##### 20.4.1.2. BuySell 观察器
##### 20.4.1.3. Trade 观察器
##### 20.4.1.4. TimeReturn 观察器
##### 20.4.1.5. DrawDown 观察器
##### 20.4.1.6. Benchmark 观察器
#### 20.4.2. 定制绘图
#### 20.4.3. 收集回测数据
### 20.5. 优化
### 20.6. 小结


## 21. 策略回测评估

<em>回测结果怎么看？这是一个策略评估问题。这里我们还将解答一个问题，如果你的策略上线了，现在表现弱于预期，在何种情况下应该中止策略？这是一个常见的面试问题。</em>

### 21.1. 回报率
#### 21.1.1. 简单回报率
#### 21.1.2. 对数回报率
#### 21.1.3. Cumulative Returns
#### 21.1.4. Aggregate Returns
#### 21.1.5. Annual Return
### 21.2. 风险调整收益率
#### 21.2.1. sharpe ratio
#### 21.2.2. sharpe 比率与资产曲线的关系
#### 21.2.3. sortino 指标
#### 21.2.4. Max DrawDown （最大回撤）
#### 21.2.5. Sharpe 与 max drawdown 的关系
#### 21.2.6. 年化波动率
#### 21.2.7. Calmar Ratio
#### 21.2.8. Omega Ratio
### 21.3. 基准对照类指标
#### 21.3.1. information ratio
#### 21.3.2. alpha/beta
### 21.4. 策略评估的可视化
#### 21.4.1. Metrics
#### 21.4.2. plots
#### 21.4.3. basic 和 full
#### 21.4.4. html
  

## 22. 回测陷阱

<em>你听说过的回测吃肉、实盘吃土的现象吗？它是如何造成的呢？这一节我们介绍回测陷阱，将以丰富的实战功力，助你快速补齐实战经验不足的问题。</em>

### 22.1. 幸存者偏差
### 22.2. Look-ahead bias
#### 22.2.1. 引用错误
#### 22.2.2. 偷价
#### 22.2.3. 复权引起的前视偏差
#### 22.2.4. PIT数据
### 22.3. 复权引起的问题
#### 22.3.1. 使用复权数据的必要性
#### 22.3.2. 后复权的问题
#### 22.3.3. 复权相关的其它问题
### 22.4. 交易规则
#### 22.4.1. T+1交易
#### 22.4.2. 涨、跌限制
### 22.5. 过度拟合
### 22.6. 回测时长
### 22.7. 回测与实盘的差异
#### 22.7.1. 信号闪烁
#### 22.7.2. 冲击成本
#### 22.7.3. 不可能成交的价格
#### 22.7.4. 撮合问题
### 22.8. 大富翁回测框架
#### 22.8.1. 回测功能简介
##### 22.8.1.1. 架构和风格
#### 22.8.2. 策略框架
##### 22.8.2.1. 数据和数据格式
##### 22.8.2.2. 跨周期数据
##### 22.8.2.3. 驱动模式与性能
##### 22.8.2.4. 回测报告
#### 22.8.3. 一个完整的策略示例
#### 22.8.4. 参数优化
### 22.9. 参考文献

<div class="module">VI. 接入实盘</div>

<em>所有的准备，最终都是为了接入实盘。最后两节课，将为你介绍各种接入方案。</em>

## 23. 实盘交易接口 (1)
### 23.1. easytrader
#### 23.1.1. 安装
#### 23.1.2. 生命期
##### 23.1.2.1. 连接客户端
##### 23.1.2.2. 获取账户信息
##### 23.1.2.3. 交易
#### 23.1.3. 服务器模式
#### 23.1.4. 自动跟单
### 23.2. 东方财富 EMC 智能交易终端
#### 23.2.1. 安装
##### 23.2.1.1. 配置文件单目录
#### 23.2.2. 运行和维护
##### 23.2.2.1. 启动
##### 23.2.2.2. 每日维护
#### 23.2.3. 故障排除与帮助
#### 23.2.4. 撮合配置规则
### 23.3. Trader-gm-adaptor
#### 23.3.1. 冒烟测试
#### 23.3.2. 客户端与服务器交互
##### 23.3.2.1. 客户端请求
##### 23.3.2.2. 返回结果
#### 23.3.3. API 示例
##### 23.3.3.1. 资产表
##### 23.3.3.2. 持仓表
##### 23.3.3.3. 限价买入
##### 23.3.3.4. 市价买入
##### 23.3.3.5. 限价卖出
##### 23.3.3.6. 市价卖出
##### 23.3.3.7. 取消委托
##### 23.3.3.8. 查询当日委托
  
## 24. 实盘交易接口（2）
### 24.1. ptrade
#### 24.1.1. 申请与安装
#### 24.1.2. 策略框架概述
##### 24.1.2.1. initialize
##### 24.1.2.2. before_trading_start
##### 24.1.2.3. handle_data
##### 24.1.2.4. after_trading_end
#### 24.1.3. 一个双均线策略
#### 24.1.4. 复权机制
### 24.2. QMT
#### 24.2.1. 安装和申请量化权限
#### 24.2.2. 功能概览
##### 24.2.2.1. 我的板块
##### 24.2.2.2. 模型研究
##### 24.2.2.3. 模型交易
### 24.3. QMT-Mini
### 24.4. XtData
#### 24.4.1. 获取证券列表
#### 24.4.2. 获取交易日历
#### 24.4.3. 获取行情数据
### 24.5. XtTrader
#### 24.5.1. 封装成web服务
  
