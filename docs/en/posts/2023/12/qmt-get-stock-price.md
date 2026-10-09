---
title: "Free Quant Data with QMT: XtQuant Setup Guide"
date: 2023-12-21
slug: en/posts/tools/qmt-get-stock-price
tags: [QMT, XtQuant, Market Data]
excerpt: "XtQuant is QMT's standalone SDK for free market data and trading. This guide shows how to cache history with download_history_data and read bars with get_market_data."
lang: en
translation_of: posts/tools/qmt-get-stock-price
auto_translated: true
source_sha: ba07729828707b698698a6dd810e8d29ecadf208
---

!!! tip "Key Takeaways"
    - xtquant provides both market data and trading APIs
    - xtquant can run standalone, outside QMT
    - download_history_data
    - download_history_data2
    - get_market_data

<!--more-->

## Introduction to QMT and XtQuant
QMT is one of the most accessible interfaces for live trading in quantitative trading. It ships as a locally deployed quant platform that supports both backtest and live trading, plus an SDK that runs independently of the platform — XtQuant.

XtQuant only exposes market data and trading APIs — there is no backtest engine. Standard market data is currently free through XtQuant, though rate-limited. In testing, one request per second is well within the limit.

## Fetching Market Data with XtQuant
In XtQuant, data access is a two-step process: cache first, then read.

Cache-stage APIs generally start with `download_`.

So to get historical bars, you first populate the local cache with:

```python
def download_history_data(stock_code: str='', 
                      period: str='', 
                      start_time: str='', 
                      end_time: str='', 
                      incrementally: Optional[bool]=None
                      )
```

To download bars for multiple securities in one go, use `download_history_data2`.

Once the `start_time` to `end_time` range is cached, you can read it with `get_market_data`:

```python
def get_market_data(field_list = [], 
                    stock_list = [], 
                    period = '1d',
                    start_time = '', 
                    end_time = '', 
                    count = -1,
                    dividend_type = 'none', 
                    fill_data = True
)
```

This method supports `'1m'`, `'5m'`, `'15m'`, `'30m'`, `'1h'`, `'1d'`, and `tick` data. Available fields vary by period. Except for ticks, you get timestamp, OHLC, volume (in lots) and amount (in currency value).

!!! warning
    Set `fill_data` to False. When True, it forward-fills from the previous bar, similar to `ffill` in pandas `fillna`. Market-data terminals skip those missing bars when computing indicators instead of using filled values, so you should set `fill_data` to False to stay consistent with everyone else.

Note that this method cannot return adjustment factors. If you plan to archive the data into another database rather than just using the returned bars directly, also call `get_divid_factors` and store the unadjusted bars together with the factors. Persisting already-adjusted data is meaningless — even backward-adjusted data can introduce errors.

## Example

```python
from xtquant import xtdata

stocks = ['000001.SZ', '600000.SH']
xtdata.download_history_data(stocks[0], '1d')
xtdata.download_history_data(stocks[1], '1d')

# 或者
# XTDATA.DOWNLOAD_HISTORY_DATA2(STOCKS, '1D')

end = "20231220"
bars = xtdata.get_market_data(stock_list=stocks, 
                              period='1d', 
                              end_time=end, 
                              count=-1, 
                              dividend_type="front_ratio")

end = "20231220"
bars = xtdata.get_market_data(stock_list=stocks, period='1d', end_time=end, count=-1, dividend_type="front_ratio")

display(bars['close'].T.tail())
```

`get_market_data` returns a dict. Each key is a market-data field such as `time`, `open`, or `close`, and each value is a frame indexed by ticker with timestamps as columns. In the example above we transpose it, which is how you will normally work with it.

The final output looks like this:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/qmt_get_price.png)

Note the date format used by xtquant: `"YYYYMMDD"` for the `1d` period, and `"YYYYMMDDHHmmss"` for intraday periods. If you start from a datetime.datetime, format it like this:

```python
import datetime

now = datetime.datetime.now()
print(now.strftime("%Y%m%d%H%M%S"))

import arrow
arrow.get(now).format("YYYYMMDDHHmmss")
```

`strftime` format strings are hard to remember. The arrow library improves on this with a progressive, largest-to-smallest pattern that is much easier to recall. When performance is not critical, convert to an Arrow object first and then format.
