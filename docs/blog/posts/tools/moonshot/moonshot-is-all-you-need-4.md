---
date: 2025-09-18
title: 研报复现之如何正确筛选『连续两年分红』股票（附代码）
category: tools
excerpt: 这个系列的跨度有点久了，在开始之前，先做一个前情提要。这个系列我们选择的是中金 2023 年 12 月的一份研报，名为《在手之鸟，红利优选策略》。
tags: [Moonshot, 回测，研报，tushare]
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/4.jpg
---

这个系列的跨度有点久了，在开始之前，先做一个前情提要。这个系列我们选择的是中金 2023 年 12 月的一份研报，名为《在手之鸟，红利优选策略》。它是一个基本面策略，通过这份研报的实现，我们可以了解到：

!!! abstract
    1. 如何获取各种基本面数据，并且对部分数据的含义及编纂方法进行讲解
    2. 月度调仓换股回测策略应该如何实现
    3. 获得一个红利优选基础策略。通过适当改变参数，即可用以实战。

该策略要用到以下数据：

1. 行情数据。任何策略都默认需要它，至少会在计算远期收益时使用。 <!-- pro.daily -->
2. 股息率，用来按股息率筛选个股，以及计算两年股息率均值因子。 <!-- pro.daily_basic -->
3. 分红数据。只有过去两年连续分红的公司才能入选。 <!-- pro.dividend -->
4. 审计意见。只有过去十年没有审计保留意见的公司才能入选。<!--pro.audit-->
5. 市值数据。只有市值大于 50 亿的公司才能入选。 <!-- pro.daily_basic -->
6. 净利润、营业收入和营业利润数据，用来计算净利润稳定性因子。<!-- pro.income -->
7. 股东数量变化 <!-- pro.stk_holdernumber -->
8. 换手率。用来计算换手波动率。<!-- pro.daily_basic -->
9. pe_ttm，用来计算 ep 因子。
10. 经营现金流数据，用来计算经营现金流资产比因子。<!-- pro.cashflow_vip.n_cashflow_act-->
11. 资产总计数据，与 10 一起，用来计算经营现金流资产比因子。 <!-- pro.balancesheet_vip.total_assets -->
12. 盈余公积金数据。与 11 一起，用来计算留存收益资产比因子。<!-- pro.balancesheet_vip.surplus_rese -->

<!--PAID CONTENT START-->
```python
import tushare as ts
from helper import qfq_adjustment
from fetchers import fetch_bars
from store import ParquetUnifiedStorage, CalendarModel
from moonshot import Moonshot
```
<!--PAID CONTENT END-->

在前面的分期文章中，我们已经获得了第 1~2 步的数据，并实现了按股息率进行票池筛选。回测表明，仅仅是通过股息率因子，我们就可以获得一定的年化超额，和更好的夏普比。

在这一期，我们将探讨如何把分红数据也纳入进来。研报要求，只有过去两年连续分红的公司才能入选票池。这是一个**看似简单，但实现上有一点点复杂度的需求**。这里实际上有一些魔术师的戏法，荟聚了多个 pandas 的技巧，才为一个简单的需求，提供了简洁的实现，而这也正是作者一直追求的目标。

## 获取分红数据

在上一篇中，我们已经获取了股息率数据，但要实现『连续两年分红』这个条件，为精确起见，我们不能把『连续两年股息率大于零』来当成『连续两年分红』，而是要直接获取分红原始记录。

!!! info
    通过 daily_basic 获得的股息率是一个按过去 12 个月滚动计算的股息率。根据它的计算方式，就可能存在这样的情况，比如 2023 年 12 月进行了分红，2024 年全年没有分红，但是直到 2024 年 11 月，股息率都会一直大于零。如此一来，在 2025 年 2 月，当我们问道，该股是否连续两年分红时，就会得到一个错误结果。在这方面，分红记录可能略微精确一点。

