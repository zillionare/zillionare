---
title: "第42个因子:年化17.6%，15年累计10倍"
date: 2024-10-18
category: factor&strategy
slug: alpha042
motto: 俟河之清 人寿几何
img: https://images.jieyu.ai/images/university/Free-University-tibilisi.webp
stamp_width: 60%
stamp_height: 60%
tags: [factor,alpha101,alpha]
---

![题图：第比利斯自由大学，Kahushadze在此任教](https://images.jieyu.ai/images/university/Free-University-tibilisi.webp)

《101个公式化因子》是Zura Kahushadze于2015年发表的paper。在这篇paper中，他拿出了在worldquant广泛使用的因子中，便于公式化的因子（约80个），加上其它自创因子，共101个，集结发表在预印论文网站arXiv上。

这一paper甫一发表，便引起业界关注。现在，Alpha101因子已成为国内机构广泛使用的付费因子。但是，Alpha101因子中的公式比较晦涩难懂，使用了自定义的算子、大量魔术数字和数不清的括号嵌套，让无数人不得不从入门到放弃。

---

然而，如果你因此放弃Alpha101，不能不说是巨大的损失。比如，我们近期对第42个因子进行了回测，发现它在A股有相当好的表现。

!!! info
    回测使用2008年到2022年的数据，随机抽取2000支个股参与回测。考虑到2018年A股才1800支个股左右，这一回测在2018年前几乎是全覆盖。具有很强的代表性。

回测结果表明，这一因子的年代收益达到16.1%， 累计收益达到7倍（15年）。

![](https://images.jieyu.ai/images/2024/10/alpha042-alpha-beta.png)

![](https://images.jieyu.ai/images/2024/10/alpha042-cumulative-return.png)

---

不过，驾驭Alpha101并不容易。不得不说，它的公式有点晦涩难懂，比如第29号因子，它的公式如下：


```python
(min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1),
5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))
```

这只是Alpha101中中等阅读难度的因子。如果我们把它展开，相当于：

```python
(
    min(
        product(
            rank(
                rank(
                    scale(
                        log(
                            sum(
                                ts_min(
                                    rank(rank((-1 * rank(delta((close - 1), 5))))), 2
                                ),
                                1,
                            )
                        )
                    )
                )
            ),
            1,
        ),
        5,
    )
    + ts_rank(delay((-1 * returns), 6), 5)
)
```

---

不仅是了解其含义非常困难，就是实现它也不是件容易的事。而且，Alpha101中还存在大量待优化的部分，以及少部分错误（对于一篇免费、公开的文章，仍然是相当宝贵的资源）。比如，对于42号因子，它仍然有改进空间。这是我们改进后的因子表现（同等条件下，源码仅对学员开放）：

![](https://images.jieyu.ai/images/2024/10/alpha042-refactored-returns.png)

我们看到，年化alpha有了1.5%的上涨。而下面这张分层收益图，懂行的人一看就知道，简直是完美。西蒙斯所谓追随美的指引，应该就是指的这种图了。

![](https://images.jieyu.ai/images/2024/10/alpha042-refactor-quantile.png)

---

累积收益图也很完美。A股2008年触顶6124之后，持续下跌数年，但这期间此因子的收益仍然保持上涨。

![](https://images.jieyu.ai/images/2024/10/alpha042-refactor-culmulative-return.png)


不过，Alpha101确实很难懂。比如公式001看起来并不复杂：

```python
(rank(Ts_ArgMax(SignedPower((
    (returns < 0) ? stddev(returns, 20) : close), 2.)
    , 5)) -0.5)
```

但它却做了许多无用操作。它实际上是对现价对近期高点的距离排序，你看明白了吗？所以，这个因子到底有没有效呢？在什么情况下，它会出现出人意料的表现呢？

还有，像这样的因子，从公式到代码，再到结合数据进行因子检验，又该如何操作呢？如果你感兴趣，快来加入我们一起学习吧！
