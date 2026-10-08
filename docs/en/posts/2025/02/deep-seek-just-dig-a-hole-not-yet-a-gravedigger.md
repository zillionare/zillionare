---
title: "DeepSeek Didn’t Dig the Grave, But Junior Devs Are Trapped"
date: 2025-02-10
slug: en/posts/uncategory/deep-seek-just-dig-a-hole-not-yet-a-gravedigger
tags: []
excerpt: "This article benchmarks a 18-year China A-share factor mining dataset, optimizing data loading from 5s to 91ms using Polars and DuckDB. It demonstrates how AI can accelerate factor analysis, yet highlights the irreplaceable role of senior quant developers in validating and refining AI-generated solutions. ===TAG=== Factor Mining, Polars, DuckDB, AI-Assisted Quant Development ===BODY=== In our *Factor Analysis and Machine Learning Strategies* course, we provide 18 years of daily data (over 11 million records) from 2005 to 2023 for students to conduct factor mining and validation. Initially, we cached this data in memory using the `lru_cache` decorator from `functools`. This approach meant that while the first call took several seconds (e.g., ~5s), subsequent calls were executed in milliseconds.  ## The Problem  However, this approach led to excessive memory consumption. A single factor analysis session could consume over 5GB of RAM. Since JupyterLab lacks the ability to automatically close idle kernels (a feature available in Google Colab and Kaggle), our memory resources were quickly exhausted.  Our data is organized as a dictionary and saved on disk:  <div style='width:75%;text-align:center;margin: 0 auto 1rem'> <img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/20250210121041.png'> <span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span> </div>  Each stock’s key is its ticker symbol, and the corresponding value is a Numpy structured array. While this data structure may seem unique, the rationale behind it will become clear shortly.  Before conducting factor analysis, users load market data by specifying a `universe` (a stock pool) and a start/end date range. The `universe` can be a predefined list of securities or simply a target size. The date range allows users to adjust the observation window, often for performance reasons (e.g., using a small data slice for initial debugging, then switching to full data for backtesting or segmented observation).  The function returns a DataFrame with a dual index of `date` and `asset` (ticker), containing OHLC, volume, and other columns. These columns are dynamically forward-adjusted based on the `end` date (dynamic forward adjustment). Additionally, an `amount` column is included, which remains unadjusted.  <div style='width:75%;text-align:center;margin: 0 auto 1rem'> <img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/20250210202407.png'> <span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span> </div>  Thus, the function signature is:  ```python def load_bars(start_date:datetime.date,                end_date:datetime.date,                universe: Tuple[str]|int = 500)->pd.DataFrame:     pass ```  Students learn by reading our notebook documents and experimenting with the code cells, potentially modifying and re-running them. This is an interactive process. Generally, a user wait time of under 3 seconds is acceptable. A response time of under 1 second is considered ideal.  Without caching, the initial implementation took approximately 5 seconds:  ```python start = datetime.date(2023, 12,1) end = datetime.date(2023, 12,31) %time load_bars(start, end, 2000) ```  _Subsequent tests will use these same parameters._  Of course, using a larger `universe` would further increase the time.  Since this result exceeds the 3-second threshold, we sought to optimize the code. Performance optimization is challenging in programming, as it requires a deep understanding of execution principles and proficiency across multiple tech stacks. In this process, I explored the capabilities of DeepSeek R1, which I hope serves as a useful reference.  ## The Initial Approach  The initial code was as follows:  ```python def load_bars_v1(     start: datetime.date, end: datetime.date, universe: Tuple[str]|int = 500 )->pd.DataFrame:      if barss is None:         with open(os.path.join(data_home, \"bars_1d_2005_2023.pkl\"), \"rb\") as f:             barss = pickle.load(f)      keys = list(barss.keys())     if isinstance(universe, int):         if universe == -1:             selected_keys = keys         else:             selected_keys = random.sample(keys, min(universe, len(keys)))             try:                 pos = selected_keys.index(\"000001.XSHE\")                 swp = selected_keys[0]                 selected_keys[0] = \"000001.XSHE\"                 selected_keys[pos] = swp             except ValueError:                 selected_keys[0] = \"000001.XSHE\"      else:         selected_keys = universe      dfs = []     for symbol in selected_keys:         qry = \"frame >= @start & frame <= @end\"         df = pd.DataFrame(barss[symbol]).assign(asset=symbol).query(qry)          if len(df) == 0:             logger.debug(\"no bars for %s from %s to %s\", symbol, start, end)             continue         # Forward adjustment         last = df.iloc[-1][\"factor\"]         adjust_factor = df[\"factor\"] / last         adjust = [\"open\", \"high\", \"low\", \"close\", \"volume\"]         df.loc[:, adjust] = df.loc[:, adjust].multiply(adjust_factor, axis=\"index\")          dfs.append(df)      df = pd.concat(dfs, ignore_index=True)     df.set_index([\"frame\", \"asset\"], inplace=True)     df.index.names = [\"date\", \"asset\"]     df.drop(\"factor\", axis=1, inplace=True)     df[\"price\"] = df[\"open\"].shift(-1)     return df ```  The code had already undergone significant optimization (partially based on AI suggestions). For instance, saving data as a dictionary, filtering by `universe` first, and then concatenating into a DataFrame, rather than saving all data as a single DataFrame and filtering via Pandas (which would take several times longer).  Additionally, during forward adjustment, it used the `multiply` method, allowing simultaneous adjustment of multiple columns—a suggestion from AI.  However, the code still contained a `for` loop. Could eliminating this loop further improve speed?  Below, I attempted to use DeepSeek R1 for this task.  Here is the first round of prompts:  !!! quote     I have a DataFrame with a joint index of `date` and `asset`, containing columns such as `open`, `high`, `low`, `close`, `volume`, `amount`, and `factor`. The `factor` column represents the adjustment factor.<br>     I need to implement the following functionality for this data structure:<br>         1. Filter records where `asset` is in `selected_symbols` and `date` is within `[start, end]`.         2. Group these records by `asset`, then forward-adjust `open`, `high`, `low`, `close`, and `volume`.         3. Return the result as a DataFrame, maintaining the `date`/`asset` index, with columns for the adjusted `open`, `high`, `low`, `close`, `volume`, and the unprocessed `amount`.         <br>Please provide implementations based on Pandas, PyArrow, Polars, and DuckDB, and recommend the one with the best performance.   DeepSeek’s reasoning process was lengthy, so I will skip it. We will directly look at its answer. Since disk read/write speeds have minimal impact on overall performance, we first load the data from disk into `barss`:  ```python with open(os.path.join(data_home, \"bars_1d_2005_2023.pkl\"), \"rb\") as f:     data = pickle.load(f)  dfs = [] for symbol, bars in data.items():     df = pd.DataFrame(bars)     df[\"asset\"] = symbol     df = df.rename(columns={\"frame\": \"date\"})     dfs.append(df)  barss = pd.concat(dfs,ignore_index=True).set_index([\"date\", \"asset\"]).sort_index() print(len(barss))  # Define a consistent universe for comparison universe = barss.index.get_level_values(\"asset\").unique().tolist() ```  The following code is generated by DeepSeek. We asked it to provide solutions for the most time-consuming parts: filtering and adjustment.  ## Pandas Implementation  ```python def adjust_pandas(df, selected_symbols, start, end):     # Filter data     idx = pd.IndexSlice     filtered = df.loc[idx[start:end, selected_symbols], :]          # Calculate the last adjustment factor grouped by asset     grouped = filtered.groupby('asset', group_keys=False)     last_factor = grouped['factor'].transform('last')          # Calculate adjustment ratio     ratio = filtered['factor'] / last_factor          # Calculate adjusted fields     adjusted = filtered.assign(         open   = filtered['open'] * ratio,         high   = filtered['high'] * ratio,         low    = filtered['low'] * ratio,         close  = filtered['close'] * ratio,         volume = filtered['volume'] * (last_factor / filtered['factor'])     )          # Select final columns and maintain index     return adjusted[['open', 'high', 'low', 'close', 'volume', 'amount']]  %time adjust_pandas(barss, universe, start, end) adjust_pandas(barss, universe, start, end) ```  Although I am familiar with Pandas, there are still some APIs I didn’t know, such as `transform`. However, using the correct API is precisely the key to improving performance in Python.  The average runtime for this version was 7 seconds, indicating that Pandas filtering is indeed slow.  We will skip the PyArrow version. The PyArrow version took approximately 3.7 seconds, showing only slight improvement over the original version. This also highlights that in Python 3.11, `for` loops run quite fast.  ## Polars Implementation  Here is the Polars version provided by DeepSeek:  ```python import polars as pl  def adjust_polars(df, selected_symbols, start, end):     # Filter data     filtered = df.filter(         (pl.col(\"date\").is_between(start, end)) &         (pl.col(\"asset\").is_in(selected_symbols))     )          # Calculate the last adjustment factor and adjustment ratio     adjusted = filtered.with_columns(         last_factor = pl.col(\"factor\").last().over(\"asset\")     ).with_columns(         ratio = pl.col(\"factor\") / pl.col(\"last_factor\"),         volume_ratio = pl.col(\"last_factor\") / pl.col(\"factor\")     ).with_columns(         open   = pl.col(\"open\") * pl.col(\"ratio\"),         high   = pl.col(\"high\") * pl.col(\"ratio\"),         low    = pl.col(\"low\") * pl.col(\"ratio\"),         close  = pl.col(\"close\") * pl.col(\"ratio\"),         volume = pl.col(\"volume\") * pl.col(\"volume_ratio\")     )          # Select final columns     return adjusted.select([\"date\", \"asset\", \"open\", \"high\", \"low\", \"close\", \"volume\", \"amount\"])  adjust_polars(barss, universe, start, end) ```  I was previously unfamiliar with Polars, and DeepSeek instantly expanded my capabilities. If I had to learn and implement this feature through self-study, I am unsure how long it would take to discover the `.over` API, as this is a unique window operation API in Polars, and I couldn’t easily migrate knowledge from my familiarity with Pandas.  However, this version had an error: it did not adhere to my data format, treating `barss` as a Polars DataFrame with `asset` and `date` columns instead of an index. Using Tongyi Lingma, I corrected this error. The corrected code is as follows:  ```python %time adjust_polars(pl.from_pandas(barss.reset_index()), universe, start, end) ```  The resulting runtime was 1.01 seconds, which is very close to our ideal target speed.  ## DuckDB Implementation  Now, let’s look at the DuckDB version provided by DeepSeek:  ```python import duckdb  def adjust_duckdb(df, selected_symbols, start, end):     query = f\"\"\"     SELECT          date, asset,         open * (factor / last_factor) AS open,         high * (factor / last_factor) AS high,         low * (factor / last_factor) AS low,         close * (factor / last_factor) AS close,         volume * (last_factor / factor) AS volume,         amount     FROM (         SELECT              *,             LAST_VALUE(factor) OVER (                 PARTITION BY asset                  ORDER BY date                  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING             ) AS last_factor         FROM df         WHERE              asset IN ({','.join([f\"'{s}'\" for s in selected_symbols])})             AND date BETWEEN '{start}' AND '{end}'     )     \"\"\"     return duckdb.query(query).to_df()  adjust_duckdb(barss, universe, start, end) ```  A similar error occurred here: the query required `asset` and `date` columns, but they were in the index. We made a minor correction to run it:  ```python %time adjust_duckdb(barss.reset_index(), universe, start, end) ```  The final runtime was 1.21 seconds, slightly slower than Polars in this example, ranking second among all solutions (on another machine with a mechanical hard drive and a stronger CPU, DuckDB was faster). However, the DuckDB solution may have advantages in data scale; if the dataset were one or two orders of magnitude larger, it would likely surpass Polars.  Both Polars and DuckDB require flat result data structures (i.e., `asset`/`date` as columns, not indices). Therefore, we can consider restructuring the data structure and writing it to disk in Apache Parquet format, keeping the total solution time around 1 second.  ## The Ultimate Prompt: \"Quickly, Quickly, Biu Biu Biu\"  !!! info     It is said that \"Ji Ji Ru Lü Ling\" translates to \"quickly, quickly, biu biu biu\" 😁  In the previous sections, we did a lot of thinking on behalf of DeepSeek because we worried it lacked a sense of the final execution speed of the code. Now, let’s try throwing the final question directly and see what happens:  !!! quote     I have a DataFrame with a joint index of `date` and `asset`, containing columns such as `open`, `high`, `low`, `close`, `volume`, `amount`, and `factor`. The `factor` column represents the adjustment factor.      I need to implement the following functionality for this data structure:      1. Filter records where `asset` is in `selected_symbols` and `date` is within `[start, end]`.     2. Group these records by `asset`, then forward-adjust `open`, `high`, `low`, `close`, and `volume`.     3. Return the result as a DataFrame, maintaining the `date`/`asset` index, with columns for the adjusted `open`, `high`, `low`, `close`, `volume`, and the unprocessed `amount`.      The input data exceeds 10 million records, spanning from 2005 to 2023. By the end of 2023, there were approximately 5,000 stocks. The output will contain data for 2,000 stocks from 2005 to 2023. Please provide a Python-based solution that can achieve the above functionality in around 1 second.  This time, we limited the technical scope to Python, giving DeepSeek significant room to maneuver.  DeepSeek not only provided code but also a \"evaluation report,\" claiming that its solution could achieve the requested speed on a specific CPU+memory combination.  DeepSeek believed that for datasets with tens of millions of records, parallelization libraries like parallel Pandas were necessary to meet the target. **In fact, this认知 is incorrect.**  The code provided by DeepSeek this time had low executability, making it difficult to verify if the speed truly improved after parallelization. However, what was impressive was that it also provided a performance benchmark. Whether this was self-generated via GAN, based on actual tests by someone else, or derived from similar scales remains unknown.  Importantly, by giving DeepSeek more freedom, it identified a key reason for the poor performance in previous filtering: **`asset` was of string type!**  String searches in massive records are extremely slow. In Pandas, we can convert integers to the `category` type, making subsequent filtering much faster:  ```python import pyarrow as pa import pyarrow.parquet as pq  data_home = os.path.expanduser(data_home) origin_data_file = os.path.join(data_home, \"bars_1d_2005_2023.pkl\") with open(origin_data_file, 'rb') as f:     data = pickle.load(f)  dfs = [] for symbol, bars in data.items():     df = pd.DataFrame(bars)     df[\"asset\"] = symbol     df = df.rename(columns={\"frame\": \"date\"})     dfs.append(df)  barss = pd.concat(dfs,ignore_index=True) barss['asset'] = barss['asset'].astype('category') print(len(barss))  table = pa.Table.from_pandas(barss)  parquet_file_path = \"/tmp/bars_1d_2005_2023_category.parquet\"  with open(parquet_file_path, 'wb') as f:     pq.write_table(table, f) ```  Now, let’s look at the runtime"
lang: en
translation_of: posts/uncategory/deep-seek-just-dig-a-hole-not-yet-a-gravedigger
auto_translated: true
source_sha: a488b9f8a35072508426b6ece70f7349b2d34ba7
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/IMG_20250204_110950.jpg"
---

