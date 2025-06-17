---
title: Quantstats Reloaded
date: 2025-06-16
category: tools
img: 
tags: 
    - python
    - quantstats
---

Quantstats 是一款用于交易策略绩效分析的 Python 库，深受量化圈用户喜爱，在 Github 上获得了超过 5.8k 的 stars。但很遗憾，由于原作者长期未维护，现在新安装的 Quantstats，尤其是在 Python 3.12 及以上高版本中，几乎无法运行。

我们带来了更新。

---

<div style='width:500px;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://images.jieyu.ai/images/2025/06/Ran-Aroussi.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

Quantstats 是 Ran Aroussi 的一个开源项目。Ran Aroussi 是一位软件开发者、金融创新者和独立创业者。他创建了多个受欢迎的 Python 库，比如广为人知的 YFinance（17.9k stars）和 Quantstats。他还创立了 Tradologics —— 一个程序化交易的云平台。目前他还是一名播客，主持着『Old School, New Tech』节目。

与匡醍一样，他致力于『创建工具以帮助人们更智能地工作』，并分享『可操作的技巧、真实世界的策略，以及关于编码、独立开发、金融和创业的内幕故事』。


也可能正是因为参与的活动太多，他不得不忽略了对 Quantstats 这一知名项目的维护责任。最后一次更新还是 8 个月前。此后，社区已提交了大量 issue report。例如，在 Python 3.12 版本下（其他版本新安装 Quantstats 也可能出现），会遇到如下错误：

![issue 416](https://images.jieyu.ai/images/2025/06/quantstats-issue-416.jpg)

这是一个只在 Jupyter Notebook 下出现的问题，主要由于 nbformat 升级导致。该问题修复后，你还可能遇到如下错误：

![issue 420](https://images.jieyu.ai/images/2025/06/quantstats-issue-420.jpg)

几个月来，尽管社区不断提交修复，但作者一直没有时间发布新版本。可能因为原版 Quantstats 没有单元测试和 CI，每次发布都需手动测试，极为繁琐，作者难以抽身。

在匡醍的量化课程中，我们也向学员推荐了 Quantstats。为保证学员体验，我们决定接手 Quantstats 的维护工作，并发布了 quantstats-reloaded 新包（原包只能由 Ran Aroussi 发布）。

如果你也受到 Quantstats 问题影响，请使用 quantstats-reloaded。本版本除了修复 #416、#420 等 bug，还进行了如下重构：

!!! Abstract
    1. 移除了对 yfinance 的依赖，改用人工合成数据进行测试，大幅提升测试可复现性。
    2. 改用 poetry 进行依赖管理，未来将提供更严格、基于语义的依赖版本控制。
    3. 增加了单元测试，覆盖率由 0% 提升至 21%。
    4. 移除对过时 Python 版本（如 3.6~3.9）的支持。
    5. 增加了多平台、多版本测试框架和 CI。

考虑到 #416 等 bug 的紧迫性，我们提前发布了该版本。后续将在提升单元测试覆盖率、通过多平台（mac、windows、linux）和 CI（GitHub Actions）测试后，发布新版本。

现在，请尝试：

```bash
pip install quantstats-reloaded
```
