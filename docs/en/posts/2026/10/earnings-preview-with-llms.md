---
title: "Why Good News Doesn't Lift Stocks: AI Earnings Prediction Contest"
date: 2026-10-01
slug: en/posts/tools/earnings-preview-with-llms
tags: [Factor Investing, Machine Learning, Quantitative Trading]
excerpt: "Optiver and UChicago test AI systems predicting stock reactions to earnings. Using R², they reveal that understanding market expectations, not just model strength, is key to explaining why good news fails to lift prices."
lang: en
translation_of: posts/tools/earnings-preview-with-llms
auto_translated: true
source_sha: ed9157ba40c214886108f925e574ca832f8a5b48
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261001095444-earnings-preview-with-llms.jpg"
---

The market on today (September 30) was volatile and erratic. On the news front, a major interest-rate subsidy policy was released the night before, theoretically a positive for the real estate sector. Yet, the relevant sectors opened lower and fell, dropping as much as 4.35% at one point. Fortunately, they dipped first and rose later, closing up 0.91%.

Obviously, we must ask: why does good news lead to a lower open and decline? Is this the so-called "good news is bad news" upon realization?

This is a problem quantitative research has long sought to solve. Of course, the policy response in China A-shares is not the same mechanism as the earnings response in US stocks. This article merely borrows the question "why doesn't good news lift prices" to discuss the issue.

Today, we introduce a platform launched by Optiver in collaboration with University of Chicago researchers (Ralph & Bradford): explainingmarkets.ai. It is hosting a public competition for global participants: **participants build AI systems to predict stock reactions to earnings announcements and face real-market results for verification.**

From the organizer's side, the platform's researchers also conducted a set of control experiments: using three OpenAI models—GPT-6 Luna, Sol, and Astra—to test how much different data inputs can improve the "AI's ability to explain earnings reactions."

Ralph S. J. Koijen and Bradford (Lynch) Levy are both from the University of Chicago Booth School of Business. The competition is based on the benchmark proposed in their co-authored working paper, *Assessing the Benefits of Optimized Agentic AI Systems for Asset Pricing*, and comes with an SDK for researchers to evaluate AI systems under real-time, out-of-sample standards.

The University of Chicago is the Mecca for global economists, the birthplace of the Chicago School, which has profoundly shaped the landscape of modern economics.

## /01 The Old Question: Why Do Stocks Fall When Earnings Beat Expectations?

Every earnings season, traders encounter this scene: a company's revenue, profit, and next-quarter guidance all exceed analyst expectations, yet the stock price drops the next day.

Nvidia is a typical example. According to the Explaining Markets blog, prior to Nvidia's earnings report in August 2026, it had exceeded expectations in revenue, EPS, and next-quarter guidance for four consecutive quarters. Yet, each time triggered a next-day stock price drop, with an average beat magnitude of about 4.8%.

This indicates that stock prices do not reflect "good news," but rather "news better than expected." But what exactly are expectations? They are hard to quantify and even harder for AI to understand.

## /02 Explaining Markets: A Global "AI System" Competition

The participation process has three steps:

1. **Build and Connect.** Download the example Notebook or use the official launch template based on the Modal cloud platform to set up your agent and connect to the platform. The official site claims most people can get running within 30 minutes.
2. **Receive Real-Time Events.** When a company releases earnings, your agent receives a summary of key points from the earnings call and submits a prediction before the deadline.
3. **Track Performance.** Each prediction is compared with actual market performance, and scores are updated on a public leaderboard.

For each event, the agent submits a number between 0 and 1, representing its expectation of the stock's market reaction relative to the percentile of all earnings announcements in that quarter: 0 is the most negative, 0.5 is median, and 1 is the most positive. It tests relative ranking, not the specific magnitude of price changes. Each event is judged by the first valid submission; late submissions, format errors, or out-of-bounds values count as misses. Missed events are filled in by the organizers using your average prediction, so skipping is not cost-effective.

The platform uses $R^2$ to measure the fit between predictions and actual returns, which can be understood as "the proportion of return variance explained by the prediction." The leaderboard provides three numbers for each agent:

- The baseline $R^2$ using only "earnings beat";
- The full model $R^2$ including the agent's prediction;
- The difference $\Delta R^2$, i.e., how much more variance the prediction explains compared to "just looking at earnings beats."

The quarterly leaderboard is ranked by $\Delta R^2$, while the prize ranking is calculated based on $\Delta R^2$ across all scored events. The scoring logic is fully open in the example repository.

Anyone can participate, including students, researchers, engineers, and independent developers, with no financial background required—just Python skills. There is no registration fee; costs depend mainly on which models are called and how frequently. The official site states that the total budget for Koijen and Levy's paper was less than $10. Each account can submit up to 5 agents, with up to 10 members per agent.

The top five share a total of $7,500 ($2,500, $2,000, $1,500, $1,000, $500), funded by Optiver and distributed by the University of Chicago.

## /03 What Are Participants Competing On?

All participants receive the same official materials: each event is pushed via the platform interface with an information package for that event, the core of which is the summary of key points from the earnings call.

The rules do not limit models or tools, nor do they restrict you from supplementing data, **provided that no information after the event's "knowledge cutoff" is used.** This restriction covers the entire process of data collection, prompting, retrieval, external search, manual research, and manual adjustment. Market signals such as prices, volumes, and options data after the cutoff cannot be used unless provided by the official interface. Violators are ineligible for prizes, may be publicly flagged or removed from the leaderboard, and winners may be required to provide logs, timestamps, and other records, potentially undergoing audits.

Thus, differences can only come from participants' own methods: how to design prompts and reasoning flows, which models to choose, what pre-cutoff public data to supplement, and how to handle official materials. Look-ahead bias is the primary concern this benchmark seeks to avoid, which is exactly why the rules are so strict. Participants do not need to publish code or prompts, only a high-level method description.

As of September 30, the full model $R^2$ for the top three on the Q3 season leaderboard was 26.5%, 26.1%, and 26.0%, with a baseline $R^2$ of 9.7%, and $\Delta R^2$ values of 0.168, 0.164, and 0.162, respectively. The scoring period for this season does not end until October 2, so these are preliminary results and will only count after eligibility and compliance verification.

## /04 Experiment One: Let AI Read Earnings Calls

In addition to the competition, **the organizers are also conducting data experiments** to decide which new data sources to add to each season's competition. These new sources are believed to improve the explanatory power of participants' models.

!!! tip
    In a sense, you can consider that through this competition, top-tier funds and economists have provided their latest research directions for LLM factor mining. Readers might consider applying these findings to other competitions, such as the WorldQuant ranking contest, potentially uncovering new Alpha.

The baseline is earnings surprise (Earnings Surprise), the gap between actual performance and analyst consensus. In the most recent earnings season (Q3 2026), relying solely on earnings surprise, $R^2$ was approximately **10%**, slightly higher than previous quarters, but still leaving about 90% of the variance unexplained.

Beyond numbers, there is information. The organizers extracted structured facts from earnings calls and fed them to three OpenAI models: Luna (smallest), Sol, and Astra (strongest). Taking Nvidia as an example, the extracted key points included:

- Q2 revenue hit a record high of $96 billion;
- Q3 revenue guidance is $108 billion ($\pm$2%);
- Gross margin was lowered due to rising storage prices, approximately 74% in Q3, bottoming out at 71%–72% in Q4;
- Data center revenue was $89 billion, a 18% quarter-on-quarter increase;
- China data center computing power revenue is still excluded from the outlook.

Adding these facts increased the full model's $R^2$ from 10% to **21%–23%**, more than doubling it.

However, the organizers also pointed out: the performance of the three models was very close. Increasing the reasoning intensity from medium to highest provided no benefit to Luna. The organizers' explanation is that stock prices only react to new information, and whether information is "new" depends on what the market expected beforehand. "Revenue of $96 billion" is neither good nor bad in itself: if the expectation was $92 billion, it's a big surprise; if the expectation was $95 billion, it's just a small beat. The model only sees "96 billion" and doesn't know the expectation, making it difficult to judge even if it's smart.

## /05 Experiment Two: Agents Write Research Reports Before Earnings

