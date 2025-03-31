---
title: Pandas核心语法[7]
series: 量化人的 Numpy 和 Pandas
seq: "7"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-17
date: 2025-04-03
category: tools
motto: Perseverance is not a long race; it is many short races one after the other.
img: https://images.jieyu.ai/images/hot/mybook/women-sweatshirt-indoor.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“Pandas 的 DataFrame 提供了强大的样式功能，可以通过 Styler 对象实现类似 Excel 的条件着色效果。此外，Pandas 内置的绘图方法支持多种图表类型，轻松满足数据可视化需求。”

---

## 1. 表格和样式
Pandas 的 DataFrame 提供了强大的样式功能，可以通过 Styler 对象实现类似 Excel 的条件着色效果。以下是关键方法和示例：

### 1.1. ​基础样式设置
通过 DataFrame.style 访问样式功能，支持链式调用：

```python
df.style.set_caption("标题").set_properties(**{'background-color': 'lightgray'})
```

![50%](https://images.jieyu.ai/images/2025/03/070.png)

### 1.2. ​条件着色
### 1.2.1. 单列条件着色

---

```python
def color_negative_red(val):
    color = 'red' if val < 0.2 else 'black'
    return f'color: {color}'
df.style.applymap(color_negative_red)
```

![50%](https://images.jieyu.ai/images/2025/03/071.png)

### 1.2.2. 多列条件着色
```python
df.style.apply(lambda x: ['background: yellow' if v > 0.2 else '' for v in x], 
                        subset=['A', 'C'])
```

![50%](https://images.jieyu.ai/images/2025/03/072.png)

### 1.2.3. ​极值高亮

---

```python
df.style.highlight_max(color='lightgreen').highlight_min(color='pink')
```

![50%](https://images.jieyu.ai/images/2025/03/073.png)


### 1.2.4. 渐变色背景
```python
df.style.background_gradient(cmap='Blues', subset=['B'])
```

![50%](https://images.jieyu.ai/images/2025/03/074.png)

### 1.2.5. 条形图样式
```python
df.style.bar(subset=['C'], color='#5fba7d')
```

![50%](https://images.jieyu.ai/images/2025/03/075.png)

---

### 1.2.6. 自定义表格样式
```python
headers = {'selector': 'th',
    'props': 'background-color: #5e17eb; color: white;'}
df.style.set_table_styles([headers])
```

![50%](https://images.jieyu.ai/images/2025/03/076.png)

### 1.2.7. 动态条件着色（复杂逻辑）​
```python
def highlight_risk(row):
    # 当A列>90且B列<50时标黄
    return ['background: yellow' if (row['A']>0.3) & 
    (row['B']<0.5) else '' for _ in row]  # 返回与行等长的样式列表
df.style.apply(highlight_risk, axis=1)  # axis=1表示按行处理
```

![50%](https://images.jieyu.ai/images/2025/03/077.png)

!!! Notes
    - 样式仅在 Jupyter Notebook 或导出为 HTML 时生效，不支持直接修改原始数据。
    - 使用 subset 参数可限定着色范围。
    - 渐变色 (background_gradient) 支持调整色域范围 (low=0.2, high=0.8)。

---

## 2. Pandas 内置绘图功能
在 pandas 中，我们可能有多列数据，还有行标签和列标签。pandas 自身就有内置的方法，用于简化从 DataFrame 和 Series 绘制图形。

### 2.1. 线形图
Series 和 DataFrame 都有一个 plot 属性，用于绘制基本图表。默认情况下，plot() 生成的是线形图。

```python
s = pd.Series(np.random.standard_normal(10).cumsum(), index=np.arange(0, 100, 10))
s.plot()
```

![50%](https://images.jieyu.ai/images/2025/03/065.png)

---

该 Series 对象的索引会被传给matplotlib，并用于绘制 x 轴。可以通过 use_index=False 来禁用索引。x 轴的刻度和界限可以通过 xtick 和 xlim 选项进行调节，y 轴用 yticks 和 ylim 调节。plot 参数的部分列表参见下表：

| 参数          | 说明                                                                 |
|---------------|--------------------------------------------------------------------|
| alpha       | 图形填充透明度（0~1 之间）                                      |
| ax          | matplotlib 的 Axes 对象，默认为当前 Axes (gca())          |
| colormap    | 指定颜色映射（如 'viridis'）                                  |
| figsize     | 图像尺寸，格式为 (宽度, 高度)（单位：英寸）                    |
| fontsize    | 刻度标签字体大小                                            |
| grid        | 是否显示网格线（默认为 None，遵循 matplotlib 默认样式）    |
| kind        | 图形类型，可选：'line'（折线图，默认）、'bar'（柱状图）、'barh'（横向柱状图）、'hist'（直方图）、'box'（箱线图）、'kde'/'density'（核密度估计）、'area'（面积图）、'pie'（饼图） |
| label       | 图例标签名称                                                |
| legend      | 是否显示图例（默认为 False）                              |
| logx/logy | 是否对 x/y 轴使用对数刻度（默认为 False）                 |
| loglog      | 是否对 x/y 轴同时使用对数刻度                               |
| position    | 柱状图的柱子位置（需避免与 kind='bar' 冲突）                  |
| rot         | 刻度标签旋转角度（如 45 表示 45 度）                      |
| secondary_y | 是否使用右侧的第二个 y 轴（默认为 False）                 |
| style       | 线条样式（如 'k--' 表示黑色虚线）                         |
| table       | 是否在图表下方显示数据表格（默认为 False）                |
| title       | 图表标题（字符串）                                          |
| use_index   | 是否使用 Series 的索引作为 x 轴刻度标签（默认为 True）     |
| xerr/yerr | 为柱状图添加误差线                                          |
| xlim/ylim | 设置 x/y 轴显示范围（格式：(min, max)）                   |
| xticks/yticks | 自定义 x/y 轴刻度值（列表）                            |
| **kwds      | 其他 matplotlib 绘图参数（如 color='red'）                |

---

pandas 的大部分绘图方法都接收一个可选的 ax 参数，它可以是 matplotlib 的子图对象，这使你能够在网格布局中更为灵活地处理子图的位置。

DataFrame 的 plot 方法将各个列绘制成同一子图中的线，并自动创建图例。

```python
df = pd.DataFrame(np.random.standard_normal((10, 4)).cumsum(0),
                  columns=['A', 'B', 'C', 'D'],
                  index=np.arange(0, 100, 10))
plt.style.use('grayscale')
df.plot()
```

![50%](https://images.jieyu.ai/images/2025/03/066.png)

!!! Notes
    这里使用了 plt.style.use('grayscale') 将配色模式设置为灰度模式。

对于不同的绘图类型，plot 属性包含很多方法。例如，df.plot() 等价于 df.plot.line()。

---

!!! Notes
    plot 的额外关键字参数会传递给相应的 matplotlib 绘图函数，所以要更进一步自定义图表，就必须学习更多有关matplotlib API的知识。

DataFrame 还有一些用于对列进行灵活处理的选项。例如：要将所有列都绘制到同一个子图中还是分别创建各自的子图。下表展示了专属于DataFrame的plot参数：

| 参数          | 说明                                                                 |
|---------------|--------------------------------------------------------------------|
| subplots    | 是否为每一列数据创建子图，默认为 False                          |
| sharex      | 如果 subplots=True，是否共享 x 轴，默认为 True（当 ax=None 时） |
| sharey      | 如果 subplots=True，是否共享 y 轴，默认为 False               |
| layout      | 子图的行列布局，格式为 (rows, columns)                          |
| legend     | 添加子图图例（默认为True）                    |
| sort_columns| 是否按列名排序，默认为 False                                    |

### 2.2. 柱状图
plot.bar() 和 plot.barh() 分别用于绘制水平柱状图和垂直柱状图。对于柱状图，Series 或 DataFrame 的索引将被用作x轴（bar）或y轴（barh）的刻度。

```python
fig, axes = plt.subplots(2,1)
data = pd.Series(np.random.uniform(size=16), index=list('abcdefghijklmnop'))
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.barh(ax=axes[1], color='k', alpha=0.7)
```

---

![50%](https://images.jieyu.ai/images/2025/03/067.png)

对于 DataFrame，柱状图会将每一行的值分为一组，并排显示。

```python
df = pd.DataFrame(np.random.uniform(size=(6, 4)),
        index=["one", "two", "three", "four", "five", "six"],
        columns=pd.Index(["A", "B", "C", "D"], name="Genus"))
df.plot.bar()
```

![50%](https://images.jieyu.ai/images/2025/03/068.png)

注意，DataFrame 各列的名称“Genus”被用作图例标题。

---

传入stacked=True即可为DataFrame生成堆积柱状图，这样每行的值就会水平堆积在一起。

```python
df.plot.bar(stacked=True,alpha=0.5)
```

![50%](https://images.jieyu.ai/images/2025/03/069.png)



