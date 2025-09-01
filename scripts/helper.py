import datetime
from pathlib import Path

import pandas as pd


def fetch_dv_ttm(start: datetime.date, end: datetime.date) -> pd.DataFrame:
    """从tushare获取股息率数据
    
    Args:
        start: 开始日期
        end: 结束日期
        
    Returns:
        包含股息率等数据的DataFrame
    """
    from startup import pro_api
    
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        dfs.append(df)

    df = pd.concat(dfs)
    return df.rename(columns={"trade_date": "date", "ts_code": "asset"})


def load_dv_ttm(start: datetime.date, end: datetime.date) -> pd.DataFrame:
    """获取[start, end]区间的股息率数据。

    先检查 data_home / "dv_ttm.parquet" 是否存在，如果存在，从其中加载数据为 df，
    该数据应该包含 asset, date, dv_ttm, total_mv, turnover_rate, pe_ttm 字段。

    然后比较 [start, end]与 df["date"].unique(), 找出df 中没有的日期，
    再调用 fetch_dv_ttm 补齐后返回。
    """
    # 定义数据存储路径
    data_home = Path("/tmp/moonshot/data")
    cache_file = data_home / "dv_ttm.parquet"
    
    # 确保目录存在
    data_home.mkdir(parents=True, exist_ok=True)
    
    # 如果缓存文件存在，则加载
    if cache_file.exists():
        df = pd.read_parquet(cache_file)
        
        # 获取现有数据的日期范围
        existing_dates = set(pd.to_datetime(df["date"]).dt.date)
        requested_dates = set(pd.bdate_range(start, end).date)
        
        # 找出缺失的日期
        missing_dates = requested_dates - existing_dates
        
        if missing_dates:
            # 将缺失的日期分为两个区间：早于现有数据的和晚于现有数据的
            min_existing_date = min(existing_dates) if existing_dates else start
            max_existing_date = max(existing_dates) if existing_dates else start
            
            dates_to_fetch = sorted(list(missing_dates))
            early_dates = [d for d in dates_to_fetch if d < min_existing_date]
            late_dates = [d for d in dates_to_fetch if d > max_existing_date]
            
            # 获取缺失的数据
            dfs_to_concat = [df]
            if early_dates:
                early_start = min(early_dates)
                early_end = max(early_dates)
                early_df = fetch_dv_ttm(early_start, early_end)
                dfs_to_concat.append(early_df)
                
            if late_dates:
                late_start = min(late_dates)
                late_end = max(late_dates)
                late_df = fetch_dv_ttm(late_start, late_end)
                dfs_to_concat.append(late_df)
                
            # 合并数据并保存回缓存
            df = pd.concat(dfs_to_concat, ignore_index=True)
            df.to_parquet(cache_file)
    else:
        # 如果缓存文件不存在，获取数据并创建缓存
        df = fetch_dv_ttm(start, end)
        df.to_parquet(cache_file)
        
    # 筛选指定日期范围内的数据
    df["date"] = pd.to_datetime(df["date"])
    mask = (df["date"].dt.date >= start) & (df["date"].dt.date <= end)
    result = df[mask].copy()
    
    return result