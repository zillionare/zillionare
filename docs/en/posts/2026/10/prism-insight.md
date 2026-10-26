---
title: "390-Day Live AI Trading System: PRISM-INSIGHT Architecture Breakdown"
date: 2026-10-25
slug: en/posts/tools/prism-insight
tags: [AI Trading, Multi-Agent Systems, Factor Investing, Quantitative Analysis]
excerpt: "A Korean developer's open-source AI trading system achieves 12.97% returns during a 10.36% market decline over 390 days. This article dissects its Python-hardcoded screening, multi-Agent analysis, and reinforcement learning feedback loops."
lang: en
translation_of: posts/tools/prism-insight
auto_translated: true
source_sha: d15ad7578041875672eaccd4eaf2ee744fd8ff66
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261026005742-prism-insight.jpg"
---

Large Language Models (LLMs) and Agents have entered the quantitative trading arena for nearly two years. How far have they actually come?

Over the past year, we’ve observed a fascinating polarization. On one hand, open-source projects on GitHub related to “multi-agent trading” garner massive attention; for instance, the well-known `TradingAgents` has surpassed 100,000 stars. On the other hand, those that actually deploy systems for live trading or real-time simulation often yield disappointing results.

At the end of last year, the overseas website `nof1.ai` conducted a highly publicized experiment by live-streaming the real-money trading of multiple AI Agents. Nine months later, the site has seen its traffic dwindle. The reason is pragmatic: the best-performing Agent in the experiment achieved a Sharpe ratio of only 0.019, underperforming even average retail investors. In other words, in the first phase of public testing, allowing general-purpose LLMs to directly analyze charts and execute orders was a failure.

However, we recently noticed an open-source project by a Korean developer: **PRISM-INSIGHT**.

This is a system capable of executing live trades on US and Korean stock markets. The author built a website that allows the system to trade automatically every day, synchronizing positions and net asset value (NAV) results to the web in real-time. As of now, this system has been running continuously for 390 days. Based on the public ledger from the last six months, while the Korea Composite Stock Price Index (KOSPI) fell by 10.36%, the system’s simulated account maintained a positive return of 12.97%, and the author’s small-capital live account achieved a profit of 20.23%.

After examining six or seven mainstream AI investment research and trading projects on the market, we believe PRISM-INSIGHT is the most worthy sample for detailed dissection. The reasons are primarily fourfold:

1.  **Continuous public out-of-sample testing:** It has run for over 390 days, enduring various market conditions, with a relatively stable ledger.
2.  **End-to-end closed loop:** While many similar projects remain at the stage of “assisting humans in writing reports,” this one has truly connected to broker APIs, completing the full process from information collection to automatic order execution and post-market review.
3.  **Built on mature trading frameworks:** It does not ask AI to invent investment philosophies from scratch but modernizes William O’Neil’s classic **CAN SLIM** growth stock momentum framework.
4.  **Clear engineering boundaries:** It is not purely “Vibe Trading” based on intuition but adheres to a pragmatic principle—**assigning qualitative reasoning to LLMs and strict discipline to Python code.**

For anyone looking to use AI for investment assistance or quantitative development, observing how it designs its architecture, falls into pitfalls, and modifies rules based on loss statements can save significant trial-and-error costs.

---

## /01 Architecture Breakdown: Python Hard Rules + Multi-Agent Four-Stage Pipeline

From a systems engineering perspective, PRISM-INSIGHT is a four-stage closed-loop pipeline composed of a “Python monolithic program + multiple LLM Agents”: **Screening > Analysis > Trading > Feedback**.

### Step 1: Coarse Screening Using Basic Volume-Price Rules

In the first stage (Screening), the system does not call large models at all. Instead, it obtains market data via `yfinance` and broker APIs, setting six hard trigger conditions using pure Python code:

1.  **Early-Month Volume Surge:** Requires trading volume to increase by more than 30% compared to the mean.
2.  **Early-Month Gap Momentum:** Gap-up magnitude exceeds 1%, and the candlestick closes bullish.
3.  **Market Cap and Capital Concentration:** A comprehensive scoring index, truncated by ranking stocks.
4.  **Intraday Trend Strength:** Requires intraday gains between 3% and 15%, closing bullish.
5.  **Late-Month Strength:** Requires closing position above a set threshold, accompanied by increased volume, and total daily gains between 0% and 15%.
6.  **High-Volume Consolidation:** Volume increase rate > 50%, absolute price change < 5%, and stock price above the 20-day moving average.

