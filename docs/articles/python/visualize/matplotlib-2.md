---
title: matplotlib的布局问题（2）
slug: layout-of-matplotlib-2
---

上一期文章介绍了如何使用 GridSpect 来进行布局。当我们使用 GridSpec 布局时，一般是为了创建较复杂的布局，比如异形网格。这种情况下，我们往往是先生成若干小的网格，再通过 span 来合并网格，以生成异形网格。

这是一种自底向上的方法，即由小的网格生成大的网格。

这篇笔记我们将介绍另一种自顶向下的方法，即先生成大的网格，再通过 subgridspec，在这些网格中，进一步切分出小的网格。

## 自顶向下 - subgridspec

```python
import matplotlib.pyplot as plt

def my_text(name):
    exec(
        name
        + ".text(0.5, 0.5, name, ha='center', "\
        "va='center', fontsize=16, color='darkgrey')"
    )

fig = plt.figure(constrained_layout=True)

# 生成一行两列的等面积网格
gs = fig.add_gridspec(1, 2)

# 将第一个网格再划分成 2 * 2 的单元格
gs_left = gs[0].subgridspec(2, 2)

# 将第二个网格再划分成 3 * 1 的单元格
gs_right = gs[1].subgridspec(3, 1)

for a in range(2):
    for b in range(2):
        exec(f"ax{a}{b} = fig.add_subplot(gs_left[{a},{b}])")
        my_text(f"ax{a}{b}")

for a in range(3):
    exec(f"ax{a} = fig.add_subplot(gs_right[{a}])")
    my_text(f"ax{a}")

# 增加 FIGURE-LEVEL 的标题
_ = fig.suptitle("nested gridspecs")
```
这种方法较之上一篇中使用的方法，似乎更为优雅和符合直觉。

## 神奇的 Mosaic

对于密集、均匀的网格，我们有 Figure.subplots；对于更复杂的布局，我们可以使用 Gridspec + 单元格合并，或者本篇讲的 subgridspec 方法来创建网格。

但是，我们仍然要记住我们是如何合并这些单元格的，以及记住合并后的单元格 (Axes 对象）的索引。

subplot_mosaic 提供了一个直观地、语义化布局和命名 Axes 的方法。这种方法作为 Grid 布局中的一种，正在 R，Web 等多个地方流行。

subplot_mosaic 函数提供了一种优雅且可读的方式来创建复杂的子图排列。我们不用从数字角度考虑子图网格，而是根据布局模式来考虑它们。我们提供一个表示为字符串列表列表的可视化布局，其中每个字符串代表一个子图。每个唯一的字符串对应一个唯一的子图，而布局中重复的字符串将创建跨越重复位置的更大的子图。

我们通过一个例子来理解它：

```python
import numpy as np

# 用来标识子图对象 (AXES)
def identify_axes(ax_dict, fontsize=48):
    kw = dict(ha="center", va="center", fontsize=fontsize, color="darkgrey")
    for k, ax in ax_dict.items():
        ax.text(0.5, 0.5, k, transform=ax.transAxes, **kw)

fig = plt.figure(layout="constrained")
np.random.seed(19680801)
hist_data = np.random.randn(1_500)
ax_dict = fig.subplot_mosaic(
    [
        ["bar", "plot"],
        ["hist", "image"],
    ],
)
ax_dict["bar"].bar(["a", "b", "c"], [5, 7, 9])
ax_dict["plot"].plot([1, 2, 3])
ax_dict["hist"].hist(hist_data)
ax_dict["image"].imshow([[1, 2], [2, 1]])

# 把 AXES 名字标记在子图上
identify_axes(ax_dict)
```

![50%]](https://images.jieyu.ai/images/2023/07/promo-pyvisual-matplot-2-1.png)

这个方法的优美之处在于，我们在创建每个子图时，就给了它们一个名字，后面绘图（第 12 到第 15 行）时，可以直接使用名字来引用这些子图。

在定义网格时，我们使用了一个 2*2 的字符串数组来表示要生成一个 2*2 的网格，这也很符合直觉。

更有趣的是，我们甚至可以嫌弃数组定义过于繁复：

```python
mosaic = "AB;CD"
fig = plt.figure(layout="constrained")
ax_dict = fig.subplot_mosaic(mosaic)

identify_axes(ax_dict)
```

这里我们定义 ABCD 4 个子图，仅仅是通过 mosaic = "AB;CD"就完成了指定。

![50%]](https://images.jieyu.ai/images/2023/07/promotion-mosaic-abcd.png)

如果我们把 mosaic 指定为这样：
```
"""
ABD
CCD
"""
```
应该很容易猜到这将生成什么样的网格布局。我们通过代码演示一下：

```python
axd = plt.figure(layout="constrained").subplot_mosaic(
    """
    ABD
    CCD
    """
)

axd["A"].bar(["a", "b", "c"], [5, 7, 9])
axd["C"].plot([1,2,3])
identify_axes(axd)
```

对 Axes 的引用非常直观，我们直接使用 axd["A"] 或者 axd["C"] 即可。

![50%]](https://images.jieyu.ai/images/2023/07/promotion-mosaic-abdccd.png)

如果我们需要一些更怪异的布局，比如，在某个位置上，我们想留空：

```
    A.C
    BBB
    .D.
    """
```

使用"."的地方将会留空。这将生成下图：

![50%]](https://images.jieyu.ai/images/2023/07/promo-pyvis-matplot-4.png)

上面我们生成的都是均匀长度的子图（在合并之前）。subplot_mosaic 接受 gridspec_kw 参数：

```python
axd = fig.subplot_mosaic(
    mosaic,
    gridspec_kw={
        "bottom": 0.05,
        "top": 0.75,
        "left": 0.6,
        "right": 0.95,
        "wspace": 0.5,
        "hspace": 0.5,
    },
)
```

也许我们还怀念 subgridspec 那种自顶向下的创建方式--没问题，subplot_mosaic 支持嵌套：

```python
inner = [
    ["inner A"],
    ["inner B"],
]

# 在这里我们把 INNER 网格嵌套进来了
outer_nested_mosaic = [
    ["main", inner],
    ["bottom", "bottom"],
]
axd = plt.figure(layout="constrained").subplot_mosaic(
    outer_nested_mosaic, empty_sentinel=None
)
identify_axes(axd, fontsize=36)
```

![50%]](https://images.jieyu.ai/images/2023/07/promo-pyvis-matplot-2-5.png)

好，看完这一期文章，你应该完全精通 matplotlib 的布局了！
