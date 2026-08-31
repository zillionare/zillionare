#!/usr/bin/env python3
"""Weekly, forecast-first LLM experiment on CSI 1000 (000852.SH).

This module is deliberately honest about what it does: choosing an exposure for
the coming week *is* a forecast of the next week's return. We feed the model a
four-week feature window (weekly PnL, daily ATR, daily RSI, daily z-score) and
ask it to predict next week's return / choose a position. We then measure the
hit-rate and risk-adjusted performance against that same next-week return.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

TRADING_DAYS = 252
WEEKS_PER_YEAR = 52

WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五"]


def load_env():
    if load_dotenv is None:
        return
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        candidate = parent / ".env"
        if candidate.exists():
            load_dotenv(candidate)
            break


def env(name, default=""):
    return os.getenv(name, default)


@dataclass
class Config:
    symbol: str = "000852.SH"
    start: str = "20160101"
    rebalance_weekday: int = 0  # 0=Mon ... 4=Fri
    rsi_period: int = 5
    rsi_warmup: int = 60
    atr_period: int = 14
    z_window: int = 5
    weeks_history: int = 4
    history_weeks: int = 48  # 每次会话附带的历史周数（含下一周结果标签）
    cost_bps: float = 5.0
    max_weeks: int = None  # None -> all rebalance weeks
    model: str = ""


# --------------------------------------------------------------------------- #
# Data acquisition + caching (avoid hitting tushare on every debug run)
# --------------------------------------------------------------------------- #
def first_column(columns, alternatives):
    lookup = {str(item).strip().lower(): item for item in columns}
    return next((lookup[name.lower()] for name in alternatives if name.lower() in lookup), None)


def fetch_index(symbol, start, end=None, cache_path=None):
    import tushare as ts

    token = env("tushare_token")
    if not token:
        raise RuntimeError("请在 .env 中设置 tushare_token。")

    # Cache: reuse a downloaded frame so we don't call tushare each run.
    if cache_path and Path(cache_path).exists():
        frame = pd.read_parquet(cache_path)
        frame.index = pd.to_datetime(frame.index)
        return frame

    raw = ts.pro_api(token).index_daily(
        ts_code=symbol,
        start_date=start,
        end_date=end or pd.Timestamp.today().strftime("%Y%m%d"),
    )
    if raw is None or raw.empty:
        raise RuntimeError("Tushare 没有返回数据；请检查 token、权限、代码与网络。")

    date_col = first_column(raw.columns, ["trade_date", "date", "日期"])
    frame = raw.rename(columns={date_col: "date"}).copy()
    for col in ["open", "high", "low", "close", "pre_close"]:
        if col not in frame.columns:
            raise RuntimeError("指数日线缺少列：%s" % col)
    frame["date"] = pd.to_datetime(frame["date"].astype(str).str.strip(), format="%Y%m%d", errors="coerce")
    frame = frame.dropna(subset=["date", "close"]).set_index("date").sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    for col in ["open", "high", "low", "close", "pre_close"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")

    if cache_path:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(cache_path)
    return frame


# --------------------------------------------------------------------------- #
# Indicators
# --------------------------------------------------------------------------- #
def true_range(high, low, prev_close):
    prev = prev_close.shift(1).fillna(prev_close)
    tr = pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)
    return tr


def atr(high, low, prev_close, period=14):
    tr = true_range(high, low, prev_close)
    return tr.ewm(alpha=1.0 / period, min_periods=period).mean()


def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.fillna(50.0)


def zscore(close, window=20):
    mean = close.rolling(window).mean()
    std = close.rolling(window).std().replace(0, np.nan)
    return (close - mean) / std


# --------------------------------------------------------------------------- #
# Feature snapshot for one rebalance date
# --------------------------------------------------------------------------- #
def make_features(data, config):
    f = data.copy()
    f["atr"] = atr(f.high, f.low, f.pre_close, config.atr_period)
    f["atr_pct"] = f["atr"] / f["close"]
    f["rsi5"] = rsi(f["close"], config.rsi_period)
    # 至少用 60 日数据算 RSI，丢掉前 59 个计算结果
    f.loc[f.index < f.index[config.rsi_warmup - 1], "rsi5"] = np.nan
    f["z5"] = zscore(f["close"], config.z_window)
    return f


def _week_features(feats, closes, i):
    """第 i 个调仓周（以调仓日收盘为界）的特征。"""
    date = closes.index[i]
    window = feats.loc[:date].tail(5)  # 该周的 5 个交易日（含调仓日当天）
    return {
        "date": str(date.date()),
        "pnl": float(closes.iloc[i] / closes.iloc[i - 1] - 1.0),
        "atr_pct": float(window["atr_pct"].astype(float).mean()),
        "rsi5": [float(x) for x in window["rsi5"]],
        "zscore5": [float(x) for x in window["z5"]],
    }


def _next_week_outcome(feats, closes, i):
    """第 i 周对应的下一周结果：涨跌幅与周日收益年化夏普。"""
    d0, d1 = closes.index[i], closes.index[i + 1]
    daily_rets = feats["close"].pct_change().loc[(feats.index > d0) & (feats.index <= d1)]
    pnl = float(closes.iloc[i + 1] / closes.iloc[i] - 1.0)
    std = float(daily_rets.std(ddof=1)) if len(daily_rets) > 1 else 0.0
    sharpe = float(daily_rets.mean() / std * np.sqrt(TRADING_DAYS)) if std else 0.0
    return {"next_pnl": pnl, "next_sharpe": sharpe}


def build_records(feats, config):
    """One record per weekly rebalance date.

    每条记录 = 本周特征 + 过去 history_weeks 周的（特征 + 下一周结果）历史表。
    历史表让 LLM 像读训练集一样对照“当时长什么样、下一周发生了什么”。
    """
    candidates = feats.index[feats.index.weekday == config.rebalance_weekday]
    closes = feats["close"].reindex(candidates).dropna()

    records = []
    first_with_history = config.history_weeks  # 需要足够长的前史
    for k in range(config.weeks_history, len(closes) - 1):
        date = closes.index[k]
        close_k = closes.iloc[k]
        w_pnl = [closes.iloc[k] / closes.iloc[k - w] - 1.0 for w in range(1, config.weeks_history + 1)]

        history = []
        if k >= first_with_history:
            for i in range(k - config.history_weeks, k):
                entry = _week_features(feats, closes, i)
                entry.update(_next_week_outcome(feats, closes, i))
                history.append(entry)

        next_date = closes.index[k + 1]
        records.append({
            "date": date,
            "close": float(close_k),
            "w4_pnl": float(w_pnl[3]),
            "w3_pnl": float(w_pnl[2]),
            "w2_pnl": float(w_pnl[1]),
            "w1_pnl": float(w_pnl[0]),
            "this_week": _week_features(feats, closes, k),
            "history": history,
            "next_week_return": float(closes.iloc[k + 1] / close_k - 1.0),
        })
    return records


# --------------------------------------------------------------------------- #
# LLM call (trend analysis -> position action) + cache
# --------------------------------------------------------------------------- #
PROMPT_VERSION = "trend-v2"  # 提示词/特征/仓位语义版本：变化时应升级，避免复用旧缓存；v3 已实验否决


RAISE_ACTIONS = {"买入", "加大仓位"}
LOWER_ACTIONS = {"减少仓位", "空仓观望"}


def reconcile_position(prev_position, action, position):
    """强制 action 与 position 自洽：买入/加仓须高于上周仓，减仓/空仓须低于上周仓。"""
    a = str(action or "").strip()
    p = position
    if a in RAISE_ACTIONS and p <= prev_position:
        p = min(1.0, round(prev_position + 0.10, 2))
    elif a in LOWER_ACTIONS and p >= prev_position:
        p = max(0.0, round(prev_position - 0.10, 2))
    return p


def llm_forecast(record, config, prev_position=0.0):
    api_key = env("LLM_API_KEY")
    base_url = env("LLM_BASE_URL")
    model = config.model or env("LLM_MODEL") or "glm-5.3"
    if not api_key:
        raise RuntimeError("未设置 LLM_API_KEY")
    if not base_url:
        base_url = "https://api.deepseek.com/v1"

    # 防护：特征含 NaN（预热期未满）不发请求，由外层降级为空仓
    def _has_nan(week):
        return any(np.isnan(v) for v in week["rsi5"] + week["zscore5"] + [week["pnl"], week["atr_pct"]])

    if _has_nan(record["this_week"]) or any(_has_nan(h) for h in record["history"]):
        raise ValueError("特征含 NaN（预热期未满），该周不调用 LLM")

    instruction = {
        "任务": (
            "你是周频趋势研判员。结合历史样本，判断当前市场处于：上涨趋势、下跌趋势、"
            "还是即将反转/正在反转/已经反转；并据此决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
            "只做多，不做空。研究回测，非投资建议。"
        ),
        "特征含义": {
            "pnl": "该周涨跌幅（按调仓日收盘对上周调仓日收盘计算）",
            "atr_pct": "该周 5 个交易日 ATR/收盘价 的均值（波动强度）",
            "rsi5": "该周每个交易日当天及前 4 天（5 日窗口）的 RSI 序列，按时间升序",
            "zscore5": "该周每个交易日收盘价相对 5 日均线的 z-score 序列，按时间升序",
            "next_pnl": "（仅历史样本有）该周对应的下一周实际涨跌幅",
            "next_sharpe": "（仅历史样本有）下一周日收益的年化夏普",
        },
        "研判要求": [
            "先从历史样本中找与当前周特征相似的阶段，看它们下一周实际表现（next_pnl / next_sharpe）",
            "再判断当前趋势状态与动能变化（停滞、加速、反转迹象）",
            "最后给出下周动作与目标仓位；证据不足时保持中等仓位，不要满仓赌单一情形",
        ],
        "仓位自洽规则": (
            "position 必须与 action 自洽：action 为『买入』或『加大仓位』时，新的 position 必须【大于】当前已有仓位 prev_position；"
            "action 为『减少仓位』或『空仓观望』时，position 必须【小于】prev_position。系统会据此校正你的输出。"
        ),
        "prev_position": prev_position,  # 上周（上个调仓日）的持仓仓位（初始为 0）
        "当前周": {k: record["this_week"][k] for k in ["date", "pnl", "atr_pct", "rsi5", "zscore5"]},
        "历史样本（过去 %d 周，由远及近，均含下一周实际结果）" % len(record["history"]): record["history"],
        "输出格式": {
            "trend": "上涨趋势|下跌趋势|反转酝酿|反转进行中|反转已确立",
            "action": "买入|加大仓位|减少仓位|空仓观望",
            "position": "下周目标仓位，浮点数 [0,1]，且与 action 自洽（参考 prev_position）",
            "confidence": "0-1",
            "reason": "一句话理由",
        },
    }

    # max_tokens 必须显式给足：推理模型的思考 token 也计入，默认上限会截断正文导致拿不到 JSON
    # reasoning_effort=max 让模型尽力推理；部分网关不支持该字段时会自行忽略
    payload = {"model": model, "stream": False, "max_tokens": 16000,
               "reasoning_effort": "max",
               "messages": [
                   {"role": "system", "content": "只输出 JSON。"},
                   {"role": "user", "content": json.dumps(instruction, ensure_ascii=False)},
               ]}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    request = urllib.request.Request(
        endpoint, data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key, "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    last_error = None
    text = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
            last_error = None
            break
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = error
    if last_error is not None:
        raise RuntimeError("LLM 请求失败：%s" % last_error) from last_error

    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM 未返回 JSON。")
    parsed = json.loads(text[start:end + 1])
    action = str(parsed.get("action", "")).strip()
    position = min(1.0, max(0.0, float(parsed.get("position", 0.5))))
    # 与 action 自洽：买入/加仓须高于上周，减仓/空仓须低于上周
    position = reconcile_position(prev_position, action, position)
    return {
        "trend": str(parsed.get("trend", "")),
        "action": action,
        "position": position,
        "confidence": float(parsed.get("confidence", 0.0)),
        "reason": str(parsed.get("reason", "") or parsed.get("adjustment_reason", "")),
        "raw": text,
    }


def forecast_cached(record, config, out, prev_position=0.0):
    out.mkdir(parents=True, exist_ok=True)
    cache_path = out / ("llm-%s-%s.json" % (PROMPT_VERSION, str(record["date"].date())))
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        cached["position"] = reconcile_position(prev_position, cached.get("action", ""), cached["position"])
        return cached, True
    forecast = llm_forecast(record, config, prev_position)
    cache_path.write_text(json.dumps(forecast, ensure_ascii=False, indent=2), encoding="utf-8")
    return forecast, False


# --------------------------------------------------------------------------- #
# Backtest / evaluation
# --------------------------------------------------------------------------- #
def run_backtest(records, positions, cost_bps=5.0):
    equity = 1.0
    rows = []
    peak = 1.0
    for rec, pos in zip(records, positions):
        gross = pos * rec["next_week_return"]
        cost = abs(pos) * cost_bps / 10000.0
        net = gross - cost
        equity *= 1.0 + net
        peak = max(peak, equity)
        rows.append({"date": rec["date"], "position": pos, "next_week_return": rec["next_week_return"],
                     "gross_return": gross, "net_return": net, "equity": equity, "drawdown": equity / peak - 1.0})
    return pd.DataFrame(rows).set_index("date")


def metrics(df):
    ret = df["net_return"]
    years = len(ret) / WEEKS_PER_YEAR
    eq = df["equity"]
    drawdown = eq / eq.cummax() - 1
    # 长多头口径：以 0.5 为中性线，仓位明显偏离中性且方向与下周一致记为命中
    tilt = df["position"] - 0.5
    clear = (tilt.abs() >= 0.25) & (df["next_week_return"] != 0)
    hit_rate = float((np.sign(tilt[clear]) == np.sign(df["next_week_return"][clear])).mean()) if clear.any() else float("nan")
    return {
        "total_return": float(eq.iloc[-1] - 1.0),
        "cagr": float(eq.iloc[-1] ** (1 / years) - 1.0) if years > 0 else 0.0,
        "annual_vol": float(ret.std(ddof=0) * np.sqrt(WEEKS_PER_YEAR)),
        "sharpe": float(ret.mean() / ret.std(ddof=0) * np.sqrt(WEEKS_PER_YEAR)) if ret.std(ddof=0) else 0.0,
        "max_drawdown": float(drawdown.min()),
        "hit_rate": hit_rate,
        "clear_weeks": int(clear.sum()),
        "avg_position": float(df["position"].mean()),
        "corr": float(df["position"].corr(df["next_week_return"])),
        "weeks": int(len(ret)),
    }


def main():
    global config
    parser = argparse.ArgumentParser(description="周频、诚实的 LLM 预测回测（中证1000）")
    parser.add_argument("--start", default="20160101")
    parser.add_argument("--weekday", type=int, default=0, choices=[0, 1, 2, 3, 4], help="调仓日：0=周一 ... 4=周五")
    parser.add_argument("--max-weeks", type=int, default=None, help="最多评估的周数（用于调试，None=全部）")
    parser.add_argument("--out", type=Path, default=Path("output"))
    args = parser.parse_args()

    load_env()
    config = Config(rebalance_weekday=args.weekday, max_weeks=args.max_weeks, model=env("LLM_MODEL"))

    cache = Path(args.out) / "data" / (config.symbol.replace(".", "_") + ".parquet")
    data = fetch_index(config.symbol, args.start, None, cache_path=cache)
    print("数据：%d 根日线（缓存 %s）" % (len(data), cache))
    feats = make_features(data, config)
    records = build_records(feats, config)
    if config.max_weeks:
        records = records[-config.max_weeks:]
    print("周频样本数：%d" % len(records))

    # Buy & Hold: position always 1.0
    bh = run_backtest(records, [1.0] * len(records), config.cost_bps)
    # Simple momentum rule (long-only): 持有当且仅当上周为正收益
    mom = run_backtest(records, [1.0 if r["w1_pnl"] > 0 else 0.0 for r in records], config.cost_bps)

    # LLM forecast（仓位随 prev_position 顺序累积，保证 action 自洽）
    llm_positions = []
    llm_dir = Path(args.out) / "llm_cache"
    llm_failures = 0
    prev_position = 0.0
    for rec in records:
        try:
            fc, _ = forecast_cached(rec, config, llm_dir, prev_position)
            prev_position = fc["position"]
            llm_positions.append(fc["position"])
        except Exception as error:
            llm_failures += 1
            # 失败降级为空仓：释放上周仓位
            prev_position = 0.0
            llm_positions.append(0.0)
            print("  第 %s 周 LLM 失败，改用空仓：%s" % (rec["date"].date(), error))
    print("LLM 失败周数：%d / %d" % (llm_failures, len(records)))
    llm = run_backtest(records, llm_positions, config.cost_bps)

    print("\n== 买入持有 ==")
    print(json.dumps(metrics(bh), ensure_ascii=False, indent=2))
    print("\n== 动量规则 ==")
    print(json.dumps(metrics(mom), ensure_ascii=False, indent=2))
    print("\n== LLM 预测 ==")
    print(json.dumps(metrics(llm), ensure_ascii=False, indent=2))

    bh.to_csv(Path(args.out) / "daily_bh.csv", encoding="utf-8-sig")
    mom.to_csv(Path(args.out) / "daily_mom.csv", encoding="utf-8-sig")
    llm.to_csv(Path(args.out) / "daily_llm.csv", encoding="utf-8-sig")
    print("\n输出目录：%s" % args.out.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
