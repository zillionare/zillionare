---
title: "Moonshot 02: Mastering Monthly Backtests with Tushare & Local Caching"
date: 2025-08-15
slug: en/posts/tools/moonshot/moonshot-is-all-you-need-2
tags: [Monthly Backtest, Tushare, Price Adjustment, Local Caching]
excerpt: "Learn to efficiently fetch, adjust, and cache monthly stock data using Tushare. This guide solves Alphalens’ limitations for monthly factor testing via local caching and precise price adjustment techniques."
lang: en
translation_of: posts/tools/moonshot/moonshot-is-all-you-need-2
auto_translated: true
source_sha: 4591cd5b487f2b6b575a477df027be1d7bd8b443
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/square/food/4.jpg"
---

Being able to replicate research reports is a baseline requirement for our students. In our course, we detail the **Alphalens** factor analysis framework, which is ideal for rapid daily factor backtesting. However, Alphalens falls short when it comes to monthly strategies.

This is why we developed **Moonshot**: not only to fill this gap, but to ensure our students can apply their knowledge to live trading.

In the previous article, we introduced the core philosophy of Moonshot: you place all data (monthly opening/closing prices, factors, or trading signals) into a DataFrame indexed by month and asset code. Moonshot then executes the backtest and generates reports.

Now, let’s start from the basics of data acquisition and step-by-step master monthly strategy backtesting.

## Data Overview

The research report "Fundamental Quant Series 14" requires a wide variety of data types and preprocessing steps, making the engineering workload substantial. Using this as an example, we demonstrate how the Moonshot framework can organize and simplify complex projects.

Here is the strategy’s data checklist:

1.  **Market Data.** Essential for any strategy, at least for calculating forward returns. <!-- pro.daily -->
2.  **Dividend Yield.** Used to screen stocks by dividend yield and to calculate the two-year average dividend yield factor. <!-- pro.daily_basic -->
3.  **Dividend Data.** Only companies with continuous dividends over the past two years are eligible. <!-- pro.dividend -->
4.  **Audit Opinions.** Only companies without qualified audit opinions in the past ten years are eligible. <!-- pro.audit -->
5.  **Market Cap Data.** Only companies with a market cap greater than 5 billion RMB are eligible. <!-- pro.daily_basic -->
6.  **Net Profit, Operating Revenue, and Operating Profit Data.** Used to calculate the net profit stability factor. <!-- pro.income -->
7.  **Changes in Number of Shareholders.** <!-- pro.stk_holdernumber -->
8.  **Turnover Rate.** Used to calculate turnover volatility. <!-- pro.daily_basic -->
9.  **PE (TTM).** Used to calculate the EP factor.
10. **Operating Cash Flow Data.** Used to calculate the operating cash flow-to-assets factor. <!-- pro.cashflow_vip.n_cashflow_act-->
11. **Total Assets Data.** Together with item 10, used to calculate the operating cash flow-to-assets factor. <!-- pro.balancesheet_vip.total_assets -->
12. **Surplus Reserve Data.** Together with item 11, used to calculate the retained earnings-to-assets factor. <!-- pro.balancesheet_vip.surplus_rese -->

We will explain what each data point means, its purpose, and where to obtain it. By following this series, you will gain comprehensive experience in building fundamental monthly rebalancing strategies.

In this installment, we cover how to acquire market data via **Tushare** and apply price adjustments.

## Daily Market Data and Price Adjustment

We need to obtain market data for all individual stocks in the backtest period. After resampling, we can calculate monthly returns using the month’s opening price and the month-end closing price. Additionally, we will introduce how to efficiently implement price adjustment (adjustment for splits/dividends).

!!! tip Why Adjust Prices?
    If a stock opens at 10 RMB and executes a 10-for-10 stock split, the ex-rights price becomes 5 RMB. Assume the month closes at 6 RMB, a 20% increase from the split price. If we do not adjust prices, the calculated return would be -40%, which would clearly cause the strategy to fail.

