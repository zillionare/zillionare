---
title: "比Deepseek还要Deep！起底GBDT做回归预测的秘密"
date: 2025-03-09
category: algo
slug: how-gradient-boost-learned-from-regression
motto: 逻辑是证明的工具 直觉是发明的工具
img: 
stamp_width: 60%
stamp_height: 60%
tags: [GBDT, 机器学习, LightGBM, XGBoost]
---

决策树是机器学习中一类重要的算法。它本质是这样一种算法，即将由程序hard-coded的各种if-else逻辑，改写成为可以通过数据训练得到的模型，而该模型在效果上等价于硬编码的if-else逻辑。

```python
for 有房, 年薪 in [("有", "40万"), ("有", "20万"), ("无", "100万")]:
    if 有房 == "有" and 年薪 > "30万":
        print("见家长！")
    else:
        print("下次一定")
```

这样做的好处是，大大增强了算法的普适性：只要有标注数据，无须编码，都可以转换成为对应的决策树模型，条件越复杂，这种优越性就表现的越明显。此外，在决策树的训练过程中，也自然地考虑了数据分布的统计特征、加入了容错（只要数据标注是正确的）。

## 单细胞生物： 决策树

比如，假如我是霸总的助理，要根据他的生活习惯来安排明天是否工作。我收集到过往的数据如下：

```python
data = {
    '天气': ['晴', '晴', '晴', '晴', '阴', '阴', '雨', '雨'],
    '气温': ['高温', '高温', '舒适', '凉爽', '凉爽', '凉爽', '凉爽', '凉爽'],
    '宜工作': [0, 0, 1, 1, 1, 1, 0, 0],
}

df = pd.DataFrame(data)
df
```

<!-- BEGIN IPYNB STRIPOUT -->
<div>
<table border="1" class="z-table-purple">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>天气</th>
      <th>气温</th>
      <th>宜工作</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>晴</td>
      <td>高温</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>晴</td>
      <td>高温</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>晴</td>
      <td>舒适</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>晴</td>
      <td>凉爽</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>阴</td>
      <td>凉爽</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>阴</td>
      <td>凉爽</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>雨</td>
      <td>凉爽</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>雨</td>
      <td>凉爽</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

<!-- END IPYNB STRIPOUT -->

我们就可以用决策树来训练一个模型，从而为他安排明天的出差。如果哪一天他与某个女艺人热恋了，这样会新增一个判断条件，如果头一天晚上学了英语，第二天就不工作了，这样我们就只需要改数据就行了。


```python
data = {
    '天气': ['晴', '晴', '晴', '晴', '阴', '阴', '雨', '雨'],
    '气温': ['高温', '高温', '舒适', '凉爽', '凉爽', '凉爽', '凉爽', '凉爽'],
    '学英语':[0, 1, 0, 0, 1, 0, 0, 1],
    '宜工作': [0, 0, 1, 1, 1, 1, 0, 0],
}

df = pd.DataFrame(data)
df
```

下面这个决策树模型简单是简单了点，不过，它涉及到了决策树模型构建的全部过程：

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# 创建示例数据
data = {
    '天气': ['晴', '晴', '晴', '晴', '阴', '阴', '雨', '雨'],
    '气温': ['高温', '高温', '舒适', '凉爽', '凉爽', '凉爽', '凉爽', '凉爽'],
    '学英语':[0, 0, 0, 0, 1, 0, 0, 1],
    '宜工作': [0, 0, 1, 1, 0, 1, 0, 0],
}

df = pd.DataFrame(data)
df

# 将分类变量转换为数值
df['天气'] = df['天气'].map({'晴': 0, '阴': 1, '雨': 2})
df['气温'] = df['气温'].map({'高温': 0, '舒适': 1, '凉爽': 2})

X = df[['天气', '气温', '学英语']]
y = df['宜工作']

# 创建并训练决策树模型
clf = DecisionTreeClassifier()
clf.fit(X, y)

# 可视化决策树
plt.figure(figsize=(12, 8))
plot_tree(clf, filled=True, feature_names=['天气', '气温', '学英语'], class_names=['诸事不宜', '宜工作'], fontsize=10)
plt.title('霸总工作否？')
plt.show()

# 预测第二天是否工作
weather = "晴"
temp = "高温"
dating=0

sample = pd.DataFrame([(weather, temp, dating)], columns=["天气", "气温", "学英语"])
sample['天气'] = sample['天气'].map({'晴': 0, '阴': 1, '雨': 2})
sample['气温'] = sample['气温'].map({'高温': 0, '舒适': 1, '凉爽': 2})

prediction = clf.predict(sample)
dating_desc = "没学英语" if dating == 0 else "昨晚学了英语"
if prediction[0] == 1:
    print(weather, temp, dating_desc, "宜工作")
else:
    print(weather, temp, dating_desc, "诸事不宜")
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/02/20250309123941.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

## 增加