In our *Factor Analysis and Machine Learning Strategies* course, we provide 18 years of daily data (over 11 million records) from 2005 to 2023 for students to conduct factor mining and validation. Initially, we cached this data in memory using the `lru_cache` decorator from `functools`. This approach meant that while the first call took several seconds (e.g., ~5s), subsequent calls were executed in milliseconds.

## The Problem

However, this approach led to excessive memory consumption. A single factor analysis session could consume over 5GB of RAM. Since JupyterLab lacks the ability to automatically close idle kernels (a feature available in Google Colab and Kaggle), our memory resources were quickly exhausted.

Our data is organized as a dictionary and saved on disk:

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/20250210121041.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

Each stock’s key is its ticker symbol, and the corresponding value is a Numpy structured array. While this data structure may seem unique, the rationale behind it will become clear shortly.

Before conducting factor analysis, users load market data by specifying a `universe` (a stock pool) and a start/end date range. The `universe` can be a predefined list of securities or simply a target size. The date range allows users to adjust the observation window, often for performance reasons (e.g., using a small data slice for initial debugging, then switching to full data for backtesting or segmented observation).

The function returns a DataFrame with a dual index of `date` and `asset` (ticker), containing OHLC, volume, and other columns. These columns are dynamically forward-adjusted based on the `end` date (dynamic forward adjustment). Additionally, an `amount` column is included, which remains unadjusted.

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/20250210202407.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

