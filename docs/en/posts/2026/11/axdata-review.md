---
title: "AxData: More Than Just Another Quant Data Source"
date: 2026-11-09
slug: en/posts/tools/axdata-review
tags: [Quant Data Infrastructure, Factor Investing, Open Source, DuckDB]
excerpt: "AxData pairs pluggable multi-source access with local Parquet/DuckDB tiered storage, keeping core A-share data on disk so backtests run faster without rate limits. Open source and community-built."
lang: en
translation_of: posts/tools/axdata-review
auto_translated: true
source_sha: 509796be99114008e198a2a15e6bc6a391c5f55c
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261111101854-axdata-review.jpg"
---

When you start doing quant work on China A-shares, the first roadblock is where to get your data. You've probably already tried AKShare, Pytdx, Tushare, JQData, BaoStock, xtquant, and others. And there's one unavoidable problem:

Free data comes with **rate limits**, **coverage limits**, and **history limits**. Rate limits mean the server only lets you call the API so many times per minute, or return so many rows. Coverage limits mean whether you're allowed to obtain certain critical data at all — historical ST status and historical price-limit data, for instance, sit behind paid tiers or high point thresholds on some sources. History limits mean the maximum lookback span you're permitted when pulling data.

On top of that, the data sources themselves aren't reliably stable. Some block web scrapers to push their own skill packages and quant platform suites; others shut down for policy reasons.

An ideal solution is to **spread data requests across multiple sources and enable standardized local storage.** Once local storage is in place, historical requests read straight from local disk instead of repeatedly hitting remote servers — that removes rate limits entirely and speeds up backtests dramatically. You can also break through history limits by importing data externally or backfilling at low frequency. And using multiple sources lets you combine the strengths of each, unlocking coverage limits.

AxData is a quant data solution evolving in exactly this direction. It's still under active development — first published on GitHub four months ago, and it hasn't even hit 1k stars yet. Frankly, it is not yet a "finished database" that you install and it automatically pulls ten years of full-market history. But because it's essentially the first open-source project to make <b>"pluggable multi-source ingestion + tiered local Parquet/DuckDB storage + unified SDK/HTTP data serving"</b> work under a rigorous engineering architecture, we think it's well worth recommending. After all, the only thing that keeps an open-source project moving is attention and contributions from the community.


## /01 AxData's dual-track design at a glance

From a strategy developer's point of view, the ideal data experience would be a single unified semantic API: you just declare "which instruments, which time range," and the API works out which data can be read locally and which needs to be fetched remotely and cached automatically.

Probably because reconciling different data sources is hard, AxData only puts a very small set of core data into local storage — collected on a schedule and read locally at use time. Most data still goes through remote fetch. So AxData currently runs a dual-track approach to data.


![AxData data pipeline](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261112131455-mermaid-axdata-review.jpg)

As the diagram shows, AxData delivers excellent engineering order:


- **Left track (collect and store)**: only data explicitly pulled through Collector tasks (triggered manually or scheduled on trading days) passes through queue throttling and quality checks, then lands as open **Parquet** files under the `raw -> staging -> core -> factor` four-layer model, with **DuckDB** providing blazing-fast local SQL and view queries.
- **Right track (direct fetch)**: when you call `client.call()` or `POST /v1/request/*`, the system validates parameters at the gateway, requests upstream, normalizes fields, and returns directly — **no disk write by default**. Good for intraday monitoring, API debugging, or ad-hoc pulls.
- **Seamless local/LAN switching**: the Python SDK reads Parquet/DuckDB directly on the local machine with no background service needed. On a LAN you just start the HTTP API (port `8666`) and other machines pass `api_base` to run the exact same code remotely; the web console (port `8667`) handles visual management of tasks, plugins, and data quality.


## /02 The full picture: 9 data sources, 257 interfaces

If you only look at the local core tables, you might underestimate AxData's coverage. In fact, at the "direct fetch" layer, AxData already ships preinstalled plugins connecting **9 major source categories, 257 data interfaces in total** — covering not only traditional A-share price/volume and fundamentals, but extending to futures, options, convertible bonds, and that very distinctive A-share category: short-term limit-up chasing and thematic sentiment data.

We've organized them by source below (search the project docs site for specific API names):

