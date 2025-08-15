---
title: 『Moonshot is all you need』 02 - 用tushare玩转月线回测：复权与本地缓存的秘密武器
date: 2025-08-15
excerpt: 本篇聚焦月线策略回测的『数据难题』，揭秘如何通过 tushare 高效获取、复权行情数据并实现本地缓存，彻底解决Alphalens在月线回测上的短板。跟随实战案例，掌握复权原理与缓存技巧，为复杂研报复现打下坚实基础。
category: tools
tags: [Moonshot, 回测, 研报, tushare]
---

能够自己复现研报，是我们学员的一个基本要求。在课程中我们详细介绍了 Alphalens 因子分析框架，它非常适合日线因子的快速回测。但是，对一些月线策略，Alphalens 在回测上就力有不逮。

这就是为什么我们开发了moonshot：不仅是要填补这一空白，更是要确保我们的学员能将所学的知识用以实战。

上一篇我们大致介绍了 moonshot 的核心思想：你将所有的一切（月开盘价、月收盘价、因子或者交易信号）放入一个以月和资产代码为索引的 DataFrame 中，通过 moonshot 就能执行回测，并输出报告。

现在，我们就从最基础的获取数据开始，一步步带大家掌握月线策略的回测。

## 数据总览

『基本面量化系列14』这篇研报要求的数据各类比较多，加上一些预处理步骤，所以整个工程量并不小。以此为例，也正好演示通过 Moonshot 框架，如何把复杂的项目条理化、简单化。

这是策略的数据清单：

1. 行情数据。任何策略都默认需要它，至少会在计算远期收益时使用。 <!-- pro.daily -->
2. 股息率，用来按股息率筛选个股，以及计算两年股息率均值因子。 <!-- pro.daily_basic -->
3. 分红数据。只有过去两年连续分红的公司才能入选。 <!-- pro.dividend -->
4. 审计意见。只有过去十年没有审计保留意见的公司才能入选。<!--pro.audit-->
5. 市值数据。只有市值大于50亿的公司才能入选。 <!-- pro.daily_basic -->
6. 净利润、营业收入和营业利润数据，用来计算净利润稳定性因子。<!-- pro.income -->
7. 股东数量变化 <!-- pro.stk_holdernumber -->
8. 换手率。用来计算换手波动率。<!-- pro.daily_basic -->
9. pe_ttm，用来计算 ep 因子。
10. 经营现金流数据，用来计算经营现金流资产比因子。<!-- pro.cashflow_vip.n_cashflow_act-->
11. 资产总计数据，与10一起，用来计算经营现金流资产比因子。 <!-- pro.balancesheet_vip.total_assets -->
12. 盈余公积金数据。与11一起，用来计算留存收益资产比因子。<!-- pro.balancesheet_vip.surplus_rese -->

我们将一一介绍这些数据是什么意思，有何作用，从何处可以获取到。因此，跟随这个系列，你将获取比较完整的基本面月度调仓策略构建经验。

在这一期中，我们将介绍如何获得行情数据（tushare），并对数据进行复权处理。

## 日线行情数据及复权

我们需要获得回测区间所有个股的行情数据，这样通过重采样之后，就能用月初开盘价、月末收盘价计算出个股的月收益率。此外，我们还要介绍如何高效实现复权。

!!! tip 为什么要复权？
    如果某支股票月初是10元，执行了10送10，除权后股价变为5元。又假设当月收于6元，上涨20%。如果我们不进行复权，则计算出的收益会是-40%。这显然会导致策略失败。

在 tushare 中，我们可以用 daily 或者 pro_bar 来获取行情数据。两者的区别是，在实现上，pro_bar 是一个集成接口，它在内部会（根据需要）调用 daily, adj_factor, daily_basic 等方法来获取数据，再进行合并对齐。

这里我们推荐掌握 daily 和 adj_factor 等基础 API 的用法。原因是，通过这两个 API，我们可以将历史数据存储到本地，然后以追加的方式完成行情数据的更新。一旦历史数据得到缓存，此后的更新就会比较快。这是 pro_bar 方法难以做到的。

下面是获取日线行情数据的方法，注意返回的数据中，已附带了复权因子。随后我们可以根据自己的需要，对任何时间段，自由进行前后复权。