Thus, the function signature is:

```python
def load_bars(start_date:datetime.date, 
              end_date:datetime.date, 
              universe: Tuple[str]|int = 500)->pd.DataFrame:
    pass
```

Students learn by reading our notebook documents and experimenting with the code cells, potentially modifying and re-running them. This is an interactive process. Generally, a user wait time of under 3 seconds is acceptable. A response time of under 1 second is considered ideal.

Without caching, the initial implementation took approximately 5 seconds:

```python
start = datetime.date(2023, 12,1)
end = datetime.date(2023, 12,31)
%time load_bars(start, end, 2000)
```

_Subsequent tests will use these same parameters._

Of course, using a larger `universe` would further increase the time.

Since this result exceeds the 3-second threshold, we sought to optimize the code. Performance optimization is challenging in programming, as it requires a deep understanding of execution principles and proficiency across multiple tech stacks. In this process, I explored the capabilities of DeepSeek R1, which I hope serves as a useful reference.

## The Initial Approach

The initial code was as follows:

```python
def load_bars_v1(
    start: datetime.date, end: datetime.date, universe: Tuple[str]|int = 500
)->pd.DataFrame:

    if barss is None:
        with open(os.path.join(data_home, "bars_1d_2005_2023.pkl"), "rb") as f:
            barss = pickle.load(f)

    keys = list(barss.keys())
    if isinstance(universe, int):
        if universe == -1:
            selected_keys = keys
        else:
            selected_keys = random.sample(keys, min(universe, len(keys)))
            try:
                pos = selected_keys.index("000001.XSHE")
                swp = selected_keys[0]
                selected_keys[0] = "000001.XSHE"
                selected_keys[pos] = swp
            except ValueError:
                selected_keys[0] = "000001.XSHE"

    else:
        selected_keys = universe

    dfs = []
    for symbol in selected_keys:
        qry = "frame >= @start & frame <= @end"
        df = pd.DataFrame(barss[symbol]).assign(asset=symbol).query(qry)

        if len(df) == 0:
            logger.debug("no bars for %s from %s to %s", symbol, start, end)
            continue
        # Forward adjustment
        last = df.iloc[-1]["factor"]
        adjust_factor = df["factor"] / last
        adjust = ["open", "high", "low", "close", "volume"]
        df.loc[:, adjust] = df.loc[:, adjust].multiply(adjust_factor, axis="index")

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df.set_index(["frame", "asset"], inplace=True)
    df.index.names = ["date", "asset"]
    df.drop("factor", axis=1, inplace=True)
    df["price"] = df["open"].shift(-1)
    return df
```

