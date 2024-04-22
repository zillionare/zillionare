import datetime
import functools
import os
import pickle
from typing import Optional, Tuple

import akshare as ak
import arrow
import numpy as np
import pandas as pd
from coretypes import Frame, FrameType
from IPython.display import display
from numpy.typing import NDArray
from omicron import tf
from scipy.signal import argrelmax


@functools.lru_cache
def get_secs(exclude_st=True, exclude_kcb=True, size=(0, 1)):
    with open("/data/secs.pkl", "rb") as f:
        df = pickle.load(f)
        
        if exclude_st:
            df = df[df.name.str.find("ST")==-1]
            
        if exclude_kcb:
            df = df[~df.symbol.str.startswith("68")]
            
        low = df.cap.quantile(size[0])
        high = df.cap.quantile(size[1])
                         
        return df[(df.cap >= low) & (df.cap <= high)].to_records(index=False)
    
@functools.lru_cache
def get_name(symbol):
    df = get_secs(exclude_st=False, exclude_kcb=False)
    name = df[df.symbol == symbol]["name"]
    return name.item()

def get_index_bars(symbol: str, n: int, frame_type: FrameType, end: Optional[Frame]=None)-> NDArray:
    """获取指数行情数据

    Args:
        symbol: 指数代码，如"000001"
        n: 获取最近n个周期的数据
    returns:
        返回一个结构化数组，包含以下字段：frame, open, high, low, close, volume, amount, turnover, pct
    """
    if frame_type not in [FrameType.MIN1,
                          FrameType.MIN30,
                          FrameType.DAY,
                          FrameType.MONTH,
                          FrameType.WEEK
                        ]:
        raise ValueError("frame_type must be one of FrameType.MIN30, FrameType.DAY, FrameType.MONTH, FrameType.WEEK")
        
    period = {
        FrameType.MIN1: '1',
        FrameType.MIN30: '30',
        FrameType.DAY: 'daily',
        FrameType.MONTH: 'monthly',
        FrameType.WEEK: 'weekly'
    }.get(frame_type)

    mapper = {
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount",
        "换手率": "turnover"
    }

    end = arrow.get(end or arrow.now("Asia/Shanghai")).naive
    floor_end = tf.floor(end, frame_type)
    start = tf.shift(floor_end, -n, frame_type)
    if frame_type in [FrameType.MIN1, FrameType.MIN30]:
        df = ak.index_zh_a_hist_min_em(symbol, period=period)
        mapper["时间"] = "frame"
    else:
        start_at = start.strftime("%Y%m%d")
        end_at = end.strftime("%Y%m%d")
        df = ak.index_zh_a_hist(symbol, period=period, start_date=start_at, end_date=end_at)
        mapper["日期"] = "frame"

    df = df.rename(mapper, axis=1)
    
    if "turnover" in df.columns:
        df["turnover"] = df["turnover"] /100
    df["frame"] = pd.to_datetime(df.frame).astype("O")

    print(start, end, df)
    if frame_type in [FrameType.MIN1, FrameType.MIN30]:
        df = df[(df.frame >= start) & (df.frame <= end)]
    
    cols = ["frame", "open", "high", "low", "close", "volume", "amount"]
    if "turnover" in df.columns:
        cols.append("turnover")
    if "pct" in df.columns:
        cols.append("pct")
        
    return df[cols].to_records(index=False)


