---
title: "UV & Pydantic：重塑 2026 Python 工程化基石"
date: 2025-12-23
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251224163832.png
excerpt: "本文将探讨两项彻底改变 Python 开发体验的技术：Astral 的 UV —— 一个旨在替代 pip、poetry、pyenv 的全能包管理器；以及 Pydantic 2.0 —— 由 Rust 驱动的数据验证与解析库。它们的结合，构成了 2026 年高性能量化系统的标准地基。"
categories:
  - Tools
  - Quant
tags: [python, UV, Pydantic, Engineering]
addons:
  - slidev_themes/addons/slidev-addon-quantide-layout
  - slidev_themes/addons/slidev-addon-mouse-trail-pen
  - slidev_themes/addons/slidev-addon-array
  - slidev_themes/addons/slidev-addon-interactive-table
  - slidev_themes/addons/slidev-addon-card
aspectRatio: 3/4
layout: cover-random-img-portrait
---


量化人度过了一个喜悦的2025年。站在 2025 年的尾巴展望未来，我们发现量化交易的技术图谱正在经历一场前所未有的重构。岁末年初，正是厉兵秣马的时机，于是我们为你梳理了明年需要掌握的量化技术栈。

这个系列中，匡醍(Quantide)团队将梳理2026年十大量化技术趋势。这些技术有的是刚刚出现的新突破，有的则是成名已久，推成出新以适应变化中的需求。作为前言，我们略举几例，然后就转向今天的主题， 重塑 Python 工程化基石的两项技术 -- uv和 Pydantic 2.0。

## 1. 引言

在2025年，Polars发布了里程碑式的1.0版本。在明年，它很可能成为量化人的标配。而 Pandas 也不会坐视自己被 Polars 取代，全新的3.0版本将很快发布，它以 Apache Arrow 为底层数据模型（而不再是 Numpy），CoW成为默认行为，在字符串处理上将提升10倍以上的速度，综合来看也将提升一倍左右的速度。

Polars 与 Pandas 双雄逐🦌，带来的是更快、更好用的数据分析工具！

过去量化（包括人工智能领域）人必须依赖前端工程师才能生成一个美观和功能丰富的界面。如果不这样，他们就要借助 Streamlit 来构建界面。然而，发布于2024年，在今年急速崛起的 **FastHTML** 很可能成为新一轮游戏规则的制定者。它如此易用、如此强大，我想你非得了解它不可。

!!! tip
    FastHTML背后的男人是 Jeremy 教授。他开发了 FastAI, NBDev等一众明星工具，致力于让更多人能把 AI 使用起来。他和他的妻子有超过25年的 web 开发经验。在ASGI 和 HTMX技术成熟之后，他看到了前端编程领域的革命性机会。Jeremy一直是博主的偶像。如果你要快速学习 AI并致力于应用，他的 FastAI课程相当不错。


随着财经网站实施更加严厉的反爬措施，通过Akshare 来获得实时行情数据越来越困难。在2026年拿到低成本实时分钟线、日线的方法可能是通过 QMT 订阅全推tick 数据并重采样。

但要如何处理奔流而来的 tick 数据，并且**零延时**地重采样为分钟线、日线，以供后续分析？ 在Zillionare 2.0中我们不得不使用 lua 脚本来实现这个功能。但是，在今年5月发布的 Redis 8.0中，5000支个股的 tick 数据可以在**亚毫秒级**完成录入、重采样和发布，速度提升了百倍以上。

当然，我们也不会忘了人工智能在量化策略模型技术方面的重要进展。尽管我们不知道未来的路会通向多么遥远的远方，但已经可以确定，人工智能绝对可用于量化模型。

我会带你浏览 Agentic AI、强化学习和 Transformer 在时序模型方面的应用，以及，如何通过 SHAP 等类似技术，给 AI 黑盒模型做一个 X 光检验。当黑盒的行为得到了解释，我们就能信任和改进它。

...

还有很多新技术要介绍。然而，万丈高楼平地起。在这些炫酷的“上层建筑”之下，**Python 代码本身的健壮性与工程化效率**才是决定系统能否长期稳定运行的关键，是量化系统的隐形地基。

本文作为系列文章的第一篇，将带你深入了解 uv 和 Pydantic 2.0这两个看似基础、实则革命性的工具，看看它们如何为 2026 年的量化工程铺平道路。


## 2. UV， Poetry门口的野蛮人

长期以来，Python 的工具链是碎片化的：我们用 `pyenv` 管理版本，用 `venv` 创建环境，用 `pip` 安装包，用 `pip-tools` 锁定依赖。

