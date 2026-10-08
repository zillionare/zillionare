---
title: "Word-Count Factor: News Sentiment via TF-IDF"
date: 2024-12-04
slug: en/posts/factor-strategy/word-count
tags: [Factor Mining, NLP, Sentiment Analysis, Quantitative Trading]
excerpt: "Leverage TF-IDF to build a word-count factor from news data. By comparing stock mention frequency against moving averages, this approach captures early sentiment signals before volume spikes."
lang: en
translation_of: posts/factor-strategy/word-count
auto_translated: true
source_sha: 03960041fd17656a12128ecefa839655c900a328
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/my-company.jpg"
---

If you visit a shopping mall, you’ll notice that the best-selling stores and products always occupy the prime, high-traffic spots. The same logic applies to the stock market: stocks frequently mentioned in news and social media tend to attract significantly higher trading volume.

When a stock gains popularity, its trading volume surges, showing a strong correlation. However, trading volume lags behind popularity indicators. By the time volume spikes, it may be too late to catch the move (especially if the stock hits the price limit). If we can detect popularity signals in advance, we might identify entry opportunities earlier.

So, how do we model this?

First, let’s cover some basics of information retrieval, then demonstrate how to use statistics and information retrieval concepts to model the problem above.

## TF-IDF

TF stands for Term Frequency, which counts how many times a specific word appears in a document. IDF stands for Inverse Document Frequency. Roughly speaking, the more documents a word appears in, the less information it carries.

For instance, we use words like "the," "a," or "of" (in English equivalents) in almost every sentence. These words appear in nearly every context (document) and thus carry little informational weight. A common adage in journalism is, "Dog bites man is not news; man bites dog is news." Essentially, the former happens too often to be newsworthy, so it carries no unique information.

The inventors of TF-IDF were likely Gerard Salton from Cornell University (known for its strong computer science department) and British computer scientist Karen Spärck Jones. Today, the Association for Computing Machinery (ACM) awards the Gerard Salton Award every three years to recognize outstanding contributions to information retrieval.

The construction process of TF-IDF is as follows:

Suppose we have 3 documents:

1. Apple Orange Banana
2. Apple Banana Banana
3. Orange Banana Pear

They may not look like documents, but this is the simplest form of a document—a collection of words (in the TF-IDF era, word order could not be processed). In Document 1, "Orange," "Banana," and "Apple" each appear once, so the TF for each is recorded as 1, yielding:

```
TF_1 = {
    'Apple': 1/3,
    'Banana': 1/3,
    'Orange': 1/3,
}
```

In Document 2, "Apple" appears once, and "Banana" appears twice. "Orange" and "Pear" do not appear. Thus:

```
TF_2 = {
    'Apple': 1/3,
    'Banana': 2/3,
}
```

The TF calculation for Document 3 follows similarly.

IDF represents the information weight of each word, calculated using the following formula:

$$
\text{IDF}(t) = \log \left( \frac{N + 1}{1 + \text{DF}(t)} \right) + 1
$$

1. DF: The number of documents in which a word appears.
2. $N$ is the total number of documents. Here, there are 3 documents, so $N=3$.
3. Adding 1 to both the numerator and denominator in the formula prevents division by zero since $DF(t)$ is always positive. It also acts as a form of L1 regularization, which is the approach used in `sklearn`.

We can now calculate the IDF for all words:

$$
\text{Apple} = \text{Orange} = \log \left( \frac{4}{2+1} \right) + 1 = 1.2876
$$

$$
\text{Pear} = \log \left( \frac{4}{1+1} \right) + 1 = 1.6931
$$

Since "Pear" appears rarely, its emergence is like the "man bites dog" event, giving it high informational weight. "Banana," however, is a common term appearing in all 3 documents, so we penalize it, resulting in a negative informational weight adjustment:

$$
\text{Banana} = \log \left( \frac{4}{3+1} \right) + 1 = 1
$$

Finally, we obtain the TF-IDF for each word:

$$
\text{TF-IDF} = \text{TF} \times \text{IDF}
$$

By using all possible words as columns and the TF-IDF values of appearing words in each document as values, we obtain the following sparse matrix:

|        | Apple    | Banana   | Orange   | Pear     |
| ------ | -------- | -------- | -------- | -------- |
| Doc 1  | 1.2876/3 | 1/3      | 1.2876/3 | 0        |
| Doc 2  | 1.2876/3 | 1/3 * 2  | 0        | 0        |
| Doc 3  | 0        | 1/3      | 1.2876/3 | 1.6931/3 |

In `sklearn`, an L2 normalization is applied to the TF-IDF of each word at the end. We will not calculate this manually here.

