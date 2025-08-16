---
title: 『Moonshot is all you need』 03 - 
date: 2025-08-16
excerpt: 
category: tools
tags: [Moonshot, 回测, 研报, tushare]
img: 
---

这是复现基本面月度调仓策略的第三篇。在第一篇里，我们介绍了月度调仓的核心思想。在第二篇里，我们介绍了研报要求的数据清单，并以 tushare 为例，介绍了如何获取日线行情数据，并且实现了数据增量更新的一个高性能、但又极简的框架。

现在，我们就进入到第二阶段，逐步增加因子，并进行回测。

我们首先要添加的是股息率，并且根据股息率来实现股票池的筛选。

## 获取股息率

在 tushare 中，我们有两种方案可以获取股息率。其一是通过 daily_basic 接口。其二是先通过 dividend 接口获取每股分红，再除以每股股价，即可得到股息率。

在这里，我们只演示第一种方法。但在后面实现按两年连续分红条件筛选公司时，我们会演示如何使用 dividend 接口。

daily_basic 接口可用来获取以日期为索引的一些常用数据，比如当日收盘价、换手率、市盈率、市值等大约15列数据。它的签名如下：

```python
def daily_basic(
    ts_code: str, trade_date: str, start_date: str, end_date: str
) -> pd.DataFrame:
    pass
```

其中 ts_code 与 trade_date 必选其一。与其它多数 tushare 函数一样，它有返回记录限制，目前是6000条。这样在一次存取中，可以取某支股票25年左右的数据，或者所有股票一天的数据。

!!! attention 存取限制
    一次可存取记录条数限制可能取决于你的账号。这里6000条是积分5000以上账号的限制。


下面的代码演示了如何获取股息率及 PE 等数据：

```python
# example-1
def fetch_dv_ttm(start: datetime, end: datetime) -> pd.DataFrame:
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        dfs.append(df)

    return pd.concat(dfs)


df = fetch_dv_ttm(datetime.date(2019, 10, 8), datetime.date(2019, 11, 1))
df
```

在示例期间共有19个交易日。获取19个交易日的数据，大约花了10.3秒。相当于每0.5秒能获取一天的数据。这样获取一年的数据，大约需要2分钟。

!!! info
    根据后面策略的需要，我们通过这段代码，将[2018年8月1日 ~ 2023年11月30日]期间的数据存入本地磁盘。

    ```python
    data_home = Path("/tmp/moonshot/data")
    df.to_parquet(data_home / "dv_ttm.parquet")
    ```


我们也可以使用 undocumented 的参数来加快这个进程：


```python
# example-2
def _fetch_dv_ttm(start: datetime.date, end: datetime.date):
    """递归获取完整的daily_basic数据，处理offset限制问题"""
    dfs = []
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"

    page_size = 6_000
    offset_limit = 100_000

    current_start = start
    current_end = end

    def fetch_batch(batch_start: datetime.date, batch_end: datetime.date):
        batch_dfs = []
        last_trade_date = None

        for i in range(0, int(offset_limit / page_size)):
            offset = i * page_size
            df = pro.daily_basic(
                start_date=batch_start.strftime("%Y%m%d"),
                end_date=batch_end.strftime("%Y%m%d"),
                fields=cols,
                offset=offset,
                pagesize=page_size,
            )

            if len(df) == 0:
                break

            batch_dfs.append(df)
            last_trade_date = df.iloc[-1]["trade_date"]  # 最后一条记录的日期

            # 如果返回的数据少于page_size，说明已经获取完毕
            if len(df) < page_size:
                return batch_dfs, None

        # 如果达到了offset_limit，返回最后获取到的交易日期
        return batch_dfs, last_trade_date

    # 主循环：处理可能需要多次调用的情况
    while current_start <= current_end:
        batch_dfs, last_date = fetch_batch(current_start, current_end)
        print(f"获取数据: {current_start} ~ {current_end}，最后数据日: {last_date}")
        dfs.extend(batch_dfs)

        if last_date is None:
            # 数据获取完毕
            break

        # 将last_date转换为datetime.date格式
        last_date_obj = datetime.datetime.strptime(last_date, "%Y%m%d").date()

        # 确保new_end不小于start
        if last_date_obj < start:
            break

        current_end = last_date_obj

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        # 去重，因为可能有重复的日期数据
        result_df = result_df.drop_duplicates(subset=["ts_code", "trade_date"])
        # 按交易日期排序
        result_df = result_df.sort_values(["trade_date", "ts_code"])
        return result_df
    else:
        return pd.DataFrame()
```

