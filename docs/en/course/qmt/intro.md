---
title: "Mastering XtQuant: QMT Live Trading with Third-Party Frameworks"
date: 2024-01-10
slug: en/articles/course/qmt/intro
tags: [XtQuant, QMT, Live Trading, Factor Investing]
excerpt: "QMT offers a cost-effective live trading solution for China A-shares. This course details integrating XtQuant with third-party frameworks to bypass platform lock-in, enhance backtest speed, and enable advanced strategy development."
lang: en
translation_of: articles/course/qmt/intro
auto_translated: true
source_sha: d5f9be0782da6d121dfa5b9969352674cb51bbbd
---

QMT is a quantitative trading software developed by Xuntou. As an institution-side procurement solution, it provides direct interfaces for live quantitative trading. Currently, approximately 50 brokerages have customized and procured QMT. The threshold for activating quantitative permissions varies from tens of thousands to hundreds of thousands of RMB. Beyond securing favorable commission rates (as low as 1/10,000, or even zero commissions), activating these permissions grants free access to historical and real-time market data, making it one of the most cost-effective solutions for live trading integration today.

## Course Overview

As a quantitative software, QMT offers two primary usage modes. The first is its built-in quantitative trading platform, which allows for strategy development, backtesting, and live trading through an embedded Python environment. The second mode utilizes the XtQuant library provided by QMT, enabling strategy development, backtesting, and live trading driven by third-party quantitative frameworks.

Implementing quantitative trading via XtQuant combined with third-party frameworks offers several distinct advantages:

1.  **Superior Strategy Development Tools:** By using third-party frameworks, you can leverage IDEs like VS Code or PyCharm for strategy development and debugging. These tools offer significantly higher efficiency compared to QMT’s built-in programming interface.
2.  **Faster Backtesting Speeds:** Multiple users have reported that backtesting within QMT’s internal environment is relatively slow.
3.  **Unrestricted Backtesting Time:** Some brokerages’ QMT versions undergo maintenance on weekends, preventing strategy development and backtesting during those periods. Additionally, certain brokerages restrict simulated trading to post-market hours only.
4.  **Avoiding Platform Lock-in:** Relying on QMT’s built-in quantitative features inevitably leads to lock-in effects, including:
    1.  **Technical Lock-in:** The built-in QMT environment restricts the installation of arbitrary Python libraries. This prevents the use of advanced technologies, putting you at a disadvantage from the start in quantitative competitions.
    2.  **Data Lock-in:** When using built-in QMT, if you encounter data not provided by QMT but available from third-party sources, there is often no clear documentation or example on how to acquire or integrate it. Quantitative researchers maintain their own factor libraries; extracting, storing, and reading these libraries within the built-in environment remains an unaddressed aspect in official documentation.
    3.  **Migration Lock-in:** Once significant software assets are locked into QMT’s built-in platform, future migration costs can be prohibitive. Triggers for migration are numerous: other brokerages offering more favorable commission rates, the need to open accounts across multiple brokerages, or specific data being available only on other platforms. External factors also play a role; for instance, in 2023, the partnership between JoinQuant and Yichuang Securities was terminated, forcing users to migrate their strategies to QMT.

For these reasons, this course focuses on integrating XtQuant with third-party quantitative frameworks to achieve live quantitative trading.

## Main Content

1.  Activating and installing QMT and XtQuant
2.  XtQuant’s data functionality
3.  XtQuant’s trading interfaces
4.  Encapsulating XtQuant as a service
5.  Integrating XtQuant with the "Da Wang Fu" (Rich Man) quantitative framework

!!! info "Da Wang Fu Quantitative Framework"
    Version 2.1 of the Da Wang Fu framework will integrate XtData’s data and trading interfaces, becoming a complete third-party platform supporting QMT quantitative trading. Data storage is built on ClickHouse, providing extremely low query response times even while accommodating small data volumes.