| Data source                      | Core data types covered                                                                                                                                                                                                                                                                                         | Role in quant practice and usage constraints                                                                                                                                                                      |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TDX (通达信)** <br>(91)         | **Stock/ETF/index** basic lists, price-limit bounds, pre-market share capital, ST/suspension lists; daily/weekly/monthly/minute/second K-lines, adjustment factors; current and historical intraday series, tick-by-tick trades, call auction detail; five-level order book, real-time snapshots and incremental streams; F10 financials, chip distribution, smart-money control, consecutive limit-up ladder, thematic strength.                                                                                    | **The A-share price/volume and short-term smart-money source**. Built on a 7709-protocol Actor connection pool (multi-server failover plus WebSocket real-time streaming). Currently the only source with 8 independent scheduled collectors built in by default.                                         |
| **Sina Finance** <br>(60)       | **Options** (CFFEX index options, SSE option quotes and Greeks, commodity options), **futures** (main continuous contracts, daily/minute bars, open-interest rankings, realized volatility), **bonds and convertible bonds** (China/US Treasury yields, convertible bond overview), **funds/ETFs** (AUM, dividends), A-share three financial statements as JSON, Dragon-Tiger list seat tracking, lock-up expiries, ESG scores, HK/US stocks and global indices, BOC FX rates.                  | **A treasure trove of derivatives and cross-market data**. Fills in the option Greeks, commodity/index futures minute bars, and structured financial statements that free sources sorely lack; it's a public HTTP interface, currently direct-fetch only (`source_request-only`) by default — high-frequency calls need to watch out for anti-scraping throttling. |
| **CNINFO (巨潮资讯)** <br>(32)       | **Listed company announcements** (announcement lists, PDF metadata, scheduled disclosures, research-call announcements), **Hudongyi investor Q&A** (questions and board-secretary replies), **corporate governance** (share pledges, external guarantees, litigation), **share capital and shareholders** (executive buying/selling, shareholder counts and concentration, controller changes, rights-issue plans), **bond/convertible bond issuance and conversion**, fund heavy holdings and asset allocation, IPOs and listing-committee approvals, industry classification and P/E. | **Fundamentals, event-driven, and alternative data**. Official disclosure standard — ideal for event-driven strategies (sharp drops in shareholder count, executive buying, NLP on research-call text); announcement PDFs return only metadata and download links and are not stored by default.                            |
| **TDX extended quotes** <br>(31) | **Futures** (contract lists, K-lines, intraday series, current/historical ticks, real-time snapshots), **options** (contract lists, T-shaped quote chain, K-lines, intraday), **bonds**, **funds** (NAV and trends), **FX** (K-lines, intraday, ticks), **macro indicators** (lists, snapshots, series).                                                                                                | **Multi-asset high-frequency and history supplement**. Independent of the regular TDX plugin (`axdata-source-tdx-ext`); provides option T-shaped quotes with up to 55 fields and futures/FX tick detail; requires a TDX server that supports extended quotes.                              |
| **Eastmoney (东方财富)** <br>(13)       | Real-time snapshots for A-shares and broad indices, **industry/concept sectors** (real-time sector quotes, constituents, a stock's sector memberships), **short-term pools** (limit-up pool, limit-down pool, yesterday's limit-ups today, order-book anomaly detail), **daily Dragon-Tiger list summary**, **margin trading detail**, individual stock research report lists.                                                                                                    | **The go-to for sector mapping and intraday anomalies**. Sector constituents and order-book anomaly categories (large buys, limit-up sealing) are extremely granular; it's a public HTTP interface with no default scheduled collector — guard against IP bans from high-frequency requests.                                                   |
| **Cailianshe (财联社)** <br>(12)         | Telegraph news flashes, **market sentiment**, today's mainline opportunities, today's hot sectors and leading stocks, sector heat rankings, sector rotation, limit-up pool with limit-up reasons, intraday series and K-lines for individual stocks.                                                                                                                                                                                  | **Thematic hotspots and text sentiment**. The limit-up pool directly attaches editor-distilled "limit-up reasons," making it extremely well suited to short-term theme mining and public-opinion monitoring; mostly same-day cross-sectional data with little long history.                                                        |
| **Kaipanhong (开盘红)** <br>(9)          | **Historical limit-up/limit-down stocks**, historical limit-up review, **historical sector constituents**, historical bellwethers, limit-up ladder, market sentiment, sector rankings, market recap events.                                                                                                                                                                                            | **A rare historical short-term review source**. Fills the gap where ordinary free sources "only have today's hotspots, with no historical sector constituents or historical limit-up/limit-down review" — ideal for backtesting limit-up chasing and relay strategies.                                                                  |
| **Tencent Finance** <br>(6)        | A-share historical daily bars, index historical daily bars, earliest-history-year lookup, A-share real-time quote lists, real-time snapshots, A-share tick data.                                                                                                                                                                                                                   | **A lightweight, stable backup quote source**. Fast HTTP responses and simple structure — good for lightweight real-time snapshot polling or cross-checking against TDX daily bars; direct-fetch only by default, and it does not automatically replace TDX for storage.                                                         |
| **Exchanges** <br>(3)          | **Trading calendar** (SSE/SZSE/BSE), **stock basic info** (official listing status, industry, total/float shares, VIE/profitability flags), **historical stock lists**.                                                                                                                                                                            | **System-level authoritative master data**. `trade_cal` has been productized as a system base-data cache; every daily quote collection job depends on it for trading-day alignment and gap checks before it runs.                                                                   |


