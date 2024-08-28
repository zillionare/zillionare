---
slug: numpy-pandas-syllabus
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

<p>§ 量化交易中的 NUMPY 和 PANDAS</p>
<h1 style="text-align:center">课程大纲 </h1>
<div class="cols">

## 1. 导论
## 2. Numpy 核心语法 (1)
<!--https://github.com/yingzk/100_numpy_exercises/blob/master/cn_100_numpy_exercises.md-->
### 2.1. 基本数据结构
#### 2.1.1. 创建数组
_创建数组的常用方法，以及几个内置数组，这些数组在量化中也非常常用_
#### 2.1.2. 增删改操作
_如何向数组中追加、插入、删除元素，以及修改？_
#### 2.1.3. 定位、读取和搜索
_介绍indexing, slicing, searchsorted等_
<!--indexing,slicing and mask-->
#### 2.1.4. 审视 (inspecting) 数组
### 2.2. 数组操作
#### 2.2.1. 升维
#### 2.2.2. 降维
#### 2.2.3. 转置

## 3. Numpy 核心语法 (2)
### 3.1. Structured Array
### 3.2. 运算类
#### 3.2.1. 逻辑运算和比较
#### 3.2.2. 集合运算
#### 3.2.3. 数学运算和统计
_矩阵运算等数学运算及均值、方差、协方差、percentile 等统计函数_
### 3.3. 类型转换和 Typing
_深入了解Numpy数据类型及其转换，以及Typing库，帮助我们写出健壮的代码_
## 4. Numpy 核心语法 (3)
### 4.1. 处理包含 np.nan 的数据
_我们从第三方获得的数据可能包含np.nan数据；技术指标在冷启动期的值也常常是np.nan。在数据包含None或者np.nan的情况下，如果计算其均值、最大值？将介绍 np.isnan, nanmean, nanmax 等 nan *函数_
### 4.2. 随机数和采样
<!--https://github.com/Kyubyong/numpy_exercises-->
_随机数和采样是量化的高频操作，在“造”数据方面非常好用_
### 4.3. IO 操作
_介绍如何读取csv、保存csv等io操作_
### 4.4. 日期和时间
_从其它库中得到的行情数据的时间、日期，怎么转换？_
### 4.5. 字符串操作
_如何在Numpy数组中进行字符串查找等操作?_
## 5. Numpy 量化场景应用案例
### 5.1. 连续值统计
_举例：如何高效地寻找连续涨停、N 连阳和计算 connor's rsi 中 streaks_
### 5.2. cumsum 与分时均价线的计算
_分时均价线在日内交易中非常重要，一般来说，两次攻击分时线不破，就是日内买入（卖出）的信号。我们要如何计算分时均线呢？_
### 5.3. 移动均线的计算
_如何用 numpy 快速计算均线？介绍一个卷积算法_
### 5.4. 自适应参数如何选择才合理？
_很多时候，我们需要自适应参数。怎么选？percentile很多时候是个好方案_
### 5.5. 计算最大回撤
_如果你有经验，就能判断出 2 月 7 日的大反弹。反弹之日，要找跌幅最大的股票。怎么选呢？_
### 5.6. 如何判断个股的长期走势？
_不要买入长期看跌的个股。关键是，如何判断呢？这一节将介绍多项式回归_
### 5.7. Alpha101 中的函数例程
_Alpha101 中有好几个基础函数，因子就构建在这些基础函数上。如何高效地实现它们？_
### 5.8. 寻找相似的k线
_介绍 corrcoef 和 correlate_
### 5.9. 资产组合的收益与波动率示例
_从随机生成若干资产开始，计算资产的期望收益和波动率。这是高频应用场景之一。_
<!--https://www.quantrocket.com/code/?repo=quant-finance-lectures&path=%2Fcodeload%2Fquant-finance-lectures%2Fquant_finance_lectures%2FLecture03-Introduction-to-NumPy.ipynb.html-->
## 6. Numpy 高性能编程实践
### 6.1. Broadcasting
_深入Numpy高效的底层原理_
### 6.2. 使用 NumExpr
<!--https://github.com/aialgorithm/Blog/issues/48-->
### 6.3. 启用多线程
### 6.4. 使用bottleneck库
### 6.5. Numpy 的其它替代方案

