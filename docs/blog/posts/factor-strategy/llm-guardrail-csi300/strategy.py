#!/usr/bin/env python3
"""Research-only LLM position-risk backtest for mainland-China data users.

It is intentionally long-only and does not connect to a broker.
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


def load_env():
    """Load .env from the repo root (walk up from this file)."""
    if load_dotenv is None:
        return
    here = Path(__file__).resolve()
    for parent in (here.parent, *here.parents):
        candidate = parent / ".env"
        if candidate.exists():
            load_dotenv(candidate)
            break


def env(name, default=""):
    return os.getenv(name, default)


@dataclass
class Config:
    train_years: int = 3
    target_vol: float = 0.18
    cost_bps: float = 5.0
    max_exposure: float = 1.0
    drawdown_limit: float = 0.15
    cooldown_days: int = 5
    max_flat_days: int = 10
    model: str = ""


def first_column(columns, alternatives):
    lookup = {str(item).strip().lower(): item for item in columns}
    return next((lookup[name.lower()] for name in alternatives if name.lower() in lookup), None)


def normalise(raw, date_column, close_column):
    frame = raw[[date_column, close_column]].rename(columns={date_column: "date", close_column: "close"}).copy()
    date_text = frame["date"].astype(str).str.strip()
    parsed = pd.to_datetime(date_text, format="%Y%m%d", errors="coerce")
    frame["date"] = parsed.fillna(pd.to_datetime(date_text, errors="coerce"))
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame = frame.dropna().drop_duplicates("date", keep="last").sort_values("date").set_index("date")
    if len(frame) < 800:
        raise ValueError("有效日线不足 800 条；请提供更长的历史数据。")
    return frame


def read_csv(path):
    raw = pd.read_csv(path)
    date = first_column(raw.columns, ["date", "trade_date", "日期", "交易日期"])
    close = first_column(raw.columns, ["close", "收盘", "收盘价"])
    if date is None or close is None:
        raise ValueError("CSV 需要日期（date/trade_date/日期）和收盘价（close/收盘）列。")
    return normalise(raw, date, close)


def read_tushare_index(symbol, start, end):
    try:
        import tushare as ts
    except ImportError as error:
        raise RuntimeError("请执行 pip install tushare，或改用 --csv。") from error
    token = env("tushare_token")
    if not token:
        raise RuntimeError("请在 .env 中设置 tushare_token，或改用 --csv。")
    raw = ts.pro_api(token).index_daily(
        ts_code=symbol,
        start_date=start,
        end_date=end or pd.Timestamp.today().strftime("%Y%m%d"),
    )
    if raw is None or raw.empty:
        raise RuntimeError("Tushare 没有返回数据；请检查 Token、积分权限、代码和网络。")
    return normalise(raw, "trade_date", "close")


def make_features(prices):
    frame = prices.copy()
    frame["ret"] = frame.close.pct_change()
    frame["trend_20"] = frame.close.pct_change(20)
    frame["momentum_63"] = frame.close.pct_change(63)
    frame["vol_20"] = frame.ret.rolling(20).std() * np.sqrt(TRADING_DAYS)
    frame["vol_median"] = frame.vol_20.rolling(252, min_periods=126).median()
    mean_20 = frame.close.rolling(20).mean()
    std_20 = frame.close.rolling(20).std().replace(0, np.nan)
    frame["zscore_20"] = (frame.close - mean_20) / std_20
    frame["ma_50"] = frame.close.rolling(50).mean()

    trend = pd.Series(np.where(frame.trend_20 >= 0, "趋势上行", "趋势下行"), index=frame.index)
    volatility = pd.Series(np.where(frame.vol_20 > frame.vol_median, "波动偏高", "波动偏低"), index=frame.index)
    distance = pd.Series(np.select([frame.zscore_20 >= 0.75, frame.zscore_20 <= -0.75], ["价格偏强", "价格偏弱"], default="价格中性"), index=frame.index)
    frame["state"] = trend.str.cat(volatility, sep="|").str.cat(distance, sep="|")
    frame.loc[frame[["trend_20", "vol_20", "vol_median", "zscore_20"]].isna().any(axis=1), "state"] = np.nan
    # The state at close t is assessed against return t+1.  There is no same-day signal.
    frame["next_ret"] = frame.ret.shift(-1)
    return frame


def state_stats(train):
    usable = train.dropna(subset=["state", "next_ret"])
    rows = []
    for name, ret in usable.groupby("state").next_ret:
        count = int(ret.count())
        mean = float(ret.mean())
        std = float(ret.std(ddof=1)) if count > 1 else 0.0
        rows.append({"state": name, "count": count, "mean_next_return": mean, "sharpe_like": mean / std * np.sqrt(TRADING_DAYS) if std else 0.0})
    return sorted(rows, key=lambda item: item["state"])


def rule_policy(rows):
    policy = {}
    for row in rows:
        if row["count"] < 30:
            exposure = 0.75
        elif row["mean_next_return"] > 0 and row["sharpe_like"] >= 0.25:
            exposure = 1.0
        elif row["mean_next_return"] < 0 and row["sharpe_like"] <= -0.25:
            exposure = 0.50
        else:
            exposure = 0.75
        policy[row["state"]] = exposure
    return policy


def deepseek_policy(rows, config):
    api_key = env("LLM_API_KEY")
    base_url = env("LLM_BASE_URL")
    model = config.model or env("LLM_MODEL") or "deepseek-chat"
    if not api_key:
        raise RuntimeError("未设置 LLM_API_KEY")
    if not base_url:
        base_url = "https://api.deepseek.com/v1"
    instruction = {
        "任务": "你是研究回测里的仓位风控助手。不要预测涨跌，不要给投资建议。",
        "要求": "按样本数、下一日平均收益、风险调整指标为每个状态选择满仓、半仓或低仓；证据不足选半仓；仅返回 JSON。",
        "格式": {"policy": {"状态名": "满仓|半仓|低仓"}},
        "状态统计": rows,
    }
    body = json.dumps({"model": model, "stream": False, "messages": [{"role": "system", "content": "只输出 JSON。"}, {"role": "user", "content": json.dumps(instruction, ensure_ascii=False)}]}, ensure_ascii=False).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    request = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
            last_error = None
            break
        except urllib.error.URLError as error:
            last_error = error
            continue
    if last_error is not None:
        raise RuntimeError("LLM 请求失败：%s" % last_error) from last_error
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM 没有返回 JSON。")
    supplied = json.loads(text[start:end + 1]).get("policy", {})
    mapping = {"满仓": 1.0, "半仓": 0.75, "低仓": 0.50}
    return {row["state"]: mapping.get(str(supplied.get(row["state"], "半仓")), 0.75) for row in rows}


def policy_for_month(day, train, mode, config, out):
    rows = state_stats(train)
    fallback = rule_policy(rows)
    key = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()[:12]
    cache = out / "policy_cache" / (day.strftime("%Y-%m") + "-" + mode + "-" + key + ".json")
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        cached = json.loads(cache.read_text(encoding="utf-8"))
        return {name: float(value) for name, value in cached["policy"].items()}, cached["source"] + "（缓存）"
    policy, source = fallback, "规则基准"
    if mode == "deepseek":
        try:
            policy, source = deepseek_policy(rows, config), config.model or env("LLM_MODEL") or "LLM"
        except (RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
            source = "LLM 失败，退回规则基准：" + str(error)
    cache.write_text(json.dumps({"as_of": str(day.date()), "source": source, "statistics": rows, "policy": policy}, ensure_ascii=False, indent=2), encoding="utf-8")
    return policy, source


def performance(equity, turnover):
    ret = equity.pct_change().dropna()
    years = len(ret) / TRADING_DAYS
    drawdown = equity / equity.cummax() - 1
    return {"total_return": float(equity.iloc[-1] - 1.0), "cagr": float(equity.iloc[-1] ** (1 / years) - 1.0), "annual_volatility": float(ret.std(ddof=1) * np.sqrt(TRADING_DAYS)), "sharpe_zero_rate": float(ret.mean() / ret.std(ddof=1) * np.sqrt(TRADING_DAYS)) if ret.std(ddof=1) else 0.0, "max_drawdown": float(drawdown.min()), "average_daily_turnover": float(turnover.mean()), "observations": int(len(ret))}


def backtest(frame, config, mode, out):
    first_oos = frame.index.searchsorted(frame.index[0] + pd.DateOffset(years=config.train_years))
    if first_oos >= len(frame) - 20:
        raise ValueError("数据不足以保留训练期和有效样本外区间。")
    equity = peak = 1.0
    previous_position = 0.0
    cooldown = flat_days = 0
    last_month = None
    policy, notes, results = {}, [], []
    for i in range(first_oos, len(frame)):
        day, yesterday, today = frame.index[i], frame.iloc[i - 1], frame.iloc[i]
        month = day.to_period("M")
        if month != last_month:
            # Exclude yesterday: its next-day return (today) was not known at the decision time.
            policy, note = policy_for_month(day, frame.iloc[:max(0, i - 1)], mode, config, out)
            notes.append(day.strftime("%Y-%m") + ": " + note)
            last_month = month
        state = yesterday.state
        base = policy.get(state, 0.75) if isinstance(state, str) else 0.75
        past_vol = float(yesterday.vol_20) if pd.notna(yesterday.vol_20) else config.target_vol
        position = base * min(config.max_exposure, config.target_vol / max(past_vol, 1e-6))
        position *= 1.15 if yesterday.momentum_63 > 0 else 0.85
        position = min(config.max_exposure, max(0.0, position))
        previous_drawdown = equity / peak - 1.0
        trend_broken = yesterday.momentum_63 < 0 and yesterday.close < yesterday.ma_50
        action = "正常"
        if cooldown:
            position, cooldown, flat_days, action = 0.0, cooldown - 1, flat_days + 1, "冷静期"
        elif previous_drawdown <= -config.drawdown_limit and trend_broken and flat_days < config.max_flat_days:
            position, cooldown, flat_days, action = 0.0, config.cooldown_days - 1, flat_days + 1, "回撤硬止损"
        elif previous_drawdown <= -config.drawdown_limit and trend_broken:
            flat_days, action = 0, "强制再入场，防止风控死锁"
        elif previous_drawdown <= -0.60 * config.drawdown_limit:
            position, flat_days, action = position * 0.5, 0, "回撤预警，仓位减半"
        else:
            flat_days = 0
        turnover = abs(position - previous_position)
        cost = turnover * config.cost_bps / 10000.0
        gross = position * float(today.ret)
        net = gross - cost
        equity *= 1.0 + net
        peak = max(peak, equity)
        results.append({"date": day, "close": today.close, "state_used": state, "base_position": base, "position": position, "asset_return": today.ret, "gross_return": gross, "turnover": turnover, "cost": cost, "net_return": net, "equity": equity, "drawdown": equity / peak - 1.0, "risk_action": action})
        previous_position = position
    output = pd.DataFrame(results).set_index("date")
    return output, performance(output.equity, output.turnover), notes


def main():
    parser = argparse.ArgumentParser(description="大陆数据环境下的 LLM 仓位风控研究回测")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--csv", type=Path, help="含日期和收盘价的本地 CSV")
    source.add_argument("--tushare-index", help="指数代码，例如中证1000 000852.SH")
    parser.add_argument("--start", default="20160101")
    parser.add_argument("--end")
    parser.add_argument("--policy", choices=["rule", "deepseek"], default="rule")
    parser.add_argument("--out", type=Path, default=Path("output"))
    parser.add_argument("--train-years", type=int, default=3)
    parser.add_argument("--cost-bps", type=float, default=5.0)
    args = parser.parse_args()
    load_env()
    try:
        prices = read_csv(args.csv) if args.csv else read_tushare_index(args.tushare_index, args.start, args.end)
        config = Config(train_years=args.train_years, cost_bps=args.cost_bps, model=env("LLM_MODEL"))
        args.out.mkdir(parents=True, exist_ok=True)
        result, metrics, notes = backtest(make_features(prices), config, args.policy, args.out)
        result.to_csv(args.out / "daily_results.csv", encoding="utf-8-sig")
        (args.out / "metrics.json").write_text(json.dumps({"config": asdict(config), "policy_mode": args.policy, "metrics": metrics, "policy_notes": notes}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        print("已写入：%s" % args.out.resolve())
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print("运行失败：%s" % error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