Those familiar with short-term trading in China A-shares might smile at these six conditions—they are essentially the market features often discussed by experts on platforms like Taoguba. This shows that the underlying logic of momentum trading is universal across regions; even high-end AI pipelines often rely on the most basic volume-price factors for initial screening. In O’Neil’s CAN SLIM framework, this step roughly corresponds to the letter **S** (Supply and Demand) and part of **L** (Leader).

### Step 2: Specialized Analysis by Six Independent Agents

After the stock pool is narrowed down through coarse screening, it formally enters the analysis layer composed of six LLM Agents:

-   **Technical Analyst:** Note that PRISM does not feed raw candlestick numbers directly to the LLM for “chart reading.” Instead, the program first calculates moving averages (5-day, 20-day, 110-day, 200-day) and classic indicators like RSI, MACD, and Bollinger Bands. The Agent then evaluates support/resistance levels and the validity of moving average breakouts based on these pre-calculated structured results.
-   **Investor Analyst (Corresponding to Letter I):** Calls data from Korea Investment Securities (KIS) to track daily buying and selling trends of institutions, foreign investors, and retail investors, determining who is currently buying and whether capital flow resonates or diverges from price trends. In our previous blog posts (e.g., *Research on Fast Fourier Transform and Stock Price Prediction*), we discussed that market trends are essentially composite waves formed by capital博弈 across different cycles: institutions have large positions and slow turns, holding for quarters; retail capital moves fast. Identifying the dominant capital nature is crucial for judging trend sustainability.
-   **Fundamental and Event Analysis (Includes `company_status`, `company_overview`, and `news_analysis` Agents):** The first two are responsible for breaking down recent quarterly revenue and profit growth, annual growth trends, and peer valuation comparisons (corresponding to letters **C** and **A**). `news_analysis` specifically uses search and crawler tools to investigate whether the company has new products, new businesses, new management changes, or daily event catalysts (corresponding to letter **N**).
-   **Market Analyst (Corresponding to Letter M):** Evaluates the overall direction and market style of the broader market, deciding whether the system should attack or defend.

### Step 3 and 4: Summary Decision and Post-Market Feedback

In the project’s early stages, the author designed up to 13 Agents but streamlined them in subsequent iterations. Currently, the core trading chain involves mainly 8 Agents (6 analysts + 1 summary + 1 buy/sell decision), plus several post-market auxiliary modules:

-   **Strategy Summary and Trade Execution:** In Step 3, the **Strategy Summary Agent** integrates the six reports from different dimensions into an investment strategy draft. In Step 4 (Trading), the **Buy Decision Agent** scores the written evaluation table from 1 to 10 and explicitly writes the trigger scripts for adding positions after建仓 (opening positions). The **Sell Decision Agent** monitors stop-loss and take-profit during the holding period.
-   **Post-Market Auxiliary Modules:** One is the **Communication Module**, which uses an Evaluator-Optimizer Loop to condense lengthy analysis reports into Telegram messages under 400 words, translated into multiple languages for subscribers. The other is the crucial **Log and Memory Module**, which automatically conducts post-market reviews after each trade is closed, extracting lessons for future buy decisions.

### Why Split into Multiple Agents?

At this point, you might ask a practical engineering question: Why go to such lengths to split into so many Agents? Wouldn’t it be simpler to feed all data into a single context window and let one omnipotent Agent make the decision at once?

In engineering practice, the core value of splitting into multiple Agents lies in **“Perspective Isolation”** and **“Tool-Data Specialization Binding.”**

LLMs inherently possess a strong “Coherence Bias,” excelling at weaving chaotic information into a logically self-consistent story. Consider this thought experiment: If you only use one omnipotent Agent and feed it a beautiful candlestick chart showing a breakout to new highs, several hot news articles praising the theme, and a financial statement with a very high debt-to-asset ratio, what would happen? When the model sees the stock price surging and public opinion rejoicing, it is likely to “self-persuade” within the same context, conveniently rationalizing high debt as “strategic investment to welcome industry explosions,” thereby turning a blind eye to imminent financial risks.