## 7. Pandas 核心语法（1）
<!--https://github.com/justmarkham/pandas-videos-->
<!--https://bkds.flygon.net/#/docs/pyda-3e/README-->
### 7.1. 基本数据结构
<!--理解 index, columns 等-->
#### 7.1.1. Series
#### 7.1.2. 创建 DataFrame
#### 7.1.3. 快速探索 DataFrame
_index, info,describe,columns,head,tail 等_
#### 7.1.4. DataFrame 的合并和连接
<!--concat, join, merge-->
#### 7.1.5. 删除行和列
#### 7.1.6. 定位、读取和修改
_介绍Pandas中的索引(indexing)、数据选择_
#### 7.1.7. 转置
#### 7.1.8. 重采样（resample）
_盘中实时获得分钟线惊人地昂贵。所以，我们需要从tick级数据自己合成。这就是重采样_

## 8. Pandas 核心语法 (2)
### 8.1. 逻辑运算和比较
_dataframe中包含了我们提取的特征。要选取PE最大同时是PB最小的前30列，怎么做？_
### 8.2. 分组运算（groupby）
_因子分析数据表包含了行业标签和各公司的PE值。如何选出每个行业PE最强的5支_
### 8.3. 多重索引和高级索引
_这是pandas中比较难懂的内容之一_
### 8.4. 窗口函数
_用以计算移动平均等具有滑动窗口的指标_
### 8.5. 数学运算和统计
_均值、方差、协方差、percentile,diff,pct_change,rank 等统计函数，量化基础_
## 9. Pandas 核心语法 (3)
### 9.1. 数据预处理类
_因子分析的预处理过程中，要进行缺失值、缩尾、去重等操作，怎么做？_
<!--fillna, clip, winsorize,dropna-->
### 9.2. IO 操作
_如何将数据从csv,网页,数据库,parquet等地方读进来_
#### 9.2.1. csv
_除基本操作外，还将介绍读取 csv 时如何加速_
#### 9.2.2. pkl 和 hdf5
#### 9.2.3. parque
#### 9.2.4. html 和 md
<!--换个思路，就是爬虫-->
#### 9.2.5. sql
### 9.3. 日期和时间
_我们从其它库中得到的行情数据的时间、日期，怎么转换？_
### 9.4. 字符串操作
_dataframe存放了证券基本信息，比如名字和代码。如何排除科创板？_
## 10. Pandas 核心语法（4）
### 10.1. 表格和样式
_让pandas拥有excel一样丰富的条件着色功能_
### 10.2. Pandas 内置绘图功能
## 11. Pandas 量化场景应用案例
### 11.1. 通过rolling方法实现通达信例程
_实现通达信公式中的HHV,LLV,HHVBARS,LAST等方法_
### 11.2. 补齐分钟线缺失的复权因子
_介绍最新版引入的as-of-join功能。量化必遇场景_
### 11.3. 为Alphalens准备数据
_使用Alphalens进行因子分析时，最常用的dataframe操作_
## 12. Pandas 性能
### 12.1. 内存优化
_使用category,以及更紧湊的数据类型压缩内存使用_
### 12.2. 优化迭代
_使用 itertuples 而不是 iterrows, 使用 apply 来优化迭代，先筛选再计算_
### 12.3. 使用numpy和numba
### 12.4. 使用eval或者query
<!--使用 isin 筛选 https://zhuanlan.zhihu.com/p/97012199-->
### 12.5. Pandas 的其它替代方案
#### 12.5.1. modin
_一行代码，实现pandas替代，并拥有多核、不受内存限制的计算能力_
#### 12.5.2. polars
_最快的tableu解决方案_
#### 12.5.3. dask
_分布式tableu，可运行在数千结点上_

</div>
<!--
rename columns, sort_values
filter rows by column value 
logical operator
change datatype
Pandas Index
pivot_table https://www.joinquant.com/view/community/detail/92d2ccab2d412dbfa7df366369e6373b
-->
