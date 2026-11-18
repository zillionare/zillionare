---
title: "Zero Defaults, Still Wiped Out: The Truth About the Risk-Free Rate"
date: 2026-11-18
slug: en/posts/2026/11/what-is-rf
tags: [Risk-Free Rate, Duration Mismatch, Bond Yields, Asset Pricing]
excerpt: "In finance, \"risk-free\" means zero variance, not capital preservation. Even a 100% default-free government bond can bankrupt an institution once durations mismatch."
lang: en
translation_of: posts/2026/11/what-is-rf
auto_translated: true
source_sha: bdb1e3da77917dde1a465cdd26eb8e466e358aa5
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261118093646-what-is-rf.jpg"
---

We habitually treat government bond yields as the risk-free rate. So when the question arises — "is the risk-free rate really free of risk?" — it is natural to follow the literal reading and ask, "will the government default?" But stopping at default probability means we have not yet reached the most counterintuitive layer of finance: a government bond that carries a 100% guarantee of no default can still bankrupt an institution, and even a bond whose terms state in black and white that you will lose money at maturity is, in the language of finance, still a textbook risk-free asset.

The awkwardness comes from the fact that "risk" in everyday speech and "risk" in a pricing formula are simply not the same word.

## /01 In finance, "risk-free" means "zero variance"

For most people, the first reaction to "risk-free" is capital preservation, safety, a guaranteed profit. But in modern finance — from Markowitz's mean–variance model through to CAPM — risk is defined mathematically as the uncertainty of returns, i.e. variance $\sigma^2$. So in finance, "risk-free" does not mean "you cannot lose money"; it means "zero variance."

As long as an asset's nominal return at the end of a given holding period is fully known in advance and exhibits no fluctuation whatsoever ($\sigma = 0$) — and therefore by construction does not co-move with risky assets — the pricing models call it a "risk-free asset." Whether that certain outcome is actually a good deal is something the models simply do not care about.

The most absurd yet most rigorous proof of this played out in Europe in 2019–2020, when 10-year German and Swiss government yields briefly fell below $-0.5\%$. In other words, you lend the German government €100, hold it for ten years, and Berlin does not renege on a single cent — it hands you back roughly €95, exactly as the contract stipulates. By everyday intuition this is "a 100% guaranteed loss." Yet across the entire euro-area pricing system, that money-losing Bund remained the immovable benchmark for the "risk-free rate." Because for central banks, pension funds and insurers steering hundreds of billions, stacking physical cash in a vault carries steep security, counting and depreciation costs; paying a small "storage fee" in exchange for a sovereign promise that "in ten years you get exactly €95 back" is simply the lowest-uncertainty anchor they can find.

So what the risk-free rate genuinely promises is that the nominal return is beyond doubt — never that purchasing power is preserved.

## /02 Zero defaults do not save you from duration mismatch

Even back in a positive-rate world, is putting everything into "zero-default" government bonds absolutely safe? The 2023 collapse of Silicon Valley Bank is a textbook piece of dark comedy.

After vacuuming up deposits from tech companies, SVB did not go out and make risky loans, nor did it buy junk bonds. It behaved with extreme conservatism, allocating enormous sums to long-dated US Treasuries and agency mortgage-backed securities (MBS). Judged purely on credit default risk, this was about the safest portfolio in the dollar universe.

Then the Fed launched its aggressive hiking cycle, yields on newly issued Treasuries soared, and the market price of SVB's book of low-coupon legacy Treasuries fell sharply. Had SVB been able to hold those bonds to maturity, the US Treasury would of course have paid principal and interest in full; but depositors withdrew en masse, the bank was forced to sell bonds at a loss before maturity to raise cash, paper losses turned into hard realized losses overnight, and within 48 hours a run had killed the bank.

This tears away the harsh precondition buried inside "risk-free": the risk-free label on a government bond holds only for money that can be held strictly to maturity and never forcibly liquidated in between (and pushed to its logical extreme, only for zero-coupon bonds whose duration exactly matches the holding period — otherwise even the rate at which interim coupons get reinvested is uncertain). Once the holding period mismatches asset duration, the interest-rate and liquidity risk of a zero-default asset is every bit as lethal.

## /03 So how do we actually pick the "risk-free rate"?

This is a good moment to clear up a common misunderstanding in domestic discussions. Some argue that because China's government bond issuance quota is limited and gets snapped up by retail savers the moment it hits the market, the only workable proxy in China is the 1-year bank deposit rate.

That conflates savings bonds sold over the bank counter to individuals with book-entry government bonds traded in the interbank market. In real financial and quantitative practice, posted bank deposit rates are rigid for long stretches and reflect the true opportunity cost of market funding poorly; book-entry government bonds, by contrast, trade in enormous daily cash-bond volume in the interbank market, and the ChinaBond government bond yield curve compiled from them is the core risk-free benchmark for domestic asset pricing.