## /03 A deliberately minimal Core layer

Having seen the rich direct-fetch interfaces, let's return to the heart of it: local backtest storage.

First, a question: for quant people, **what is the minimum dataset that must be included?** On the face of it, the answer depends on your strategy, since different strategies need different data.
A **minimal quant backtest data subset** must contain all six of the following:

1. **Calendar** (determines trading days and drives the time axis)
2. **Security list** (with listing/delisting dates, eliminating survivorship bias)
3. **Daily OHLC, Volume, Amount** (basic price/volume facts)
4. **Daily adjustment factors** (to compute forward/backward-adjusted prices dynamically)
5. **Daily price limit bounds** (whether you can buy at limit-up or sell at limit-down)
6. **Daily ST list** (determines whether the 5% or 10%/20% band applies, plus instrument filtering)

That said, AxData's Core layer doesn't yet provide all of these. Its `core` (core fact table) layer currently defines only the first four tables: `trade_cal` (trading calendar), `stock_basic_exchange` (stock list), `daily` (unadjusted daily bars), and `adj_factor` (adjustment factors). Judged on the `core` layer alone, it indeed doesn't fully cover the minimal backtest subset, and the default jobs only pull a small sample of `000001.SZ` — there's no out-of-the-box full-market historical database.

There are two reasons for this. The AxData author considers the ST list obtained via TDX to be only a current snapshot rather than point-in-time (PIT) data, and until that's solved it can't be written into the core layer.

- `tdx.stock_daily_price_limit_tdx.snapshot` (daily price limit bounds)
- `tdx.stock_st_list_tdx.snapshot` (ST stock list)
- `tdx.stock_suspensions_tdx.snapshot` (suspension/resumption list)
- `tdx.stock_daily_share_tdx.snapshot` (daily pre-market share capital)

Accumulating these snapshots over time can eventually fill in this data. But a faster route is to extend AxData and pull in data from other sources — historical ST lists, for example, can be obtained from BaoStock. Below, we use fetching historical price-limit data from Tushare as an example to show how to extend AxData.


## /04 Hands-on: how to extend AxData

Once you understand AxData's architectural boundaries, you'll see it is essentially <b>a quant data foundation that has already built the task scheduler, concurrency resource pool, Parquet writer, quality checker, and DuckDB query engine for you</b>.

If you want to really persist the **daily price limit bounds**, **historical ST lists**, **full-market daily bars**, or **Kaipanhong's historical limit-up/limit-down data and Sina's financial statements** into the local `core` layer to form a complete proprietary backtest database, you only need two extension steps following AxData's plugin spec:

### 1. Write a standalone Collector plugin

In AxData, data source interfaces (Provider) and collectors (Collector) are decoupled. To get data stored on a schedule, create a lightweight Python plugin package (declare the `axdata.plugins` entry point in `pyproject.toml` and include an `axdata-plugin.json` manifest file). In the manifest's `collectors` list, declare a `CollectorSpec` (its `collector_plugin_id` must match the top-level `plugin.plugin_id` in the manifest):