def get_bars(symbol: str, n: int, frame_type: FrameType,  end: Optional[Frame]=None, fq='qfq')-> NDArray:
    """获取股票行情数据(仅限股票，不能用于获取指数)

        Args:
            symbol: 股票代码，6位数字
            n: 获取最近n个周期的数据
            frame_type: FrameType.MIN30, FrameType.DAY, FrameType.MONTH, FrameType.WEEK
            end: 截止日期/时间。如果未提供，则使用当前系统时间
        returns:
            返回一个结构化数组，包含以下字段：frame, open, high, low, close, volume, amount, turnover, pct
    """
    if frame_type not in [FrameType.MIN1, 
                          FrameType.MIN30, 
                          FrameType.DAY, 
                          FrameType.MONTH, 
                          FrameType.WEEK
                        ]:
        raise ValueError("frame_type must be one of FrameType.MIN1, FrameType.MIN30, FrameType.DAY, FrameType.MONTH, FrameType.WEEK")
        
    period = {
        FrameType.MIN1: '1',
        FrameType.MIN30: '30',
        FrameType.DAY: 'daily',
        FrameType.MONTH: 'monthly',
        FrameType.WEEK: 'weekly'
    }.get(frame_type)

    mapper = {
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount",
        "换手率": "turnover",
        "涨跌幅": "pct"
    }

    end = arrow.get(end or arrow.now("Asia/Shanghai")).naive
    floor_end = tf.floor(end, frame_type)
    start = tf.shift(floor_end, -n, frame_type)
    if frame_type in [FrameType.MIN1, FrameType.MIN30]:
        df = ak.stock_zh_a_hist_min_em(symbol, period='30', adjust=fq)
        mapper["时间"] = "frame"
    else:
        start_at = start.strftime("%Y%m%d")
        end_at = end.strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(symbol, period=period, start_date=start_at, end_date=end_at, adjust=fq)
        mapper["日期"] = "frame"

    df = df.rename(mapper, axis=1)
    
    columns = ["frame", "open", "high", "low", "close", "volume", "amount"]
    if "pct" in df.columns:
        df["pct"] = df["pct"]/100
        columns.append("pct")
    if "turnover" in df.columns:
        df["turnover"] = df["turnover"] /100
        columns.append("turnover")

    if frame_type in [FrameType.MIN1, FrameType.MIN30]:
        df["frame"] = pd.to_datetime(df.frame).astype("O")
        df = df[(df.frame >= start) & (df.frame <= end)]
        
    return df[columns].to_records(index=False)


def find_strike(bars:pd.DataFrame, threshold: float=0.33)->Tuple[float, pd.DataFrame]:
    """判断是否存在上涨超过9%的情况，如果存在，返回以该时刻为起点的bars，否则返回None.
    
    """
    if len(bars) < 2:
        return None, None
    
    strikes = np.argwhere(bars[1:]["high"]/bars[:-1]["close"] - 1 > 0.09).flatten()
    if len(strikes) == 0:
        return None, None
            
    # where strike happend
    pos = strikes[-1] + 1
    
    # 计算之后的反向成交量
    try:
        ratio, index = reverse_volume_direction(bars[pos:])
        # index 不为零，意味着后面出现更大的量, ratio为零表明最大成交量为阴线
        if 0 < ratio <= threshold and index == 0:
            return ratio, bars[pos:]
    except Exception:
        pass
    
    return None, None

def arc_string_score(arc, digits:int = 3) -> float: # type: ignore
    """根据弓与弦关系来计算时间序列`ts`的方向性

    将弦围成的面积，与弦与ts围成的面积进行相加的结果，除以序列长度进行归一化后，作为分数返回。

    如果ts为一条直线，无波动，则返回值相当于直线斜率。否则，ts[0]与ts[-1]构成的弦上，位于其上的点构成卖出动力，围成的面积算负，在其下的点构成买入回归动力，围成的面积算正。

    由于chord严重依赖于最后一期ts的值，从而影响到score，因此，建议在均线上使用。

    Returns:
        代表方向性的数值，范围不明，大致在[-0.1, 0.1]之间。如为负数，则表明方向向下，如果为正，则表明方向向上。
    """
    arc_ = arc/arc[0]
    string = np.linspace(arc_[0], arc_[-1], len(arc))
    area1 = sum(string - arc_[0])
    area2 = sum(string - arc_)

    return round((area1 + area2)/len(arc), 3)


def bear_bull_ratio(returns):
    # Separate the positive and negative returns
    positive_returns = returns[returns >= 0]
    negative_returns = returns[returns < 0]
    # Calculate the median of positive returns
    median_positive = np.median(positive_returns)

    n1 = np.count_nonzero(negative_returns <= -median_positive)
    n2 = np.count_nonzero(positive_returns >= median_positive)

    # Calculate the ratio
    ratio = n1/(n1+n2)

    return round(ratio, 3)


