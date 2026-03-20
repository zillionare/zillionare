import datetime
from typing import Iterable
from tqdm import tqdm
import pandas as pd
import polars as pl
import tushare as ts
from loguru import logger


def _fetch_by_dates(
    func_name: str,
    dates: Iterable[datetime.date] | datetime.date,
    *args,
    fields: str | None = None,
    rename_as: dict[str, str] | None = None,
    **kwargs,
) -> pd.DataFrame:
    """通用 fetch 函数。

    Tushare 许多方法都是通过 trade_date 为主要参数，以获得该交易日某一类型全部数据。本方法在这些方法的基础上，提供多日数据的聚合，排序、字段重命名、错误处理等功能，对日期字段转换为 datetime.date 等。

    Args:
        func_name: tushare 方法名
        dates: 日期，可以是单个日期，也可以是日期列表。
        fields: tushare 返回字段。它的顺序也将成为返回 dataframe中的列序。
        rename_as: 如果不为 None，则将据此重命名字段。如果为 None，则固定将 ts_code/trade_date 重命名为 asset/date。如果不希望发生重命名，请传入{}
    """
    all_data = []
    errors = []

    if isinstance(dates, Iterable):
        _dates = list(dates)
    else:
        _dates = [dates]

    _rename_as = (
        {"ts_code": "asset", "trade_date": "date"} if rename_as is None else rename_as
    )

    pro = ts.pro_api()
    func = getattr(pro, func_name)

    with tqdm(total=len(_dates), desc=f"获取{func_name}数据") as pbar:
        for date in sorted(_dates):  # type: ignore
            pbar.set_description(f"获取{func_name}数据 - {date}")
            pbar.update(1)
            str_date = date.strftime("%Y%m%d")
            try:
                df = func(trade_date=str_date, fields=fields)
            except Exception as e:
                logger.error("调用 {} 时出错, {}", func_name, e)
                errors.append([func_name, date, f"调用{func_name}时出现异常"])
                continue

            if df is None or df.empty:
                all_data.append(df)
                error_msg = f"{func_name}获取{date}日数据失败"
                logger.warning(error_msg)
                errors.append([func_name, date, error_msg])
            else:
                all_data.append(df)

    if len(all_data) == 0:
        return pd.DataFrame()

    result = pd.concat(all_data, ignore_index=True)
    if fields:
        columns = map(lambda x: x.strip(), fields.split(","))
        result = result[columns]

    if len(_rename_as) != 0:
        result = result.rename(columns=_rename_as)

    result["date"] = pd.to_datetime(result["date"], format="%Y%m%d").dt.date
    result = result.sort_values(by="date")

    return result


def fetch_calendar(start: datetime.date) -> pd.DataFrame:
    """从tushare获取交易日历，并保存到SQLite数据库

    Returns:
        包含交易日历的DataFrame
    """
    logger.info(f"获取从 {start} 起的交易日历")

    pro = ts.pro_api()

    # 获取交易日历数据
    df = pro.trade_cal(exchange="SSE", start_date=start.strftime("%Y%m%d"))

    if df is None or df.empty:
        logger.warning("没有获取到交易日历数据")
        return pd.DataFrame()

    # 转换日期格式
    df["date"] = pd.to_datetime(df["cal_date"], format="%Y%m%d").dt.date
    df["prev"] = pd.to_datetime(df["pretrade_date"], format="%Y%m%d").dt.date

    df = df.sort_values("date").set_index("date")
    return df[["is_open", "prev"]]


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
            df = pro.fina_audit(
                ts_code=sec,
                start_date=start.strftime("%Y%m%d"),
                end_date=end.strftime("%Y%m%d"),
            )
            if not df.empty:
                all_data.append(df)
        except Exception as e:
            logger.error(f"获取 {sec} 的财务审计意见失败: {e}")
            continue

    if len(all_data) == 0:
        logger.warning(f"在 {start} 到 {end} 之间，没有获取到任何财务审计意见数据")
        return None

    df = pd.concat(all_data, ignore_index=True)
    df = df.rename(columns={"end_date": "date", "ts_code": "asset"})

    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d").dt.date

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
        return pd.DataFrame(
            columns=[
                "ts_code",
                "trade_date",
                "dv_ttm",
                "total_mv",
                "turnover_rate",
                "pe_ttm",
            ]
        )

    df = pd.concat(dfs)
    df = df.rename(columns={"trade_date": "date", "ts_code": "asset"})

    # 确保 date 列为 datetime.date 类型
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        # 如果不是 datetime 类型，先转换为 datetime
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

    # 转换为 date 类型
    df["date"] = df["date"].dt.date

    return df


