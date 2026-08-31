---
title: 大模型不必猜明天：一个面向中证 1000 的仓位风控实验
date: 2026-08-26
description: 用 Tushare 与 LLM 重建一套可审计的日频仓位风控回测，并把它运行在一个 Jupyter Notebook 里。
tags: [量化交易, 风险管理, 大模型, Tushare, 中证1000]
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
  kernelspec:
    display_name: Python (llm-guard)
    language: python
    name: llm-guard
---

> 本文是基于公开研究思路写成的原创中文实验文章，不是原文逐段翻译，也不构成投资建议。配套代码完整嵌入本文，可用 jupytext 直接转成可运行的 Notebook：
>
> 　`jupytext --to ipynb llm-guardrail-csi300.md`

许多“大模型交易策略”一开始就问错了问题：明天会涨还是会跌？对流动性很好的指数而言，要求一个语言模型给出稳定的隔日方向预测，往往是把它推向最不擅长、也最难验证的位置。

这里换一个问题：**在不同的市场状态里，我今天应该暴露多少风险？** 这不是让模型去找神秘的 alpha，而是让它在一套明确的风险框架中，对仓位作有限选择。大模型只能在“满仓、半仓、低仓”三档里回答；它不能做空，不能加杠杆，也不能直接下单。

这种限制很重要。它把模型从“交易员”降级为一个**有记录、可替换、可审计的风控顾问**。

## 这份实验如何工作

程序先用收盘价构造三类特征：20 日趋势、20 日实现波动率，以及价格相对 20 日均线的 Z-score，再把它们翻译成自然语言状态，例如：

`趋势上行｜波动偏高｜价格偏强`

每天的状态不是用来解释当天收益，而是用于决定**下一交易日**的仓位。回测在每个月初重新统计过去三年的历史：每一种状态出现过多少次、随后的日收益均值是多少、风险调整后的得分如何。代码特意丢弃了紧邻决策日、尚未实现的那一笔收益，避免把今天的答案偷偷放回昨天的训练集。

默认的 `rule`（规则）模式用明确规则分仓：样本不足半仓；历史均值与风险调整都较好就满仓；都较弱就低仓。**只有当 `.env` 里配置好了 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 时**，程序（CLI 的 `--policy deepseek`，也就是下方 Notebook 里的 `mode="llm"`）才会把同一张状态统计表交给大模型，要求它返回三档仓位的 JSON。任何网络错误、密钥缺失或格式错误都会在缓存里留下原因，然后退回规则基准，而不会悄悄改写回测结果。

## 为什么不直接读 Yahoo Finance

为了让大陆读者能跑起来，这个版本直接用 Tushare 下载中证 1000（`000852.SH`）的日线。Token 放 `.env` 的 `tushare_token` 里；模型相关的三个变量 `LLM_MODEL`、`LLM_BASE_URL`、`LLM_API_KEY` 也统一从 `.env` 读取，代码里不再出现任何硬编码密钥。数据从哪来、是否复权、是否授权，都由研究者掌控。指数方便说明方法，但它并非可直接买入的资产；若研究 ETF 或个股，应换成相应品种的复权序列并重设成本与交易约束。

```python
# 第 1 个 Cell：依赖与常量
import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

TRADING_DAYS = 252
OOS_START = "2019-01-01"  # 3 年训练期之后的第一天
```

```python
# 第 2 个 Cell：读取 .env
# 把 tushare_token、LLM_MODEL、LLM_BASE_URL、LLM_API_KEY 放在仓库根目录的 .env 里。
if load_dotenv is not None:
    load_dotenv(Path.home() / ".env")
    load_dotenv(Path.cwd() / ".env")
    load_dotenv(Path.cwd().parent.parent.parent.parent / ".env")
    load_dotenv(Path.cwd().parent.parent.parent.parent.parent / ".env")


def env(name, default=""):
    return os.getenv(name, default)


print("tushare_token 已配置:", bool(env("tushare_token")))
print("LLM_MODEL:", env("LLM_MODEL"))
print("LLM_BASE_URL:", env("LLM_BASE_URL"))
print("LLM_API_KEY 已配置:", bool(env("LLM_API_KEY")))
```

```python
# 第 3 个 Cell：配置
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


config = Config(train_years=3, cost_bps=5.0)
config.model = env("LLM_MODEL") or "deepseek-chat"
config
```

```python
# 第 4 个 Cell：数据读取
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


def read_tushare_index(symbol, start, end=None):
    import tushare as ts
    token = env("tushare_token")
    if not token:
        raise RuntimeError("请在 .env 中设置 tushare_token。")
    raw = ts.pro_api(token).index_daily(
        ts_code=symbol,
        start_date=start,
        end_date=end or pd.Timestamp.today().strftime("%Y%m%d"),
    )
    if raw is None or raw.empty:
        raise RuntimeError("Tushare 没有返回数据；请检查 token、权限、代码与网络。")
    return normalise(raw, "trade_date", "close")


SYMBOL = "000852.SH"  # 中证 1000 指数
prices = read_tushare_index(SYMBOL, "20160101")
print("共", len(prices), "根日线")
prices.tail()
```

