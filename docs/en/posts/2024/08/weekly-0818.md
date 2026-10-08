---
title: "OpenBB & HybridRAG: Free Market Data and AI for Quant Research"
date: 2024-08-18
slug: en/posts/uncategory/weekly-0818
tags: [OpenBB, HybridRAG, Market Data, Quantitative Investing]
excerpt: "This week: Monkeypox impacts markets, China's M2/M1 diverges, and US inflation cools. Deep dive: OpenBB for free global data and BlackRock's HybridRAG for financial document extraction."
lang: en
translation_of: posts/uncategory/weekly-0818
auto_translated: true
source_sha: 4a98ed9fa32116025381cbc7c9ebc276bf91ea63
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/kenneth-griffin.jpg"
---

### This Week's Headlines

* Global monkeypox cases exceed 15,600; related US stock GeoVax Labs surged 110.75%.
* PBOC releases key data: July M2 grew 6.3% YoY, while M1 fell 6.6% YoY.
* US July CPI rose 2.9% YoY, with retail sales increasing 1% MoM.
* *Securities Times*: State-owned enterprises should abandon the "implicit guarantee" belief for convertible bonds.

### Next Week's Watchlist

* **Wednesday**: ETF options expiration. Historical data suggests heightened volatility on this day.
* **Wednesday & Thursday**: Massive reverse repos maturing (RMB 369.2 billion and RMB 577.7 billion, respectively). The PBOC has previously indicated it will roll over these maturing repos.
* **Tuesday**: The Shanghai Stock Exchange and CSI Index Company released the STAR 200 Index.
* **Gaming**: *Black Myth: Wukong* officially launches, receiving high scores from multiple media outlets.

### This Week's Selection

* **OpenBB in Action**: How to easily access overseas market data?
* **BlackRock Launches HybridRAG**: Extracts insights from financial documents with 100% accuracy!

---

## This Week's Headlines in Detail

* The World Health Organization (WHO) declared on the 14th that the monkeypox outbreak constitutes a "Public Health Emergency of International Concern." Cases reported this year have exceeded 15,600, surpassing last year's total, with 537 deaths. On the 15th, the General Administration of Customs issued an announcement requiring travelers from outbreak areas to self-declare and undergo testing. The topic topped the East Money hot list, reaching 1.07 million views by press time, far exceeding the second-place topic (AI glasses) at 630,000 views (Xinhua, East Money).
* The PBOC released key data on the 13th, showing that at the end of July, the M2 balance was RMB 303.31 trillion, up 6.3% YoY; the M1 balance fell 6.6% YoY, while M0 grew 12% YoY. M1 has seen negative growth for four consecutive months, indicating a decline in corporate demand deposits, with some funds gradually shifting into wealth management products (First Financial).
* In July, the US CPI rose 2.9% YoY and 0.2% MoM. Core CPI rose 3.2% YoY, marking the lowest year-over-year increase since April 2021, though still above the Fed's 2% long-term inflation target (Xinhua).
* US July retail sales increased 1% MoM, beating market expectations and marking the highest level since January 2023. Sales grew across automobiles, electronics, and food. Economists believe the US economy will achieve a "soft landing," cooling inflation without entering a recession (China News Service).
* The Nasdaq Composite rose 5.29% for the week, and the Dow Jones Industrial Average rose 2.94%. A further 2% rise would set a new all-time high.
* *Securities Times*: Recently, a state-owned enterprise (SOE) announced the default of its convertible bond upon maturity, unable to repay principal and interest. This marks the first SOE convertible bond default in China, shattering the "implicit guarantee" (rigid redemption) belief. In a mature market, the actual operational and financial health of the issuer determines the risk level of its financial products. When allocating assets, investors should prioritize the issuer's operational and financial status rather than "upgrading" or "discriminating" based on identity. The emergence of the first SOE convertible bond default is a small step for the convertible bond market but a significant step toward letting market forces play their role and supporting high-quality economic development (Remark: Convertible bonds have long been suitable for individual and small-to-medium institutional allocation, offering downside protection via bond characteristics and upside potential via equity characteristics, making them a candidate for grid trading strategies).