在同样的起止区间（2019年10月8日到2019年12月31日）里，示例1需要45.5秒；示例2需要24秒左右。如果我们存取的时间区间更早一点，那么这个加速比还会更大一点。因为早期上市公司的数量更少，所以，按天存取数据，一天能获取的记录数会大大小于6000。

不过，尽管如此，我们还是要谨慎使用这些 undocumented 的参数。

## 题外话： 获取日线行情

任何策略数据都需要行情数据--至少是为了计算远期收益。这是一个简单的任务，为了完备起见，我们也把如何通过 tushare 来获取日线行情数据的代码附在这里，并且，我们还将提供复权的高效实现代码。

提到行情数据，就离不开复权。我们先看如何高效地实现复权。







## 条件1： 按股息率进行筛选
## 获取股息率

在 tushare 中，我们有两种方案可以获取股息率。其一是通过 daily_basic 接口。其二是先通过 dividend 接口获取每股分红，再除以除以每股股价，即可得到股息率。

在这里，我们只演示第一种方法。但在后面实现按两年连续分红条件筛选公司时，我们会演示如何使用 dividend 接口。

daily_basic 接口可用来获取以日期为索引的一些常用数据，比如当日收盘价、换手率、市盈率、市值等大约15列数据。它的签名如下：

```python
def daily_basic(
    ts_code: str, trade_date: str, start_date: str, end_date: str
) -> pd.DataFrame:
    pass
```

其中 ts_code 与 trade_date 必选其一。与其它多数 tushare 函数一样，它有返回记录限制，在我们的测试中，目前是6000条。这样在一次存取中，可以取某支股票25年左右的数据，或者所有股票一天的数据。

这个接口也支持通过 offset 和 pagesize 参数，在一次查询中返回更多的数据，不过它们是 undocumented 的参数，并不可靠，并且，依然受到单次返回6000条记录的限制，所以网络往返的时间并不能省下来。根据具体的需求来看，使用这个 undocumented 的参数，速度的提升大致会在20%到80%之间。

下面的代码演示了如何获取股息率及 PE 等数据：

```python
# example-1
def fetch_dv_ttm(start: datetime, end: datetime) -> pd.DataFrame:
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        dfs.append(df)

    return pd.concat(dfs)


df = fetch_dv_ttm(datetime.date(2019, 10, 8), datetime.date(2019, 11, 1))
df
```
在示例期间共有19个交易日。获取19个交易日的数据，大约花了10.3秒。相当于每0.5秒能获取一天的数据。这样获取一年的数据，大约需要2分钟。

!!! info
    根据后面策略的需要，我们通过这段代码，将[2018年8月1日 ~ 2023年11月30日]期间的数据存入本地磁盘。

    ```python
data_home = Path("/tmp/moonshot/data")
    df.to_parquet(data_home / "dv_ttm.parquet")
```


我们也可以使用 undocumented 的参数来加快这个进程：