def diag(symbol:str, at: datetime.datetime=None, show_msg=True):
    """诊断`symbol`的以下指标：
    
    1. 日线arc: 5, 10, 20
    2. 30分线arc: 5, 10, 20
    3. 日线和30分线RSI
    
    指标：
    
    | 股票   | 日期 | 阳线率 | 20 日涨幅 | d5    | d10   | d20   | m5    | m10   | m20    |
    |-------|------|-------|----------|-------|-------|-------|-------|-------|--------|
    | 博迈科 | 3/28 | 0.55  | 0.095    | 0.039 | 0.064 | 0.053 | 0.011 | 0.004 | -0.006 |

    """
    arc_win = 16

    if at is None:
        at = arrow.now("Asia/Shanghai").floor('hour').replace(hour=15).naive
        
    dbars = get_bars(symbol, 48, end=at.date())
    mbars = get_m30_bars(symbol, 48, end=at)
    
        
    features = extract_features(dbars, mbars)
    d5, d10, d20 = (features[0][i] for i in ("d5", "d10", "d20"))
    m5, m10, m20 = (features[0][i] for i in ("m5", "m10", "m20"))
        
    name = get_name(symbol)
    
    msg = []
    
    reverse_vol_ratio, bars_ = find_strike(mbars[-16:])
    if reverse_vol_ratio is not None:
        msg.append(("冲击涨停", "✅", f"反向量{reverse_vol_ratio} | {len(bars_)}周期"))

    if np.all(np.array([d5, d10, d20]) > 0.01):
        if np.sum(np.array([m5, m10, m20]) > 0.001) >= 2:
            msg.append(("均线走势(日线/30)", "✅ ✅", f"{d5} {d10} {d20} | {m5} {m10} {m20}"))
        elif np.sum(np.array([m5, m10, m20]) < 0) >= 2:
            msg.append(("均线走势(日线/30)", "✅ ⚠️", f"{d5} {d10} {d20} | {m5} {m10} {m20}"))
    elif np.all(np.array([d5, d10, d20]) < 0):
        if np.sum(np.array([m5, m10, m20]) < 0) >= 2:
            msg.append(("均线走势(日线/30)", "⚠️ ⚠️", f"{d5} {d10} {d20} | {m5} {m10} {m20}"))
        elif np.sum(np.array([m5, m10, m20]) > 0.001) >= 2:
            msg.append(("均线走势(日线/30)", "⚠️ ✅", f"{d5} {d10} {d20} | {m5} {m10} {m20}"))

    pnl,br, drsi_flag, mrsi_flag = features[0]["pnl"], features[0]["br"], features[0]["drsi_flag"], features[0]["mrsi_flag"]
    drsi = list(features[0][[f"drsi{i}" for i in range(5, 0, -1)]])
    mrsi = list(features[0][[f"mrsi{i}" for i in range(5, 0, -1)]])

    if drsi_flag == 1:
        dflag = "✅"
    elif drsi_flag == -1:
        dflag = "⚠️"
    else:
        dflag = " "
            
    if mrsi_flag == 1:
        mflag = "✅"
    elif mrsi_flag == -1:
        mflag = "⚠️"
    else:
        mflag = " "
        
    msg.append(("rsi(日线/30)", f"{dflag} {mflag}", f"{drsi[-2]}->{drsi[-1]} | {mrsi[-2]}->{mrsi[-1]}"))
    
    
    if np.max(drsi) > 90:
        msg.append(("日线 RSI 超过90", "⚠️", f"{drsi}"))
        
    if np.max(mrsi) > 90:
        msg.append(("30分RSI超过90", "⚠️", f"{drsi}"))
        
    dsupport, dresist = features[0]["dsupport"], features[0]["dresist"]
    if dsupport != 0:
        msg.append(("日线支撑", "✅", f"{dsupport}"))
    if dresist != 0:
        msg.append(("日线压力",  "⚠️", f"{dresist}"))
    
    msupport, mresist = features[0]["msupport"], features[0]["mresist"]
    if msupport != 0:
        msg.append(("30分支撑", "✅", f"{msupport}"))
    if mresist != 0:
        msg.append(("30分压力", "⚠️", f"{mresist}"))
              
    max_r, min_r, norm_r = features[0]["max_r"], features[0]["min_r"], features[0]["norm_r"]
    if max_r > 0.095 and norm_r > 0.55 and 0.07 <= pnl < 0.18 and br >= 0.7:
        flag = "✅"
    elif br <= 0.5 and pnl < 0:
        flag = "⚠️"
    else:
        flag = ""
        
    msg.append(("20日涨幅、阳线率", flag, f"涨跌: {pnl:.1%} | 阳线: {br:.0%} | 最大涨幅: {max_r:.1%} | 涨跌比: {norm_r: .0%}"))
    
    # 上影线压力确认
    pos, price = shadow_pressure(dbars)
    if pos == -1:
        msg.append(("上影线压力", "⚠️", f"压力位{price}"))
        
    # 提示 顶背离
    div_flag, p0, dist = rsi_peak_divergent(dbars)
    if div_flag:
        msg.append(("RSI顶背离", "⚠️", f"{p0} {dist}"))
    
    if show_msg:
        print(f"======== {name} ========")

        # set_properties(subset=["Abbreviation", "Storage"], **{'text-align': 'center'})
        df = pd.DataFrame(msg, columns=["item", "flag", "data"])
        styled = df.style.hide_index().hide_columns().set_properties(subset=["flag", "data"],**{'text-align':'left'})
        display(styled)
    
    return features
    
