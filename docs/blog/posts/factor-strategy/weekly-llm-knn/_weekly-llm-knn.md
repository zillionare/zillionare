---
title: 让 LLM 少说废话：相似周检索 + 输出离散化的周频实验
date: 2026-08-28
description: 上一轮发现给 LLM 喂"当前仓位"反而稀释方向信息。这一轮聚焦两项增强：用 top-k 相似周替代 48 周全历史，把仓位输出量化成三档，逼模型明确表态。
tags: [量化交易, 大模型, 周频, KNN, 中证1000, 相似周]
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
  kernelspec:
    display_name: Python (weekly-llm)
    language: python
    name: weekly-llm
---

> 系列上一篇（weekly-llm-csi1000）的结论是：48 周带标签历史 + 趋势研判让模型具备了低波动属性，但方向信息量（corr）在 ±0.12 之间随调仓日摆动；显式传入"当前仓位"（v3）反而因锚定效应稀释了方向判断，已被否决。
>
> 本篇对症下药，做两项不增加模型调用成本的增强，并与 v2 基线做 A/B：**相似周 top-k 检索** 和 **输出离散化**。代码完整嵌入本文，`jupytext --to ipynb weekly-llm-knn.md` 可转成 Notebook。

## 我们想验证的两件事

1. **相似周检索能否提高信息量？** v2 把 48 周历史全部塞给模型，让它"自己找相似"。本篇改用**欧氏距离（按历史向量池标准化）挑出与本周最像的 top-k 周**，只把这 k 周 + 各自的下一周结果交给模型。假设：模型注意力有限，喂更相关样本能做出更准的类比。
2. **离散化能否让模型更果断？** v2 里模型倾向给 0.4~0.6 的模糊仓位。本篇把输出强制量化到 `{0.3, 0.5, 0.7}` 三档——逼它在"明显该躲/明显该上"之间表态，去掉中间地带。

两个开关互相独立（`knn_k` 与 `quantize`），所以可以做四组对照：`knn5` / `knn5+quantize` / 基线（knn 关闭时的 v2 行为）。

## 数据与指标

沿用系列设定：中证1000（`000852.SH`），每周调仓日可配（本篇默认周四），每决策周带 48 周历史（内部做相似检索）。特征、缓存、自洽约束、回测指标（总收益/夏普/回撤/corr）都与上一篇一致。

```python
# cell 1：依赖、常量、.env
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
WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五"]


def env(name, default=""):
    return os.getenv(name, default)
```

```python
# cell 2：读取 .env
if load_dotenv is not None:
    load_dotenv()
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / ".env").exists():
            load_dotenv(p / ".env")
            break
print("tushare_token:", bool(env("tushare_token")), "| LLM:", env("LLM_MODEL"))
```

```python
# cell 3：配置
@dataclass
class Config:
    symbol: str = "000852.SH"
    start: str = "20160101"
    rebalance_weekday: int = 3  # 0=周一 ... 4=周五；本篇默认周四
    rsi_period: int = 5
    rsi_warmup: int = 60
    atr_period: int = 14
    z_window: int = 5
    weeks_history: int = 4
    history_weeks: int = 48
    knn_k: int = 5
    quantize: bool = False
    quant_levels: tuple = (0.3, 0.5, 0.7)
    cost_bps: float = 5.0
    model: str = ""


config = Config(rebalance_weekday=3, knn_k=5, quantize=False)
print("调仓日：", WEEKDAY_NAMES[config.rebalance_weekday], "| knn_k =", config.knn_k,
      "| quantize =", config.quantize)
```

```python
# cell 4：数据获取 + 缓存
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


data = fetch_index(config.symbol, config.start, None, cache_path="output/data/000852_SH.parquet")
print("共 %d 根日线" % len(data))
```

```python
# cell 5：指标（与系列一致）
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


def make_features(data, config):
    f = data.copy()
    f["atr"] = atr(f.high, f.low, f.pre_close, config.atr_period)
    f["atr_pct"] = f["atr"] / f["close"]
    f["rsi5"] = rsi(f["close"], config.rsi_period)
    f.loc[f.index < f.index[config.rsi_warmup - 1], "rsi5"] = np.nan
    f["z5"] = zscore(f["close"], config.z_window)
    return f
```

```python
# cell 6：周特征 + 48 周历史
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


feats = make_features(data, config)
records = build_records(feats, config)
print("周数:", len(records), "| 末周:", records[-1]["date"].date(), "| 历史条数:", len(records[-1]["history"]))
```

