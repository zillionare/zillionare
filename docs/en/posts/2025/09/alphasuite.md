---
title: "AlphaSuite: A Lean Quant Framework with CANSLIM & Risk Prompts"
date: 2025-09-17
slug: en/posts/tools/alphasuite
tags: [Quant Framework, Llm Prompts, Canslim, Streamlit]
excerpt: "AlphaSuite offers a lightweight, open-source quantitative framework for individual developers. It integrates CANSLIM models and LLM-driven risk prompts, prioritizing rapid prototyping over production-grade complexity."
lang: en
translation_of: posts/tools/alphasuite
auto_translated: true
source_sha: 7061a58f913b2cc1b3f7bb56f1ab5a23ad1d2112
cover: "https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/square/food/16.jpg"
---

Many quantitative researchers build their own libraries, investing significant time in the process. Is it truly worth it? My personal answer is yes, because I am among the countless developers who have built their own "wheels."

The value of exploration lies in the exploration itself. Physicist Richard Feynman left behind many quotes, one of which perfectly explains why it is worthwhile to repeatedly build wheels:

!!! info
    What I cannot create, I do not understand.
    This phrase was found on the blackboard in Feynman’s office after his death in February 1988.

Drivers in the last century often repaired their own cars. Some sailors prefer to build their own sailboats. Quant developers who build their own frameworks are similar. What we may be pursuing is not necessarily to build a giant ship that never sinks, but to learn to listen to the wind and understand the waves while assembling each plank and calibrating every rope.

Today, I introduce a project open-sourced on GitHub just three weeks ago, with only a handful of stars. Despite its small size—consisting of roughly 30 files, each around 250 lines—it provides a valuable reference model for a specific group: those with some trading experience and programming skills, but who are not professional developers (although the author of AlphaSuite appears to have a strong AI background) and cannot invest significant time in building complex systems.

More importantly, the author seems to possess substantial domain expertise, providing prompts for building risk warning and CANSLIM analysis strategy models.

## 1. The Origin of AlphaSuite

This library demonstrates how to quickly build a "small yet functional" personal investment research system around your own investment philosophy. According to the author, he developed several strategy models based on LightGBM that performed well in the US and Canadian markets, prompting him to open-source the project:

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250916210416.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>Backtest curve, provided by Richard Shu</span>
</div>

Of course, one must treat any return curves seen here with caution. Furthermore, the author has not disclosed his actual model. Although LightGBM is used in the code, neither the feature engineering nor the final model are included. The only strategies explicitly provided in the code are the dual moving average strategy and the Donchian Channel strategy.

## 2. How to Use LLMs for Risk Warning Searches?

The `News_Intelligence.py` file in this library is worth reviewing. It defines several classic macro-risk frameworks, such as "Credit and Real Estate Crisis," "Inflation and Federal Reserve Policy Shocks," "Geopolitical and Supply Chain Disruptions," and "Technology Sector Health and Concentration Risk." For each framework, the author has defined corresponding prompts. While this functionality has not yet been implemented, the prompts used can serve as a reference. Here is an excerpt:

```md
Focus on signs of stress in credit markets and real estate. Look for:
- News about rising corporate or consumer loan defaults.
- Failures or significant distress in regional banks, especially related to 
Commercial Real Estate (CRE) loans.
- Reports of falling commercial property values or rising office vacancies.
- Warnings from credit rating agencies about specific sectors or companies.
- A sudden freeze in the high-yield ("junk") bond market.
```

## 3. The CANSLIM Model

Another interesting aspect of this project is its introduction of the CANSLIM investment model. CANSLIM is a classic growth stock investment strategy proposed by William O’Neil. Its core is to screen for high-quality stocks with high growth potential that can consistently outperform the market through seven key dimensions, essentially a stock selection framework combining "fundamentals + technicals."

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/CANSLIM.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>CANSLIM Model</span>
</div>

To implement this analysis, it uses the following prompt:

```md
You are a financial analyst specializing in the CANSLIM investment strategy. 
Analyze the provided data for {ticker}.

**Ticker:** {ticker}
**Company Information:** {company_info}
**Recent News Snippets:** {company_news}
**Overall Market Posture (SPY Trend):** {market_posture}
**Competitive Landscape Summary:**
{industry_analysis_summary}
**CANSLIM Metrics Table:**
{canslim_metrics_md}

**Analysis Task:**
Provide a concise and confident analysis based on the data.

1.  **CANSLIM Summary:** Briefly evaluate the stock against the key CANSLIM 
criteria (Earnings, Financial Strength, Relative Strength, Volume).
2.  **"N" Factor (New Things):** Discuss any new products, management 
changes, or significant news that could act as a catalyst.
3.  **Investment Thesis:** Conclude with a clear Bull vs. Bear thesis, 
considering its position within its industry. What are the primary reasons to
 be bullish or bearish on this stock right now?

Present your analysis in a structured, easy-to-read format.
```

This is only a partial list. In the `technical_analysis_tools.py` file, there are additional prompts regarding technical indicator analysis:

```md
...

Analyze trends and signals across daily, weekly, and monthly timeframes. 
Identify confirmations and divergences between timeframes.  Note instances
 where timeframes support or contradict each other.

Indicators and Price Action Analysis:

* Price trends, recent swing highs/lows, support/resistance levels, 
breakouts/breakdowns.
* SMA/EMA trends, moving average crossovers (e.g., 50-day crossing above 
200-day), price relative to SMA/EMA.

...
```

Again, only a portion is shown. However, the most compelling part of this snippet is its requirement for the LLM to perform multi-timeframe analysis. This demonstrates genuine investment skill.

## 4. Other Notable Aspects

Finally, and perhaps the most inspiring aspect for individual developers, is the way the system is constructed. It shows how to achieve a fully functional investment research workstation with the lowest technical barrier. The entire project is almost entirely based on the Python technology stack, particularly for the frontend implementation.

Instead of choosing a frontend framework with a steep learning curve, it fully embraces Streamlit. As can be seen from the individual Python files in the `pages/` directory, each page is an independent script. This is a wise choice for individual developers who primarily want to validate investment logic rather than polish product details. It allows you to focus the majority of your energy on "how to analyze" rather than expending effort on tedious engineering tasks such as front-end/back-end separation and API debugging.

Streamlit is a Python library for building web interfaces, popular in the AI community. For instance, HuggingFace Spaces are built on Streamlit. Frontends built with Streamlit are unlikely to be powerful or flashy, nor can they handle heavy traffic requests (though I am curious about the traffic volume on HuggingFace). However, its greatest advantage is solving the problem of how Python programmers can quickly build web applications.

!!! attention
    Times have changed. Using Streamlit was a good idea three years ago. But in 2025, even if you don't know frontend development, achieving the effect of Streamlit only requires asking an AI bot. Therefore, Python full-stack development is no longer as "sexy" as it was three years ago.

Additionally, I noticed that the project does not use LLMs for text analysis throughout. For sentiment analysis, it uses the `vaderSentiment` library. We have introduced this library before; it is somewhat old-school, but its advantages are simplicity and ease of use. Its results may be more reliable than those from LLMs, and it is zero-cost to use. However, its last release was three years ago, and there may not be future versions. Therefore, I do not recommend continuing to use it, as Moore's Law is taking effect in the AI field, and tokens are rapidly depreciating.

Of course, this library is not perfect. I am not recommending that you use AlphaSuite. AlphaSuite is not a technically flawless work. To be blunt, I am more critical of it than appreciative of it. New faces always require attention—whether black or red, traffic ensures it is not lonely. Therefore, whether recommended or criticized, it should be welcomed by the inventor. This is why I dare to hold a fair perspective.

As statistician George Box said, "All models are wrong, but some are useful." AlphaSuite is imperfect, but it is still a "useful" model. Its greatest value lies in providing a clear, feasible technical path for those who wish to code their investment thoughts, while also demonstrating how to use prompts to obtain risk reports and investment advice.

The significance of building a similar system may lie not just in obtaining the final analysis results. More importantly, the creative process itself forces you to organize vague, scattered investment ideas in your mind into clear, logical rules and frameworks. Only when you can construct your thoughts into a system do you truly understand them.

The true essence of trading lies precisely in the intuition and reverence for market risks that cannot be learned from books. It is in this process of "hand-forging" that these insights are deeply imprinted in our cognition.