In my courses *Factor Analysis and Machine Learning Strategies* and *Twenty-Four Lessons in Quantitative Investing*, I built a programming exercise that computes CAPM and Jensen's Alpha from scratch: take any CSI 300 constituent, combine the past year of CSI 300 index returns with the risk-free rate, regress out the risk coefficient $\beta$, then compute the risk-adjusted benchmark return and the excess return $\alpha$.

When it comes to actually writing the code that fetches the risk-free rate, the object we pull is precisely the ChinaBond government bond yield curve:

```python
import akshare as ak
import arrow

end = arrow.get('2023-12-31')
start = end.shift(years=-1)

# 获取过去一年的中债收益率曲线数据
bond = ak.bond_china_yield(
    start_date=start.format('YYYYMMDD'),
    end_date=end.format('YYYYMMDD')
)
bond.set_index(keys='曲线名称', inplace=True)

# 提取“中债国债收益率曲线”1年期收益率均值作为区间无风险利率近似
rf = bond.loc['中债国债收益率曲线', '1年'].mean() / 100
assert abs(rf - 0.021) < 1e-3  # 2023年1年期国债收益率均值约为2.1%
```

Plot that data and the temper of the whole curve becomes obvious at a glance. In 2023 the long end was a textbook bull market: the 10-year yield slid one-way from 2.82% at the start of the year to 2.56% at year-end, a cumulative decline of roughly 27bp, touching a 2023 low of 2.54% on August 21. The 30-year fell in tandem from 3.19% to 2.83%, about 37bp. The short end told a completely different story: the 1-year yield dropped to 1.73% on July 24, was shoved back up by quarter-end funding conditions and negotiable certificate of deposit rates, then spiked to 2.40% on December 6 — a full-year amplitude of nearly 66bp, far larger than the 10-year's entire annual decline. The result was a 10y–1y term spread that kept getting compressed and yanked back and forth: roughly 71bp at the start of the year, squeezed to just 48bp by year-end, and narrowing to as little as 26bp at its tightest. A long end in structural decline and a short end whipped around by funding conditions — that is the real-world footnote to every duration-mismatch discussion that follows.

![ChinaBond government bond yield curve in 2023: key tenors, monthly curve families and a term-structure heatmap](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/11/20261118154000-cbond-yield-2023.png)

Once you actually run this code, your understanding of the "risk-free rate" snaps from a textbook concept into something concrete, and at least two things become clear.

First, the risk-free rate must be aligned with the horizon over which you are evaluating the investment. For long-horizon corporate DCF valuation, institutions typically anchor to the 10-year government yield; but in the Alpha attribution exercise above, with its 1-year backtest window, we pull the `'1年'` (1-year) government yield. Misalign the tenor and the yardstick itself distorts — SVB's downfall was, at bottom, a downfall of duration mismatch.

Second, even pinning down a single $R_f$ in code involves an engineering approximation. Open the `bond` table and you will see the "1-year government yield" jumping around every single day in 2023. In code, do you lock in the 1-year yield at the start of the period, average it over the full year as we do above, or feed the daily risk-free rate day by day into the excess return series $R_{i,t} - R_{f,t}$ for the regression? In that course's exercise we compared four different ways of computing Alpha, and you will find that merely changing how $R_f$ enters the calculation and how annualization is handled produces subtle differences in the resulting $\beta$ and $\alpha$. Never mind that CSI 300 returns were actually negative in 2023, so plugging into $R_f + \beta (R_m - R_f)$ yields an ex-post performance attribution benchmark, not the positive expected return CAPM implies ex ante.

So even in the most precision-obsessed quantitative models, the "risk-free rate" is never a constant that exists absolutely, independent of tenor and of pricing convention.

## /04 Does an "absolutely risk-free" asset exist at all?

Which naturally leads to a deeper question: if even government bonds carry interest-rate volatility and duration-mismatch risk, does an "absolutely risk-free" asset exist anywhere in the world?

It depends on whose perspective you take. From the standpoint of a large government with independent monetary sovereignty, local-currency government bonds can indeed come arbitrarily close to absolutely default-free when it comes to "nominal principal and interest repayment." Russia's 1998 default and Latin America's repeated sovereign defaults typically stemmed from borrowing in foreign currency they could not print; for local-currency debt, former Fed Chair Greenspan, responding to a US debt-rating scare, put it bluntly: the US government can always repay any local-currency obligation, because it can always print the money — the default probability is zero. How much purchasing power that money will still have by then is another matter entirely.

In other words, sovereign local-currency debt achieves "nominal zero default" not because the risk has vanished into thin air, but because the state apparatus uses monetary sovereignty to translate credit default risk into inflation-dilution risk shared collectively by everyone holding the currency.

So there is no point searching the real world for an absolutely risk-free asset that "never loses money, never loses purchasing power, and can be liquidated at any moment without a price drop" — such a thing is logically impossible. The "risk-free rate" is really nothing more than a zero mark that finance calibrates artificially, by temporarily stripping out default and return volatility, so that it has a baseline against which to account for every shifting risky asset.
