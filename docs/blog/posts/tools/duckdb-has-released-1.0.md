---
title: 里程碑！DuckDB 发布 1.0
date: 2024-08-16
category: tools
slug: duckdb-has-reached-1.0
motto: 
img: https://images.jieyu.ai/images/2024/08/unsplash-duck.jpg
stamp_width: 60%
stamp_height: 60%
tags: [tools, duckdb]
---

有一个数据库项目，每月下载次数高达数百万，仅扩展的下载流量每天就超过 4 TB 。在 GitHub 和社交媒体平台上，该数据库拥有数以万计的 Stars 和粉丝，这是数据库类的产品难以企及的天花板。最近，这个极具人气的数据库迎来了自己的第一个大版本。

这个项目，就是 DuckDB。Duckdb 是列存储的方式，非常适合个人用户用作行情数据的存储。这也是我们关注它的原因。

Duckdb 这次发布 1.0 的主要准则是，它的数据存储格式已经稳定（并且目前来看最优化）了，不仅完全向后兼容，也提供了一定程度上的向前兼容。也就是说，达到这个版本之后，后面发布的更新，一般情况下将不会出现破坏式更新 -- 即不会出现必须手动处理迁移数据的情况。

从 1.0 发布以来，duckdb 的似乎受到了更大的欢迎：

![](https://images.jieyu.ai/images/2024/08/duckdb-star-history-2024816.png)

在这次发布之后， duckdb 还发布了历年来 duckdb 性能上的提升：

![](https://images.jieyu.ai/images/2024/08/duckdb-perf-benchmark-over-self.jpg)

当然在性能的横向比较上，duckdb 仍然是位居榜首的。这是 groupby 查询的比较：

![](https://images.jieyu.ai/images/2024/08/duckdb-over-others-groupby.jpg)

Duckdb，Clickhouse 和 Polars 位居前三。Dask 会出 out-of-memory 错误，也是出人意料。这还做什么大数据、分布式啊。Pandas 虽然用了接近 20 分钟，但最终还是给出了结果，而 Modin 还不知道在几条街之后，你这要如何无缝替换 pandas?

这个是 50GB， 1B 行数据的 join 操作，直接让一众兄弟们都翻了车：

![](https://images.jieyu.ai/images/2024/08/duckdb-benchmark-join-50gb.jpg)

所以，Polars 还是很优秀啊。Clickhouse 有点出丑，直接出了异常。

不过，Clickhouse 之所以被拉进来测试，主要是因为它的性能很强悍，所以应该被拉来比划。但是，它跟 Duckdb 在功能上有很大的差异，或者说领先，比如分布式存储，并发读写（Duckdb 只支持一个读写，或者同时多个只读），此外还有作为服务器必不可少的账号角色管理等。另外，Duckdb 能管理的数据容量在 1TB 以下。更多的数据，还得使用 Clickhouse。

Duckdb 在资本市场上也很受欢迎。基于 DuckDB 的初创公司， MotherDuck 开发了 DuckDB 的无服务器版本，目前已经筹集了 5000 多万美元资金，估值达到 4 亿美元。在 AI 时代，能拿到这么高估值的传统软件公司非常罕见。作为对比，AI 教母李飞飞创办的 World Labs 目前估值也才 10 亿左右。

不过，Duckdb 也不是没有竞争者。除了 Polars 之外，直接使用 Clickhouse 引擎的 chDB 最近风头也很强劲，在 clickhouse 的官方 benchmark 比拼中，紧追 Duckdb。性能上尽管略微弱一点，但 chDB 已经支持 clickhouse 作为后端数据源，这一点上可能会吸引需要存储和分析更大体量数据的用户。