def fetch_daily_basic(dates: Iterable[datetime.date] | datetime.date) -> pd.DataFrame:
    fields = "ts_code,trade_date,close,turnover_rate,turnover_rate_f,dv_ratio, dv_ttm, pe, pe_ttm, total_mv,circ_mv"
    rename_as = {"ts_code": "asset", "trade_date": "date"}

    return _fetch_by_dates("daily_basic", dates, fields=fields, rename_as=rename_as)


def fetch_bars(
    dates: Iterable[datetime.date] | datetime.date,
) -> pd.DataFrame:
    """通过 tushare 接口，获取日线行情数据

    返回数据未复权，但包含了复权因子，因此可以增量获取叠加。返回数据为升序。

    Args:
        dates: 需要获取的交易日列表，允许不连续

    Returns:
        DataFrame: 包含date, asset, open,high,low,close,volume,amount
        Error: date, msg
    """
    fields = "trade_date,ts_code,open,high,low,close,vol,amount"
    rename_as = {"ts_code": "asset", "trade_date": "date", "vol": "volume"}

    return _fetch_by_dates("daily", dates, fields=fields, rename_as=rename_as)


def fetch_adjust_factor(
    dates: Iterable[datetime.date] | datetime.date,
) -> pd.DataFrame:
    """获取指定交易日的复权因子

    因子以 adjust 字段返回
    """
    rename_as = {
        "trade_date": "date",
        "adj_factor": "adjust",
        "ts_code": "asset",
    }
    return _fetch_by_dates("adj_factor", dates, rename_as=rename_as)


def fetch_bars_ext(
    dates: Iterable[datetime.date] | datetime.date,
) -> pd.DataFrame:
    """获取日线行情、ST 和涨跌停价

    返回的 dataframe 将包含以下字段：
        date, asset, open,high,low,close,volume,amount,adjust
    Args:
        dates (list[datetime.date] | datetime.date): 交易日

    Returns:
        tuple[pd.DataFrame, list[list]]: 行情数据和错误信息
    """
    bars = fetch_bars(dates)
    adjust = fetch_adjust_factor(dates)

    if bars.empty:
        return pd.DataFrame()

    # use polars for performance
    bars_pl = pl.from_pandas(bars).lazy()
    adjust_pl = pl.from_pandas(adjust).lazy()

    df = bars_pl.join(adjust_pl, on=["date", "asset"], how="left").collect().to_pandas()

    # to_pandas 会导致日期变为 datetime.datetime 类型
    df["date"] = df["date"].dt.date
    return df


def fetch_dividend(start: datetime.date, end: datetime.date):
    """每年分红除权情况

    Args:
        start (datetime.date): 起始日期
        end (datetime.date): 截止日期

    Returns:
        返回 dataframe, date 为公告日期，fiscal_year 为公告对应财年
    """
    dfs = []
    limit = 2000
    pro = ts.pro_api()
    for yr in range(start.year, end.year + 1):
        dt = f"{yr}1231"
        # 对每一个交易日，都可能有超过 limit 条记录
        for offset in range(0, 99):
            df = pro.dividend(end_date=dt, offset=offset * limit, limit=limit)
            dfs.append(df)
            if len(df) < 2000:
                break

    # 如果取太快，会导致 tushare 拒绝访问
    data = pd.concat(dfs)
    data["date"] = pd.to_datetime(data["ann_date"]).dt.date
    data["fiscal_year"] = pd.to_datetime(data["end_date"]).dt.year

    return (
        data.rename(columns={"ts_code": "asset"})
        .drop(["end_date", "ann_date"], axis=1)
        .dropna(subset=["date"])
    )