By splitting into six independent Agents:

First, **role settings (System Prompts) and stances are physically isolated**. The Financial Agent’s prompt requires it to focus only on valuation, profitability quality, and balance sheets; it simply does not see how狂热 the market is, thus maintaining a cold auditor’s perspective. The News Agent is bound to Perplexity search and Firecrawl web scraping tools, specializing in verifying the authenticity of catalysts. The Capital Flow Agent only looks at seat-by-seat trading data.

Second, each Agent first forms independent evidence slices within their respective professional dimensions, which are then handed over to the summary and decision Agents for collision and weighing. Additionally, different stages can configure models of different tiers as needed—medium-sized models for basic information organization, flagship models with the strongest reasoning capabilities for final buy/sell decisions, and lightweight models for daily summaries and translations. This preserves the objectivity of analytical perspectives while keeping monthly Token bills within a reasonable range.

---

## /02 Horizontal Comparison: Four Schools of AI Investment Research and Trading Systems

If we broaden our perspective and compare PRISM-INSIGHT with three other popular projects on GitHub—`TradingAgents`, `easy-stock`, and `Vibe-Research`—we find they represent four different design philosophies for introducing LLMs into investment:

| Project Name | Core Positioning | Architectural Highlights and Design Focus | Includes Live Trading Closed Loop? |
| :--- | :--- | :--- | :--- |
| **TradingAgents** | Multi-agent research and experimental framework | **Viewpoint Confrontation and Debate Mechanism:** After four analysts (fundamentals, sentiment, news, technicals), it specifically establishes Bullish and Bearish researchers for multi-round structured debates, forcing out hidden risks of one-sided thinking. | No (Focuses on single-point experiments, no built-in live trading or continuous ledger) |
| **easy-stock** | Local-First short-term trading workstation for China A-shares | **Structured Calculation First, AI Interpretation Second:** For A-share-specific limit-up chains and theme structures, it first uses a Go backend to calculate limit-up tiers, promotion rates, theme strength, and sentiment cycles, then hands them to Agents for interpretation; periodically scrapes Xueqiu and Taoguba review posts to extract market consensus and divergence; scores holdings based on logic, structure, risk, and strategy matching for same-time rebalancing comparison. | No (Decision rights left to humans, an efficiency tool for limit-up and short-term traders) |
| **Vibe-Research** | Investment research workstation focusing on fundamentals and multi-dimensional data | **Strict “Digital Source Auditing”:** Connects to 168 data endpoints for China A-shares, HK stocks, and US stocks. In six-stage individual stock research, the program forces verification of every number output by AI—must find basis in original inputs, API returns, research report texts, or explicit formulas, cutting off “data hallucination” from an engineering perspective. | No (Focuses on deep investment research and evidence verification) |
| **PRISM-INSIGHT** | End-to-end fully automated live trading and research system | **Rule-based Coarse Screening + Multi-Agent Judgment + Language Space Reinforcement Learning:** Connects the complete closed loop from stock selection, analysis, live order execution, to post-market position closing and review, continuously iterating the system’s experience library with real profits and losses. | Yes (Supports live trading in Korean and US stocks, continuously running publicly for 390 days) |

Among these four projects, PRISM-INSIGHT’s most unique feature is not just its willingness to connect directly to live trading, but its implementation of a sophisticated self-evolution mechanism in the post-market review phase.

### How to Make Agents Smarter Without Changing Model Weights?

Many friends attempting AI-based trading encounter the same bottleneck: We have accumulated a batch of live or backtest trading records and want to feed this first-hand experience back to the Agent to improve its judgment, but individuals and small teams obviously lack the computing power and conditions to re-fine-tune (Fine-tune) large models with hundreds of billions of parameters. So, without changing model weights, can the post-closing review loop truly enhance the system’s prediction and trading capabilities?

The answer is yes. This is currently a very focused direction in academia and industry, commonly referred to as **In-Context Reinforcement Learning**, or more vividly—**“Natural Language Space Reinforcement Learning.”**