def diag_month(symbol, frame: datetime.date=None, show_msg=True):
    bars = get_bars(symbol, 48, end = frame, frame_type=FrameType.MONTH)
    if len(bars) < 48:
        return None
    
    close = bars["close"]
    frames = bars["frame"]

    rsi = ta.RSI(close.astype(np.float64), 6)[-5:]
    rsi = array_math_round(rsi, 1)
    name = get_name(symbol)
    max_profit = round(np.max(close[-24:])/np.min(close[-24:])-1,3)
    
    rsi_warning = (np.max(rsi) > 90) | (rsi[-1] < rsi[-2])
    row = [name, symbol, max_profit]
    scores = []
    for win in (5, 10, 20, 30):
        ma = moving_average(close, win)[-12:]
        score = math_round(arc_string_score(ma), 3)
        scores.append(score)
        row.append(score)

    row.extend((rsi_warning, rsi[-1]))
    
    msg = []
    flag = "⚠️" if max_profit > 1 else ""
    if max_profit > 1 or max_profit < 0.2:
        flag = "⚠️"
    else:
        flag = "✅"
        
    msg.append((flag, "12月最大涨幅", f"{max_profit}"))
    
    scores = np.array(scores)

    if np.sum(scores < 0.001) >= 2:
        flag = "⚠️"
    elif np.sum(scores > 0.001) >= 3:
        flag = "✅"
    msg.append((flag, "均线走势", f"{scores[0]} {scores[1]} {scores[2]} {scores[3]}"))
    
    flag = "⚠️" if rsi_warning else "✅"
    msg.append((flag, "rsi报警", f"{np.max(rsi)} | {rsi[-1]}"))
    
    if show_msg:
        print(f"========== {name} ==========")
        df = pd.DataFrame(msg, columns=["flag", "item", "data"])
        styled = df.style.hide_index().hide_columns().set_properties(subset=["flag", "item", "data"],**{'text-align':'left'})
        display(styled)
    
    return row

def reverse_volume_direction(bars) -> Tuple[float, int]:
    """最大成交量出现以后，逆向成交量的占比
    
    如果返回值为负，说明最大成交量为阴线。
    """
    volume = bars["volume"]
    frames = bars["frame"]

    flags = np.select(
        (bars["close"] > bars["open"], bars["close"] < bars["open"]), [1, -1], 0
    )

    # 最大成交量位置
    pmax = np.argmax(volume)

    # 最大成交量及之后的成交量，带方向
    vol = (volume * flags)[pmax:]
    vmax = vol[0]
    
    # pmax之后的异向成交量
    reverse_vol = np.max(np.abs(vol[1:][flags[pmax + 1:] != flags[pmax]]))
    
    
    return round(reverse_vol / vmax, 2), pmax