2019年，Sébastien Eustace 发布了 Poetry 的第一个正式、稳定版本，从而把依赖管理、虚拟环境和产品打包构建统一起来。Poetry 的出现是划时代的，我们《Python 高效编程实践指南》一书中用一章的篇幅专门介绍了它，并且分享了它的依赖管理如何拯救了我的生活。

从那时起，在我构建的任何一个 Python 项目中，我总是使用 Poetry 来管理环境和依赖。

**UV 的出现结束了这一切。**

Uv 由Astral（Ruff 的开发者）出品，它使用 Rust 开发语言构建，一经问世，就以高效率和零依赖的特点，迅速成为 Poetry 最有力的竞争者。

Uv 在两个方面上超过了 Poetry。首先，它是操作系统级的工具，不依赖于 Python，即实现了『自举』。你可以在机器上没有 Python 的情况下，就安装任何一个 Python 版本并构建虚拟环境。这是 Poetry 和 venv 无法做到的。

相对于 Poetry，它的另一个优势是速度更快。uv在两个方向上提升了速度。一是它解析依赖的速度超过了 Poetry。UV 采用了全新的 PubGrub 算法优化版，配合 Rust 的高性能，能在几毫秒内解决复杂的依赖冲突。

当然，这也有一个前提，就是所有依赖的库都已下载并缓存在系统之中了。

与其它语言一样，Python的库也有一个中央存储库，称为 PyPI（Python Package Index）。但与其它语言不一样的是，由于历史的原因，这个中央存储库中只保存了 Python 库的发行物(artifacts)，而没有单独保存artifacts 的元数据（特别是依赖信息）。这些依赖信息只能在把 artifacts 完全下载并解包之后，才能分析得出来，遇到一些比较大的 Python 库，又要遍历许多版本以查找依赖关系时，这个过程就会取决于网络下载速度。在这种情况下，uv 的速度优势就不明显了。

第二个速度提升的诀窍是：**零拷贝**。uv 在安装依赖时，不会复制任何文件到虚拟环境中，而是直接创建硬链接（Linux/Windows）或 Copy-on-Write（macOS）。这意味着，你可以在多个项目之间共享同一个依赖，而不会占用额外的空间。同时，由于没有拷贝文件，安装速度当然也会提升很多。

!!! tip
    也有可能你完全不知道我们在讨论什么。如果是这样，你真的要去了解一下 Python 虚拟环境的概念，并且立即 用起来！它会 save your time, save your life.

当然，相比 Poetry，目前 uv 还不是尽善尽美。uv 比较新，它的功能目前还没有 Poetry 全，特别是它的构建后端能力还不如 Poetry 强。不过，既然我们在讨论2026年，也许新年一过，对C、C++或者 Rust扩展包的编译支持就完全解决了，从而提供类似于 Rust Cargo 一样的一致性体验。

让我们一起期待 Python 的 Cargo 时刻吧。


## 3. Pydantic 2.0：Agent 时代的“通用语”

如果说 UV 解决了“怎么跑”的问题，Pydantic 2.0 则解决了“跑什么”的问题。

量化开发里最昂贵的 bug，往往不是算法写错了，而是数据在不同来路的软件间“悄悄变形”：

- 行情网关发来的是 `dict`，字段今天叫 `last` 明天叫 `last_price`
- 成交回报里 `price` 偶尔是字符串，偶尔是浮点数
- 时间戳有时是秒，有时是毫秒；时区一会儿本地，一会儿 UTC

这类问题的共同点是：它们不会立刻报错，却会在回测统计、风控阈值、乃至实盘下单的最后一刻，把你推下悬崖。

量化系统天然是多模块协作：采集、存储、清洗、特征、信号、交易、风控、监控。模块边界越多，口头约定越不可靠。

为了防止这种问题的发生，我们用尽了各种方法：通过 typing 和 lint 进行静态类型检查，单元测试和各种运行时的 validation 来保证类型正确。

### 3.1. Pydantic 的数据校验

但 Pydantic 让validation 这件事变得简洁、优雅和规范。它提供了常见、规范的数据校验器，比如 gt, le，电子邮件地址，URL 等。这些规范化的校验既保证正确，又更加快速。

比如，当我们收到一个 tick 数据包时，我们期望它包含以下字段：

- `symbol`：股票代码，字符串
- `ts`：时间，datetime.datetime 类型
- `price`：最新价格，必须为正浮点数
- `volume`：成交量，必须为非负整数

但是，当我们从行情软件获取数据时，收到的 price 可能是字符串（比如 akshare），时间可能是一个 unix 时间戳，或者一个字符串，而且，这个 unix 时间戳可能是秒级的，也可能是毫秒级的。

通过 Pydantic，我们既可以拒绝错误的数据，也可以抢救虽然不规范、但实际上能用的数据（毕竟如果全世界错了，你能做的，也只能是选择加入！）