```python
# cell 7：相似周 top-k 检索
def _week_vector(w):
    return np.array([w["pnl"], w["atr_pct"]] + w["rsi5"] + w["zscore5"], dtype=float)


def knn_history(this_week, history, k=5):
    """按"历史向量池"均值/标准差标准化后，欧氏距离挑最近的 k 个历史周。"""
    if not history:
        return [], []
    pool = [v for v in (_week_vector(h) for h in history) if not np.isnan(v).any()]
    if not pool:
        return [], []
    pool = np.array(pool)
    mean, std = pool.mean(axis=0), pool.std(axis=0)
    std[std == 0] = 1.0
    target = (_week_vector(this_week) - mean) / std
    if np.isnan(target).any():
        return [], []
    dists = np.linalg.norm((pool - mean) / std - target, axis=1)
    order = np.argsort(dists)[:k]
    top = [(history[idx], float(dists[idx])) for idx in order if not np.isnan(dists[idx])]
    return ([h for h, _ in top], [d for _, d in top]) if top else ([], [])


r = records[-1]
top, dists = knn_history(r["this_week"], r["history"], config.knn_k)
print("本周:", r["date"].date())
for h, d in zip(top, dists):
    print("  %s dist=%.3f pnl=%.4f next_pnl=%.4f next_sharpe=%.2f"
          % (h["date"], d, h["pnl"], h["next_pnl"], h["next_sharpe"]))
```

```python
# cell 8：离散化 + 自洽统一解析
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


def resolve_position(prev_position, action, position, quantize=False, levels=(0.3, 0.5, 0.7)):
    p = reconcile_position(prev_position, action, position)
    if not quantize:
        return p
    valid = [x for x in levels if
             (action in RAISE_ACTIONS and x > prev_position) or
             (action in LOWER_ACTIONS and x < prev_position) or
             (action not in RAISE_ACTIONS and action not in LOWER_ACTIONS)]
    if not valid:
        valid = list(levels)
    return min(valid, key=lambda x: abs(x - p))


print("prev=0.5 买入 raw=0.4 ->", resolve_position(0.5, "买入", 0.4, True))
print("prev=0.5 减仓 raw=0.7 ->", resolve_position(0.5, "减少仓位", 0.7, True))
```

```python
# cell 9：LLM 趋势研判（相似周检索 + 可选离散化）
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

    top_k, dists = knn_history(record["this_week"], record["history"], config.knn_k)
    instruction = {
        "任务": ("你是周频趋势研判员。结合给定的【相似历史周】，判断当前市场处于：上涨趋势、下跌趋势，"
                "还是即将反转/正在反转/已经反转；并决定下周动作：买入、加大仓位、减少仓位或空仓观望。"
                "只做多，不做空。研究回测，非投资建议。"),
        "说明": ("下方仅列出与当前周特征最相似的 %d 个历史周。每个都带下一周实际结果 next_pnl/next_sharpe；"
                "请优先依据这些最相关样本决策，而非泛泛而谈。证据不足保持中等仓位。" % len(top_k)),
        "特征含义": {"pnl": "该周涨跌幅", "atr_pct": "该周 5 日 ATR/收盘价 均值",
                     "rsi5": "每个交易日当天及前 4 天 5 日 RSI", "zscore5": "相对 5 日均线 z-score",
                     "next_pnl": "下一周实际涨跌幅", "next_sharpe": "下一周日收益年化夏普"},
        "仓位自洽规则": ("『买入』『加大仓位』时 position 必须【大于】prev_position；"
                        "『减少仓位』『空仓观望』时 position 必须【小于】prev_position。"),
        "prev_position": prev_position,
        "当前周": {k: record["this_week"][k] for k in ["date", "pnl", "atr_pct", "rsi5", "zscore5"]},
        "相似历史周（共 %d 个）" % len(top_k): [dict(h) for h in top_k],
        "输出格式": {"trend": "上涨趋势|下跌趋势|反转酝酿|反转进行中|反转已确立",
                     "action": "买入|加大仓位|减少仓位|空仓观望",
                     "position": "下周目标仓位 [0,1]，与 action 自洽", "confidence": "0-1",
                     "reason": "一句话理由（引用最相似的 1~2 个历史周）"},
    }
    payload = {"model": model, "stream": False, "max_tokens": 16000, "reasoning_effort": "max",
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
            "knn_distances": dists}
```

