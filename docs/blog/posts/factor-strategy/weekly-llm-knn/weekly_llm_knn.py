#!/usr/bin/env python3
"""weekly-llm-knn: 在 v2 基础上做两项增强的对照实验：
   A. 相似周 top-k 检索 —— 用归一化欧氏距离从历史中挑最像的 k 周喂给 LLM；
   B. 输出离散化 —— 把连续仓位量化到 {0.3, 0.5, 0.7}，逼模型明确表态。
图形本与 v2(weekly_llm.py) 一致，改动点集中在 build_records / knn 检索 / 量化三处。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
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
        if (parent / ".env").exists():
            load_dotenv(parent / ".env")
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
    history_weeks: int = 48
    knn_k: int = 5            # 相似周 top-k
    quantize: bool = False    # 输出是否离散化到 {0.3,0.5,0.7}
    quant_levels: tuple = (0.3, 0.5, 0.7)
    cost_bps: float = 5.0
    max_weeks: int = None
    model: str = ""


# --------------------------------------------------------------------------- #
# Data acquisition + caching
# --------------------------------------------------------------------------- #
def fetch_index(symbol, start, end=None, cache_path=None):
    import tushare as ts
    token = env("tushare_token")
    if not token:
        raise RuntimeError("请在 .env 中设置 tushare_token。")
    if cache_path and Path(cache_path).exists():
        frame = pd.read_parquet(cache_path)
        frame.index = pd.to_datetime(frame.index)
        return frame
    raw = ts.pro_api(token).index_daily(ts_code=symbol, start_date=start,
                                        end_date=end or pd.Timestamp.today().strftime("%Y%m%d"))
    if raw is None or raw.empty:
        raise RuntimeError("Tushare 没有返回数据。")
    frame = raw.rename(columns={"trade_date": "date"}).copy()
    frame["date"] = pd.to_datetime(frame["date"].astype(str).str.strip(), format="%Y%m%d", errors="coerce")
    for col in ["open", "high", "low", "close", "pre_close"]:
        if col not in frame.columns:
            raise RuntimeError("缺列：" + col)
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=["date", "close"]).set_index("date").sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    if cache_path:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(cache_path)
    return frame


# --------------------------------------------------------------------------- #
# Indicators (与 v2 相同)
# --------------------------------------------------------------------------- #
def true_range(high, low, prev_close):
    prev = prev_close.shift(1).fillna(prev_close)
    return pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)


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
    return (100 - 100 / (1 + rs)).fillna(50.0)


def zscore(close, window=20):
    mean = close.rolling(window).mean()
    std = close.rolling(window).std().replace(0, np.nan)
    return (close - mean) / std


def make_features(data, config):
    f = data.copy()
    f["atr"] = atr(f.high, f.low, f.pre_close, config.atr_period)
    f["atr_pct"] = f["atr"] / f["close"]
    f["rsi5"] = rsi(f["close"], config.rsi_period)
    f.loc[f.index < f.index[config.rsi_warmup - 1], "rsi5"] = np.nan
    f["z5"] = zscore(f["close"], config.z_window)
    return f


def _week_features(feats, closes, i):
    date = closes.index[i]
    window = feats.loc[:date].tail(5)
    return {
        "date": str(date.date()),
        "pnl": float(closes.iloc[i] / closes.iloc[i - 1] - 1.0),
        "atr_pct": float(window["atr_pct"].astype(float).mean()),
        "rsi5": [float(x) for x in window["rsi5"]],
        "zscore5": [float(x) for x in window["z5"]],
    }


def _next_week_outcome(feats, closes, i):
    d0, d1 = closes.index[i], closes.index[i + 1]
    daily_rets = feats["close"].pct_change().loc[(feats.index > d0) & (feats.index <= d1)]
    pnl = float(closes.iloc[i + 1] / closes.iloc[i] - 1.0)
    std = float(daily_rets.std(ddof=1)) if len(daily_rets) > 1 else 0.0
    sharpe = float(daily_rets.mean() / std * np.sqrt(TRADING_DAYS)) if std else 0.0
    return {"next_pnl": pnl, "next_sharpe": sharpe}


# --------------------------------------------------------------------------- #
# 相似周 top-k 检索
# --------------------------------------------------------------------------- #
def _week_vector(w):
    """把一周特征压成固定长度向量。"""
    return np.array([w["pnl"], w["atr_pct"]] + w["rsi5"] + w["zscore5"], dtype=float)


def knn_history(this_week, history, k=5):
    """用"历史向量池"的均值/标准差做标准化，再按欧氏距离挑最近的 k 个历史周。"""
    if not history:
        return [], []
    pool = [v for v in (_week_vector(h) for h in history) if not np.isnan(v).any()]
    if not pool:
        return [], []
    pool = np.array(pool)                      # (n, d)
    mean, std = pool.mean(axis=0), pool.std(axis=0)
    std[std == 0] = 1.0
    target = (_week_vector(this_week) - mean) / std
    if np.isnan(target).any():
        return [], []
    pool_norm = (pool - mean) / std
    dists = np.linalg.norm(pool_norm - target, axis=1)   # (n,)
    order = np.argsort(dists)[:k]
    top = [(history[idx], float(dists[idx])) for idx in order if not np.isnan(dists[idx])]
    if not top:
        return [], []
    return [h for h, _ in top], [d for _, d in top]


# --------------------------------------------------------------------------- #
# 输出量化
# --------------------------------------------------------------------------- #
def quantize_position(p, levels=(0.3, 0.5, 0.7)):
    return min(levels, key=lambda x: abs(x - p))


def resolve_position(prev_position, action, position, quantize=False, levels=(0.3, 0.5, 0.7)):
    """自洽 + 可选离散化，二者协调：先满足自洽，再在网格上取合法点。"""
    p = reconcile_position(prev_position, action, position)
    if not quantize:
        return p
    grid = list(levels)
    valid = [x for x in grid if
             (action in RAISE_ACTIONS and x > prev_position) or
             (action in LOWER_ACTIONS and x < prev_position) or
             (action not in RAISE_ACTIONS and action not in LOWER_ACTIONS)]
    if not valid:
        # 无法自洽时退化为普通量化
        valid = grid
    # 距连续值 p 最近的合法档位
    return min(valid, key=lambda x: abs(x - p))
RAISE_ACTIONS = {"买入", "加大仓位"}
LOWER_ACTIONS = {"减少仓位", "空仓观望"}


def reconcile_position(prev_position, action, position):
    a = str(action or "").strip()
    p = position
    if a in RAISE_ACTIONS and p <= prev_position:
        p = min(1.0, round(prev_position + 0.10, 2))
    elif a in LOWER_ACTIONS and p >= prev_position:
        p = max(0.0, round(prev_position - 0.10, 2))
    return p


def llm_forecast(record, config, prev_position=0.0):
    api_key, base_url = env("LLM_API_KEY"), env("LLM_BASE_URL")
    model = config.model or env("LLM_MODEL") or "deepseek-v4-flash"
    if not api_key:
        raise RuntimeError("未设置 LLM_API_KEY")
    if not base_url:
        base_url = "https://api.deepseek.com/v1"

    def _has_nan(week):
        return any(np.isnan(v) for v in week["rsi5"] + week["zscore5"] + [week["pnl"], week["atr_pct"]])
    if _has_nan(record["this_week"]):
        raise ValueError("特征含 NaN（预热期未满），该周不调用 LLM")

    # 相似周检索：只把最像的 top-k 历史周给模型
    top_k, dists = knn_history(record["this_week"], record["history"], config.knn_k)

    instruction = {
        "任务": (
            "你是周频趋势研判员。结合给定的【相似历史周】，判断当前市场处于：上涨趋势、下跌趋势，"
            "还是即将反转/正在反转/已经反转；并决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
            "只做多，不做空。研究回测，非投资建议。"
        ),
        "说明": (
            "下方仅列出与当前周特征最相似的 %d 个历史周（按相似度排序）。"
            "每个历史周都带有其下一周的实际结果 next_pnl / next_sharpe——请优先依据这些最相关样本决策，"
            "而不是泛泛而谈。证据不足时保持中等仓位，不要满仓赌单一情形。" % len(top_k)
        ),
        "特征含义": {
            "pnl": "该周涨跌幅", "atr_pct": "该周 5 日 ATR/收盘价 均值",
            "rsi5": "该周每个交易日当天及前 4 天的 5 日 RSI", "zscore5": "该周每个交易日相对 5 日均线的 z-score",
            "next_pnl": "该历史周对应的下一周实际涨跌幅", "next_sharpe": "下一周日收益年化夏普",
        },
        "仓位自洽规则": (
            "position 必须与 action 自洽：『买入』『加大仓位』时 position 必须【大于】当前仓位 prev_position；"
            "『减少仓位』『空仓观望』时 position 必须【小于】prev_position。"
        ),
        "prev_position": prev_position,
        "当前周": {k: record["this_week"][k] for k in ["date", "pnl", "atr_pct", "rsi5", "zscore5"]},
        "相似历史周（共 %d 个）" % len(top_k): [dict(h) for h in top_k],
        "输出格式": {
            "trend": "上涨趋势|下跌趋势|反转酝酿|反转进行中|反转已确立",
            "action": "买入|加大仓位|减少仓位|空仓观望",
            "position": "下周目标仓位，浮点数 [0,1]，与 action 自洽（参考 prev_position）",
            "confidence": "0-1",
            "reason": "一句话理由（应引用最相似的 1~2 个历史周）",
        },
    }

    payload = {"model": model, "stream": False, "max_tokens": 16000,
               "reasoning_effort": "max",
               "messages": [{"role": "system", "content": "只输出 JSON。"},
                            {"role": "user", "content": json.dumps(instruction, ensure_ascii=False)}]}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
          "Authorization": "Bearer " + api_key, "User-Agent": "Mozilla/5.0"}, method="POST")
    last_error, text = None, None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                text = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
            last_error = None
            break
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_error = e
    if last_error is not None:
        raise RuntimeError("LLM 请求失败：%s" % last_error) from last_error

    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b < a:
        raise ValueError("LLM 未返回 JSON。")
    parsed = json.loads(text[a:b + 1])
    action = str(parsed.get("action", "")).strip()
    position = min(1.0, max(0.0, float(parsed.get("position", 0.5))))
    position = resolve_position(prev_position, action, position,
                                quantize=config.quantize, levels=config.quant_levels)
    return {"trend": str(parsed.get("trend", "")), "action": action, "position": position,
            "confidence": float(parsed.get("confidence", 0.0)), "reason": str(parsed.get("reason", "")),
            "knn_distances": dists, "raw": text}


def forecast_cached(record, config, out, prev_position=0.0):
    out.mkdir(parents=True, exist_ok=True)
    tag = "knn%d%s" % (config.knn_k, "q" if config.quantize else "")
    cache_path = out / ("llm-%s-%s-%s.json" % (tag, str(record["date"].date()), config.model or env("LLM_MODEL")))
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        cached["position"] = resolve_position(prev_position, cached.get("action", ""), cached["position"],
                                              quantize=config.quantize, levels=config.quant_levels)
        return cached, True
    forecast = llm_forecast(record, config, prev_position)
    cache_path.write_text(json.dumps(forecast, ensure_ascii=False, indent=2), encoding="utf-8")
    return forecast, False


# --------------------------------------------------------------------------- #
# Backtest / evaluation
# --------------------------------------------------------------------------- #
def run_backtest(records, positions, cost_bps=5.0):
    eq = peak = 1.0
    rows = []
    for rec, pos in zip(records, positions):
        gross = pos * rec["next_week_return"]
        cost = abs(pos) * cost_bps / 10000.0
        net = gross - cost
        eq *= 1.0 + net
        peak = max(peak, eq)
        rows.append({"date": rec["date"], "position": pos, "next_week_return": rec["next_week_return"],
                     "gross_return": gross, "net_return": net, "equity": eq, "drawdown": eq / peak - 1.0})
    return pd.DataFrame(rows).set_index("date")


def metrics(df):
    ret = df["net_return"]; eq = df["equity"]
    years = len(ret) / WEEKS_PER_YEAR
    dd = eq / eq.cummax() - 1
    tilt = df["position"] - 0.5
    clear = (tilt.abs() >= 0.25) & (df["next_week_return"] != 0)
    hit = float((np.sign(tilt[clear]) == np.sign(df["next_week_return"][clear])).mean()) if clear.any() else float("nan")
    return {"total_return": float(eq.iloc[-1] - 1), "cagr": float(eq.iloc[-1] ** (1 / years) - 1),
            "annual_vol": float(ret.std(ddof=0) * np.sqrt(WEEKS_PER_YEAR)),
            "sharpe": float(ret.mean() / ret.std(ddof=0) * np.sqrt(WEEKS_PER_YEAR)) if ret.std() else 0.0,
            "max_drawdown": float(dd.min()), "hit_rate": hit, "clear_weeks": int(clear.sum()),
            "avg_position": float(df["position"].mean()),
            "corr": float(df["position"].corr(df["next_week_return"])), "weeks": int(len(ret))}


def build_records(feats, config):
    candidates = feats.index[feats.index.weekday == config.rebalance_weekday]
    closes = feats["close"].reindex(candidates).dropna()
    records = []
    for k in range(config.weeks_history, len(closes) - 1):
        history = []
        if k >= config.history_weeks:
            for i in range(k - config.history_weeks, k):
                entry = _week_features(feats, closes, i)
                entry.update(_next_week_outcome(feats, closes, i))
                history.append(entry)
        records.append({"date": closes.index[k], "close": float(closes.iloc[k]),
                        "this_week": _week_features(feats, closes, k), "history": history,
                        "next_week_return": float(closes.iloc[k + 1] / closes.iloc[k] - 1.0)})
    return records


def main():
    parser = argparse.ArgumentParser(description="weekly-llm-knn: 相似周 top-k + 输出离散化 对照实验（中证1000）")
    parser.add_argument("--weekday", type=int, default=0, choices=[0, 1, 2, 3, 4])
    parser.add_argument("--k", type=int, default=5, help="相似周 top-k")
    parser.add_argument("--quantize", action="store_true", help="输出离散化到 {0.3,0.5,0.7}")
    parser.add_argument("--max-weeks", type=int, default=None)
    parser.add_argument("--out", type=Path, default=Path("output"))
    args = parser.parse_args()

    load_env()
    config = Config(rebalance_weekday=args.weekday, knn_k=args.k, quantize=args.quantize,
                    max_weeks=args.max_weeks, model=env("LLM_MODEL"))
    cache = Path(args.out) / "data" / (config.symbol.replace(".", "_") + ".parquet")
    data = fetch_index(config.symbol, config.start, None, cache_path=cache)
    records = build_records(make_features(data, config), config)
    if config.max_weeks:
        records = records[-config.max_weeks:]
    print("周频样本数：%d  knn_k=%d  quantize=%s  model=%s" % (len(records), config.knn_k, config.quantize, config.model))

    bh = run_backtest(records, [1.0] * len(records), config.cost_bps)
    mom = run_backtest(records, [1.0 if r["this_week"]["pnl"] > 0 else 0.0 for r in records], config.cost_bps)

    llm_positions, llm_dir, llm_failures, prev = [], Path(args.out) / "llm_cache", 0, 0.0
    for rec in records:
        try:
            fc, _ = forecast_cached(rec, config, llm_dir, prev)
            prev = fc["position"]
            llm_positions.append(fc["position"])
        except Exception as error:
            llm_failures += 1
            prev = 0.0
            llm_positions.append(0.0)
            print("  第 %s 周 LLM 失败，改用空仓：%s" % (rec["date"].date(), error))
    print("LLM 失败周数：%d / %d" % (llm_failures, len(records)))
    llm = run_backtest(records, llm_positions, config.cost_bps)

    for name, bt in [("买入持有", bh), ("动量规则", mom), ("LLM 趋势研判", llm)]:
        m = metrics(bt)
        print("%s: tot=%.1f%% cagr=%.1f%% vol=%.1f%% sharpe=%.2f maxdd=%.1f%% corr=%.3f avgpos=%.2f weeks=%d"
              % (name, m["total_return"] * 100, m["cagr"] * 100, m["annual_vol"] * 100, m["sharpe"],
                 m["max_drawdown"] * 100, m["corr"], m["avg_position"], m["weeks"]))
    print("输出目录：%s" % args.out.resolve())


if __name__ == "__main__":
    raise SystemExit(main())