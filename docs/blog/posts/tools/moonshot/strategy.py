import datetime
import os
import sys
from pathlib import Path

import fire
import pandas as pd
import polars as pl
import tushare as ts
from loguru import logger

sys.path.append(str(Path(__file__).parent))
import tushare as ts
from helper import (ParquetUnifiedStorage, dividend_yield_screen, fetch_bars,
                    fetch_dv_ttm)
from moonshot import Moonshot

if Path("/data").exists():
    data_home = Path("/data")
else:
    data_home = Path("~/workspace/data/").expanduser()

def dividend_yield_screen(data: pd.DataFrame, n: int = 500)->pd.Series:
    """股息率筛选方法
    
    对每个月的股息率进行排名，选择前n名股票，标记为1，
    与现有flag进行逻辑与运算
    
    Args:
        n: 每月选择的股票数量，默认500
    """
    logger.info("开始进行股息率筛选...")
    
    if 'dv_ttm' not in data.columns:
        raise ValueError("数据中不存在 dv_ttm 列，无法应用筛选器")
    
    def rank_top_n(group):
        # 计算每个股票在当月的排名（降序，股息率高的排名靠前）
        ranks = group.rank(method='first', ascending=False)

        return (ranks <= n).astype(int)
    
    # 按date分组，对 dividend_rate_ttm 进行排名筛选
    dividend_flags = data.groupby(level='month')['dv_ttm'].transform(rank_top_n)

    logger.info(f"已筛选出前{n}名股息率股")
    return dividend_flags


def main():
    start = datetime.date(2018, 1, 1)
    end = datetime.date(2023, 12, 31)

    store_path = data_home / "rw/bars.parquet"
    bars_store = ParquetUnifiedStorage(store_path = store_path, fetch_data_func=fetch_bars)

    barss = bars_store.load_data(start, end)
    ms = Moonshot(barss)

    store_path = data_home / "rw/dv_ttm.parquet"
    dv_store = ParquetUnifiedStorage(store_path = store_path, fetch_data_func=fetch_dv_ttm)

    dv_ttm = dv_store.load_data(start, end)

    ms.append_factor(dv_ttm, "dv_ttm", resample_method = 'last')
    # 添加股息率筛选器
    (ms.screen(dividend_yield_screen, data = ms.data, n=500)
        .calculate_returns()
        .report())
    
fire.Fire(main)