```python
# example-2
def _fetch_dv_ttm(start: datetime.date, end: datetime.date):
    """递归获取完整的daily_basic数据，处理offset限制问题"""
    dfs = []
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"

    page_size = 6_000
    offset_limit = 100_000

    current_start = start
    current_end = end

    def fetch_batch(batch_start: datetime.date, batch_end: datetime.date):
        batch_dfs = []
        last_trade_date = None

        for i in range(0, int(offset_limit / page_size)):
            offset = i * page_size
            df = pro.daily_basic(
                start_date=batch_start.strftime("%Y%m%d"),
                end_date=batch_end.strftime("%Y%m%d"),
                fields=cols,
                offset=offset,
                pagesize=page_size,
            )

            if len(df) == 0:
                break

            batch_dfs.append(df)
            last_trade_date = df.iloc[-1]["trade_date"]  # 最后一条记录的日期

            # 如果返回的数据少于page_size，说明已经获取完毕
            if len(df) < page_size:
                return batch_dfs, None

        # 如果达到了offset_limit，返回最后获取到的交易日期
        return batch_dfs, last_trade_date

    # 主循环：处理可能需要多次调用的情况
    while current_start <= current_end:
        batch_dfs, last_date = fetch_batch(current_start, current_end)
        print(f"获取数据: {current_start} ~ {current_end}，最后数据日: {last_date}")
        dfs.extend(batch_dfs)

        if last_date is None:
            # 数据获取完毕
            break

        # 将last_date转换为datetime.date格式
        last_date_obj = datetime.datetime.strptime(last_date, "%Y%m%d").date()

        # 确保new_end不小于start
        if last_date_obj < start:
            break

        current_end = last_date_obj

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        # 去重，因为可能有重复的日期数据
        result_df = result_df.drop_duplicates(subset=["ts_code", "trade_date"])
        # 按交易日期排序
        result_df = result_df.sort_values(["trade_date", "ts_code"])
        return result_df
    else:
        return pd.DataFrame()
```
在同样的起止区间（2019年10月8日到2019年12月31日）里，示例1需要45.5秒；示例2需要24秒左右。如果我们存取的时间区间更早一点，那么这个加速比还会更大一点。因为早期上市公司的数量更少，所以，按天存取数据，一天能获取的记录数会大大小于6000。

不过，尽管如此，我们还是要谨慎使用这些 undocumented 的参数。

## 题外话： 获取日线行情

任何策略数据都需要行情数据--至少是为了计算远期收益。这是一个简单的任务，为了完备起见，我们也把如何通过 tushare 来获取日线行情数据的代码附在这里，并且，我们还将提供复权的高效实现代码。

提到行情数据，就离不开复权。我们先看如何高效地实现复权。







## 条件1： 按股息率进行筛选
获取股息率

在 tushare 中，我们有两种方案可以获取股息率。其一是通过 daily_basic 接口。其二是先通过 dividend 接口获取每股分红，再除以除以每股股价，即可得到股息率。

在这里，我们只演示第一种方法。但在后面实现按两年连续分红条件筛选公司时，我们会演示如何使用 dividend 接口。

daily_basic 接口可用来获取以日期为索引的一些常用数据，比如当日收盘价、换手率、市盈率、市值等大约15列数据。它的签名如下：

```python
def daily_basic(
    ts_code: str, trade_date: str, start_date: str, end_date: str
) -> pd.DataFrame:
    pass
```

其中 ts_code 与 trade_date 必选其一。与其它多数 tushare 函数一样，它有返回记录限制，在我们的测试中，目前是6000条。这样在一次存取中，可以取某支股票25年左右的数据，或者所有股票一天的数据。

这个接口也支持通过 offset 和 pagesize 参数，在一次查询中返回更多的数据，不过它们是 undocumented 的参数，并不可靠，并且，依然受到单次返回6000条记录的限制，所以网络往返的时间并不能省下来。根据具体的需求来看，使用这个 undocumented 的参数，速度的提升大致会在20%到80%之间。

下面的代码演示了如何获取股息率及 PE 等数据：

```python
# example-1
def fetch_dv_ttm(start: datetime, end: datetime) -> pd.DataFrame:
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        dfs.append(df)

    return pd.concat(dfs)


df = fetch_dv_ttm(datetime.date(2019, 10, 8), datetime.date(2019, 11, 1))
df
```
在示例期间共有19个交易日。获取19个交易日的数据，大约花了10.3秒。相当于每0.5秒能获取一天的数据。这样获取一年的数据，大约需要2分钟。

!!! info
    根据后面策略的需要，我们通过这段代码，将[2018年8月1日 ~ 2023年11月30日]期间的数据存入本地磁盘。

    ```python
data_home = Path("/tmp/moonshot/data")eee
    df.to_parquet(data_home / "dv_ttm.parquet")
```