We refer to each row as a document vector, representing the document’s features. If two document vectors are identical, they likely represent the same article (approximately, because even with identical words and frequencies, different articles can be written).

For example, the characters "可以清心也" (can clear the heart/mind) can be arranged into "以清心也可" or "心也可以清" or "清心也可以," all forming coherent sentences.

In practice, we can use `sklearn`’s `TfidfVectorizer` to compute TF-IDF:

```python
import pandas as pd
def jieba_tokenizer(text):
    return list(jieba.cut(text))

d1 = "苹果橙子香蕉"
d2 = "苹果香蕉香蕉"
d3 = "橙子香蕉梨"

vectorizer = TfidfVectorizer(tokenizer = jieba_tokenizer)
matrix = vectorizer.fit_transform([d1, d2, d3])

df = pd.DataFrame(matrix.toarray(), columns = vectorizer.get_feature_names_out())
df
```

<!-- BEGIN IPYNB STRIPOUT -->
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pear</th>
      <th>Orange</th>
      <th>Apple</th>
      <th>Banana</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.000000</td>
      <td>0.619805</td>
      <td>0.619805</td>
      <td>0.481334</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.541343</td>
      <td>0.840802</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.720333</td>
      <td>0.547832</td>
      <td>0.000000</td>
      <td>0.425441</td>
    </tr>
  </tbody>
</table>
</div>
<!-- END IPYNB STRIPOUT -->

The results differ from our manual calculation because we omitted the computationally intensive L2 normalization during manual calculation.

From the example above, we see that TF-IDF is used to extract feature vectors from articles. With these feature vectors, we can compare the similarity of two documents by calculating the cosine distance. This can be applied to plagiarism detection, information retrieval, comparative literature, and content recommendation applications like Toutiao.

For instance, to prove that Cao Xueqin only wrote the first 87 chapters of *Dream of the Red Chamber*, one could calculate the TF-IDF for the first 87 chapters and the subsequent text separately, then compute the cosine distance to observe the differences.

Similarly, if we analyze Qiong Yao’s works using TF-IDF, you will find that after removing some key nouns, many of her articles show high similarity. Below are the most significant words and their TF-IDF scores from an analysis of *My Fair Princess*:

```
Ziwei: 0.0876
Emperor: 0.0754
Erkang: 0.0692
Empress: 0.0621
Fifth Prince: 0.0589
Rong Momo: 0.0573
Xiao Yanzi: 0.0556
Fourth Prince: 0.0548
Fujin: 0.0532
Jin Suo: 0.0519
```

Does this match your impression? However, the role of TF-IDF analysis in quantitative trading has not yet been demonstrated.

That concludes the discussion on TF-IDF’s role in quantitative trading. Next, we will step outside the TF-IDF framework to construct our own factor!

## Word-Count Factor

Based on the TF-IDF concept, we propose a **word-count factor**. Its construction involves fetching daily news data via `tushare`, tokenizing the text using `jieba`, and counting the occurrences of listed company names each day. This constitutes the TF component.

For the IDF component, we deviate from the classic method but adopt a simpler approach better suited for quantitative scenarios. We take the moving average of each word’s TF as the IDF. **This IDF constitutes the baseline noise for each word.** If a word’s frequency on a given day significantly exceeds this baseline noise, it indicates the company is in the news!

Finally, we divide the day’s frequency of a specific word by its moving average reading to form the factor. Clearly, the larger this value, the greater the informational weight it carries, indicating that the word (i.e., the company) has been frequently mentioned in the news recently.

## Fetching News Text Data

We can fetch news via the `news` interface in `tushare`. The method is:

```text
news = pro.news(src='sina', 
                date=start,
                end_date=end,
)
```

We save the fetched news data locally to allow for further mining later:

!!! attention
    Even with a premium account, `tushare` limits the number of news items callable per day. Therefore, please install `tushare` locally, apply for a premium account to run the following code, and do not run it in the Quantide Research environment!!
    
    Before running the code, specify the `data_home` variable to save the news locally.

````markdown
```python
def retry_fetch(start, end, offset):
    i = 1
    while True:
        try:
            df =pro.news(**{
                "start_date": start,
                "end_date": end,
                "src": "sina",
                "limit": 1000,
                "offset": offset
            }, fields=[
                "datetime",
                "content",
                "title",
                "channels",
                "score"])
            return df
        except Exception as e:
            print(f"fetch_new failed, retry after {i} hours")
            time.sleep(i * 3600)
            i = min(i*2, 10)

def fetch_news(start, end):
    for i in range(1000):
        offset = i * 1000
        df = retry_fetch(start, end, offset)

        df_start = arrow.get(df.iloc[0]["datetime"]).format("YYYYMMDD_HHmmss")
        df_end = arrow.get(df.iloc[-1]["datetime"]).format("YYYYMMDD_HHmmss")
        df.to_csv(os.path.join(data_home, f"{df_start}_{df_end}.news.csv"))
        if len(df) == 0:
            break

        # tushare limits both the call frequency and the number of news items returned per request
        time.sleep(3.5 * 60)
```
````

