---
title: LLM 能做交易吗？中证 1000 上的三个递进实验
date: 2026-09-14
description: 直播里 LLM 读指标做交易很热闹，但热闹不等于有效。三个递进实验回答：LLM 能做交易吗、有效性在哪一层、为什么。
tags: "[大模型, Agent, 中证1000, 量化交易, 回测, AI量化]"
excerpt: "LLM 真能下单吗？nof1.ai 直播实验夏普仅 0.019，九个月后 AI 突飞猛进，结论会变吗？本文在中证 1000 上设计三个递进实验：先让模型只预测仓位，把趋势、波动、乖离率翻译成自然语言状态再回测，逐步逼近交易本质，并给出可复现的完整代码与指标对比。"
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260920142100-llm-csi1000-three-experiments.jpg"
---
Agent 能做交易吗？nof1.ai 在去年底做了一场实验并在互联网上进行了直播。和小龙虾一样，当时引起了巨大的轰动。不过，今天这个直播网站已是门前冷落鞍马稀了。

部分原因是，参与交易的 Agent，最好的成绩也只取得了0.019的夏普率，还不如 A 股散户，这一局，Agent 完败。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260915111717.png)

不过，时间又过去了9个月。这9个月，是有史以来，人工智能发展最迅速的时刻。9个月之后，情况又会如何？

这篇文章将介绍三个实验。这三个实验不仅仅是要验证 Agent 是否有交易能力，更要挖掘 Agent 交易背后的原理，探索改进之道。

## /01 只预测仓位

第一个实验的构建方法如下：

程序先用收盘价构造三类特征：20 日趋势、20 日实现波动率，以及价格相对 20 日均线的 Z-score（乖离率），再把它们翻译成自然语言状态（离散化），例如：

`趋势上行｜波动偏高｜价格偏强`

趋势和波动各有两种状态，乖离率按以下公式计算强弱，共分三档：

$$
zscore_{20} = (close-mean_{20})/std_{20}
$$

当zscore_20 大于等于0.75时，就认为是价格偏强；小于等于负0.75时，认为价格偏弱；其余的状态算成价格中性。因此，三类特征总共构成12种状态。

在回测时，在每个月初重新统计过去三年的历史：每一种状态出现过多少次、随后的日收益均值是多少、风险调整后的得分如何。

我们给 LLM 的输入如下：

```json
{
  "任务": "你是研究回测里的仓位风控助手。不要预测涨跌，不要给投资建议。",
  "要求": "按样本数、下一日平均收益、风险调整得分，为每个状态选择满仓、半仓或低仓；证据不足选半仓；仅返回 JSON。",
  "格式": {"policy": {"状态名": "满仓|半仓|低仓"}},
  "状态统计": "rows"
}
```

其中 rows 类似于：

```json
[
  {"state": "趋势上行|波动偏低|价格偏强", "count": 142, "mean_next_return": 0.0008, "sharpe_like": 0.31},
  {"state": "趋势下行|波动偏高|价格偏弱", "count": 118, "mean_next_return": -0.0012, "sharpe_like": -0.42},
  {"state": "趋势上行|波动偏高|价格中性", "count": 18, "mean_next_return": 0.002, "sharpe_like": 0.5}
]
```

LLM将输出以下结论：

```json
{"policy": {
  "趋势上行|波动偏低|价格偏强": "满仓",
  "趋势下行|波动偏高|价格偏弱": "低仓",
  "趋势上行|波动偏高|价格中性": "半仓"
}}
```

然后程序把仓位翻译成操作指令，实现回测。

<!--PAID CONTENT START-->

三个实验方法有所不同，但仍有一些共同方法，为避免冗长的篇幅，我们把公共代码提取如下：

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

以下就是实验一的实现方案：

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

### 实验一的结果

样本外区间 2019-01-02 → 2026-08-28（规则/LLM 并行逐日结算 1855 个交易日；LLM 共 92 个决策月，本次重跑全部成功、0 个回退月）：


