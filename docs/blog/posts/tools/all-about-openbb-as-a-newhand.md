---
title: OpenBB实战！轻松获取海外市场数据
date: 2024-08-13
category: tools
slug: all-about-openbb-as-a-newhand
motto: 
img: https://images.jieyu.ai/images/2024/08/unsplash-claudio.jpg
stamp_width: 60%
stamp_height: 60%
tags: [tools, openbb, 数据]
---

你有没有这样的经历？常常看到一些外文的论文或者博文，研究方法很好，结论也很吸引人，忍不住就想复现一下。

但是，这些文章用的数据往往都是海外市场的。我们怎么才能获得**免费的**海外市场数据呢？

之前有 yfinance，但是从 2021 年 11 月起，就对内陆地区不再提供服务了。我们今天就介绍这样一个工具，OpenBB。它提供了一个数据标准，通过它可以聚合许多免费和付费的数据源。

在海外市场上，Bloomberg 毫无疑问是数据供应商的老大，产品和服务包括财经新闻、市场数据、分析工具，在全球金融市场中具有极高的影响力，是许多金融机构、交易员、分析师和决策者不可或缺的信息来源。不过 Bloomberg 的数据也是真的贵。如果我们只是个人研究，或者偶尔使用一下海外数据，显然，还得寻找更有性价比的数据源。

于是，OpenBB 就这样杀入了市场。从这名字看，它就是一个 Open Source 的 Bloomberg。

OpenBB 有点纠结。一方面，它是开源的，另一方面，它又有自己的收费服务。当然，在金融领域做纯开源其实也没有什么意义，指着人家免费，自己白嫖赚钱，这事也说不过去。大家都是冲着赚钱来的，付费服务不寒碜人。

!!! info
    感谢这些开源的产品，让所有人都有机会，From Zero To Hero! 金融一向被视为高端游戏，主要依赖性和血液来传播。开源撕开了一条口子，让普通人也能窥见幕后的戏法。<br>如果使用过 OpenBB，而它也确实达成了它的承诺，建议你前往 Github，为它点一个赞。<br>开源项目不需要我们用金钱来支持，但如果我们都不愿意给它一个免费的拥抱，最后大家就只能使用付费产品了。

## 安装 openbb

通过以下命令安装 openbb:

```bash
pip install openbb[all]
```

!!! tip
    openbb 要求的 Python 版本是 3.11 以上。你最好单独为它创建一个虚拟环境。

安装后，我们有多种方式可以使用它。

## 使用命令行

安装后，我们可以在命令行下启动 openbb。