In Tushare, we can use `daily` or `pro_bar` to fetch market data. The difference is that `pro_bar` is an integrated interface that internally calls methods like `daily`, `adj_factor`, and `daily_basic` (as needed) to fetch and align data.

We recommend mastering the basic APIs like `daily` and `adj_factor`. The reason is that with these APIs, we can store historical data locally and update market data in an append-only manner. Once historical data is cached, subsequent updates are much faster—a feat difficult to achieve with `pro_bar`.

Below is the method to fetch daily market data. Note that the returned data includes the adjustment factor. We can then freely apply forward or backward adjustment for any time period based on our needs.

```python
def fetch_bars(start: datetime.date, end: datetime.date) -> pd.DataFrame | None:
    """通过 tushare 接口，获取日线行情数据

    返回数据未复权，但包含了复权因子，因此可以增量获取叠加。返回数据为升序。

    Args:
        start: 开始日期
        end: 结束日期

    Returns:
        DataFrame: 包含date, asset, open,high,low,close,volume,amount,adj_factor
    """
    all_data = []

    pro = ts.pro_api()

    for date in pd.bdate_range(start, end):
        try:
            str_date = date.strftime("%Y%m%d")
            df = pro.daily(trade_date=str_date)
            if df.empty:
                continue

            try:
                adj_factor = pro.adj_factor(ts_code="", trade_date=str_date)
                if adj_factor.empty:
                    continue
            except Exception:
                continue

            df = pd.merge(df, adj_factor, on=["ts_code", "trade_date"], how="inner")

            # 重命名列并转换数据类型
            df = df.rename(
                columns={"trade_date": "date", "vol": "volume", "ts_code": "asset"}
            )

            # tushare返回的是字符串格式的日期，如'20231229'
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

            all_data.append(df)

        except Exception as e:
            print(f"Error loading data for {date}: {e}")
            continue

    if not all_data:
        return None

    # 合并所有数据。由获取数据逻辑知此时数据已为有序
    result = pd.concat(all_data, ignore_index=True)

    result = result[
        [
            "date",
            "asset",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "adj_factor",
        ]
    ]

    return result
```

Fetching three months of daily data takes approximately 165 seconds. However, if done incrementally (i.e., pre-storing all historical data and running daily to fetch only new data), each run takes only about 2.7 seconds.

## Price Adjustment

The daily data returned in the previous section is unadjusted. We isolate the adjustment function. First, let’s look at forward adjustment.

```python
def qfq_adjustment(
    df: pd.DataFrame, adj_factor_col: str = "adj_factor"
) -> pd.DataFrame:
    """
    前复权算法 (qfq - 前复权)
    以最新价格为基准，调整历史价格
    成交量需要反向调整，因为拆分后成交量增加

    Args:
        df: pandas DataFrame，包含asset, open, high, low, close, volume, adj_factor列
        adj_factor_col: 复权因子列名，默认为"adj_factor"

    Returns:
        复权后的pandas DataFrame
    """
    lf = pl.from_pandas(df).lazy()

    # 按asset分组，计算每个股票的最新复权因子
    result = (
        lf.with_columns(
            [pl.col(adj_factor_col).last().over("asset").alias("latest_adj_factor")]
        )
        .with_columns(
            [
                # 前复权价格计算：price * adj_factor / latest_adj_factor
                (
                    pl.col("open")
                    * pl.col(adj_factor_col)
                    / pl.col("latest_adj_factor")
                ).alias("open"),
                (
                    pl.col("high")
                    * pl.col(adj_factor_col)
                    / pl.col("latest_adj_factor")
                ).alias("high"),
                (
                    pl.col("low") * pl.col(adj_factor_col) / pl.col("latest_adj_factor")
                ).alias("low"),
                (
                    pl.col("close")
                    * pl.col(adj_factor_col)
                    / pl.col("latest_adj_factor")
                ).alias("close"),
                # 前复权成交量计算：volume * latest_adj_factor / adj_factor（反向调整）
                (
                    pl.col("volume")
                    * pl.col("latest_adj_factor")
                    / pl.col(adj_factor_col)
                ).alias("volume"),
            ]
        )
        .drop("latest_adj_factor")
        .collect()  # 执行lazy计算
    )

    return result.to_pandas()
```

