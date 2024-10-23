---
title: 10 月 24 日，庆祝码农节！Python 刚刚发布了 3.13 版本
date: 2024-10-24
category: python
slug: python-release-3.13
motto: 
img: https://images.jieyu.ai/images/2024/10/python-3.13.png
stamp_width: 60%
stamp_height: 60%
tags: []
---

![](https://images.jieyu.ai/images/2024/10/python-3.13.png)

今天（10 月 24 日）是码农节。这一天也是裘伯君、Chris Lattner, Robert Khan 等人的生日。Lattner 是 LLVM 开源编译器的创始人、Swift 和 Mojo 语言的主要设计者。Khan 是互联网奠基人之一，他与温顿。瑟夫共同发明了 TCP/IP 协议。

不过，最令程序员兴奋的是，Python 3.13 正式版本发布了！

这个版本的重点是，引入了一个新的交互式解释器，并且对自由线程模型（PEP 703）和即时编译器（PEP 744）提供了实验性支持。这是 Python 程序员多少年以来，翘首以盼的性能改进！

## REPL

新的交互式解释器这一功能可能会引起误解。它实际上指的是一个新的交互式 shell，而不是语言解释器本身。这个新的 shell 来自于 PyPy 项目。这个解释器支持彩色输出、多行编辑、历史回顾和多行粘贴模式。

![Lattner 和 Mojo 语言。Mojo 号称比 Python 快 6.8 万倍](https://images.jieyu.ai/images/2024/10/chris-lattner.png)

Python 的交互式 shell 一直是它的特色和优势，想了解一个函数的功能和用法，直接在终端中输入 ipython 之后，就可以立即尝试这个函数。我是常常拿 ipython 当计算器使用，特别方便。

## JIT

从 3.11 起，Python 开始引进 JIT 的一些特性。在 Python 3.11 版本中，当解释器检测到某些操作涉及的类型总是相同的时候，这些操作就会被“专门化”，替换成特别的字节码，这使得代码中这部分区域的运行速度提升 10%到 25%。到了 3.13 版本，它已经能在运行时生成实际的机器代码，而不仅仅是专门的字节码。现在，提速还不是很明显，但为未来的优化铺平了道路。

不过，目前 JIT 还被认为是实验性的，默认情况下未启用。CPython 团队还在观察它对整个社区的影响，一旦成熟，就会成为默认选项。

## Free Threaded CPython

![Robert Kahn，互联网之父](https://images.jieyu.ai/images/2024/10/robert-kahn.png)

之前大家讨论很久的无 GIL 版本，现在官方名称确定为 Free Threaded CPython。在这个版本下，CPython 允许线程完全并行运行。这将立刻**数倍**提升 Python 的性能。不过，目前该功能也是实验性的。

要启用这两个实验性的功能，你需要自己从源代码编译 CPython。同样地，这已经让人看到了曙光。而且，这个等待时间并不会太长，这些功能已经在 Meta 内部广泛使用了。

## 其它性能优化

这一版在 Windows 上，将提供精度为 1 微秒的计时器，而不再是过去精度只有 15.6 毫秒的时钟。这一变化将使得 Python 在 Windows 上将能执行一些实时任务。

之前 typing 库的部分模块会导致导入时间过长，现在，这个时间已减少了大约 1/3。当然，我们平常可能感受不出来，但如果你的程序会启动子进程来执行一些简短的计算密集型任务的话，这个区别就比较大了。

说到子进程，subprocess 现在会更多地使用 posix_spawn 函数创建子进程，这将带来一些性能上的提升。

## 弃用版本管理

在 Python 中，弃用版本管理一直是通过第三方库来实现的。现在，这一特性终于被内置了：

```python
from warnings import deprecated
from typing import overload

@deprecated("Use B instead")
class A:
    pass

@deprecated("Use g instead")
def f():
    pass

@overload
@deprecated("int support is deprecated")
def g(x: int) -> int: ...
@overload
def g(x: str) -> int: ...
```

不过，第三方库 deprecation 似乎仍然在功能上更胜一筹。这是 deprecation 的用法：

```python
from deprecation import deprecated

@deprecated("2.0.0", details="use function `bar` instead")
def foo(*args):
    pass
```

## 你就是列文。虎克！

这是网上的一个梗，说的是有些人看图特别仔细，拿着显微镜找 bug。列文。虎克就是发明显微镜的人。10月24日也是他的生日。

![](https://images.jieyu.ai/images/2024/10/abstract-raindrop.jpg)

列文。虎克裁缝学徒出身，没受过正规教育。后来成为一名布匹商，为了检验布匹的质量，他购买了放大镜来观察布匹的纤维，也由此开启了他的大国工匠之路（17 世纪的荷兰的确是大国。世界上的第一个证券交易所 -- 资本主义的标志，就诞生在 17 世纪的荷兰）。

列文。虎克没有受过正规训练，凭着兴趣和热爱，发明了显微镜，为人类打开了从未见过的世界。他的成就最终被英国皇家学会接受，在 1680 年当选为皇家学会成员。终其一生，他为这个世界留下的，除了他自己的名字，还有 cell 这个词。

“我总是尽力做到最好，即使是最小的事物也值得认真对待”。正是凭着这种信仰，他才得以见微知著，于一粒沙中发现宇宙。
