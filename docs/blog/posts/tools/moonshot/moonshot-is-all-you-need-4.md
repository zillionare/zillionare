---
date: 2023-01-01
---

这个系列的跨度有点久了，在开始之前，做一个前情提要。这个系列我们选择的是中金2023年12月的一份研报，名为《在手之鸟，红利优选策略》。它是一个基本策略，通过这份研报的实现，我们可以了解到：

!!! abstract
    1. 获取众多基本面数据，并且我们会对部分数据的含义及编纂方法进行讲解
    2. 月度调仓换股回测策略应该如何实现
    3. 获得一个红利优选基础策略。通过适当改变参数，即可用以实战。


该策略要用到以下数据：

1. 行情数据。任何策略都默认需要它，至少会在计算远期收益时使用。 <!-- pro.daily -->
2. 股息率，用来按股息率筛选个股，以及计算两年股息率均值因子。 <!-- pro.daily_basic -->
3. 分红数据。只有过去两年连续分红的公司才能入选。 <!-- pro.dividend -->
4. 审计意见。只有过去十年没有审计保留意见的公司才能入选。<!--pro.audit-->
5. 市值数据。只有市值大于50亿的公司才能入选。 <!-- pro.daily_basic -->
6. 净利润、营业收入和营业利润数据，用来计算净利润稳定性因子。<!-- pro.income -->
7. 股东数量变化 <!-- pro.stk_holdernumber -->
8. 换手率。用来计算换手波动率。<!-- pro.daily_basic -->
9. pe_ttm，用来计算 ep 因子。
10. 经营现金流数据，用来计算经营现金流资产比因子。<!-- pro.cashflow_vip.n_cashflow_act-->
11. 资产总计数据，与10一起，用来计算经营现金流资产比因子。 <!-- pro.balancesheet_vip.total_assets -->
12. 盈余公积金数据。与11一起，用来计算留存收益资产比因子。<!-- pro.balancesheet_vip.surplus_rese -->

<!--PAID CONTENT START-->
```python
import sys
sys.path.append(str(Path(__file__).parent))

from helper import (ParquetUnifiedStorage, dividend_yield_screen, fetch_bars,
                    fetch_dv_ttm)
from moonshot import Moonshot
```
<!--PAID CONTENT END-->

我们已经获得了第1~2步的数据，并实现了按股息率进行票池筛选。回测表明，仅仅是通过股息率因子，我们就可以获得一定的年化超额，和更好的夏普比。

在这一期，我们将探讨如何把分红数据也纳入进来。研报要求，只有过去两年连续分红的公司才能入选票池。这是一个看似简单，但实现上有一点点复杂度的需求。

## 获取分红数据

在上一篇中，我们已经获取了股息率数据，但要实现『连续两年分红』这个条件，为精确起见，我们不能把『连续两年股息率大于零』来当成『连续两年分红』，而是要直接获取分红原始记录。

!!! info
    通过 daily_basic 获得的股息率是一个按过去12个月滚动计算的股息率。根据它的计算方式，就可能存在这样的情况，比如2023年12月进行了分红，2024年全年没有分红，但是直到2024年11月，股息率都会一直大于零。如此以来，在2025年2月，当我们问道，该股是否连续两年分红时，就会得到一个错误结果。在这方面，分红记录可以略微精确一点。


在 tushare 中，我们要通过 dividend 接口来获取分红数据。我们的回测发生在2018年到2023年之间，我们再一次遇到如何在 tushare 中，获取这么长跨度的数据的问题。根据我们之前的讨论，我们应该选择一次查询可以获得最多数据的接口（参数）。

该接口签名如下：

```{code-block}python
def dividend(ts_code: str|None = None, ann_date: str|None = None, record_date: str|None = None, ex_date: str|None = None, imp_ann_date: str|None = None):
    pass
```

但是，如果按这些参数来进行查询，每次返回的数据量会很小，导致获取数据时间过长。这里我们还发现了一个隐藏参数，大家可以根据自己的情况来决定是否采用。这个参数就是 end_date。我们把使用各个参数进行查询所能得到的记录数比较一下：

```python
df_ann = pro.dividend(ann_date="20250419")
print("by ann_date", len(df_ann))

df_end = pro.dividend(end_date="20241231", offse=0, limit=6000)
print("by end_date", len(df_end))

df_ex = pro.dividend(ex_date="20250419")
print("by ex_date", len(df_ex))

df_record = pro.dividend(record_date="20250419")
print("by record_date", len(df_record))

df_imp = pro.dividend(imp_ann_date="20250419")
print("by imp_ann_date", len(df_imp))
```

可以看到，使用 end_date 参数，可以获得的数据远远超过其它参数；但是，它的limit 并不是我们常见的6000，而是只能返回2000。这些行为上的不一致，是我们要注意的。

由于这里的 limit 只有2000，而现在 A 股有5000多支个股，所以，我们在通过 end_date获取数据时，还必须通过 offset/limit 多次调用，才能取全一天的数据。

下面的代码演示了如何取区间[start, end]之间的数据：

```python
import time

def fetch_dividend(start: datetime.date, end: datetime.date):
    dates = pd.date_range(start, end)
    dfs = []
    limit = 2000
    for dt in dates:
        # 对每一个交易日，都可能有超过 limit 条记录
        for offset in range(0, 99):
            str_date = dt.strftime("%Y%m%d")
            df = pro.dividend(end_date=str_date, offset=offset * limit)
            dfs.append(df)
            if len(df) < 2000:
                break

    # 如果取太快，会导致 tushare 拒绝访问
    time.sleep(0.125)
    data = pd.concat(dfs)
    data["date"] = pd.to_datetime(data["ann_date"]).dt.date
    return data.rename(columns={"ts_code": "asset"})
```