在 tushare 中，我们要通过 dividend 接口来获取分红数据。回测发生在 2018 年到 2023 年之间，我们再一次遇到如何在 tushare 中，获取这么长跨度的数据的问题。根据我们之前的讨论，我们应该选择一次查询可以获得最多数据的接口（参数）。

该接口签名如下：

```{code-block} python
def dividend(ts_code: str|None = None, 
             ann_date: str|None = None, 
             record_date: str|None = None, 
             ex_date: str|None = None, 
             imp_ann_date: str|None = None):
    pass
```

但是，如果按这些『**列出来**』的参数来进行查询，每次返回的数据量会很小，导致获取数据时间过长。这里我们又发现了一个**隐藏参数**，大家可以根据自己的情况来决定是否采用。这个参数就是 end_date。我们把使用各个参数进行查询所能得到的记录数比较一下：

```python
pro = ts.pro_api()

df_ann = pro.dividend(ann_date="20250419")
print("ann_date 一次返回数据：", len(df_ann))

df_end = pro.dividend(end_date="20241231", offse=0, limit=6000)
print("end_date 一次返回数据：", len(df_end))

df_ex = pro.dividend(ex_date="20250419")
print("ex_date 一次返回数据：", len(df_ex))

df_record = pro.dividend(record_date="20250419")
print("record_date 一次返回数据：", len(df_record))

df_imp = pro.dividend(imp_ann_date="20250419")
print("imp_ann_date 一次返回数据：", len(df_imp))
```

可以看到，使用 end_date 参数，可以获得的数据远远超过其它参数；但是，它的 limit 并不是我们常见的 6000，而是只能返回 2000。这些行为上的不一致，是我们要注意的。

由于这里的 limit 只有 2000，而现在 A 股有 5000 多支个股，所以，我们在通过 end_date 获取数据时，还必须通过 offset/limit 多次调用，才能取全一天的数据。

下面的代码演示了如何取区间 [start, end] 之间的数据：

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
    在本系列前面的章节中，我们在计算 [start, end] 之间的日期列表时，一般使用 bdate_range。它将获取一个排除了周六、周日的日期列表（但显然它不懂黄金周）。使用它来获取交易数据是 OK 的。但是，基本面数据可能发表在任何一天，所以，在这里，我们必须遍历全部日历，才能确保不漏掉一条数据。你有没有犯过类似的错误，从而不得不为排错浪费掉一个周末呢？

在最后，我们对数据进行了一些处理，使得返回的数据包含 asset, date 这两列，以便我们能像其它数据一样，自动化地利用缓存。

现在，我们就用之前开发的缓存来保存这些数据：

<!--PAID CONTENT START-->
```{code-block} python
# 本段代码已在课程环境中运行，数据已缓存，请勿重复运行
path = data_home / "rw/dividend.parquet"
store = ParquetUnifiedStorage(path, calendar)

for yr in (2018, 2019, 2020, 2021, 2022, 2023):
    start = datetime.date(yr, 1, 1)
    end = datetime.date(yr, 12, 31)

    data = fetch_dividend(start, end)
    store.append_data(data[data["div_proc"] == "实施"])

print(store.start, store.end)
store
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
```python
path = data_home / "rw/dividend.parquet"
store = ParquetUnifiedStorage(path, calendar)

for yr in (2018, 2019, 2020, 2021, 2022, 2023):
    start = datetime.date(yr, 1, 1)
    end = datetime.date(yr, 12, 31)

    data = fetch_dividend(start, end)
    store.append_data(data[data["div_proc"] == "实施"])