```python
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, field_validator

class Tick(BaseModel):
    symbol: str
    ts: datetime
    price: StrictFloat = Field(gt=0)
    volume: StrictInt = Field(ge=0)

    @field_validator('ts', mode='before')
    @classmethod
    def parse_ts(cls, v):
        if isinstance(v, int):
            if v > 10_000_000_000:
                return datetime.fromtimestamp(v / 1000)
            return datetime.fromtimestamp(v)
        return v
```

这段代码要求传入的数据中，volumen必须为非负数， price 必须为正数（大于零）。 如果传入的 ts 是整数，它还能自动识别是秒级还是毫秒级。

现在，**当 Tick 进入系统的那一刻，你就把秒/毫秒/时区/字段多余这类风险一次性清掉了。**

### 3.2. 别名和格式转换

假设你要做一个交易系统，实盘 API 使用的是迅投的 QMT。你需要把迅投返回过来的  XtOrder 保存到数据库中。显然，你可以直接使用 XtOrder 的所有字段作为表字段、以及要求客户端下单时，传递过来的Order也正是 XtOrder 模型。

这样没什么问题。但如果你突然想到，有一天你可能会换一家供应端，他们使用的 Order 定义就会有所不同，所以，你想自己定义一个更通用的 Order 模型，在系统中一直使用这个模型，直到定单提交到 xtquant (xtquant是 迅投的实盘 API sdk)，才将它转换为 XtOrder 模型。这就是 Pydantic 的另一个用武之地。

假设我们自己的 Order 模型定义如下：

```python
from enum import IntEnum

class BidType(IntEnum):
    FIXED = 1
    LATEST = 2

class Order:
    oid: str                     # 本系统的订单号
    asset: str                   # 股票代码
    bid_type: BidType            # 委托类型
    price: float                 # 订单价格
    volume: int                  # 订单数量
```

迅投的交易 API 接受的参数如下：

```python
order_stock(account, stock_code, order_volume, price_type, price, ...)
```

也就是它对应的报单类型是：

```python
class XtOrderType:
    stock_code: str
    price_type: int
    order_volume: int
    price: float
    ...
```

当我们报单时，需要将 asset转换为 stock_code, volume 转换为 order_volume, bid_type 转换为 price_type，并且两边的值还需要转换。

此外，xtquant 允许通过 order_remark 来传递一些信息，在订单状态改变，返回 XtOrder 时，也会包含这个信息。为了便于跟踪订单状态，我们就希望利用 order_remark 这个字段，把我们自己的 oid 传递给 xtquant。这样一来，当订单成功，xtquant 返回时，我们就可以找到自己系统中的订单。

这些都可以通过 Pydantic 来完成。

```python
from enum import IntEnum
from pydantic import BaseModel, ConfigDict, Field, field_validator

class BidType(IntEnum):
    FIXED = 1
    LATEST = 2

class Order(BaseModel):
    model_config = ConfigDict(populate_by_name=True)   # ①

    oid: str = Field( # ②
        default_factory=lambda: "qtide-" + uuid.uuid4().hex[:16], 
        alias="order_remark"
    )
    asset: str = Field(..., alias="stock_code")
    bid_type: BidType = Field(..., alias="price_type")
    price: float
    volume: int = Field(..., alias="order_volume")

class XtOrderType(BaseModel):    
    stock_code: str
    order_volume: int
    price_type: int
    price: float
    order_remark: str

    @field_validator("price_type", mode='before')
    @classmethod
    def _(cls, v): # ③
        mapping = {BidType.FIXED: 20, BidType.LATEST: 21}
        return mapping.get(v, v)
```

在注释①中，我们让 Order 构建时，也可以通过原字段名来填充。你很快将在下面的注释④中看到它的作用。

在注释②中，我们通过 default_factory 来设置默认值。这确保了，当我们创建 Order 实例时，如果没有显式传递 oid，它会自动生成一个唯一的字符串。

在注释③中，我们通过一个 before 类型的 field_validator 来把bid_type 字段的值重新映射到 Xtquant 支持的值。

在定义完成 Order, XtOrderType 之后，从我们系统的 Order 转换到 XtOrderType 的转换就变得易如反掌：

```python
order = Order(stock_code="000001.SZ", bid_type=BidType.FIXED, price=10, volume=101) # ④
order_dict = order.model_dump(by_alias=True) #⑤
xt_order = XtOrderType(**order_dict) # ⑥
```

在注释④中，构造 Order 时，我们既使用了原来的字段名，比如 bid_type, volume，也使用了别名（即在 XtOrderType 中的字段名），比如 stock_code。通过指定`populate_by_name=True`，Pydantic 就会同时允许这种*混杂*模式。

