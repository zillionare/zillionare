---
title: The Battle for a New Dawn<br>量化新基建（四）：Pandas 3.0 
date: 2026-01-19
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/1280px-Oxford_University_Museum_of_Natural_History,_Oxford,_UK_-_Diliff.jpg
excerpt: 深度解析 pandas 3.0 在 2026 年量化技术栈中的核心地位，探讨从 NumPy 到 PyArrow 的架构转型、字符串处理革命、Copy-on-Write 机制以及开发者背后的故事。
categories: tools
tags:
  - pandas
  - Python
  - 量化交易
  - 大数据
  - PyArrow
addons:
  - slidev_themes/addons/slidev-addon-quantide-layout
  - slidev_themes/addons/slidev-addon-mouse-trail-pen
  - slidev_themes/addons/slidev-addon-array
  - slidev_themes/addons/slidev-addon-interactive-table
  - slidev_themes/addons/slidev-addon-card
aspectRatio: 3/4
layout: cover-random-img-portrait
---

在量化技术栈中，可能还从来没有哪一个工具能像 pandas 与量化人的联系如此紧密。我们曾在一篇名为《月亮和 Pandas》的文章中，致敬了 Wes McKinney -- Pandas 的开创者。

今天，在服役近 20 年后，遭无数人质疑 Pandas 廉颇老矣，尚能饭否之时，又一位量化人举起了中兴大旗。

他就是 Patrick Hoefler， Pandas 3.0 核心团队最活跃的成员之一，现任 Citadel 的软件工程师。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/20260119151727.png)

---

在数次延期之后，现在 Pandas 3.0 已进入 RC 阶段，黎明的破晓即将到来。Pandas 3.0 将给量化人带来哪些激动人心的新体验？

## 大象席地而坐

从 2008 年 AQR（全球领先的量化对冲基金 AQR Capital Management）的 Wes McKinney 写下第一行代码至今，pandas 已经陪伴量化人走过了近二十年。

在 2008 年，pandas 凭借对 Excel 和 SQL 逻辑的完美封装，迅速成为了量化研究的标配。它将原本枯燥的向量化计算，变成了优雅的 `df.groupby()` 和 `df.rolling()`。可以说，Pandas 的意义远超一款软件本身，它是某种意义上的『立王者』，正是 Pandas（以及后来的 AI），带领 Python  一步步走上程序语言的巅峰。

---

然而，进入 2020 年代后，随着高频数据、Tick 级别回测以及万亿规模资金的涌入，这头昔日的“大象”开始显得步履蹒跚：
*   **内存“刺客”**：经典的 `BlockManager` 机制在处理混合类型数据时，往往会导致内存占用达到原始数据的 3-10 倍。在 128GB 内存的服务器上，处理 20GB 的 Tick 数据竟然会触发 OOM。
*   **性能困局**：由于底层对 NumPy Object 类型的依赖，处理合约代码、状态标签等字符串数据时，速度慢得令人发指。
*   **并发荒漠**：受限于 Python 的 GIL 和底层架构，pandas 很难原生支持多核并行计算，这在 24 核、32 核 CPU 普及的今天，显得格格不入。

与此同时，Polars、DuckDB 等基于 Rust 或现代 C++ 的工具异军突起。它们没有历史包袱，直接拥抱 Arrow 和并行化。面对后辈的挑战，这被困的大象必须完成一次最惊险的“转身”。

这次转身规划由来以久。最早写入核心规划议程的日期，可以追溯到 2022 年的 PyData Global 大会。

---

3.0 的核心不是「功能迭代」，而是「底层架构革命」—— 把 Pandas 的内部数据存储、类型系统、IO 读写全部从 NumPy 迁移到 Apache PyArrow，解决 NumPy 带来的所有历史痛点。

## 核心革命：从 NumPy 转向 PyArrow

Pandas 3.0 最根本的变化是将底层数据结构从 NumPy 数组全面转向 **PyArrow**。尽管目前在 RC 版本中这仍是一个可选的增强项，但在 2026 年的量化实战中，这将成为默认的技术标准。