| 策略             | 总收益 | 年化收益 | 年化波动 | Sharpe | Sortino | 最大回撤 |
| ---------------- | ------ | -------- | -------- | ------ | ------- | -------- |
| 买入持有（同窗） | +76.0% | +8.0%    | 25.0%    | 0.43   | 0.60    | -46.7%   |
| 规则基准         | +0.4%  | +0.1%    | 9.3%     | 0.05   | 0.07    | -26.3%   |
| LLM 风控         | +0.4%  | +0.1%    | 9.3%     | 0.05   | 0.07    | -26.3%   |

**结论**：LLM 把波动（25%→9.3%）和回撤（-46.7%→-26.3%）砍半——它是合格的"风险调制器"；但在 2019–2026 的大牛市窗口里大幅跑输买入持有，且与规则基准几乎重合（92 个月里 LLM 的选择与规则逐日一致），说明这套统计表里没有方向 alpha。

![实验一规则净值 vs 同窗买入持有、实验二周一动量净值、实验三周四 knn5+q 净值](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-curves.png)

![knn5+q 周四与实验一规则的回撤对比](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-drawdowns.png)

这基本上就是我们在 nof1.ai 上看到的情况。

## /02 标签历史 + 趋势研判

实验一的特点是，它完全只利用过去的统计特征，而『剥离』了近期走势：它不知道"当前像历史上哪一段"，也不知道"那种情形之后发生了什么"。这会导致在一个长期熊市之后，即使行情好转，但统计特征如果还没有扭转，它就只能机械压仓位，从而大幅跑输买入持有。

统计特征实际上是压缩了信息。在压缩过程中，它丢失了趋势。即使 LLM 能够看懂趋势，它也得不到此信息输入。所以，我们进行以下改进：不做统计，而是把原始的数据直接喂给 AI：

1. 每次决策附带 48 周"特征 + 下一周真实结果"的带标签历史表，让 LLM 做历史类比
2. 缩短调仓周期，使得 LLM 可以更灵活地响应趋势变化。我们把调仓改成周频；任务则从"选仓位档"改成"趋势/反转研判 + 动作 + 仓位"。

现在，我们给 LLM 的输入就变成了：

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

可以看出，输入的特征已经变了：

1. 我们提供了每周的 pnl —— 每轮预测最多附带 48 周历史，趋势信息已经包括在内，只是看 LLM 能否提取到
2. 乖离率也依然提供。不过现在我们使用的是 zscore5 —— 即 5 日窗口的乖离率。
3. 波动率以 atr （真实波动率）的方式提供，并且是百分比形式
4. 提供了反转指标 rsi5

除了特征之外，我们还提供可以参考的预测值： next_pnl 与 next_sharpe，看 LLM 能否把特征与未来的走势关联起来并找出规律。

<!--PAID CONTENT START-->

以下是实验二的代码：

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

回测这样进行：

1. 在调仓周进行快照（含本周 5 日 RSI/z-score 序列）
2. 过去 48 周每条都带其下一周真实结果
3. LLM 输出趋势 + 动作 + 仓位（自洽校正）→ 失败降级空仓 → 次周结算。

评估取**最近 100 周**（2024-08 → 2026-08，五个调仓日各自窗口），买入持有/动量取同窗。

以下是实验二的结果（2026-09-16 用 `deepseek-v4-flash` 全量重跑，周一到周五五个调仓日各取最近 100 周；LLM 统一为 v2 自洽提示词，失败周降级空仓计入）：

![实验二结果：买入持有 vs 动量规则 vs LLM 同窗同日对比，总收益、年化波动、Sharpe、Sortino、最大回撤五面板分组柱状图](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-exp2-bars.png)

与实验一相比，实验二的成绩大幅提升。从 Sharpe 分布图中可以看出，几乎在每一个调仓日，**LLM 都取得了更好的夏普率**。通过观察总收益和最大回撤图，我们可以得出结论，夏普的提升主要是通过降低波动和回撤风险带来的。

大幅改进的原因主要是：

1. 缩短调仓周期，更及时响应趋势变化
2. 给 LLM 更多原始信息（带标签历史），让它可以自己做时序类比。
3. 增加了更多的反转特征

但是，我们还能不能进一步提升数据表现呢？ 很显然，我们还可以加入更多的特征。在实验二中，我们还只使用了**两个**反转特征，即乖离率和 RSI 值。但实际上，确实有一些非常有效的**短线见顶和见底特征**我们没有加入。

