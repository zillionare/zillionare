---
title: "Zillionare 2.0 Data Sync Guide"
date: 2024-02-23
slug: en/articles/products/zillionare-maintain
tags: [Data Synchronization, Backtesting, System Maintenance]
excerpt: "Learn how Zillionare handles data synchronization, from initial warm-up to real-time updates, ensuring accurate backtesting and live trading readiness."
lang: en
translation_of: articles/products/zillionare-maintain
auto_translated: true
source_sha: c9cceee5361471675c842d5c0351e7175e171460
---

## Market Data Synchronization Principles

After installing Zillionare, the database is initially incomplete due to various technical reasons and requires a maintenance process. This guide explains that process and its underlying mechanics.

When building the Zillionare Docker container, we only packaged 30-minute and higher timeframe data from January 2022 to February 2023 for backtesting research. Consequently, your database does not initially cover the full historical range. A comprehensive dataset should include all minute-level and higher data (i.e., 5, 15, 30, 60 minutes, daily, weekly, and monthly bars) starting from January 2005.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/02/data-sync-pointer.jpg)

We determine the synchronized data range and the range requiring synchronization using the `epoch_start`, `sync head`, and `sync tail` pointers (stored in Redis database `db1`) along with the current time, as shown in the image above. When we released the Zillionare container, we set `sync head` equal to `epoch_start`. Therefore, once you configure your JoinQuant account, data synchronization will prioritize catching up from December 30, 2022, to the present. After this data catch-up is complete, you can modify the head pointer in the Redis database to align with the actual start point of the data in InfluxDB. At this stage, Zillionare will use your remaining daily quota to backfill historical data until it reaches `epoch_start` (i.e., January 4, 2005). You can also reset the pointer back to `epoch_start` to halt synchronization if you no longer need earlier data after syncing a certain amount.

!!! info
    This design exists because leveraging Zillionare’s backtesting framework requires matching orders using minute-level market data. However, minute-level data is extremely large.

This is the first thing you need to know about data maintenance. The second key point is how Zillionare stores and retrieves data.

To update data in real-time and accurately, Zillionare’s data synchronization is divided into two parts: closed data and open data. Closed data is considered accurate and immutable, so it is recorded in InfluxDB for persistence. Open data (unclosed bars) is synthesized in real-time from lower-timeframe closed data.

!!! info
    To ensure closed data is accurate, Zillionare’s data synchronization is scheduled to start around 2:00 AM. By this time, upstream data is generally fully calibrated. The same data is pulled twice, and only if the two pulls are identical is the data saved.

In other words, looking at the market before 15:00 on a trading day, yesterday’s daily bars, last week’s weekly bars, and last month’s monthly bars are stored in InfluxDB. However, today’s daily bars, this week’s weekly bars, etc., must be calculated and updated in real-time. These updates originate from 1-minute data, which is cached in Redis. This 1-minute data is updated in real-time during trading hours and triggers the calculation of other unclosed timeframes.

If you install Zillionare after market close, there will be no minute-level or sub-minute market data in Redis during the initial run. Consequently, `zillionare-omega` may log some errors. These errors can be ignored. Starting from midnight (on a trading day) after deployment, multiple download tasks will run. Once the data catch-up is complete, these issues will cease to appear.

After the first trading day post-deployment, the aforementioned errors should disappear. However, whether the `week` and `month` unclosed bars are calculated correctly depends on your quota. If your quota is sufficient to sync one week’s worth of minute and daily data, the weekly bar will be correct; if it can sync one month’s worth, the monthly bar will be correct. Otherwise, you will need to wait.
