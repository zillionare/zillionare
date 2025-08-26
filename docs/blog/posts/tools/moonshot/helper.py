import datetime
import logging
import time

import pandas as pd
import polars as pl
import tushare as ts

logger = logging.getLogger("quantide")

# ts.set_token("cd37b17c96794f7a7b3c5e1f1b982cc70b4c94c2ac79b81a09d356b8")
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


# def pro_api():
#     """
#     获取tushare pro api实例
    
#     Returns:
#         tushare pro api实例
#     """
#     return ts.pro_api()


def get_calendar(start: datetime.date, end: datetime.date) -> pd.Series:
    """通过tushare获取交易日历
    
    返回值为Series，索引为交易日历，值为前一个交易日。数据类型为datetime.date
    """
    pro = pro_api()
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

    pro = pro_api()

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
