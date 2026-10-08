---
title: "Python 3.13 Released: Free Threading, JIT, and REPL"
date: 2024-10-24
slug: en/posts/python/python-just-released-3.13
tags: [Python 3.13, Free Threading, JIT Compiler, Quantitative Development]
excerpt: "Python 3.13 introduces experimental free-threading, JIT compilation, and a new REPL. This release marks a major leap in performance and developer experience, aligning with the global celebration of programmers on October 24."
lang: en
translation_of: posts/python/python-just-released-3.13
auto_translated: true
source_sha: 043ac4c4a338a40386e03c6b1a861834ce252937
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/python-3.13.png"
---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/python-3.13.png)

Today, October 24, is celebrated globally as Programmers’ Day. It also marks the birthdays of notable figures such as Bo Qiu Jun, Chris Lattner, and Robert Kahn. Lattner is the founder of the LLVM open-source compiler and the primary designer of Swift and Mojo. Kahn, a foundational figure of the internet, co-invented the TCP/IP protocol with Vint Cerf.

However, the most significant news for developers is the official release of **Python 3.13**.

This version introduces a new interactive interpreter and provides experimental support for the free-threaded model (PEP 703) and the Just-In-Time (JIT) compiler (PEP 744). These performance enhancements have been eagerly anticipated by the Python community for years.

## REPL

The term "new interactive interpreter" can be misleading. It refers to a new interactive shell, not the language interpreter itself. This shell is derived from the PyPy project and supports colored output, multi-line editing, history recall, and multi-line paste modes.

![Chris Lattner and the Mojo language. Mojo claims to be 68,000 times faster than Python](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/chris-lattner.png)

Python’s interactive shell has long been one of its key strengths. To explore a function’s capabilities, developers can simply type `ipython` in the terminal to test it immediately. I often use `ipython` as a calculator, which is incredibly convenient.

## JIT

Starting from version 3.11, Python began introducing JIT features. In Python 3.11, when the interpreter detects that certain operations always involve the same types, these operations are "specialized" and replaced with specialized bytecode, improving execution speed in those code regions by 10% to 25%.

In Python 3.13, the JIT compiler can now generate actual machine code at runtime, rather than just specialized bytecode. While the immediate performance gains may not be dramatic, this paves the way for future optimizations.

Currently, JIT is still considered experimental and is disabled by default. The CPython team is monitoring its impact on the broader community. Once mature, it will become the default option.

## Free Threaded CPython

![Robert Kahn, Father of the Internet](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/robert-kahn.png)

The long-discussed version without the Global Interpreter Lock (GIL) has officially been named **Free Threaded CPython**. In this version, CPython allows threads to run completely in parallel, potentially boosting Python’s performance by **several times**. However, this feature is also experimental.

To enable these two experimental features, you must compile CPython from source. Nevertheless, this signals a bright future, and the waiting period is not expected to be long. These features are already widely used internally at Meta.

## Other Performance Optimizations

On Windows, this version introduces a timer with 1-microsecond precision, replacing the previous clock with only 15.6-millisecond precision. This change enables Python to execute real-time tasks on Windows more effectively.

Previously, certain modules in the `typing` library caused excessively long import times. Now, this time has been reduced by approximately one-third. While this may not be noticeable in typical usage, it makes a significant difference if your program spawns subprocesses to perform short, compute-intensive tasks.

Regarding subprocesses, `subprocess` now utilizes the `posix_spawn` function more frequently to create child processes, resulting in performance improvements.

## Deprecation Management

In Python, deprecation management has historically been handled via third-party libraries. This feature is now built into the language:

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

However, the third-party library `deprecation` still appears to offer more robust functionality. Here is how it is used:

```python
from deprecation import deprecated

@deprecated("2.0.0", details="use function `bar` instead")
def foo(*args):
    pass
```

## You Are the Leeuwenhoek!

This is an internet meme referring to individuals who scrutinize images with extreme precision, searching for bugs like using a microscope. Leeuwenhoek, the inventor of the microscope, shares his birthday on October 24.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/abstract-raindrop.jpg)

Leeuwenhoek began as a tailor’s apprentice with no formal education. He later became a draper and purchased magnifying glasses to inspect fabric quality, which sparked his journey as a master craftsman (17th-century Holland was indeed a global power; the world’s first stock exchange, a hallmark of capitalism, was born there).

Without formal training, Leeuwenhoek invented the microscope driven by curiosity and passion, revealing a world previously unseen by humanity. His achievements were eventually recognized by the Royal Society, and he was elected a Fellow in 1680. Throughout his life, he left behind not only his name but also the term "cell."

"I always tried to do the best I could, even the smallest things deserve to be taken seriously." It was this belief that allowed him to see the universe in a grain of sand.
