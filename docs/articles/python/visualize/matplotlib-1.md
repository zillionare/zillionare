---
title: matplotlib的布局问题（1）
---

这一篇笔记，我们来介绍matplotlib中的布局概念。

matplotlib中的布局，主要涉及到GridSpec, layout以及相关的函数构成。

在matplotlib中，除了像我们上一篇笔记指出的那样，直接通过`fig.add_axes`方法进行子图的定位外，一般采用网格定位。即通过subplots中的nrows/ncols方法指定有多少个等长（宽）的网格，或者通过gridspec指定网格的规格。

指定等长网格的比较简单，我们看看如何通过gridspec来创建更复杂一些的网格：

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def annotate_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)


fig = plt.figure(facecolor='0.8')

fig.suptitle("Controlling spacing around and between subplots")

gs1 = GridSpec(3, 3, left=0.3, right=0.48, wspace=0.05)
ax1 = fig.add_subplot(gs1[:-1, :])
ax2 = fig.add_subplot(gs1[-1, :-1])
ax3 = fig.add_subplot(gs1[-1, -1])

gs2 = GridSpec(3, 3, left=0.55, right=0.98, hspace=0.05)
print("gs2 is:", gs2[:, :-1])

ax4 = fig.add_subplot(gs2[:, :-1])
ax5 = fig.add_subplot(gs2[:-1, -1])
ax6 = fig.add_subplot(gs2[-1, -1])

annotate_axes(fig)

def show_grid(gs, pos):
    # Get the grid positions
    bottoms, tops, lefts, rights = gs.get_grid_positions(plt.gcf())

    ax = plt.axes([0,0,1,1], facecolor=(1,1,1,0))

    vlines = sorted([*lefts, *rights])
    for x in vlines:
        ax.axvline(x, ls='-', lw=1, ymin=min(bottoms), ymax=max(tops))

    hlines = sorted([*bottoms, *tops])
    for y in hlines:
        ax.axhline(y, ls='-', lw=1, xmin=min(lefts), xmax=max(rights))

show_grid(gs1, [0.3, 0, 0.48, 1])
show_grid(gs2, [0.55,0, 0.98, 1])

plt.show()
```
这段代码中，我们先通过GridSpec创建了两个3*3的网格，一左一右，然后通过add_subplot创建了6个子图，在创建时，将gridspec传入。

在创建子图，我们通过给子图绑定到不同的网格，实现了类似excel中的单元格合并的效果，从而实现了异形网格。

![50%](https://images.jieyu.ai/images/2023/07/using_grid_spec.png?2))

这段代码展示了非常多的绘图技巧，值得好好研究。

首先，每个Gridspec可以指定它们在Figure中的位置和大小。比如，这里的gs1就是从x轴的0.3到0.48处（占据了全部高度，因为没有指定）。

其次，我们为了显示每个网格（即每个3*3的小格子）是如何分配到每个ax的，我们将这些格子进行了描边。

因此，从上图可以看出，1~6的小网格都分配给了ax1，这是由代码gs[:-1,:]来指定的。gs[:-1,:]意味着把直到最后一行（不
<!--page-->
包括）的所有列对应的网格都分配给ax1,也就是前6个网格。关于如何阅读切片，在我们课程第9讲中有详细说明，并且给出了绘图。

对ax2，分配的是gs1[-1,:-1]，这意味着是把最后一行，直到最后一列的所有grid都分配给它，这对应着两个小的单元格，即7和8号单元格。

最后，ax3分到最后的单元格，gs1[-1,-1]。

对gs2，逻辑类似。ax4得到了gs2[:,:-1]，这意味着所有行的前两列都分配给了ax4；ax5则是得到了最后一列的前两行；ax6得到了gs2[-1,-1]。

**注意这里还有一个技巧**，即在绘制网格线时，我们是通过新建的ax来进行绘制的。这是因为，我们的绘制应该发生成figure级别上（因为要跨越不同的axes），但是，figure并没有相应的绘制直线的方法（figure有哪些方法，在课程一开始有介绍），因此，我们必须增加一个与Figure同等大小的ax：
```python
ax = plt.axes([0,0,1,1], facecolor=(1,1,1,0))
```
通过它来绘制这些网格线。

这里介绍的方法和原理都是比较偏底层的，属于matplotlib的高
<!--page-->
级绘制技巧，掌握了这些技巧和原理，就算是精通了matplotlib。

***绘图不仅仅是创造美丽的可视化效果，更是为了释放数据的全部潜力，并揭示原本隐藏的insights，它是数字语言和故事语言之间的桥梁，使得个人和组织能够做出明智的决策，并创造有意义的变革***

本笔记是《Python数据分析可视化》的一部分。全系列将像本笔记一样，通过详尽的图示、可运行的代码，深入浅出地讲解Python中的绘图原理和技巧，包括：

## matplotlib 

![](https://images.jieyu.ai/images/2023/07/matplotlib.png)

主要介绍绘图领域的基础知识，包括图的构成、布局、颜色、坐标等基础概念。

<!--page-->
## plotly 

plotly是一个高级绘图工具，它可以创建交互式绘图甚至动画！这一部分我们还将介绍Dash，学会后，你也可以仅仅通过Dash，就完成一个能绘制精美图形，并与用户交互的网站应用。

![](https://images.jieyu.ai/images/2023/07/plotly.png)

<!--page-->
### seaborn 
seaborn是基于matplotlib的高级绘图库，它屏蔽了matplotlib中的大部分绘图细节，让你聚焦于探索数据之间的联系与语义！

![75%](https://images.jieyu.ai/images/2023/07/seaborn.png)

## PyEcharts 

![75%](https://images.jieyu.ai/images/2023/07/echarts.png)

<!--page-->
这是国人贡献出来的一个Apache顶级库，类似于plotly，也可以生成交互式绘图。