!!! attention
    在本系列前面的章节中，我们在计算[start, end]之间的日期列表时，一般使用 bdate_range。它将获取一个排除了周六、周日的日期列表。当我们使用它来获取交易数据时，这些是 OK 的。但是，基本面数据可能发表在


在最后，我们对数据进行了一些处理，使得返回的数据包含 asset, date 这两列，以便我们能像其它数据一样，自动化地利用缓存。

现在，我们就用之前开发的缓存来保存这些数据：

```python
path = data_home / "rw/dividend.parquet"
store = ParquetUnifiedStorage(store_path = path)

for yr in (2018, 2019, 2020, 2021, 2022, 2023):
    start = datetime.date(yr, 1, 1)
    end = datetime.date(yr, 12, 31)

    data = fetch_dividend(start, end)
    store.append_data(data[data["div_proc"] == "实施"])

print(store.start, store.end)
store
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250905204554.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>原始分红记录</span>
</div>
<!-- END IPYNB STRIPOUT -->

分段获取的原因是为了保证万一出错，我们也不会损失太多数据。

文档没有说明这些记录是如何编纂的。根据我们的分析，公司可能在一年内有多次分红（这样的公司太少了）；对每一次分红，它可能有多条记录，分别对应于预案、股东大会通过和实施三个阶段。

对我们本次需求来说，只要关注『预案』阶段的记录就好。因为预案一旦发布，相关炒作资金就会闻风而动，不会等到实施阶段。在预案中，我们又只需要关注 end_date, ann_date，这是计算是否有连续两年分红的关键。

但是，在示例代码，我们保存的是 div_proc 为『实施』阶段的数据。因为在大多数情况下，它包含了预案阶段的全部信息，同时又提供了实施阶段的一些额外信息，可以为今后使用。不过，我们要注意，在回测中，当我们把 ann_date 当成最新的时刻时，是不能去读 cash_div，record_date, ex_date 等信息的，此时它们还是『未来数据』

!!! attention
    tushare 的记录中给出了税后分红(cash_div)，但文档中并没有明确指出它的计算方法，欢迎讨论！按相关法规，企业与个人股东的分红税率不一样，个人股东持有时间长短不一样，分红税率也不一样。因此，理论上讲，每一个 cash_div_tax，都应该对应多个 cash_div -- 看谁来读它。


要如何判断某只股票是否连续分红呢？我们需要通过 end_date 提取出会计年度，并且将 ann_date 转换为年/月的格式。由于我们是在月末才进行调仓换股，假设现在是2020年6月30日，如果此时存在会计年度为2018， 2019年的两条以上记录，则可以认为该股连续两年分红了。而在回测中，我们还要加一条限制，才能防止使用未来数据。这条限制是，ann_date 必须小于等于 2020-06-30，即在回测时，已经可以拿到这两条数据了。

!!! attention
    做基本面回测的难度主要在于数据。在现实中，在2020年6月30日这一天，如果分红实施方案是在6月30日公布的，理论上你应该可以在当天晚上就得到数据，并且用它来决定投资策略。但是，这取决于你使用的数据源。对所有人都公开所得的数据，也不一定对你的计算机程序可得。如果你在实盘中使用的数据源处理起来没有那么快，那么，你的回测结果仍然无法用以实盘。


逻辑很简单。复杂性在于，如何高效地为每一个月生成 flag（以表明在该月，该股是否连续两年分红）。这里我们将使用以下技巧：

1. 通过月度和股票代码创建一个笛卡尔积，作为每支股票、每月 flag 的索引。这是最终我们所求结果的索引
2. 通过pivot_table 及聚合函数，快速生成个股每年分红表，用来向量化计算是否存在连续两年分红
3. 由表2和表1，把连续两年分红标记计算到月


## 预处理和生成索引

我们需要先将数据进行一点预处理，为每一条记录加上 fiscal_year 和 announce_ym 字段，并且生成一个空的 dataframe，用来存放处理后的数据。


```python
df = store.load_data(store.start, store.end)

df["end_date"] = pd.to_datetime(df["end_date"])
df["ann_date"] = pd.to_datetime(df["ann_date"])

df["fiscal_year"] = df["end_date"].dt.year
df["announce_ym"] = df["ann_date"].dt.to_period("M")

cols = ["asset", "fiscal_year", "announce_ym", "ann_date", "end_date"]
display(df[df.asset == "000001.SZ"][cols])

# 为每个股票-会计年度创建分红标记表
dividend_flags = df.pivot_table(
    index='asset',
    columns='fiscal_year',
    values='ann_date',
    aggfunc='count'  # 只要有分红就记为1
).fillna(0).astype(int)
    
dividend_flags
```

<!-- BEGIN IPYNB STRIPOUT -->

<!-- END IPYNB STRIPOUT -->

下面创建结果集：

```python
all_assets = df['asset'].unique()
all_months = pd.period_range(
    start=df['announce_ym'].min(),
    end=df['announce_ym'].max(),
    freq='M'
).astype(str)

# 生成所有可能的(月份, 股票)组合作为基础索引
index = pd.MultiIndex.from_product(
    [all_months, all_assets],
    names=['month', 'asset']
)
result_df = pd.DataFrame(index=index)

result_df
```