print(store.start, store.end)
store
```
<!-- END IPYNB STRIPOUT -->

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250905204554.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>原始分红记录</span>
</div>
<!-- END IPYNB STRIPOUT -->

分段获取的原因是为了保证万一出错，我们也不会损失太多数据。

文档没有说明这些记录是如何编纂的。根据我们的分析，公司可能在一年内有多次分红（可惜这样的公司太少了，所以你才不得不放弃价值投资，转学量化！）；对每一次分红，它可能有多条记录，分别对应于预案、股东大会通过和实施三个阶段。

对我们本次需求来说，只要关注『预案』阶段的记录就好。因为预案一旦发布，相关炒作资金就会闻风而动，不会等到实施阶段。在预案中，我们又只需要关注 end_date, ann_date，这是计算是否有连续两年分红的关键。

但是，请注意在示例代码，我们保存的是 div_proc 取值等于『实施』的记录。因为这条记录已经包含了预案阶段的全部信息，同时又提供了实施阶段的一些额外信息，还可以为今后其它用途使用。不过，我们要注意，在回测中，当我们把 ann_date 当成最新的时刻时，是不能去读 cash_div，record_date, ex_date 等信息的，此时它们还是『未来数据』

!!! tip
    tushare 的记录中给出了税后分红 (cash_div)，但文档中并没有明确指出它的计算方法，欢迎讨论！按相关法规，企业与个人股东的分红税率不一样，个人股东持有时间长短不一样，分红税率也不一样。因此，理论上讲，每一个 cash_div_tax，都应该对应多个 cash_div -- 看谁来读它。

要如何判断某只股票是否连续两年分红呢？最好是通过一个数据实例。不过，在讨论之前，我们要对数据进行一些预处理，这样讨论起来才会更加清晰易懂。

## 预处理和生成索引

判断『是否连续两年分红』的关键是，在每个月末，判断前两个年度（或者今年、去年）的分红方案是否已宣布。如果是，则我们可以标记该月为『满足连续分红条件』，记为 True；否则，记为 False。

因此，我们实际上只需要关心数据中的 asset, end_date 和 ann_date 三列，并且，为了比较和查找方便，我们应该将后二者分别转换为 fiscal_year（整数，对应的财年）和 announc_ym （宣布分红的年月）。

因此，我们要先进行以下转换：

```python
def pre_process(
    store, start: datetime.date | None = None, end: datetime.date | None = None
):
    df = store.get_and_fetch(start or store.start, end or store.end, call_direct=True)

    df["end_date"] = pd.to_datetime(df["end_date"])
    df["ann_date"] = pd.to_datetime(df["ann_date"])

    df["fiscal_year"] = df["end_date"].dt.year
    df["month"] = df["ann_date"].dt.to_period("M")

    # 某些个股在一个财年，可能会有多次分红，我们取最早的一次
    (
        df.sort_values(["asset", "fiscal_year", "ann_date"])
        .groupby(["asset", "fiscal_year"], as_index=False)
        .first()
    )

    cols = ["asset", "month", "fiscal_year"]
    return df[cols].set_index(["asset", "month"])


calendar = CalendarModel(data_home / "rw/calendar.parquet")

path = data_home / "rw/dividend.parquet"
store = ParquetUnifiedStorage(path, calendar, fetch_data_func = fetch_dividend)

start = datetime.date(2018, 11,30)
end = datetime.date(2023,11,30)
df = pre_process(store, start, end)
display(df.head())

df.query("asset == '000001.SZ'")