我们也可以使用 undocumented 的参数来加快这个进程：


```python
# example-2
def _fetch_dv_ttm(start: datetime.date, end: datetime.date):
    """递归获取完整的daily_basic数据，处理offset限制问题"""
    dfs = []
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"

    page_size = 6_000
    offset_limit = 100_000

    current_start = start
    current_end = end

    def fetch_batch(batch_start: datetime.date, batch_end: datetime.date):
        batch_dfs = []
        last_trade_date = None

        for i in range(0, int(offset_limit / page_size)):
            offset = i * page_size
            df = pro.daily_basic(
                start_date=batch_start.strftime("%Y%m%d"),
                end_date=batch_end.strftime("%Y%m%d"),
                fields=cols,
                offset=offset,
                pagesize=page_size,
            )

            if len(df) == 0:
                break

            batch_dfs.append(df)
            last_trade_date = df.iloc[-1]["trade_date"]  # 最后一条记录的日期

            # 如果返回的数据少于page_size，说明已经获取完毕
            if len(df) < page_size:
                return batch_dfs, None

        # 如果达到了offset_limit，返回最后获取到的交易日期
        return batch_dfs, last_trade_date

    # 主循环：处理可能需要多次调用的情况
    while current_start <= current_end:
        batch_dfs, last_date = fetch_batch(current_start, current_end)
        print(f"获取数据: {current_start} ~ {current_end}，最后数据日: {last_date}")
        dfs.extend(batch_dfs)

        if last_date is None:
            # 数据获取完毕
            break

        # 将last_date转换为datetime.date格式
        last_date_obj = datetime.datetime.strptime(last_date, "%Y%m%d").date()

        # 确保new_end不小于start
        if last_date_obj < start:
            break

        current_end = last_date_obj

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        # 去重，因为可能有重复的日期数据
        result_df = result_df.drop_duplicates(subset=["ts_code", "trade_date"])
        # 按交易日期排序
        result_df = result_df.sort_values(["trade_date", "ts_code"])
        return result_df
    else:
        return pd.DataFrame()
```
在同样的起止区间（2019年10月8日到2019年12月31日）里，示例1需要45.5秒；示例2需要24秒左右。如果我们存取的时间区间更早一点，那么这个加速比还会更大一点。因为早期上市公司的数量更少，所以，按天存取数据，一天能获取的记录数会大大小于6000。

不过，尽管如此，我们还是要谨慎使用这些 undocumented 的参数。

## 题外话： 获取日线行情

任何策略数据都需要行情数据--至少是为了计算远期收益。这是一个简单的任务，为了完备起见，我们也把如何通过 tushare 来获取日线行情数据的代码附在这里，并且，我们还将提供复权的高效实现代码。

提到行情数据，就离不开复权。我们先看如何高效地实现复权。







## 条件1： 按股息率进行筛选
## 获取股息率

在 tushare 中，我们有两种方案可以获取股息率。其一是通过 daily_basic 接口。其二是先通过 dividend 接口获取每股分红，再除以除以每股股价，即可得到股息率。

在这里，我们只演示第一种方法。但在后面实现按两年连续分红条件筛选公司时，我们会演示如何使用 dividend 接口。

daily_basic 接口可用来获取以日期为索引的一些常用数据，比如当日收盘价、换手率、市盈率、市值等大约15列数据。它的签名如下：

```python
def daily_basic(
    ts_code: str, trade_date: str, start_date: str, end_date: str
) -> pd.DataFrame:
    pass
```

其中 ts_code 与 trade_date 必选其一。与其它多数 tushare 函数一样，它有返回记录限制，在我们的测试中，目前是6000条。这样在一次存取中，可以取某支股票25年左右的数据，或者所有股票一天的数据。

这个接口也支持通过 offset 和 pagesize 参数，在一次查询中返回更多的数据，不过它们是 undocumented 的参数，并不可靠，并且，依然受到单次返回6000条记录的限制，所以网络往返的时间并不能省下来。根据具体的需求来看，使用这个 undocumented 的参数，速度的提升大致会在20%到80%之间。

