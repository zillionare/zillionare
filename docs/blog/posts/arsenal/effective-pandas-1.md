---
title: Pandas高级技巧-1
subtitle: 
slug: effective-pandas-1
date: 2024-7-15
category: arsenal
motto: 知止而后有定 定而后能安 安而后能虑 虑而后能得 -- 大学
img: https://images.unsplash.com/photo-1719014323201-d7ae3f83d260?q=80&w=1204
lineNumbers: true
tags: 
    - quantlib
    - pandas
---


在量化领域，Pandas是不可或缺的工具，它以强大的数据处理和分析功能，极大地简化了数据操作流程。

今天我们介绍两个技巧，都跟因子检验场景相关。第一个技巧是日期按月对齐；第二个是如何提取分组的前n条记录。讲解的概念涉及到group操作、索引的frequency概念以及多级索引的操作（读取和删除）。

在最后一个例子中，更是反复使用了groupby，以简洁的语法，完成了一个略为复杂的数据操作。

---

## 日期按月对齐

我们在做因子检验的时候，如果使用的是日线以上的频率，依赖于所使用的数据源，就有可能遇到这样一种情况：比如，今年的1月份收盘日是1月31日，但个股可能在1月31日停牌，那么数据源传给我们的月线，就可能把日期标注在1月30日。也就是，我们在生成月度因子数据时，有的个股的日期是1月31日，有的则是1月30或者更早的时间。

如果我们使用Alphalens来进行因子检验，就会产生日期无法对齐，计算前向收益出错的问题。不过，这不是我们今天要介绍的问题。我们今天只讲解决方案，即如何实现所有个股的因子日期都对齐到月。

假设我们有以下数据：

![](https://images.jieyu.ai/images/2024/07/pandas-freq-m.jpg)

---

这里无论是1月还是2月，两个个股的收盘日期都不一致。最简单的方案是使用`index.to_period`函数，将日期对齐到月份。


```python
df.index = df.index.to_period(freq='M')
```

经过转换，就会生成下面的结果：

![](https://images.jieyu.ai/images/2024/07/pandas-freq-m-result.jpg)

这样的转换尽管实现了对齐，但会丢失具体的日期信息。我们也可以使用groupby来实现同样的功能：

```python
(df
    .groupby(['asset', pd.Grouper(freq='M')])
    .last()
    .reset_index("asset")
```

---

结果是：


![50%](https://images.jieyu.ai/images/2024/07/padas-group-by-m.jpg)

语法要点是，asset与index构成一个事实上的惟一索引，我们现在要调整索引的日期，按'asset'进行分组，并且通过Grouper来指定分组的频率。Grouper是作用在索引上的。

`.last()`提供了如何从分组记录中选取记录的功能。它是一种聚合函数，除此之外，还有first, min, max, mean等。在我们的例子中，由于asset与index构成一个惟一的索引，所以，无论使用first, last还是min, max，结果都一样。

## 提取分组的前n条记录

假如，我们通过因子检验，已经确认了某个因子有效，想使用test数据集来进行验证。test数据集也由好多期数据组成，我们需要对每一期数据，取前20%的股票，然后计算它在之后的T1~Tn期的收益，以决定这个因子是否能投入使用。

这实际上是一个DataFrame分组，再取头部n条记录的问题。

---

假设数据是：

```python
df = pd.DataFrame(
    [
        (datetime.datetime(2024, 1, 31), "000001", 9.86),
        (datetime.datetime(2024, 1, 31), "000002", 10.2),
        (datetime.datetime(2024, 1, 31), "000003", 9.84),
        (datetime.datetime(2024, 1, 31), "000004", 11.2),
        (datetime.datetime(2024, 2, 29), "000001", 10.2),
        (datetime.datetime(2024, 2, 29), "000002", 11.2),
        (datetime.datetime(2024, 2, 29), "000003", 9.83),
        (datetime.datetime(2024, 2, 29), "000004", 11),
    ],
    columns=["date", "asset", "factor"]
)
```

我们要取每个月factor最大的前n个，并且生成一个dict，key为每月日期，values为对应的asset数组。

```python
top_n_assets = (df
      .groupby(level=0)
      .apply(lambda x: x.nlargest(2, 'factor')['asset'])
      .reset_index(level = 1, drop = True)
      .groupby(level=0)
      .apply(list)
     ).todict()

top_n_assets
```

---

输出结果是：

```python
date
2024-01-31    [000004, 000002]
2024-02-29    [000002, 000004]
Name: asset, dtype: object

```

这里的技巧是，当我们要按索引进行分组时，我们要使用`grouby(level=?)`的语法。Pandas支持多级索引，第一级索引一般使用level=0来引用，第二级索引使用level=1来引用。

在使用groupby之后，生成的DataFrame就有了两级索引，这个中间结果显示如下：

```python
date        date      
2024-01-31  2024-01-31    000004
            2024-01-31    000002
2024-02-29  2024-02-29    000002
            2024-02-29    000004
Name: asset, dtype: object
```

我们通过第4行的reset_index来删除掉第二级索引。注意在Pandas中，删除索引也是通过调用reset_index来实现的。到此为止，我们实际上已经实现了提取分组的前n条记录的任务。

---

第5~6行是将提取结果扁平化，即将按多行排列的asset，压缩成一个list，结果仍然是一个DataFrame，但每个日期只有一行，其值包含了当期前n个asset。

今天介绍的两个小技巧，都是因子检验中常常遇到的。熟悉掌握Pandas技巧，就能快速搞定因子检验，加快我们因子研发的迭代速度，你学会了吗？

![](https://images.jieyu.ai/images/hot/quant-resources.jpg)

