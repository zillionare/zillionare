---
title: "First Movers: Why Early Earnings Announcements Signal Alpha"
date: 2024-08-08
slug: en/posts/factor-strategy/time-will-tell
tags: [Factor Investing, Earnings Announcement, Market Efficiency, Quantitative Trading]
excerpt: "Research confirms that early earnings announcements signal positive news, while delays indicate bad news. This article explores the \"first-mover\" strategy in China A-shares, adapting academic findings on announcement timing to live trading for potential excess returns."
lang: en
translation_of: posts/factor-strategy/time-will-tell
auto_translated: true
source_sha: d77b9b7a1554e771357a11bd54a9cfe3d905635d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/purdue-engfountain.jpg"
---

Cover image: Engineering Fountain at Purdue University. Purdue is located in Indiana, 100 miles from Chicago, ranked 89th globally by QS. Its motto, "Every giant leap starts with one small step," reminds us that no journey begins without a single step.

---

!!! quote
    A handful of artemisia, soaked in two liters of water, wrung for its juice, and consumed entirely.

    This is ancient empirical knowledge. However, lacking a grasp of the underlying laws, these methods were inconsistent and never became the mainstream approach for treating malaria. In 1972, Tu Youyou isolated the artemisinin monomer from sweet wormwood, discovering a stable and effective drug preparation method. In 1982, Roche completed the first total synthesis of artemisinin using menthol as a raw material, marking humanity’s complete mastery of malaria treatment.

    I appreciate these conventional wisdoms, but I apply the scientific method to re-examine them all.

Many years ago, before I entered the quantitative finance field, a friend shared his money-making strategy: trade stocks only once a year by buying the company that discloses its annual report first, aiming for a ~20% return before exiting.

He was not a professional investor and still needed his day job to support his family. Thus, I merely remembered this strategy and never implemented it.

Recently, however, I read several papers empirically validating this strategy, or similar ones. In this article, we first introduce these papers, and then I will propose a minor extension to adapt this strategy to the domestic market.

---

## Research on Earnings Announcement Timing

Since the 1980s, researchers like William Kross have conducted sustained studies on earnings announcement timing.

In 1981, William Kross, then at Purdue University (now a Distinguished Professor Emeritus at the University at Buffalo, SUNY), published *Earnings and Announcement Time Lags*. After analyzing 108 companies (filtered from an initial sample of 200) and 432 observations, he reached the following conclusion:

!!! quote
    Consistent with widespread consensus, it is certain that the later the earnings are released, the more likely they contain bad news. If the actual release date is one week or more later than the forecasted date, the signaling effect becomes stronger.

Research in this area has continued and intensified since then.

In 1999, Mark Bagnoi, also a Distinguished Professor Emeritus from Purdue University, published *A Day Late, A Penny Short*, further concluding that if a company announces an earnings release date but misses it, the unexpected return per share decreases by approximately one cent for each day of delay.

---

Bagnoi used data from First Call, which revealed other interesting trends, such as companies becoming more accurate in announcing their release dates. In 1995, only 59% of companies released earnings on the announced date, whereas by 1998, this proportion had risen to 80%.<remark>Obviously, this is closely related to advancements in IT technology.</remark>

In 2018, Travis L. Johnson published *Time Will Tell: Information in the Timing of Scheduled Earnings News* in the *Journal of Financial and Quantitative Analysis*, elevating this research to new heights. The 63-page paper is rich in content. Since its publication in 2018, it has been cited 99 times, indicating strong academic recognition.

Travis L. Johnson is from the University of Texas at Austin, founded in 1883 as the flagship institution of the University of Texas System and renowned as a "Public Ivy," meaning its academic standards and educational quality rival those of the Ivy League. UT Austin enjoys high prestige across multiple disciplines, particularly in business and engineering, with its accounting program ranking first in the nation for many consecutive years.

Previous studies primarily examined how deviations between the actual announcement date and the forecasted date impact future return predictions.

Johnson’s paper investigates whether the *forecasted* announcement date itself carries signaling value. If such a signal exists, its impact on investment would be significant, as investors can react in advance. Naturally, this research is more challenging, making the paper highly academic. Its methodology is arguably more valuable than its conclusions.

Johnson concludes that the forecasted announcement date predicts corporate earnings news, but the market often waits until the actual announcement to react. This implies the market is not strongly efficient, providing sufficient time for arbitrage.

!!! info
    Johnson is not the final "champion" of this series. On quant.stackexchange.com, a question arises: If I have the exact timing (down to the millisecond) of all earnings announcements over the past 10 years, can I reasonably predict the specific timing of the next earnings release? Perhaps related to machine learning?

## Adapting the Strategy to the Market

In summary, these papers highlight two points:

1. The forecasted earnings announcement date generally implies positive earnings news.
2. The more the actual release date is delayed, the more likely it is bad news.

Regarding point 2, let’s extend it slightly. The papers study cases where a company provides a scheduled release date but fails to meet it, implying failure or bad news.

What if a company does not provide a scheduled release date in advance?

If you are not decent, the system will make you decent. Both in US and China A-shares, there is an implicit "release date," defined by the deadline for reporting after the fiscal year ends.

In China A-shares, forecast deadlines vary by board and profitability. Some companies are not required to issue forecasts and can simply release reports by April 30.

Therefore, we treat this deadline as the forecast date. The later the release, the greater the corporate governance issues and the more likely it hides bad news; conversely, earlier releases signal good news.

!!! tip
    Note that earnings forecasts can be either positive (pre-joy) or negative (pre-loss).

Driven by performance chasing or the desire to be first, companies that release annual report forecasts earliest often attract capital追捧 (pursuit).

Additionally, this strategy implicitly involves "market timing," as the earliest annual report forecasts are often released before the Spring Festival. Statistically, 80% of concept-driven rallies in China A-shares occur during the Spring Festival period.

This is the fundamental reason why my friend’s strategy generates profits.

However, we can slightly refine this strategy to enhance its robustness. Specifically, within each Shenwan Level I industry, we buy the company that releases its earnings forecast first, holding positions across approximately 10 industries. There is no need to hold more, as not all industries generate profits.

If anyone is interested in this strategy, I will next write about how to automatically fetch company earnings forecasts. 😁

As per tradition, the papers mentioned in this issue will be shared in the group.
