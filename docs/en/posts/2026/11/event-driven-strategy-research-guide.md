---
title: "Event-Driven Arbitrage: Pricing Logic, Framework, and Real-World Cases"
date: 2026-11-25
slug: en/posts/2026/11/event-driven-strategy-research-guide
tags: [Event-Driven Arbitrage, Risk Arbitrage, Factor Investing, Quantitative Trading]
excerpt: "Deconstructing arbitrage pricing through the Deppon case: time value, risk premiums, and the four profit sources of event-driven strategies. Includes a 6-step institutional framework and actionable screening checklists for retail investors."
lang: en
translation_of: posts/2026/11/event-driven-strategy-research-guide
auto_translated: true
source_sha: 1284e0f1bccd234e6b6412b39d7bb1be1db1c0e1
---

On the evening of January 13, 2026, a major announcement rippled through the China A-shares market: **Deppon Shipping (603056.SH) proposed a voluntary delisting**. JD Logistics would acquire all outstanding floating shares for a cash consideration of **RMB 19.00 per share**.

Prior to suspension (January 8), Deppon’s closing price was only **RMB 14.04**. JD Logistics’ move offered a **35.33% cash premium**. Many retail investors placed orders overnight, even using multiple accounts to accumulate shares.

A 35% spread looks generous. But is this an opportunity or a trap?

The subsequent price action gave those who believed in the deal three consecutive limit-up days. However, after the limit opened, the stock hovered around **RMB 18.85** right up until suspension, rather than hitting the 19.00 target.

This left a tiny spread of **0.8%**. Small as it is, why would investors willingly forgo this money?

To understand the Deppon deal, focus on three points:

1.  **How to participate**: Buy on January 20, declare via the code "Deppon Cash" on February 9, and settle at **RMB 19.00** ([Declaration Announcement](http://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=603056&id=11946276)).
2.  **Cycle and Return**: The lock-up period crosses the Spring Festival, with funds arriving in about 38 days ([Clearing Announcement](https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=603056&id=11969570)). After fees, the net profit is approximately **0.72%**, annualized to about **6.9%**.
3.  **Nature of the Spread**: JD already holds over 80% of shares, has ample cash, and faces no anti-monopoly hurdles. The market treats 19.00 as a certainty. This 0.8% primarily represents the **time arbitrage fee** (including taxes) surrendered by funds unwilling to lock up over the holiday, plus a small "insurance premium" for tail risk—details of which follow.

Consider another common M&A scenario: Company A announces a cash acquisition of Company B at **RMB 20 per share** (pre-suspension price of 14), with an expected 6-month settlement. Upon resumption, B’s stock trades at **RMB 18**, leaving a thick spread of **2.00 yuan (11.1%)**.

This is not a theoretical exercise. In real-life mega-deals like Microsoft’s acquisition of Activision Blizzard or Musk’s acquisition of Twitter, the potential upside relative to market price once reached **20%–66%**.

Why does the Deppon deal leave only a 0.8% arbitrage fee, while other cases leave spreads of 10% or more?

Comparing these two examples reveals the pricing logic of event-driven strategies. Next, we calculate this pricing anchor and systematically deconstruct the profit sources, research framework, and practical screening checklist for event-driven investing.

## /01 Best Bid

When you see an event news item, the first question is: If you participate, what price should you bid?

Taking Deppon as an example, the final suspension price cannot be 19.00; otherwise, arbitrageurs could not even cover transaction fees and taxes. So, where will the market ultimately price it? If you know this final pricing $x$, you know how to participate: as long as the previous trading day’s closing price is below $x/1.1$ (approx. $0.909x$), the next day’s limit-up price will not exceed $x$, allowing you to safely place limit-up orders to accumulate shares; if the stock price exceeds this level, as long as the buy price is below $x$, there is still profit. Thus, the key is to calculate $x$ first.

This requires understanding the pricing principles in M&A events.

Any M&A or delisting spread is composed of three hard costs: **risk-free time value + transaction taxes/fees + risk premium for transaction failure (including liquidity discount)**. Remarkably, this calculation can be precise to two decimal places.

Let’s run a test calculation for **Deppon Shipping**. Assume that around late January 2026, the market’s risk-free benchmark—reverse repo on government bonds—had an annualized rate of **1.4%**. From buying on January 20 to funds arriving at the end of February, the lock-up period is about **38 days**. Working backward from 19.00:

1.  **Risk-free time value**: Calculated at 1.4% reverse repo, the 38-day yield is only $1.4\% \times \frac{38}{365} \approx 0.15\%$, approx. **RMB 0.028 per share** (less than 3 cents).
2.  **Two-way transaction taxes/fees**: Buying commission plus stamp duty and commission on exercise/transfer (charged at standard A-share selling rates) total about 0.08%, approx. **RMB 0.015 per share**.
3.  **Risk and liquidity premium**: At suspension on January 20, the extraordinary general meeting on January 29 had not yet convened. By rules, the voluntary delisting proposal requires approval by two-thirds of voting rights held by shareholders present, and two-thirds of voting rights held by minority shareholders present. If a low-probability意外 rejection occurs, the stock price could fall back to the pre-suspension 14.04, causing an instant loss of **RMB 4.81 per share (-25.5%)**. If the market assigns a **2%** probability to this意外, the actuarial insurance premium is $2\% \times 4.81 \approx \mathbf{0.096 \text{ yuan}}$.

Summing these three items: **0.028 (time value) + 0.015 (taxes/fees) + 0.096 (2% failure insurance) = 0.139 yuan**. Subtracting 0.139 from 19.00, the theoretical price is exactly $x = \mathbf{18.86 \text{ yuan}}$—almost identical to the January 19 closing price of **18.86 yuan** and the January 20 closing price of **18.85 yuan**!

With this anchor price $x = 18.86$ yuan ($x / 1.1 \approx 17.15$ yuan), how to bid on each day after Deppon resumes becomes a primary school arithmetic problem (assuming a 10% limit-up on the main board, rounded to cents):

*   **January 14 (15.44 yuan), January 15 (16.98 yuan), January 16 (18.68 yuan)**: The limit-up prices for these three days are all below 18.86 yuan, so you can **directly place limit-up orders to accumulate shares**. Especially buying on the 14th and 15th offers a safety margin of 11%–22%; even if you queue at 18.68 on the 16th, there is still nearly 1% profit margin before 18.86.
*   **January 19, January 20 (must open)**: Because the limit-up price on the 4th reaches $18.68 \times 1.1 = \mathbf{20.55 \text{ yuan}}$, far exceeding the 19.00 acquisition price, the limit will inevitably open. After opening, you must no longer blindly place limit-up orders; **you can only buy at prices below 18.85–18.86 yuan**.

Another question: Before suspension, the stock price stabilized around 18.85 yuan, with easy execution for both buying and selling. Should you hold shares or hold cash (switch to reverse repo)? This requires comparing the annualized returns of both schemes. Holding Deppon requires a lock-up of about 38 days, with an annualized return of about 6.9% after fees; holding cash yields only 1.4%, but carries no risk (if the delisting proposal is rejected, the stock price will likely fall back to around 14.04, a loss of approx. 25%), and allows flexibility to enter the stock market after the holiday.

More interestingly: **Who, exactly, pinned the price so precisely at 18.85 yuan?** The answer is **professional arbitrage capital** (brokerage proprietary trading, low-volatility private equity, quantitative cash management pools). For retail investors, locking up 100,000 yuan for 38 days to earn 720 yuan is troublesome and risks missing out, so retail investors are the main sellers after the limit opens; but for institutional idle capital managing hundreds of millions of yuan, which typically earns only 1.4% from reverse repos, Deppon’s volume exceeding 3.5 billion yuan over two days on January 19–20 is a high-quality "quasi-fixed income" deal with ample capacity and nearly 7% annualized return. Large capital uses models to lock in target annualized thresholds, placing massive support orders at 18.84–18.86 yuan—prices below 18.84 are swept instantly, while prices above 18.87 offer insufficient annualized return, so large capital stops chasing. The extremely narrow 3-cent amplitude throughout the day is precisely **nail-by-nail calculated by the marginal pricers with their calculators**.

Now, apply the same ruler to an M&A case with a **20 yuan acquisition price and 18 yuan current price**, and the picture changes completely.

Assuming a risk-free rate of 3% and a 6-month settlement, the capital time cost is only $18 \times 3\% \times 0.5 \approx \mathbf{0.27 \text{ yuan}}$. The remaining approx. **1.73 yuan** is almost entirely the **failure insurance premium** demanded by the market—this is true **Risk Arbitrage** on Wall Street.

Harvard Business School’s Malcolm Baker and Serkan Savasoglu analyzed 1,901 US M&A cases from 1981–1996 ([Limited Arbitrage in Mergers and Acquisitions, JFE 2002](https://www.hbs.edu/ris/Publication%20Files/arbitrage_af05900b-acd4-44db-8210-70a9fbc3cf6c.pdf)). They offer a vivid metaphor: M&A arbitrageurs are essentially **selling insurance**. Original shareholders fear the deal might fail and the stock price might crash in the coming months, preferring to exit at a discount; arbitrage funds have limited capital and fear losses, so they demand a generous premium.

Professional arbitrageurs calculate the cost before placing orders using the **implied success probability formula**. Let the current price be $P_0$, the acquisition price be $P_{offer}$, and the "floor price" if the deal fails and the stock drops be $P_{down}$. Ignoring dividends and interest, the break-even success probability $p^*$ for zero profit/loss is:

$$
p^* \times (P_{offer} - P_0) - (1 - p^*) \times (P_0 - P_{down}) = 0 \implies p^* = \frac{P_0 - P_{down}}{P_{offer} - P_{down}}
$$

Plugging in the two cases, the gap is obvious:

*   **Deppon Shipping (19.00 yuan exercise, 18.85 yuan close, 14.04 yuan floor)**: $p^* \approx \mathbf{97.0\%}$. After deducting time costs and taxes, the market-implied success rate is as high as **98%**, a low-risk arbitrage.
*   **20 yuan acquisition, 18 yuan current price, 14 yuan floor**: $p^* = \frac{18 - 14}{20 - 14} = \mathbf{66.7\%}$. The market believes there is a one-third probability of failure! This deal is only worth placing if your due diligence confirms the true win rate is significantly higher than 66.7% (e.g., 85%).

But don’t think calculating $p^*$ guarantees easy profits. Mark Mitchell and Todd Pulvino studied 4,750 M&A cases from 1963–1998 ([Characteristics of Risk and Return in Risk Arbitrage, Journal of Finance 2001](https://ideas.repec.org/a/bla/jfinan/v56y2001i6p2135-2175.html)), exposing the fatal weakness of this strategy: In calm or rising markets, M&A arbitrage returns are almost unrelated to the broader market; but when the stock market crashes, deal failure rates rise sharply, and arbitrage portfolios fall in sync with the market.

Its return curve resembles **selling naked put options**—steadily collecting small premiums normally, but potentially losing years of profits in a single black swan event. After deducting risks and transaction costs, long-term annualized excess returns are around **4%**.

How is this pricing logic applied in real battlefields? Look at two recent US mega-deals, one **positive and one negative**, where ordinary investors can directly extract actionable trading disciplines.

### Positive Case: Musk’s Acquisition of Twitter

In April 2022, Musk signed to acquire Twitter for **$54.20** in all cash ([Twitter SEC Filing](https://d18rn0p25nwr6d.cloudfront.net/CIK-0001418091/bfcefac6-7b00-4d5f-9e6a-fc72218de9df.pdf)). Then, tech stocks crashed, and on July 8, he sent a letter to terminate the deal ([PR Newswire](https://www.prnewswire.com/news-releases/twitter-board-confident-in-merger-agreement-and-intends-to-close-transaction-at-54-20-per-share-price-301583272.html)). The market panic drove Twitter down to **$32.65** ([Fortune](https://fortune.com/2022/07/12/elon-musk-twitter-deal-stock-price/)), creating a potential upside of up to **66%**.

Hedge funds hired top lawyers to meticulously review the contract, confirming Musk signed strict **specific performance clauses**, and the Delaware court would likely rule he must pay up ([Goodwin Law](https://www.goodwinlaw.com/en/insights/publications/2022/07/07_26-securities-snapshot)). Greenlight Capital founder David Einhorn publicly calculated the deal at the time: buying at $37, winning earns $17, losing loses $17—**the market gave a 50/50 win rate, while they judged the true win rate to be over 95%** ([Forbes](https://www.forbes.com/sites/hanktucker/2022/11/16/elon-musks-twitter-buyout-was-a-billion-dollar-windfall-for-these-13-hedge-funds/)). Ultimately, in October, Musk capitulated and performed at $54.20 ([Wikipedia](https://en.wikipedia.org/wiki/Acquisition_of_Twitter_by_Elon_Musk)). The 13 hedge funds that bought the dip collectively earned **over $1 billion**, with Carl Ichan netting approx. $250 million ([Fortune](https://fortune.com/2022/10/05/elon-musk-u-turn-twitter-arbitrage-traders-investors-billionaire-carl-icahn-laughing-bank/)).

**How can ordinary investors implement this?** Retail investors previously faced two dead walls in such trades: hundreds of pages of M&A agreements are hard to understand, and domestic private equity holdings are not public, making it impossible to "copy homework." But in the **AI era**, these two walls have been completely breached, allowing ordinary people to get started in three steps:

1.  **Calculate implied win rate $p^*$ in 30 seconds**: Input three numbers—the acquisition price $P_{offer}$, current price $P_0$, and estimated floor price $P_{down}$ after deal failure (reference pre-announcement price, adjusted for fundamentals and broader market trends during the period). For Twitter, with a $54.20 acquisition price, $37 current price, and $20 estimated floor, $p^* = (37 - 20) / (54.20 - 20) \approx 50\%$, immediately revealing the market only gave a 50/50 win rate.
2.  **Feed the announcement PDF to AI to act as your "free M&A lawyer"**: Upload hundreds of pages of restructuring drafts or acquisition agreements directly to large models, asking them to check four hard indicators line-by-line—**Is it a formal agreement or an oral intent? Are there specific performance clauses or high breakup fees? Is the acquisition funding from own cash or uncertain private placements? Which regulatory and shareholder approvals are required?**
3.  **Use AI with financial databases to check historical precedents**: Some AI products now integrate professional financial databases, at much lower cost than traditional financial terminals costing tens of thousands of yuan per year. Directly ask AI to retrieve historical pass rates, precedent trends, and buyer performance records for similar M&A cases. After obtaining an objective win rate, compare it with the $p^*$ calculated in step one—this is the truly replicable hardcore gameplay for retail investors.

### Negative Case: JetBlue’s Acquisition of Spirit Airlines

In July 2022, JetBlue signed to acquire budget airline Spirit Airlines (SAVE), with a cash bid of **$33.50** (up to **$34.15** including extension fees, [SEC Filing](https://www.sec.gov/Archives/edgar/data/1498710/000119312522229137/d378607dprem14a.htm)). After the US Department of Justice sued for anti-monopoly reasons, the stock price fell to around **$15** before the January 2024 judgment—seemingly offering doubling space, attracting many retail investors and arbitrage funds.

On January 16, 2024, a federal judge ruled to block the deal. Spirit Airlines’ intraday price dropped over **50%**, closing down **47%** to **$7.92** ([Quartz](https://qz.com/spirit-airlines-stock-jet-blue-merger-blocked-1851170021); [Forbes](https://www.forbes.com/sites/antoniopequenoiv/2024/01/16/spirit-airlines-stock-plummets-over-50-after-jetblue-deal-blocked/)). After the deal was canceled in March, the stock price fell below $5.80 and slid toward bankruptcy restructuring due to heavy debt ([Quartz](https://qz.com/spirit-airlines-stock-price-jetblue-merger-cancelled-1851305688); [XTB](https://www.xtb.com/int/market-analysis/news-and-research/spirit-airlines-slump-pushes-airline-stocks-up)).

**How can ordinary investors avoid pitfalls?** This iron rule is more practical than finding positive cases: **Check the financial statements before placing orders, asking only one question—“If the acquisition is canceled tomorrow, can this company survive on its own without selling itself?”** Retail investors may not see through anti-monopoly lawsuits, but anyone can instantly see Spirit Airlines’ years of massive losses and heavy debt. Once talks collapse, the floor price $P_{down}$ is the floor price. For any target that is continuously bleeding and relies entirely on selling itself to survive, regardless of how tempting the spread, give it an immediate veto.

## /02 Beyond M&A: Where Else Can Event-Driven Strategies Make Money?

M&A arbitrage is easy to understand because there is a白纸黑字 (black-and-white) acquisition price as an anchor. So, where does the money come from for events like spin-offs, index rebalancing, and share buybacks—**events with no fixed acquisition price**?

Looking at all event-driven strategies, the core actually consists of **four money-making mechanisms**:

| Strategy Type                  | Typical Events                                       | Counterparty Who?                        | What Money Is Made?                     | Return Characteristics                     |
| :----------------------------- | :--------------------------------------------------- | :--------------------------------------- | :-------------------------------------- | :----------------------------------------- |
| **Risk Underwriting & Certainty Arbitrage** | M&A, Privatization, Voluntary Delisting              | Original shareholders fearing delays & wanting to lock in profits | Time cost + Failure "Insurance Premium" | High win rate, low payout (anti-black swan) |
| **Non-Fundamental Forced Buying/Selling** | Spin-offs, Index Rebalancing, Rating Downgrades      | Institutions restricted by rules, must mechanically buy/sell | Liquidity compensation + Mispricing repair | Higher win rate, depends on chip mismatch depth |
| **Information Lag (Underreaction)** | Earnings Good/Bad News (beat/miss), Large Buybacks   | Traditional funds with fixed views & slow rebalancing | Price drift from gradual information realization | Longer cycle, requires factor filtering     |
| **Governance Improvement & Value Catalyst** | Activist Shareholder Entry, Bankruptcy Restructuring | Management lacking motivation or in困境       | Valuation repair from governance improvement | Long cycle, high divergence, extreme due diligence required |

Below, we pick the three most representative types to see how institutions actually execute.

### 1. Spin-offs: Picking Up Chips "Forced to Sell by Institutions"

When a large company spins off a smaller business and directly distributes new shares proportionally to existing shareholders, a strange phenomenon often occurs: many institutions **don’t even look at the financial reports and smash the stock blindly at the open**.

The reason is simple—rules constrain them. Large-cap funds tracking the S&P 500 have contracts prohibiting holding small-cap stocks outside the index; industry funds cannot hold cross-industry stocks; new companies are just independent, with no sell-side research reports yet, so institutional risk control directly clears positions.

Patrick Cusatis, James Miles, and J. Randall Woolridge analyzed 146 pure spin-offs from 1965–1988 ([Restructuring through spinoffs, JFE 1993](https://longrunplan.com/wp-content/uploads/2018/09/restructuring-through-spinoffs.pdf)), finding that spin-off subsidiaries and parent companies had significant excess returns for up to 3 years post-spin-off. The reason is not just mispricing repair, but also more focused management incentives and easier becoming independent M&A targets.

Hedge fund legend Joel Greenblatt told a legendary case in his classic book [《Stock Market Genius》（You Can Be a Stock Market Genius）](https://books.google.it/books?id=5dQnKZR0h7wC&lr=&hl=it&source=gbs_navlinks_s): In 1993, Marriott spun off its light asset management business (Marriott International) and heavy asset hotel business (Host Marriott). At the time, everyone despised Host Marriott, and institutions sold at any cost, creating a golden pit, followed by a massive stock price surge over subsequent months ([Case Review](https://manassaloi.com/booksummaries/2016/03/09/stock-market-genius-joel-reenblatt.html)).

The recent textbook case is **General Electric’s (GE) three-way split**. GE spun off its healthcare business GE HealthCare in January 2023 ([GE News](https://www.ge.com/news/press-releases/ge-completes-separation-of-ge-healthcare)), and its energy business GE Vernova in April 2024 ([GE Vernova](https://www.gevernova.com/news/press-releases/ge-vernova-completes-spin-off-begins-trading-new-york-stock-exchange)). After shedding the "large and comprehensive" valuation burden, GE’s stock price surged approx. **129%** from the healthcare spin-off to March 2024, outperforming the S&P 500 index by approx. **96%** ([Forbes](https://www.forbes.com/sites/joecornell/2024/03/05/ge-massively-outperforms-the-index-as-spin-off-unlocks-value/)).

### 2. Index Rebalancing: From "Front-Running Passive Funds" to "Anti-Crowding"

Early index rebalancing arbitrage was simple: stocks added to major indices forced tracking ETFs to mechanically buy according to rules, pushing stock prices up. Andrei Shleifer confirmed significant positive excess returns from S&P 500 additions as early as 1986 ([Do Demand Curves for Stocks Slope Down?, Journal of Finance 1986](https://shleifer.scholars.harvard.edu/publications/do-demand-curves-stocks-slope-down)); Honghui Chen et al. later found that additions have persistent premiums, while deletions often rebound and repair ([Journal of Finance, 2004](https://www.researchgate.net/publication/4992686_The_Price_Response_to_SP_500_Index_Additions_and_Deletions_Evidence_of_Asymmetry_and_a_New_Explanation)).

**But copying the old playbook now easily makes you a bag holder.**

New research by Robin Greenwood and Marco Sammon ([The Disappearing Index Effect, HBS / JF](https://www.hbs.edu/ris/Publication%20Files/23-025_563e45c6-df92-4d9c-ae05-608d4d0acab1.pdf)) found that the S&P 500 index effect in US stocks has shrunk significantly over the past decade. The reason is realistic: on one hand, many stocks only "promoted" from mid-cap indices, so net buying is not that large; on the other hand, too many hedge funds front-run and埋伏, exhausting all gains in advance.

The most extreme case was **Tesla’s inclusion in the S&P 500 in December 2020**. At the time, funds tracking the S&P 500 exceeded $4.6 trillion ([Dimensional](https://www.dimensional.com/ca-en/insights/teslas-charge-reveals-weak-points-of-indexing)), with Tesla’s weight at 1.56% ([SustainableInvest](https://sustainableinvest.com/tesla-now-eligible-for-addition-to-the-sp-500-esg-index/)). Front-running funds pushed the stock price skyward before effectiveness. Research Affiliates later calculated: if you **shorted Tesla and went long on deleted stocks AIV at the close on December 18 when rebalancing took effect**, you could earn a relative excess return of **78.6%** in just 6 months ([RAFI](https://www.rafi.com/research/publications/articles/832-revisiting-teslas-addition-to-the-sp500))!

In China A-shares, due to limited short-selling tools, the gameplay is different. Tsinghua Wudaokou’s research confirms that CSI 300 rebalancing indeed involves passive fund impact ([Regression Discontinuity Empirical Study](http://cfrc.pbcsf.tsinghua.edu.cn/__local/7/A1/2F/3439A97D91C0913CDC56FC9521E_597DEABF_14507A.pdf?e=.pdf)); but a paper in 《Financial Research》 points out a hidden big pit ([Tail Becoming Head: Neglected Index Component Stock Exchanges](http://www.jryj.org.cn/CN/abstract/abstract758.shtml))—many "tails" deleted from the CSI 300 turn into "heads" with large weights in the CSI 500, with net capital actually flowing in. Blindly shorting "deleted" stocks can easily lead to being counter-killed.

### 3. Easily Ignored "Slow Events": Earnings Drift, Buybacks, and Activist Shareholders

Besides the above structural trades, there are three types of "slow-burning" events with equally惊人 (stunning) long-term win rates:

*   **Post-Earnings Announcement Drift (PEAD) on Beats**: Good earnings reports do not rise in one day. Victor Bernard and Jacob Thomas found that portfolios long extreme beats and short extreme misses earn an average of **4.19%** more over 60 days post-announcement, expanding to **7.74%** over 180 days ([Journal of Accounting Research, 1989](https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html); [ResearchGate](https://www.researchgate.net/publication/2770487_Post-Earnings_Announcement_Drift)).
*   **Large Stock Buybacks**: David Ikenberry et al. found an average excess return of **12.1%** over 4 years post-public market buyback announcements; but adding a filter—only buying undervalued "value stocks"—sends 4-year excess returns soaring to **45.3%**, while buybacks of high-valuation hot stocks are almost useless ([JFE, 1995](https://ideas.repec.org/a/eee/jfinec/v39y1995i2-3p181-208.html)).
*   **Activist Shareholder Entry**: Alon Brav et al. found that when activist hedge funds push for company reforms via entry, announcements bring approx. **7%** abnormal returns near the announcement period, which are not given back in the following year ([Journal of Finance, 2008](https://www.researchgate.net/publication/4992790_Hedge_Fund_Activism_Corporate_Governance_and_Firm_Performance)).

## /03 How Do Professional Institutions Conduct Event Strategy Research?

After discussing opportunities, back to the core question: If you really want to turn event-driven into a replicable strategy, rather than just looking at stories and guessing, how should you systematically research?

Regular quantitative and event-driven funds generally strictly complete the following **6-step closed loop**:

### Step 1: Clearly State Logical Assumptions Before Running Data

Before touching data, you must answer three soul-searching questions: **Who is your counterparty? Since the news is public, why are they willing to sell to you at a loss? Why won’t this spread disappear in 1 day?** If you cannot find institutional constraints (e.g., index fund contract restrictions) or risk transfer needs (e.g., M&A insurance premium), the "high returns" you backtest are likely historical coincidences.

### Step 2: Verify Identity Using Standard Event Study Method

To verify whether an event truly generates excess returns, the industry standard is the standardized framework established by A. Craig MacKinlay ([Event Studies in Economics and Finance, JEL 1997](https://ideas.repec.org/a/aea/jeclit/v35y1997i1p13-39.html)) and the econometrics guide by S. P. Kothari and Jerold B. Warner ([Econometrics of Event Studies, 2007](https://www.bu.edu/econ/files/2011/01/KothariWarner2.pdf)). Focus on three things:

1.  **Pinpoint the "zero point" $t=0$**: Announcements made after market close (e.g., Deppon’s evening announcement on January 13) must be delayed to the next trading day (January 14) for trading; never make the mistake of using future data for backtesting ("look-ahead bias").
2.  **Strip out the broader market to calculate pure excess returns**: Estimate the stock’s normal trend using the $[-250, -30]$ trading days before the event, then use actual returns minus model-predicted normal returns (or broader market/style benchmark returns) within the event window $[-10, +60]$ to accumulate Cumulative Abnormal Returns ($CAR$) and the full sample mean ($CAAR$).
3.  **Plot curves, prevent statistical illusions**: Good events should not significantly front-run before $t<0$ (otherwise it means news leaked early), and should move decisively after $t \ge 0$. Also be careful of **Event Clustering**—e.g., earnings concentrated in the same month, index rebalancing effective on the same day, causing stocks to rise and fall together. Do not directly treat them as independent samples to calculate significance; must use Calendar-Time Portfolio methodology for cross-verification.

### Step 3: Conditional Grouping to Filter Noise

The "full-market average" of almost all event strategies is mediocre; true暴利 (super profits) lie in **secondary screening**. Just like Ikenberry’s (1995) buyback research: full sample 4-year excess return was only 12.1%, but picking only low-valuation value stocks raised it to 45.3%. When researching, you must split backtests by business characteristics:

*   **M&A**: Split to see cash vs. stock swaps, friendly vs. hostile, industry consolidation (prone to anti-monopoly) vs. cross-industry M&A.
*   **Buybacks**: Strictly monitor "buyback for cancellation" vs. "equity incentives," buyback amount as a percentage of floating shares, and whether the company’s free cash flow is sufficient.
*   **Index Rebalancing**: Calculate **net passive inflow / past 20-day average turnover**, and conveniently filter out pseudo-good news where "cross-index migration results in negative net inflow."

### Step 4: Account for All Real Transaction Costs

Event stocks often "look beautiful" in backtests but lose money in live trading. Three costs must be deducted strictly:

*   **Limit-up Days and Slippage**: Stocks hitting limit-up on the day after announcement (e.g., Deppon pulling 3 limit-ups in a row) are impossible to buy. Backtests must use **actual executable open-limit prices or next-day average prices** for position building, never pre-announcement closing prices.
*   **Shorting Costs**: Stock-swap M&A requires simultaneously shorting the acquirer to lock spreads. If securities sources are tight and annualized shorting fees reach 10%, seemingly attractive spreads are instantly eaten up.
*   **Capital Capacity**: Event strategies are inherently low-capacity; buying too much will erase the spread yourself. Must calculate return decay under different capital volumes.

### Step 5: Guard Left-Tail Risk, Never Heavy-Position Single Cases

Since M&A arbitrage is essentially "earning small money normally, losing big money when things go wrong," risk control is more valuable than stock picking:

*   **Position Sizing Based on Max Loss**: Do not use equal weighting; derive position sizes based on $P_0 - P_{down}$—e.g., stipulate that a single case failure should never impact portfolio NAV by more than 1%–1.5%.
*   **Prevent Hidden Homogeneous Risk**: Do not heavy-position 5 tech M&A deals all stuck in US anti-monopoly reviews (FTC or DOJ). Although buying 5 stocks, you are actually betting on the same regulatory attitude.
*   **Buy Tail Protection**: For the "deal failure clustering during market crashes" risk discovered by Mitchell & Pulvino (2001), mature funds allocate a small portion of returns to buy out-of-the-money index put options to hedge systemic crashes.

### Step 6: Monitor Crowding, Exit Decisively When Strategy Fails

There is no permanent money-printing machine in financial markets. Just as the S&P 500 index effect gradually disappeared in Greenwood & Sammon’s research, live trading must build a **crowding monitoring table**: closely watch announcement-day gap-up magnitude, historical arbitrage spread percentiles, and shorting fee rate anomalies. Once front-running is too fierce, and remaining profit margins cannot even cover tail risks, either reduce positions or turn counter-party to the crowded funds.

## /04 How to Distinguish "Real Opportunities" from "Fake Noise" at a Glance When Seeing an Announcement?

Finally, back to daily practice. Announcements fly everywhere daily; how to decide in 30 seconds whether an announcement goes into the tracking list or is directly crossed out? The core lies in two points: **Are there calculable hard capital constraints? Is management’s interest aligned with yours?**

| Event Type               | Add to Tracking List (Worth Deep Dive)                                                                                                                                                                                                                   | Looks Hot, Cross Out Immediately (Likely Noise)                                                                                                                                                       |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M&A and Delisting**    | 1. Signed legally binding formal agreements, specifying breakup fees or specific performance (e.g., Twitter case), or major shareholders offering clear cash selection rights (e.g., Deppon case);<br>2. Cash acquisition with funds in place, not relying on high-leverage financing;<br>3. Market smashes deep pits due to short-term litigation or regulatory panic, and floor price $P_{down}$ has solid fundamental support.          | 1. Only issued non-binding "letters of intent/framework agreements";<br>2. Cross-industry hot-topic chasing, absurd valuation premiums, relying on private placements to raise funds;<br>3. Targets themselves losing money year after year with high debt, facing bankruptcy risk if talks collapse (e.g., Spirit Airlines case).                     |
| **Spin-offs**            | 1. Directly "physically distributing" subsidiary stocks to existing shareholders, with subsidiaries small or cross-industry, inevitably forcing **mechanical smashing by index funds**;<br>2. Post-spin-off management receives independent equity incentives, with core businesses previously buried by the parent company starting to exert force.                                                                   | 1. "Partial equity IPO spin-offs" just for fundraising, where existing shareholders are not forced to smash;<br>2. Parent companies use spin-offs to dump rotten businesses and huge debts onto subsidiaries;<br>3. "Spin-off concepts" already hyped sky-high before announcement, valuations more expensive than peers.                       |
| **Index Rebalancing**    | 1. Rules transparent and list calculable in advance, with passive net buying funds exceeding 3–5 times daily turnover;<br>2. Clarify cross-index linkages (e.g., deleted from CSI 300 but added to CSI 500), only doing targets with clear net impact direction and not over-front-run;<br>3. Encountering extreme crowding like Tesla’s massive inclusion, reverse-monitor **mean reversion post-effectiveness**. | 1. Tracking funds extremely small for edge or thematic index adjustments;<br>2. Chasing highs after announcement for "star rebalancing stocks" that already surged;<br>3. Not checking cross-index exchanges, blindly shorting upon seeing "deleted."                                                  |
| **Share Buybacks**       | 1. **Buyback for cancellation** (real money boosting EPS), amount high as percentage of floating shares (e.g., above 3%–5%);<br>2. Company low valuation, good cash flow, historical buyback commitments kept;<br>3. Executives simultaneously buying with their own money in secondary market.                                                                | 1. "Pie-in-the-sky" buybacks: ceilings blown high, floors pitifully low, or only used for employee incentives without cancellation;<br>2. High-valuation hot stocks symbolically buying back at highs to defend;<br>3. Habitual offenders who repeatedly issue increase/buyback plans with much fanfare but little action.                   |
| **Earnings and Forecasts** | 1. Deducted net profit, revenue growth significantly **higher than market consensus expectations** (not just year-on-year increases), driven by main business volume;<br>2. Stock gaps up with volume on earnings day and does not fill gaps in subsequent days, accompanied by密集 sell-side earnings upgrades (typical PEAD starting point).                                                   | 1. Performance high growth but **lower than market high expectations** (typical "sell the news"), or relying entirely on non-recurring gains/government subsidies to polish;<br>2. Rushing to "buy the dip" after earnings miss hitting limit-down—PEAD empirical evidence shows negative surprise drift often lasts 1–3 months. |

Ultimately, masters of event-driven investing do not look at "how explosive the news is," but rather **contractual terms, rigid capital constraints, and asymmetric pricing of probability and payout**.

When you see an announcement, stop conditionally asking "Is this good or bad news," and instead habitually pick up your calculator to ask: **"Which capital is forced to buy or sell at what time and price due to this news, and what is my worst-case floor?"**—only then have you truly stepped through the door of event-driven strategies.
