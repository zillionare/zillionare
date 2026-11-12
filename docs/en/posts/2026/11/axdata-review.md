---
title: "AxData: More Than Just Another A-Share Quant Data Source"
date: 2026-11-09
slug: en/posts/tools/axdata-review
tags: [Quant Data Infrastructure, Factor Investing, Backtest, Open Source]
excerpt: "AxData pairs pluggable multi-source ingestion with tiered local Parquet/DuckDB storage, keeping core A-share data on disk—no rate limits, faster backtests, one unified SDK/HTTP interface."
lang: en
translation_of: posts/tools/axdata-review
auto_translated: true
source_sha: 2534873a60b5eb10e7ecb5c28ecddb664a719692
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261111101854-axdata-review.jpg"
---

Building quant strategies for China A-shares, the first roadblock is where to get the data. You have probably already tried AKShare, Pytdx, Tushare, JQData, BaoStock, xtquant and the rest. The unavoidable problem:

Free data comes with **rate limits**, **coverage limits** and **history limits**. Rate limits mean the server only lets you call an API so many times per minute and pull so many rows; coverage limits mean whether you are allowed to obtain a particular key dataset — historical ST status and historical price-limit data, two of the most commonly used, sit behind a paywall or a high credit threshold at several providers; history limits mean the maximum lookback span you are permitted when pulling data.

On top of that, the data sources themselves are not exactly reliable. Some block web scrapers to push their own proprietary toolkits and quant platform suites; others get shut down for policy reasons.

An ideal fix: **spread data requests across multiple sources and turn on standardized local storage.** Once local storage is enabled, historical requests read straight from disk instead of hammering remote servers again and again — which removes rate limits outright and speeds up backtests enormously. You can also break the history limit by importing data externally or backfilling at low frequency. And multiple sources let you combine each one's strengths to get around coverage limits.

AxData is a quant data solution evolving in exactly that direction. It is under active development: first published on GitHub four months ago, still under 1k stars. Frankly, it is not yet a "finished database" that you install and it auto-pulls ten years of full-market history. But because it is arguably the first open-source project to run <b>"pluggable multi-source ingestion + tiered local Parquet/DuckDB storage + unified SDK/HTTP data serving"</b> through a rigorous engineering architecture, we think it is well worth recommending. After all, the only thing that keeps an open-source project alive is attention and contributions from the community.


## /01 AxData's Dual-Track Design at a Glance

From a strategy developer's point of view, the ideal data experience should really be a single unified semantic API: you just declare "which symbols, which time range," and the API decides for itself what can be read locally and what must be fetched from a remote server and written back into the cache automatically.

Probably because unifying different data sources is hard, AxData only puts a very small set of core data into local storage, collected on a schedule and read locally at use time; most data still goes the remote-fetch route for now. So AxData currently runs a dual-track system on the data side.


![AxData data pipeline](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261112131455-mermaid-axdata-review.jpg)

As the diagram shows, AxData brings excellent engineering order:


- **Left track (collect and store)**: only data explicitly pulled by a Collector task (triggered manually or on a trading-day schedule) passes through queue-based rate limiting and a quality check, then lands as open **Parquet** files under the four-layer `raw -> staging -> core -> factor` model, with **DuckDB** providing fast local SQL and view queries.
-  **Right track (source-direct)**: when you call `client.call()` or `POST /v1/request/*`, the gateway validates parameters, requests upstream, normalizes the fields and returns directly — **nothing is written to disk by default**, which suits intraday monitoring, API debugging or one-off pulls.
- **Seamless local-to-LAN switching**: the Python SDK reads Parquet/DuckDB directly on the local machine with no background service required; on a LAN you just start the HTTP API (port `8666`) and other machines pass in `api_base` to pull data with exactly the same code, while the web console (port `8667`) handles visual management of tasks, plugins and data quality.


## /02 Data Landscape: 9 Data Sources, 257 Datasets

