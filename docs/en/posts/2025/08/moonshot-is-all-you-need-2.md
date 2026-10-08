---
title: "Moonshot 02: Mastering Monthly Backtests with Tushare & Local Caching ===EXCUTIVE SUMMARY=== This article details how to efficiently fetch, adjust, and cache monthly stock data using Tushare. It explains forward/backward adjustment logic and implements a local Parquet caching framework to accelerate complex factor mining and backtesting workflows. ===TAGS=== Factor Mining, Backtesting, Data Engineering, Tushare ===BODY=== Being able to replicate research reports is a baseline requirement for our students. In our course, we introduce the **Alphalens** factor analysis framework, which is ideal for rapid daily-factor backtesting. However, Alphalens falls short when handling monthly strategies.  This is why we developed **Moonshot**: not just to fill this gap, but to ensure our students can apply their knowledge to live trading.  In the previous post, we outlined Moonshot’s core philosophy: you feed all data (monthly open/close prices, factors, or trading signals) into a DataFrame indexed by month and asset code. Moonshot then executes the backtest and generates reports.  Now, we start from the basics of data acquisition, guiding you step-by-step through monthly strategy backtesting.  ## Data Overview  The research report *\"Fundamental Quant Series 14\"* requires a wide variety of data types and preprocessing steps, making the engineering effort substantial. Using this as an example, we demonstrate how the Moonshot framework can organize and simplify complex projects.  Here is the strategy’s data checklist:  1.  **Market Data.** Essential for any strategy, at least for calculating forward returns. <!-- pro.daily --> 2.  **Dividend Yield.** Used to screen stocks by dividend yield and to calculate the two-year average dividend yield factor. <!-- pro.daily_basic --> 3.  **Dividend Data.** Only companies with continuous dividends over the past two years are eligible. <!-- pro.dividend --> 4.  **Audit Opinions.** Only companies without qualified audit opinions over the past ten years are eligible. <!-- pro.audit --> 5.  **Market Cap Data.** Only companies with a market cap > 5 billion RMB are eligible. <!-- pro.daily_basic --> 6.  **Net Profit, Operating Revenue, and Operating Profit.** Used to calculate the net profit stability factor. <!-- pro.income --> 7.  **Changes in Shareholder Count.** <!-- pro.stk_holdernumber --> 8.  **Turnover Rate.** Used to calculate turnover volatility. <!-- pro.daily_basic --> 9.  **PE (TTM).** Used to calculate the EP factor. 10. **Operating Cash Flow Data.** Used to calculate the operating cash flow-to-assets factor. <!-- pro.cashflow_vip.n_cashflow_act --> 11. **Total Assets.** Used with item 10 to calculate the operating cash flow-to-assets factor. <!-- pro.balancesheet_vip.total_assets --> 12. **Surplus Reserve.** Used with item 11 to calculate the retained earnings-to-assets factor. <!-- pro.balancesheet_vip.surplus_rese -->  We will explain what each data point represents, its purpose, and where to obtain it. By following this series, you will gain comprehensive experience in building fundamental monthly-rebalancing strategies.  In this installment, we cover how to acquire market data via **Tushare** and apply price adjustments.  ## Daily Market Data and Price Adjustment  We need to acquire market data for all stocks in the backtest period. After resampling, we can calculate monthly returns using the month-start open price and month-end close price. Additionally, we will demonstrate how to efficiently implement price adjustment (adjustment factor application).  !!! tip Why Adjust Prices?     If a stock opens at 10 RMB and executes a \"10 shares for 10 bonus\" split, the ex-rights price drops to 5 RMB. If it closes at 6 RMB that month, the nominal return is +20%. Without adjustment, the calculated return would be -40%, causing the strategy to fail.  In Tushare, we can use `daily` or `pro_bar` to fetch market data. The difference lies in implementation: `pro_bar` is an integrated interface that internally calls `daily`, `adj_factor`, `daily_basic`, etc., to fetch and align data.  We recommend mastering the basic APIs `daily` and `adj_factor`. Why? Because these APIs allow us to store historical data locally and update it incrementally. Once historical data is cached, subsequent updates are much faster—a feat difficult to achieve with `pro_bar`.  Below is the method to fetch daily market data. Note that the returned data includes the adjustment factor, allowing you to freely apply forward or backward adjustment to any time period.  ```python def fetch_bars(start: datetime.date, end: datetime.date) -> pd.DataFrame | None:     \"\"\"Fetch daily market data via Tushare interface      Returns unadjusted data but includes the adjustment factor, enabling incremental updates. Data is sorted ascending.      Args:         start: Start date         end: End date      Returns:         DataFrame: Contains date, asset, open, high, low, close, volume, amount, adj_factor     \"\"\"     all_data = []      pro = ts.pro_api()      for date in pd.bdate_range(start, end):         try:             str_date = date.strftime(\"%Y%m%d\")             df = pro.daily(trade_date=str_date)             if df.empty:                 continue              try:                 adj_factor = pro.adj_factor(ts_code=\"\", trade_date=str_date)                 if adj_factor.empty:                     continue             except Exception:                 continue              df = pd.merge(df, adj_factor, on=[\"ts_code\", \"trade_date\"], how=\"inner\")              # Rename columns and convert data types             df = df.rename(                 columns={\"trade_date\": \"date\", \"vol\": \"volume\", \"ts_code\": \"asset\"}             )              # Tushare returns dates as strings, e.g., '20231229'             df[\"date\"] = pd.to_datetime(df[\"date\"], format=\"%Y%m%d\")              all_data.append(df)          except Exception as e:             print(f\"Error loading data for {date}: {e}\")             continue      if not all_data:         return None      # Concatenate all data. Based on the fetch logic, data is already ordered     result = pd.concat(all_data, ignore_index=True)      result = result[         [             \"date\",             \"asset\",             \"open\",             \"high\",             \"low\",             \"close\",             \"volume\",             \"amount\",             \"adj_factor\",         ]     ]      return result ```  Fetching three months of daily data takes approximately 165 seconds. If performed incrementally (i.e., pre-storing all historical data and running daily to fetch only new data), a single run takes only about 2.7 seconds.  ## Price Adjustment  The daily data returned in the previous section is unadjusted. We isolate the adjustment functions. First, forward adjustment.  ```python def qfq_adjustment(     df: pd.DataFrame, adj_factor_col: str = \"adj_factor\" ) -> pd.DataFrame:     \"\"\"     Forward Adjustment Algorithm (qfq - Forward Adjustment)     Adjusts historical prices based on the latest price.     Volume must be adjusted inversely, as splits increase volume.      Args:         df: pandas DataFrame containing asset, open, high, low, close, volume, adj_factor columns         adj_factor_col: Name of the adjustment factor column, default is \"adj_factor\"      Returns:         Adjusted pandas DataFrame     \"\"\"     lf = pl.from_pandas(df).lazy()      # Group by asset and calculate the latest adjustment factor for each stock     result = (         lf.with_columns(             [pl.col(adj_factor_col).last().over(\"asset\").alias(\"latest_adj_factor\")]         )         .with_columns(             [                 # Forward adjustment price calculation: price * adj_factor / latest_adj_factor                 (                     pl.col(\"open\")                     * pl.col(adj_factor_col)                     / pl.col(\"latest_adj_factor\")                 ).alias(\"open\"),                 (                     pl.col(\"high\")                     * pl.col(adj_factor_col)                     / pl.col(\"latest_adj_factor\")                 ).alias(\"high\"),                 (                     pl.col(\"low\") * pl.col(adj_factor_col) / pl.col(\"latest_adj_factor\")                 ).alias(\"low\"),                 (                     pl.col(\"close\")                     * pl.col(adj_factor_col)                     / pl.col(\"latest_adj_factor\")                 ).alias(\"close\"),                 # Forward adjustment volume calculation: volume * latest_adj_factor / adj_factor (inverse adjustment)                 (                     pl.col(\"volume\")                     * pl.col(\"latest_adj_factor\")                     / pl.col(adj_factor_col)                 ).alias(\"volume\"),             ]         )         .drop(\"latest_adj_factor\")         .collect()  # Execute lazy computation     )      return result.to_pandas() ```  Here is the code for backward adjustment:  ```python def hfq_adjustment(     df: pd.DataFrame, adj_factor_col: str = \"adj_factor\" ) -> pd.DataFrame:     \"\"\"     Backward Adjustment Algorithm (hfq - Backward Adjustment)     Adjusts subsequent prices based on historical prices.     Volume is not adjusted; original values are kept.      Args:         df: pandas DataFrame containing asset, open, high, low, close, volume, adj_factor columns         adj_factor_col: Name of the adjustment factor column, default is \"adj_factor\"      Returns:         Adjusted pandas DataFrame     \"\"\"     lf = pl.from_pandas(df).lazy()      result = (         lf.with_columns(             [pl.col(adj_factor_col).last().over(\"asset\").alias(\"latest_adj_factor\")]         )         .with_columns(             [                 # Backward adjustment price calculation: price * latest_adj_factor / adj_factor                 (                     pl.col(\"open\")                     * pl.col(\"latest_adj_factor\")                     / pl.col(adj_factor_col)                 ).alias(\"open\"),                 (                     pl.col(\"high\")                     * pl.col(\"latest_adj_factor\")                     / pl.col(adj_factor_col)                 ).alias(\"high\"),                 (                     pl.col(\"low\") * pl.col(\"latest_adj_factor\") / pl.col(adj_factor_col)                 ).alias(\"low\"),                 (                     pl.col(\"close\")                     * pl.col(\"latest_adj_factor\")                     / pl.col(adj_factor_col)                 ).alias(\"close\"),                 # Backward adjustment volume: No adjustment, keep original value                 pl.col(\"volume\").alias(\"volume\"),             ]         )         .drop(\"latest_adj_factor\")         .collect()  # Execute lazy computation     )      # Convert back to pandas DataFrame     return result.to_pandas() ```  Note that besides the different application methods for adjustment factors, there is a significant difference in how volume is handled: for forward adjustment, we generally adjust volume; for backward adjustment, we generally keep the original values.  !!! info Why Different Volume Handling in Forward vs. Backward Adjustment?     In forward adjustment, adjusting volume ensures logical consistency between price and volume, preventing distorted volume analysis due to price adjustments. Logically, backward adjustment should also adjust volume. However, adjusting volume in backward adjustment would distort the original trading scale, affecting order matching judgments in backtests. Therefore, whether to adjust volume depends on how the data is typically used. Adjusting volume in backward adjustment is permissible if there is a reasonable use case.  Here is a supplementary note on **Polars** syntax. The `lazy` method delays computation, meaning expressions written in the Python domain are not executed immediately (as they would be sequentially) but are recorded as a \"computation plan.\" Data substitution and evaluation are deferred until the final evaluation, executed in Polars' C domain. This reduces data format conversions between the Python and C domains, enhancing efficiency. In the example code, execution occurs only when `collect` is called.  Second, regarding `with_columns`: its purpose is to add new columns to a DataFrame while allowing Polars to parallelize the execution of multiple passed statements (note that we pass an array). `with_columns` always returns a new DataFrame, enabling chained calls.  Third, in Polars, to reference columns for delayed operations in a DataFrame, you must use the `.col` syntax. If you call it via `pl[\"open\"]`, it will be evaluated immediately, causing unnecessary data copying and transmission.  Finally, operations like `pl.col(\"close\") * pl.col(\"latest_adj_factor\")` generate temporary columns (unnamed). To reference them later, you must call `alias` to name the temporary result columns. The renamed results are returned along with the data copy generated by `with_columns`.  ## Sidebar: Local Caching  Even if we are only replicating this research report, it is best to cache the data obtained from Tushare. Our replication steps are unlikely to succeed on the first try. Using cached data significantly accelerates our efficiency.  If this is for long-term research, doing so is even more necessary—and you must persist in updating it. The following minimal framework demonstrates how to efficiently implement this:  ```python import polars as pl from pathlib import Path   class ParquetUnifiedStorage:     def __init__(self, file_path: str):         self.file_path = file_path         self._start_date = None         self._end_date = None         self._load_date_range()      def _load_date_range(self):         \"\"\"Load date range from file and cache\"\"\"         if not Path(self.file_path).exists():             self._start_date = None             self._end_date = None             return          # Use LazyFrame for efficient large-file processing         lazy_df = pl.scan_parquet(self.file_path)          # Get min and max dates         date_range = lazy_df.select(             [pl.min(\"date\").alias(\"start_date\"), pl.max(\"date\").alias(\"end_date\")]         ).collect()          # Cache results         self._start_date = date_range[0, \"start_date\"]         self._end_date = date_range[0, \"end_date\"]      def _update_date_range(self, df: pl.DataFrame):         \"\"\"Update cached date range based on new data\"\"\"         if df.is_empty():             return          # Get date range of new data         new_dates = df.select(             [pl.min(\"date\").alias(\"min_date\"), pl.max(\"date\").alias(\"max_date\")]         )          new_min = new_dates[0, \"min_date\"]         new_max = new_dates[0, \"max_date\"]          # Update cached date range         if self._start_date is None or new_min < self._start_date:             self._start_date = new_min         if self._end_date is None or new_max > self._end_date:             self._end_date = new_max      @property     def start(self):         \"\"\"Get data start date\"\"\"         return self._start_date      @property     def end(self):         \"\"\"Get data end date\"\"\"         return self._end_date      def append_data(self, df: pl.DataFrame | pd.DataFrame):         \"\"\"Append data to Parquet file\"\"\"         if isinstance(df, pd.DataFrame):             df = pl.from_pandas(df)          if Path(self.file_path).exists():             # Read existing data             existing_df = pl.read_parquet(self.file_path)             # Merge and deduplicate             combined_df = pl.concat([existing_df, df]).unique([\"date\", \"asset\"])         else:             combined_df = df          # Sort by date and asset to optimize queries         combined_df = combined_df.sort([\"date\", \"asset\"])          # Write to file (automatic compression)         combined_df.write_parquet(self.file_path, compression=\"snappy\")          # Update cached date range         self._update_date_range(df)      def query_stock_bars(         self,         asset: str,         start_date: datetime.date = None,         end_date: datetime.date = None,     ):         \"\"\"Query individual stock data\"\"\"         lazy_df = pl.scan_parquet(self.file_path)          # Build filter conditions         filters = [pl.col(\"asset\") == asset]          if start_date:             filters.append(pl.col(\"date\") >= start_date)         if end_date:             filters.append(pl.col(\"date\") <= end_date)          return lazy_df.filter(pl.all_horizontal(filters)).collect()      def query_cross_section(self, date: datetime.date):         \"\"\"Query cross-sectional data for a specific date\"\"\"         return pl.scan_parquet(self.file_path).filter(pl.col(\"date\") == date).collect() ```  The core APIs of the framework are:  1.  `append_data`: Appends data to local storage (supports both forward and backward appending). 2.  `query_stock_bars`: Queries market data for a single stock. 3.  `query_cross_section`: Queries data for all stocks on a specific date. 4.  `start` and `end` properties: Help determine the start and end dates of the locally cached market data.  The following code demonstrates its usage:  ```python # Local file; may or may not exist yet store = ParquetUnifiedStorage(\"/tmp/bars.parquet\")  # Fetch historical market data start = datetime.date(2019, 10, 8) end = datetime.date(2019, 10, 12) bars = fetch_bars(start, end)  # Store locally store.append_data(bars)  # Query start and end dates print(store.start, store.end)  # Append new data dt = datetime.date(2019, 10, 14) bars = fetch_bars(dt, dt) store.append_data(bars)  # Query print(store.end) store.query_stock_bars(\"000001.SZ\") ```  Now you have the simplest local data caching framework and have acquired daily market data. In the next article, we will cover how to acquire dividend yield data and call Moonshot to screen stocks by dividend yield and verify the screening results."
date: 2025-08-15
slug: en/posts/tools/moonshot/moonshot-is-all-you-need-2
tags: [Factor Mining, Backtesting, Data Engineering, Tushare]
excerpt: "月频回测总踩复权坑？手把手教你用Tushare抓行情、前复权/后复权实战+Parquet本地缓存提速60倍，轻松复刻基本面量化研报。"
lang: en
translation_of: posts/tools/moonshot/moonshot-is-all-you-need-2
auto_translated: true
source_sha: 4591cd5b487f2b6b575a477df027be1d7bd8b443
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/square/food/4.jpg"
---

