---
title: "Dragon-Phoenix Mania: Detecting Name Hype With Quant Methods"
date: 2024-01-23
slug: en/posts/factor-strategy/magic-hot-word-factor
tags: [Factor Mining, Alternative Factors, China A-Shares]
excerpt: "Quants never ignore a potential profit opportunity, no matter how irrational it looks. We boldly hypothesize, then carefully verify — including China's magical stock-name speculation."
lang: en
translation_of: posts/factor-strategy/magic-hot-word-factor
auto_translated: true
source_sha: c8dea80593a99576f7663e20c2b5759a1e8e2ad3
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/dragon-and-phoenix.jpg"
---

As quants, we watch the market closely and never let a potential profit opportunity slip by. Once we spot one, we don't care what others think or whether the textbooks cover it. **But: bold hypothesis, careful verification.**

The factor I'm sharing today is quite magical — I call it magic Chinese characters. If you find that kind of no-holds-barred speculation hard to stomach, let's call it by another name: an alternative factor.

<!--more-->

In late 2023, the market started bidding up stocks with "Dragon" (龙) in their names, then moved on to "Phoenix" (凤) — dubbed an auspicious union (龙凤呈祥). The character of the year for 2024 might be "Hua" (华). It's magical, nonsensical speculation. But just as there are four seasons in a year, China A-shares stages this kind of magical rally at least once a year.

This is nothing new in history. Veteran investors will remember Eastern Communications, a 10-bagger that emerged in late 2018 to early 2019. It sparked a run on the word "East" (东方). For a while, any stock with "东方" in its name got a lift.

Now let's see how to implement this factor.

!!! tip Strategy
    1. Take the strongest stocks of the day (i.e., stocks hitting limit-up)
    2. Use tokenization to find the most frequent word
    3. Find stocks containing that word but that did not hit limit-up that day, and group them into a basket
    4. Get the next 10 days of market data for the basket and compute PnL over 1-day, 5-day and 10-day horizons.

We'll skip how to fetch the daily limit-up list. You can get historical limit-up data with either AKShare or JQDataSDK.

When hunting for the hottest word, we first drop generic terms like "shares", "technology" and "holdings". They appear so frequently in company names that, by TF-IDF logic, they carry no information.

```python
# 使用的数据源在证券名称上，没有提供PIT数据。当前已退市的标的，
# 其名字为None。我们要先滤掉这部分。注意这里已经引入了一个回测
# 偏差
text = " ".join(filter(lambda x: x, df["alias"]))

# 排除掉没有信息量的词
cleaned = re.sub(r"股份|科技|控股", "", text)
```

Next we extract the hot words. Observation shows a hot word can be a two-character word like "东方" (East), or a single character like "龙" (dragon) and "兔" (rabbit). So we process them in two passes, prioritizing two-character words.

```python
    for word in jieba.cut(cleaned):
        if word == " " and len(word) != 2:
            continue
        if word in two:
            two[word] += 1
        else:
            two[word] = 1
```

Here we use jieba, the go-to Python tokenizer for Chinese. I'm not sure about the current landscape, but through 2021 it was definitely the leader for Chinese word segmentation in Python. It splits a name like "东方通信" (Eastern Communications) into "东方" and "通信", for example. If "东方航空" (China Eastern Airlines) also hits limit-up, it splits into "东方" and "航空", giving "东方" two counts, while "通信" and "航空" get one each.

We handle single-character words the same way. The result (like `two`) is a collection. To pick the most frequent character (word), we sort it by count:

```python
two = sorted(two, key = lambda x: x[1], reverse=True)
```

This is a very common Python idiom.

Building the basket isn't hard, but we need a security list. This is why we always stress: before paying for any data source, check whether it provides a few essential APIs. Without something as basic as a security list, you can hardly build any strategy.

Once we have the list of stocks that did NOT hit limit-up on that day, we pull market data for that day plus the next 10 days, then use pandas' `pct_change` to compute 1-, 5- and 10-day holding returns.

In factor analysis, this kind of function is conventionally called `forward_returns`, so we name ours `get_forward_returns` here for readability.

```python
async def get_forward_returns(dt: datetime.date, n=10):
    ...
    end = tf.day_shift(dt, n)
    barss = {}
    for sec in secs:
        bars = await Stock.get_bars(sec, n+1, FrameType.DAY, end=end)
        if len(bars) != n + 1:
            continue
        barss[sec] = bars["close"]

    df = pd.DataFrame.from_dict(barss)
    returns = []
    for period in (1, 5, 10):
        returns.append(df.pct_change(period).mean())

    df = pd.concat(returns, axis=1).rename(columns={0:"1d", 1:"5d", 2:"10d"})
    mn = df.mean()
    print(f"{dt} {concept} 1D: {mn.iloc[0]:.2%} 5D: {mn.iloc[1]:.2%} 10D: {mn.iloc[2]:.2%}")
    return df
```

During processing we already print the basket's 1-, 5- and 10-day forward returns (if such thematic speculation exists that day) for debugging. We also return the result for further analysis.

Finally, we ran it over Feb 10 – Mar 5, 2019, with these results:

![Forward returns of the hot-word speculation basket, Feb 10 - Mar 5, 2019](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/magic-word-factor-forward-returns.jpg)

That's how your money gets taken. If you can't beat them, join them!

The source code is available for free preview within one week of publication. See [here](https://blog.quantide.cn/articles/course/24lectures/preview/) for how to preview it.