---

## OpenBB in Action!

Have you ever had this experience? You come across foreign papers or blogs with excellent research methods and compelling conclusions, and you can't help but want to reproduce them.

However, the data used in these articles is often from overseas markets. How can we obtain **free** overseas market data?

Previously, `yfinance` was an option, but it stopped serving users in mainland China from November 2021. Today, we introduce a tool called **OpenBB**. It provides a data standard that aggregates many free and paid data sources.

In the overseas market, Bloomberg is undoubtedly the leading data provider. Its products and services include financial news, market data, and analytical tools, exerting immense influence in global financial markets. It is an indispensable information source for many financial institutions, traders, analysts, and decision-makers. However, Bloomberg data is indeed expensive. If you are conducting individual research or occasionally using overseas data, you显然 need to look for more cost-effective data sources.

Thus, OpenBB entered the market. Judging by its name, they aim to build an Open Source Bloomberg.

## Installing OpenBB

Install OpenBB using the following command:

```bash
pip install openbb[all]
```

!!! tip
    OpenBB requires Python version 3.11 or higher. It is highly recommended to create a separate virtual environment for it.

---

After installation, there are multiple ways to use it.

## Using the Command Line

After installation, you can launch OpenBB from the command line.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/openbb-cli.jpg)

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/open-bb-quotes-view.jpg)

You can then follow the prompts to input commands. For example, to obtain market data, you can sequentially input `equity > price`, followed by `historical --symbol LUV --start_date '2024-01-01' --end_date '2024-08-01'` to retrieve the historical data for this stock.

OpenBB will pop up a window displaying the market data in a table format, allowing you to export the data.

The effect is somewhat surprising, haha.

---

Interestingly, they designed the commands in a Unix path style. Therefore, after executing the previous command, you can input other commands starting from the root directory, such as:

``` bash
/economy/gdp
```

You can then query global GDP data.

## Using Python

We will demonstrate its usage via a notebook.

```python
from openbb import obb

obb
```

This `obb` object is our entry point for using OpenBB. When you directly input `obb` in a cell, it prompts you with its attributes and methods:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/help-openbb-jupyter.jpg)

Here, OpenBB maintains interface consistency. The content we see is similar to what we see in the CLI.

Now, let's demonstrate some specific features. First, search for a stock code by name:

---

```python
from openbb import obb

obb.equity.search("JPMorgan", provider="nasdaq").to_df().head(3)
```

The output is:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/openbb-equity-search.jpg)

As a foreigner, figuring out the relationship between stock codes and data providers can be tricky. However, if you research it daily, spending some time is justified.

From the previous results, we learned that the stock code for "JPMorgan" (often confused as JPMorgan Chase vs. Morgan Stanley, but easy to remember: Morgan Stanley is one, JPMorgan Chase is the other) is **AMJB** (specifically for JPMorgan Chase). We then want to check its historical market data. If we can successfully retrieve it, our tutorial would end here.

However, when we call the following code:

```python
obb.equity.price.historical("AMJB")
```

It errors out! The prompt says: `No result found.`

## Using Free Data Sources Requiring Registration

The real reason is that OpenBB has only one out-of-the-box free data source -- CBOE, but this stock is not included in the free CBOE data. We need to choose another data source, such as FMP. However, we must first register for an FMP account (free) and add the FMP API key to the OpenBB Hub.

---

[FMP](https://site.financialmodelingprep.com/) is a data provider from Financial Modeling Prep. It offers free (limited to 250 calls) and paid services, with data covering US stocks, cryptocurrencies, forex, and detailed corporate financial data. Free data can retrieve 5 years of historical data.

!!! tip
    OpenBB supports many data sources. These sources often provide some free usage limits. Through OpenBB's aggregation, you can use as many data sources for free as possible.

Registering for FMP only requires an email address, so if 250 calls are insufficient, it appears easy to increase the quota. After registration, you can see your API key in the dashboard:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/fmp-keys.jpg)

Then, register for an OpenBB Hub account and add this API key to the OpenBB Hub.

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/openbb-hub.jpg)