Being able to replicate research reports is a baseline requirement for our students. In our course, we introduce the **Alphalens** factor analysis framework, which is ideal for rapid daily-factor backtesting. However, Alphalens falls short when handling monthly strategies.

This is why we developed **Moonshot**: not just to fill this gap, but to ensure our students can apply their knowledge to live trading.

In the previous post, we outlined Moonshot’s core philosophy: you feed all data (monthly open/close prices, factors, or trading signals) into a DataFrame indexed by month and asset code. Moonshot then executes the backtest and generates reports.

Now, we start from the basics of data acquisition, guiding you step-by-step through monthly strategy backtesting.

## Data Overview

The research report *"Fundamental Quant Series 14"* requires a wide variety of data types and preprocessing steps, making the engineering effort substantial. Using this as an example, we demonstrate how the Moonshot framework can organize and simplify complex projects.

Here is the strategy’s data checklist:

1.  **Market Data.** Essential for any strategy, at least for calculating forward returns. <!-- pro.daily -->
2.  **Dividend Yield.** Used to screen stocks by dividend yield and to calculate the two-year average dividend yield factor. <!-- pro.daily_basic -->
3.  **Dividend Data.** Only companies with continuous dividends over the past two years are eligible. <!-- pro.dividend -->
4.  **Audit Opinions.** Only companies without qualified audit opinions over the past ten years are eligible. <!-- pro.audit -->
5.  **Market Cap Data.** Only companies with a market cap > 5 billion RMB are eligible. <!-- pro.daily_basic -->
6.  **Net Profit, Operating Revenue, and Operating Profit.** Used to calculate the net profit stability factor. <!-- pro.income -->
7.  **Changes in Shareholder Count.** <!-- pro.stk_holdernumber -->
8.  **Turnover Rate.** Used to calculate turnover volatility. <!-- pro.daily_basic -->
9.  **PE (TTM).** Used to calculate the EP factor.
10. **Operating Cash Flow Data.** Used to calculate the operating cash flow-to-assets factor. <!-- pro.cashflow_vip.n_cashflow_act -->
11. **Total Assets.** Used with item 10 to calculate the operating cash flow-to-assets factor. <!-- pro.balancesheet_vip.total_assets -->
12. **Surplus Reserve.** Used with item 11 to calculate the retained earnings-to-assets factor. <!-- pro.balancesheet_vip.surplus_rese -->