Traditional reinforcement learning modifies the floating-point weights of neural networks via backpropagation based on profit/loss rewards after each game or trade. In large model applications, although we cannot change the underlying weights, we can leverage the large model’s strong context learning capabilities. If we structurally save the “buy basis, market status at the time, final profit/loss result, and post-market review reasons” of each historical trade, summarizing and compressing them into a continuously updated “Experience Rule Library (Intuitions).” The next time a candidate stock with a similar pattern appears, the system automatically retrieves the most relevant positive and negative examples and feeds them into the buy decision prompt. Mathematically, although the model’s parameters have not changed, the **conditional probability distribution** of the model’s output decision has changed given the new context conditions—we are not performing gradient descent in parameter space but strategy iteration in natural language prompt space.

Looking at the commit history of the PRISM repository from the past week, the author just made a very interesting upgrade (Commit title: `rebuild BUY intuitions from big movers vs lookalikes`).

In the early version, its memory system simply asked the model to write “self-criticism essays” for losing trades. But the author soon found that writing self-criticism only made the model increasingly timid. So he changed it to a **Positive/Negative Example Contrast Extraction Method**: The system places historically true big-mover stocks (Big Movers, positive samples) and those “fake breakout stocks” (Lookalikes, i.e., Hard Negatives in machine learning) that looked identical in indicators and breakout patterns at purchase but stopped out at a loss, together, asking the large model to specifically compare the subtle differences between these two groups in fundamental quality, catalyst quality, or volume-price details, thereby extracting “Intuitions” to distinguish true from false breakouts.

More rigorously, the author specifically wrote a statistical validation function in the code to continuously track the comparison between “trades that referenced historical intuitions and adjusted scores” and “trades that did not reference historical intuitions,” to see if the former’s actual win rate and average return outperform the latter. If an extracted intuition has a win rate below 30% in subsequent live trading verification, or has not been triggered for verification for over 90 days, the cleanup script will automatically deactivate it.

This closed loop of “positive/negative example contrast extraction + live trading win rate verification + inferior experience elimination” is, in principle, very close to a complete non-parametric reinforcement learning system.

---

## /03 Examining O’Neil’s Framework: Is a 1960s Method Still Useful Today?

After discussing the technical architecture, let’s explore a more fundamental investment question: The **William O’Neil CAN SLIM framework** upon which PRISM relies was born in the 1960s. In the 1960s, information dissemination relied on newspapers and mailed financial reports, and it might take weeks for the market to digest a piece of fundamental information. Today, with the internet and high-frequency computing, the speed of information pricing has been compressed to intraday or even second-level.

This raises a “cycle mismatch” question that many quants doubt: Company financial reports are updated quarterly, while volume-price data jumps every second. Since any piece of fundamental information is often fully reflected in the stock price within one or two trading days, and there are no new fundamental changes in the remaining dozens of trading days, how useful is this system that mixes slow variables (fundamentals) and fast variables (volume-price) today? Can daily jumping volume-price information not fully reflect fundamentals?

### Why Can’t Fundamentals Be Digesting in One or Two Days?

Our view is: **The speed of information dissemination has indeed become second-level, but the physical process of large capital changing positions is still measured in “weeks” and “months.” The role of fundamentals today is not for “intraday front-running” but for “true/false falsification” of volume-price anomalies and “qualitative determination of holding periods.”**

This can be understood from two levels:

First, **large institution’s position building is constrained by physical liquidity.** This explains why CAN SLIM requires investor structure analysis (Letter I). Large institutions like public funds, pension funds, and long-term foreign capital, constrained by strict risk control compliance and market depth, cannot possibly buy hundreds of billions of positions in one go at the next day’s call auction even if a company’s financial report exceeds expectations tonight—doing so would directly crash the stock price. The gap-up surge in the first one or two trading days after the report is often the “ignition signal” created by hot money, quantitative event-driven funds, and proactive active buyers. Over the following two to three months, as the industrial logic is continuously verified by upstream and downstream orders, large institutions build positions in batches during pullbacks, forming the complete main uptrend.

Second, **pure volume-price signals are prone to “Lookalikes.”** In the early morning of a trading day, a concept stock relying purely on small rumors and suffering annual losses in its main business, and a high-quality growth stock that just secured a large overseas order and faces industry capacity shortages, can look exactly the same in their intraday charts and daily candlesticks showing “volume breakout and net capital inflow.” If only looking at volume-price, the system cannot distinguish whether this is the start of a main uptrend or a bull trap created by hot money pumping and shipping out.

