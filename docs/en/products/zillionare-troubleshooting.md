---
title: "Zillionare 2.0: Resolving 'Unclosed Bar' Build Failures"
date: 2024-02-23
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154342-cover-products-zillionare-troubleshooting.md.jpg"
slug: en/articles/products/zillionare-troubleshooting
tags: [Zillionare, Error Handling, Data Maintenance]
excerpt: "Fix the \"failed to build unclosed bar\" error in Omega logs caused by missing minute-level data during initial post-market startup."
lang: en
translation_of: articles/products/zillionare-troubleshooting
auto_translated: true
source_sha: b230214fa49b58b5da0fabf0b3a35e975cb532cb
---

## 1. Resolving the "failed to build unclosed bar for ..." Error in Omega Logs
This error appears as shown in the image below:
![50%](rebuild-unclosed-bar-error.png)

The root cause is that the initial startup occurs after market close, leaving the Redis database without minute-level data. Consequently, certain data aggregations cannot be completed. This log message will clear once the next trading day ends and the data is fully populated. For more details, see [Data Maintenance](/articles/products/zillionare-maintain/).