Thus, the core experiment for Q3 emerged. In Q3 2026, before each earnings call, the organizers ran an agent task: letting Claude Opus 5, in the Claude Code environment, run Anthropic's earnings preview skill.

This agent was only told the company name, fiscal quarter, and release time, and was expected to find other information on the public internet to produce a standardized forward-looking research report, including **consensus expectations and company guidance, the most critical metrics of the quarter, bull/base/bear scenarios and their corresponding stock price reactions, and market positions and sentiment.** Out of 546 competition events, reports were generated for 542.

This method of having AI write research reports and then using them as input is also something we can learn from. The following uses the Nvidia earnings event as an example to look at several core facts and viewpoints from the AI research report.

### Case: Nvidia Earnings Event

The earnings were released after the US Eastern Time market close on August 26, 2026. When the report was written, the stock price was approximately $212.51, with a market capitalization of about $5.24 trillion, roughly 10% below the 52-week high ($236.54).

#### Distinguishing "Sell-Side Consensus" from "Buy-Side Thresholds"

| Metric | Company Guidance | Sell-Side Consensus | Buy-Side/Whisper |
| :--- | :--- | :--- | :--- |
| Revenue | $91 billion $\pm$2% | $91.9–92.3 billion | $94–95 billion |
| Non-GAAP EPS | — | $2.08–2.09 | Above approx. $2.15 |
| Data Center Rev | — | Approx. $85.7 billion | High $80 billion tier |
| Gross Margin | Approx. 75% | Approx. 75% | $\ge$75%, not diluted by Rubin ramp |
| Next Q Rev Guid | — | $103.8–104.1 billion | Above $105 billion |

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930193726305.png)

This table represents exactly what previous models lacked. The report explicitly wrote: exceeding $92 billion is just an "entry ticket"; what truly distinguishes the outcome is above $95 billion.

#### Key博弈 Points

The report considered only one number to be most critical: **next-quarter revenue guidance**. $105 billion is the long-side dividing line, and $103 billion is the disappointment line. It also stated that the stock price reactions in the last four quarters were driven by the guidance relative to the buy-side threshold, not by the magnitude of this quarter's beat.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930193947599.png)

This corresponds exactly to the phenomenon mentioned at the beginning: "four consecutive beats but price drops." The beat was against the sell-side numbers, not the buy-side.

#### Scenarios and Probabilities

| Scenario | Probability | Next Q Guidance | Key Drivers | Expected Stock Reaction |
| :--- | :--- | :--- | :--- | :--- |
| Bull | Approx. 25% | $\ge$106–108 billion | Rubin early, margin holds 75%, China included | +6% to +11% |
| Base | Approx. 50% | 104–105.5 billion | Routine small beat, margin approx. 75% | −3% to +3% |
| Bear | Approx. 25% | $\le$103 billion | Guidance only meets expectations, margin slides to approx. 73.5% | −8% to −13% |

The report also noted that options-implied volatility was approximately $\pm$5.4% to $\pm$5.9% (from secondary data on the internet, not the same source as the official statistics provided by the platform below); semiconductor funds saw a net outflow of approx. $6.3 billion over three weeks; the Bank of America Bull/Bear indicator was at an extreme position of 9.5 (leaning towards a contrarian bullish signal), indicating that market sentiment was not frenzied. Its conclusion was: the volatility priced in by options was lower than the bull and bear scenarios, so if one is confident in tail outcomes, the options pricing is considered reasonable.

#### Post-Mortem Comparison: Roughly Within the Bull Scenario

The actual disclosure during the earnings call was: revenue $96 billion, next-quarter guidance $108 billion, data center revenue $89 billion. The market-adjusted return within the reaction window was **+8.1%**.

- **Revenue** of $96 billion falls within the bull scenario range ($95–97 billion) and is higher than the upper bound of the buy-side whisper.
- **Next-quarter guidance** of $108 billion reaches the upper bound of the bull scenario, far exceeding the $105 billion long-side line.
- **Data center revenue** of $89 billion exactly meets the $89 billion required by the bull scenario.
- **Stock price** +8.1% falls within the expected range of the bull scenario (+6% to +11%).

