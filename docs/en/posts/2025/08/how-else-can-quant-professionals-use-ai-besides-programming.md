---
title: "AI for Quants: Beyond Coding to Autonomous Trading Teams"
date: 2025-08-05
slug: en/posts/tools/AI-tools/how-else-can-quant-professionals-use-ai-besides-programming
tags: [Quantitative Trading, Artificial Intelligence, Multi-Agent Systems, Factor Investing]
excerpt: "Explore how AI transforms quant workflows: from Grok-curated news and AI-generated research podcasts to TradingAgents, a multi-agent framework boosting annualized returns by 30% through rational, team-based decision-making."
lang: en
translation_of: posts/tools/AI-tools/how-else-can-quant-professionals-use-ai-besides-programming
auto_translated: true
source_sha: 52f146f4d2cb1eb98dc202ee4d6d8125335ab47a
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/brooke-lark-8beTH4VkhLI-unsplash.jpg"
---

**Zhihu Question: Beyond Programming, How Can Quants Use AI?**

**AI will rebuild everything.** This morning, I saw a comment from "Mr. Dan" stating that AI is a once-in-a-decade wave, comparable to the internet in 2000 or mobile payments in 2013. If we don’t invest in computing power, models, and applications now, we’ll only be kicking ourselves later. This is the first thought on how quants should approach AI: going **'All in AI'** for investment.

Let’s get real. Everyone says we live in an era of intense involution (neijuan). For quants, new technologies, algorithms, models, and information emerge daily, making it impossible to read or learn everything.

So, what do we do?

## Grok: Personalized Intelligence

Life is full of contradictions.

On one hand, we often lament information overload and advocate for "information fasting." On the other hand, we often feel we are still living in an information wasteland.

The missing piece is a smart assistant. If we had an assistant that proactively collected and filtered information, delivering only the news we care about directly to us, we wouldn’t have to worry about "nutrition." For this, we can use **Grok subscription tasks**.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250805151337.png)

The usage is straightforward, and I assume no quant needs me to explain it. Simply enter an email address at the end, and the news summaries will arrive in your inbox on schedule.

## AI Podcasts: The Ultimate Self-Study Tool

Reading is a visual dimension, but when there is too much material to read, our eyes get tired. Thus, we thought of creating a *Quant Voice* podcast, opening another dimension for learning and growth—the auditory dimension. This serves as an audiobook for commuting on the subway or before bed.

In the process of producing these programs, we discovered new uses for AI, which I’d like to share with you—you can use them to create your own exclusive podcasts, turning quantitative papers and research reports that you don’t have time to "read" into podcast content. This allows you to learn while on the road.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/promotion/voice.jpg)

There are two tools here. One is **Doubao’s AI Podcast**. Simply upload a research report, and Doubao will automatically generate an audio podcast. It features a standard male-female duo chat, with natural, fluent, light, and lively voices, akin to listening to an emotional talk show.

The other is **Google’s NotebookLM**. Compared to Doubao, its voice sounds more like a news broadcast—steady and dignified. However, the key difference lies in customizability.

Doubao podcasts cannot customize content and can only ingest one material source at a time. **Google’s NotebookLM**, on the other hand, can ingest multiple material sources and guide content generation via prompts. For example, for a research report, we can customize the prompt as follows:

!!! tip
    You are a quantitative finance expert. You have been given a research report to generate a two-person dialogue podcast. The two hosts will discuss the following questions:
    1. What viewpoints does this research report propose?
    2. What is the value of the report?
    3. What knowledge points, skills, methods, or data can listeners learn from it?
    4. What are the specific implementation steps for the methods mentioned in the report?
    5. How should quants apply these conclusions?
    
    Your generated content must be completely faithful to the research report, including every number, every conclusion, and every derivation, without modification. The tone should not be too exaggerated, and avoid excessive praise for the report and its conclusions.

Now, take these prompts and try it yourself.

Based on large language models, it can clearly deconstruct the key content of research reports and reorganize it into a relaxed, lively two-person dialogue.

It takes only about 5–10 minutes to "listen" to a research report. This is crucial. Without dedicated work hours, I doubt anyone has the time to read 300 research papers in a year.

By using this method, we can quickly "listen" to 300 research reports and then selectively read the most important ones in depth. This significantly accelerates our ability to extract the essence of others' work.

## One Person + AI = A Trading Team

This is likely one of the most advanced uses of AI for quants: building a trading team via AI.

In traditional trading teams, we hope to hear diverse voices, as "listening to both sides makes one enlightened." However, human nature dictates that we are least tolerant of dissenting voices. Therefore, even if a trading team collects information and viewpoints from different angles, it is difficult to achieve scientific decision-making, often resulting in a "one voice dominates" scenario.

This is the core value brought by the **TradingAgents** project.

**TradingAgent** is a **multi-agent financial trading framework based on Large Language Models (LLM)**, developed by Chinese scholars from UC Berkeley, MIT, and other universities. It has garnered over 18k stars on GitHub.

Its essence is to simulate the **collaborative workflow of a real trading team**, using multiple specialized agents (Agents) to complete trading decisions collaboratively. In other words, by deploying a TradingAgent, you effectively obtain a trading team. This is why so many people are using it.

The core composition of this "team" is:

- **Analyst Team**: Includes agents for fundamental analysis, technical analysis, and news/social media sentiment analysis, responsible for data cleaning and indicator generation.
- **Research Team**: Divided into "optimistic" and "pessimistic" factions, generating buy-side and sell-side evidence respectively to simulate multi-perspective debates.
- **Trade Execution Chain**: A trader agent integrates evidence from both sides to form trading recommendations, which are reviewed by a risk control team before the "fund manager" agent makes the final execution decision.

What problem does TradingAgents solve? It collects and integrates multi-dimensional information, data, and indicators. It simulates the complex interactions of a real trading team while overcoming human communication difficulties and subjective biases, avoiding information distortion, loss, and irrational interpersonal conflicts during communication.

This diagram basically illustrates its operational mode:

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250805160149.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

It features multiple agents divided into five layers. The bottom layer consists of "analysts" (the workhorses) responsible for scraping relevant data. The data and indicators they output are passed to the research layer.

The agents in this layer are divided into two factions: the optimistic and the pessimistic. These two factions engage in fierce debates. Through debate, facts are clarified, and logic becomes clearer. Finally, they propose buy-side and sell-side recommendations to the trading layer agents.

This is where the advantage of AI is further demonstrated. The AI Trader bases decisions solely on facts and data, rather than on personal preferences or dislikes. It avoids the scenario where a leader’s single opinion overrides all others.

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/vitaly-gariev-VZQAo20ArSA-unsplash.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

After the truth becomes clearer through debate, the trading recommendations are sent to the risk control layer agents. Finally, the risk control agents evaluate the suggestions and propose trading recommendations to the manager layer, where the manager agent makes the final trading decision and execution. Doesn’t this resemble a real trading team managing billions in assets?

Backtests of TradingAgents show that for targets like Apple, Google, and Amazon, annualized returns increased by nearly 30%, with max drawdowns controlled exceptionally well.

What is the core value and significance of TradingAgents? Perhaps its greatest value is that **its collaboration exceeds human capability**. On one hand, agents collect information, think, and communicate much faster than humans. On the other hand, their collaboration is unaffected by emotional fluctuations.

Unaffected by personal likes or dislikes, they always engage in **rational debate**, which is precisely a goal humans cannot fully achieve.
