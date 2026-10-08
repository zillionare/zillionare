---
title: "Why Good News Fails: AI Earnings Forecasting Revealed"
date: 2026-10-01
slug: en/posts/tools/earnings-preview-with-llms
tags: [Factor Mining, Earnings Surprise, AI Trading, Market Expectations]
excerpt: "Nvidia beat estimates four times yet dropped. Optiver and UChicago test AI systems predicting stock reactions to earnings, using live R² to expose the \"good news, no rise\" paradox."
lang: en
translation_of: posts/tools/earnings-preview-with-llms
auto_translated: true
source_sha: ed9157ba40c214886108f925e574ca832f8a5b48
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261001095444-earnings-preview-with-llms.jpg"
---

The market on September 30 was volatile and erratic. On the news front, a major interest-rate subsidy policy was released the previous night, theoretically bullish for the real estate sector. Yet, the relevant sectors opened lower and fell, dropping as much as 4.35% at one point. Fortunately, the sector dipped first then rallied, closing up 0.91% by the end of the day.

Clearly, we must ask: Why does good news lead to a lower open and decline? Is this the so-called "sell the news" phenomenon?

This is a problem quantitative research has long sought to solve. Of course, the policy response in China A-shares is not the same mechanism as the earnings response in US equities. This article merely borrows the question "Why doesn't good news lead to gains?" to discuss the issue.

Today, we introduce a platform launched by Optiver in collaboration with researchers from the University of Chicago (Ralph S. J. Koijen and Bradford Lynch): **explainingmarkets.ai**. It is hosting a public competition for global participants: **Participants build AI systems to predict stock reactions to earnings announcements and are tested against real market outcomes.**

From the organizer's side, the platform's researchers have also conducted a set of controlled experiments: using three OpenAI models—GPT-6 Luna, Sol, and Astra—to test how much different data inputs can improve the "AI's ability to explain earnings reactions."

Ralph S. J. Koijen and Bradford (Lynch) Levy are both from the University of Chicago Booth School of Business. The competition is based on the benchmark proposed in their co-authored working paper, *Assessing the Benefits of Optimized Agentic AI Systems for Asset Pricing*, and comes with an SDK for researchers to evaluate AI systems under real-time, out-of-sample standards.

The University of Chicago is the Mecca for global economists and the birthplace of the Chicago School, which has profoundly shaped the face of modern economics.

## /01 The Old Question: Why Do Stocks Fall After Beating Estimates?

Every earnings season, traders encounter this scenario: A company's revenue, profit, and next-quarter guidance all exceed analyst expectations, yet the stock price drops the next day.

Nvidia is a typical example. According to the Explaining Markets blog, prior to its August 2026 earnings report, Nvidia had beaten estimates on revenue, EPS, and next-quarter guidance for four consecutive quarters. Yet, each time triggered a next-day stock price decline, with an average beat magnitude of about 4.8%.

This indicates that stock prices do not reflect "good news," but rather "news that is better than expected." But what exactly constitutes expectations is hard to quantify, and even harder for AI to understand.

## /02 Explaining Markets: A Global "AI System" Competition

The participation process involves three steps:

1. **Build and Connect.** Download the example Notebook or use the official launch template based on the Modal cloud platform to set up the agent and connect to the platform. The official site claims most people can get it running within 30 minutes.
2. **Receive Real-Time Events.** When a company releases earnings, your agent receives a summary of the earnings call points and submits a prediction before the deadline.
3. **Track Performance.** Each prediction is compared with actual market performance, and scores are updated on the public leaderboard.

For each event, the agent submits a number between 0 and 1, indicating the percentile rank of the expected market reaction for that stock among all earnings announcements in that quarter: 0 is the most negative, 0.5 is neutral, and 1 is the most positive. The test focuses on relative ranking, not the absolute magnitude of price changes. Each event is judged by the first valid submission; late, incorrectly formatted, or out-of-bounds submissions count as misses. Missed events are filled in by the organizers using your average prediction, so skipping is not cost-effective.

The platform uses $R^2$ to measure the fit between predictions and actual returns, which can be understood as "the proportion of return variance explained by the prediction." The leaderboard provides three numbers for each agent:

- The baseline $R^2$ using only "earnings beat";
- The complete model $R^2$ including the agent's prediction;
- The difference $\Delta R^2$, representing how much more variance the prediction explains compared to "just looking at earnings beats."

The quarterly leaderboard is ranked by $\Delta R^2$, while the prize ranking is calculated based on $\Delta R^2$ across all scored events. The scoring logic is fully open in the example repository.

Anyone can participate, including students, researchers, engineers, and independent developers, with no financial background required—just Python skills. There is no entry fee; costs depend mainly on which models are called and how frequently. The official site states that the total budget for Koijen and Levy's paper was less than $10. Each account can submit up to 5 agents, with up to 10 team members per agent.

The top five share a total of $7,500 ($2,500, $2,000, $1,500, $1,000, $500), funded by Optiver and distributed by the University of Chicago.

