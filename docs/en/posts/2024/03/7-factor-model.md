---
title: "Fung & Hsieh 7-Factor Model: Beyond Market, Size and Momentum"
date: 2024-03-26
slug: en/posts/factor-strategy/7-factor-model
tags: [Factor Investing, Hedge Funds, Multi-Factor Model]
excerpt: "Fung and Hsieh's 7-factor model extends beyond market, size, value and momentum with trend-following and bond factors. This article breaks down all seven factors and China's adapted 8-factor version."
lang: en
translation_of: posts/factor-strategy/7-factor-model
auto_translated: true
source_sha: 791dce9bbabe80c9dee4076a0af138300f8bf567
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/duke.jpg"
---

This post was prompted by a reader question: beyond market, size, value and momentum, what are the other factors in the seven-factor model? It's the perfect excuse to introduce the Fung & Hsieh seven-factor model.

The seven-factor model usually refers to the 7-factor model proposed by David Hsieh and William Fung in their 2004 paper, *Hedge Fund Benchmarks: A Risk Based Approach*.

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/david-hsieh.jpg)
David Hsieh, pictured above, was born in Hong Kong and is a professor at Duke University with deep and wide-ranging research on hedge funds and alternative beta. William Fung is a visiting professor at the Centre for Hedge Fund Education and Research at London Business School.

Since publication, the paper has been cited more than 1,300 times. It also earned the authors the CFA Institute's Graham and Dodd Award and the Fischer Black Memorial Foundation Award, among other honors. It holds an important place in quant history and is well worth studying.

In [this paper](/assets/ebooks/Hedge-Fund-Benchmarks-A-Risk-Based-Approach.pdf), the 7-factor model consists of the following seven:

1. Bond Trend-Following Factor
2. Currency Trend-Following Factor
3. Commodity Trend-Following Factor
4. Equity Market Factor
5. The Equity Size Spread Factor
6. The Bond Market Factor
7. The Bond Size Spread Factor

Among them, the equity market factor and the size-spread factor are essentially the market factor and the size factor.

The first three factors come from another paper by Fung and Hsieh, *The Risk in Hedge Fund Strategies: Theory and Evidence from Trend Followers*. A few years after that paper was published, Fung and Hsieh added an eighth factor, the MSCI Emerging Markets Index.

The paper also discusses several common biases in hedge fund research, which are worth highlighting here.

!!! tip
    In investing, understanding what is wrong and how it goes wrong may matter more than knowing what is right. After all, only sound methods and methodology keep working over time, while so-called "correct conclusions" are always products of a specific time and place.

The first bias in hedge fund research is selection bias. Mutual funds must publicly disclose their investment activities, but hedge funds do not. Hedge fund data is typically collected by vendors, and that collection process can introduce selection bias, so the funds in a database may not be a representative sample of the full universe.

Second is survivorship bias. This is a common issue in all fund research. As we cover in our course, stock listings and delistings follow strict rules, and historical data remains readily available even after a company delists. Defunct funds, however, are typically dropped from databases. This point is raised here and in many other papers.

The third bias is instant history bias. When a fund enters a database, it backfills its past track record, even though that record was created during its incubation period. And if performance during incubation is not good enough, the fund is often shut down. Clearly, such track records are not fully reliable.

Avoiding various systematic biases in quantitative research is an important skill. That expertise does not come from academic research alone — it requires understanding the full process from data collection to processing. Since few people can observe that pipeline directly, industry exchange is essential.

Back to the original question: beyond market, size, value and momentum, what are the other factors in the seven-factor model? The question likely stems from an 8-factor model widely used for domestic private funds in China.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/20240326193718.png)

This model was disclosed by Tsinghua University's National Institute of Financial Research in a March 2017 briefing ([Risk Factor Analysis for Chinese Private Funds](/assets/ebooks/中国私募基金风险因子分析.pdf)). Drawing on Fung and Hsieh's 7-factor model, it proposes eight factors:

1. Equity market risk factor (MKT)
2. size factor (SMB)
3. value factor (HML)
4. momentum factor (MOM)
5. Bond factor (BOND10)
6. Credit risk factor (CBMB10)
7. Aggregate bond market factor (BOND_RET)
8. Commodity market risk factor

As you can see, this 8-factor model starts from the classic Fama-French three factors — market, size, and value — adds the momentum factor (Jegadeesh and Titman), and combines them with several factors from Fung and Hsieh's seven-factor set.

In this model, the equity market risk factor is defined as:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/mkt-factor.png)

$RET_HS300_t$ is the monthly return of the CSI 300 in month $t$, and $RF_t$ is the monthly rate implied by the 1-year time-deposit rate in month $t$. This choice is somewhat surprising — government bonds are generally safer than bank deposits (large deposits are only insured up to RMB 500,000) and yield a bit more, so Treasury yields are more commonly used as the risk-free rate.

Its size factor is built with annual rebalancing. The portfolio is formed once a year at the end of June: China A-shares are divided by grouping into small-cap and large-cap groups by free-float market cap. Stocks are then ranked by book-to-market ratio calculated from T-1 annual reports and free-float market cap (ME) into growth, neutral, and value groups in 30%, 40%, 30% proportions. Finally, the two groupings are intersected to form six groups, and the monthly return is calculated for each group.

Its value factor and momentum factor are constructed in a similar way to the size factor.

The bond factor is defined as:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/bond10.jpg)

The credit risk factor is:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/cbmb10.jpg)

The aggregate bond market factor is:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/03/bond_ret.jpg)

It uses the ChinaBond Composite Full-Price Index. Although only ten pages long, the note explains factor construction in considerable detail — well worth reading if you are interested.

The cover image shows Duke University's landmark — Duke Chapel. I once drove past Duke and thought, ah, so this is Duke — a pity I hadn't planned ahead and couldn't go in for a visit.

Since CAPM and APT, factors have been proposed in an endless stream, creating the so-called factor zoo. With so many factors, how should you study them and map out their lineage? Beginners can easily feel lost. We have put together a systematic quant course (*Quant in 24 Lessons*) and are about to launch a new course on factor analysis and machine learning strategies — feel free to get in touch. Enroll in *Quant in 24 Lessons* now and get a free upgrade to the Factor Analysis and Machine Learning Strategies course.

Links to download the two papers mentioned above can be found [here](https://blog.quantide.cn/blog/2024/03/26/what-is-7-factor-model/).