```python
def fetch_bars(start: datetime.date, end: datetime.date) -> pd.DataFrame|None:
    """通过 tushare 接口，获取日线行情数据

    返回数据未复权，但包含了复权因子，因此可以增量获取叠加。返回数据为升序。

    Args:
        start: 开始日期
        end: 结束日期

    Returns:
        DataFrame: 包含date, asset, open,high,low,close,volume,amount,adj_factor
    """
    all_data = []

    pro = pro_api()

    for date in pd.bdate_range(start, end):
        try:
            str_date = date.strftime("%Y%m%d")
            df = pro.daily(trade_date = str_date)
            if df.empty:
                continue

            try:
                adj_factor = pro.adj_factor(ts_code='', trade_date=str_date)
                if adj_factor.empty:
                    continue
            except Exception:
                continue

            df = pd.merge(df, adj_factor, on = ["ts_code", "trade_date"], how="inner")

            # 重命名列并转换数据类型
            df = df.rename(columns={
                'trade_date': 'date',
                "vol": "volume",
                "ts_code": "asset"
            })

            # tushare返回的是字符串格式的日期，如'20231229'
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

            all_data.append(df)

        except Exception as e:
            print(f"Error loading data for {date}: {e}")
            continue

    if not all_data:
        return None

    # 合并所有数据。由获取数据逻辑知此时数据已为有序
    result = pd.concat(all_data, ignore_index=True)

    result = result[['date', 'asset', 'open', 'high', 'low', 'close', 'volume', 'amount', 'adj_factor']]

    return result
```

通过此方法获得三个月的日线数据，大约需要165秒。如果是以增量的方式（即事先预存了全部历史数据，此后每日运行一次获取当日新增数据），则运行一次只需要2.7秒左右。

## 复权

前一节返回的日线数据是没有复权的。我们把复权函数独立出来。首先是前复权。


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

这是执行后复权的代码：

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

要注意前后复权中，除了复权因子的应用方法不一样之外，对成交量的处理有重大不同：对前复权，我们一般要进行成交量复权；但对于后复权，我们一般保持原始值。

!!! info 为何在前后复权中，对成交量的处理不一样？
    在前复权中，对成交量也进行复权，是为了确保量价关系在逻辑上一致，避免因价格调整导致量能分析失真；按此逻辑，后复权中，似乎也应该进行成交量复权；但是，对成交量进行后复权之后，会破坏原始交易规模，影响回测中的成交撮合判断。因此，是否对成交量进行复权，实际上是看多数情况下，我们将如何使用数据来确定的。在有合理的使用场景时，对成交量进行后复权也是允许的。

这里补充一点 polars 的语法。lazy 方法的作用是将计算延迟，这样使得我们在 python 域写下的表达式，可以不会立即执行（通常情况下，表达式按顺序执行），而是被记录成一个『计算计划』。代入数据并求值会被推迟到最终求值时，才在 polars 运行的 c 作用域里执行。这样会少一些 python 域与 c 域的数据格式转换，从而更加高效。在示例代码中，最终执行是在 `collect` 被调用时才执行的。

第二点是关于 with_columns 的用法。它的作用是在 DataFrame 中增加新的列，同时让 polars 尽可能地并行化执行传入的多条语句（注意到我们传入的是一个数组）。with_columns 总是返回一个新的 DataFrame，因此，可以被链式调用。

第三点是在 polars 中，要对 DataFrame 中的列进行延时操作，必须使用.col 这样的语法来引用列。如果你通过 pl["open"]这样的语法来进行调用，那么，它将被立即求值。这会导致数据不必要的拷贝和传递。

最后，像pl.col("close") * pl.col("latest_adj_factor") 这样的运算，都会生成临时列（没有名字）。为了之后方便引用它们，就需要调用 alias 为临时结果列命名。重命名之后的结果，将会随 with_columns 生成的数据副本一同返回。


## 题外话: 本地缓存

即使仅仅是为了复现本研报，我们也最好将从 tushare 获得的各项数据缓存下来。因为我们的复现步骤不太可能一次成功。使用缓存的数据，将大大加快我们的效率。