In the dozens of trading days without financial reports, fundamentals play the role of a **“Slow Variable Filter”** and a **“Holding Confidence Anchor.”** Only by confirming the true底色 (background/color) of the fundamentals can the system dare to judge that a 4% drop in volume after a pullback on the 5th day post-breakout is a normal washout and continue holding, rather than panic-cutting losses. In short: Volume-price is the fast variable, responsible for providing the timing to pull the trigger; fundamentals are the slow variable, responsible for filtering false signals and deciding how long you can hold this trade.

### Why Is It Worth Rewriting CAN SLIM with Agents?

Since this system is not obsolete, why is it worth rewriting it with large models? Haven’t traditional quantitative quants written countless versions of CAN SLIM strategies over the past few decades?

If we return to O’Neil’s original book *How to Make Money in Stocks* and the official definition of *Investor’s Business Daily (IBD)*, and break down the seven letters of **CAN SLIM** one by one, we discover the huge regrets left by traditional quantification:

-   **C (Current Quarterly Earnings) and A (Annual Earnings Growth):** These two letters were the easiest for traditional quantification to implement over the past few decades; writing a few lines of SQL to query the financial database can filter them out. Today, the incremental value LLMs can provide in C and A is relatively limited, mainly reading financial report footnotes to help eliminate “fake growth” made up by selling land, subsidiaries, or exchange gains, and comparing whether performance exceeds buyer expectations.
-   **N (New Products, New Management, New Highs off Properly Formed Bases):** Please note O’Neil’s original definition—he condensed **“New Products, New Services, New Management, New Industry Changes”** (fundamental novelty) and **“Stock Price Breaking Out from Properly Formed Bases to New Highs”** (price novelty) into the same letter N. O’Neil statistically found that 95% of super bull stocks have some major “new change” as the engine behind them at startup. This is like what A-share friends often say: The stocks are the same, but there are new themes every year.
    However, how did quants write the N factor in the past few decades of traditional quantification? Because code cannot read what “disruptive new products” mean, almost all quantitative strategies simplified N into a single price indicator—“current closing price is near or at 52-week high.” As a result, the core soul of N (stock price hitting new highs driven by new fundamental changes) was castrated.
    **This is the first core breakthrough where large language models play a value role.** In PRISM, when the volume-price script detects a stock’s abnormal breakout, the `News Analyst` and `Company Overview` immediately call search and crawler tools to read the company’s latest announcements, press releases, and industry reports, using natural language understanding capabilities to verify: Behind this breakout, is there really a substantive new product launch, large new order landing, or industry policy catalyst? If not, and the stock price simply rises inexplicably, the Buy Agent will directly lower the score when scoring.
-   **S (Supply and Demand):** Moderate circulating shares, stock buybacks, and key breakout day volume increasing by more than 50%. This part is easily calculated by traditional volume-price code.
-   **L (Leader or Laggard):** This is the second ceiling hit by traditional quantification. O’Neil emphasized buying true leaders (Leader) in the industry, never buying laggards (Laggard) that follow up due to being cheap. To quantify this, he invented the famous RS index (Relative Price Strength, scored 1 to 99).
    But the problem is, **does “price rising fast” equal “true industry leader”?** In the early stage of concept hype, a marginal small-cap stock touching the concept might hit several limit-ups, with its RS score reaching 99, but it has no bargaining power in the industry chain, revealing its true form when the tide recedes. **This is the second core breakthrough brought by large models:** By reading research reports and company main business composition, large models can directly sort out “who controls core capacity in the HBM memory or optical module industry chain, whose gross margin is highest, and who supplies core large factories.” Combining **“Qualitative Industry Competitive Position (Business Leader)”** with **“Quantitative Relative Price Strength (Price Leader)”**, the letter L is truly complete.
-   **I (Institutional Sponsorship) and M (Market Direction):** These two areas are still basically the playground for traditional quantitative indicators.

Following this line of thought, one can draw inferences: Over the past few decades, the investment world has accumulated many classic frameworks—whether O’Neil’s CAN SLIM, Peter Lynch’s growth stock classification, or Buffett’s moat theory. Previously, when doing quantification, we could only pick parts with ready-made structured data to write code, forcing us to discard the qualitative dimensions that truly determine success or failure. The emergence of large language models essentially gives us the first tool to pick up those “qualitative puzzles” abandoned by traditional quantification and put them back into automated pipelines.