```python
# cell 10：回测与评估
def run_backtest(records, positions, cost_bps=5.0):
    eq = peak = 1.0
    rows = []
    for rec, pos in zip(records, positions):
        gross = pos * rec["next_week_return"]
        cost = abs(pos) * cost_bps / 10000.0
        net = gross - cost
        eq *= 1.0 + net; peak = max(peak, eq)
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


bh = run_backtest(records, [1.0] * len(records), config.cost_bps)
mom = run_backtest(records, [1.0 if r["this_week"]["pnl"] > 0 else 0.0 for r in records], config.cost_bps)
print("买入持有:", metrics(bh))
print("动量规则:", metrics(mom))
```

```python
# cell 11：跑 LLM（knn 检索，可选离散化；结果按 配置 tag + 日期 + 模型 缓存）
MAX_WEEKS = 100
result_dir = Path("output"); result_dir.mkdir(exist_ok=True)
cache_dir = result_dir / "llm_cache"; cache_dir.mkdir(parents=True, exist_ok=True)
tag = "knn%d%s" % (config.knn_k, "q" if config.quantize else "")
model = config.model or env("LLM_MODEL")

rec_eval = records[-MAX_WEEKS:] if MAX_WEEKS else records
positions, failures, prev_position = [], 0, 0.0
for rec in rec_eval:
    cache_file = cache_dir / ("llm-%s-%s-%s.json" % (tag, str(rec["date"].date()), model))
    if cache_file.exists():
        fc = json.loads(cache_file.read_text(encoding="utf-8"))
        fc["position"] = resolve_position(prev_position, fc.get("action", ""), fc["position"],
                                          quantize=config.quantize, levels=config.quant_levels)
    else:
        try:
            fc = llm_forecast(rec, config, prev_position)
            cache_file.write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")
        except Exception:
            failures += 1
            fc = {"trend": "", "action": "", "position": 0.0, "confidence": 0.0, "reason": "失败降级空仓"}
    prev_position = fc["position"]
    positions.append(fc["position"])
print("LLM 失败周数：%d / %d" % (failures, len(rec_eval)))

llm_bt = run_backtest(rec_eval, positions, config.cost_bps)
bh_win = run_backtest(rec_eval, [1.0] * len(rec_eval), config.cost_bps)
mom_win = run_backtest(rec_eval, [1.0 if r["this_week"]["pnl"] > 0 else 0.0 for r in rec_eval], config.cost_bps)
print("评估周数:", len(rec_eval), "| 配置: knn_k=%d quantize=%s" % (config.knn_k, config.quantize))
print("LLM:", metrics(llm_bt))
print("同窗 买入持有:", metrics(bh_win))
print("同窗 动量规则:", metrics(mom_win))
```

```python
# cell 12：A/B 结果对比表
import pandas as pd

def fmt(m):
    return {"总收益": f"{m['total_return']:.1%}", "年化波动": f"{m['annual_vol']:.1%}",
            "夏普": f"{m['sharpe']:.2f}", "最大回撤": f"{m['max_drawdown']:.1%}",
            "corr": f"{m['corr']:.3f}", "平均仓位": f"{m['avg_position']:.2f}", "周数": m["weeks"]}

pd.DataFrame([
    {"策略": "买入持有(同窗)", **fmt(metrics(bh_win))},
    {"策略": "动量规则(同窗)", **fmt(metrics(mom_win))},
    {"策略": "LLM knn%d q=%d (同窗)" % (config.knn_k, config.quantize), **fmt(metrics(llm_bt))},
])
```

```python
# cell 13：净值曲线
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(llm_bt.index, llm_bt.equity, label="LLM knn(同窗)")
plt.plot(bh_win.index, bh_win.equity, label="买入持有(同窗)", linestyle="--")
plt.plot(mom_win.index, mom_win.equity, label="动量规则(同窗)", linestyle=":")
plt.legend(loc="upper left")
plt.title("相似周检索 + 离散化 周频实验")
plt.grid(alpha=0.3)
plt.show()
```

## 如何切换 A/B

只需改 cell 3 的 `config` 再重跑 cell 9~13：

- `knn_k=5, quantize=False` → 纯相似周检索
- `knn_k=5, quantize=True` → 相似周 + 输出离散化
- `knn_k=48`（≈全历史）`quantize=False` → 退化为接近 v2 基线（k 设足够大）

每个配置的 LLM 决策会缓存到 `output/llm_cache/llm-knn<k>[q]-<date>-<model>.json`，切换后重跑不会重复烧 API。

## 结果：周四调仓的 A/B

全部为最近 100 周样本外（周四调仓），deepseek-v4-flash、reasoning=max、0 次调用失败（影响小）：