- **Declare the write contract (`output`)**: change the target layer from the default `snapshot` to `"layer": "core"`, and declare the write mode as incremental, deduplicated upsert. The table name is given by the `CollectorSpec`'s `dataset_id`, and the on-disk path by `default_output_path_parts` in `output`:

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

  It's best to write `default_output_path_parts` explicitly rather than relying on the default. Here's a trap that's very easy to fall into: when this field is omitted, the writer falls back to a flat `[layer, default_dir_name]`, while the reader expects a `core/table=<table_name>` layout whenever the table name contains no dot. The mismatched defaults mean the file lands on disk but can't be read back — `data_browser` reports `Dataset was not found`, and `client.query` reports `Core table parquet does not exist`:

  | Config                             | Actual on-disk path                        | Path the reader looks up                      |
  | -------------------------------- | ------------------------------- | ------------------------------- |
  | Omit `default_output_path_parts` | `core/daily_price_limit/`       | `core/table=daily_price_limit/` |
  | Declare explicitly                         | `core/table=daily_price_limit/` | `core/table=daily_price_limit/` |

  AxData's `DownloadWriter` natively supports five modes: `snapshot`, `append`, `overwrite_partition` (overwrite by partition), `replace_range` (replace a closed date range, for backfills), and `upsert_by_key` (merge and dedupe by primary key). Combined with `partition_by: ["trade_date"]` + `date_field: "trade_date"`, Parquet partitions get flattened into `YYYYMMDD.parquet` files; rerunning the same day auto-dedupes by primary key and replaces only that day's file, leaving historical partitions untouched.

- **Declare dependencies and quality checks (`required_datasets` and `quality`)**: adding `"required_datasets": ["trade_cal"]` lets the scheduler validate the trading-calendar dependency before running — but note that it reads the **calendar cache** at `data/cache/exchange/trade_calendar/trade_calendar.parquet`, not the `trade_cal` table written into the `core` layer.

  Quality checks also need a more precise reading: `quality` is **mandatory** for a standalone collector (missing it throws `requires quality` and the entire plugin fails to register), but validation happens **after** the write. Non-negative numeric columns, primary-key uniqueness, and `calendar_check` all produce a `quality_status` (`ok`/`warn`/`error`) and mark the run as `quality_failed`, yet they **do not roll back partitions already written**. In other words, it's a post-hoc audit and alert, not a pre-write gate. If you really want to block bad data, validate it yourself first inside `runner_entry`, or use `quality_status` afterwards to trigger a backfill.

### 2. Implement the `runner_entry` cleaning logic and register a scheduled task

Implement the run entry point in the plugin package doing just two things — "fetch + standardize" — and leave persistence to AxData (note the return key is `meta`, not `metadata`; a typo won't raise an error, it will just silently drop the metadata):

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

The actual calling convention for `runner_entry` is `module:function`; AxData filters by parameter name and passes `params`, `fields`, `collector`, `data_root`, `output_root`, `output_dir`, `formats`, `progress_callback`, and several execution options — just absorb them all with `**_` in the signature. There is no `context` parameter.

Once written, install and enable the plugin (external plugins default to `disabled` after install and must be explicitly enabled before they enter the collector registry), then register the scheduled task (or package it as an `.axp` plugin envelope to share with your team):

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

Keep in mind that **`client.query("daily_price_limit")` still won't work just because of this**: `client.query` goes through the four tables hard-coded in `axdata_core.schema` (`stock_basic_exchange`, `trade_cal`, `daily`, `adj_factor`), and passing an unregistered table name throws `KeyError: Unknown AxData table`. To use `client.query`, you'd first have to add the table to `axdata_core.schema.SCHEMAS`; if you'd rather not touch the source, reading the files directly is simpler:

```python
from axdata_core import data_browser

summary = data_browser.get_dataset("daily_price_limit", data_root="data")
# summary.output_paths["parquet"] -> .../core/table=daily_price_limit/parquet
# 交给 DuckDB：read_parquet(f"{path}/**/*.parquet", hive_partitioning = false, union_by_name = true)
```

Note the use of `hive_partitioning = false` here: `table=` is only a directory naming convention, and the `trade_date` partitions have already been flattened by `DownloadWriter` into `YYYYMMDD.parquet` files — there is no actual `table` column in the data. Setting it to `true` makes DuckDB conjure a phantom `table` column out of thin air.

## Final thoughts

If what you want is a finished black box that installs and hands you ten years of cleaned full-market data for free, AxData at this stage may leave you thinking "why do I still have to configure tasks and write extensions myself?" But if you're fed up with the inconsistent field naming of free APIs, fragile network connections, and messy local CSV files, you'll find that AxData has already packaged up the most tedious parts: **parsing 257 interfaces across 9 sources, four-layer Parquet storage, the DuckDB engine, single-machine task scheduling, and data quality validation**.

What it lacks most right now is exactly what community developers can supply: filling in the full-market `core`-layer transformation pipelines and Collector plugins for more data sources, piece by piece, on top of this standardized foundation. If you're working on China A-shares quant too, give it a try on GitHub ([AxData docs](https://electkismet.github.io/AxData/index.html)), leave a star, or contribute your first `.axp` collector plugin.