在注释⑤中，我们把 Order 实例转换为一个字典，这里传入参数 by_alias=True，表示转换后的字段名将使用别名，现在，我们已经得到了一个 xtquant 系统下的订单字典。

在注释⑥中，我们通过 `**order_dict` 把这个字典展开，构造一个 XtOrderType 实例。在这里会触发注释3中的字段校验，从而将 bid_type 中的 Fixed 转换为 20（假定这是 xtquant 中定价单的常数）。

通过使用 Pydantic，你是不是再也不用害怕不同系统之间的数据转换了？这里介绍的方法干净、整洁。更重要的是，它们都集中在同一个地方。

### 3.3. 从Model 到数据库表

如果你喜欢以 sqlalchemy 那种方式来管理数据库 schema，但并不想全盘使用 sqlalchemy（毕竟，把数据库从 sqlite 换到 oracle 这件事，可能一辈子都不会发生），那么你可以使用 sqlite_utils 和下面的方式，既简洁又可靠地处理数据schema。

我们会在后面专门出一期讲述在2026年，为什么你要使用 sqlite_utils。在这里，我们只简单介绍下跟 Pydantic 有关的部分 -- 创建数据库表。

我们已经定义了一个个数据模型。为什么不直接通过这些 Model，来创建数据库表呢？事实上 pydantic 已经考虑到了这一点，只需要很少的改动：

```python
class OrderModel(BaseModel):
    oid: str = Field(
        default_factory=lambda: "qtide-" + uuid.uuid4().hex[:16], 
        json_schema_extra={"pk": True, "index": True}
    )
    asset: str = Field(..., json_schema_extra={"pk": True, "index": True})                             
    tm: datetime.datetime
    price: Union[None, float]
    side: OrderSide = Field(..., 
                            json_schema_extra={"sql_type": "INTEGER"}, # ⑥
                            alias="order_type")
```

正如你所见，我们只增加了 json_schema_extra 参数，它可以指定索引、主键和数据类型。在注释⑥中，我们特别指定了  side 字段的 sql_type 为 INTEGER，这是因为它是一个 Enum 类型，无法被数据库理解。

然后，我们再定义一个辅助函数，从 model 中提取 schema，就可以用以创建表结构了：

```python
def get_sqlite_schema(model: type[BaseModel]):
    """将 Pydantic 模型转换为 sqlite-utils 兼容的列定义"""
    columns = {}
    indices = []
    pk = None

    for name, field in model.model_fields.items():
        extra = field.json_schema_extra or {}
        # 提取主键信息
        if extra.get("pk"):
            pk = name
            
        # 提取索引信息
        if extra.get("index"):
            indices.append(name)

        if "sql_type" in extra:
            columns[name] = extra["sql_type"]
            break

        # 如果用户没有通过 field 改写类型
        python_type = field.annotation
        sql_type = "TEXT"

        if isinstance(python_type, type) and issubclass(python_type, enum.Enum): # ⑦
            sql_type = "INTEGER" if issubclass(python_type, IntEnum) else "TEXT"

        # 检查是否为联合类型（Union 或 A | B 语法）
        elif hasattr(python_type, "__origin__") and python_type.__origin__ is Union:
            non_none_types = [arg for arg in python_type.__args__ if arg is not type(None)]
            if non_none_types:
                sql_type = non_none_types[0]

        # 对于 A | B 语法（Python 3.10+），是 types.UnionType
        elif isinstance(python_type, types.UnionType):
            non_none_types = [arg for arg in python_type.__args__ if arg is not type(None)]
            if non_none_types:
                sql_type = non_none_types[0]

        
        columns[name] = sql_type
            
    return columns, pk, indices
```

注意注释⑦处的代码。有了这一行声明，实际上我们不需要特别为 side 字段再声明 sql_type 了。因为 OrderSide 是一个 IntEnum，因此会在这里被自动转换为 int。这样一来，我们的代码可以更简洁，基本上只需要指定主键和索引即可。

我对 sqlalchemy 是又爱又狠。我很喜欢以纯 Python 的方式来与数据库交互，但是它确实有点臃肿，会引起性能下降，也有一定的学习曲线。如果你跟我有同样的想法，也许可以考虑使用 Pydantic、sqlite-utils以及这里的简单封装来构建你的数据库应用。

再一次说明，我们将在后面的文章中介绍sqlite-utils。

如果说在完成《Python高效编程实践指南》一书后，我留下什么遗憾的话，就是在书中没有给 pydantic 留下一席之地 -- 数据校验本应该与 typing, lint，单元测试一样，在提升软件质量中占有同样重要的地位。

不过，等到2025年末再来介绍 Pydantic 2也许更好，因为它现在使用 rust 开发，并进行了重要的改进和重构。如果我在那本书出版之前介绍 Pydantic，必然会引入许多现在被废弃的功能。
