---
title: "Zillionare 2.0 Data Sync & Maintenance Guide"
date: "2026-10-09"
slug: en/articles/products/zillionare-maintain
tags: [Data Synchronization, Backtesting, System Maintenance, Quant Infrastructure]
excerpt: "Learn how Zillionare initializes and maintains market data. This guide explains the sync pointers, InfluxDB storage, and Redis caching for accurate backtesting."
lang: en
translation_of: articles/products/zillionare-maintain
auto_translated: true
source_sha: f57398b1fa2282c2c0b397d96dc35e07d22e0c04
---

## Market Data Synchronization Principles

After installing Zillionare, the database is initially incomplete due to various architectural reasons and requires a maintenance process. This process and its underlying mechanics are detailed below:

When building the Zillionare Docker container, we only packaged 30-minute and higher timeframe data from January 2022 to February 2023 for backtesting research purposes. Consequently, your database lacks comprehensive coverage immediately after installation. A fully covered dataset should include all minute-level and higher data (i.e., 5, 15, 30, 60 minutes, daily, weekly, and monthly bars) starting from January 2005.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/02/data-sync-pointer.jpg)

We determine the synchronized data range and the range requiring synchronization using the `epoch_start`, `sync_head`, and `sync_tail` pointers (located in Redis database, db1) along with the current time, as shown in the image above. When we released the Zillionare container, we set `sync_head` to `epoch_start`. Therefore, once you configure your JoinQuant account, data synchronization will prioritize catching up on data from December 30, 2022, to the present. Once this data catch-up is complete, you can modify the head pointer in the Redis database to align with the actual starting point of the data in InfluxDB. At this stage, Zillionare will use your remaining daily quota to backfill data until it reaches `epoch_start` (i.e., January 4, 2005). If you no longer need data earlier than a certain point after synchronizing a sufficient amount, you can reset the pointer back to `epoch_start` to halt synchronization.

!!! info
    This design exists because leveraging Zillionare’s backtesting framework requires matching orders using minute-level market data. However, minute-level data is extremely voluminous.

This is the first thing you need to know about data maintenance. The second key aspect is how Zillionare stores and retrieves data.

To update data in real-time and accurately, Zillionare’s data synchronization is divided into two parts: closed data and open data. Closed data is considered accurate and immutable, so it is recorded in InfluxDB for persistence. Open (unclosed) data is synthesized in real-time from lower-timeframe closed data.

!!! info
    To ensure closed data is accurate, Zillionare’s data synchronization is scheduled around 2:00 AM. By this time, upstream data is generally fully calibrated, and the same data is pulled twice. It is only saved if the two pulls are identical.

In other words, looking at the market before 15:00 on a trading day, yesterday’s daily bars, last week’s weekly bars, and last month’s monthly bars are stored in InfluxDB. However, today’s daily bars and this week’s weekly bars must be calculated and updated in real-time. These updates are derived from 1-minute data, which is cached in Redis. This 1-minute data is updated in real-time during trading hours and triggers the calculation of unclosed data for other timeframes.

If you install Zillionare after market hours, there will be no minute-level or all minute-tier market data in Redis during the initial run. At this stage, `zillionare-omega` may log some errors in the console. These errors can be ignored. Starting from midnight (on a trading day) after deployment, multiple download tasks will initiate. Once the data catch-up is complete, these issues will cease to appear.

After the first trading day following deployment, the aforementioned errors should disappear. However, whether the `week` and `month` unclosed bars are calculated correctly depends on your quota. If your quota is sufficient to synchronize one week’s worth of minute and daily data, the weekly bar will be correct; if it can synchronize one month’s worth, the monthly bar will be correct. Otherwise, you will need to wait for further synchronization.
