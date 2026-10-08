---
title: "ClickHouse: One Table to Rule Them All!"
date: 2024-01-17
slug: en/posts/tools/why-click-house-so-fast
tags: [ClickHouse, Market Data, Time-Series Database]
excerpt: "Our earlier notes covered personal setups for storing massive market data. They are called personal not for lack of speed, but because data lives locally and supports single-machine queries only."
lang: en
translation_of: posts/tools/why-click-house-so-fast
auto_translated: true
source_sha: aa9f04876a1d3f6bc5362581454699318d94601b
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/query-buillion-rows-in-ms.jpg"
---

In our last few notes, we covered personal setups for storing massive market data. We call them personal not because they are slow, but because the data lives locally and only supports single-machine queries.

Data feeds are expensive — this winter we've even heard of sizable firms asking employees to share a Wind account. So sharing network storage and paying for just one data license becomes a sensible ask. Not to mention, only with centralized management can IT own data maintenance while analysts focus purely on strategy.

<!--more-->

---

## Debunked Solutions That Keep Circulating

It's already 2024, yet you still see articles recommending MySQL for market data storage. That's just wrong. Not only MySQL — even PostgreSQL won't cut it. Not only PostgreSQL — even SQL Server or Oracle won't cut it.

Other non-starters include MongoDB. MongoDB can hold a lot, but it's a poor fit for querying time-series data like market quotes.

InfluxDB was the earliest and most famous time-series database. But its community edition is relatively weak, especially with its limits on query concurrency. Plus, its engine is written in Go, which is still several times slower than C.

DolphinDB may be considerably faster than InfluxDB, but its community edition is also too restricted. TiDB is said to perform well, but we never had a chance to benchmark it.

But with a king like the ClickHouse community edition on the table, why bother evaluating the bronze players?

## Why ClickHouse Is So F**ing Fast?

ClickHouse is a product from the fighting nation. Its developer is Russia's search engine Yandex! (and yes, you can't drop that exclamation mark). Search engines have to handle huge query and analytics workloads by nature, which gave birth to this performance monster.

---

ClickHouse optimization is full-stack. At the hardware level, it exploits SIMD CPU instructions. ClickHouse makes a point of using SIMD for parallel speedups — when you install it, it even ships a detection tool to check whether SIMD optimization can be enabled.

!!! tip
    SIMD isn't exactly exotic these days — plenty of software uses it. But ClickHouse knows how to market it, a bit like Xiaomi hyping an all-glass camera. That said, making full use of hardware instructions is genuinely one of the most important ways to optimize.

On the data-structure side, ClickHouse uses columnar storage — the same approach as Parquet and HDF5. With columnar storage, excellent compression schemes become available, and once on-disk size shrinks, IO efficiency obviously improves.

But its MergeTree-based storage engine lets queries fan out across all CPU cores and disks — not just on one machine, but across every CPU core and disk in the cluster. That's what lets query performance scale linearly with hardware.

!!! tip
    As ClickHouse itself puts it, many other data systems may use all these techniques. What makes ClickHouse faster is attention to detail. And it can sweat the details because it doesn't try to be general-purpose — it focuses only on columnar databases.

---

In this area it uses plenty of big-data tricks, such as Bloom filter indexes. It also leaves a few optimization knobs to the user, which is what this note is about: how to design a database that holds tens of billions of quote records with best-in-class performance.

## Hands-On: Start with 100 Million Rows

Although in ClickHouse we could store minute bars and daily bars in the same table, we almost never fetch two different frequencies at once, so storing them in separate tables is clearly more sensible. For our example, we'll use minute bars only:

```sql
CREATE TABLE if not exists bars_1m
(
    `frame` DateTime64 CODEC(Delta, ZSTD),
    `symbol` LowCardinality(String),
    `open` Float32 DEFAULT -1 CODEC(Delta, ZSTD),
    `high` Float32 DEFAULT -1 CODEC(Delta, ZSTD),
    `low` Float32 DEFAULT -1 CODEC(Delta, ZSTD),
    `close` Float32 DEFAULT -1 CODEC(Delta, ZSTD),
    `volume` Float64 DEFAULT -1 ,
    `money` Float64 DEFAULT -1 ,
    `factor` Float64 DEFAULT -1 CODEC(Delta, ZSTD)
)
ENGINE = MergeTree
ORDER BY (frame, symbol)
```