## /03 What Are Participants Competing On?

All participants receive the same official materials: each event is pushed through the platform interface with an information package for that event, the core of which is a summary of the earnings call.

The rules do not limit models or tools, nor do they restrict you from supplementing data, **provided that no information after the event's "knowledge cutoff" is used.** This restriction covers the entire process of data collection, prompting, retrieval, external search, manual research, and manual adjustment. Market signals such as prices, volumes, and options data after the cutoff cannot be used unless provided by the official interface. Violators are ineligible for prizes, may be publicly flagged or removed from the leaderboard, and winners may be required to provide logs, timestamps, and other records, potentially undergoing audits.

Thus, differences can only come from participants' own methods: how to design prompts and reasoning flows, which models to choose, what public data before the cutoff to supplement, and how to handle official materials. Forward-looking bias is the primary issue this benchmark seeks to avoid, which is also why the rules are so strict. Participants are not required to open-source their code or prompts, only to provide a high-level method description.

As of September 30, the complete model $R^2$ for the top three on the Q3 leaderboard was 26.5%, 26.1%, and 26.0%, with a baseline $R^2$ of 9.7%, and $\Delta R^2$ values of 0.168, 0.164, and 0.162, respectively. The scoring period for this season ends on October 2, so these are preliminary results and will only count after qualification and compliance verification.

## /04 Experiment One: Letting AI Read Earnings Calls

Besides the competition, **the organizers are also conducting data experiments** to decide which new data sources to add to each season's competition. These new sources are believed to enhance the explanatory power of participants' models.

!!! tip
    In a sense, you can consider that through this competition, top-tier funds and economists have provided their latest research directions for LLM factor mining. Readers might consider applying these insights to other competitions, such as the WorldQuant ranking contest, potentially uncovering new Alpha.

The baseline is the earnings surprise, defined as the gap between actual performance and analyst consensus. In the most recent earnings season (Q3 2026), relying solely on earnings surprise yielded an $R^2$ of approximately **10%**, slightly higher than previous quarters, but still leaving about 90% of the variance unexplained.

Beyond numbers, there is information. The organizers extracted structured facts from earnings calls and fed them into three OpenAI models: Luna (smallest), Sol, and Astra (strongest). Taking Nvidia as an example, the extracted key points included:

- Q2 revenue hit a record high of $96 billion;
- Q3 revenue guidance is $108 billion (±2%);
- Gross margin was adjusted downward due to rising storage prices, approximately 74% in Q3, hitting a bottom of 71%–72% in Q4;
- Data center revenue was $89 billion, a 18% quarter-over-quarter increase;
- China data center computing power revenue is still excluded from the outlook.

Adding these facts raised the complete model's $R^2$ from 10% to **21%–23%**, more than doubling it.

However, the organizers also pointed out: The performance of the three models was very close. Increasing the reasoning intensity from medium to highest provided no help for Luna. The organizers' explanation is that stock prices only react to new information, and whether information is "new" depends on what the market expected beforehand. "Revenue of $96 billion" is neither good nor bad in itself: if the expectation was $92 billion, it's a big surprise; if the expectation was $95 billion, it's just a slight beat. The model only sees "96 billion" and doesn't know the expectation, making it difficult to judge even with high intelligence.

## /05 Experiment Two: Agents Write Research Reports Before Earnings

Thus, the core experiment for Q3 emerged. In Q3 2026, before each earnings call, the organizers ran an agent task: having Claude Opus 5 operate within the Claude Code environment, using Anthropic's earnings preview skill.

This agent was only told the company name, fiscal quarter, and release time; it had to find the rest of the information on the public internet to produce a standardized forward-looking research report, including **consensus estimates and company guidance, the most critical metrics for the quarter, bull/base/bear scenarios and their corresponding stock price reactions, and market positioning and sentiment.** Out of 546 competition events, reports were generated for 542.

This method of having AI write research reports and then using them as input is also something we can learn from. Below, using the Nvidia earnings event as an example, we look at the core facts and viewpoints of the AI research report.

### Case: Nvidia Earnings Event

The earnings were released after the US Eastern Time market close on August 26, 2026. When the report was written, the stock price was approximately $212.51, with a market cap of about $5.24 trillion, roughly 10% below its 52-week high ($236.54).

#### Distinguishing "Sell-Side Consensus" from "Buy-Side Thresholds"

| Metric | Company Guidance | Sell-Side Consensus | Buy-Side/Whisper |
| :--- | :--- | :--- | :--- |
| Revenue | $91B ±2% | $91.9–92.3B | $94–95B |
| Non-GAAP EPS | — | $2.08–2.09 | ~$2.15+ |
| Data Center Rev | — | ~$85.7B | High $80B tier |
| Gross Margin | ~75% | ~75% | ≥75%, not diluted by Rubin ramp |
| Next Q Guidance | — | $103.8–104.1B | >$105B |

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930193726305.png)

This table represents exactly what previous models lacked. The report explicitly states: exceeding $92 billion is just an "entry ticket"; what truly differentiates is exceeding $95 billion.