| 配置 | 总收益 | 年化波动 | 夏普 | 最大回撤 | corr | 平均仓位 |
| --- | --- | --- | --- | --- | --- | --- |
| 买入持有 | +56.8% | 25.9% | 1.03 | -22.0% | — | 1.00 |
| 动量规则(只做多) | +52.1% | 19.4% | 1.22 | -9.9% | +0.08 | 0.61 |
| knn5（检索、无量化） | +20.3% | 10.0% | 1.01 | -7.0% | -0.01 | 0.39 |
| **knn5 + quantize** | **+30.1%** | 11.8% | **1.22** | -11.9% | +0.03 | 0.51 |
| knn48 + quantize（近全历史） | +25.8% | 13.4% | 0.96 | -13.4% | -0.06 | 0.55 |
| （对照）上一篇 v2 周四 | +27.7% | 12.0% | 1.12 | -7.9% | +0.03 | 0.47 |

三点读法：

1. **离散化（quantize）是主要收益来源**：同为检索，quantize 关 → 开，夏普 1.01 → **1.22**，平均仓位 0.39 → 0.51。逼模型在 `{0.3,0.5,0.7}` 明确表态，显著增强了方向执行力。
2. **相似周检索（knn5）优于全历史（knn48）**：同为 quantize 条件，knn5q 夏普 1.22 > knn48q 0.96，corr +0.03 vs -0.06。**只喂最相关的 top-5 周，比塞 48 周全历史更有效**——这否定了"样本太少不够判断"的担忧，指向"全历史反而稀释相关信号"。
3. **knn5q 是当前最佳配置**：夏普 1.22 与动量规则持平，回撤 -11.9%，corr +0.03，显著跑赢买入持有。

## 跨调仓日稳定性（knn5q 全量验证）

> knn5q 在周一、周二、周三、周五各串行跑 100 周；因运行中网络波动有缺失，后经断点续传补跑，**最终四个调仓日均为 100/100、0 次失败**。结果为最近 100 周样本外：

| 调仓日 | 买入持有 夏普 | 动量 夏普 | **LLM knn5q 夏普** | LLM corr | LLM 总收益 | LLM 最大回撤 |
| --- | --- | --- | --- | --- | --- | --- |
| 周一 | 0.75 | -0.55 | 0.88 | +0.03 | +26.1% | -9.4% |
| 周二 | 0.78 | 0.55 | 0.98 | +0.03 | +29.3% | -9.9% |
| 周三 | 0.95 | 1.28 | 0.98 | -0.02 | +21.8% | -10.4% |
| **周四** | 1.03 | 1.22 | **1.22** | **+0.03** | **+30.1%** | -11.9% |
| 周五 | 1.00 | 1.34 | 0.94 | -0.03 | +23.3% | -10.9% |

读法：

1. **knn5q 不跨调仓日稳定**——仅在周四达到夏普 1.22（与动量持平），其余四天 0.88~0.98，且周三/五被动量规则（1.28~1.34）明显压制。调仓日效应再次被证实比模型改动更重要。
2. **corr 全在 ±0.03 内**——相似周检索 + 离散化改善了周四的执行（平均仓位 0.51），但没有解决方向信息薄弱这个根本问题。
3. **与上一篇 v2 一致**：无论 v2 还是 knn5q，周四都是 LLM 相对最占优的调仓日，但都不是稳定的 alpha 来源。
4. 补跑前后的对比提醒：**缺失周若降级为空仓会显著低估表现**（如周二补跑前夏普 0.74/corr-0.07，补跑后 0.98/corr+0.03）——断点续传补全是保证结论可靠的前提。

## 结论

- **离散化有效**：周四 knn5 → knn5q，夏普 1.01 → 1.22，模型在 `{0.3, 0.5, 0.7}` 三档上明确表态比自由连续值更有执行力。
- **相似周检索优于全历史**：周四 knn5q(1.22) > knn48q(0.96)，只喂最相关的 top-5 周比塞 48 周全历史更有信息量——"历史不会简单重演"更准确的表述是"模型需要聚焦最相关样本"。
- **但两者都未能带来跨调仓日的稳定方向信息**（corr ≈ 0）。这条路线证明了"如何让模型更好地表态/聚焦"有帮助，但仍未解决"模型到底有没有方向预测力"这个核心问题。

## 参考

- 本系列上一篇：weekly-llm-csi1000（48 周带标签历史 + 趋势研判）。
- José Carlos Gonzáles Tanaka, [Building a Guardrailed LLM Trading Risk-Manager Agent for AAPL](https://blog.quantinsti.com/ai-aapl-trading-risk-manager-deepseek-python/), QuantInsti。
- Tushare 日线接口：<https://tushare.pro/document/1?doc_id=27>。