### 内存布局：列式存储与缓存一致性
NumPy 数组是为密集数值计算设计的（通常是多维的），而 PyArrow 则是为表格化数据（Tabular Data）和列式存储量身定制的。

转向 PyArrow 将带来以下改进：

---

*   **CPU 指令级优化**：Arrow 的内存布局是“列式”且“连续”的。在量化回测中，当你计算 `df['close'].mean()` 时，CPU 能够一次性将整个收盘价序列加载到高速缓存中，并利用 **SIMD (Single Instruction, Multiple Data)** 指令集在单次时钟周期内处理多个价格。在 NumPy 中，由于 BlockManager 的复杂性，数据在内存中的排列往往不是**绝对连续**的（令人惊讶！）。
*   **零拷贝（Zero-copy）与跨语言协同**：这是量化实战中最令人兴奋的点。Arrow 是一种工业级的内存标准。在 2026 年，如果你用 Rust 写了一个高频因子计算引擎，你可以直接将 pandas 3.0 的内存地址传递给 Rust，中间**不需要任何数据拷贝**。这种“原地共享”的能力，彻底终结了 Python 在数据密集型任务中的性能瓶颈。

### 字符串革命：告别 Object，拥抱 Arrow String
在 3.0 之前，字符串列（合约代码、委托状态）被存储为 Python 的 `Object` 类型。每一个字符串都是堆内存中的独立对象，这导致了严重的性能黑洞。

**为什么 Arrow String 是重大改进？**
从 object 转向 Arrow String 是内存结构的重大转变。

旧版中，一个 100 万行的合约代码列，内存里存的是 100 万个 Python String 对象的指针。而在 3.0 中，所有的字符串内容都被紧凑地存在一个大连续缓冲区里，并配有一个偏移量数组。

---

*   **实测对比**：
    *   **内存占用**：存储 100 万个 6 字符长度的代码，旧版占用约 80MB，3.0 仅需约 12MB。
    *   **计算性能**：执行 `df['symbol'].str.upper()`，3.0 的速度提升了 **30 倍**以上，因为它是在 C 语言层面直接扫描连续内存，而不是在 Python 虚拟机里逐个处理对象。

官方在 3.0 RC 中特别强调，`string` 类型将默认映射到 `string[pyarrow]`。这意味着你不再需要手动转换，系统会自动为你选择性能最优的后端。

除此之外，后端的替换也意味着对 csv 的读取速度的提升。在 Pandas 3.0 之前，读取一个 csv 时：

```python
df = pd.read_csv('large_data.csv')
```

如果你不喜欢读文档，你可能不知道它有一个 engine='pyarrow'的参数，这将大大提升性能。而在 Pandas 3.0 中，你不用记忆这个参数，一切已经是最好的安排。

## Copy-on-Write (CoW)

