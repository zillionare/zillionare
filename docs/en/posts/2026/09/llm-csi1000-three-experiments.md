---
title: "Can LLMs Trade? Three Experiments on Principles"
date: 2026-09-14
slug: en/posts/factor-strategy/llm-csi1000-three-experiments
tags: [LLM Trading, Factor Investing, Risk Management, Quantitative Investing]
excerpt: "LLM trading fails at alpha but excels at risk control. Three experiments on CSI 1000 reveal that while LLMs lack directional edge, their attention mechanisms effectively manage volatility and drawdowns through position sizing."
lang: en
translation_of: posts/factor-strategy/llm-csi1000-three-experiments
auto_translated: true
source_sha: 71e99f204e0f4fa3f419c9360478f85cb5948d15
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260920142100-llm-csi1000-three-experiments.jpg"
---

Can Agents trade? At the end of last year, nof1.ai conducted an experiment, broadcasting it live on the internet. Much like the crayfish craze, it caused a huge sensation. However, today that live-streaming website is as quiet as a deserted saddle.

Part of the reason is that the best-performing Agent in the trade achieved a Sharpe ratio of only 0.019, which is worse than China A-share retail investors. In this round, the Agent was completely defeated.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260915111717.png)

However, nine months have passed. These nine months represent the most rapid period of artificial intelligence development in history. What will the situation be like nine months later?

This article introduces three experiments. These experiments aim not only to verify whether Agents have trading capabilities but also to mine the principles behind Agent trading and explore ways to improve them.

## /01 Predicting Positions Only

The first experiment is constructed as follows:

The program first constructs three types of features using closing prices: 20-day trend, 20-day realized volatility, and the Z-score of price relative to the 20-day moving average (deviation rate). These are then translated into natural language states (discretized), for example:

`Trend Up | Volatility High | Price Strong`

Trend and volatility each have two states. The deviation rate calculates strength/weakness into three tiers based on the following formula:

$$
zscore_{20} = (close-mean_{20})/std_{20}
$$

When $zscore_{20}$ is greater than or equal to 0.75, the price is considered strong; when less than or equal to -0.75, the price is considered weak; all other states are classified as neutral. Thus, the three feature types constitute a total of 12 states.

During backtesting, at the beginning of each month, we re-statulate the past three years of history: how many times each state has appeared, the mean daily return following that state, and the risk-adjusted score.

The input provided to the LLM is as follows:

```json
{
  "任务": "你是研究回测里的仓位风控助手。不要预测涨跌，不要给投资建议。",
  "要求": "按样本数、下一日平均收益、风险调整得分，为每个状态选择满仓、半仓或低仓；证据不足选半仓；仅返回 JSON。",
  "格式": {"policy": {"状态名": "满仓|半仓|低仓"}},
  "状态统计": "rows"
}
```

Where `rows` are similar to:

```json
[
  {"state": "趋势上行|波动偏低|价格偏强", "count": 142, "mean_next_return": 0.0008, "sharpe_like": 0.31},
  {"state": "趋势下行|波动偏高|价格偏弱", "count": 118, "mean_next_return": -0.0012, "sharpe_like": -0.42},
  {"state": "趋势上行|波动偏高|价格中性", "count": 18, "mean_next_return": 0.002, "sharpe_like": 0.5}
]
```

The LLM will output the following conclusion:

```json
{"policy": {
  "趋势上行|波动偏低|价格偏强": "满仓",
  "趋势下行|波动偏高|价格偏弱": "低仓",
  "趋势上行|波动偏高|价格中性": "半仓"
}}
```

Then, the program translates the position into trading instructions to execute the backtest.

<!--PAID CONTENT START-->

The three experiments have different methods, but they share some common approaches. To avoid excessive length, we extract the common code as follows:

```python
# 公共基础：环境、数据、特征、回测引擎、三个指标（年化收益/Sharpe/Sortino，rf=0）
import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

TRADING_DAYS = 252
WEEKS_PER_YEAR = 52
TMP = Path("/tmp/llm")
TMP.mkdir(parents=True, exist_ok=True)


def load_env_here():
    # 从仓库根目录的 .env 读取 tushare_token、LLM_MODEL、LLM_BASE_URL、LLM_API_KEY
    here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd()
    for parent in (here, *here.parents):
        candidate = parent / ".env"
        if candidate.exists():
            if load_dotenv is not None:
                load_dotenv(candidate)
            break


def env(name, default=""):
    return os.getenv(name, default)


@dataclass
class Cfg:
    symbol: str = "000852.SH"
    cost_bps: float = 5.0


def fetch_index(symbol="000852.SH", start="20160101", cache_name="csi1000.parquet"):
    """tushare 日线 → /tmp/llm，供三个实验共享。"""
    import tushare as ts

    cache = TMP / cache_name
    if cache.exists():
        frame = pd.read_parquet(cache)
        frame.index = pd.to_datetime(frame.index)
        return frame
    token = env("tushare_token")
    if not token:
        raise RuntimeError("请在 .env 中设置 tushare_token。")
    raw = ts.pro_api(token).index_daily(ts_code=symbol, start_date=start,
                                        end_date=pd.Timestamp.today().strftime("%Y%m%d"))
    if raw is None or raw.empty:
        raise RuntimeError("Tushare 没有返回数据。")
    frame = raw.rename(columns={"trade_date": "date"}).copy()
    frame["date"] = pd.to_datetime(frame["date"].astype(str).str.strip(),
                                   format="%Y%m%d", errors="coerce")
    for col in ["open", "high", "low", "close", "pre_close"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=["date", "close"]).set_index("date").sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    frame.to_parquet(cache)
    return frame


def true_range(high, low, prev_close):
    prev = prev_close.shift(1).fillna(prev_close)
    return pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)


def atr(high, low, prev_close, period=14):
    return true_range(high, low, prev_close).ewm(alpha=1.0 / period, min_periods=period).mean()


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


def run_backtest(records, positions, cost_bps=5.0):
    """统一回测引擎：records 提供 date 与 next_week_return/ret；positions 为目标仓位。"""
    equity, peak, prev, rows = 1.0, 1.0, 0.0, []
    for rec, pos in zip(records, positions):
        ret_next = float(rec["next_ret"])
        gross = pos * ret_next
        turnover = abs(pos - prev)
        net = gross - turnover * cost_bps / 10000.0
        equity *= 1.0 + net
        peak = max(peak, equity)
        rows.append({"date": rec["date"], "position": pos, "next_ret": ret_next,
                     "net_return": net, "equity": equity,
                     "drawdown": equity / peak - 1.0, "turnover": turnover})
        prev = pos
    return pd.DataFrame(rows).set_index("date")


def ann_metrics(equity, net_ret, periods_per_year):
    """年化收益 / Sharpe / Sortino，统一口径：无风险利率 rf=0。"""
    eq, r = np.asarray(equity, dtype=float), np.asarray(net_ret, dtype=float)
    total = float(eq[-1] - 1.0)
    ann_ret = float(eq[-1] ** (periods_per_year / len(r)) - 1.0) if len(r) else 0.0
    sd = float(r.std(ddof=0))
    sharpe = float(r.mean() / sd * np.sqrt(periods_per_year)) if sd > 0 else 0.0
    dd = np.sqrt(np.mean(np.minimum(0.0, r) ** 2))
    sortino = float(r.mean() / dd * np.sqrt(periods_per_year)) if dd > 0 else 0.0
    dd_curve = eq / np.maximum.accumulate(eq) - 1.0
    return {"total": total, "ann": ann_ret, "sharpe": sharpe, "sortino": sortino,
            "maxdd": float(dd_curve.min()), "n": int(len(r))}


def llm_chat(instruction, model, max_tokens=8000, timeout=120):
    """统一 LLM 调用：OpenAI 兼容 chat/completions，失败重试 3 次。"""
    api_key, base_url = env("LLM_API_KEY"), env("LLM_BASE_URL")
    if not api_key:
        raise RuntimeError("未设置 LLM_API_KEY")
    if not base_url:
        base_url = "https://api.deepseek.com/v1"
    body = json.dumps({"model": model, "stream": False, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": "只输出 JSON。"},
                                    {"role": "user",
                                     "content": json.dumps(instruction, ensure_ascii=False)}]},
                      ensure_ascii=False).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    request = urllib.request.Request(
        endpoint, data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key,
                 "User-Agent": "Mozilla/5.0"}, method="POST")
    last_error, text = None, None
    for _ in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                text = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
            last_error = None
            break
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = error
    if last_error is not None:
        raise RuntimeError("LLM 请求失败：%s" % last_error) from last_error
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM 没有返回 JSON。")
    return json.loads(text[start:end + 1])
```

<!--PAID CONTENT END-->

<!--PAID CONTENT START-->

Below is the implementation plan for Experiment 1:

```python
# 实验一特有：三类特征 → 12 种市场状态 → 月度滚动统计 → 三档仓位
def exp1_features(prices):
    f = prices.copy()
    f["ret"] = f.close.pct_change()
    f["trend_20"] = f.close.pct_change(20)
    f["vol_20"] = f.ret.rolling(20).std() * np.sqrt(TRADING_DAYS)
    f["vol_median"] = f.vol_20.rolling(252, min_periods=126).median()
    mean_20 = f.close.rolling(20).mean()
    std_20 = f.close.rolling(20).std().replace(0, np.nan)
    f["zscore_20"] = (f.close - mean_20) / std_20
    trend = pd.Series(np.where(f.trend_20 >= 0, "趋势上行", "趋势下行"), index=f.index)
    vol = pd.Series(np.where(f.vol_20 > f.vol_median, "波动偏高", "波动偏低"), index=f.index)
    dist = pd.Series(np.select([f.zscore_20 >= 0.75, f.zscore_20 <= -0.75],
                               ["价格偏强", "价格偏弱"], default="价格中性"), index=f.index)
    f["state"] = trend.str.cat(vol, sep="|").str.cat(dist, sep="|")
    f.loc[f[["trend_20", "vol_20", "vol_median", "zscore_20"]].isna().any(axis=1), "state"] = np.nan
    f["next_ret"] = f.ret.shift(-1)
    return f


def exp1_state_stats(train):
    # 月初用过去 3 年样本外统计：每种状态的样本数、次日均值、风险调整得分
    usable = train.dropna(subset=["state", "next_ret"])
    rows = []
    for name, ret in usable.groupby("state").next_ret:
        count = int(ret.count())
        mean = float(ret.mean())
        std = float(ret.std(ddof=1)) if count > 1 else 0.0
        rows.append({"state": name, "count": count, "mean_next_return": mean,
                     "sharpe_like": mean / std * np.sqrt(TRADING_DAYS) if std else 0.0})
    return sorted(rows, key=lambda item: item["state"])


def exp1_rule(rows):
    # 规则基准：样本不足半仓；均值与风险调整都好满仓；都弱低仓
    policy = {}
    for row in rows:
        if row["count"] < 30:
            policy[row["state"]] = 0.75
        elif row["mean_next_return"] > 0 and row["sharpe_like"] >= 0.25:
            policy[row["state"]] = 1.0
        elif row["mean_next_return"] < 0 and row["sharpe_like"] <= -0.25:
            policy[row["state"]] = 0.50
        else:
            policy[row["state"]] = 0.75
    return policy


MAP = {"满仓": 1.0, "半仓": 0.75, "低仓": 0.50}


def exp1_llm_policy(rows, model):
    # LLM 读同一张状态统计表，输出满/半/低三档；失败由调用方退回规则
    instruction = {
        "任务": "你是研究回测里的仓位风控助手。不要预测涨跌，不要给投资建议。",
        "要求": "按样本数、下一日平均收益、风险调整指标为每个状态选择满仓、半仓或低仓；证据不足选半仓；仅返回 JSON。",
        "格式": {"policy": {"状态名": "满仓|半仓|低仓"}},
        "状态统计": rows,
    }
    supplied = llm_chat(instruction, model).get("policy", {})
    return {row["state"]: MAP.get(str(supplied.get(row["state"], "半仓")), 0.75) for row in rows}
```

<!--PAID CONTENT END-->

### Results of Experiment 1

Out-of-sample period 2019-01-02 → 2026-08-28 (Rules/LLM parallel daily settlement for 1,855 trading days; LLM made 92 decision months; all re-runs this time were successful, 0 rollback months):


| Strategy             | Total Return | Annualized Return | Annualized Volatility | Sharpe | Sortino | Max Drawdown |
| ---------------- | ------ | -------- | -------- | ------ | ------- | -------- |
| Buy & Hold (Peer) | +76.0% | +8.0%    | 25.0%    | 0.43   | 0.60    | -46.7%   |
| Rule Benchmark         | +0.4%  | +0.1%    | 9.3%     | 0.05   | 0.07    | -26.3%   |
| LLM Risk Control         | +0.4%  | +0.1%    | 9.3%     | 0.05   | 0.07    | -26.3%   |