There were two discrepancies with the report's assumptions:

- **Gross Margin.** The report set holding 75% as a bull condition and sliding below 73% as a bear signal. The actual Q3 guidance was 74%, with Q4 dropping to 71%–72%. According to the report's own framework, this is slightly negative, yet the stock price surged significantly. This shows the market values the magnitude of growth more, and the report over-weighted the gross margin.
- **China.** The report listed "China included in guidance" as one of the bull conditions, but it was not actually included, and the bull result still occurred.

**This is merely a post-hoc selected case and does not prove the report's effectiveness; validity must be seen in the overall $R^2$ in the next section.** The report is not an "accurate prediction" but provides the model with a ruler: with expected numbers like "buy-side $95 billion, guidance dividing line $105 billion," $96 billion and $108 billion have a benchmark for whether they beat expectations.

## /06 Organizers' Verification: Explanatory Power Reaches Over 30%

With the research report as additional context, every model tested by the organizers performed better, and the ranking became clear: **Astra > Sol > Luna.** The previous phenomenon where the three models had close results no longer appeared, consistent with the blog's explanation that "the bottleneck lies in the lack of expectation information."

Reasoning intensity also began to play a role, especially for the smallest model: Luna increased from 24% at medium intensity to 29% at highest intensity, costing less than $3 per 1,000 events. **GPT-6 Astra, under ultra-high (xhigh) reasoning intensity, explained over 30% of the return variance.**

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930194053450.png)

The official ranking on the leaderboard looks at $\Delta R^2$. The 30% in the blog is the full model's $R^2$, compared to a baseline of approx. 10%, with an increment of approximately 20 percentage points (this is my conversion; the blog does not give it directly).

**Comparison with the paper.** The abstract cited on the website states that the optimal agent system increased $R^2$ from approx. 8% to nearly 20%, which was a system that extracted signals from earnings call texts and optimized them. The 30% in this blog comes from new data in Q3 2026 and another set of tests by the organizers. The samples and settings of the two are different, so strict comparison is not appropriate, nor is direct comparison with the participant leaderboard, but the direction is consistent: good context significantly improves explanatory power.

## /07 Next Step: Adding Options Market Data

Based on previous research, the organizers will inject new data into the Q4 competition:

Starting October 3, 2026, the platform will attach three statistics from the options market for stocks with liquid options, all measured before the knowledge cutoff. Research reports will also become data received with every submission starting from the same day, so participants do not need to build their own research workflows.

- **Implied Earnings Volatility:** Using the at-the-money implied volatility of the first two expirations after earnings, splitting the earnings event jump from daily volatility according to the term structure method of Dubinsky et al. (2019).
- **Implied Absolute Volatility Magnitude:** The price jump magnitude expected by the market, with only size, no direction.
- **25-delta Skew:** The implied volatility of 25-delta call options minus the implied volatility of 25-delta put options (Carr and Wu, 2007). A negative value indicates that downside protection is priced higher.

Taking Nvidia as an example, its historical options statistics are:

- Implied Earnings Volatility: 6.36%
- Implied Absolute Volatility Magnitude: 5.07%
- 25-delta Skew: −1.61 volatility points

Both the research report and options statistics are placed in the event's `DisclosureBundle`, accessed via `information_url`. Both are optional; if they don't exist, they won't appear, so code must handle graceful fallback. Less than half of the Q3 events had options statistics. **How much improvement these new data points can bring has not yet been given results in the blog.**

## /08 Conclusion

Returning to the initial question: Can AI explain stock price reactions after earnings?

The competition is still ongoing. So far, there is still 70% of the variance unexplained. Of course, theoretically, we should not expect 100% of the variance to be explained.

The current answer from Explaining Markets is: **AI can already read part of the relationship between earnings and stock prices, and the key to making it work is not a stronger model, but letting it know what the market expected beforehand.**

Regardless, Koijen and Levy have provided new methods in their working paper and competition. For quants, influenced by reflexivity, there are few eternal Alphas (though there are indeed some, such as small-cap). The process of seeking Alpha is the process of seeking new information and new processing methods.