We will explain what each data point represents, its purpose, and where to obtain it. By following this series, you will gain comprehensive experience in building fundamental monthly-rebalancing strategies.

In this installment, we cover how to acquire market data via **Tushare** and apply price adjustments.

## Daily Market Data and Price Adjustment

We need to acquire market data for all stocks in the backtest period. After resampling, we can calculate monthly returns using the month-start open price and month-end close price. Additionally, we will demonstrate how to efficiently implement price adjustment (adjustment factor application).

!!! tip Why Adjust Prices?
    If a stock opens at 10 RMB and executes a "10 shares for 10 bonus" split, the ex-rights price drops to 5 RMB. If it closes at 6 RMB that month, the nominal return is +20%. Without adjustment, the calculated return would be -40%, causing the strategy to fail.

In Tushare, we can use `daily` or `pro_bar` to fetch market data. The difference lies in implementation: `pro_bar` is an integrated interface that internally calls `daily`, `adj_factor`, `daily_basic`, etc., to fetch and align data.

We recommend mastering the basic APIs `daily` and `adj_factor`. Why? Because these APIs allow us to store historical data locally and update it incrementally. Once historical data is cached, subsequent updates are much faster—a feat difficult to achieve with `pro_bar`.

Below is the method to fetch daily market data. Note that the returned data includes the adjustment factor, allowing you to freely apply forward or backward adjustment to any time period.