Here is the code for backward adjustment:

```python
def hfq_adjustment(
    df: pd.DataFrame, adj_factor_col: str = "adj_factor"
) -> pd.DataFrame:
    """
    后复权算法 (hfq - 后复权)
    以历史价格为基准，调整后续价格
    成交量不调整，保持原始值

    Args:
        df: pandas DataFrame，包含asset, open, high, low, close, volume, adj_factor列
        adj_factor_col: 复权因子列名，默认为"adj_factor"

    Returns:
        复权后的pandas DataFrame
    """
    lf = pl.from_pandas(df).lazy()

    result = (
        lf.with_columns(
            [pl.col(adj_factor_col).last().over("asset").alias("latest_adj_factor")]
        )
        .with_columns(
            [
                # 后复权价格计算：price * latest_adj_factor / adj_factor
                (
                    pl.col("open")
                    * pl.col("latest_adj_factor")
                    / pl.col(adj_factor_col)
                ).alias("open"),
                (
                    pl.col("high")
                    * pl.col("latest_adj_factor")
                    / pl.col(adj_factor_col)
                ).alias("high"),
                (
                    pl.col("low") * pl.col("latest_adj_factor") / pl.col(adj_factor_col)
                ).alias("low"),
                (
                    pl.col("close")
                    * pl.col("latest_adj_factor")
                    / pl.col(adj_factor_col)
                ).alias("close"),
                # 后复权成交量：不调整，保持原始值
                pl.col("volume").alias("volume"),
            ]
        )
        .drop("latest_adj_factor")
        .collect()  # 执行lazy计算
    )

    # 转换回pandas DataFrame
    return result.to_pandas()
```

Note that besides the different application methods for adjustment factors, there is a significant difference in how volume is handled: for forward adjustment, we generally adjust volume; for backward adjustment, we generally keep the original values.

!!! info Why Different Volume Handling in Forward vs. Backward Adjustment?
    In forward adjustment, adjusting volume ensures logical consistency between price and volume, preventing distorted volume analysis due to price adjustments. Logically, one might think backward adjustment should also adjust volume. However, backward-adjusting volume would distort the original trading scale, affecting execution matching judgments in backtests. Therefore, whether to adjust volume depends on how the data will primarily be used. Backward adjustment of volume is permissible if there is a reasonable use case.

Here are a few additional notes on **Polars** syntax:

1.  The `lazy` method delays computation. This allows expressions written in the Python domain to be recorded as a "computation plan" rather than executed immediately (as expressions are usually executed sequentially). Data substitution and evaluation are deferred until the final evaluation, which occurs in Polars’ C domain. This reduces data format conversions between the Python and C domains, resulting in higher efficiency. In the example code, execution only occurs when `collect` is called.
2.  Regarding `with_columns`: its purpose is to add new columns to a DataFrame while allowing Polars to parallelize the execution of multiple statements passed to it (note that we pass an array). `with_columns` always returns a new DataFrame, enabling chained calls.
3.  In Polars, to perform deferred operations on DataFrame columns, you must use `.col` syntax to reference columns. If you call them via `pl["open"]`, they will be evaluated immediately, leading to unnecessary data copying and passing.
4.  Operations like `pl.col("close") * pl.col("latest_adj_factor")` generate temporary columns (unnamed). To reference them later, you must use `alias` to name these temporary result columns. The renamed results are returned along with the data copy generated by `with_columns`.

## Aside: Local Caching

Even if we only aim to replicate this research report, it is best to cache the data obtained from Tushare locally. Because our replication steps are unlikely to succeed on the first try, using cached data significantly accelerates our efficiency.

For long-term research, this is even more necessary—and we must persist in updating it. The following minimal framework demonstrates how to efficiently implement this:

```python
import polars as pl
from pathlib import Path


class ParquetUnifiedStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._start_date = None
        self._end_date = None
        self._load_date_range()

    def _load_date_range(self):
        """从文件中加载日期范围并缓存"""
        if not Path(self.file_path).exists():
            self._start_date = None
            self._end_date = None
            return

        # 使用LazyFrame提高大文件处理效率
        lazy_df = pl.scan_parquet(self.file_path)

        # 获取最小和最大日期
        date_range = lazy_df.select(
            [pl.min("date").alias("start_date"), pl.max("date").alias("end_date")]
        ).collect()

        # 缓存结果
        self._start_date = date_range[0, "start_date"]
        self._end_date = date_range[0, "end_date"]

    def _update_date_range(self, df: pl.DataFrame):
        """根据新数据更新日期范围缓存"""
        if df.is_empty():
            return

        # 获取新数据的日期范围
        new_dates = df.select(
            [pl.min("date").alias("min_date"), pl.max("date").alias("max_date")]
        )

        new_min = new_dates[0, "min_date"]
        new_max = new_dates[0, "max_date"]

        # 更新缓存的日期范围
        if self._start_date is None or new_min < self._start_date:
            self._start_date = new_min
        if self._end_date is None or new_max > self._end_date:
            self._end_date = new_max

    @property
    def start(self):
        """获取数据起始日期"""
        return self._start_date

    @property
    def end(self):
        """获取数据终止日期"""
        return self._end_date

    def append_data(self, df: pl.DataFrame | pd.DataFrame):
        """追加数据到Parquet文件"""
        if isinstance(df, pd.DataFrame):
            df = pl.from_pandas(df)

        if Path(self.file_path).exists():
            # 读取现有数据
            existing_df = pl.read_parquet(self.file_path)
            # 合并并去重
            combined_df = pl.concat([existing_df, df]).unique(["date", "asset"])
        else:
            combined_df = df

        # 按 date 和 asset 排序以优化查询
        combined_df = combined_df.sort(["date", "asset"])

        # 写入文件（自动压缩）
        combined_df.write_parquet(self.file_path, compression="snappy")

        # 更新日期范围缓存
        self._update_date_range(df)

    def query_stock_bars(
        self,
        asset: str,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
    ):
        """查询个股数据"""
        lazy_df = pl.scan_parquet(self.file_path)

        # 构建过滤条件
        filters = [pl.col("asset") == asset]

        if start_date:
            filters.append(pl.col("date") >= start_date)
        if end_date:
            filters.append(pl.col("date") <= end_date)

        return lazy_df.filter(pl.all_horizontal(filters)).collect()

    def query_cross_section(self, date: datetime.date):
        """查询截面数据"""
        return pl.scan_parquet(self.file_path).filter(pl.col("date") == date).collect()
```

The core APIs of the framework are:

1.  `append_data`: Used to append data to local storage (supports both forward and backward appending).
2.  `query_stock_bars`: Queries market data for a single stock.
3.  `query_cross_section`: Queries data for all individual stocks on a specific date.
4.  `start` and `end` attributes: Help us determine the start and end dates of the cached market data.

The following code demonstrates its usage:

```python
# 本地文件，可以存在，也可以不存在
store = ParquetUnifiedStorage("/tmp/bars.parquet")

# 获取历史行情数据
start = datetime.date(2019, 10, 8)
end = datetime.date(2019, 10, 12)
bars = fetch_bars(start, end)

# 存入本地
store.append_data(bars)

# 查询起止日期
print(store.start, store.end)

# 追加新数据
dt = datetime.date(2019, 10, 14)
bars = fetch_bars(dt, dt)
store.append_data(bars)

# 查询
print(store.end)
store.query_stock_bars("000001.SZ")
```

Now, you have the simplest local data caching framework and have acquired daily market data. In the next article, we will introduce how to acquire dividend yield data and call Moonshot to screen stocks by dividend yield and verify the screening results.