def get_security_list():
    sz = ak.stock_info_sz_name_code()
    sz = (sz.rename(columns = {
    "A股代码": "symbol",
    "A股简称": "name",
    "A股流通股本": "cap"}))[["symbol", "name", "cap"]]
    sz.cap = sz.cap.apply(lambda x: float(x.replace(",", "")))
    
    shlist = ak.stock_info_sh_name_code()

    recs = []
    for symbol in shlist["证券代码"]:
        df = ak.stock_individual_info_em(symbol)
        cap = df[df.item == "流通股"].iloc[0]["value"]
        name = df[df.item == "股票简称"].iloc[0]["value"]
        recs.append((symbol, name, cap))
        
             

    sh = pd.DataFrame(recs, columns=["symbol", "name", "cap"])
    
    kcblist = ak.stock_info_sh_name_code("科创板")
    recs = []
             
    for symbol in kcblist["证券代码"]:
        df = ak.stock_individual_info_em(symbol)
        cap = df[df.item == "流通股"].iloc[0]["value"]
        name = df[df.item == "股票简称"].iloc[0]["value"]
        recs.append((symbol, name, cap))
             
    
    kcb = pd.DataFrame(recs, columns=["symbol", "name", "cap"])
             
    df = pd.concat([sh, sz, kcb])
    return df

def support_resist(bars, ma_groups=None):
    """判断是否存在均线压制或者支撑的情况
    
    如果股价在最近三期中，存在
    1. 开盘、收盘于某均线之下，最高点在[ma * 0.99, ma*1.01]之间，均线弧分在1e-4之下，每尝试一次加1分
    2. 开盘、收盘于某均线之上，最低点在[ma * 0.99, ma*1.01]之间，均线弧分在1e-3之上，每尝试一次加1分
    
    返回值为Tuple，前者为支撑分，越大表明尝试次数越多，支撑越强；后者为压力分，越大表明压力越大。均在[0,1]之间
    """
    ma_groups = ma_groups or [10, 20]

    opn = bars["open"][-3:]
    high = bars["high"][-3:]
    low = bars["low"][-3:]
    close = bars["close"][-3:]
        
    strength = [0, 0]
    for win in ma_groups:
        ma = moving_average(bars["close"], win)
        score = arc_string_score(ma[-5:])
        ma = ma[-3:]
                
        if score < 1e-4:
            flags = (opn < ma) & (close < ma) & (high > ma * 0.99)
            strength[1] += sum(flags)
        if score > 1e-3:
            flags = (opn > ma) & (close > ma) & (low <= ma * 1.01)
            strength[0] += sum(flags)

    return np.round(np.array([strength[0], strength[1]])/(3 * len(ma_groups)),2)