### Anti-Dogma: When the 60s’ “8-Week Holding Rule” Collides with Modern Markets

Of course, the O’Neil framework also has outdated aspects. When PRISM’s author truly installed this system into the system and ran it live on Korean and US stocks for over a year, he found: Even if the stock selection end is supplemented by AI for N and L, if the selling end blindly copies O’Neil’s mechanical holding rules from the 1960s, it will still suffer greatly in today’s market.

First is the pain point of “selling big bull stocks too early.” The author’s statistics on the system’s historical ledger show: Among Korean bull stocks that rose more than 30% within 60 trading days after entry, the median of their highest gains reached **+60%**, but the median profit actually captured by the system upon closing was only a pitiful **+2%**! Most big bull stocks were washed out early by moving stop-loss or sell Agents just after rising a little.

To solve the problem of not being able to hold big bull stocks, the author decided to test the most famous **“8-Week Hold Rule”** in the O’Neil framework—O’Neil’s original book stipulates that if a stock rises rapidly by 20% within 1 to 3 weeks from the breakout point, it has the potential to become a big bull stock and should be held for at least 8 weeks, or until it breaks below the 50-day moving average.

But the author did not simply launch this rule on a whim; instead, he used the project’s accumulated real historical replay ledger to conduct a rigorous backtest comparison. The results were shocking: **If blindly copying “rise 20% and hold dead until the 50-day moving average,” the single-trade cumulative returns of Korean stocks actually regressed by 43 percentage points, and US stocks by about 40 percentage points!**

Why did the master’s golden rule fail so severely in today’s market?

Because the short-term microstructure of today’s market is completely different from the 1960s. The author split the data and found: **In today’s market, stocks that surge 20% within 1 to 3 trading days after purchase are mostly emotional pulses stimulated by short-term news, not true institutional trend stocks.** After such stocks surge 20% in two or three days, the stock price is very far from the 50-day moving average below; if you mechanically execute “do not sell until breaking the 50-day moving average,” when short-term capital withdraws a few days later and the stock price drops rapidly, by the time you truly touch the 50-day moving average, the 20% floating profit has already been completely given back or turned into a loss.

Conversely, replay data shows that true long-term leading stocks are those that, within **4 to 15 trading days** after purchase, fully digest through sufficient turnover, steadily push up to +20%, and the stock price does not deviate excessively from the 50-day moving average at that time.

Based on this empirical data, the new rules launched by PRISM in early October this year made three clear corrections to O’Neil’s empirical rules:

1.  **Improved Leader Hold:** Stocks that surge 20% in 1 to 3 days do not enjoy exemption and still follow regular profit protection stop-loss to take profits in time; only stocks that rise 20% within 4 to 15 trading days and do not deviate excessively from the 50-day moving average enter “Leader Hold Mode”—holding for up to 40 trading days, as long as the closing price does not break the 50-day moving average and does not break the initial buy cost price.
2.  **AI Scenario-Based Position Adding Instead of Fixed Ladder Adding:** Abandon rigid “add 2%, add 4% mechanical adding,” change to buying 30% to 80% of one slot for the first position based on volatility, with the AI writing 2 to 4 position-adding trigger scripts at purchase (e.g., breaking a key level or stabilizing after a shrinking-volume pullback), executed by code when the price is higher than the cost and conditions are met.
3.  **Falsify and Abolish Ineffective Rules:** For example, the “Pocket Pivot” volume trigger proposed by later O’Neil disciples, and stop-losses set according to ATR volatility, were proven to have no positive returns or even worse in PRISM’s own historical data replay, so they were explicitly written into the abolition ledger and decisively abandoned by the author.

This iteration process is very persuasive. It reminds us that even when handing classic master frameworks to AI for automation, we must not be dogmatic: we must use large models to make up for the shortcomings of qualitative analysis, but we must also use real trading ledgers to correct half-century-old old parameters.

---

## /04 Understanding the Underlying Principles of AI Trading