```python
def fetch_bars(start: datetime.date, end: datetime.date) -> pd.DataFrame | None:
    """Fetch daily market data via Tushare interface

    Returns unadjusted data but includes the adjustment factor, enabling incremental updates. Data is sorted ascending.

    Args:
        start: Start date
        end: End date

    Returns:
        DataFrame: Contains date, asset, open, high, low, close, volume, amount, adj_factor
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

            # Rename columns and convert data types
            df = df.rename(
                columns={"trade_date": "date", "vol": "volume", "ts_code": "asset"}
            )

            # Tushare returns dates as strings, e.g., '20231229'
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

            all_data.append(df)

        except Exception as e:
            print(f"Error loading data for {date}: {e}")
            continue

    if not all_data:
        return None

    # Concatenate all data. Based on the fetch logic, data is already ordered
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

Fetching three months of daily data takes approximately 165 seconds. If performed incrementally (i.e., pre-storing all historical data and running daily to fetch only new data), a single run takes only about 2.7 seconds.

## Price Adjustment

The daily data returned in the previous section is unadjusted. We isolate the adjustment functions. First, forward adjustment.

```python
def qfq_adjustment(
    df: pd.DataFrame, adj_factor_col: str = "adj_factor"
) -> pd.DataFrame:
    """
    Forward Adjustment Algorithm (qfq - Forward Adjustment)
    Adjusts historical prices based on the latest price.
    Volume must be adjusted inversely, as splits increase volume.

    Args:
        df: pandas DataFrame containing asset, open, high, low, close, volume, adj_factor columns
        adj_factor_col: Name of the adjustment factor column, default is "adj_factor"

    Returns:
        Adjusted pandas DataFrame
    """
    lf = pl.from_pandas(df).lazy()

    # Group by asset and calculate the latest adjustment factor for each stock
    result = (
        lf.with_columns(
            [pl.col(adj_factor_col).last().over("asset").alias("latest_adj_factor")]
        )
        .with_columns(
            [
                # Forward adjustment price calculation: price * adj_factor / latest_adj_factor
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
                # Forward adjustment volume calculation: volume * latest_adj_factor / adj_factor (inverse adjustment)
                (
                    pl.col("volume")
                    * pl.col("latest_adj_factor")
                    / pl.col(adj_factor_col)
                ).alias("volume"),
            ]
        )
        .drop("latest_adj_factor")
        .collect()  # Execute lazy computation
    )

    return result.to_pandas()
