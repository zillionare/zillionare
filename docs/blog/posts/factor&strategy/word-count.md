---
title: "WorldQuant? Word Count!"
date: 2024-11-10
category: factor&strategy
slug: word-count-factor
motto: 
img: 
stamp_width: 60%
stamp_height: 60%
tags: []
---

如果你去商场逛，你会发现，销量最好的店和最好的商品总是占据人气中心。对股票来说也是一样，被新闻和社交媒体频频提起的个股，往往更容易获得更大的成交量。

如果一支个股获得了人气，那它的成交量一定很大，两者之间有强相关关系。但是，成交量落后于人气指标。当一支个股成交量开始放量时，有可能已经追不上了（涨停）。如果我们能提前发现人气指标，就有可能获得提前介入的时机。

具体怎么操作（建模）呢？

我们首先讲解一点信息检索的知识，然后介绍如何运用统计学和信息检索的知识，来把上述问题模型化。

## TF-IDF

TF是Term Frequency的意思。它是对一篇文档中，某个词语共出现了多少次的一个统计。IDF则是Inverse Document Frequency的意思，大致来说，如果一个词在越多的文档中出现，那么，它携带的信息量就越少。

比如，我们几乎每句话都会用到『的、地、得』，这样的词几乎在每个语境（文档）中都会出现，因此就不携带信息量。新闻业常讲的一句话，狗咬人不是新闻，人咬狗才是新闻，本质上也是前者太常出现，所以就不携带信息量了。

最早发明TF-IDF的人应该是康奈尔大学的杰拉德·索尔顿（康奈尔大学的计算机很强）和英国的计算机科学家卡伦·琼斯。到今天，美国计算机协会（ACM）还会每三年颁发一次杰拉德·索尔顿奖，以表彰信息检索领域的突出贡献者。

根据TF-IDF的思想，这里提出一个word-count因子。它的构建方法是，通过tushare获取每天的新闻信息，用jieba进行分词，统计每天上市公司名称出现的次数。这是TF部分。

在IDF构建部分，我们做法与经典方法不一样，但更简单、更适合量化场景。这个方法就是，我们取TF的移动平均做为IDF。

最后，我们把当天某个词的出现频率除以它的移动平均的读数作为因子（使用排序归一化）。显然，这个数值越大，它携带的信息量也越大。

## 获取新闻文本数据

我们可以通过tushare的news接口来获取新闻。
这个方法是：

```text
news = pro.news(src='sina', 
                date=start,
                end_date=end,
)
```

我们把获取的新闻数据先保存到本地，以免后面还可能进行其它挖掘：

```python
def fetch_news(start, end):
    # tushare对新闻接口调用次数及单次返回的新闻条数都有限制
    # 我们姑且设置为每30天做为一批次调用
    # 如果是production code，需要仔细调试这个限制，以免遗漏新闻
    date_range = pd.date_range(start=start, end=end)
    dates = pd.DataFrame([], index = date_range)
    freq = '30D'
    grouped = dates.groupby(pd.Grouper(freq=freq))
    groups = [group for _, group in grouped][::-1]

    for group in groups:
        period_start, period_end = group.index[0], group.index[-1]
        start = period_start.strftime('%Y%m%d')
        end = period_end.strftime('%Y%m%d')

        news = pro.news(src='sina', 
                        date=start,
                        end_date=end,
        )

        csv_file = os.path.join(data_home, f"{start}-{end}.news.csv")
        news.to_csv(csv_file)
        # 每小时能访问20次
        time.sleep(181)
```

在统计新闻中上市公司出现的词频时，我们需要先给jieba增加自定义词典，以免出现分词错误。比如，如果不添加关键词『万科A』，那么它一定会被jieba分解为万科和A两个词。

增加自定义词典的代码如下：

```python
def init():
    # get_stock_list 是自定义的函数，用于获取股票列表。在quantide research环境可用
    stocks = get_stock_list(datetime.date(2024,11,1), code_only=False)
    stocks = set(stocks.name)
    for name in stocks:
        jieba.add_word(name)

    return stocks
```

这里得到的证券列表，后面还要使用，所以作为函数返回值。

接下来，就是统计词频了：

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

tushare返回的数据共有三列，其中date, content是我们关心的字段。公司名词频就从content中提取。

然后我们对所有已下载的新闻进行分析，统计每日词频和移动均值：

```python
def count_words_in_files(stocks, ma_groups=None):
    ma_groups = ma_groups or [30, 60, 250]
    # 获取指定日期范围内的数据
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

count_words_in_files(stocks)
```

最后，完整的代码如下：

```python
import os
import glob
import jieba
from collections import Counter
import time

data_home = "/data/news"
def init():
    stocks = get_stock_list(datetime.date(2024,11,1), code_only=False)
    stocks = set(stocks.name)
    for name in stocks:
        jieba.add_word(name)

    return stocks

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

def count_words_in_files(stocks, ma_groups=None):
    ma_groups = ma_groups or [30, 60, 250]
    # 获取指定日期范围内的数据
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

        # tushare对新闻接口调用次数及单次返回的新闻条数都有限制
        time.sleep(3.5 * 60)

stocks = init()
start = datetime.date(2023, 1, 4)
end = datetime.date(2024, 11, 20)
# fetch_news(start, end)
factor, raw = count_words_in_files(stocks)
```

最终因子化要通过factor["count"]/factor["ma_30"]来计算并执行rank，这里的ma_30可以替换为ma_60, ma_250等。