如果你查看最新的 [pandas 3.0.0 Whatsnew](https://pandas.pydata.org/docs/dev/whatsnew/v3.0.0.html)，你会发现 **Copy-on-Write** 是绝对的主角。这不仅仅是为了性能，更是为了消除语义上的歧义。

---

在旧版本中，视图（View）和副本（Copy）的规则极其模糊。这导致了臭名昭著的 `SettingWithCopyWarning`。
```python
# 旧版中的陷阱
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
subset = df.iloc[0:1]
subset.iloc[0, 0] = 100  # 到底 df 变了吗？
```

在第三行赋值时，无论它是否改变原来的 df 数据，我们都能接受；我们不能接受的是，df 可能变了，也可能没变--这就引入了一个薛定谔式的猫一样的笑话：只有在打开盒子的时候，我们才能确定猫是否还活着。

在旧版中，这取决于 `df` 内部是单一块（Single Block）还是多块（Multi Block）管理。这种不确定性是策略 Bug 的温床。

我们当然不喜欢这种模棱两可的状态。**我们之所以做量化，要的就是确定性--哪怕他是基于概率上的确定**。

---

所以，你在一些底层量化框架（比如 alphalens）中，可以看到无处不在的 df.copy：这都是消除了引用的不确定性，但带来了性能上的损失。

### 3.0 中的确定性与安全感
在 3.0 中，默认开启 CoW 后，规则变得异常清晰：**Dataframe 的任何切片或筛选操作在修改前都是“引用”，而在修改时会自动触发“副本”创建。**
```python
# 3.0 后的行为示例
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = df["a"]  # 这在内存中只是一个轻量级引用，开销几乎为零
df2.iloc[0] = 100  # 只有在这一行，pandas 才会真正执行 Copy 操作
# 结果：df 依然是 [1, 2], df2 变成了 [100, 2]。逻辑完全符合直觉。
```

换句话说，当你使用一个引用变量并修改它的值时，你永远不会改变原始数据。在你尝试改变引用变量的数据时，引用变量会自动拷贝一个副本出来。这是操作系统在几十年前就使用了的内存共享技术。

---

你再也不需要 `df.copy()`！

## 向声明式迈进
在 3.0 RC 中，pandas 引入了一个致敬 spark 和 polars 的新特性：`pd.col()`。

```python
# 3.0 RC 中的新语法尝试
df.select(pd.col("price") * pd.col("volume"))
```
这种语法允许开发者在不直接操作 Dataframe 对象的情况下构建计算逻辑。这对于构建复杂的因子计算流（Factor Pipelines）非常有用，因为它减少了中间变量的创建，并让代码更具可读性。虽然目前仍处于起步阶段，但它揭示了 pandas 未来的演进方向：从“过程式”向“声明式”演进。

## 幕后推手：Patrick Hoefler 与 CoW 的执着

如果说 pandas 3.0 有一个灵魂人物，那么 **Patrick Hoefler**（GitHub ID: phofl）绝对是其中之一。

---

他是 pandas 核心团队中最活跃的成员之一，也是 **Copy-on-Write** 机制的主要推动者。

Patrick 是个学霸，毕业于牛津大学，现在在 Citadel 工作。

他的工作重点一直聚焦于让 pandas 变得更加“确定”。在过去的数年里，他几乎凭一己之力重构了 pandas 内部复杂的索引逻辑，目的就是为了消除那个让无数初学者崩溃的 `SettingWithCopyWarning`。
*   **从复杂回归简单**：Patrick 在多个技术分享中提到，Copy-on-Write 虽然在实现上极其复杂，但带给用户的却是极致的简单——你不再需要担心你的修改是否会意外影响到原始数据。
*   **性能与安全的平衡**：他主导的 CoW 机制，通过延迟拷贝（Lazy Copy）技术，确保了在保证数据安全的前提下，内存开销降到最低。

从 Wes McKinney 到 Patrick Hoefler，量化人一直在对开源社区和 Python 做出贡献。

---

## 迟到的 3.0

然而，Pandas 3.0 的发布之旅并不顺利。从 22 年规划，最初约定 23 年 7 月发布，推迟到 24 年，25 年，... 直到今年，RC 版本才珊珊来迟，而 Polars 尽管起步早一年，但 25 年就已推出了稳定的 1.0 版，相比之下，步履就轻快许多。你可能不禁要问，为何热锅热灶干不过另起炉灶？

**历史不是财富，是包袱**

pandas 拥有全球数百万量化研究员和数据科学家的代码资产。它不是在一张白纸上作画，而是在行驶的高铁上更换发动机。
*   **向后兼容的枷锁**：Polars 可以设计全新的、符合现代逻辑的 API（例如它的表达式语法从一开始就是声明式的）。而 pandas 必须在引入新特性的同时，确保千万个旧有的策略脚本不会报错。这种对稳定性的承诺，意味着每一项底层变更（如 BlockManager 的调整）都需要经过极其复杂的废弃周期（Deprecation Cycle）。每一个警告（Warning）的发出，背后都是数月的代码审计。
  
---

*   **NumPy 的双刃剑**：NumPy 曾是 pandas 成功的基石，它让 Python 拥有了接近 C 的数值计算能力。但 NumPy 主要是为科学计算设计的，它在处理“表格化”数据（即包含不同类型、包含缺失值的数据）时，内存管理显得力不从心。例如，NumPy 不原生支持缺失值（NaN 必须是浮点数），这导致了长久以来的“整数列含空值变浮点数”的尴尬。

相比之下，正在赶往 3.0 终点的 pandas，准备了数年，正是为了在“不打破世界”的前提下，完成从 NumPy 到 PyArrow 的惊险跳跃。这不仅仅是代码的重写，更是社区共识的重塑。

## 迎接大象的王者归来

在延宕数年之后，即使 Pandas 3.0 在今夜发布，Polars 也已领先一个身位。在领略 Polars 的极致轻快之后，可能不少人要问，为何我还需要使用 Pandas 3.0?

关键不在谁更快，而在于谁的生态更强大。

**量化研究不是孤岛**。

---

机器学习框架（Scikit-learn）、统计分析工具（Statsmodels）、回测引擎（Zipline、Backtrader）以及策略评估库 Quantstats，它们的血管里流淌的依然是 pandas 的数据格式。

Polars 虽然可以快速计算，但在与这些庞大生态协同、交付最终模型时，pandas 依然是那门“官方语言”。3.0 的意义在于，它让你在不脱离生态主权的前提下，获得了接近 Polars 的性能。

此外，尽管见仁见智，但是 **Polars 没有索引**！更不用说多级索引，以及由此带来的 pivot 表格等功能。如果你在 Pandas 中频繁使用多级索引、stack、unstack 等功能，那么你很可能会一直锁定在 Pandas 中，因为可以预料，Polars 几乎永远不会加上索引功能。

pandas 3.0 的 RC 发布，标志着 Python 数据分析生态正式迈入了 **Arrow 原生时代**。它不仅是老兵的涅槃，更是量化人应对未来十年海量数据挑战的终极底座。

---

当“大象”完成转身，它可能依然是这片森林的王者。对于量化开发者而言，现在就是最佳的学习和迁移窗口。

## 今日名校

<figure style="width: 100%; margin: 0 auto 1rem; padding: 0;">
  <img src="https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/1280px-Oxford_University_Museum_of_Natural_History,_Oxford,_UK_-_Diliff.jpg" style="width: 100%; height: auto; display: block; margin: 0 auto;">
  <figcaption style="font-size: 0.8em; color: grey; text-align: center; margin-top: 0.5rem;">
    By Diliff - Own work, CC BY-SA 3.0
  </figcaption>
</figure>

这是某著名高校的自然历史博物馆。图中的骨架是巨齿龙，是人类历史上第一个被科学命名的恐龙。

---

当时还没有恐龙 (dianosaur) 这个词，因此它被称为 Megalosaurus（巨大的蜥蜴）。

你知道这所学校是哪所学校吗？

在这所学校里，除了 Patrick Hoefler （Citadel）之外，还有以下人物与量化金融有关：

1. 保罗・威尔莫特（Paul Wilmott）, 他是 CQF项目的核心领导人，著有多部量化金融经典教材（如《期权定价：数学模型与计算》）
2. 阿尔瓦罗・卡特亚（Álvaro Cartea），该校数学金融教授，曾任职于 UCL、摩根大通，擅长用机器学习分析金融数据。
3. 拉马・孔特（Rama Cont），该校数学金融讲席教授，获法国科学院 “路易・巴舍利耶奖”（量化金融界最高荣誉之一）
4. 扬・奥布洛伊（Jan Obloj），该校数学教授，研究聚焦 “量化模型的鲁棒性”（避免过度拟合），对高频交易策略的稳定性有重要影响。研究高频交易的同学不妨找找他的文章看看。