The code had already undergone significant optimization (partially based on AI suggestions). For instance, saving data as a dictionary, filtering by `universe` first, and then concatenating into a DataFrame, rather than saving all data as a single DataFrame and filtering via Pandas (which would take several times longer).

Additionally, during forward adjustment, it used the `multiply` method, allowing simultaneous adjustment of multiple columns—a suggestion from AI.

However, the code still contained a `for` loop. Could eliminating this loop further improve speed?

Below, I attempted to use DeepSeek R1 for this task.

Here is the first round of prompts:

!!! quote
    I have a DataFrame with a joint index of `date` and `asset`, containing columns such as `open`, `high`, `low`, `close`, `volume`, `amount`, and `factor`. The `factor` column represents the adjustment factor.<br>
    I need to implement the following functionality for this data structure:<br>
        1. Filter records where `asset` is in `selected_symbols` and `date` is within `[start, end]`.
        2. Group these records by `asset`, then forward-adjust `open`, `high`, `low`, `close`, and `volume`.
        3. Return the result as a DataFrame, maintaining the `date`/`asset` index, with columns for the adjusted `open`, `high`, `low`, `close`, `volume`, and the unprocessed `amount`.
        <br>Please provide implementations based on Pandas, PyArrow, Polars, and DuckDB, and recommend the one with the best performance.