```python
# 第 5 个 Cell：特征工程 —— 描述市场的“情绪”
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
    # 状态在 t 日收盘判定，用于预测 t+1 的收益；不存在同一天信号这回事。
    frame["next_ret"] = frame.ret.shift(-1)
    return frame


feats = make_features(prices)
feats[["close", "ret", "trend_20", "vol_20", "vol_median", "zscore_20", "state", "next_ret"]].tail(10)
```

```python
# 第 6 个 Cell：把状态量化成统计表
def state_stats(train):
    usable = train.dropna(subset=["state", "next_ret"])
    rows = []
    for name, ret in usable.groupby("state").next_ret:
        count = int(ret.count())
        mean = float(ret.mean())
        std = float(ret.std(ddof=1)) if count > 1 else 0.0
        rows.append({
            "state": name,
            "count": count,
            "mean_next_return": mean,
            "sharpe_like": mean / std * np.sqrt(TRADING_DAYS) if std else 0.0,
        })
    return sorted(rows, key=lambda item: item["state"])


train = feats[feats.index < pd.Timestamp("2019-01-01")]
state_stats(train)
```

```python
# 第 7 个 Cell：规则基线（对照组）
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


rule_policy(state_stats(train))
```

```python
# 第 8 个 Cell：LLM 风控顾问 ——
# 只读状态统计表，只回“满仓 | 半仓 | 低仓”的 JSON。
def llm_policy(rows, config):
    api_key = env("LLM_API_KEY")
    base_url = env("LLM_BASE_URL")
    model = config.model or env("LLM_MODEL") or "deepseek-chat"
    if not api_key:
        raise RuntimeError("未设置 LLM_API_KEY")
    if not base_url:
        base_url = "https://api.deepseek.com/v1"
    instruction = {
        "任务": "你是研究回测里的仓位风控助手。不要预测涨跌，不要给投资建议。",
        "要求": "按样本数、下一日平均收益、风险调整得分，为每个状态选择满仓、半仓或低仓；证据不足选半仓；仅返回 JSON。",
        "格式": {"policy": {"状态名": "满仓|半仓|低仓"}},
        "状态统计": rows,
    }
    body = json.dumps({"model": model, "stream": False, "messages": [
        {"role": "system", "content": "只输出 JSON。"},
        {"role": "user", "content": json.dumps(instruction, ensure_ascii=False)},
    ]}, ensure_ascii=False).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    request = urllib.request.Request(
        endpoint, data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key, "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    last_error = None
    text = None
    for _attempt in range(3):
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
```

```python
# 第 9 个 Cell：月度策略 + 缓存
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
    if mode == "llm":
        try:
            policy, source = llm_policy(rows, config), config.model or env("LLM_MODEL") or "LLM"
        except (RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
            source = "LLM 失败，退回规则基准：" + str(error)
    cache.write_text(json.dumps({"as_of": str(day.date()), "source": source, "statistics": rows, "policy": policy}, ensure_ascii=False, indent=2), encoding="utf-8")
    return policy, source
```

```python
# 第 10 个 Cell：回测主循环（含硬性风控护盾）
def performance(equity, turnover):
    ret = equity.pct_change().dropna()
    years = len(ret) / TRADING_DAYS
    drawdown = equity / equity.cummax() - 1
    return {
        "total_return": float(equity.iloc[-1] - 1.0),
        "cagr": float(equity.iloc[-1] ** (1 / years) - 1.0),
        "annual_volatility": float(ret.std(ddof=1) * np.sqrt(TRADING_DAYS)),
        "sharpe_zero_rate": float(ret.mean() / ret.std(ddof=1) * np.sqrt(TRADING_DAYS)) if ret.std(ddof=1) else 0.0,
        "max_drawdown": float(drawdown.min()),
        "average_daily_turnover": float(turnover.mean()),
        "observations": int(len(ret)),
    }


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
            # 排除昨日：昨日的 next_ret（今天）在决策时并不可知。
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
            flat_days, action = 0, "强制再准入，防止风控死锁"
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
```

```python
# 第 11 个 Cell：配置一个输出目录并运行
from pathlib import Path as _Path

out_rule = _Path("output_rule")
out_rule.mkdir(exist_ok=True)
rule_result, rule_metrics, rule_notes = backtest(feats, config, "rule", out_rule)
rule_metrics
```

```python
# 第 12 个 Cell：运行 LLM 模式（无 key 时自动退回规则基准）
out_llm = _Path("output_llm")
out_llm.mkdir(exist_ok=True)
llm_result, llm_metrics, llm_notes = backtest(feats, config, "llm", out_llm)
llm_metrics
```