**Conclusion**: The LLM halved volatility (25%→9.3%) and drawdown (-46.7%→-26.3%)—it is a qualified "risk modulator"; but in the 2019–2026 bull market window, it significantly underperformed Buy & Hold, and almost coincided with the rule benchmark (in 92 months, the LLM's choices were identical to the rules daily). This indicates that this statistical table contains no directional alpha.

![Experiment 1 Rule NAV vs Peer Buy & Hold, Experiment 2 Monday Momentum NAV, Experiment 3 Thursday KNN5+Q NAV](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-curves.png)

![KNN5+Q Thursday vs Experiment 1 Rule Drawdown Comparison](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-drawdowns.png)

This is basically the situation we saw on nof1.ai.

## /02 Label History + Trend Judgment

The characteristic of Experiment 1 is that it relies entirely on past statistical features, "stripping" recent trends: it does not know "what current segment resembles historically," nor "what happened after such a situation." This causes it to mechanically reduce positions even if the market improves after a long bear market, provided the statistical features have not yet reversed, leading to significant underperformance against Buy & Hold.

Statistical features are essentially compressed information. During compression, it loses trend information. Even if the LLM can understand trends, it does not receive this information as input. Therefore, we make the following improvement: instead of statistics, we feed raw data directly to the AI:

1. Each decision is accompanied by a 48-week "feature + next week's actual result" labeled history table, allowing the LLM to perform historical analogy.
2. Shorten the rebalancing cycle so the LLM can respond more flexibly to trend changes. We change rebalancing to weekly frequency; the task shifts from "selecting position tiers" to "trend/reversal judgment + action + position."

Now, the input provided to the LLM becomes:

```json
instruction = {
    "任务": ("你是周频趋势研判员。结合历史样本，判断当前市场处于：上涨趋势、下跌趋势、"
            "还是即将反转/正在反转/已经反转；并决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
            "只做多，不做空。"),
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
        "position 必须与 action 自洽：action 为『买入』或『加大仓位』时，新的 position 必须【大于】"
        "当前已有仓位 prev_position；action 为『减少仓位』或『空仓观望』时必须【小于】prev_position。"
        "系统会据此校正你的输出。"
    ),
    "prev_position": prev_position,
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
```

It can be seen that the input features have changed:

1. We provide weekly PnL—each prediction is accompanied by a maximum of 48 weeks of history. Trend information is included, depending on whether the LLM can extract it.
2. The deviation rate is still provided. However, we now use $zscore_5$—the deviation rate for a 5-day window.
3. Volatility is provided in the form of ATR (Average True Range) and in percentage terms.
4. A reversal indicator, $rsi_5$, is provided.

In addition to features, we also provide reference prediction values: $next\_pnl$ and $next\_sharpe$, to see if the LLM can correlate features with future trends and find patterns.

<!--PAID CONTENT START-->

Below is the code for Experiment 2:

```python
# 实验二特有：周特征快照 + 48 周带标签历史 + 趋势研判 + 自洽仓位
def exp2_rsi(close, period=5, warmup=60):
    delta = close.diff()
    avg_gain = delta.clip(lower=0.0).ewm(alpha=1.0 / period, min_periods=period).mean()
    avg_loss = (-delta.clip(upper=0.0)).ewm(alpha=1.0 / period, min_periods=period).mean()
    out = 100 - 100 / (1 + avg_gain / avg_loss.replace(0, np.nan))
    out = out.fillna(50.0)
    out.iloc[:warmup - 1] = np.nan  # 前 59 个结果丢弃
    return out


def exp2_make_features(data):
    f = data.copy()
    f["atr"] = atr(f.high, f.low, f.pre_close, 14)
    f["atr_pct"] = f["atr"] / f["close"]
    f["rsi5"] = exp2_rsi(f["close"])
    f["z5"] = zscore(f["close"], 5)
    return f


def exp2_week_features(feats, closes, i):
    # 第 i 个调仓周（5 个交易日，含调仓日当天）+ 其下一周真实结果标签
    date = closes.index[i]
    window = feats.loc[:date].tail(5)
    d0, d1 = closes.index[i], closes.index[i + 1]
    daily_rets = feats["close"].pct_change().loc[(feats.index > d0) & (feats.index <= d1)]
    std = float(daily_rets.std(ddof=1)) if len(daily_rets) > 1 else 0.0
    return {
        "date": str(date.date()),
        "pnl": float(closes.iloc[i] / closes.iloc[i - 1] - 1.0),
        "atr_pct": float(window["atr_pct"].astype(float).mean()),
        "rsi5": [float(x) for x in window["rsi5"]],
        "zscore5": [float(x) for x in window["z5"]],
        "next_pnl": float(closes.iloc[i + 1] / closes.iloc[i] - 1.0),
        "next_sharpe": float(daily_rets.mean() / std * np.sqrt(TRADING_DAYS)) if std else 0.0,
    }


def exp2_build_records(feats, weekday):
    # 每条记录 = 本周快照 + 过去 48 周带标签历史 + 下周真实收益（结算用）
    closes = feats["close"].reindex(feats.index[feats.index.weekday == weekday]).dropna()
    records = []
    for k in range(4, len(closes) - 1):
        history = [exp2_week_features(feats, closes, i) for i in range(max(4, k - 48), k)] \
            if k >= 48 else []
        # 与历史实验一致：历史不足 48 周的早期记录仍保留（history 为空）
        this_week = exp2_week_features(feats, closes, k)
        records.append({"date": closes.index[k], "this_week": this_week, "history": history,
                        "next_ret": float(closes.iloc[k + 1] / closes.iloc[k] - 1.0)})
    return records


RAISE_ACTIONS = {"买入", "加大仓位"}
LOWER_ACTIONS = {"减少仓位", "空仓观望"}


def exp2_reconcile(prev_position, action, position):
    # 强制 action 与 position 自洽：买入/加仓须高于上周仓，减仓/空仓须低于上周仓
    a = str(action or "").strip()
    if a in RAISE_ACTIONS and position <= prev_position:
        return min(1.0, round(prev_position + 0.10, 2))
    if a in LOWER_ACTIONS and position >= prev_position:
        return max(0.0, round(prev_position - 0.10, 2))
    return position


def exp2_llm_forecast(record, model, prev_position=0.0):
    def _has_nan(week):
        return any(np.isnan(v) for v in week["rsi5"] + week["zscore5"]
                   + [week["pnl"], week["atr_pct"]])

    if _has_nan(record["this_week"]):
        raise ValueError("特征含 NaN（预热期未满），该周不调用 LLM")
    instruction = {
        "任务": ("你是周频趋势研判员。结合历史样本，判断当前市场处于：上涨趋势、下跌趋势、"
                "还是即将反转/正在反转/已经反转；并决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
                "只做多，不做空。研究回测，非投资建议。"),
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
            "position 必须与 action 自洽：action 为『买入』或『加大仓位』时，新的 position 必须【大于】"
            "当前已有仓位 prev_position；action 为『减少仓位』或『空仓观望』时必须【小于】prev_position。"
            "系统会据此校正你的输出。"
        ),
        "prev_position": prev_position,
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
    parsed = llm_chat(instruction, model)
    action = str(parsed.get("action", "")).strip()
    position = min(1.0, max(0.0, float(parsed.get("position", 0.5))))
    position = exp2_reconcile(prev_position, action, position)
    return {"trend": str(parsed.get("trend", "")), "action": action, "position": position,
            "confidence": float(parsed.get("confidence", 0.0)),
            "reason": str(parsed.get("reason", ""))}
```

<!--PAID CONTENT END-->

The backtest proceeds as follows:

1. Take a snapshot during the rebalancing week (including this week's 5-day RSI/z-score sequence).
2. Each of the past 48 weeks includes its actual result for the following week.
3. LLM outputs trend + action + position (self-consistent correction) → failure degrades to empty position → settlement the next week.

Evaluation takes the **last 100 weeks** (2024-08 → 2026-08, five rebalancing days each window), with Buy & Hold/Momentum taking the same peer window.

Below are the results of Experiment 2 (re-run completely on 2026-09-16 using `deepseek-v4-flash`, taking the last 100 weeks for each of the five rebalancing days from Monday to Friday; LLM uniformly uses v2 self-consistent prompts, with failure weeks degraded to empty positions included):

![Experiment 2 Results: Buy & Hold vs Momentum Rule vs LLM Same-Peer Same-Day Comparison, Total Return, Annualized Volatility, Sharpe, Sortino, Max Drawdown Five-Panel Grouped Bar Chart](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-exp2-bars.png)

Compared to Experiment 1, Experiment 2's performance improved significantly. From the Sharpe distribution chart, it can be seen that on almost every rebalancing day, **the LLM achieved a better Sharpe ratio**. By observing the total return and max drawdown charts, we can conclude that the improvement in Sharpe was mainly achieved by reducing volatility and drawdown risks.

The reasons for the significant improvement are mainly:

1. Shorter rebalancing cycle, responding to trend changes more timely.
2. Providing the LLM with more raw information (labeled history), allowing it to perform its own time-series analogy.
3. Adding more reversal features.

However, can we further improve data performance? Obviously, we can add more features. In Experiment 2, we only used **two** reversal features: deviation rate and RSI value. In fact, there are indeed some very effective **short-term top/bottom features** we did not include.

Considering that short-term features are controversial in academia (mostly from practitioners), in this experiment, I decided not to include these empirical rules. So how to improve?

I threw this question to the LLM.

!!! quote
    Please analyze the first two experiments and help me design Experiment 3 to improve the LLM's trading performance.

The LLM provided the following analysis:

!!! quote
    Diagnosis of three weaknesses in Experiment 2 (all visible from the first 500 lines of code):

   - Information is too scattered: 48 weeks of labeled history are stuffed into the prompt all at once, and the model must "find similarities" within 48 records—this is exactly the problem solved by statistical tables in Experiment 1 and abandoned in Experiment 2. Attention is diluted, and truly relevant historical weeks (e.g., those same weeks with "RSI low rebound + Z turning positive") are drowned in the long list.
   - Output is too conservative: `position` is a continuous value in [0,1], with model means of 0.38~0.46 below the neutral line—but this is merely "conservative" rather than "avoiding extremes": in practice, 42%~58% of positions fall outside [0.4,0.6], and five rebalancing days have all seen 0.00 full empty positions, with maximums reaching 0.80~0.90. The model dares to express opinions, but on average, dares not hold heavy positions.
   - Execution is too soft: Although actions and positions have self-consistent correction, vague expressions like "increase position" +0.10 have their contribution to returns diluted.
     The analysis provided by the LLM is interesting: the first point is an improvement suggestion on how to analyze time-series data and discover patterns; the second is an insight into the LLM's own operating mechanism. Beginners using LLMs for trading must pay close attention to the second type of issue.

Man proposes, God disposes. **LLMs can propose suggestions, but humans make decisions.** We are the gods of LLMs. How is the quality of the LLM's suggestions? We test this through Experiment 3.

## /03 Similar Week Retrieval + Output Discretization

Based on the LLM's suggestions, we make the following changes to Experiment 2:

1. Euclidean distance (standardized by historical vector pool) selects only the top-k most similar historical weeks, focusing attention;
2. Position is forced to discretize into three tiers `{0.3, 0.5, 0.7}`, forcing the LLM to express itself clearly. A/B switch: `knn5` / `knn5+quantize` / `knn48+quantize`, where `knn48+quantize` approximates full-history comparison.

<!--PAID CONTENT START-->

Below is the code for Experiment 3:

```python
# 实验三特有：相似周 top-k 检索 + 输出离散化（其余复用实验二：特征、回测、指标）
def knn_week_vector(w):
    return np.array([w["pnl"], w["atr_pct"]] + w["rsi5"] + w["zscore5"], dtype=float)


def knn_history(this_week, history, k=5):
    # 用"历史向量池"的均值/标准差做标准化，再按欧氏距离挑最近的 k 个历史周
    if not history:
        return [], []
    pool = [v for v in (knn_week_vector(h) for h in history) if not np.isnan(v).any()]
    if not pool:
        return [], []
    pool = np.array(pool)
    mean, std = pool.mean(axis=0), pool.std(axis=0)
    std[std == 0] = 1.0
    target = (knn_week_vector(this_week) - mean) / std
    if np.isnan(target).any():
        return [], []
    dists = np.linalg.norm((pool - mean) / std - target, axis=1)
    order = np.argsort(dists)[:k]
    top = [(history[idx], float(dists[idx])) for idx in order if not np.isnan(dists[idx])]
    if not top:
        return [], []
    return [h for h, _ in top], [d for _, d in top]


def quantize_position(p, levels=(0.3, 0.5, 0.7)):
    return min(levels, key=lambda x: abs(x - p))


def knn_resolve_position(prev_position, action, position, quantize=False, levels=(0.3, 0.5, 0.7)):
    # 自洽 + 可选离散化：先满足自洽，再在网格上取合法点
    p = exp2_reconcile(prev_position, action, position)
    if not quantize:
        return p
    grid = list(levels)
    valid = [x for x in grid if
             (action in {"买入", "加大仓位"} and x > prev_position) or
             (action in {"减少仓位", "空仓观望"} and x < prev_position) or
             (action not in {"买入", "加大仓位", "减少仓位", "空仓观望"})]
    if not valid:
        valid = grid
    return min(valid, key=lambda x: abs(x - p))


def knn_llm_forecast(record, model, prev_position=0.0, knn_k=5, quantize=False):
    # 与实验二同一提示词骨架；唯一差别：历史样本换成 top-k 相似周
    def _has_nan(week):
        return any(np.isnan(v) for v in week["rsi5"] + week["zscore5"]
                   + [week["pnl"], week["atr_pct"]])

    if _has_nan(record["this_week"]):
        raise ValueError("特征含 NaN（预热期未满），该周不调用 LLM")
    top_k, dists = knn_history(record["this_week"], record["history"], knn_k)
    instruction = {
        "任务": ("你是周频趋势研判员。结合给定的【相似历史周】，判断当前市场处于：上涨趋势、下跌趋势，"
                "还是即将反转/正在反转/已经反转；并决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
                "只做多，不做空。研究回测，非投资建议。"),
        "说明": ("下方仅列出与当前周特征最相似的 %d 个历史周。每个都带下一周实际结果 next_pnl/next_sharpe；"
                "请优先依据这些最相关样本决策，而不是泛泛而谈。证据不足保持中等仓位。" % len(top_k)),
        "特征含义": {
            "pnl": "该周涨跌幅", "atr_pct": "该周 5 日 ATR/收盘价 均值",
            "rsi5": "该周每个交易日当天及前 4 天的 5 日 RSI",
            "zscore5": "该周每个交易日相对 5 日均线的 z-score",
            "next_pnl": "该历史周对应的下一周实际涨跌幅",
            "next_sharpe": "下一周日收益年化夏普",
        },
        "仓位自洽规则": ("『买入』『加大仓位』时 position 必须【大于】prev_position；"
                        "『减少仓位』『空仓观望』时 position 必须【小于】prev_position。"),
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
    parsed = llm_chat(instruction, model, max_tokens=16000)
    action = str(parsed.get("action", "")).strip()
    position = min(1.0, max(0.0, float(parsed.get("position", 0.5))))
    position = knn_resolve_position(prev_position, action, position,
                                    quantize=quantize, levels=(0.3, 0.5, 0.7))
    return {"trend": str(parsed.get("trend", "")), "action": action, "position": position,
            "confidence": float(parsed.get("confidence", 0.0)),
            "reason": str(parsed.get("reason", "")), "knn_distances": dists}
```

<!--PAID CONTENT END-->

The running results are as follows:

![Experiment 2 vs Experiment 3 (KNN5+Quantize) Same-Day Comparison: Total Return, Annualized Volatility, Sharpe, Sortino, Max Drawdown Five-Panel Grouped Bar Chart](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-exp2-vs-exp3-bars.png)

![Experiment 3 2x2 Factor Decomposition: Retrieval (Top-5 × Full History 48) × Discretization (Continuous × Quantized) Sharpe Matrix and 5-Day Average](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/exp2-vs-exp3-2x2.png)

The results of the first chart are somewhat surprising. From Monday to Wednesday, Sharpe is better than Experiment 2, but from Thursday to Friday, the results are weaker than Experiment 2. However, considering the absolute value of Sharpe, even if Monday and Tuesday perform better in Experiment 3, we would not adopt them. In this regard, compared to Experiment 2, Experiment 3 actually has 1 win and 2 losses.

Chart 2 is a comparison chart of the results when the two strategies, discretization and similar week retrieval, are used separately. When used separately, both strategies yield negative results (retrieval -0.39) or depend on conditions (quantization -0.18~+0.38), and when used jointly, they cancel each other out.

## /04 Why Can LLMs Trade?

From Experiment 1 to Experiment 2, the LLM achieved better Sharpe ratios when rebalancing on Thursdays and Fridays. Since the backtest only used 100 weeks (i.e., two years) of time, we cannot yet fully say that LLMs are suitable for trading.

However, if this backtest result is credible, how should it be explained?

This may mean that Transformer/Attention can read correlations between time-series data and generate signals.

**① Attention can indeed perform "pattern-result" analogy.** When price/indicator sequences are serialized into labeled history (this week's features + next week's actual result), the LLM's attention mechanism can establish associations between "this week" and "historical weeks": the re-run correlation in Experiment 2 ranges from -0.07 to +0.16 across five rebalancing days (positive for Wed/Thu/Fri, negative for Mon/Tue), and the `reason` field in Experiment 3 frequently cites specific historical weeks ("Most similar historical week 2024-04-15 next week drop -0.78%..."). This is mechanistic evidence of "reading time-series correlations to generate signals," but the strength is limited.

**② Position management is the core value.** In the three experiments, the LLM did not actually improve returns; it improved risk control: volatility was compressed from ~30% to ~10%, and drawdown from -46% to around -10%. The mechanism is "confidence weighting"—increasing positions when evidence is strong, reducing positions when evidence is weak. Even if the directional judgment for a single week is inaccurate, this weighting itself can raise Sharpe and compress drawdown. The LLM's role here is a **risk researcher/budget allocator**, not a price prophet.

## /05 A Discussion on LLM Principles

We have discussed why LLMs can trade. But this is only one side of the coin. If we cannot fully understand the principles and mechanisms of LLMs, it is actually difficult to improve strategies, even if allowing LLMs to self-improve, which Experiment 3 basically proves.

LLMs trading first encounter issues with discontinuous price representation, distorted distance, and unreliable arithmetic. In the experiments, we inputted stock prices, RSI, and next week's price changes. In traditional quantitative trading models, these are very natural input data, which models generally use directly.

However, in LLMs, the model first processes text inputs into tokens, using BPE (Byte Pair Encoding) encoders. Numbers are continuous and infinite, but tokenizers are finite sets. Therefore, in the process of converting input text into tokens, values may be fragmented (e.g., 7.9 might be cut into `7` + `.9`, or `7.` + `9`, or it might be `7.9` as a whole), and distance is lost (even if the vocabulary simultaneously contains three tokens "7.7", "7.8", and "7.9", the pairwise distances between these three tokens are basically unequal; whereas in mathematical language, the distance between 7.7 and 7.8, and 7.8 and 7.9 are equal, and the distance between 7.7 and 7.9 is twice that of other relationships. Tokenization distorts the relationships between numbers).

Therefore, for the LLM to know that 78.1 in the RSI value is larger than 78.0 is much more difficult than we imagine; it requires massive training to produce memory, and then generates the conclusion that 78.1 is larger than 78.0 through pattern completion and reasoning during generation. This is also why LLMs often fail in the following IQ test questions:

!!! quote
    Which is larger, 9.11 or 9.9?

Additionally, LLMs have no temporal inductive bias. "Rise then fall" and "fall then rise" in price sequences are completely different signals, but the model has no built-in direction/causal structure and can only learn from data.

Finally, we must emphasize one point: we choose quantitative trading to reduce randomness and uncertainty compared to subjective trading. However, LLMs are generative models, and their output variance will be brought by sampling temperature during generation. Therefore, trading strategies based on LLMs have unexplainability and instability.

Therefore, although we achieved good returns in Experiment 2, from the perspective of LLM principles, these returns may be accidental. The conclusion obtained in the previous section, that position management is the core value, is likely the most reasonable conclusion after analyzing LLM principles.

However, Experiment 2 does point out a possibility: that Transformer/Attention can discover and apply patterns in longer time series.

How to improve? Chronos may represent a direction.

In input processing, in Chronos, the "tokenization" process changes from BPE to "numerical binning" (scaling + quantization), thereby preserving order and scale. It first standardizes the raw sequence by mean/variance, then uniformly maps continuous values to a fixed number of bins (e.g., 4096 ordered tokens). The bin ID itself is ordered—bin 100 and bin 101 are numerically adjacent, and adjacent at the tokenization level. The distance-preserving property lost by BPE is designed back here.

In the training objective, Chronos does not "predict the next word," but "predict the next bin"—i.e., modeling a discrete probability distribution for future values, naturally outputting quantiles/confidence intervals. LLMs can only give you a point estimate (position=0.55), while Chronos directly gives you "the distribution of next week's returns," which is a more native input for position sizing.

Additionally, Chronos uses causal masked autoregressive training, with the time direction hardcoded into the training objective, thereby solving the 'no temporal inductive bias' issue we mentioned earlier.

Besides Chronos, similar solutions include Moirai proposed by Salesforce. Its advantage is native multi-variable support, capable of simultaneously supporting multi-path factor time-series inputs. Chronos only supports one-factor data, requiring an additional decision layer to stitch multiple factors together in multi-factor scenarios; because channels are conditionally independent, Chronos struggles to learn cross-channel patterns like "volume expansion + price stagnation."

## /06 Reproduction Guide

The code used in this article is available on the Quantide official website. To reproduce the conclusions in this article, you need to be able to use Tushare and LLM large models. During backtesting, this article used the official version of `deepseek-v4-flash`. Using other models may yield different conclusions.