def extract_features(dbars, mbars):
    """提取以下特征
    
    1. 日线arc: 5, 10, 20 （arc_win: 16)
    2. 30分线arc: 5, 10, 20 (arc_win: 16)
    3. 日线和30分线RSI
    4. 是否出现过冲击涨停（超9%），以及此后的逆向成交量比
    5. 20日涨幅
    6. 20日内阳线占比
    7. 均线压力或支撑，前者为压力强度，后者为支撑强度
    8. 20日最大涨幅、最大跌幅及归一化比率
    
    Args:
        dbars: structured array, 日线
        mbars: structured array, 30分钟线
    """
    arc_win = 16
    ma_groups = [5, 10, 20]
    
        
    assert len(dbars) >= max(48, arc_win + max(ma_groups))
    assert len(mbars) >= max(48, arc_win + max(ma_groups))

    # 如果mbars不是在15时结束的，则dbars也要重新采样
    if mbars[-1]["frame"].hour != 15:
        # 转换为Python 时间
        end = mbars[-1]["frame"].to_pydatetime()
        
        # 要与mbars["frame"]比较
        start = np.datetime64(datetime.datetime(end.year, end.month, end.day, 10))
        filter_ = (mbars["frame"] >= start) & (mbars["frame"] <= np.datetime64(end))
        unclose = mbars[filter_]

        frame = end.date()
        opn = unclose[0]["open"]
        high = np.max(unclose["high"])
        low = np.min(unclose["low"])
        close = unclose[-1]["close"]
        volume = np.sum(unclose["volume"])
        amount = np.sum(unclose["amount"])
        turnover = np.sum(unclose["turnover"])
        pct = close/dbars[-2]["close"]-1

        rec = np.array([(frame, opn, high, low, close, volume, amount, turnover, pct)], dtype=dbars.dtype)
        dbars[-1] = rec

    # 阳线比例
    flags = (dbars["close"] >= dbars["open"])[-20:]
    bull_rate = np.count_nonzero(flags)/20


    # 20日以来的pnl
    pnl = round(dbars[-1]["close"]/dbars[-20]["close"] - 1, 3)
        
    scores = [bull_rate, pnl]
       
    # 日线及30分钟线arc score
    dscores = []
    mscores = []
    for win in ma_groups:
        ma = moving_average(dbars["close"], win)
        dscores.append(np.round(arc_string_score(ma[-arc_win:]), 3))
        
        ma = moving_average(mbars["close"], win)
        mscores.append(np.round(arc_string_score(ma[-arc_win:]), 3))
        
    scores.extend(dscores)
    scores.extend(mscores)
    
    # 日线及分钟线rsi
    drsi = ta.RSI(dbars["close"].astype(np.float64), 6)[-5:]
    mrsi = ta.RSI(mbars["close"].astype(np.float64), 6)[-5:]
    
    scores.extend(np.round(drsi[-5:], 1))
    scores.extend(np.round(mrsi[-5:], 1))
    
    # 2日内冲击涨停及此后逆向量比
    ratio, bars = find_strike(mbars[-16:])
    scores.extend((ratio, len(bars) if bars is not None else None))
    
    # 最后两期rsi的方向，上涨或者下跌？
    flag = np.select([drsi[-1] > drsi[-2] + 0.1, drsi[-1] < drsi[-2] - 0.1], [1, -1], default = 0).item()
    scores.append(flag)
    
    flag = np.select([mrsi[-1] > mrsi[-2] + 0.1, mrsi[-1] < mrsi[-2] - 0.1], [1, -1], default = 0).item()
    scores.append(flag)
    
    # 日线、30分钟均线压力支撑
    scores.extend(support_resist(dbars))
    scores.extend(support_resist(mbars))
    
    # 日线每日收益率
    returns = dbars["close"][1:]/dbars["close"][:-1]-1
    max_r = np.max(returns[-20:])
    min_r = np.min(returns[-20:])
    if max_r < 0:
        norm_r = 0
    else:
        norm_r = max_r/(abs(min_r) + max_r)
        
    scores.extend((max_r, min_r, norm_r))
    
    return pd.DataFrame([scores], columns = [
        "br", "pnl",
        *(f"d{win}" for win in (5, 10, 20)), 
        *(f"m{win}" for win in (5, 10, 20)),
        *(f"drsi{i}" for i in range(5, 0, -1)),
        *(f"mrsi{i}" for i in range(5, 0, -1)),
        "vol_r", "dist",
        "drsi_flag", "mrsi_flag",
        "dsupport", "dresist", "msupport", "mresist",
        "max_r", "min_r", "norm_r"
    ]).to_records(index=False)


def add_sample(symbol, frame: datetime.datetime, label:str, replace=False):
    """记录标注数据
    
    标注数据由symbol和frame惟一确定。
    label: 
        "B": 立即买入
        "S": 立即卖出
        "BW": 观察买入，比如下一个30分钟出现长下影，或者rsi转涨
        "SW": 观察卖出
        "H" (hold)
    """
    
    feature = diag(symbol, frame)
    name = get_name(symbol)

    
    dtypes = [("symbol", "O"), ("name", "O"), ("frame", "O"), ("label", "O")] + feature.dtype.descr
    data = np.array([], dtype=dtypes)
    
    record = np.array([(symbol, name, frame, label, *feature[0])], dtype=dtypes)
    
    
    if os.path.exists("label-data.pkl"):
        with open("label-data.pkl", "rb") as f:
            data = pickle.load(f)
        
    pos = np.argwhere((data["symbol"] == symbol) & (data["frame"] == frame)).flatten()
    if len(pos):
        if replace:
            data[pos[0]] = record
    else:
        data = np.concatenate((data, record))

            
    with open("label-data.pkl", "wb") as f:
        pickle.dump(data, f)


