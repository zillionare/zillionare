---
title: "Mastering XtQuant: QMT Live Trading with Third-Party Frameworks"
date: 2024-01-10
slug: en/articles/course/qmt/intro
tags: [XtQuant, QMT, Live Trading, Factor Investing]
excerpt: "Leverage XtQuant to integrate QMT with external frameworks like VS Code, bypassing platform lock-in, accelerating backtests, and accessing superior data for live trading."
lang: en
translation_of: articles/course/qmt/intro
auto_translated: true
source_sha: 2eb06a2317bab9e617032685379cba771e8dc7e2
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154252-cover-course-qmt-intro.md.jpg"
---

QMT, developed by迅投 (Xuntou), is a quantitative trading software procured by brokerages, providing direct interfaces for live quantitative trading. Currently, approximately 50 brokerages have customized and procured QMT. The threshold for enabling quantitative trading permissions ranges from tens of thousands to hundreds of thousands of RMB. Beyond retaining favorable commission rates (as low as 1/10,000, or even zero commission), users also receive free historical and real-time market data, making it a cost-effective solution for live trading access.

## Course Topic
As a quantitative software, QMT offers two primary usage modes. The first is its built-in quantitative trading platform, which allows for strategy development, backtesting, and live trading through an integrated Python environment. The second mode utilizes the XtQuant library provided by QMT, enabling strategy development, backtesting, and live trading driven by third-party quantitative frameworks.

Implementing quantitative trading via XtQuant combined with third-party frameworks offers several distinct advantages:

---

1. **Superior Strategy Development Tools:** By using third-party quantitative frameworks, you can leverage IDEs like VS Code or PyCharm for strategy development and debugging. These tools significantly outperform QMT’s built-in coding interface in terms of efficiency.
2. **Faster Backtesting Speeds:** Multiple users have reported that backtesting within QMT’s internal environment is relatively slow.
3. **Unrestricted Backtesting Time:** Some brokerages’ QMT versions undergo maintenance on weekends, preventing strategy development and backtesting during those periods. Additionally, certain brokerages restrict simulated trading to post-market hours.
4. **Avoiding Vendor Lock-in:** Relying on QMT’s built-in quantitative features inevitably leads to lock-in effects, including:
   1. **Technical Lock-in:** The built-in QMT environment restricts the installation of arbitrary Python libraries, preventing the use of advanced technologies and putting users at a disadvantage in quantitative competitions from the start.
   2. **Data Lock-in:** When using built-in QMT, accessing data not provided by QMT but available from third-party sources can be challenging. There is currently a lack of documentation and examples on how to obtain such data. Since quants maintain their own factor libraries, extracting, storing, and reading these libraries within the built-in environment is another aspect not covered by official documentation.
   3. **Migration Lock-in:** If significant software assets are locked into QMT’s built-in platform, future migration costs will be high. Triggers for migration include other brokerages offering more favorable commission rates, the need to open accounts with multiple brokerages, or the unavailability of critical data on other platforms. External factors also play a role; for instance, in 2023, the partnership between JoinQuant and China Securities ended, forcing users to migrate strategies to QMT.

For these reasons, this course will primarily focus on integrating XtQuant with third-party quantitative frameworks to achieve quantitative trading.

---

The main content includes:

1. Activating and installing QMT and XtQuant
2. Data functionalities of XtQuant
3. Trading interfaces of XtQuant
4. Encapsulating XtQuant as a service
5. Integrating XtQuant with the Daifuweng (Rich Man) quantitative framework

!!! info Daifuweng Quantitative Framework
    Version 2.1 of the Daifuweng framework will integrate XtData’s data and trading interfaces, becoming a complete third-party platform supporting QMT quantitative trading. Data storage is built on ClickHouse, providing extremely low query response times while accommodating small datasets.
