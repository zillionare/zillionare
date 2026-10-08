---
title: "DuckDB 1.0: A Milestone for Local Data Analytics"
date: 2024-08-16
slug: en/posts/tools/duckdb-has-released-1.0
tags: [DuckDB, Data Engineering, Open Source, Database]
excerpt: "DuckDB 1.0 stabilizes its storage format, ensuring backward compatibility and eliminating breaking updates. This release marks a significant milestone for local, columnar data processing, competing directly with Polars and ClickHouse in performance benchmarks."
lang: en
translation_of: posts/tools/duckdb-has-released-1.0
auto_translated: true
source_sha: 64d68d8d4a65cfc2a0b7dd2171d0629f8e6c451f
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/unsplash-duck.jpg"
---

# Milestone: DuckDB Releases Version 1.0

There is a database project that sees millions of downloads per month, with extension download traffic alone exceeding 4 TB daily. On GitHub and social media platforms, it boasts tens of thousands of stars and followers—a ceiling that database products rarely reach. Recently, this highly popular database has reached its first major version release.

That project is **DuckDB**. DuckDB uses a columnar storage format, making it ideal for individual users to store market data. This is precisely why we have been following it.

The primary criterion for DuckDB’s 1.0 release is that its data storage format has stabilized (and appears to be optimally configured). It is fully backward compatible and offers a degree of forward compatibility. In other words, after this version, future updates will generally not introduce breaking changes—meaning users will not typically need to manually migrate data.

Since the 1.0 release, DuckDB seems to have gained even greater popularity:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/duckdb-star-history-2024816.png)

Following this release, DuckDB also published benchmarks highlighting performance improvements over previous years:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/duckdb-perf-benchmark-over-self.jpg)

In horizontal performance comparisons, DuckDB remains at the top. Here is a comparison of `GROUP BY` queries:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/duckdb-over-others-groupby.jpg)

DuckDB, ClickHouse, and Polars take the top three spots. It was surprising to see Dask throw `out-of-memory` errors, raising questions about the need for big data or distributed systems. While Pandas took nearly 20 minutes, it eventually produced results. Modin, however, seemed far behind. How can one seamlessly replace Pandas under these conditions?

This 50 GB, 1 billion row `JOIN` operation caused many competitors to fail:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/duckdb-benchmark-join-50gb.jpg)

Polars remains impressive, while ClickHouse stumbled, throwing exceptions.

ClickHouse was included in these tests primarily because of its robust performance; it deserved to be benchmarked. However, it differs significantly from DuckDB in functionality, or rather, leads in areas where DuckDB lags. These include distributed storage, concurrent read/write capabilities (DuckDB supports only one writer or multiple readers), and essential server-side features like account and role management. Additionally, DuckDB is designed to manage data volumes under 1 TB. For larger datasets, ClickHouse remains the better choice.

DuckDB is also gaining traction in the venture capital market. MotherDuck, a startup built on DuckDB, has developed a serverless version of the database and has raised over $50 million, achieving a valuation of $400 million. In the AI era, it is rare for a traditional software company to secure such a high valuation. For comparison, World Labs, founded by AI pioneer Fei-Fei Li, currently has a valuation of around $1 billion.

Nevertheless, DuckDB is not without competitors. Besides Polars, **chDB**, which uses the ClickHouse engine directly, has recently gained significant momentum. In official ClickHouse benchmarks, chDB closely trails DuckDB. Although its performance is slightly weaker, chDB already supports ClickHouse as a backend data source, a feature that may attract users needing to store and analyze larger volumes of data.
