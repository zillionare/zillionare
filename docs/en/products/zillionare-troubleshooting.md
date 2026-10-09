---
title: "Zillionare 2.0: Resolving 'Unclosed Bar' Build Failures"
date: "2026-10-09"
slug: en/articles/products/zillionare-troubleshooting
tags: [Zillionare, Error Handling, Data Maintenance]
excerpt: "Fix the \"failed to build unclosed bar\" error in Omega logs caused by missing minute-level data during initial post-market startup."
lang: en
translation_of: articles/products/zillionare-troubleshooting
auto_translated: true
source_sha: 7b22db319f6ac298f0400d5ba15cccc9b5ff0069
---

## 1. Resolving the "failed to build unclosed bar for ..." Error in Omega Logs
This error appears as shown in the image below:
![50%](rebuild-unclosed-bar-error.png)

The root cause is that the initial startup occurs after market close, leaving the Redis database without minute-level data. Consequently, certain data aggregations cannot be completed. This log message will clear once the next trading day ends and the data is fully populated. For more details, see [Data Maintenance](/articles/products/zillionare-maintain/).
