import datetime
from pathlib import Path

import pandas as pd
import polars as pl
from loguru import logger


def ensure_date(date: datetime.datetime | str | datetime.date) -> datetime.date:
    """将输入的日期转换为datetime.date类型

    Args:
        date: 输入的日期，可以是datetime.datetime、str或datetime.date类型
            如果是str类型，格式必须为'%Y%m%d'

    Returns:
        datetime.date: 转换后的日期

    Raises:
        ValueError: 当输入的日期类型不支持时抛出
    """
    if isinstance(date, str):
        return datetime.datetime.strptime(date, "%Y%m%d").date()
    elif isinstance(date, datetime.datetime):
        return date.date()
    elif isinstance(date, datetime.date):
        return date
    else:
        raise ValueError(f"Unsupported date type: {type(date)}")


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
    df = df.with_columns(pl.col("date").cast(pl.Datetime))

    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("date").dt.year().cast(pl.Utf8),
                pl.lit("-"),
                pl.col("date").dt.month().cast(pl.Utf8).str.pad_start(2, fill_char="0"),
            ]
        ).alias("month")
    )

    # 定义支持的聚合方式映射（列名 -> 聚合表达式）
    agg_methods = {
        "first": lambda col: col.sort_by(pl.col("date")).first(),
        "last": lambda col: col.sort_by(pl.col("date")).last(),
        "mean": lambda col: col.mean(),
        "max": lambda col: col.max(),
        "min": lambda col: col.min(),
        "sum": lambda col: col.sum(),
    }

    # 构建聚合表达式列表
    agg_exprs = []
    for col_name, method in kwargs.items():
        if col_name not in df.columns:
            raise ValueError(f"数据中不存在列: {col_name}")

        # 检查聚合方式是否支持
        if method not in agg_methods:
            raise ValueError(
                f"不支持的聚合方式: {method}，支持的方式为: {list(agg_methods.keys())}"
            )

        # 添加聚合表达式
        agg_exprs.append(agg_methods[method](pl.col(col_name)).alias(col_name))

    if not agg_exprs:
        raise ValueError("至少需要指定一个列的聚合方式（如open='first'）")

    result = (
        df.group_by(pl.col("asset"), pl.col("month"))
        .agg(agg_exprs)
        .sort(pl.col("month"), pl.col("asset"))
    )

    result = result.to_pandas()
    result["month"] = pd.PeriodIndex(result["month"], freq="M")

    return result.set_index(["month", "asset"])


def get_calendar(start: datetime.date, end: datetime.date) -> pd.Series:
    """通过tushare获取交易日历

    返回值为Series，索引为交易日历，值为前一个交易日。数据类型为datetime.date
    """
    pro = ts.pro_api()
    df = pro.trade_cal(
        exchange="SSE",
        start_date=start.strftime("%Y%m%d"),
        end_date=end.strftime("%Y%m%d"),
        is_open="1",
    )

    df.index = pd.to_datetime(df["cal_date"], format="%Y%m%d").dt.date
    df["pre"] = pd.to_datetime(df["pretrade_date"], format="%Y%m%d").dt.date

    return df["pre"]


def qfq_adjustment(df: pd.DataFrame, adj_factor_col: str = "adjust") -> pd.DataFrame:
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