def read_label_data(symbol: str=None):
    with open("label-data.pkl", "rb") as f:
        data = pickle.load(f)
        if symbol is not None:
            return data[data["symbol"] == symbol]
        else:
            return data
            
def list_labels():
    with open("label-data.pkl", "rb") as f:
        data = pickle.load(f)
        return pd.DataFrame(data[["symbol", "name", "frame", "label"]])
    
def change_label(symbol, frame, label):
    with open("label-data.pkl", "rb") as f:
        data = pickle.load(f)
        filter = (data["symbol"] == symbol) & (data["frame"] == frame)
        if len(data[filter]) == 0:
            print("记录未找到！")
            return

        data["label"][filter] = label
        
    assert len(data) > 0
    with open("label-data.pkl", "wb") as f:
        pickle.dump(data, f)
        
def rsi_peak_divergent(
    bars: np.array, rsi: np.array = None, win:int=20
) -> Tuple[bool, int, int]:
    """寻找最近满足条件的rsi顶背离。

        如果存在顶背离，返回值[0]为True；如果股价新高，RSI新高，返回值[0]为False。否则返回值[0]为None
        Examples:
            603565.XSHG, FrameType.DAY, (2024, 4, 1) -> False, -4, 2
            603565.XSHG, FrameType.DAY, (2024, 4, 2) -> True, -1, 4
        Args:
            bars: 行情数组
            rsi: 如果存在，则直接使用，否则计算rsi
            win: 查找区间
        Returns:
            (是否有顶背离, 最后一个顶点距现在位置，两个顶点距离）
    """
    assert len(bars) >= win
    close = bars["close"]
    frames = bars["frame"][-win:]
    
    if rsi is None:
        rsi = ta.RSI(close.astype(np.float64), 6)
    else:
        assert len(rsi) > win
        
    rsi = rsi[-win:]

    close = close[-win:]
    pos = argrelmax(close)[0][-2:]
    if len(pos) < 2:
        return None, None, None
        
    p1, p0 = pos - win
    
    if close[p1] > close[p0]:
        maxp = p1
    else:
        maxp = p0
    
    # argrelmax不会检测最后一个bar是否为最高点
    if close[-1] > close[p0]:
        p0 = -1
        p1 = maxp
        
    if close[p0] > close[p1] and rsi[p0] < rsi[p1]:
        return True, p0, p0 - p1
    
    if close[p0] > close[p1] and rsi[p0] > rsi[p1]:
        return False, p0, p0 - p1
    
    return None, None, None

def shadow_pressure(bars, win:int=5)->Tuple[int, float]:
    """检测win周期内出现的上影线确认压力
    
    算法：最高点存在上影线，或者另一个接近最高点的，存在上影线
    Examples:
        603558 2024/3/19, -1, 11.03
        603558 2024/3/20, -2, 11.03
        603558 2024/4/12, None, None
        603558 2024/1/17, True, 10.27
    """
    bars = bars[-win:]
    shadows = upper_shadow(bars)
    high = bars["high"]
    hh = np.max(high)
    
    pos = np.argwhere(high >= hh * 0.99).flatten()
    pos2 = np.argwhere(shadows[pos] > 0.66).flatten()
    
    if len(pos2) > 0:
            latest = pos[pos2[-1]]
            return latest - win, high[latest]
    else:
        return None, None
    

def upper_shadow(bars):
    """计算上影线长度。大于0.5意味着上影线比实体长"""
    opn = bars["open"]
    close = bars["close"]
    high = bars["high"]
    
    body = np.abs(close-opn)
    shadow = high - np.select([close >= opn, close < opn], [close, opn])
    
    return shadow / (body + shadow)
