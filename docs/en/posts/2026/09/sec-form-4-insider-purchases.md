---
title: "Can Outsiders Profit From Insider Trading?"
date: 2026-09-09
slug: en/posts/factor-strategy/sec-form-4-insider-purchases
tags: [Factor Investing, Event Study, China A-Shares, Quantitative Research]
excerpt: "We test whether retail investors can profit from insider buying disclosures in China A-shares. Using a rigorous event study with placebo controls, we find the alpha is likely embedded in momentum, not a standalone edge."
lang: en
translation_of: posts/factor-strategy/sec-form-4-insider-purchases
auto_translated: true
source_sha: c86711e3e326c2e9f2601163dcd6815f59acbb78
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/oxford.jpg"
---

**Imagine this.** You open East Money, and a notification pops up in your watchlist:

> [!tip]
> As of the close on [Date], the company’s controlling shareholder and Chairman, Mr. XXX, cumulatively increased his shareholding by [Number] shares via the Shanghai Stock Exchange’s centralized bidding system, representing [Y]% of the total share capital. The total value was RMB [Z] million. The increase plan has been fully implemented.

What’s your first reaction? Most people would immediately check the market data and ask: **"Should I follow suit?"**

This is the factor we are studying today.

**Can external followers profit from insider trading disclosures?** In academic terms: After controlling shareholders with information advantages legally declare their purchases, can external investors achieve significantly positive risk-adjusted returns based on **public information** after deducting transaction costs?

The article includes complete, runnable source code. Please obtain the runnable notebook file via the attached PDF or by contacting us.

## Insider Trading: Can Outsiders Profit?

Insider trading refers to company insiders profiting from the stock market using information unavailable to the public. The James D. Logan case is a classic example of insider trading. Logan, Chairman of MicroTouch Systems, purchased 14,000 shares of MicroTouch stock in ten installments through a trust established for his minor children in May, June, and September 2000, during secret acquisition negotiations with Tyco and 3M. On November 13, 2000, MicroTouch announced it would be acquired by 3M at $21 per share. The trust sold the shares for a profit of $177,375, achieving a return of 152% in less than six months.

It was precisely to combat insider trading that the SEC legislated in 1934, mandating mandatory disclosure and the disgorgement of short-swing profits. Disgorgement refers to the rule that profits made by insiders from buying and selling (or selling and buying) within six months must be returned to the company.

This rule, combined with mandatory disclosure, largely closes the loophole for insider trading. What does mandatory disclosure mean? Directors, executives, and beneficial owners holding more than 10% of shares must declare their share changes via **Form 4** within two business days of the change.

Thus, executives can trade based on their information—seemingly unavoidable—but the public gets the same information at the latest within two business days. Although the buying timing is lagged, the public can prioritize selling before the executives. Executives have information priority; the public has trading priority. The rules are thus fair to everyone.

Therefore, the "insider trading" mentioned earlier, if executed according to regulations, becomes legal insider trading.

Can the general public derive some Alpha from "insider" trading information? A recent blog post on quantinsti explored this. China has a similar disclosure system, and relevant information can be obtained via Tushare. Thus, this article explores this Alpha.

The article is divided into two parts. Part One covers SEC Form 4 insider purchases, applicable to US stocks; Part Two focuses on the Alpha study of insider trading disclosures in China A-shares.