考虑到短线特征在学术（多数来自于实战派）上争议比较大，在本次实验中，我决定不加入这些经验。那要如何改进呢？

我把这个问题抛给了 LLM。

!!! quote
    请分析前两个实验，帮我设计实验三，以提升 LLM 的交易表现。

LLM 给出以下分析：

!!! quote
    诊断实验二的三个薄弱点（均可从前 500 行代码看出）：

   - 信息太散：48 周带标签历史一股脑塞进 prompt，模型要自己在 48 条记录里“找相似”——这正是实验一用统计表解决、实验二又放弃的问题。注意力被均摊，真正相关的历史周（比如同样“RSI 低位回升+Z 转正”的那几周）被淹没在长列表里。
   - 输出偏保守：position 是 [0,1] 连续值，模型均值 0.38~0.46 低于中性线——但这只是"偏保守"而非"回避极端"：实测 42%~58% 的仓位落在 [0.4,0.6] 之外，五个调仓日都出现过 0.00 的全空仓，最大值到 0.80~0.90。模型敢表态，只是平均不敢重仓。
   - 执行太软：动作与仓位虽有自洽校正，但“加大仓位”+0.10 这类模糊表态对收益的贡献被稀释。
     LLM 给出的分析很有意思：第一条是关于时序数据如何分析、如何发现规律的改进建议；第二条则是对 LLM 自身运行机制的洞察。对于第二类问题，用 LLM 做交易的新手一定要多加留意。

Man proposes, God disposes。**LLM 可以提出建议，但人才可以做出决定**。我们是 LLM 的神。LLM 的建议质量如何？我们通过实验三来检测一下。

## /03 相似周检索 + 输出离散化

根据 LLM 的建议，我们对实验二做以下改动：

1. 欧氏距离（按历史向量池标准化）只选 top-k 最像的历史周，聚焦注意力；
2. 仓位强制离散到三档 `{0.3, 0.5, 0.7}`，逼LLM明确表态。A/B 开关：`knn5` / `knn5+quantize` / `knn48+quantize`，其中 `knn48+quantize` 近似全历史对照。

<!--PAID CONTENT START-->

以下是实验三的代码：

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

运行结果如下：

![实验二 vs 实验三（knn5+quantize）同日对比：总收益、年化波动、Sharpe、Sortino、最大回撤五面板分组柱状图](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/llm-csi1000-exp2-vs-exp3-bars.png)

![实验三 2×2 因子分解：检索（top-5 × 全历史48）× 离散化（连续 × 量化）的 Sharpe 矩阵与五日均值](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/exp2-vs-exp3-2x2.png)

第一张图的结果比较令人意外。从周一到周三，Sharpe 好于实验二，但周四到周五的结果却弱于实验二。但是，考虑到 sharpe 的绝对值，实验三中，周一和周二的表现即使占优，我们也不会采纳。这样看来，实验三对实验二，实际上是1胜两负的结果。

图二是把离散化与相似周检索两策略单独拆开来进行实验的结果对照图。两个策略单独使用时为负（检索 -0.39）或视条件而定（量化 -0.18~+0.38），联合使用后互相抵消。

## /04 LLM 为什么能做交易

从实验一到实验二，LLM 在周四、周五调仓时，回测出较好的夏普率。由于回测只用了100周（即两年）的时间，我们还不能完全说 LLM 适合做交易。

但是，如果这个回测结果可信，又该如何解释？

这可能意味着，Transformer/Attention 能读时序数据之间的关联并生成信号。

**① Attention 确实能做"形态—结果"类比。** 当把价格/指标序列化为带标签的历史（本周特征 + 下周真实结果），LLM 的注意力机制可以在"当前周"与"历史周"之间建立关联：实验二重跑的 corr 在五个调仓日为 -0.07~+0.16（周三/四/五为正，周一/二为负）、实验三的 reason 字段频繁引用具体历史周（"最相似历史周 2024-04-15 下周下跌 -0.78%……"）。这正是"读时序关联生成信号"的机制证据，但强度有限。

**② 仓位管理是核心价值。** 三个实验中，其实 LLM 并没有改善收益，它改善的是风险控制：波动从 ~30% 压到 ~10%、回撤从 -46% 压到 -10% 上下。机制是"信心加权"——证据强时加仓、证据弱时降仓。即使单周方向判断不准，这种加权本身就能抬 Sharpe、压回撤。LLM 在这里的角色是**风险研究员/预算分配器**，不是价格预言机。