DeepSeek’s reasoning process was lengthy, so I will skip it. We will directly look at its answer. Since disk read/write speeds have minimal impact on overall performance, we first load the data from disk into `barss`:

```python
with open(os.path.join(data_home, "bars_1d_2005_2023.pkl"), "rb") as f:
    data = pickle.load(f)

dfs = []
for symbol, bars in data.items():
    df = pd.DataFrame(bars)
    df["asset"] = symbol
    df = df.rename(columns={"frame": "date"})
    dfs.append(df)

barss = pd.concat(dfs,ignore_index=True).set_index(["date", "asset"]).sort_index()
print(len(barss))

# Define a consistent universe for comparison
universe = barss.index.get_level_values("asset").unique().tolist()
```

The following code is generated by DeepSeek. We asked it to provide solutions for the most time-consuming parts: filtering and adjustment.

## Pandas Implementation

```python
def adjust_pandas(df, selected_symbols, start, end):
    # Filter data
    idx = pd.IndexSlice
    filtered = df.loc[idx[start:end, selected_symbols], :]
    
    # Calculate the last adjustment factor grouped by asset
    grouped = filtered.groupby('asset', group_keys=False)
    last_factor = grouped['factor'].transform('last')
    
    # Calculate adjustment ratio
    ratio = filtered['factor'] / last_factor
    
    # Calculate adjusted fields
    adjusted = filtered.assign(
        open   = filtered['open'] * ratio,
        high   = filtered['high'] * ratio,
        low    = filtered['low'] * ratio,
        close  = filtered['close'] * ratio,
        volume = filtered['volume'] * (last_factor / filtered['factor'])
    )
    
    # Select final columns and maintain index
    return adjusted[['open', 'high', 'low', 'close', 'volume', 'amount']]

%time adjust_pandas(barss, universe, start, end)
adjust_pandas(barss, universe, start, end)
```