#### Key Battlegrounds

The report considers the single most important number to be: **Next Quarter Revenue Guidance.** $105 billion is the long-side threshold, and $103 billion is the disappointment line. It also states that the stock price reactions in the last four quarters were driven by the guidance relative to the buy-side threshold, not the magnitude of the current quarter's beat.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930193947599.png)

This corresponds precisely to the "four consecutive beats yet declines" phenomenon mentioned at the beginning: the company beat the sell-side numbers but failed to exceed the buy-side thresholds.

#### Scenarios and Probabilities

| Scenario | Probability | Next Q Guidance | Key Drivers | Expected Stock Reaction |
| :--- | :--- | :--- | :--- | :--- |
| Bull | ~25% | ≥$106–108B | Rubin early, Gross margin holds 75%, China included in guidance | +6% to +11% |
| Base | ~50% | $104–105.5B | Routine slight beat, Gross margin ~75% | −3% to +3% |
| Bear | ~25% | ≤$103B | Guidance only meets expectations, Gross margin slides to ~73.5% | −8% to −13% |

The report also notes that options-implied volatility is approximately ±5.4% to ±5.9% (from secondary online data, not the same source as the platform's official statistics below); semiconductor funds saw a net outflow of approximately $6.3 billion over three weeks; and the Bank of America Bull/Bear indicator is at an extreme level of 9.5 (leaning towards a contrarian bullish signal), indicating that market sentiment is not frenzied. Its conclusion is: the volatility priced in by options is lower than the bull/bear scenarios; if one is confident in tail outcomes, the options pricing is reasonable.

#### Post-Event Comparison: Roughly Within the Bull Scenario

The actual disclosure during the call was: Revenue $96 billion, Next Q guidance $108 billion, Data center revenue $89 billion. The market-adjusted return within the reaction window was **+8.1%**.

- **Revenue** of $96 billion falls within the bull scenario range ($95–97 billion) and above the whisper upper bound.
- **Next Q Guidance** of $108 billion reaches the upper bound of the bull scenario, far exceeding the $105 billion long-line.
- **Data Center Revenue** of $89 billion exactly meets the $89 billion requirement for the bull scenario.
- **Stock Price** +8.1% falls within the expected range for the bull scenario (+6% to +11%).

There are two discrepancies with the report's assumptions:

- **Gross Margin.** The report set holding 75% as a bull condition and sliding below 73% as a bear signal. The actual Q3 guidance was 74%, with Q4 dropping to 71%–72%. According to the report's own framework, this is negative, yet the stock price surged significantly. This suggests the market places more weight on the magnitude of growth, and the report over-weighted the gross margin.
- **China.** The report listed "China included in guidance" as one of the bull conditions, but it was not included in reality, yet the bull result still occurred.

**This is merely a post-hoc selected case and does not prove the report's effectiveness; validity must be seen in the overall $R^2$ in the next section.** The report is not an "accurate prediction" but provides the model with a ruler: with expected numbers like "Buy-side $95 billion, Guidance threshold $105 billion," $96 billion and $108 billion have a comparative benchmark for whether they beat expectations.

## /06 Organizers' Validation: Explanatory Power Rises Above 30%

With the research report as additional context, every model tested by the organizers performed better, and the ranking became clear: **Astra > Sol > Luna.** The previous phenomenon of the three models having close results no longer appeared, consistent with the blog's explanation that "the bottleneck lies in the lack of expectation information."

Reasoning intensity also began to play a role, especially for the smallest model: Luna increased from 24% at medium intensity to 29% at highest intensity, costing less than $3 per 1,000 events. **GPT-6 Astra, under ultra-high (xhigh) reasoning intensity, explained over 30% of the return variance.**

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/09/20260930194053450.png)

The official leaderboard ranking looks at $\Delta R^2$. The 30% in the blog is the complete model's $R^2$, compared to a baseline of about 10%, an increment of approximately 20 percentage points (this is my conversion; the blog does not give this directly).

**Comparison with the Paper.** The abstract cited on the website states that the optimal agent system increased $R^2$ from about 8% to nearly 20%, which was a system that extracted signals from earnings call text and optimized them. The 30% in this blog comes from new data in Q3 2026 and another set of tests by the organizers. The samples and settings differ, so strict comparison is not appropriate, nor is direct comparison with the participant leaderboard, but the direction is consistent: good context significantly improves explanatory power.

## /07 Next Steps: Adding Options Market Data

Based on previous research, the organizers will inject new data into the Q4 competition:

Starting October 3, 2026, the platform will attach three statistics from the options market for stocks with liquid options, all measured before the knowledge cutoff. Research reports will also become data received with every submission starting from the same day, so participants do not need to build their own research workflows.

- **Implied Earnings Volatility:** Using at-the-money implied volatility from the first two expirations after earnings, splitting the earnings event jump from daily volatility according to the term structure method by Dubinsky et al. (2019).
- **Implied Absolute Volatility Magnitude:** The magnitude of price jumps expected by the market, with no
