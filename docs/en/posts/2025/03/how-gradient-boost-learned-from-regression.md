---
title: "GBDT Regression Secrets: Beyond DeepSeek"
date: 2025-03-09
slug: en/posts/algo/how-gradient-boost-learned-from-regression
tags: [Machine Learning, GBDT, Decision Trees, Quantitative Investing]
excerpt: "Decision trees transform hard-coded logic into data-driven models. This article unpacks GBDT regression, explaining how tree structures enable flexible, scalable predictive modeling for quantitative finance."
lang: en
translation_of: posts/algo/how-gradient-boost-learned-from-regression
auto_translated: true
source_sha: beb87514c048c2cfed5ecb863fdeb852fe2d2313
cover: "stamp_width: 60%"
---

Decision trees are a cornerstone of machine learning. Fundamentally, they are algorithms that convert hard-coded `if-else` logic into models trained on data, achieving functional equivalence to manual coding while offering superior scalability.

```python
for 有房, 年薪 in [("有", "40万"), ("有", "20万"), ("无", "100万")]:
    if 有房 == "有" and 年薪 > "30万":
        print("见家长！")
    else:
        print("下次一定")
```

This approach significantly enhances algorithmic universality: as long as labeled data exists, no manual coding is required to convert inputs into a decision tree model. The more complex the conditions, the more pronounced this advantage becomes. Furthermore, the training process naturally incorporates statistical features of data distribution and includes error tolerance (provided the data labels are correct).

## The Single-Cell Organism: Decision Trees

For example, suppose I am an assistant to a "CEO" (a term often used in Chinese romance novels for a dominant, wealthy male lead) and need to schedule whether he should work tomorrow based on his habits. I have collected the following historical data:

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

We can use a decision tree to train a model to schedule his business trips. If he enters a passionate romance with a female celebrity, we simply add a new condition: if he studied English the night before, he won’t work. In this case, we only need to update the data.

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

The decision tree model below is simple, but it illustrates the entire process of building a decision tree:

```python
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Create sample data
data = {
    '天气': ['晴', '晴', '晴', '晴', '阴', '阴', '雨', '雨'],
    '气温': ['高温', '高温', '舒适', '凉爽', '凉爽', '凉爽', '凉爽', '凉爽'],
    '学英语':[0, 0, 0, 0, 1, 0, 0, 1],
    '宜工作': [0, 0, 1, 1, 0, 1, 0, 0],
}

df = pd.DataFrame(data)
df

# Convert categorical variables to numerical values
df['天气'] = df['天气'].map({'晴': 0, '阴': 1, '雨': 2})
df['气温'] = df['气温'].map({'高温': 0, '舒适': 1, '凉爽': 2})

X = df[['天气', '气温', '学英语']]
y = df['宜工作']

# Create and train the decision tree model
clf = DecisionTreeClassifier()
clf.fit(X, y)

# Visualize the decision tree
plt.figure(figsize=(12, 8))
plot_tree(clf, filled=True, feature_names=['天气', '气温', '学英语'], class_names=['诸事不宜', '宜工作'], fontsize=10)
plt.title('Should the CEO Work?')
plt.show()

# Predict whether he should work the next day
weather = "晴"
temp = "高温"
dating=0

sample = pd.DataFrame([(weather, temp, dating)], columns=["天气", "气温", "学英语"])
sample['天气'] = sample['天气'].map({'晴': 0, '阴': 1, '雨': 2})
sample['气温'] = sample['气温'].map({'高温': 0, '舒适': 1, '凉爽': 2})

prediction = clf.predict(sample)
dating_desc = "Did not study English" if dating == 0 else "Studied English last night"
if prediction[0] == 1:
    print(weather, temp, dating_desc, "宜工作")
else:
    print(weather, temp, dating_desc, "诸事不宜")
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/20250309123941.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

## Adding
