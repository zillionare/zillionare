---
title: "Finding Alphas: WorldQuant's Approach to Building Strategies"
date: 2024-01-25
slug: en/posts/resources/book-intro-finding-alphas-a-quantitative-approach
tags: [Alpha, Factor Investing, Trading Strategies]
excerpt: "What does 'alpha seeking' really mean? This review of WorldQuant's Finding Alphas unpacks the definition of alpha, how to design and test trading signals, and where academic research fits in."
lang: en
translation_of: posts/resources/book-intro-finding-alphas-a-quantitative-approach
auto_translated: true
source_sha: 2c1420baad4eb2709deeea4e25a6ced0c6878648
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/kitty-in-basket.jpg"
---

Q: I keep seeing people talk about "alpha seeking" — what does it actually mean?

Rather than answer it myself, let me recommend a book: *Finding Alphas: A Quantitative Approach to Building Trading Strategies*. The title says it all. The PDF I have is the second edition from 2019, by WorldQuant founder Igor Tulchinsky and colleagues.

<!--more-->
---

Alpha dates back to the Capital Asset Pricing Model (CAPM) of the 1960s. In that framework, a stock's expected return consists of the risk-free rate, an alpha return, and market risk exposure — the beta return. Alpha is a driver of stock returns.

There are other accounts of where alpha comes from and what it means. The book recommended here, for example, traces alpha to a 1968 paper by University of Chicago economics PhD Michael Jensen. In it he coined the term Jensen's Alpha to describe a portfolio's risk-adjusted return and to judge whether it beat market expectations. In practice, this seems no different from CAPM alpha.

WorldQuant defines alpha more broadly: any trading signal that can add value to a portfolio — even a combination of algorithm, source code, and configuration parameters! Quantide's factor analysis framework, Alphalens, also carries this meaning of finding alpha, i.e., finding trading signals.

Those are my personal views on alpha. These concepts are covered in our *Quant 24 Lessons* and in our latest *Factor Analysis and Machine Learning Models*.

Now, about the book.

At under 300 pages, it is a good entry point. The first two chapters give a short history of alpha and quantitative investing. Given how much hearsay about quantitative investing is circulating widely — as we have just seen, there are several competing definitions of alpha, not to mention so-called alpha strategies — a foreword by Igor Tulchinsky helps set the record straight.

In these two chapters, EMH is taken to task once again. He effectively invokes the Grossman-Stiglitz paradox in his critique, without noting that the idea actually comes from Grossman and Stiglitz. In the introduction to *Quant 24 Lessons*, we dig deeper into the history of quant, where we explicitly argue that this paradox triggered the second founding of modern micro-finance — the transition to behavioral finance. That introduction is available as a free download from our website.

Chapter 1 introduces the key concepts for designing alpha, such as what makes a good alpha:

- Beauty in simplicity: both the underlying idea and its mathematical expression are simple
- High in-sample Sharpe ratio
- Insensitive to small changes in data/parameters. Note: this is the so-called flat parameter plateau
- Works across different universes
- Works across different equity markets

These criteria are rather abstract. In practice, factor analysis frameworks use metrics such as IC, IR, turnover, and more to characterize alpha from different angles.

The chapter also lays out the steps for factor mining:

1. Explore the distribution of the data
2. Come up with an idea
3. Translate the idea into stock positions with math
4. Test that mathematical expression

In *Factor Analysis and Machine Learning Models*, we break the workflow down as:

1. Get raw data
2. Extract factors
3. Factor preprocessing
4. Single-factor testing

Going from factors to a strategy also involves a factor-combination problem, but that is a follow-on step after factor analysis.

Chapter 2 is mainly a review of quant history, discussing whether alpha exists, where it comes from, and so on. It makes one important point worth noting: how we should view the role of academic literature in quant. When searching for sensible relationships in asset prices, academic literature has been and will continue to be an important source of ideas. But for tractability, papers often rely on incomplete assumptions, or assumptions inconsistent with real markets. In short: don't believe everything you read.

Part II, from Chapter 4 through Chapter 17, covers every aspect of finding alpha: how to handle data, evaluate alpha factors, control biases, and more. Chapters 15 and 16 show how to use machine learning to search for factors automatically.

Starting with Chapter 18, the book covers factor design for specific settings — fundamental, momentum factor, intraday, event-driven factors, and so on. This part is helpful for broadening your horizons.

The book is strong on methodology and works well as an introduction. Once you have the big picture, move on to Zura Kakushadze's *101 Formulaic Alphas*, which has more code (pseudocode). After reading both books, you may still struggle to implement factor analysis hands-on or build a strategy. If so, consider our course *Factor Analysis and Machine Learning Trading Strategies*, presented as notebooks you can read and run side by side. All the data you need is already provisioned in the environment.

We also offer the more comprehensive *Quant 24 Lessons*.

There is no Chinese edition of the book. If, like me, you prefer reading in Chinese, install the "Immersive Translate" extension in Firefox. It can translate PDF documents with a side-by-side bilingual view.

---

<div style="display:flex;">
<div style="flex:50%; ">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/finding-alphas.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/finding-alphas-toc-1.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/finding-alphas-toc-2.jpg" style="height:200px"/>
</div>
<div style="flex:50%;">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/finding-alphas-toc-3.jpg" style="height:200px"/>
</div>
</div>

[Download PDF](/assets/ebooks/finding-alphas-a-quantitative-approach-to-building-trading-strategies.pdf)
