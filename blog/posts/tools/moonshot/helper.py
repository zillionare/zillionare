import datetime
from pathlib import Path

import pandas as pd
import polars as pl
import tushare as ts
from loguru import logger


def resample_to_month(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    按月重采样，支持任意列的聚合方式

    Example:
        >>> resample_to_month(data, close='last', high='max', low='min', open='first', volume='sum')
    
    参数:
        data: DataFrame，需包含'date'和'asset'列。数据不要求有序。
        **kwargs: 关键字参数，格式为"列名=聚合方式"
                支持的聚合方式：'first'（首个值）、'last'（最后一个值）、
                                'mean'（平均值）、'max'（最大值）、'min'（最小值）
    
    返回:
        重采样后的DataFrame
    """
    df = pl.from_pandas(data)
    df = df.with_columns(pl.col('date').cast(pl.Datetime))
    
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col('date').dt.year().cast(pl.Utf8),
                pl.lit('-'),
                pl.col('date').dt.month().cast(pl.Utf8).str.pad_start(2, fill_char='0')
            ]
        ).alias('month')
    )
    
    # 定义支持的聚合方式映射（列名 -> 聚合表达式）
    agg_methods = {
        'first': lambda col: col.sort_by(pl.col('date')).first(),
        'last': lambda col: col.sort_by(pl.col('date')).last(),
        'mean': lambda col: col.mean(),
        'max': lambda col: col.max(),
        'min': lambda col: col.min(),
        'sum': lambda col: col.sum()
    }
    
    # 构建聚合表达式列表
    agg_exprs = []
    for col_name, method in kwargs.items():
        if col_name not in df.columns:
            raise ValueError(f"数据中不存在列: {col_name}")
        
        # 检查聚合方式是否支持
        if method not in agg_methods:
            raise ValueError(f"不支持的聚合方式: {method}，支持的方式为: {list(agg_methods.keys())}")
        
        # 添加聚合表达式
        agg_exprs.append(
            agg_methods[method](pl.col(col_name)).alias(col_name)
        )
    
    if not agg_exprs:
        raise ValueError("至少需要指定一个列的聚合方式（如open='first'）")
    
    result = df.group_by(
        pl.col('asset'),
        pl.col('month')
    ).agg(agg_exprs).sort(pl.col('month'), pl.col('asset'))
    
    result = result.to_pandas()
    result['month'] = pd.PeriodIndex(result['month'], freq='M')

    return result.set_index(['month', 'asset'])

def get_calendar(start: datetime.date, end: datetime.date) -> pd.Series:
    """通过tushare获取交易日历
    
    返回值为Series，索引为交易日历，值为前一个交易日。数据类型为datetime.date
    """
    pro = ts.pro_api()
    df = pro.trade_cal(exchange = 'SSE', 
                       start_date = start.strftime('%Y%m%d'), 
                       end_date = end.strftime('%Y%m%d'), 
                       is_open='1')

    df.index = pd.to_datetime(df['cal_date'], format="%Y%m%d").dt.date
    df["pre"] = pd.to_datetime(df["pretrade_date"], format="%Y%m%d").dt.date

    return df["pre"]


def qfq_adjustment(df: pd.DataFrame, adj_factor_col: str) -> pd.DataFrame:
    """
    前复权调整
    
    Args:
        df: 包含股价数据的DataFrame
        adj_factor_col: 复权因子列名
    
    Returns:
        前复权调整后的DataFrame
    """
    df = df.copy()
    price_cols = ['open', 'high', 'low', 'close']
    
    for col in price_cols:
        if col in df.columns:
            df[col] = df[col] * df[adj_factor_col]
    
    return df


def hfq_adjustment(df: pd.DataFrame, adj_factor_col: str) -> pd.DataFrame:
    """
    后复权调整
    
    Args:
        df: 包含股价数据的DataFrame
        adj_factor_col: 复权因子列名
    
    Returns:
        后复权调整后的DataFrame
    """
    df = df.copy()
    price_cols = ['open', 'high', 'low', 'close']
    
    # 计算基准复权因子（通常使用最早的复权因子）
    base_factor = df.groupby('asset')[adj_factor_col].first()
    
    for asset in df['asset'].unique():
        mask = df['asset'] == asset
        factor_ratio = base_factor[asset] / df.loc[mask, adj_factor_col]
        
        for col in price_cols:
            if col in df.columns:
                df.loc[mask, col] = df.loc[mask, col] * factor_ratio
    
    return df

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
            
            # 只有当合并后的df不为空时才添加
            if not df.empty:
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
        # 返回空的DataFrame而不是None，保持数据类型一致性
        return pd.DataFrame(columns=["date", "asset", "open", "high", "low", "close", "volume", "amount", "adj_factor"])

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
    
    # 确保 date 列为 datetime.date 类型
    if not pd.api.types.is_datetime64_any_dtype(result['date']):
        # 如果不是 datetime 类型，先转换为 datetime
        result['date'] = pd.to_datetime(result['date'], format='%Y%m%d')
    
    # 转换为 date 类型
    result['date'] = result['date'].dt.date

    return result

def fetch_dv_ttm(start: datetime.date, end: datetime.date) -> pd.DataFrame:
    """从tushare获取股息率数据
    
    Args:
        start: 开始日期
        end: 结束日期
        
    Returns:
        包含股息率等数据的DataFrame
    """    
    pro = ts.pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        # 只有当df不为空时才添加到列表中
        if not df.empty:
            dfs.append(df)
    
    # 如果没有获取到任何数据，返回空的DataFrame
    if not dfs:
        return pd.DataFrame(columns=["ts_code", "trade_date", "dv_ttm", "total_mv", "turnover_rate", "pe_ttm"])

    df = pd.concat(dfs)
    df = df.rename(columns={"trade_date": "date", "ts_code": "asset"})
    
    # 确保 date 列为 datetime.date 类型
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        # 如果不是 datetime 类型，先转换为 datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # 转换为 date 类型
    df['date'] = df['date'].dt.date
    
    return df

def dividend_yield_screen(data: pd.DataFrame, n: int = 500) -> pd.Series:
    """股息率筛选方法

    对每个月的股息率进行排名，选择前n名股票，标记为1，
    与现有flag进行逻辑与运算

    Args:
        n: 每月选择的股票数量，默认500
    """
    logger.info("开始进行股息率筛选...")

    if "dv_ttm" not in data.columns:
        raise ValueError("数据中不存在 dv_ttm 列，无法应用筛选器")

    def rank_top_n(group):
        # 计算每个股票在当月的排名（降序，股息率高的排名靠前）
        ranks = group.rank(method="first", ascending=False)

        return (ranks <= n).astype(int)

    # 按date分组，对 dividend_rate_ttm 进行排名筛选
    dividend_flags = data.groupby(level="month")["dv_ttm"].transform(rank_top_n)

    logger.info(f"已筛选出前{n}名股息率股")
    return dividend_flags



class ParquetUnifiedStorage:
    def __init__(self, store_path: str|Path, fetch_data_func=None):
        self.file_path = store_path
        self.fetch_data_func = fetch_data_func
        self._start_date = None
        self._end_date = None
        self._load_date_range()
    
    def __str__(self)->str:
        return f"{self.start} - {self.end}"
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
        
        # 缓存结果，并确保为date类型
        start_date = date_range[0, 'start_date']
        end_date = date_range[0, 'end_date']
        
        # 如果是datetime类型，转换为date类型
        if hasattr(start_date, 'date'):
            self._start_date = start_date.date()
        else:
            self._start_date = start_date
            
        if hasattr(end_date, 'date'):
            self._end_date = end_date.date()
        else:
            self._end_date = end_date
    
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
        
        # 如果是datetime类型，转换为date类型
        if hasattr(new_min, 'date'):
            new_min = new_min.date()
        if hasattr(new_max, 'date'):
            new_max = new_max.date()
        
        # 更新缓存的日期范围
        if self._start_date is None or new_min < self._start_date:
            self._start_date = new_min
        if self._end_date is None or new_max > self._end_date:
            self._end_date = new_max
    
    def load_data(self, start: datetime.date, end: datetime.date) -> pd.DataFrame:
        """
        根据指定的日期范围加载数据。
        如果本地缓存中包含完整的数据，则从缓存中加载；
        如果数据不足，则调用fetch_data_func方法获取数据。
        
        Args:
            start: 开始日期
            end: 结束日期
            
        Returns:
            DataFrame: 包含指定日期范围内数据的DataFrame
            
        Raises:
            ValueError: 如果未提供fetch_data_func且缓存中没有足够数据
        """
        # 检查是否有缓存数据且完全覆盖请求范围
        if (self._start_date is not None and self._end_date is not None and 
            self._start_date <= start and self._end_date >= end):
            # 完全覆盖，直接从缓存加载
            logger.info(f"从缓存加载数据: {start} 到 {end}")
            df = pl.scan_parquet(self.file_path)
            result = df.filter(
                (pl.col('date') >= start) & (pl.col('date') <= end)
            ).collect()
            return result.to_pandas()
        
        # 如果没有足够的缓存数据，需要获取缺失部分
        if self.fetch_data_func is None:
            raise ValueError("缓存中没有足够的数据，且未提供fetch_data_func方法")
        
        # 需要获取的数据列表
        dfs_to_append = []
        
        # 获取开始日期前缺失的数据
        if self._start_date is None or start < self._start_date:
            fetch_end = min(end, self._start_date - datetime.timedelta(days=1)) if self._start_date else end
            logger.info(f"获取开始日期前缺失的数据: {start} 到 {fetch_end}")
            new_data = self.fetch_data_func(start, fetch_end)
            if new_data is not None and (not new_data.empty if isinstance(new_data, pd.DataFrame) else not new_data.is_empty()):
                # 确保数据格式为Polars DataFrame
                if isinstance(new_data, pd.DataFrame):
                    new_data = pl.from_pandas(new_data)
                dfs_to_append.append(new_data)
        
        # 获取结束日期后缺失的数据
        if self._end_date is None or end > self._end_date:
            fetch_start = max(start, self._end_date + datetime.timedelta(days=1)) if self._end_date else start
            logger.info(f"获取结束日期后缺失的数据: {fetch_start} 到 {end}")
            new_data = self.fetch_data_func(fetch_start, end)
            if new_data is not None and (not new_data.empty if isinstance(new_data, pd.DataFrame) else not new_data.is_empty()):
                # 确保数据格式为Polars DataFrame
                if isinstance(new_data, pd.DataFrame):
                    new_data = pl.from_pandas(new_data)
                dfs_to_append.append(new_data)
        
        # 检查是否需要获取中间缺失的数据（缓存中存在数据但不连续）
        if (self._start_date is not None and self._end_date is not None and 
            self._start_date <= end and self._end_date >= start):
            # 存在缓存数据且与请求范围有交集，检查是否需要获取中间缺失的数据
            if self._end_date < end and start < self._end_date and self._start_date < start:
                # 需要获取中间缺失的数据
                fetch_start = self._end_date + datetime.timedelta(days=1)
                fetch_end = start - datetime.timedelta(days=1)
                if fetch_start <= fetch_end:
                    logger.info(f"获取中间缺失的数据: {fetch_start} 到 {fetch_end}")
                    new_data = self.fetch_data_func(fetch_start, fetch_end)
                    if new_data is not None and (not new_data.empty if isinstance(new_data, pd.DataFrame) else not new_data.is_empty()):
                        # 确保数据格式为Polars DataFrame
                        if isinstance(new_data, pd.DataFrame):
                            new_data = pl.from_pandas(new_data)
                        dfs_to_append.append(new_data)
        
        # 如果有新数据需要添加，则调用append_data
        if dfs_to_append:
            # 合并所有新数据
            if len(dfs_to_append) > 1:
                new_data_combined = pl.concat(dfs_to_append)
            else:
                new_data_combined = dfs_to_append[0]
            
            # 通过append_data添加新数据并获取合并后的完整数据
            combined_df = self.append_data(new_data_combined)
        elif self._start_date is not None and self._end_date is not None:
            # 没有新数据，但缓存中已有数据，直接从现有缓存加载
            logger.info("请求的数据已全部在缓存中")
            df = pl.scan_parquet(self.file_path)
            combined_df = df.collect()
        else:
            # 缓存中没有数据，且fetch_data_func没有返回数据
            logger.warning(f"fetch_data_func未返回{start}到{end}范围内的数据")
            # 返回空的DataFrame
            return pd.DataFrame()
        
        # 确保combined_df存在
        if 'combined_df' not in locals() or combined_df is None:
            logger.error("未能获取到任何数据")
            return pd.DataFrame()
        
        # 返回请求范围内的数据
        # 检查combined_df是否为空，避免过滤空DataFrame时出错
        if combined_df.height > 0:
            result = combined_df.filter(
                (pl.col('date') >= start) & (pl.col('date') <= end)
            )
        else:
            # 如果combined_df为空，直接返回空的DataFrame
            result = combined_df
        
        # 确保结果存在且为DataFrame
        if result is None:
            logger.error(f"数据过滤失败，未能获取{start}到{end}范围内的数据")
            return pd.DataFrame()
            
        return result.to_pandas()
    
    def append_data(self, df: pl.DataFrame|pd.DataFrame) -> pl.DataFrame:
        """追加数据到Parquet文件
        
        Args:
            df: 要追加的数据
            
        Returns:
            合并后的完整数据
        """
        if isinstance(df, pd.DataFrame):
            df = pl.from_pandas(df)
        
        # 检查df是否为空
        if df.is_empty():
            if Path(self.file_path).exists():
                # 如果传入的数据为空，但文件已存在，直接返回文件中的数据
                existing_df = pl.read_parquet(self.file_path)
                # 更新日期范围缓存
                self._update_date_range(existing_df)
                return existing_df
            else:
                # 如果传入的数据为空且文件不存在，返回空的DataFrame
                empty_df = pl.DataFrame(schema=df.schema)
                return empty_df
            
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
        
        return combined_df
    
    @property
    def start(self)->datetime.date|None:
        """获取数据起始日期"""
        return self._start_date
    
    @property
    def end(self)->datetime.date|None:
        """获取数据终止日期"""
        return self._end_date
    
    def query_single(self, asset: str, start_date: datetime.date|None = None, end_date: datetime.date|None = None):
        """查询单个资产在[start_date, end_date]之间的记录
        
        Args:
            asset: 资产代码
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            
        Returns:
            DataFrame: 查询结果
        """
        lazy_df = pl.scan_parquet(self.file_path)
        
        # 构建过滤条件
        filters = [pl.col('asset') == asset]
        
        assert isinstance(start_date, datetime.date) and (not isinstance(start_date, datetime.datetime)), "start_date必须为date类型"

        assert isinstance(end_date, datetime.date) and (not isinstance(end_date, datetime.datetime)), "end_date必须为date类型"

        filters.append(pl.col('date') >= start_date)
        filters.append(pl.col('date') <= end_date)
        
        return lazy_df.filter(pl.all_horizontal(filters)).collect()
    
    def query_range(self, start_date: datetime.date, end_date: datetime.date):
        """获取在[start_date, end_date]区间内的所有记录
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame: 查询结果
        """
        assert isinstance(start_date, datetime.date) and (not isinstance(start_date, datetime.datetime)), "start_date必须为date类型"

        assert isinstance(end_date, datetime.date) and (not isinstance(end_date, datetime.datetime)), "end_date必须为date类型"
            
        lazy_df = pl.scan_parquet(self.file_path)
        
        # 构建过滤条件
        filters = [
            pl.col('date') >= start_date,
            pl.col('date') <= end_date
        ]
        
        return lazy_df.filter(pl.all_horizontal(filters)).collect()
    
    def query(self, assets: list[str], start_date: datetime.date | None = None, 
              end_date: datetime.date | None = None):
        """查询在[start_date, end_date]间 asset 列在 assets 中的记录
        
        Args:
            assets: 资产代码列表
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            
        Returns:
            DataFrame: 查询结果
        """
        lazy_df = pl.scan_parquet(self.file_path)
        
        # 构建过滤条件
        filters = [pl.col('asset').is_in(assets)]
        
        assert isinstance(start_date, datetime.date) and (not isinstance(start_date, datetime.datetime)), "start_date必须为date类型"

        assert isinstance(end_date, datetime.date) and (not isinstance(end_date, datetime.datetime)), "end_date必须为date类型"

        filters.append(pl.col('date') >= start_date)
        filters.append(pl.col('date') <= end_date)

        return lazy_df.filter(pl.all_horizontal(filters)).collect()
    
    def query_cross_section(self, date: datetime.date):
        """查询截面数据"""
        assert isinstance(date, datetime.date) and (not isinstance(date, datetime.datetime)), "date必须为date类型"
            
        return (pl.scan_parquet(self.file_path)
                .filter(pl.col('date') == date)
                .collect())