如果是为了长期研究，我们就更有必要这么做了 -- 并且要坚持更新。下面的极简框架演示了如何高效实现这一点：

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
        date_range = lazy_df.select([
            pl.min('date').alias('start_date'),
            pl.max('date').alias('end_date')
        ]).collect()
        
        # 缓存结果
        self._start_date = date_range[0, 'start_date']
        self._end_date = date_range[0, 'end_date']
    
    def _update_date_range(self, df: pl.DataFrame):
        """根据新数据更新日期范围缓存"""
        if df.is_empty():
            return
            
        # 获取新数据的日期范围
        new_dates = df.select([
            pl.min('date').alias('min_date'),
            pl.max('date').alias('max_date')
        ])
        
        new_min = new_dates[0, 'min_date']
        new_max = new_dates[0, 'max_date']
        
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
    
    def append_data(self, df: pl.DataFrame|pd.DataFrame):
        """追加数据到Parquet文件"""
        if isinstance(df, pd.DataFrame):
            df = pl.from_pandas(df)

        if Path(self.file_path).exists():
            # 读取现有数据
            existing_df = pl.read_parquet(self.file_path)
            # 合并并去重
            combined_df = pl.concat([existing_df, df]).unique(['date', 'asset'])
        else:
            combined_df = df
        
        # 按 date 和 asset 排序以优化查询
        combined_df = combined_df.sort(['date', 'asset'])
        
        # 写入文件（自动压缩）
        combined_df.write_parquet(self.file_path, compression='snappy')
        
        # 更新日期范围缓存
        self._update_date_range(df)
    
    def query_stock_bars(self, asset: str, start_date: datetime.date = None, end_date: datetime.date = None):
        """查询个股数据"""
        lazy_df = pl.scan_parquet(self.file_path)
        
        # 构建过滤条件
        filters = [pl.col('asset') == asset]
        
        if start_date:
            filters.append(pl.col('date') >= start_date)
        if end_date:
            filters.append(pl.col('date') <= end_date)
        
        return lazy_df.filter(pl.all_horizontal(filters)).collect()
    
    def query_cross_section(self, date: datetime.date):
        """查询截面数据"""
        return (pl.scan_parquet(self.file_path)
                .filter(pl.col('date') == date)
                .collect())
```

框架的核心 API 是：

1. append_data，用来向本地存储追加数据（向前和向后都允许）
2. query_stock_bars，查询单支股票的行情
3. query_cross_section，查询某一日所有个股的数据
4. start 和 end 两个属性，帮助我们确定本地缓存的行情数据的起止日期。

下面的代码演示了它的用法：

```
{code-block} python
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

现在，你就有了一个最简单的本地数据缓存框架。 # 获取最小和最大日期
        date_range = lazy_df.select([
            pl.min('date').alias('start_date'),
            pl.max('date').alias('end_date')
        ]).collect()
        
        # 缓存结果
        self._start_date = date_range[0, 'start_date']
        self._end_date = date_range[0, 'end_date']
    
    def _update_date_range(self, df: pl.DataFrame):
        """根据新数据更新日期范围缓存"""
        if df.is_empty():
            return
            
        # 获取新数据的日期范围
        new_dates = df.select([
            pl.min('date').alias('min_date'),
            pl.max('date').alias('max_date')
        ])
        
        new_min = new_dates[0, 'min_date']
        new_max = new_dates[0, 'max_date']
        
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
    
    def append_data(self, df: pl.DataFrame|pd.DataFrame):
        """追加数据到Parquet文件"""
        if isinstance(df, pd.DataFrame):
            df = pl.from_pandas(df)

        if Path(self.file_path).exists():
            # 读取现有数据
            existing_df = pl.read_parquet(self.file_path)
            # 合并并去重
            combined_df = pl.concat([existing_df, df]).unique(['date', 'asset'])
        else:
            combined_df = df
        
        # 按 date 和 asset 排序以优化查询
        combined_df = combined_df.sort(['date', 'asset'])
        
        # 写入文件（自动压缩）
        combined_df.write_parquet(self.file_path, compression='snappy')
        
        # 更新日期范围缓存
        self._update_date_range(df)
    
    def query_stock_bars(self, asset: str, start_date: datetime.date = None, end_date: datetime.date = None):
        """查询个股数据"""
        lazy_df = pl.scan_parquet(self.file_path)
        
        # 构建过滤条件
        filters = [pl.col('asset') == asset]
        
        if start_date:
            filters.append(pl.col('date') >= start_date)
        if end_date:
            filters.append(pl.col('date') <= end_date)
        
        return lazy_df.filter(pl.all_horizontal(filters)).collect()
    
    def query_cross_section(self, date: datetime.date):
        """查询截面数据"""
        return (pl.scan_parquet(self.file_path)
                .filter(pl.col('date') == date)
                .collect())
```

框架的核心 API 是：

1. append_data，用来向本地存储追加数据（向前和向后都允许）
2. query_stock_bars，查询单支股票的行情
3. query_cross_section，查询某一日所有个股的数据
4. start 和 end 两个属性，帮助我们确定本地缓存的行情数据的起止日期。

下面的代码演示了它的用法：

```{code-block} python
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

现在，你就有了一个最简单的本地数据缓存框架。