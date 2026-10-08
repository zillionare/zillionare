---
title: "Mastering Matplotlib Layouts: Subgridspec and Mosaic"
date: "2026-10-09"
slug: en/articles/python/visualize/matplotlib-2
tags: [Matplotlib, Data Visualization, Python, Plotting]
excerpt: "Learn advanced matplotlib layout techniques using subgridspec and subplot_mosaic. This guide covers top-down grid creation, semantic axis naming, and complex nested layouts for precise figure design."
lang: en
translation_of: articles/python/visualize/matplotlib-2
auto_translated: true
source_sha: 37b70e1b139d386c3545e1a77944314348b934f5
---

The previous article introduced how to use `GridSpec` for layout. When using `GridSpec`, the goal is typically to create complex layouts, such as irregular grids. In these cases, we usually generate several small grids first and then merge them using `span` to form the irregular structure.

This is a bottom-up approach, where small grids are combined to form larger ones.

In this note, we will introduce another approach: top-down. This method starts by creating large grids and then uses `subgridspec` to further divide them into smaller grids.

## Top-Down Approach: Subgridspec

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
This method appears more elegant and intuitive compared to the approach used in the previous article.

## The Magic of Mosaic

For dense, uniform grids, we use `Figure.subplots`. For more complex layouts, we can use `GridSpec` with cell merging or the `subgridspec` method discussed in this article.

However, we still need to remember how we merged these cells and keep track of the indices of the merged cells (Axes objects).

`subplot_mosaic` provides an intuitive, semantic way to layout and name Axes. As a type of Grid layout, it is gaining popularity in R, Web development, and other areas.

The `subplot_mosaic` function offers an elegant and readable way to create complex subplot arrangements. Instead of thinking about subplot grids numerically, we consider them based on layout patterns. We provide a visual layout represented as a list of lists of strings, where each string represents a subplot. Each unique string corresponds to a unique subplot, while repeated strings in the layout create larger subplots spanning those repeated positions.

Let’s understand this with an example:

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

![50%]](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/promo-pyvisual-matplot-2-1.png)

The elegance of this method lies in the fact that we assign names to each subplot when creating them. Later, during plotting (lines 12 to 15), we can directly reference these subplots by name.

When defining the grid, we used a 2x2 string array to indicate the generation of a 2x2 grid, which is also quite intuitive.

More interestingly, we can even find the array definition too verbose:

```python
mosaic = "AB;CD"
fig = plt.figure(layout="constrained")
ax_dict = fig.subplot_mosaic(mosaic)

identify_axes(ax_dict)
```

Here, we define four subplots (A, B, C, D) simply by setting `mosaic = "AB;CD"`.

![50%]](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/promotion-mosaic-abcd.png)

If we specify the mosaic as follows:
```
"""
ABD
CCD
"""
```
It should be easy to guess what kind of grid layout this will generate. Let’s demonstrate it with code:

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

Referencing the Axes is very intuitive; we can directly use `axd["A"]` or `axd["C"]`.

![50%]](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/promotion-mosaic-abdccd.png)

If we need some more unusual layouts, such as leaving a position empty:

```
    A.C
    BBB
    .D.
    """
```

Using "." in the layout will leave that area empty. This will generate the following figure:

![50%]](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/promo-pyvis-matplot-4.png)

The subplots we generated above were of uniform length (before merging). `subplot_mosaic` accepts the `gridspec_kw` parameter:

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

Perhaps you still miss the top-down creation style of `subgridspec`—no problem, `subplot_mosaic` supports nesting:

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

![50%]](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/promo-pyvis-matplot-2-5.png)

After reading this article, you should have mastered matplotlib layouts!