## /05 谈一点 LLM 原理

前面讲过了 LLM 为什么可以做交易。但这只是硬币的一面。如果我们不能完全理解 LLM 的原理和机制，实际上是很难改进策略的，即使是让 LLM 自我改进也不可能，实验三基本上证明了这一点。

LLM 做交易，首先会遇到价格表征不连续，距离失真和算术不可靠的问题。在实验中，我们输入了股票的价格、RSI 和下周的涨跌幅。在传统的量化交易模型中，这些是非常自然的输入数据，模型一般直接使用它们。

但在 LLM 中，模型首先要把文本输入处理成为 token，这里要用到 BPE（Byte Pair Encoding）编码器。数字是连续的、无穷多的，但分词器是有限集。因此，在将输入文本转换成 token 的过程中，数值可能被切碎（比如 7.9 可能会被切成 `7` + `.9`，或者 `7.` + `9`，也可能整体就是 `7.9`），距离会丢失（即使词表中同时存在"7.7", "7.8"和"7.9"这样三个 token，那么，三个 token 之间，两两距离基本上是不等的；而在数学语言中，7.7与7.8， 7.8与7.9是等距的，而7.7与7.9之间的距离，是其它关系的两倍。token 化将数字之间的关系扭曲了）。

因此，LLM 要知道 RSI数值中，78.1要比78.0大，比我们想像的要吃力得多，它需要大量的训练产生记忆，然后在生成时，通过模式补全加推理来得出78.1比78.0大的结论。这也是以下智商测试题中，LLM 过去常常翻车的原因：

!!! quote
    9.11和9.9哪个大？

此外，LLM 还有无时间归纳偏置。价格序列里"先涨后跌"和"先跌后涨"是完全不同的信号，但模型没有内建的方向/因果结构，只能从数据里学。

最后还要强调一点，我们选择量化交易，是为了相对于主观交易，减少随机性和不确定性。但是，LLM 是生成模型，它在输出时，会因为采样温度带来输出方差。所以，基于 LLM 的交易策略，具有不可解释性、不稳定性。

因此，尽管我们在实验二中，取得了不错的收益，但从 LLM 的原理来看，这种收益可能有偶然性。前一节中得到的结论，仓位管理是核心价值，这可能是结合 LLM 原理分析之后，最合理的结论。

但是，实验二也确实指出一种可能，那就是 transformer/attention 能够在较长的时间序列中，发现规律和应用规律。

如何进行改进了？Chronos可能代表了一种方向。

在进行输入处理时，在 Chronos 中，"分词"这件事从 BPE 换成了"数值分箱"（scaling + quantization），从而保住了序和尺度。它先是对原始序列先做均值/方差标准化，再把连续值均匀映射到固定数量的箱（bin，如 4096 个有序 token）。bin 的 id 本身就是有序的——bin 100 和 bin 101 在数值上相邻，分词层面也相邻。BPE 丢掉的保距性在这里被设计回来了。

在训练目标上，Chronos不是"预测下一个词"，而是"预测下一个 bin"——即对未来值建模一个离散概率分布，天然输出分位数/置信区间。LLM 只能给你一个点估计（position=0.55），Chronos 直接给你"下周收益的分布"，这对仓位 sizing 是更原生的输入。

另外， Chronos使用因果掩码的自回归训练，时间方向被硬编码进训练目标，从而也解决了我们前面所说的，『无时间归纳偏置』的问题。

除了 Chronos，类似的方案还有 Salesforce 提出的 Moirai。它的优势在于多变量原生，可以同时支持多路因子时序输入。而 Chronos 只支持一路因子数据，多因子场景下还需要外加一个决策层把多个因子拼起来；因为通道之间是条件独立的，Chronos 就难以学到"成交量放大 + 价格滞涨"这种跨通道形态。

## /06 复现指南

本文使用的代码可在 quantide 官方网站获取。要复现本文结论，你需要能使用 tushare和 LLM 大模型。本文在进行回测时，使用的是 deepseek-v4-flash 正式版。使用其它模型，可能得出不同的结论。