If you only look at the local core tables, you will underestimate AxData's coverage. In fact, on the "source-direct" layer, AxData already ships preinstalled plugins covering **9 major data-source families with 257 data interfaces in total** — spanning not only conventional A-share price/volume and fundamentals, but also futures, options, convertible bonds, and the very A-share-specific "short-term limit-up / theme sentiment" data.

Here is the breakdown by source (exact API names can be looked up on the project docs site):

| Data source                      | Core datasets covered                                                                                                                                                                                                                                                                                         | Role in live quant work and usage caveats                                                                                                                                                                      |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tongdaxin (TDX)** <br>(91)         | **Stocks/ETFs/indices**: basic lists, limit-up/limit-down prices, pre-market share capital, ST/suspension lists; daily/weekly/monthly/minute/second K-lines and adjustment factors; intraday and historical time series, tick-by-tick trades, call-auction detail; five-level order book, real-time snapshots and incremental streams; F10 financials, chip distribution, main-force control, consecutive-limit-up ladder and theme strength.                                                                                    | **The go-to source for A-share price/volume and short-term main-force data.** Built on a 7709-protocol Actor connection pool (multi-server auto-failover plus WebSocket real-time streaming). Currently the only source with 8 independent scheduled collectors built in by default.                                         |
| **Sina Finance** <br>(60)       | **Options** (CFFEX index options, SSE option quotes and Greeks, commodity options), **futures** (main continuous contracts, daily/minute bars, open-interest rankings, realized volatility), **bonds and convertibles** (China/US Treasury yields, convertible overview), **funds/ETFs** (AUM, dividends), A-share three financial statements as JSON, Dragon-Tiger list seat tracking, lock-up expiries, ESG scores, HK/US stocks and global indices, Bank of China FX rates.                  | **A treasure trove for derivatives and cross-market data.** Fills gaps that free sources leave wide open: option Greeks, commodity/index futures minute bars and structured financial statements. These are public HTTP endpoints, currently source-request-only (`source_request-only`) by default; watch for web-side anti-scraping rate limits on high-frequency calls. |
| **CNINFO** <br>(32)       | **Listed-company announcements** (announcement lists, PDF metadata, scheduled disclosure, research-call announcements), **Hudongyi Q&A** (investor questions and secretary replies in full), **corporate governance** (equity pledges, external guarantees, litigation), **share capital and shareholders** (executive increases/decreases, shareholder counts and concentration, controller changes, rights-issue plans), **bond/convertible issuance and conversion**, fund heavy holdings and asset allocation, IPOs and listing-committee approvals, industry classification and P/E ratios. | **Fundamentals, event-driven and alternative data.** Official disclosure standards, ideal for event-driven strategies (sudden drops in shareholder counts, insider buying, NLP analysis of research-call transcripts); announcement PDFs return metadata and download links only and are not stored by default.                            |
| **TDX Extended Quotes** <br>(31) | **Futures** (contract lists, K-lines, intraday series, current-day/historical ticks, real-time snapshots), **options** (contract lists, T-quote chains, K-lines, intraday series), **bonds**, **funds** (NAV and trends), **FX** (K-lines, intraday series, ticks), **macro indicators** (lists, snapshots, series).                                                                                                | **Multi-asset high-frequency and historical supplement.** A separate plugin from the standard TDX one (`axdata-source-tdx-ext`), providing option T-quote chains with up to 55 fields plus futures/FX tick detail; requires a TDX server that supports extended quotes.                              |
| **Eastmoney** <br>(13)       | Real-time snapshots for A-shares and broad-market indices, **industry/concept sectors** (real-time sector quotes, sector constituents, a stock's sectors), **short-term pools** (limit-up pool, limit-down pool, yesterday's limit-ups and today's performance, order-book anomaly detail), **daily Dragon-Tiger list summary**, **margin trading detail**, per-stock research report lists.                                                                                                    | **The tool of choice for sector mapping and intraday anomalies.** Sector constituents and order-book anomalies (large buys, sealing the limit-up) are classified in fine detail; public HTTP endpoints with no default scheduled collectors, so guard against IP bans from high-frequency requests.                                                   |
| **Cailian Press** <br>(12)         | News flashes, **market sentiment**, today's main-line opportunities, today's hot sectors and their leaders, sector heat rankings, sector rotation, a limit-up pool annotated with limit-up reasons, per-stock intraday series and K-lines.                                                                                                                                                                                  | **Theme/hotspot and text-sentiment source.** The limit-up pool ships with editor-distilled "limit-up reasons," making it ideal for short-term theme mining and public-opinion monitoring; mostly same-day cross-sectional data with little historical depth.                                                        |
| **Kaipanhong** <br>(9)          | **Historical limit-up/limit-down stocks**, historical limit-up reviews, **historical sector constituents**, historical bellwethers, limit-up ladder, market sentiment, sector rankings, market-structure events.                                                                                                                                                                                            | **A rare source of historical short-term reviews.** Fills the gap in ordinary free sources that only offer today's hot spots with neither historical sector constituents nor historical limit-up reviews — ideal for backtesting limit-up chasing and continuation strategies.                                                                  |
| **Tencent Finance** <br>(6)        | A-share historical daily bars, index historical daily bars, earliest-available-year lookup, A-share real-time quote lists, real-time snapshots, A-share tick-by-tick trades.                                                                                                                                                                                                                   | **A lightweight, stable backup quote source.** Fast HTTP responses with a simple structure — good for lightweight real-time snapshot polling or cross-checking against TDX daily bars; source-request-only by default and does not automatically replace TDX for storage.                                                         |
| **Exchanges** <br>(3)          | **Trading calendar** (SSE/SZSE/BSE), **stock basic info** (official listing status, industry, total/float shares, VIE/profitability flags), **historical stock lists**.                                                                                                                                                                            | **System-level authoritative master data.** `trade_cal` has been productized as a system base-data cache that every daily-frequency quote collector depends on for trading-day alignment and gap checks before it runs.                                                                   |


## /03 A Deliberately Minimal Core Layer

Having toured the rich source-side interfaces, let's return to the heart of it: local backtest storage.

First, a question: for quants, **what must a minimal dataset contain?** On the face of it the answer depends on your strategy, since different strategies need different data.
A **minimal quant backtest data subset** must contain all six of the following:

1. **Calendar** (fixes trading days, drives the time axis)
2. **Security list** (with listing/delisting dates, eliminating survivorship bias)
3. **Daily OHLC, volume, amount** (the basic price/volume facts)
4. **Daily adjustment factors** (to compute forward/backward-adjusted prices dynamically)
5. **Daily price limits** (to judge whether a limit-up can be bought and a limit-down can be sold)
6. **Daily ST list** (to determine 5% vs 10%/20% limits and to filter symbols)

Yet AxData's Core layer does not currently provide all of these. Its `core` (core fact table) layer defines only the first four tables: `trade_cal` (trading calendar), `stock_basic_exchange` (stock list), `daily` (unadjusted daily bars) and `adj_factor` (adjustment factors). Judged on the `core` layer alone, it genuinely does not yet cover the minimal backtest subset, and the default task only pulls a tiny sample of `000001.SZ` — there is no ready-to-use full-market historical database.

There are two reasons for this. The AxData author argues that the ST list obtained through TDX is only a current snapshot, not point-in-time data, and so cannot be written into the core layer until that is solved.

- `tdx.stock_daily_price_limit_tdx.snapshot` (daily limit-up/limit-down prices)
- `tdx.stock_st_list_tdx.snapshot` (ST stock list)
- `tdx.stock_suspensions_tdx.snapshot` (suspension/resumption list)
- `tdx.stock_daily_share_tdx.snapshot` (daily pre-market share capital)

Accumulating these snapshots over time will eventually fill the gap. But a faster route is to extend AxData a little and wire in data from other sources — historical ST lists, for instance, are available from baostock. Here we will use Tushare to fetch historical price-limit data as the example and walk through how to extend AxData.


## /04 Hands-On: How to Extend AxData

Once you understand AxData's architectural boundaries, you will see it is essentially <b>a quant data foundation that has already built the task scheduler, concurrency resource pool, Parquet writer, quality checker and DuckDB query engine for you</b>.

If you want to persist the **daily price limits**, **historical ST lists**, **full-market daily bars** mentioned above — or **Kaipanhong's historical limit-ups** and **Sina's financial statements** — into your local `core` layer to form a complete in-house backtest database, you only need two extension steps following AxData's plugin spec:

### 1. Write a standalone Collector plugin

In AxData, data-source providers and collectors are decoupled. To get data into storage on a schedule, create a lightweight Python plugin package (declare the `axdata.plugins` entry point in `pyproject.toml` and include an `axdata-plugin.json` manifest). Declare a `CollectorSpec` in the manifest's `collectors` list (its `collector_plugin_id` must match the top-level `plugin.plugin_id`):

- **Declare the write contract (`output`)**: change the target layer from the default `snapshot` to `"layer": "core"` and set the write mode to incremental upsert-dedup. The table name is given by the `CollectorSpec`'s `dataset_id`, and the on-disk path by `default_output_path_parts` in `output`:

  ```json
  {
    "name": "my_plugin.daily_limit.core",
    "display_name_zh": "每日涨跌停价格采集",
    "collector_plugin_id": "my_plugin.core_collectors",
    "dataset_id": "daily_price_limit",
    "resource_group": "tushare.http",
    "runner_entry": "my_axdata_core_collectors.runner:run",
    "output": {
      "layer": "core",
      "formats": ["parquet"],
      "default_output_path_parts": ["core", "table=daily_price_limit"],
      "write_mode": "upsert_by_key",
      "primary_key": ["ts_code", "trade_date"],
      "partition_by": ["trade_date"],
      "date_field": "trade_date"
    },
    "quality": {
      "required_columns": ["ts_code", "trade_date"],
      "primary_key": ["ts_code", "trade_date"]
    }
  }
  ```

  Write `default_output_path_parts` explicitly rather than relying on the default. There is a trap here that is very easy to fall into: when the item is omitted, the writer uses a flat `[layer, default_dir_name]`, whereas the reader expects a `core/table=<table name>` layout when the table name contains no dot. The two defaults disagree, so files do land on disk but cannot be read back — `data_browser` reports `Dataset was not found` and `client.query` reports `Core table parquet does not exist`:

  | Configuration                             | Actual on-disk path                        | Reader lookup path                      |
  | -------------------------------- | ------------------------------- | ------------------------------- |
  | `default_output_path_parts` omitted | `core/daily_price_limit/`       | `core/table=daily_price_limit/` |
  | Explicitly declared                         | `core/table=daily_price_limit/` | `core/table=daily_price_limit/` |

  AxData's `DownloadWriter` natively supports five modes: `snapshot`, `append`, `overwrite_partition` (overwrite by partition), `replace_range` (replace by closed date interval, for backfills) and `upsert_by_key` (merge and dedup by primary key). Combined with `partition_by: ["trade_date"]` + `date_field: "trade_date"`, parquet partitions are flattened into `YYYYMMDD.parquet` files; rerunning the same day dedups by primary key and replaces only that day's file, leaving historical partitions untouched.

- **Declare dependencies and quality checks (`required_datasets` and `quality`)**: adding `"required_datasets": ["trade_cal"]` lets the scheduler validate the trading-calendar dependency before running — but note that it reads the **calendar cache** at `data/cache/exchange/trade_calendar/trade_calendar.parquet`, not the `trade_cal` table written into the `core` layer.

  Understand the quality check precisely, too: `quality` is a **required** field for standalone collectors (omitting it throws `requires quality` and the whole plugin fails to register), but validation runs **after** the write. Non-negative numeric columns, primary-key uniqueness and `calendar_check` all produce a `quality_status` (`ok`/`warn`/`error`) and mark the run as `quality_failed`, yet they **do not roll back partitions already written**. In other words, it is a post-hoc audit and alert, not a pre-write gate. If you really want to block bad data, validate inside `runner_entry` first, or trigger a backfill afterwards based on `quality_status`.

### 2. Implement the `runner_entry` cleaning logic and register a scheduled task

Inside the plugin package, implement the run entry point to do just two things — fetch and standardize — and leave writing to AxData (note the return key is `meta`, not `metadata`; getting it wrong raises no error, it just silently drops your metadata):

```python
def run(*, params=None, fields=None, collector=None, data_root=None,
        output_root=None, output_dir=None, formats=None, progress_callback=None, **_):
    # 1. 拉取全市场或指定日期范围的上游数据（如涨跌停限价、历史 ST 或全量日线）
    # 2. 执行 staging 标准化：统一代码后缀（.SH/.SZ/.BJ）、对齐 YYYYMMDD 日期、转换手/千元单位
    return {
        "records": cleaned_rows,
        "meta": {"source": "custom_core_pipeline", "data_date": trade_date},
    }
```

The actual `runner_entry` convention is `module:function`. AxData filters by parameter name and passes in `params`, `fields`, `collector`, `data_root`, `output_root`, `output_dir`, `formats`, `progress_callback` and several execution options — catch the rest with `**_` in the signature. There is no `context` parameter.

Once written, install and enable the plugin (external plugins are `disabled` by default after installation and must be explicitly enabled to enter the collector registry), then register the scheduled task (or package it as an `.axp` plugin envelope to share with your team):

```powershell
# 1. 安装并启用自定义采集器插件
.\.venv\Scripts\python -m pip install -e .\my-axdata-core-collectors
.\.venv\Scripts\axdata plugin enable my_plugin.core_collectors

# 2. 注册为每个交易日盘后 18:30 自动运行的常驻任务
.\.venv\Scripts\axdata collector task add my_plugin.daily_limit.core `
  --task-id core_limit_daily `
  --trigger-type daily `
  --daily-time 18:30 `
  --formats parquet

# 3. 手动触发一次运行并等待完成
.\.venv\Scripts\axdata collector task run core_limit_daily --wait
```

Once it runs, data lands via `upsert_by_key` at `data/core/table=daily_price_limit/parquet/YYYYMMDD.parquet`, and `axdata data list` will discover it right away.

One caveat: **`client.query("daily_price_limit")` will not work just because of this.** `client.query` goes through the four tables hard-coded in `axdata_core.schema` (`stock_basic_exchange`, `trade_cal`, `daily`, `adj_factor`), and passing an unregistered table name throws `KeyError: Unknown AxData table`. To use `client.query`, add the table to `axdata_core.schema.SCHEMAS` first; if you would rather not touch the source, reading the files directly is simpler:

```python
from axdata_core import data_browser

summary = data_browser.get_dataset("daily_price_limit", data_root="data")
# summary.output_paths["parquet"] -> .../core/table=daily_price_limit/parquet
# 交给 DuckDB：read_parquet(f"{path}/**/*.parquet", hive_partitioning = false, union_by_name = true)
```

Note `hive_partitioning = false` here: `table=` is only a directory naming convention, and the `trade_date` partitions have already been flattened by `DownloadWriter` into `YYYYMMDD.parquet` files — there is no `table` column in the data. Setting it to `true` makes DuckDB conjure a phantom `table` column out of thin air.

## Final Thoughts

If what you want is a finished black box that installs and hands you ten years of cleaned full-market data for free, today's AxData may feel like "why do I still have to configure tasks and write extensions myself?" But if you have had enough of free APIs that each invent their own field names, fragile network connections and a pile of messy local CSVs, you will find that AxData has already wrapped up the most tedious parts: **parsing 257 interfaces across 9 sources, four-layer Parquet storage, the DuckDB engine, single-machine task scheduling and data quality validation**.

What it lacks most right now is exactly the community: developers taking this standardized foundation and filling in the full-market `core`-layer transformation pipelines and Collector plugins for more data sources, piece by piece. If you also work on A-share quant, give it a try on GitHub ([AxData docs](https://electkismet.github.io/AxData/index.html)), drop a star, or contribute your first `.axp` collector plugin.