![](https://images.jieyu.ai/images/2024/08/openbb-cli.jpg)

然后就可以按照提示，输入命令。比如，如果我们要获得行情数据，就可以一路输入命令 equity > price, 再输入 historical --symbol LUV --start_date '2024-01-01' --end_date '2024-08-01'，就可以得到这支股票的行情数据。

openbb 会在此时弹出一个窗口，以表格的形式展示行情数据，并且允许你在此导出数据。

![](https://images.jieyu.ai/images/2024/08/open-bb-quotes-view.jpg)

效果有点出人意料，哈哈。

比较有趣的是，他们把命令设计成为 unix 路径的模式。所以，在执行完刚才的命令之后，我们可以输入以根目录为起点的其它命令，比如：

``` bash
/economy/gdp
```
我们就可以查询全球 GDP 数据。

## 使用 Python

我们通过 notebook 来演示一下它的使用。

```python
from openbb import obb

obb
```

这个 obb 对象，就是我们使用 openbb 的入口。当我们直接在单元格中输入 obb 时，就会提示我们它的属性和方法：

![](https://images.jieyu.ai/images/2024/08/help-openbb-jupyter.jpg)

在这里，openbb 保持了接口的一致性。我们看到的内容和在 cli 中看到的差不多。

现在，我们演示一些具体的功能。首先，通过名字来查找股票代码：

```python
from openbb import obb

obb.equity.search("JPMorgan", provider="nasdaq").to_df().head(3)
```

输出结果为：

![](https://images.jieyu.ai/images/2024/08/openbb-equity-search.jpg)

作为一个外国人，表示要搞清楚股票代码与数据提供商的关系，有点困难。不过，如果是每天都研究它，花点时间也是应该的。

我们从刚才的结果中，得知小摩（我常常记不清 JPMorgan 是大摩还是小摩。但实际上很好记。一个叫摩根士丹利，另一个叫摩根大通。大通是小摩）的股票代码是 AMJB（名字是 JPMorgan Chase 的那一个），于是我们想查一下它的历史行情数据。如果能顺利取得它的行情数据，我们的教程就可以结束了。

但是，当我们调用以下代码时：

```python
obb.equity.price.historical("AMJB")
```

出错了！提示 No result found.

## 使用免费、但需要注册的数据源

真实原因是 OpenBB 中，只有一个开箱即用的免费数据源 -- CBOE，但免费的 CBOE 数据源里没有这个股票。我们要选择另外一个数据源，比如 FMP。但是，需要先注册 FMP 账号（免费），再将 FMP 账号的 API key 添加到 OpenBB hub 中。

[FMP](https://site.financialmodelingprep.com/) 是 Financial Modeling Prep (FMP) 数据提供商，它提供免费（每限 250 次调用）和收费服务，数据涵盖非常广泛，包括了美国股市、加密货币、外汇和详细的公司财务数据。免费数据可以回调 5 年的历史数据。

!!! tip
    OpenBB 支持许多数据源。这些数据源往往都提供了一些免费使用次数。通过 OpenBB 的聚合，你就可以免费使用尽可能多的数据。

注册 FMP 只需要有一个邮箱即可，所以，如果 250 次不够用，看起来也很容易加量。注册完成后，就可以在 dashboard 中看到你的 API key:

![](https://images.jieyu.ai/images/2024/08/fmp-keys.jpg)

然后注册 Openbb Hub 账号，将这个 API key 添加到 OpenBB hub 中。

![](https://images.jieyu.ai/images/2024/08/openbb-hub.jpg)

现在，我们将数据源改为 FMP，再运行刚才的代码，就可以得到我们想要的结果了。

```python
obb.equity.price.historical("AMJB", provider="fmp").to_df().tail()
```

我们将得到如下结果：

![](https://images.jieyu.ai/images/2024/08/openbb-amjb-quotes.jpg)

换一支股票，apple 的，我们也是先通过 search 命令，拿到它的代码'AAPL'（我常常记作 APPL），再代入上面的代码，也能拿到数据了。

需要做一点基本面研究，比如，想知道 apple 历年的现金流数据？

```python
obb.equity.fundamental.cash("AAPL", provider='fmp').to_df().tail()
```

任何时候，交易日历、复权信息和成份股列表都是回测中不可或缺的（在 A 股，还必须有 ST 列表和涨跌停历史价格）。我们来看看如何获取股标列表和成份股列表：

```python
# 获取所有股票列表
all_companies = obb.equity.search("", provider="sec")

print(len(all_companies.results))
print(all_companies.to_df().head(10))

# 获取指数列表
indices = obb.index.available(provider="fmp").to_df()
print(indices)

# 获取指数成份股，DOWJONES, NASDAQ, SP500（无权限）
obb.index.constituents("dowjones", provider='fmp').to_df()
```

好了。尝试一个新的库很花时间。而且往往只有花过时间之后，你才能决定是否要继续使用它。如果最终不想使用它，那么前面的探索时间就白花了。

于是，我们就构建了一个计算环境，在其中安装了 OpenBB，并且注册了免费使用的 fmp 数据源，提供了示例 notebook，供大家练习 openbb。

这个环境是免费提供给大家使用的。如果你也想免安装立即试试 OpenBB，那么就进群看公告，领取登陆地址吧！