```

Here is the code for backward adjustment:

```python
def hfq_adjustment(
    df: pd.DataFrame, adj_factor_col: str = "adj_factor"
) -> pd.DataFrame:
    """
    Backward Adjustment Algorithm (hfq - Backward Adjustment)
    Adjusts subsequent prices based on historical prices.
    Volume is not adjusted; original values are kept.

    Args:
        df: pandas DataFrame containing asset, open, high, low, close, volume, adj_factor columns
        adj_factor_col: Name of the adjustment factor column, default is "adj_factor"

    Returns:
        Adjusted pandas DataFrame
    """
    lf = pl.from_pandas(df).lazy()

    result = (
        lf.with_columns(
            [pl.col(adj_factor_col).last().over("asset").alias("latest_adj_factor")]
        )
        .with_columns(
            [
                # Backward adjustment price calculation: price * latest_adj_factor / adj_factor
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
                # Backward adjustment volume: No adjustment, keep original value
                pl.col("volume").alias("volume"),
            ]
        )
        .drop("latest_adj_factor")
        .collect()  # Execute lazy computation
    )

    # Convert back to pandas DataFrame
    return result.to_pandas()
```

Note that besides the different application methods for adjustment factors, there is a significant difference in how volume is handled: for forward adjustment, we generally adjust volume; for backward adjustment, we generally keep the original values.

!!! info Why Different Volume Handling in Forward vs. Backward Adjustment?
    In forward adjustment, adjusting volume ensures logical consistency between price and volume, preventing distorted volume analysis due to price adjustments. Logically, backward adjustment should also adjust volume. However, adjusting volume in backward adjustment would distort the original trading scale, affecting order matching judgments in backtests. Therefore, whether to adjust volume depends on how the data is typically used. Adjusting volume in backward adjustment is permissible if there is a reasonable use case.

Here is a supplementary note on **Polars** syntax. The `lazy` method delays computation, meaning expressions written in the Python domain are not executed immediately (as they would be sequentially) but are recorded as a "computation plan." Data substitution and evaluation are deferred until the final evaluation, executed in Polars' C domain. This reduces data format conversions between the Python and C domains, enhancing efficiency. In the example code, execution occurs only when `collect` is called.

Second, regarding `with_columns`: its purpose is to add new columns to a DataFrame while allowing Polars to parallelize the execution of multiple passed statements (note that we pass an array). `with_columns` always returns a new DataFrame, enabling chained calls.

Third, in Polars, to reference columns for delayed operations in a DataFrame, you must use the `.col` syntax. If you call it via `pl["open"]`, it will be evaluated immediately, causing unnecessary data copying and transmission.

Finally, operations like `pl.col("close") * pl.col("latest_adj_factor")` generate temporary columns (unnamed). To reference them later, you must call `alias` to name the temporary result columns. The renamed results are returned along with the data copy generated by `with_columns`.

## Sidebar: Local Caching

Even if we are only replicating this research report, it is best to cache the data obtained from Tushare. Our replication steps are unlikely to succeed on the first try. Using cached data significantly accelerates our efficiency.

If this is for long-term research, doing so is even more necessary—and you must persist in updating it. The following minimal framework demonstrates how to efficiently implement this:

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
        """Load date range from file and cache"""
        if not Path(self.file_path).exists():
            self._start_date = None
            self._end_date = None
            return

        # Use LazyFrame for efficient large-file processing
        lazy_df = pl.scan_parquet(self.file_path)

        # Get min and max dates
        date_range = lazy_df.select(
            [pl.min("date").alias("start_date"), pl.max("date").alias("end_date")]
        ).collect()

        # Cache results
        self._start_date = date_range[0, "start_date"]
        self._end_date = date_range[0, "end_date"]

    def _update_date_range(self, df: pl.DataFrame):
        """Update cached date range based on new data"""
        if df.is_empty():
            return

        # Get date range of new data
        new_dates = df.select(
            [pl.min("date").alias("min_date"), pl.max("date").alias("max_date")]
        )

        new_min = new_dates[0, "min_date"]
        new_max = new_dates[0, "max_date"]

        # Update cached date range
        if self._start_date is None or new_min < self._start_date:
            self._start_date = new_min
        if self._end_date is None or new_max > self._end_date:
            self._end_date = new_max

    @property
    def start(self):
        """Get data start date"""
        return self._start_date

    @property
    def end(self):
        """Get data end date"""
        return self._end_date

    def append_data(self, df: pl.DataFrame | pd.DataFrame):
        """Append data to Parquet file"""
        if isinstance(df, pd.DataFrame):
            df = pl.from_pandas(df)

        if Path(self.file_path).exists():
            # Read existing data
            existing_df = pl.read_parquet(self.file_path)
            # Merge and deduplicate
            combined_df = pl.concat([existing_df, df]).unique(["date", "asset"])
        else:
            combined_df = df

        # Sort by date and asset to optimize queries
        combined_df = combined_df.sort(["date", "asset"])

        # Write to file (automatic compression)
        combined_df.write_parquet(self.file_path, compression="snappy")

        # Update cached date range
        self._update_date_range(df)

    def query_stock_bars(
        self,
        asset: str,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
    ):
        """Query individual stock data"""
        lazy_df = pl.scan_parquet(self.file_path)

        # Build filter conditions
        filters = [pl.col("asset") == asset]

        if start_date:
            filters.append(pl.col("date") >= start_date)
        if end_date:
            filters.append(pl.col("date") <= end_date)

        return lazy_df.filter(pl.all_horizontal(filters)).collect()

    def query_cross_section(self, date: datetime.date):
        """Query cross-sectional data for a specific date"""
        return pl.scan_parquet(self.file_path).filter(pl.col("date") == date).collect()
```

The core APIs of the framework are:

1.  `append_data`: Appends data to local storage (supports both forward and backward appending).
2.  `query_stock_bars`: Queries market data for a single stock.
3.  `query_cross_section`: Queries data for all stocks on a specific date.
4.  `start` and `end` properties: Help determine the start and end dates of the locally cached market data.

The following code demonstrates its usage:

```python
# Local file; may or may not exist yet
store = ParquetUnifiedStorage("/tmp/bars.parquet")

# Fetch historical market data
start = datetime.date(2019, 10, 8)
end = datetime.date(2019, 10, 12)
bars = fetch_bars(start, end)

# Store locally
store.append_data(bars)

# Query start and end dates
print(store.start, store.end)

# Append new data
dt = datetime.date(2019, 10, 14)
bars = fetch_bars(dt, dt)
store.append_data(bars)

# Query
print(store.end)
store.query_stock_bars("000001.SZ")
```

Now you have the simplest local data caching framework and have acquired daily market data. In the next article, we will cover how to acquire dividend yield data and call Moonshot to screen stocks by dividend yield and verify the screening results.