---

Here's the first benefit of ClickHouse. It's fully compatible with core SQL syntax. When we were designing zillionare 2.0, InfluxDB drove us crazy — who knows why they abandoned SQL compatibility to invent a brand-new query language from scratch!

This means if we install ClickHouse across the team — usually IT's job — analysts can get started right away, because anyone doing data analysis already knows SQL.

There are a few tricks here you won't find in plain SQL.

First, the **CODEC(Delta, ZSTD) compression** on the frame column. It cleverly turns the column into a sparse vector by storing row-to-row deltas — slashing both storage size and read time. In market data, huge numbers of timestamps are identical or differ by only a tiny delta. For example, if we stuff minute data for 5,000+ stocks into one table, we'll often see 5,000 identical timestamps in a row, all of which can be stored as zeros!

**The default values for OHLC** are also deliberate. If a symbol is halted for a day, its OHLC data is null. ClickHouse allows nulls, but then it has to store nulls in separate files and join them back at query time. That costs time. So here we use an impossible value as the default, keeping all data together, which speeds up both storage and computation.

---

OHLC values move in tiny steps, so we compress them with DELTA encoding too. Volume and turnover, by contrast, can jump wildly, so compression would cost more than it saves.

We can make these optimizations because we know the distribution of the data — just as a data analyst has to know data distributions — that's how ClickHouse squeezes out performance.

We used single precision for OHLC but 64-bit floats for factor. That's necessary. They may both look small, but OHLC has a tiny value range with no precision issues, while factor data is different — it has to be more accurate.

!!! note
    How do we know the difference? Because we hit this exact issue while building zillionare. When we defined factor as 32-bit, our backtest showed portfolio-value discrepancies of a few to tens of yuan on around 100 million in capital. You might want to check whether the framework you're using has the same problem.

For the symbol column we used another optimization. With this encoding, we actually store integers instead of strings, which greatly improves storage efficiency and query speed. If you're familiar with pandas performance tuning, you've seen this before — it's much like the categorize optimization in pandas.

Finally, we set frame and symbol as the primary key. Most of our queries will filter on those two fields.

---

So how does our table actually perform?

Let's insert 1 million, 10 million, and 100 million rows respectively, and measure insert and query times. When preparing the data, we used fully random data — that matters. If we reused identical values, it would run faster.

* Insert 1 million rows in 8.3s; query returning 200 rows in 0.1s.
* Insert 10 million rows in 77.7s; query returning 2000 rows in 0.7s.
* Insert 100 million rows in about 16 minutes; query returning 20200 rows in 13.7s.

This is already excellent. But it doesn't look beyond expectations, right? For comparison, on InfluxDB, returning 1 million records took about 55 seconds, with network transfer and client-side reassembly accounting for ~30 seconds — so ClickHouse may not have beaten InfluxDB in this round. And at the 10-million scale, a fully tuned MySQL can also answer within 0.7 seconds, though it can't handle hundreds of millions of rows.

Why no surprise? I checked my test environment:

A VM with only 8 CPUs and 8GB RAM (backed by a disk array, to be fair), and I'd already opened 4 VS Code windows, leaving only 0.6GB free memory. When we tested InfluxDB, we used a physical machine with 48 CPUs + 96GB RAM and 3+ billion total records.

I'll rerun an apples-to-apples comparison when I get the chance. But the ClickHouse team has already benchmarked a similar market-data database:

On a MacBook Pro, an argmax query over 240 million records took just 0.9 seconds! That's not enough for HFT, but plenty for most use cases.

Still, the ClickHouse test differs a lot from ours:

In the ClickHouse test, the result set was tiny; in our test, the query returned 20,000 rows.

That points to another optimization direction. Push as much work as possible to the ClickHouse server. In other words, much of the factor computation we used to do by pulling data back into Python can now be done directly in ClickHouse — we just take the result.

That's what our upcoming notes will cover.