> [!info]
> In August 2026, AlphaAI founder **Mikhail Makeev** conducted a rigorous event study on all C-suite insider purchases from **2022Q1 to 2026Q2** using SEC’s free EDGAR data—*[SEC Form 4 Insider Purchases in Python: A Filing-Date Event Study with Free EDGAR Data](https://blog.quantinsti.com/sec-form-4-insider-trading-python-event-study/)* (QuantInsti, 2026-08). This article was inspired by that work to conduct localized research. Due to data limitations, the value of this article lies in demonstrating a rigorous research methodology rather than directly providing reusable factors/strategies.

## SEC Form 4 Insider Purchases

To prevent insider trading, Section 16 of the US Securities Exchange Act of 1934 requires three types of "insiders" to disclose shareholding changes:

- Company **directors**
- **Officers**, primarily the C-suite
- Beneficial owners holding **more than 10%** of registered equity securities

Whenever a "change in beneficial ownership" occurs, these individuals must submit **Form 4** (Insider Trading Report) via EDGAR.

**Reporters must complete the filing within two business days of the reportable transaction.** This deadline makes Form 4 an **extremely convenient dataset for market making and quantitative research**: it is public, structured, and has a very short disclosure lag.

### Form 4 Transaction Codes

In the non-derivative transaction table of Form 4, there is a key field: "transaction code." The original article only used records with code **P**, excluding others for the following reasons:

| Code | SEC Meaning (Excerpt)        | Original Treatment |
| ---- | ---------------------------- | ------------------ |
| **P** | Open market purchase **or** private purchase | ✅ Used             |
| S     | Open market sale or private sale | ❌ Excluded         |
| A     | Grants/awards under 16b-3(d) | ❌ Excluded         |
| M     | Exercise/conversion of derivatives | ❌ Excluded         |
| F     | Securities delivered/withheld to pay exercise price or taxes | ❌ Excluded         |
| G     | Bona fide gift               | ❌ Excluded         |
| Other | Conversion, issuer disposition, exercise, etc. | ❌ Excluded         |

Why exclude sale records? **Shouldn't stock prices fall if executives and major shareholders are selling?** If we combine purchases and sales, shouldn't the factor's effect be better?

We will provide a theoretical explanation here, and later, using China A-shares as a sample, we will complete an **empirical study**. The results of the empirical study will not only answer this question but also strongly illustrate why subjective trading based on intuition inevitably loses to quantitative trading.

For ordinary investors, we often sell because we are bearish on a stock's prospects. However, executives' reasons for selling stocks often include diversification, liquidity needs, and tax planning—motivations unrelated to the company's prospects. Purchases (especially when executives invest their own money) are more likely to bet that "the stock price is below intrinsic value." Cohen/Malloy/Pomorski (2012) finely categorized trades into opportunistic vs. routine, further confirming that purchases better distinguish information-driven trades.

When we project our own experiences onto others, explaining their behavior based on our own experience, we inevitably draw the one-sided conclusion that if executives sell, the company's prospects are dim, and the stock must fall.

Excluding one-sided subjective experience and restoring objective truth is precisely the advantage of quantitative analysis.

### Core Results of the Original Article

Original sample: Insider purchases by C-suite executives with Code P and non-10b5-1 filings from 2022Q1 to 2026Q2. After filtering, we obtained **7,405 scoreable signals** (issuer × filing date). The **filing-date event study** using SPY as the benchmark:

| Indicator | N     | Mean        | Two-way Clustered t |
| --------- | ----- | ----------- | ------------------- |
| SPY Adj. (1-day) | 7,405 | **+0.534%** | 6.460               |
| SPY Adj. (5-day) | 7,404 | **+1.009%** | 5.053               |
| CAR (21 trading days) | 7,397 | +0.980%     | 1.678               |
| CAR (63 trading days) | 7,048 | +1.103%     | 1.194               |

The original article's conclusion is phrased very cautiously, but the data itself is quite powerful:

1. **Short-term (1-day +0.53%, 5-day +1.01%) shows statistically significant SPY-adjusted excess returns**, with two-way clustered t-values of 6.46 / 5.05, and confidence intervals excluding 0.
2. **Longer-term (21/63 days) CAR/BHAR confidence intervals include 0**—there is no stable evidence of persistent drift after insider purchases.

## A-Shares "Form 4"

Although A-shares do not have Form 4, there is a system of the same nature: **share changes by directors, supervisors, senior management, and shareholders holding more than 5% (major shareholders) must be disclosed.**

Here we summarize how to obtain insider trading disclosure information across the three securities markets mentioned in this article:

| Region | Platform       | Legal Basis              | Subjects               |
| ------ | -------------- | ------------------------ | ---------------------- |
| US     | **EDGAR**      | Securities Exchange Act Sec 16 | Directors, Officers, Beneficiaries >10% |
| HK     | **HKEXnews**   | SFO Part XV              | Directors, Officers, Shareholders >5% |
| A-Shares | **CNINFO**   | Securities Law + SSE/SZSE Rules | Directors, Supervisors, Senior Management, Shareholders >5% |

All three are **statutory, public, free electronic disclosures**.

However, in A-shares, legally mandated data is disclosed in text format. To use it directly, we need to scrape and parse the data. Therefore, we generally obtain insider trading information through third-party software, such as Tushare.

## Tushare Corresponding Data Interface

Tushare (requires certain points) provides **structured data on director/supervisor/senior management/shareholder increases and decreases**:

1. **`stk_holdertrade` (Shareholder Increases/Decreases)** — The interface closest to Form 4. The returned data includes the following fields:
   - `ann_date`: Announcement date
   - `holder_name`: Shareholder/Executive name
   - `holder_type`: **G=Executive (Director/Supervisor/Senior Mgmt), P=Individual Shareholder (>5%), C=Corporate Shareholder**
   - `in_de`: **IN=Increase, DE=Decrease** (corresponds to Form 4's P (buy) / S (sell))
   - ... (omitted)
   - `begin_date`: Increase/decrease start date
   - `close_date`: Increase/decrease end date

2. `stk_managers` (Director/Supervisor/Senior Mgmt List), `top10_holders` (Top 10 Shareholders) can serve as supplementary alignment tools.

<!--PAID CONTENT START-->
Here is example code for obtaining data. For efficiency, we also implemented data caching:

```python
from pathlib import Path
import tempfile
import pandas as pd
import numpy as np

import tushare as ts

pro = ts.pro_api()

# cell 2：数据获取 + 缓存（stk_holdertrade 单次调用上限 3000 行，必须分片）
# ---- 数据跨度开关（调试用）----
# SAMPLE_YEARS = 0   → 用全部近 FULL_YEARS(7) 年（正式结论）
# SAMPLE_YEARS = 1   → 只用最近 1 年（调试跑通逻辑，快）
# 调通后把 SAMPLE_YEARS 设回 0 即可跑全量。
FULL_YEARS = 7
SAMPLE_YEARS = 0   # ← 正式：0（7 年全量）；调试可改 1（仅 1 年，速跑通）

YEARS = FULL_YEARS if SAMPLE_YEARS == 0 else SAMPLE_YEARS
END_DATE = pd.Timestamp.today().strftime("%Y%m%d")
START_DATE = (pd.Timestamp.today() - pd.DateOffset(years=YEARS)).strftime("%Y%m%d")

# 缓存目录：使用系统临时目录，保证任何环境（无需 .runtime）都能直接运行
def runtime_dir():
    return Path(tempfile.gettempdir()) / "sec-form4-insider-purchases"

RUNTIME_DIR = runtime_dir()
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
CACHE = RUNTIME_DIR / f"holder_data_{YEARS}y.parquet"   # 缓存按年份命名，避免调试/正式误用
print(f"缓存目录：{RUNTIME_DIR}")
print(f"数据范围：{START_DATE} ~ {END_DATE}（{'近 7 年' if SAMPLE_YEARS == 0 else f'调试模式：仅 {YEARS} 年'}）")
```
<!--PAID CONTENT END-->

<!--PAID CONTENT START-->
Using the following method, we obtain Tushare data and utilize caching.

```python
# cell 2b：数据获取（含 begin_date/close_date 字段，用于披露滞后判断）
# 调试开关：DEBUG_YEARS=1 只拉 1 年（快）；=0 用 cell 2 的 SAMPLE_YEARS 决定（正式 7 年）
DEBUG_YEARS = 0  # ← 正式：0（7 年全量）；调试：1（1 年）
_EFFECTIVE_YEARS = DEBUG_YEARS if DEBUG_YEARS else YEARS
_CACHE = RUNTIME_DIR / f"holder_data_{_EFFECTIVE_YEARS}y_v2.parquet"  # v2: 含 begin/close 字段

def fetch_holdertrade_all(start=None, end=None, chunk="3M"):
    start = start or (pd.Timestamp.today() - pd.DateOffset(years=_EFFECTIVE_YEARS)).strftime("%Y%m%d")
    end = end or pd.Timestamp.today().strftime("%Y%m%d")
    if _CACHE.exists():
        df = pd.read_parquet(_CACHE)
        if "close_date" in df.columns:  # 字段齐全才复用，否则重拉
            return df
    # 按季度分片，绕过单次 3000 行上限；显式请求 begin_date/close_date（默认不返回）
    fields = "ts_code,ann_date,holder_name,holder_type,in_de,change_vol,change_ratio,after_share,after_ratio,avg_price,total_share,begin_date,close_date"
    idx = pd.date_range(start, end, freq=chunk).strftime("%Y%m%d").tolist()
    idx.append(end)
    frames = []
    for a, b in zip(idx, idx[1:]):
        df = pro.stk_holdertrade(start_date=a, end_date=b, fields=fields)
        if df is not None and not df.empty:
            frames.append(df)
    out = pd.concat(frames).drop_duplicates()
    out.to_parquet(_CACHE)
    return out

raw = fetch_holdertrade_all()
print(f"原始记录：{len(raw)} 行（调试 {_EFFECTIVE_YEARS} 年，v2 含 begin/close 字段）")
print("字段含 begin_date/close_date:", "begin_date" in raw.columns and "close_date" in raw.columns)
```

Through the above code, we retrieve all increase/decrease records within the [START_DATE, END_DATE] interval and save them as a parquet cache file, eliminating the need to call Tushare for subsequent debugging.

<!--PAID CONTENT END-->

What do these fields mean? Tushare's documentation is not very detailed. They may consider some aspects "industry common sense" and thus omit them from the documentation. However, we must actually clarify the following time-related information:

1. Increase start time: `begin_date` in Tushare
2. Increase end time: `close_date` in Tushare
3. Announcement time after the increase ends: `ann_date` in Tushare
4. The time Tushare makes this announcement data available. Tushare does not provide its compilation time.

Some information is sufficient from the documentation, while others require **distribution studies** of existing data to accurately understand their meanings. Ultimately, we found:

1. `ann_date < begin_date`: 0.0%. Thus, Tushare data does not collect information when companies release increase plans.
2. `ann_date` within `[begin, close]`: 6.5% — This is unreasonable, likely reflecting poor data quality.
3. `ann_date > close_date`: 93.5%. This is the announcement after completion.

If we further decompose the distribution of `ann_date > close_date`, we find:

1. The median of `ann_date - close_date` is 2 days — meaning companies usually announce 1-2 business days after the increase ends. However, the mean is 40 days, the 90th percentile is 107 days, and the longest record exceeds 10 years — this may not be a Tushare error.
2. Tushare's compilation and entry time is 1-3 days later than `ann_date`; but this data sampling is insufficient and involves speculation (only using data from September 8th — at that time, Tushare had only compiled data up to last Friday, not the previous trading day's Monday).

Given the above data distribution, we should handle signal construction as follows:

1. Only take records where `ann_date - close_date <= 2` days.
2. Starting from the day after `ann_date` ($T_0$): Day 1's return is $T_{1,close}/T_{1,open} - 1$; thereafter, calculate daily returns using $C_n/C_{n-1} - 1$.

Based on the previous conclusion, we can construct the buy signal as follows: Only take records where `ann_date - close_date <= 2` days — only these "increase ends, then announcement" signals.

<!--PAID CONTENT START-->
The following code constructs the buy signal:

```python
# cell 3：构造"买入信号"（映射 Form 4 漏斗的简化版，保留全部信号）
# 按前文结论：只取 ann_date - close_date <= 2 天的记录 —— 只有这类"增持结束即公告"
# 的信号，其公告日才是"公众首次可见"的时点，才适合做公告日事件研究。
MAX_DISCLOSURE_LAG = 2  # 增持结束(close_date)到公告(ann_date)的最长滞后（自然日）

def build_signals(raw):
    """增持 + 高管/个人/公司股东 → 同一股票×公告日合并为一个信号。
    过滤：ann_date - close_date <= MAX_DISCLOSURE_LAG（排除滞后公告/补录数据）。"""
    if "close_date" not in raw.columns:
        raise ValueError("缺少 close_date 字段，请先运行 cell 2b（需显式请求该字段）")
    s = raw[raw["in_de"] == "IN"].copy()
    # 披露滞后 = 公告日 - 增持结束日
    s["ann_dt"] = pd.to_datetime(s["ann_date"], format="%Y%m%d")
    s["close_dt"] = pd.to_datetime(s["close_date"], format="%Y%m%d", errors="coerce")
    s = s.dropna(subset=["close_dt"])                    # 无 close_date 的记录无法判断时效，排除
    s["disclosure_lag"] = (s["ann_dt"] - s["close_dt"]).dt.days
    s = s[s["disclosure_lag"].between(0, MAX_DISCLOSURE_LAG)]  # 0~2 天：完成后立即公告
    s["value"] = s["change_vol"] * s["avg_price"].fillna(0)
    signals = (s.groupby(["ts_code", "ann_date"], as_index=False)
                .agg(signals_n=("holder_name", "size"),
                     holders=("holder_name", "nunique"),
                     change_vol_sum=("change_vol", "sum"),
                     value_sum=("value", "sum"),
                     holders_type=("holder_type", lambda x: ",".join(sorted(set(x.astype(str))))))
                .rename(columns={"ann_date": "filing_date", "ts_code": "ticker"}))
    return signals

signals = build_signals(raw)
print(f"买入信号数（股票×公告日，滞后≤{MAX_DISCLOSURE_LAG}天，全量）: {len(signals)}")
print(f"涉及股票数: {signals['ticker'].nunique()}")
print(f"信号时间跨度: {signals['filing_date'].min()} ~ {signals['filing_date'].max()}")
```

<!--PAID CONTENT END-->

### Experimental Design

After knowing how to construct the buy signal, the entire backtest is routine. However, the statistics we designed this time are different, so it is necessary to explain them.

**CAR**

We will not use the direct return of individual stocks after purchase, but rather their calibrated return, CAR.

CAR = **C**umulative **A**bnormal **R**eturn. The calculation method is as follows:

- **"Abnormal return"**: The portion of a single day's individual stock return that **exceeds the benchmark** (here, benchmark = CSI 300):
  `AR_t = Individual Stock Return_t − CSI 300 Return_t`
- **"Cumulative"**: Summing the daily AR from day 1 to day h after the announcement (compound multiplication):
  `CAR_h = ∏(1 + AR_t) − 1`, t = 1..h

Thus, **CAR_1 = Cumulative abnormal return 1 day after announcement**, CAR_21 = Cumulative abnormal return 21 trading days after announcement, and so on. We introduce this concept because if we directly calculate the cumulative return n days after the announcement, it would include market volatility.

**pooled t**

After obtaining several CAR returns, we must first determine whether these returns are due to random error or truly contain "something," which requires significance testing using the pooled t-test.

The pooled t-test is essentially a regular t-test that treats N CARs as mutually independent samples, just under a different name:

`pooled t = Mean CAR / (Sample Standard Deviation / √N)`

It answers: "How many standard errors is the mean CAR from 0?" — > 4~5 is generally "highly significant."

However, the pooled t-statistic has a flaw: it assumes the N signals are independent. In reality, **the same stock may increase holdings multiple times over 7 years, and multiple stocks may increase holdings in the same month**. These events are not independent. The pooled t-test "inflates" the sample size, causing significance to be **overestimated**.

Thus, we introduced two-way clustering.

**Two-way clustered t (two-way clustered t)**

To address the independence flaw of the pooled t-test, we use **Cameron–Gelbach–Miller (CGM) two-way clustering** to correct standard errors:

- Cluster simultaneously along two dimensions: **stock (issuer)** and **announcement month (entry-month)**
- Multiple increases by the same stock, and increases by multiple stocks in the same month, are "merged" into dependencies within the cluster, not treated as N independent samples
- The resulting standard errors are larger and more conservative, and t-values are typically **smaller and more credible** than pooled t

The pooled t is the "naive upper bound," and the two-way clustered t is the "honest lower bound." The larger the gap between them, the stronger the internal dependence of the samples.

If the above indicators give us an optimistic result, is it sufficient to believe that Alpha exists here?

Obviously, it is still too optimistic.

CAR only eliminates the market factor (by subtracting CSI 300); a positive CAR is not necessarily caused by the "announcement." It could be that the "stock was already rising" (e.g., executives often increase holdings during strong periods, and the announcement timing is selected on days likely to continue rising). To solve this problem, we must also adopt a method commonly used in medicine: using a **placebo** to eliminate bias.

The literal meaning of **placebo** is the "placebo" in medical experiments — **pairing true events with a control group that "looks the same but is not this event."**

It answers:

> "If we replace the announcement day with another [ordinary day] for this stock, is the return still this large?"

The specific procedure is:

1. For each true signal, within the trading days of the same stock, **exclude the true announcement day ±63 day window**;
2. Among the remaining days, **match based on the momentum and volatility of the 20 days prior to the announcement day**, selecting a batch of "fake dates" most similar in characteristics to the true announcement day;
3. Using the **exact same next-day open entry rule**, treat each fake date as an "event day" to calculate CAR;
4. Compile a **distribution** of CAR for fake dates (placebo panel).

Interpretation: If the true average CAR is **higher than 95% of the fake dates**, it indicates that "this timing" is truly special; if it falls in the middle of the distribution, it indicates that this return **exists on any ordinary day**, unrelated to the announcement itself.

<!--PAID CONTENT START-->
The following cells 4~7 implement this design. Cells 4/5 calculate CAR, cell 6 calculates two-way clustered t, and cell 7 constructs the placebo; cell 8 summarizes the final statistical table and chart. **(Complete runnable code available in the cloud drive ipynb; only key method points are shown below.)**

```python
# cell 4：日线数据与事件研究说明
# 关键设计：公告一般是【盘后】发布，外部投资者最早只能【次日开盘】买入。
# 所以事件研究的入场点 = 公告日之后第一个交易日的【开盘价】，
# 第 1 日收益 = 次日 open→close；之后为 close→close。基准做同样处理。
# 这避免了"用当日收盘价"——那是公告出来前就实现不了的收益（lookahead）。
def fetch_daily(ticker, start=None, end=None):
    df = pro.daily(ts_code=ticker, start_date=start or START_DATE, end_date=end or END_DATE)
    if df is None or df.empty:
        return None
    df = df.set_index(pd.to_datetime(df["trade_date"])).sort_index()
    df["open_ret"] = df["open"].pct_change().fillna(0)     # 开盘→收盘
    df["close_ret"] = df["close"].pct_change().fillna(0)   # 收盘→收盘
    return df

def fetch_benchmark(start=None, end=None):
    df = pro.index_daily(ts_code="000300.SH", start_date=start or START_DATE, end_date=end or END_DATE)
    if df is None or df.empty:
        return None
    df = df.set_index(pd.to_datetime(df["trade_date"])).sort_index()
    df["open_ret"] = df["open"].pct_change().fillna(0)
    df["close_ret"] = df["close"].pct_change().fillna(0)
    return df

print("基准：沪深 300（000300.SH）")
print("入场规则：公告日（盘后）→ 次日开盘买入 → 第 1 日 open→close，之后 close→close")
```

```python
# cell 5：事件研究主循环（次日开盘入场，CAR_1/2/3/5/21/63）
def event_study(signals, daily_func, bench_func,
                horizons=(1, 2, 3, 5, 21, 63), start=None, end=None):
    """对每个信号：公告日(盘后)后首个交易日【开盘】进场。
    第 1 日收益 = 次日 open→close（当天持有）；之后 close→close。
    个股与基准各自如此，逐日算超额收益后累乘为 CAR_h = prod(1+x)-1。
    返回逐信号 DataFrame：ticker/filing_date/month + CAR_1..CAR_63。
    """
    bmk = bench_func(start, end)
    if bmk is None:
        return pd.DataFrame()
    bmk = bmk[~bmk.index.duplicated(keep="last")].sort_index()
    rows = []
    for sig in signals.itertuples():
        px = daily_func(sig.ticker, start, end)
        if px is None or px.empty:
            continue
        px = px[~px.index.duplicated(keep="last")].sort_index()
        i0 = px.index.searchsorted(pd.Timestamp(sig.filing_date)) + 1  # 公告后首个交易日
        if i0 + max(horizons) > len(px):
            continue
        # 对齐基准（个股交易日 reindex 到基准）
        bmk_al = bmk[["open", "close"]].reindex(px.index).ffill()
        rec = {"ticker": sig.ticker, "filing_date": str(sig.filing_date)}
        # 第 1 日（i0）：开盘买、收盘卖
        s1 = px["close"].iloc[i0] / px["open"].iloc[i0] - 1
        b1 = bmk_al["close"].iloc[i0] / bmk_al["open"].iloc[i0] - 1
        for h in horizons:
            # 构造前 h 日的超额收益序列
            xs = []
            for t in range(h):
                idx = i0 + t
                if t == 0:
                    xs.append(s1 - b1)
                else:
                    xs.append((px["close"].iloc[idx] / px["close"].iloc[idx - 1] - 1)
                              - (bmk_al["close"].iloc[idx] / bmk_al["close"].iloc[idx - 1] - 1))
            rec[f"CAR_{h}"] = float(np.prod(1.0 + np.array(xs)) - 1.0)
        rows.append(rec)
    out = pd.DataFrame(rows)
    if not out.empty:
        out["month"] = pd.to_datetime(out["filing_date"]).dt.to_period("M").astype(str)
    return out

print("event_study() 已升级：次日开盘入场 + CAR_1/2/3/5/21/63，返回逐信号 CAR 表。")
```

```python
# cell 6：双向聚类 t（Cameron–Gelbach–Miller）——"股票 × 公告月" 聚类
# 文章"完整复现需要补什么"第 3 点的实现。输入：每个信号一行 CAR + ticker + 公告年月。
def two_way_cluster_t(car_df, y_col, g1_col, g2_col):
    """CGM 最小充分量估计：t = mean / se，se 由 股票 × 公告月 双向聚类给出。"""
    import numpy as np  # 局部 import，保证 cell 独立可运行

    y = car_df[y_col].values
    n = len(y)
    g1 = car_df[g1_col].values       # 股票（issuer）
    g2 = car_df[g2_col].values       # 公告月（entry-month）

    # within-cluster sums for union adjustment
    g1_ids, g1_inv = np.unique(g1, return_inverse=True)
    g2_ids, g2_inv = np.unique(g2, return_inverse=True)

    # depvar residual (demeaned, no regressors -> residual = y - mean)
    res = y - y.mean()

    # meat = sum over clusters of (sum of res in cluster)^2
    def meat(clusters, nids):
        M = np.zeros(nids)
        for i in range(n):
            M[clusters[i]] += res[i]
        return (M ** 2).sum()

    # sandwich: V = (n-1)/(n-2) * [meat_g1/n^2 + meat_g2/n^2 - meat_union/n^2]
    union = (g1.astype(str) + "|" + g2.astype(str))
    _, union_inv = np.unique(union, return_inverse=True)
    meat_g1, meat_g2 = meat(g1_inv, len(g1_ids)), meat(g2_inv, len(g2_ids))
    meat_union = meat(union_inv, len(np.unique(union_inv)))
    n1, n2 = len(g1_ids), len(g2_ids)
    df_adj = min(n1, n2) - 1
    V = (n - 1) / (n - 2) * (meat_g1 + meat_g2 - meat_union) / n ** 2
    se = np.sqrt(V)
    return y.mean() / se if se > 0 else np.nan, df_adj

print("two_way_cluster_t() 就绪：把每个信号的 CAR 与 ticker、公告月拼成 DataFrame 即可用。")
```

```python
# cell 7：placebo 对照（同一 ticker、事件窗口外、匹配动量/波动率的对照日期）
def build_placebo(car_df, daily_years, bmk_daily, horizons=(1, 2, 3, 5, 21),
                  blackout=63, n_placebo=200, seed=42):
    """为每个真实信号构建"假日期"(placebo) 的 CAR，衡量"如果这天不是公告日，收益如何"。
    
    设计（对应原文 §placebo）：
      1. 对每个真实信号，在其同一只股票的【真实公告日 ±63 日之外】的交易日里，
         挑出与公告日前 20 日动量/波动相似的一批候选日；
      2. 以这些假日期为"事件日"，用与真实信号完全相同的次日开盘入场规则算 CAR；
      3. 得到 placebo 面板：dict[horizon -> list[list[float]]]。
    
    解读："真实平均 CAR" 若显著高于 placebo 分布上尾(如 95% 分位)，
    才说明"公告这个时点本身"携带信息；否则正收益更可能来自股票本身
    的动量/波动特征，与公告无关。
    """
    import numpy as np, pandas as pd  # 局部 import

    bmk = bmk_daily
    if bmk is None or bmk.empty:
        return {h: [] for h in horizons}
    bmk = bmk[~bmk.index.duplicated(keep="last")].sort_index()
    bmk_al = bmk[["open", "close"]].reindex  # 后面按个股索引对齐
    rng = np.random.default_rng(seed)
    panels = {h: [] for h in horizons}
    for sig in car_df.itertuples():
        px = daily_years.get(sig.ticker)
        if px is None or px.empty:
            continue
        px = px[~px.index.duplicated(keep="last")].sort_index()
        bmk_px = bmk_al(px.index).ffill()
        i0 = px.index.searchsorted(pd.Timestamp(sig.filing_date))
        cand = [i for i in range(60, len(px) - max(horizons) - 1)
                if abs(i - i0) > blackout]
        def feat(i):
            w = px["close"].pct_change().iloc[max(0, i - 20):i]
            return (w.mean(), w.std())
        target = feat(i0)
        scored = sorted(((abs(feat(i)[0] - target[0]) + abs(feat(i)[1] - target[1]), i)
                         for i in cand), key=lambda x: x[0])
        # 候选数不足 n_placebo 时"有多少用多少"（1 年调试数据日期有限，7 年全量则充足）
        top = [i for _, i in scored[:max(1, min(n_placebo, len(scored)))]]
        if len(top) < 1:
            continue
        for h in horizons:
            vals = []
            for i in top:
                if i + h >= len(px):
                    continue
                # 与 event_study 相同的次日开盘入场规则
                s1 = px["close"].iloc[i + 1] / px["open"].iloc[i + 1] - 1
                b1 = bmk_px["close"].iloc[i + 1] / bmk_px["open"].iloc[i + 1] - 1
                xs = [s1 - b1]
                for t in range(1, h):
                    idx = i + 1 + t
                    xs.append((px["close"].iloc[idx] / px["close"].iloc[idx - 1] - 1)
                              - (bmk_px["close"].iloc[idx] / bmk_px["close"].iloc[idx - 1] - 1))
                vals.append(float(np.prod(1.0 + np.array(xs)) - 1.0))
            panels[h].append(vals)
    return panels

print("build_placebo() 就绪：placebo 面板的均值分布 vs 真实 CAR——真实若显著高于 placebo 上尾，才说明申报时点本身有信息。")
```
 
```python
# cell 8：真正执行事件研究 + 出图
# 设计要点：
#   - 样本：近 _EFFECTIVE_YEARS 年的全部买入信号（cell 2b 控制；调试 1 年、正式 7 年）；
#   - 入场：公告日(盘后)→次日开盘买入（CAR_1/2/3 用 open→close，之后 close→close）；
#   - 视距：1/2/3/5/21/63 个交易日（事件初期几天更重要，故加 CAR_2/CAR_3）；
#   - 日线：每个 ticker 只拉一次并落盘缓存（按年份命名，调试/正式不互相污染）。
import matplotlib.pyplot as plt
import os

# 与 cell 2b 的有效年份一致
_ES = (pd.Timestamp.today() - pd.DateOffset(years=_EFFECTIVE_YEARS)).strftime("%Y%m%d")
_EE = pd.Timestamp.today().strftime("%Y%m%d")

# 日线缓存也放系统临时目录（cell 2 已定位 RUNTIME_DIR）
DAILY_CACHE = RUNTIME_DIR / f"daily_cache_{_EFFECTIVE_YEARS}y_v2"
DAILY_CACHE.mkdir(parents=True, exist_ok=True)

def daily_cached(ticker, start=None, end=None):
    """拉取并缓存个股日线。event_study 会传 (ticker, start, end)；
    缓存在 [start,end] 覆盖范围内即可复用（调试/正式按年份分目录）。"""
    fp = DAILY_CACHE / f"{ticker}.parquet"
    if fp.exists():
        return pd.read_parquet(fp)
    df = fetch_daily(ticker, start=start or _ES, end=end or _EE)
    if df is not None and not df.empty:
        df.to_parquet(fp)
    return df

# 1) 逐信号算 CAR（对 signals 全量）
print(f"对 {len(signals)} 个信号做事件研究（{_ES}~{_EE}，每个 ticker 日线只拉一次）...")
bmk_full = fetch_benchmark(start=_ES, end=_EE)
car_df = event_study(signals, daily_cached, lambda s, e: bmk_full, start=_ES, end=_EE)
print(f"事件研究完成：{len(car_df)} 个信号有 CAR")

# 2) 各视距：均值 CAR + pooled t + 双向聚类 t（股票×公告月）
HORIZONS = (1, 2, 3, 5, 21, 63)
print("\n视距 | 均值CAR | pooled t | 双向聚类t(股票×公告月) | n")
for h in HORIZONS:
    if f"CAR_{h}" not in car_df.columns:
        continue
    y = car_df[f"CAR_{h}"].dropna()
    n = len(y)
    mean = y.mean()
    pooled_t = mean / (y.std(ddof=1) / np.sqrt(n)) if y.std(ddof=1) > 0 else np.nan
    t2, _ = two_way_cluster_t(car_df.dropna(subset=[f"CAR_{h}"]), f"CAR_{h}", "ticker", "month")
    print(f"  {h:>3}日 | {mean*100:+.3f}% | {pooled_t:.2f} | {t2:.2f} | {n}")

# 3) 图 1：CAR 路径（含 CAR_1/2/3，事件初期更密集）
horizon_list = [0, 1, 2, 3, 5, 21, 63]
exist = [h for h in horizon_list[1:] if f"CAR_{h}" in car_df.columns]
mean_cars = [0.0] + [car_df[f"CAR_{h}"].mean() for h in exist]
plt.figure(figsize=(8, 4))
plt.plot([0] + exist, [m * 100 for m in mean_cars], marker="o", label="买入信号 均值CAR")
plt.axhline(0, color="gray", ls="--", lw=0.8)
plt.xlabel("公告后交易日"); plt.ylabel("均值 CAR (%)")
plt.title("买入信号 CAR 路径（相对沪深300，次日开盘入场）")
plt.grid(alpha=0.3); plt.legend(); plt.show()

# 4) placebo 对照：CAR_1 与 CAR_21 各看一次
# 7 年全量 7092 信号下，对每个信号都跑 200 个对照会很慢；
# placebo 只用于"分布对比"，随机抽 max_placebo_signals 个信号构建即可(仍然稳健)。
import random
random.seed(42)
MAX_PLACEBO_SIGNALS = 1200
n_placebo = 100
for h in (1, 21):
    if f"CAR_{h}" not in car_df.columns:
        continue
    sig_sub = car_df[["ticker", "filing_date"]].sample(min(MAX_PLACEBO_SIGNALS, len(car_df)), random_state=42)
    panels = build_placebo(sig_sub,
                           daily_years={t: daily_cached(t) for t in sig_sub["ticker"].unique()},
                           bmk_daily=bmk_full, horizons=(h,),
                           blackout=63, n_placebo=n_placebo, seed=42)
    ph = panels.get(h, [])
    if ph:
        real_vals = car_df[f"CAR_{h}"].dropna().values
        ph_means = np.array([np.mean(p) for p in ph if len(p)])
        real_rank = (np.mean(real_vals) > ph_means).mean()
        plt.figure(figsize=(8, 4))
        plt.hist(ph_means * 100, bins=25, alpha=0.6, label="placebo 面板均值分布")
        plt.axvline(np.mean(real_vals) * 100, color="red", ls="--", lw=2,
                    label=f"真实 CAR_{h} 均值 = {np.mean(real_vals)*100:+.3f}%")
        plt.axvline(np.quantile(ph_means, 0.95) * 100, color="orange", ls=":", lw=1.5,
                    label=f"placebo 95 分位 = {np.quantile(ph_means, 0.95)*100:+.3f}%")
        plt.xlabel(f"CAR_{h} (%)"); plt.ylabel("频数")
        plt.title(f"买入信号 CAR_{h} vs placebo（时点是否真有信息？）")
        plt.legend(); plt.grid(alpha=0.3); plt.show()
        verdict = ">95%：申报时点本身携带信息" if real_rank > 0.95 else "≤95%：无法确认时点有信息（可能是风格/动量背景）"
        print(f"真实 CAR_{h} 高于 placebo 面板的比例 = {real_rank:.1%} → {verdict}")
    else:
        print(f"placebo 面板为空（CAR_{h}）：请确认 ticker 日线可拉取。")
```

<!--PAID CONTENT END-->

## 3. Conclusion

We used Tushare's nearly 7-year full data (2019-09 ~ 2026-09) + disclosure lag filtering to conduct an event study.

Based on the data design above, the formal analysis **only takes signals where `ann_date − close_date ≤ 2 days` ("increase ends, then announcement")** (excluding polluted data from lagged announcements/historical backfilling). Among the nearly 7-year full 60,000+ increase/decrease records, satisfying this condition and merged into (stock × announcement day) **buy signals total 4,747** (involving 1,905 stocks), of which **4,476** event study samples matched with complete daily window data are scoreable.

| Horizon | Mean CAR | pooled t | Two-way Clustered t (Stock × Announcement Month) | n     |
| ------- | -------- | -------- | ------------------------------------------------ | ----- |
| 1 day   | +0.217%  | 4.80     | **2.41**                                         | 4,476 |
| 2 days  | +0.336%  | 5.25     | 1.81                                             | 4,476 |
| 3 days  | +0.438%  | 5.55     | 1.60                                             | 4,476 |
| 5 days  | +0.763%  | 7.57     | 1.62                                             | 4,476 |
| 21 days | +1.305%  | 6.33     | 1.34                                             | 4,476 |
| 63 days | +2.829%  | 7.87     | 2.19                                             | 4,476 |

Placebo control: The proportion of true CAR_1 higher than the fake date panel is **78.5%**; CAR_21 is **61.1%** — both **≤95%**.

![Buy Signal CAR Path (Relative to CSI 300, Next-Day Open Entry)](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/sec-form-4-car-path.png)

![True CAR_1 vs Placebo Distribution](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/sec-form-4-placebo-car1.png)
![True CAR_21 vs Placebo Distribution](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/sec-form-4-placebo-car21.png)

How to interpret this table?

1. **CAR is significantly non-zero**: The two-way clustered t reaches 2.41 at 1 day, which is statistically significant. However, the **mean CAR_1 is only +0.22%**, and this is **gross** excess return — a daily +0.22% annualized is considerable, but it does not deduct transaction costs, slippage, or taxes, and it is an equal-weight average of 4,476 signals.
2. **The gap between pooled t and two-way clustered t is an important warning**: The pooled t (4.8~7.9) is much larger than the two-way clustered t (1.3~2.4), indicating that the **inter-sample dependence caused by multiple increases by the same stock and increases by multiple stocks in the same month is very strong** — naively treating them as independent samples overestimates significance by nearly 2~4 times. However, this is also a direction for further factor exploration.
3. **Placebo did not cross the line**: Even though the pooled t for 1-day CAR is as high as 4.80 and the two-way t is 2.41, **the proportion of true CAR higher than the fake date panel is only 78.5%** (not reaching 95%). This indicates that **the information carried by the "timing" of the increase announcement itself is weaker than "this batch of stocks was already in a relatively strong momentum period."**

Objectively speaking, **we cannot say this factor has no Alpha**, but it is **not necessarily** an independent Alpha factor. It likely already resides within the momentum factor.

Since momentum factor calculation is simpler and data is more reliable, we do not need to use the method in this article to construct a factor. However, the CAR, pooled t, two-way clustered t, and placebo methods introduced in this article are very valuable in quantitative research — they help us **distinguish true signals from noise**.

# Do Insider Sell-offs Signal Short Opportunities?

This article tests whether insider sell-off announcements in China A-shares trigger negative abnormal returns or positive momentum, challenging the intuition that减持 equals bad news.

**Tags:** Factor Investing, Event Study, China A-Shares, Insider Trading

## Is a Sell-off a Sell Signal?

We previously posed a question: **If insider buying is a bullish signal implying a long position, why not treat insider selling as a bearish signal implying a short position?**

To address this, we conducted a preliminary event study using China A-share data to test whether stock prices actually fall after sell-off announcements as intuition might suggest. This is a distinct problem from buy-side research: when you see "CFO sells heavily," does the market treat it as "bad news" and dump the stock, or does it ignore it as "executive deleveraging"?

The conclusion is both surprising and, perhaps, logical.

### Hypothesis

> **Hypothesis H1 (Psychological Shock):** Sell-off announcements trigger retail investor panic, causing the cumulative abnormal return (CAR) of individual stocks to be **significantly negative** 1–5 days after the announcement.
>
> **Null Hypothesis:** Sell-offs are noise or already priced in, resulting in CARs near zero (pooled t-test shows no significance) after the announcement.

### Methodology (Preliminary)

- **Data:** `stk_holdertrade`, fetched in quarterly slices for 2022 (4 quarters × 3,000 rows max). Filtered for `in_de='DE'` (sell-off) and `holder_type` containing G (executives) or P (major individual shareholders)—signals closest to "insider psychological shock." Total: **2,173 signals** (stock × announcement date).
- **Matching:** Randomly sampled 300 signals; successfully matched to daily data for **183 signals**.
- **Event Study:** Entered positions on the first trading day after the announcement date (`ann_date`). Calculated cumulative CAR (`individual stock return − CSI 300 return`) over 1/5/21/63 days. Mean calculated via simple average, t-statistic = mean / (std/√n). **Note:** This is a preliminary pooled statistic, without two-way clustering (stock × month) or placebo tests.

### Results

| Horizon | Mean CAR | Median CAR | t     | n   | Hypothesis H1?                 |
| ------- | -------- | ---------- | ----- | --- | ------------------------------ |
| 1 Day   | +0.073%  | -0.163%    | 0.39  | 183 | Not Supported (H1 requires sig. neg.) |
| 5 Days  | +2.919%  | +2.582%    | 5.78  | 183 | Significantly Positive (**Refutes H1**) |
| 21 Days | +13.348% | +10.837%   | 11.31 | 183 | Significantly Positive (**Refutes H1**) |
| 63 Days | +11.646% | +9.117%    | 5.78  | 183 | Significantly Positive (**Refutes H1**) |

### Why Did Bad News Turn into Good News?

We did not perform stricter tests here—the t-values in the table above remain the most basic pooled t-statistics, without two-way clustering, placebo controls, or disclosure lag filtering. However, superficially, **sell-off announcements did not trigger a "psychological shock" decline; instead, they yielded significantly positive CARs.**

This may point to genuine "insider trading"—at least in terms of motive, those preparing to sell off have an incentive to pump the price before distributing shares. The topic may be sensitive, so readers are encouraged to investigate further.

## References

- Mikhail Makeev, *SEC Form 4 Insider Purchases in Python: A Filing-Date Event Study with Free EDGAR Data*, QuantInsti, 2026-08.
- SEC, [Form 4 and general instructions](https://www.sec.gov/files/form4data%2C0.pdf).
- SEC, [Insider Transactions Data Sets](https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets).
- Lakonishok & Lee (2001), *Are Insider Trades Informative?*, RFS.
- Cohen, Malloy & Pomorski (2012), *Decoding Inside Information*, JF.
- Cameron, Gelbach & Miller (2011), *Robust Inference With Multiway Clustering*, JBES.
- Tushare, [Shareholder Increase/Decrease (stk_holdertrade) API Documentation](https://tushare.pro/document/2?doc_id=170).
