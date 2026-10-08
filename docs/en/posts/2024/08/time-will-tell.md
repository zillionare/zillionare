---
title: "First Movers: Exploiting Early Earnings Announcements in China A-Shares ===EXCUT=== This article explores the alpha from early annual report disclosures in China A-shares, adapting academic findings on earnings timing to a sector-neutral, multi-stock strategy for live trading. ===TAGS=== Factor Investing, Earnings Timing, China A-Shares, Quantitative Strategy ===BODY=== Cover: Engineering Fountain at Purdue University. Purdue is located in Indiana, 100 miles from Chicago, ranked 89th globally by QS. Its motto, \"Every giant leap starts with one small step,\" reflects the principle that no journey begins without the first step.  ---  !!! quote     A handful of sweet wormwood, soaked in two liters of water, wrung for juice, and consumed entirely.      This is ancient empirical knowledge. However, lacking a grasp of the underlying mechanisms, these methods were inconsistent and never became the mainstream treatment for malaria. In 1972, Tu Youyou isolated artemisinin monomers from sweet wormwood, discovering a stable and effective drug preparation method. In 1982, Roche completed the first total synthesis of artemisinin using menthol as a raw material, marking humanity’s complete mastery of malaria treatment.      I value these conventional wisdoms, but I apply the scientific method to re-evaluate them all.  Many years ago, before I entered the quantitative finance field, a friend shared his money-making strategy: trade stocks only once a year by buying the company that discloses its annual report first, aiming for a ~20% return before exiting.  He was not a professional investor and still needed to work to support his family, so I merely remembered this strategy and never implemented it.  However, recent papers have empirically validated this strategy, or similar ones. In this article, we first introduce these papers, then extend the strategy slightly to adapt it to the domestic market.  ---  ## Research on Earnings Announcement Timing  Since the 1980s, William Kross and others have conducted continuous research on earnings announcement timing.  In 1981, William Kross, then at Purdue University (now a Distinguished Professor Emeritus at the University at Buffalo, SUNY), published *Earnings and Announcement Time Lags*. After studying 108 companies (filtered from an initial sample of 200) with 432 observations, he concluded:  !!! quote     Consistent with widespread consensus, it can be stated with certainty that the later the earnings are released, the more likely they contain bad news. If the actual release date is one week or more later than the forecasted date, the signal is stronger.  Research in this area has continued and intensified since then.  In 1999, Mark Bagnoi, also a Distinguished Professor Emeritus from Purdue University, published *A Day Late, A Penny Short*, further concluding that if a company misses its scheduled earnings release date, the unexpected return per share decreases by approximately one cent for every day of delay.  ---  Bagnoi used data from First Call, which also revealed other interesting trends, such as companies becoming more accurate in their earnings release dates. In 1995, only 59% of companies released earnings on the scheduled date, whereas this figure rose to 80% in 1998.<remark>Clearly, this is closely related to advancements in IT technology.</remark>  In 2018, Travis L. Johnson published *\"Time Will Tell: Information in the Timing of Scheduled Earnings News\"* in the *Journal of Financial and Quantitative Analysis*, elevating this research to new heights. The 63-page paper is rich in content. Since its publication in 2018, it has been cited 99 times, gaining significant academic recognition.  Travis L. Johnson is from the University of Texas at Austin, founded in 1883 as the flagship institution of the University of Texas System and renowned as a \"Public Ivy,\" meaning its academic standards and educational quality rival those of the Ivy League. UT Austin enjoys high prestige across multiple disciplines, with its business and engineering schools particularly notable; its accounting program ranked first in the U.S. for many consecutive years.  Previous articles primarily examined how deviations between actual and forecasted earnings release dates impact future return predictions.  Johnson’s paper investigates whether the forecasted release date itself carries a signal. If such a signal exists, its investment implications are significantly greater, as investors can react in advance. Naturally, this research is more challenging, making the paper’s methodology more instructive than its conclusions.  Johnson’s conclusion is that the forecasted earnings release date predicts corporate earnings news, but the market often waits until the actual announcement to react. This indicates the market is not strongly efficient, providing sufficient time for arbitrage.  !!! info     Johnson is not the final \"king\" of this series. On quant.stackexchange.com, a question arises: If I have the exact timing (down to the millisecond) of all earnings announcements over the past 10 years, can I reasonably predict the specific timing of the next earnings release? Perhaps related to machine learning?  ## Adapting the Strategy to the Market  In summary, these papers highlight two points:  1. The forecasted earnings release date generally signals earnings news. 2. The later the actual release date, the more likely it indicates bad news.  Regarding point 2, let us extend it appropriately. The papers study cases where companies fail to meet their pre-announced schedules, implying failure or bad news.  What if a company does not pre-announce an earnings release schedule?  If you are not decent, the system will make you decent. In both U.S. and China A-shares, there is a predetermined \"release deadline\": earnings must be released within a certain number of days after the fiscal year ends.  In China A-shares, forecast deadlines vary by board and profitability. Some companies are not required to issue forecasts and can simply release reports by April 30.  Thus, we treat this deadline as the forecast date. The later the release, the greater the corporate governance issues and the more likely it hides bad news; conversely, earlier releases signal good news.  !!! tip     Of course, earnings forecasts can be either positive (pre-happiness) or negative (pre-loss).  Driven by performance chasing or the desire to be first, companies that release annual report forecasts earliest often attract capital追捧 (pursuit).  Furthermore, this strategy implicitly involves \"market timing\"—since the earliest annual report forecasts are often released before the Spring Festival, and statistics show that 80% of A-share thematic rallies occur during the Spring Festival period.  This is the fundamental reason my friend’s strategy generates profits.  However, we can slightly refine this strategy to enhance robustness. Specifically, within each Shenwan Level 1 industry, buy the company that releases its earnings forecast earliest, holding positions in approximately 10 industries. There is no need to hold more, as not all industries generate profits.  If anyone likes this strategy, I will next write about how to automatically fetch company earnings forecasts. 😁  As per tradition, the papers mentioned in this issue will be shared in the group."
date: 2024-08-08
slug: en/posts/factor-strategy/time-will-tell
tags: [Factor Investing, Earnings Timing, China A-Shares, Quantitative Strategy]
excerpt: ""
lang: en
translation_of: posts/factor-strategy/time-will-tell
auto_translated: true
source_sha: d77b9b7a1554e771357a11bd54a9cfe3d905635d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/purdue-engfountain.jpg"
---