When counting the frequency of listed company names in the news, we must first add custom dictionaries to `jieba` to avoid tokenization errors. For example, if the keyword "Vanke A" is not added, `jieba` will inevitably split it into "Vanke" and "A."

The code to add custom dictionaries is as follows:

```python
def init():
    # get_stock_list is a custom function to fetch the stock list, available in the quantide research environment
    stocks = get_stock_list(datetime.date(2024,11,1), code_only=False)
    stocks = set(stocks.name)
    for name in stocks:
        jieba.add_word(name)

    return stocks
```

The security list obtained here will be used later, so it is returned as a function value.

Next, we count the word frequencies:

```python
def count_words(news, stocks)->pd.DataFrame:
    data = []
    for dt, content, _ in news.to_records(index=False):
        words = jieba.cut(content)
        word_counts = Counter(words)
        for word, count in word_counts.items():
            if word in stocks:
                data.append((dt, word, count))
    df = pd.DataFrame(data, columns=['date', 'word', 'count'])
    df["date"] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    return df
```

The data returned by `tushare` has three columns, among which `date` and `content` are the fields of interest. The company name frequencies are extracted from `content`.

Then, we analyze all downloaded news to count daily word frequencies and moving averages:

```python
def count_words_in_files(stocks, ma_groups=None):
    ma_groups = ma_groups or [30, 60, 250]
    # Fetch data within the specified date range
    results = []

    files = glob.glob(os.path.join(data_home, "*.news.csv"))
    for file in files:
        news = pd.read_csv(file, index_col=0)

        df = count_words(news, stocks)
        results.append(df)

    df = pd.concat(results)
    df = df.sort_index()
    df = df.groupby("word").resample('D').sum()
    df.drop("word", axis=1, inplace=True)
    df = df.swaplevel()
    unstacked = df.unstack(level="word").fillna(0)
    for win in ma_groups:
        df[f"ma_{win}"] = unstacked.rolling(window=win).mean().stack()
    
    return df
```

Finally, the complete code is as follows:

!!! attention
    The following code requires that news data be stored in the directory specified by the variable `data_home`, otherwise it will throw an error.

```python
import os
import glob
import jieba
from collections import Counter
import time

data_home = "/data/rw/news"
def init():
    stocks = get_stock_list(datetime.date(2024,12,2), code_only=False)
    stocks = set(stocks.name)
    for name in stocks:
        jieba.add_word(name)

    return stocks

def count_words(news, stocks)->pd.DataFrame:
    data = []
    for dt, content, *_ in news.to_records(index=False):
        if content is None or not isinstance(content, str):
            continue

        try:
            words = jieba.cut(content)
            word_counts = Counter(words)
            for word, count in word_counts.items():
                if word in stocks:
                    data.append((dt, word, count))
        except Exception as e:
            print(dt, content)
    df = pd.DataFrame(data, columns=['date', 'word', 'count'])
    df["date"] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    return df

def count_words_in_files(stocks, ma_groups=None):
    ma_groups = ma_groups or [30, 60, 250]
    # Fetch data within the specified date range
    results = []

    files = glob.glob(os.path.join(data_home, "*.news.csv"))
    for file in files:
        news = pd.read_csv(file, index_col=0)

        df = count_words(news, stocks)
        results.append(df)

    df = pd.concat(results)
    df = df.sort_index()
    df = df.groupby("word").resample('D').sum()
    df.drop("word", axis=1, inplace=True)
    df = df.swaplevel()
    unstacked = df.unstack(level="word").fillna(0)
    for win in ma_groups:
        df[f"ma_{win}"] = unstacked.rolling(window=win).mean().stack()
    
    return df.sort_index(), unstacked.sort_index()

stocks = init()
factor, raw = count_words_in_files(stocks)
factor.tail(20)
```

Here, we are still calculating raw data. The final factorization requires computing `factor["count"]/factor["ma_30"]` and executing a rank. Here, `ma_30` can be replaced with `ma_60`, `ma_250`, etc.

Unlike previous articles, this time we did not directly obtain good results. Much of our research involves lonely waiting, followed by selecting successful examples
