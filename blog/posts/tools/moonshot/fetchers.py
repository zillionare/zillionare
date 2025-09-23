import datetime

import pandas as pd
import tushare as ts
from loguru import logger


def fetch_fina_audit(start: datetime.date, end: datetime.date) -> pd.DataFrame | None:
    """
    通过 tushare 接口，获取财务审计意见数据。该函数通过遍历指定日期范围内的每一天来获取数据。

    Args:
        start: 开始日期 (基于公告日期 ann_date)
        end: 结束日期 (基于公告日期 ann_date)

    Returns:
        DataFrame: 包含审计意见等数据的DataFrame，如果无数据则返回None
    """
    pro = ts.pro_api()
    all_data = []

    df = pro.daily_basic()
    securities = df["ts_code"].tolist()

    for sec in securities:
        try:
            df = pro.fina_audit(ts_code = sec, 
                            start_date = start.strftime("%Y%m%d"), 
                            end_date=end.strftime("%Y%m%d"))
            if not df.empty:
                all_data.append(df)
        except Exception as e:
            logger.error(f"获取 {sec} 的财务审计意见失败: {e}")
            continue

    if len(all_data) == 0:
        logger.warning(f"在 {start} 到 {end} 之间，没有获取到任何财务审计意见数据")
        return None
        
    df = pd.concat(all_data, ignore_index=True)
    df = df.rename(columns={'end_date': 'date', 'ts_code': 'asset'})

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.date
    
    return df


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