At this point, many friends might ask: Since large models are so capable, will they completely replace traditional quantitative models in the future? What are the underlying taboos when using large models for trading?

### Large Models Cannot Predict Price Increases or Decreases Based Solely on Volume-Price Data

In the article *["Can LLMs Do Trading? Three Experiments Explain the Principles" (LLM CSI1000 Three Experiments)](/posts/factor-strategy/llm-csi1000-three-experiments)* published in mid-September this year, we conducted a set of progressive experiments based on Quantpedia’s ideas.

The starting point of the experiment was interesting: Researchers did not ask large models to directly predict tomorrow’s stock price increases or decreases. Instead, they first translated 20-day price changes, 20-day annualized volatility, and price deviation from the monthly moving average into discrete natural language states such as `Trend Upward | Volatility Low | Price Strong`, and then asked the large model to output three positions for position control: “Full Position, Half Position, Low Position.”

At that time, we were curious: Why not directly feed historical momentum features and future returns to the large model to let it learn the mapping relationship between momentum factors and future returns by itself? So we conducted extended experiments. The results of backtesting on CSI 1000 showed that although this scheme’s Sharpe ratio was slightly higher than Buy & Hold, its annual absolute return still underperformed Buy & Hold, and far lagged behind traditional machine learning models (such as tree models or neural networks).

Why do large models with hundreds of billions of parameters, claiming to know human knowledge, fail to beat even simple traditional machine learning when directly processing numbers and predicting prices? There are three underlying principles that are easily overlooked:

1.  **Tokenizers are “Number Colorblind” (Discontinuous Price Representation):** All inputs received by large language models are essentially text strings. In the preprocessing tokenization stage, continuous decimals in human eyes (e.g., `9.11`) are chopped by the tokenizer into `9`, `.`, `11` (or `9`, `.1`, `1`)—several unrelated Token combinations. Continuous price sequences are chopped at the first step.
2.  **High-Dimensional Vector Space Distance Distortion:** Mathematically, the distance between numbers 7, 8, 9 is equal (7 to 8 equals 8 to 9), and the distance from 7 to 9 is twice that of 7 to 8. But inside large language models, texts `7`, `8`, `9` correspond to three high-dimensional embedding vectors (Embeddings). The geometric distance of these three vectors in high-dimensional space does not naturally satisfy arithmetic equidistance. Distance is the core of arithmetic and regression; once distance is distorted, it is difficult for the model to calculate quantitative relationships accurately.
3.  **Transformers Lack Native Temporal Priors:** The sequence order of text Transformers is only given by positional encoding and causal masks (Causal Mask). They do not have the inductive biases of locality, periodicity, and state transitions inherent in specialized time-series models. All temporal patterns must be hard-learned from massive amounts of data.

Understanding these three underlying limitations explains why general-purpose large models in `nof1.ai` that directly look at charts and place orders lose miserably, and why PRISM-INSIGHT absolutely does not let large models calculate indicators directly, but instead honestly uses Python to convert volume-price into discrete text semantic signals like “breakout moving average,” “volume increase 30%,” etc., before handing them to large models for qualitative reasoning.

### What Large Models Are Really Good At: Generating Explicit “Market Expectation Benchmarks”

Since they cannot be used directly for price calculation, where lies the core incremental value of large models in financial trading? Besides supplementing `N` and `L` of CAN SLIM as mentioned earlier, the **Explaining Markets** global competition held by the University of Chicago Booth School of Business in collaboration with top global market maker Optiver (see *[Why Good News Doesn’t Mean Rise? AI Earnings Forecast Competition Revealed](/posts/tools/earnings-preview-with-llms)*) reveals another extremely important usage: **Generating explicit market expectations.**

When watching charts daily, we often hear: “A company’s stock price fell sharply after releasing financial reports because performance did not meet expectations; or despite a huge surge in performance, it opened high and fell low because good news was exhausted.” The most headache-inducing problem here is: **What is the “real expectation” of the market? Where does it come from?**

In financial markets, expectations usually come from three sources: one is sell-side analyst consensus (such as domestic Wind, East Money Choice, Chaoyang Yongshu summarized data); two is company management guidance (such as the interval given in the last quarterly conference call or performance forecast); three is the expectation derived from option market implied volatility. More troublesome is that when these sources have inconsistent calibers, or when there are higher buyer “Whisper Numbers” circulating in the market, looking only at the absolute numbers after financial report publication, AI cannot judge whether this is a surprise or a shock.