Now, we change the data source to FMP and run the previous code again to get the desired result.

---

```python
obb.equity.price.historical("AMJB", provider="fmp").to_df().tail()
```

We will get the following result:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/openbb-amjb-quotes.jpg)

For another stock, Apple, we first use the `search` command to obtain its code, 'AAPL' (often misremembered as APPL), and then substitute it into the previous code to retrieve the data.

Need to do some fundamental research, such as wanting to know Apple's historical cash flow data?

```python
obb.equity.fundamental.cash("AAPL", provider='fmp').to_df().tail()
```

Trading calendars, adjusted price information, and constituent lists are indispensable in backtesting (in China A-shares, ST lists and historical price limit data are also required). Let's see how to obtain stock lists and index constituent lists:

```python
# Get all stock lists
all_companies = obb.equity.search("", provider="sec")

print(len(all_companies.results))
print(all_companies.to_df().head(10))

# Get index lists
indices = obb.index.available(provider="fmp").to_df()
print(indices)

# Get index constituents, DOWJONES, NASDAQ, SP500 (no permission)
obb.index.constituents("dowjones", provider='fmp').to_df()
```

---

Trying out a new library takes time. Often, you only decide whether to continue using it after investing that time. If you ultimately decide not to use it, the exploration time is wasted.

Therefore, we have built a computing environment where OpenBB is installed and the FMP data source is registered, providing an example notebook for everyone to practice with OpenBB.

This environment is provided free of charge. The login address is [here](http://139.196.218.124:5180/openbb_bb/login), and the password is: `ope@db5d`.

---

## BlackRock Launches HybridRAG

Large language models (LLMs) are ubiquitous. Programmers have found that using LLMs to generate code is very useful -- but this has a key caveat: the programmer must know what they are doing and verify whether the code generated by the LLM is correct.

However, in the financial domain, things become more complex. No one knows if the answer generated by an LLM is correct, and it is impossible to verify it like a programmer -- such verification would either cause you to miss opportunities or cost you money.

The ability to extract relevant insights from unstructured text, such as earnings call transcripts and financial reports, is crucial for making informed decisions that affect market forecasts and investment strategies. This has long been a core viewpoint for BlackRock, the world's largest asset manager.

Recently, their researchers, in collaboration with NVIDIA, launched a novel method called **HybridRAG**. This method integrates the advantages of VectorRAG and GraphRAG (knowledge graph-based RAG) to create a more robust system for extracting information from financial documents.

HybridRAG operates through a complex two-layer approach. Initially, VectorRAG retrieves context based on text similarity, which involves dividing documents into smaller chunks and converting them into vector embeddings stored in a vector database. The system then performs similarity searches in this database to identify and rank the most relevant chunks. Simultaneously, GraphRAG uses knowledge graphs to extract structured information, representing entities and their relationships in financial documents. By combining these two contexts, HybridRAG ensures that the language model generates contextually accurate and detail-rich responses.

The effectiveness of HybridRAG was demonstrated through extensive experiments using a dataset of earnings call transcripts from companies in the Nifty 50 index. This dataset covers various sectors, including infrastructure, healthcare, and financial services, providing a diverse basis for evaluating system performance. Researchers compared HybridRAG, VectorRAG, and GraphRAG, focusing on key metrics such as faithfulness, answer relevance, context precision, and context recall.

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/benchmark-hybrid-rag.jpg)

Analysis results indicate that HybridRAG outperforms both VectorRAG and GraphRAG across multiple metrics. HybridRAG achieved a faithfulness score of 0.96, indicating that the generated answers align with the provided context. Regarding answer relevance, HybridRAG scored 0.96, outperforming VectorRAG (0.91) and GraphRAG (0.89).

GraphRAG performed excellently in context precision, scoring 0.96, while HybridRAG maintained strong performance in context recall, achieving a perfect score of 1.0 alongside VectorRAG. These results highlight HybridRAG's advantage in providing accurate, contextually relevant responses while balancing vector-based and graph-based retrieval methods.

[Paper Link](https://arxiv.org/abs/2408.04948)
