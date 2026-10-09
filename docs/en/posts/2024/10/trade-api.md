---
title: "Live Trading Interfaces: Easytrader, Ptrade, QMT & EMC"
date: 2024-10-22
slug: en/posts/tools/trade-api
tags: [Live Trading, China A-Shares, Quant Infrastructure, Algorithmic Trading]
excerpt: "A comparative guide to live trading interfaces for China A-shares, evaluating Easytrader, Ptrade, QMT, and EMC based on stability, latency, and deployment flexibility."
lang: en
translation_of: posts/tools/trade-api
auto_translated: true
source_sha: 6c36e44347d663eb6e94485bb807d6b3cd95861f
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154846-cover-posts-2024-10-trade-api.md.jpg"
---

## Easytrader
Easytrader is a trading agent that executes trades by simulating keyboard and mouse events to control brokerage client GUIs. In this architecture, Easytrader exposes trading APIs (e.g., `buy`, `sell`) that strategies call; the agent then translates these calls into mouse-click events on the brokerage client, finalizing the trade.

The primary advantage is that integration requires no formal application process, and it supports a wide range of brokers (excluding Huatai, Haitong, and Guojin, which can be accessed via Tonghuashun). However, because it relies on simulating GUI interactions, it suffers from poor stability and slow response times.

If you must use it for live trading, deploy it on a dedicated, high-performance physical machine running only the brokerage client and Easytrader. Run Easytrader in server mode, and connect to it via its remote client from your strategy machine. Ensure no one manually operates this physical machine to avoid interfering with Easytrader’s automated inputs. Additionally, disable automatic updates and other background services on that machine.

## Hundsun Ptrade
Ptrade is a quantitative platform developed by Hundsun Technologies. An official video tutorial is available for free registration. It is also covered in my course, *Monopoly Quantitative Programming in Practice*.

Ptrade operates on a broker-hosted model. Brokers purchase the Ptrade software, customize it, and provide it to their clients. Users develop strategies using Ptrade’s strategy editor; once backtested, they upload the strategy to run on the broker’s servers. This integration method provides a Python SDK, allowing orders to be placed via the SDK’s trading APIs.

In hosted mode, users typically cannot access the internet, update Python or dependency versions, or install third-party software. Quant strategies are tightly coupled with the broker’s trading and data APIs, making switching brokers costly later. The inability to install custom software limits the use of newer third-party algorithms. If you employ machine learning or reinforcement learning, these libraries may not be available in the broker’s environment, or their versions may differ from your local setup, often without GPU support.

The advantages are faster market data speeds and eliminated server maintenance responsibilities.

Ptrade cannot be downloaded publicly; you must open an account with a broker to obtain it. Live trading access generally requires a minimum asset threshold of 300,000 RMB. Currently, you can apply for Ptrade access through brokers such as Guojin, Guosheng, Guoyuan, Anxin, and Dongguan. If you require specific commission rates (e.g., 0.01% with no minimum) or lower asset thresholds (down to 20,000 RMB), feel free to contact me.

## QMT
QMT (Xintou QMT) is developed by Beijing Ruizhi Rongke. Like Ptrade, it is a broker-procured, customized solution. However, QMT supports a local execution mode, offering better strategy security.

QMT offers two integration methods: file-based order scanning and API-based execution. The API method requires writing and running strategies within the QMT platform, imposing restrictions on Python versions and available libraries (though third-party libraries can sometimes be added via a whitelist).

The file-based order scanning mode has no such restrictions.

QMT is not publicly downloadable; you must open an account with a broker to access it. Currently, live trading access can be requested through Guojin, Guosheng, Guoyuan, Anxin, and Dongguan. If you need specific commission rates (e.g., 0.01% with no minimum) or lower asset thresholds (down to 20,000 RMB), feel free to contact me.

## East Money EMC
East Money EMC requires a minimum asset threshold of 1,000,000 RMB. You must join their official quantitative technical support group to apply for access. It supports both API trading and local file-based order scanning.

The local file-based order scanning method achieves response times under 10ms. Since it is decoupled from the quantitative program, the strategy can run on any machine, using any Python version and third-party libraries.

However, users must manually convert trading instructions (e.g., `buy`, `sell`) into the file order format. EMC also returns order results in CSV format, requiring user-side parsing.

`gmadaptor` provides this encapsulation. Furthermore, it wraps itself as a server, allowing quantitative strategies to run on different machines and operating systems (EMC itself is Windows-only).

## Other Integration Methods
Huatai MATIC requires opening an account with Huatai Securities. This method has a high asset threshold of 10,000,000 RMB, though I can help apply for a reduced threshold of 5,000,000 RMB.

Yichuang Juquan also provides quantitative trading integration using a hosted model.

## Reference Resources
If you need learning materials for Easytrader, Ptrade, QMT, and East Money EMC, I have relevant resources available. Please leave a comment to obtain them.