```python
# 第 13 个 Cell：汇总对比
import pandas as pd

rows = []
for name, m in [("规则基准", rule_metrics), ("LLM 风控", llm_metrics)]:
    rows.append({
        "策略": name,
        "年化收益率": f"{m['cagr']:.2%}",
        "年化波动率": f"{m['annual_volatility']:.2%}",
        "夏普(零利)": f"{m['sharpe_zero_rate']:.2f}",
        "最大回撤": f"{m['max_drawdown']:.2%}",
        "日均换手": f"{m['average_daily_turnover']:.3f}",
    })
pd.DataFrame(rows)
```

```python
# 第 14 个 Cell：净值曲线
import matplotlib.pyplot as plt

buy = feats.loc[rule_result.index, "close"] / feats.loc[rule_result.index, "close"].iloc[0]

plt.figure(figsize=(10, 5))
plt.plot(rule_result.index, rule_result.equity, label="规则基准")
plt.plot(llm_result.index, llm_result.equity, label="LLM 风控")
plt.plot(rule_result.index, buy, label="中证1000 买入持有")
plt.legend()
plt.title("样本外净值曲线（2019–2026）")
plt.grid(alpha=0.3)
plt.show()
```

## 为什么要做 walk-forward（滚动前推）

回测最怕“用未来骗自己”。代码把数据切成两段：前 3 年训练，之后才做真正意义上的**样本外**回测；并且从第 4 年开始，每个月初都**重新**用一个只包含过去数据的窗口重建统计表与仓位档位，再持有一个月。净值从一个起点连续累加，不每个月重置成 1.0——这才是市场真正前后的样子。

## 回测结果（样本外：2019 年起）

下面是笔记本第 13、14 个 Cell 在本机跑出的真实数字（`rule` 与 `llm` 各有 92 个月、合并约 1853 个样本外交易日）：

| 策略 | 年化收益 | 年化波动 | 夏普(零利率) | 最大回撤 | 日均换手 |
| --- | --- | --- | --- | --- | --- |
| 买入持有指数 | +7.3% | 25.0% | 0.41 | -46.7% | — |
| 规则基准 | -0.1% | 9.4% | 0.02 | -26.2% | 0.064 |
| LLM 风控 | +0.1% | 9.5% | 0.04 | -26.4% | 0.063 |

（买入持有为同区间指数的复利累计，仅作参照，非可直接交易资产。）

先不要只看收益，至少同时比较这几个数：

- **年化波动**：仓位调节把组合波动从指数的 25% 压到约 9.5%，这正是“拿收益换低波动”的直接侧面。
- **最大回撤**：从指数的 -46.7% 收窄到约 -26%，但保护也付出回报成本：在 2019–2026 这段中证 1000 强烈上行的区间里追不上指数。
- **平均日换手**：约 0.06，说明低频信号没有被频繁调仓吃掉。
- **规则与 LLM 的并排结果**：两者几乎重合——这说明在“满仓/半仓/低仓”三档和 `<3 年训练窗`下，简明规则已经逼近 LLM 的判断。**如果规则不弱于 LLM，就不要为了用 LLM 而保留 LLM。**

这个结论本身就是研究的一部分：LLM 的价值是**风险调制**而不是 alpha 生成，它并没有把一个“拿收益换回撤”的护栏变成可持续的超额收益。

## 真正棘手的 bug：风控把自己锁死

回撤止损有个不显眼的逻辑陷阱。假设策略亏到阈值，于是把仓位降为零；仓位为零后净值不再变，回撤永远不能自然收回；次日系统再见同一回撤，又继续把仓位设为零。一个本打算短暂保护的止损，变成了无限期停摆。

上面第 10 个 Cell 里，`cooldown`（冷静期）和 `max_flat_days`（强制再准入）正是为此设计。它不声称强制再准入必然正确；它只是把“永远不再参与市场”从一个隐蔽的程序事故，变成一个必须明说出来的研究选择。

## 关键细节：缓存不仅能省钱

第 9 个 Cell 会把每个月策略或模型看到的统计数据、作出的仓位映射和来源写进 `policy_cache/`。有三个作用：

1. 重跑不需要再调 API；
2. 结果可被审计——能清楚地看到到底这个月模型给了哪个状态多少仓位；
3. 失败记录也是证据：谁会退回规则、为什么不退回，都留痕。

## 结语

大模型在这里最有价值的身份不是**预言者**，而是受约束的**比较器**：它读一张已经由历史数据生成的状态表，对被噪声污染的统计作有限度的仓位判断。它若不能稳定优于朴素的规则，就没有理由留在系统里。

`deepseek`（LLM）与 `rule`（规则）的具体数字，以你在笔记本里运行的结果为准——这比任何结论都诚实。

## 参考

- José Carlos Gonzáles Tanaka, [Building a Guardrailed LLM Trading Risk-Manager Agent for AAPL](https://blog.quantinsti.com/ai-aapl-trading-risk-manager-deepseek-python/), QuantInsti。
- DeepSeek（或你的 LLM）API 文档。
- Tushare 日线接口说明：<https://tushare.pro/document/1?doc_id=27>。