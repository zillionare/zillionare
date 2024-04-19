---
title: 量化交易中的遗传算法
slug: genetic-algo
date: 2023-12-20
categories:
    - strategies
tags:
    - quant
    - algorithm
    - python
---


## 什么是遗传算法？

- 遗传算法利用自然选择的概念来确定问题的最佳解决方案。
- 遗传算法通常用作优化器，调整参数使得目标最优
- 遗传算法可以独立 | 在人工神经网络的构建中使用。

<!--more-->

比如，交易规则可能使用MACD, RSI等指标，遗传算法将值输入到这些参数中，以利润最大化为目标。随着时间推移，突变产生，突变中有利的影响被保留给下一代。

遗传操作共有三种类型：

1. 交叉(crossover)代表生物学中的繁殖和交叉，即孩子具有父母的某些特征
2. 突变(Mutations)代表生物突变，通过引入随机的小变化来维持从一代到下一代的遗传多样性。
3. 选择（Selections）是从群体中选择个体基因组用于以后育种（重组或交叉）的阶段。

## 遗传算法的实现步骤
1. 初始化一个随机群体，其中每个染色体的长度为 n，其中 n 是参数的数量。即，建立随机数量的参数，每个参数具有n个元素。
2. 选择可增加理想结果（大概是净利润）的染色体或参数。
3. 将突变或交叉算子应用于选定的父母并生成后代。
4. 使用选择算子将后代和当前种群重组，形成新的种群。
5. 重复第二步到第四步

## Python遗传算法库

我们可以通过 geneticalgorithm 这个python库，在量化策略中运用遗传算法。

```python
pip install geneticalgorithm
```


```python
import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def f(X):
    # X为因子。在本方法中，根据因子寻找股票，计算收益率并返回

varbound=np.array([[0,10]]*3)

model=ga(function=f,dimension=3,variable_type='real',
        variable_boundaries=varbound)

model.run()
```

遗传算法也是优化算法的一种，对不明白的地方，可以对照优化算法的概念来理解。


