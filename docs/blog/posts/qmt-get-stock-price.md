---
theme: /apps/slidev_themes/theme_calendar
title: 免费行情方案之QMT
slug: qmt-get-stock-price
date: 2023-12-21
lunar: 11 月初九
canvasWidth: 1200
categories:
    - QMT
tags:
    - QMT
    - 数据源
    - XTQUANT
---

!!! tip "学习要点"
    - xtquant 提供了数据和交易接口
    - xtquant 可以独立于 QMT 之外运行
    - download_history_data
    - download_history_data2
    - get_market_data

<!--more-->

## QMT 和 XtQuant 简介
QMT 是目前接入门槛最低的量化实盘接口之一。它提供了本地部署的量化平台（可以回测和实盘），也提供了可独立于该平台运行的 SDK，即 XtQuant。

XtQuant 仅提供行情数据和交易接口，不提供回测功能。目前通过 XtQuant 获取普通行情数据是免费的，但有流速限制，据测试，低于 1 秒获取一次是没有问题的。

## XtQuant 获取行情数据

XtQuant 中，数据获取一般分两个阶段，首先是缓存阶段，然后是读取阶段。


缓存阶段的 API 一般以 download_开头。

因此，我们要获取历史行情数据，首先要进行缓存。使用的 API 是：

```python
def download_history_data(stock_code: str='', 
                      period: str='', 
                      start_time: str='', 
                      end_time: str='', 
                      incrementally: Optional[bool]=None
                      )
```

如果我们要一次下载多支证券的行情数据，还可以使用`download_history_data2`这个 API。

如果在 start_time 到 end_time 区间的数据被缓存后，我们就可以调用`get_market_data`来获取行情数据。

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

该方法可以获取'1m', '5m', '15m', '30m', '1h', '1d'和分笔 (`tick`) 数据。不同的周期下，返回的字段有所不同。除分笔外，能返回的数据包括时间，OHLC，volume（成交手）和 amount（成交金额）。



!!! warning
    `fill_data`建议都设置为 False。它的行为是使用前一条数据进行填充，类似于 pandas 的 fillna 中的`ffil`。但行情软件在计算技术指标时，都是跳过这些缺失数据，而不是使用的填充数据。因此，我们也应该将`fill_data`设置为 False, 以避免与其它人行为不一致。


注意该方法不能返回复权因子。因此，如果我们不是为了直接使用返回的数据，而是要将其转存到其它数据库的话，我们还需要调用`get_divid_factors`来获得复权因子，与这里获得的未复权数据一起保存。直接转存任何已经复权的数据是没有意义的。即使是后复权，也存在出错的可能。