Although I am familiar with Pandas, there are still some APIs I didn’t know, such as `transform`. However, using the correct API is precisely the key to improving performance in Python.

The average runtime for this version was 7 seconds, indicating that Pandas filtering is indeed slow.

We will skip the PyArrow version. The PyArrow version took approximately 3.7 seconds, showing only slight improvement over the original version. This also highlights that in Python 3.11, `for` loops run quite fast.

## Polars Implementation

Here is the Polars version provided by DeepSeek:

```python
import polars as pl

def adjust_polars(df, selected_symbols, start, end):
    # Filter data
    filtered = df.filter(
        (pl.col("date").is_between(start, end)) &
        (pl.col("asset").is_in(selected_symbols))
    )
    
    # Calculate the last adjustment factor and adjustment ratio
    adjusted = filtered.with_columns(
        last_factor = pl.col("factor").last().over("asset")
    ).with_columns(
        ratio = pl.col("factor") / pl.col("last_factor"),
        volume_ratio = pl.col("last_factor") / pl.col("factor")
    ).with_columns(
        open   = pl.col("open") * pl.col("ratio"),
        high   = pl.col("high") * pl.col("ratio"),
        low    = pl.col("low") * pl.col("ratio"),
        close  = pl.col("close") * pl.col("ratio"),
        volume = pl.col("volume") * pl.col("volume_ratio")
    )
    
    # Select final columns
    return adjusted.select(["date", "asset", "open", "high", "low", "close", "volume", "amount"])

adjust_polars(barss, universe, start, end)
```

I was previously unfamiliar with Polars, and DeepSeek instantly expanded my capabilities. If I had to learn and implement this feature through self-study, I am unsure how long it would take to discover the `.over` API, as this is a unique window operation API in Polars, and I couldn’t easily migrate knowledge from my familiarity with Pandas.

However, this version had an error: it did not adhere to my data format, treating `barss` as a Polars DataFrame with `asset` and `date` columns instead of an index. Using Tongyi Lingma, I corrected this error. The corrected code is as follows:

```python
%time adjust_polars(pl.from_pandas(barss.reset_index()), universe, start, end)
```

The resulting runtime was 1.01 seconds, which is very close to our ideal target speed.

## DuckDB Implementation

Now, let’s look at the DuckDB version provided by DeepSeek:

```python
import duckdb

def adjust_duckdb(df, selected_symbols, start, end):
    query = f"""
    SELECT 
        date, asset,
        open * (factor / last_factor) AS open,
        high * (factor / last_factor) AS high,
        low * (factor / last_factor) AS low,
        close * (factor / last_factor) AS close,
        volume * (last_factor / factor) AS volume,
        amount
    FROM (
        SELECT 
            *,
            LAST_VALUE(factor) OVER (
                PARTITION BY asset 
                ORDER BY date 
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS last_factor
        FROM df
        WHERE 
            asset IN ({','.join([f"'{s}'" for s in selected_symbols])})
            AND date BETWEEN '{start}' AND '{end}'
    )
    """
    return duckdb.query(query).to_df()

adjust_duckdb(barss, universe, start, end)
```

A similar error occurred here: the query required `asset` and `date` columns, but they were in the index. We made a minor correction to run it:

```python
%time adjust_duckdb(barss.reset_index(), universe, start, end)
```

The final runtime was 1.21 seconds, slightly slower than Polars in this example, ranking second among all solutions (on another machine with a mechanical hard drive and a stronger CPU, DuckDB was faster). However, the DuckDB solution may have advantages in data scale; if the dataset were one or two orders of magnitude larger, it would likely surpass Polars.

Both Polars and DuckDB require flat result data structures (i.e., `asset`/`date` as columns, not indices). Therefore, we can consider restructuring the data structure and writing it to disk in Apache Parquet format, keeping the total solution time around 1 second.

## The Ultimate Prompt: "Quickly, Quickly, Biu Biu Biu"

!!! info
    It is said that "Ji Ji Ru Lü Ling" translates to "quickly, quickly, biu biu biu" 😁

In the previous sections, we did a lot of thinking on behalf of DeepSeek because we worried it lacked a sense of the final execution speed of the code. Now, let’s try throwing the final question directly and see what happens:

!!! quote
    I have a DataFrame with a joint index of `date` and `asset`, containing columns such as `open`, `high`, `low`, `close`, `volume`, `amount`, and `factor`. The `factor` column represents the adjustment factor.

    I need to implement the following functionality for this data structure:

    1. Filter records where `asset` is in `selected_symbols` and `date` is within `[start, end]`.
    2. Group these records by `asset`, then forward-adjust `open`, `high`, `low`, `close`, and `volume`.
    3. Return the result as a DataFrame, maintaining the `date`/`asset` index, with columns for the adjusted `open`, `high`, `low`, `close`, `volume`, and the unprocessed `amount`.

    The input data exceeds 10 million records, spanning from 2005 to 2023. By the end of 2023, there were approximately 5,000 stocks. The output will contain data for 2,000 stocks from 2005 to 2023. Please provide a Python-based solution that can achieve the above functionality in around 1 second.

This time, we limited the technical scope to Python, giving DeepSeek significant room to maneuver.

DeepSeek not only provided code but also a "evaluation report," claiming that its solution could achieve the requested speed on a specific CPU+memory combination.

DeepSeek believed that for datasets with tens of millions of records, parallelization libraries like parallel Pandas were necessary to meet the target. **In fact, this认知 is incorrect.**

The code provided by DeepSeek this time had low executability, making it difficult to verify if the speed truly improved after parallelization. However, what was impressive was that it also provided a performance benchmark. Whether this was self-generated via GAN, based on actual tests by someone else, or derived from similar scales remains unknown.

Importantly, by giving DeepSeek more freedom, it identified a key reason for the poor performance in previous filtering: **`asset` was of string type!**

String searches in massive records are extremely slow. In Pandas, we can convert integers to the `category` type, making subsequent filtering much faster:

```python
import pyarrow as pa
import pyarrow.parquet as pq

data_home = os.path.expanduser(data_home)
origin_data_file = os.path.join(data_home, "bars_1d_2005_2023.pkl")
with open(origin_data_file, 'rb') as f:
    data = pickle.load(f)

dfs = []
for symbol, bars in data.items():
    df = pd.DataFrame(bars)
    df["asset"] = symbol
    df = df.rename(columns={"frame": "date"})
    dfs.append(df)

barss = pd.concat(dfs,ignore_index=True)
barss['asset'] = barss['asset'].astype('category')
print(len(barss))

table = pa.Table.from_pandas(barss)

parquet_file_path = "/tmp/bars_1d_2005_2023_category.parquet"

with open(parquet_file_path, 'wb') as f:
    pq.write_table(table, f)
```

Now, let’s look at the runtime
