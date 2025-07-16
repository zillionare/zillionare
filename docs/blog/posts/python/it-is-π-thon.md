---
title: "π-thon以及他的朋友们"
date: 2025-07-15
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/meme/π-thon.png
category: python
motto: 相信自己能做到，你就已经成功了一半
desc: 在6月中旬，Python发布了Python 3.14 beta3。它可不是一个普通的预发布版本 -- 它是第一个正式支持期待已久的自由线程或『无 GIL』的版本。而有没有GIL，绝对是Python发展史上的有一个分水岭。
seq: 宽粉读研报
lunar:
tags: 
    - quantlib
    - python
    - numpy
    - scikit-learn
---



最近的Python社区热闹异常。

在6月中旬，Python发布了Python 3.14 beta3。它可不是一个普通的预发布版本 -- 它是第一个正式支持期待已久的自由线程或『无 GIL』的版本。而有没有GIL，绝对是Python发展史上的有一个分水岭。

这个版本将在今年的程序员节（10月24日）发布，版本号正是神奇的数字π。

---

## No Gil, No!

Python程序员苦GIL久矣。正是因为GIL的限制，Python的多线程一直只是个银样蜡枪头，无论你的笔记本电脑性能多么强大，Python的多线程程序永远都是一核有难，多核围观 -- 它们永远只会使用一个核。

!!! tip
    移除GIL并非没有代价。它会使Python的单线程性能下降10%左右 -- 但在 apple arm下，仅下降3%左右 -- 同时可能使内存开销上升20%。很快，我们将看到这样的文化衫出售： 我站GIL!

## Numpy 2.3

Numpy是最重要的Python库之一。它刚刚在7月12发布了最新的2.3版本，以适配最新的Python 3.14的Free-thread特性。不过，我们测试了一下，不要指望这个版本的Numpy，即使运行在Python 3.14下，能带来多大的性能提升。Numpy很早就是GIL-Free的了，所以，当你通过ThreadPoolExecuter提交一个基于Numpy的计算任务时，在很久以前，这个线程池就能有效地利用你的多核CPU了。所以，这一版的Numpy，在free-thread上面，主要是增强兼容性。

所以，对量化研究员来说，可能π-thon并不会立即提升你程序的运行效率--如果你之前已经充分利用了numpy、pandas、polars、duckdb等高性能库的向量化运算的话。

π-thon对性能的真正提升，可能会体现在像Django这样的web应用程序上。它们往往都是纯粹的Python代码，一直以来受到GIL的束缚，为了提高性能，这些Web框架常常不得不设计为多进程的--但这样也带来了一些性能上的额外开销。

## scikit-learn, 现在支持GPU啦

另一个值得关注的发布是scikit-learn的1.7版本，这个发布也在最近。现在可以使用CuPy或者Pytorch的张量作为数据输入，并且在GPU上运行。当然，这个版本的发布，也是在宣告，作为Python社区重要的一员，scikit-learn现在也是free-thread ready!

不过，scikit-learn上没有太复杂的模型，感觉用不用GPU和多线程，训练都很快。

## Ruff 0.12

如果你是一名严肃的开发者，那么很可能使用过各种lint工具了，也应该吐槽过Black, Flake8, isort, ...等等工具的速度。现在流行将所有的工具都有rust重写一篇，所以，这些工具现在也被重写了。这就是Ruff的目标。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/Ruff_v_0_12_0_header.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

除了Ruff之外，被Rust重写的工具还有uv（计划替代poetyr/piptools），Pyrefly(代替mypy和pyright)。这些项目表明，2025 年可能会被铭记为 Rust 中的 Python 工具不再是新鲜事物而成为必备工具的一年。

不过，它的版本还是如此之低，似乎我们可以悠着点，先让其它人踩坑。毕竟。如果Ruff错报的话，花时间去修复一个错误的报告，会是一个不可容忍的错误。