In the Q3 season of this competition, the organizers verified a very effective core technique: **Before the company’s financial report is released, send an Agent with full-network search capabilities to collect various calibers, industry dynamics, and market sentiment, and write a standardized “Financial Report Preview Research Report” in advance, explicitly fixing the expectation thresholds for Bull/Base/Bear scenarios.** When the financial report is truly released, let the model compare the actual performance with this pre-generated expectation benchmark. Experiments proved that just by this step of “pre-generating explicit expectations,” the model’s explanatory power ($R^2$) for stock price reactions after financial reports achieved a significant leap.

---

## /05 Practical Implementation Guide: Personal Deployment and A-Share Modification Ideas

Finally, let’s talk about the practical issues everyone cares about most: If you feel tempted after reading and want to deploy PRISM-INSIGHT to run yourself, or even modify it for use in the China A-share market, is it feasible? How much does it cost?

### Operational Cost Estimation

PRISM-INSIGHT itself is completely open-source (free for non-commercial use). The main daily expenses lie in large model Token consumption and search tool calls. According to the Korean developer’s own actual bill tests, if the entire process directly calls OpenAI series official APIs, it will cost about **$300+ per month**.

Of course, if you use subscription channel services, or replace information organization and daily summary links with domestic large models that currently have good cost-performance and capabilities, the monthly operational cost can be greatly compressed.

### Three Steps for A-Share Localization

The original PRISM-INSIGHT defaults to connecting only to Korean stocks (via KIS interface) and US stock data. Migrating it to the China A-share market is actually a very good geek engineering project, with core work mainly in three areas:

1.  **Connect Agent-Friendly Data Sources (Skills / MCP):**
    Note that a considerable portion of data in the PRISM architecture is autonomously called by Agents during reasoning. Therefore, we need to use MCP (Model Context Protocol) or Agent Skills technology to package traditional A-share data interfaces into tools that large models can directly call.
    The good news is that there are already many ready-made wheels available. For example, East Money previously launched a Skill for Agents to directly call market and fundamental data (we introduced this in *[Cyber Old Technicians Who Can Train AI, Quant Developers Should Also Start Installing Skills](/posts/uncategory/量化人也该开始装skills了)*); in addition, the familiar Tongda Xin recently launched an SDK for personal quantification, which also includes support for Agent calls (Note: Some hosted call methods will consume additional Token quotas, so pay attention to their billing rules during deployment).
2.  **Write A-Share Specific Trading System Constraints:**
    US and Korean stocks are T+0 trading, and US stocks have no price limit restrictions, while A-shares have strict **T+1 settlement systems** and **10% / 20% / 30% price limit restrictions**. This means the intraday stop-loss and early-month breakout chase logic in the original code must be added with T+1 holding lock periods and hard constraints for no buying at limit-up and no selling at limit-down.
3.  **Parameter Adaptation for Market Microstructure:**
    With the help of current AI Coding tools, the workload for data interface replacement and system rule modification in the first two steps is actually not large, and the code can be run through in a few days. **The most hidden and patience-testing modification is parameter adaptation for A-share microstructure.**
    As seen in the previous text, even O’Neil’s classic “8-Week Hold Rule” had to undergo drastic corrections when moved to today’s Korean and US stocks; A-share’s retail capital proportion, theme rotation speed, and limit-up ecology differ greatly from overseas markets. For example, “volume increase 30%” or “gap-up 1%” in the initial screening stage, or “rise 20% within 4 to 15 days” for holding leading stocks, directly moving to A-shares will likely result in acclimatization issues.

Therefore, the safest approach is: First reuse its multi-Agent perspective isolation architecture and post-market review framework, connect to A-share data, and run a period of simulated trading (Paper Trading) or historical replay, allowing the system to run out statistical patterns on its own in A-share’s real positive and negative examples (Big Movers vs. Lookalikes), and then gradually fine-tune trigger and take-profit parameters.

After all, even AI has learned to踏踏实实 (steadily) modify rules based on loss statements. As quants, what reason do we have to still迷信 (superstition) about a “Holy Grail” that works once and for all?