下面的代码演示了如何获取股息率及 PE 等数据：

```python
# example-1
def fetch_dv_ttm(start: datetime, end: datetime) -> pd.DataFrame:
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"
    dfs = []
    for dt in pd.bdate_range(start, end):
        dtstr = dt.strftime("%Y%m%d")
        df = pro.daily_basic(trade_date=dtstr, fields=cols)
        dfs.append(df)

    return pd.concat(dfs)


df = fetch_dv_ttm(datetime.date(2019, 10, 8), datetime.date(2019, 11, 1))
df
```
在示例期间共有19个交易日。获取19个交易日的数据，大约花了10.3秒。相当于每0.5秒能获取一天的数据。这样获取一年的数据，大约需要2分钟。

!!! info
    根据后面策略的需要，我们通过这段代码，将[2018年8月1日 ~ 2023年11月30日]期间的数据存入本地磁盘。

    ```python
    data_home = Path("/tmp/moonshot/data")
    df.to_parquet(data_home / "dv_ttm.parquet")
    ```


我们也可以使用 undocumented 的参数来加快这个进程：


```python
# example-2
def _fetch_dv_ttm(start: datetime.date, end: datetime.date):
    """递归获取完整的daily_basic数据，处理offset限制问题"""
    dfs = []
    pro = pro_api()
    cols = "ts_code,trade_date,dv_ttm,total_mv,turnover_rate,pe_ttm"

    page_size = 6_000
    offset_limit = 100_000

    current_start = start
    current_end = end

    def fetch_batch(batch_start: datetime.date, batch_end: datetime.date):
        batch_dfs = []
        last_trade_date = None

        for i in range(0, int(offset_limit / page_size)):
            offset = i * page_size
            df = pro.daily_basic(
                start_date=batch_start.strftime("%Y%m%d"),
                end_date=batch_end.strftime("%Y%m%d"),
                fields=cols,
                offset=offset,
                pagesize=page_size,
            )

            if len(df) == 0:
                break

            batch_dfs.append(df)
            last_trade_date = df.iloc[-1]["trade_date"]  # 最后一条记录的日期

            # 如果返回的数据少于page_size，说明已经获取完毕
            if len(df) < page_size:
                return batch_dfs, None

        # 如果达到了offset_limit，返回最后获取到的交易日期
        return batch_dfs, last_trade_date

    # 主循环：处理可能需要多次调用的情况
    while current_start <= current_end:
        batch_dfs, last_date = fetch_batch(current_start, current_end)
        print(f"获取数据: {current_start} ~ {current_end}，最后数据日: {last_date}")
        dfs.extend(batch_dfs)

        if last_date is None:
            # 数据获取完毕
            break

        # 将last_date转换为datetime.date格式
        last_date_obj = datetime.datetime.strptime(last_date, "%Y%m%d").date()

        # 确保new_end不小于start
        if last_date_obj < start:
            break

        current_end = last_date_obj

    if dfs:
        result_df = pd.concat(dfs, ignore_index=True)
        # 去重，因为可能有重复的日期数据
        result_df = result_df.drop_duplicates(subset=["ts_code", "trade_date"])
        # 按交易日期排序
        result_df = result_df.sort_values(["trade_date", "ts_code"])
        return result_df
    else:
        return pd.DataFrame()
```
在同样的起止区间（2019年10月8日到2019年12月31日）里，示例1需要45.5秒；示例2需要24秒左右。如果我们存取的时间区间更早一点，那么这个加速比还会更大一点。因为早期上市公司的数量更少，所以，按天存取数据，一天能获取的记录数会大大小于6000。

不过，尽管如此，我们还是要谨慎使用这些 undocumented 的参数。

## 题外话： 获取日线行情

任何策略数据都需要行情数据--至少是为了计算远期收益。这是一个简单的任务，为了完备起见，我们也把如何通过 tushare 来获取日线行情数据的代码附在这里，并且，我们还将提供复权的高效实现代码。

提到行情数据，就离不开复权。我们先看如何高效地实现复权。







## 条件1： 按股息率进行筛选