```

预处理的核心思想是把细粒度的时间数据转换成粗粒度的时间数据。这是月度回测中的核心技巧之一。在经过这样的转换之后，数据的查找、对齐和偏移计算就会易如反掌了。

其它值得注意的地方是，有一些个股会在一个财年，多次分红。这种情况下，我们需要进行去重，只保留最早的分红信息，因为最早的这条分红信息就足以说明财年有分红了。

这段示例的最后，我们截取了 PAYH 的一小段记录。从这段记录，我们可以推断，在 2022 年 3 月之后直到当年底，我们都可以认为 PAYH 在 2020 年的 2021 年是满足连续两年都分红的条件的。但是，在 2022 年 1 月到 2 月，过去两年的财政年度是 2020 和 2021 年，但 21 年可能仍然会分红，只是财报暂时还没批露。这种情况下，我们应该认为 PAYH 是满足连续两年都分红的条件，还是不满足？ To be or not to be，这还真是一个问题。而研报并没有给出答案。

在这里，我们只考虑大多数情况，那就是，如果是在当年的 4 月份前，未有分红记录的，只要前两年都有分红的，仍然按连续两年分红算。不过，凡事都有例外。好的公司年报预告会发得早；如果到了 4 月才发年报的，那么多数并不会有分红 -- 这相当于，如果倒数第三年、第二年经营业绩好，但倒数第一年经营业绩变差，我们必须延迟到 4 月底才能确认这一点。这会使得我们的策略引入一些不利的因素。

<!-- 复现基本面研报做基本面回测的难度主要在于数据。在现实中，在 2020 年 6 月 30 日这一天，如果分红实施方案是在 6 月 30 日公布的，理论上你应该可以在当天晚上就得到数据，并且用它来决定投资策略。但是，这取决于你使用的数据源。对所有人都公开所得的数据，也不一定对你的计算机程序可得。如果你在实盘中使用的数据源处理起来没有那么快，那么，你的回测结果仍然无法用以实盘。

逻辑很简单。复杂性在于，如何高效地为每一个月生成 flag（以表明在该月，该股是否连续两年分红）。这里我们将使用以下技巧：

1. 通过月度和股票代码创建一个笛卡尔积，作为每支股票、每月 flag 的索引。这是最终我们所求结果的索引
2. 通过 pivot_table 及聚合函数，快速生成个股每年分红表，用来向量化计算是否存在连续两年分红
3. 由表 2 和表 1，把连续两年分红标记计算到月 -->

## 连续两年分红的逻辑的代码实现

刚刚我们对数据进行了一些预处理，在此基础上，讨论清楚了站在具体的时间节点上，『什么叫连续两年分红』。

现在，我们如何将这个逻辑代码化？

首先，明确我们的目标，是要得到这样一个输出：对每一个 asset 的每一个 month，存在一个标记 (flag)，能指出该 asset 在该 month 时，是否满足连续两年分红的条件。

我们来看看这个结果表格应该长什么样：

```python
all_assets = df.index.levels[0].unique()
months = df.index.levels[1].unique()

all_months = pd.period_range(start=months.min(), end=months.max(), freq="M")

# 生成所有可能的（月份，股票）组合作为基础索引
index = pd.MultiIndex.from_product([all_assets, all_months], names=["asset", "month"])

# result_df 目前是一个空表格
result_df = pd.DataFrame(columns = ["consective_div"], index=index)
```

接下来，我们把前面得到的关于 fiscal_year 和 announce_ym 的表格展开到与上述 result_df 对齐。对齐之后，剩下的计算就会变成是从一个表格映射到另一个表格那样简单。

```python
# 按结果表格进行索引展开
expanded = pd.merge(pd.DataFrame(index=index), 
                  df, how="left", 
                  left_index=True, 
                  right_index=True
            )

# 将 fiscal_year 前向填充
expanded = expanded.groupby(level = "asset").ffill()
expanded.tail()
```

现在，我们只需要对上述展开后的 dataframe，按 asset 进行 groupby，然后在每个分组中，启用一个大小为 24 的滑动窗口，再判断索引 month 是否在滑动窗口的 fiscal_year 集合内即可。

```python
# example-consective-div
def calc_asset_flag(group: pd.DataFrame):
    df = group.copy()

    df["month_num"] = df.index.levels[1].month
    df["year"] = df.index.levels[1].year

    # 这里无法使用 rolling，因为 rolling 后面要跟聚合函数，不能返回 set
    df["prev_fiscal_set"] = [
        set(df.iloc[max(0, i - 24) : i]["fiscal_year"]) for i in range(len(df))
    ]

    def calc_row_flag(row):
        prev_fiscal = row["prev_fiscal_set"]
        month_num = row["month_num"]
        year = row["year"]

        if month_num > 4:  # 4 月之后，必须最近两年财年都有分红
            flag = ((year - 1) in prev_fiscal) and ((year - 2) in prev_fiscal)
            return flag
        else:  # 4 月之前，最近两财年有分红，或者之前两个财年有分红。
            flag = (((year - 1) in prev_fiscal) and ((year - 2) in prev_fiscal)) or (
                ((year - 2) in prev_fiscal) and ((year - 3) in prev_fiscal)
            )
            return flag

    df["consective_div"] = df.apply(calc_row_flag, axis=1)

    return df.drop(columns=["month_num", "year", "prev_fiscal_set"]).droplevel(level=0)