Cover: Engineering Fountain at Purdue University. Purdue is located in Indiana, 100 miles from Chicago, ranked 89th globally by QS. Its motto, "Every giant leap starts with one small step," reflects the principle that no journey begins without the first step.

---

!!! quote
    A handful of sweet wormwood, soaked in two liters of water, wrung for juice, and consumed entirely.

    This is ancient empirical knowledge. However, lacking a grasp of the underlying mechanisms, these methods were inconsistent and never became the mainstream treatment for malaria. In 1972, Tu Youyou isolated artemisinin monomers from sweet wormwood, discovering a stable and effective drug preparation method. In 1982, Roche completed the first total synthesis of artemisinin using menthol as a raw material, marking humanity’s complete mastery of malaria treatment.

    I value these conventional wisdoms, but I apply the scientific method to re-evaluate them all.

Many years ago, before I entered the quantitative finance field, a friend shared his money-making strategy: trade stocks only once a year by buying the company that discloses its annual report first, aiming for a ~20% return before exiting.

He was not a professional investor and still needed to work to support his family, so I merely remembered this strategy and never implemented it.

However, recent papers have empirically validated this strategy, or similar ones. In this article, we first introduce these papers, then extend the strategy slightly to adapt it to the domestic market.

---

## Research on Earnings Announcement Timing

Since the 1980s, William Kross and others have conducted continuous research on earnings announcement timing.

In 1981, William Kross, then at Purdue University (now a Distinguished Professor Emeritus at the University at Buffalo, SUNY), published *Earnings and Announcement Time Lags*. After studying 108 companies (filtered from an initial sample of 200) with 432 observations, he concluded:

!!! quote
    Consistent with widespread consensus, it can be stated with certainty that the later the earnings are released, the more likely they contain bad news. If the actual release date is one week or more later than the forecasted date, the signal is stronger.

Research in this area has continued and intensified since then.

In 1999, Mark Bagnoi, also a Distinguished Professor Emeritus from Purdue University, published *A Day Late, A Penny Short*, further concluding that if a company misses its scheduled earnings release date, the unexpected return per share decreases by approximately one cent for every day of delay.

---

Bagnoi used data from First Call, which also revealed other interesting trends, such as companies becoming more accurate in their earnings release dates. In 1995, only 59% of companies released earnings on the scheduled date, whereas this figure rose to 80% in 1998.<remark>Clearly, this is closely related to advancements in IT technology.</remark>

In 2018, Travis L. Johnson published *"Time Will Tell: Information in the Timing of Scheduled Earnings News"* in the *Journal of Financial and Quantitative Analysis*, elevating this research to new heights. The 63-page paper is rich in content. Since its publication in 2018, it has been cited 99 times, gaining significant academic recognition.

Travis L. Johnson is from the University of Texas at Austin, founded in 1883 as the flagship institution of the University of Texas System and renowned as a "Public Ivy," meaning its academic standards and educational quality rival those of the Ivy League. UT Austin enjoys high prestige across multiple disciplines, with its business and engineering schools particularly notable; its accounting program ranked first in the U.S. for many consecutive years.

Previous articles primarily examined how deviations between actual and forecasted earnings release dates impact future return predictions.

Johnson’s paper investigates whether the forecasted release date itself carries a signal. If such a signal exists, its investment implications are significantly greater, as investors can react in advance. Naturally, this research is more challenging, making the paper’s methodology more instructive than its conclusions.

Johnson’s conclusion is that the forecasted earnings release date predicts corporate earnings news, but the market often waits until the actual announcement to react. This indicates the market is not strongly efficient, providing sufficient time for arbitrage.

!!! info
    Johnson is not the final "king" of this series. On quant.stackexchange.com, a question arises: If I have the exact timing (down to the millisecond) of all earnings announcements over the past 10 years, can I reasonably predict the specific timing of the next earnings release? Perhaps related to machine learning?

## Adapting the Strategy to the Market

In summary, these papers highlight two points:

1. The forecasted earnings release date generally signals earnings news.
2. The later the actual release date, the more likely it indicates bad news.

Regarding point 2, let us extend it appropriately. The papers study cases where companies fail to meet their pre-announced schedules, implying failure or bad news.

What if a company does not pre-announce an earnings release schedule?

If you are not decent, the system will make you decent. In both U.S. and China A-shares, there is a predetermined "release deadline": earnings must be released within a certain number of days after the fiscal year ends.

In China A-shares, forecast deadlines vary by board and profitability. Some companies are not required to issue forecasts and can simply release reports by April 30.

Thus, we treat this deadline as the forecast date. The later the release, the greater the corporate governance issues and the more likely it hides bad news; conversely, earlier releases signal good news.

!!! tip
    Of course, earnings forecasts can be either positive (pre-happiness) or negative (pre-loss).

Driven by performance chasing or the desire to be first, companies that release annual report forecasts earliest often attract capital追捧 (pursuit).

Furthermore, this strategy implicitly involves "market timing"—since the earliest annual report forecasts are often released before the Spring Festival, and statistics show that 80% of A-share thematic rallies occur during the Spring Festival period.

This is the fundamental reason my friend’s strategy generates profits.

However, we can slightly refine this strategy to enhance robustness. Specifically, within each Shenwan Level 1 industry, buy the company that releases its earnings forecast earliest, holding positions in approximately 10 industries. There is no need to hold more, as not all industries generate profits.

If anyone likes this strategy, I will next write about how to automatically fetch company earnings forecasts. 😁

As per tradition, the papers mentioned in this issue will be shared in the group.