consective_div = expanded.groupby(level="asset").apply(calc_asset_flag)
consective_div.tail()

```

这段代码中，值得注意的地方有两处。首先，当提到『滚动』求值时，我们很容易想到使用滑动窗口。但在第 7 行处，我们使用循环，而不是 rolling.apply 来找出对应行的前两年数值。因为 rolling.apply 一般应用于聚合操作，函数的返回值必须是数值型。

第 2 点就是第 29 行，它实际上仍然是一个循环。考虑到 calc_row_flag 只是在行内进行比较操作，这里可以进一步优化，以启用并行机制。在我的电脑上，这段代码运行了 13 秒，速度还是有点慢的。

如何验证这里的逻辑正确呢？对 PAYH，我们看到，从 2020 年 3 月起，每个月的 flag 都是 1；这是正确的，因为它每一年都有分红。我们还找了一个反面的例子， 920819，这是它的分红记录：

<!--PAID CONTENT START-->
```python
df_ = ts.pro_api().dividend(ts_code = "920819.BJ")
df_[df_.div_proc == '实施'][["ts_code", "end_date", "ann_date"]]
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250908181932.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

它在 2020， 2022， 2024 年都有分红，但在 2021 年没有分红（有预案，但没有通过）。所以，只有从 2024 年 1 月起，『连续两年分红』查询才显示它满足条件。

这证明了我们的实现是正确的。

## 应用分红筛选

```python
def consective_dividend_screen(data):
    return data.consective_div

start = datetime.date(2018, 1, 1)
end = datetime.date(2023, 12, 31)

store_path = data_home / "rw/bars.parquet"
bars_store = ParquetUnifiedStorage(store_path, calendar, fetch_data_func=fetch_bars)

barss = bars_store.get_and_fetch(start, end)
ms = Moonshot(barss)

# consecative_div 示例 example-consective-div
ms.append_factor(consective_div, "consective_div")

# 我们把上一篇的股息率筛选也加上
store_path = data_home / "rw/dv_ttm.parquet"
dv_store = ParquetUnifiedStorage(store_path, calendar, fetch_data_func=fetch_dv_ttm)
dv_ttm = dv_store.get_and_fetch(start, end)
ms.append_factor(dv_ttm, "dv_ttm", resample_method = 'last')

output = get_jupyter_root_dir() / "reports/moonshot_v4.html"
# 筛选！ 回测！ 报告！
(
    ms.screen(dividend_yield_screen, data = ms.data, n=500)
   .screen(consective_dividend_screen, data = ms.data)
   .calculate_returns()
   .report(output = output)
)

```

最终，我们得到以下报告：

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250908210330.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

!!! info
    研究平台用户请双击 /reports/moonshot_v4.html 来查看更详细的报告。此目录和文件可以 jupyter lab 的侧边栏中找到。

你也许已经发现，在加入新的筛选条件之后，策略的超额收益、相对夏普超额（如果可以这么说的话）都超过了前一期。尽管报告是这么说的，也确实应该如此，不过任何时候，在面对回测时的好消息时，你都应该再核对一遍：

这**两次回测的时间区间不一样，所以，它们无法直接比较**。尽管我们获取数据时，都使用了一样的起止区间，但是，『连续两年分红』筛选存在一个两年的『冷启动』期。它导致了策略必须在指定的起始时间之后两年才能开始回测。

尽管这里存在需要数据对齐的问题，幸运的是，Moonshot 默默承担了一切。

<!-- BEGIN IPYNB STRIPOUT -->
## 后记

如果你对本文代码感兴趣，可以加入会员，我们提供数据、代码和运行环境，立即运行和验证策略。如果对文中技术细节不太熟悉，可选修我们的课程。

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/promotion/fa.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

