---
title: "UV & Pydantic 2.0: The 2026 Python Engineering Foundation for Quant Systems"
date: 2025-12-23
slug: en/posts/tools/2026十大量化技术/uv-pydantic
tags: [Python Engineering, Quantitative Development, Data Validation, Dependency Management]
excerpt: "Astral’s UV and Pydantic 2.0 redefine Python engineering for 2026. UV accelerates dependency management with Rust, while Pydantic ensures robust data validation, forming the critical foundation for high-performance quantitative systems."
lang: en
translation_of: posts/tools/2026十大量化技术/uv-pydantic
auto_translated: true
source_sha: 4e6fb1280d32964ae88e75efb46280946694a79f
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251224163832.png"
---

Quantitative professionals have enjoyed a triumphant 2025. As we stand on the precipice of 2026, we observe an unprecedented restructuring of the quantitative trading technology landscape. The turn of the year is the ideal time to sharpen our tools, which is why we have curated the quantitative tech stack you need to master next year.

In this series, the Quantide team will outline the top ten quantitative technology trends for 2026. Some of these are emerging breakthroughs, while others are mature technologies refined to meet evolving demands. As a preface, we briefly mention a few examples before turning to today’s topic: two technologies reshaping the engineering foundation of Python—uv and Pydantic 2.0.

## 1. Introduction

In 2025, Polars released its milestone 1.0 version. Next year, it is likely to become the standard tool for quantitative researchers. Pandas, however, will not sit idly by while being replaced by Polars. Its new 3.0 version will be released soon, featuring Apache Arrow as its underlying data model (replacing NumPy), Copy-on-Write (CoW) as the default behavior, and string processing speeds improved by more than tenfold. Overall, performance will roughly double.

The rivalry between Polars and Pandas delivers faster, more user-friendly data analysis tools!

In the past, quantitative researchers (including those in AI) had to rely on frontend engineers to build beautiful, feature-rich interfaces. Without them, they had to resort to Streamlit. However, **FastHTML**, released in 2024 and rapidly gaining traction this year, is likely to become the new rule-maker. It is so easy to use and so powerful that you simply must understand it.

!!! tip
    The mind behind FastHTML is Professor Jeremy. He developed star tools like FastAI and NBDev, dedicated to making AI accessible to more people. He and his wife have over 25 years of web development experience. With ASGI and HTMX technologies maturing, he saw a revolutionary opportunity in frontend programming. Jeremy has always been an idol to this blog’s author. If you want to quickly learn AI and focus on applications, his FastAI course is excellent.

As financial websites implement stricter anti-scraping measures, obtaining real-time market data via AkShare is becoming increasingly difficult. In 2026, the low-cost method to obtain real-time minute and daily bars may be subscribing to full-tick data via QMT and resampling it.

But how do you process this torrent of tick data and **zero-latency** resample it into minute and daily bars for subsequent analysis? In Zillionare 2.0, we had to use Lua scripts to achieve this. However, with the May 2025 release of Redis 8.0, tick data for 5,000 stocks can be ingested, resampled, and published in **sub-millisecond** time, a speed increase of over 100 times.

Of course, we won’t forget the significant advancements in AI for quantitative strategy models. While we don’t know how far the road ahead leads, it is certain that AI will be applicable to quantitative models.

I will guide you through the applications of Agentic AI, reinforcement learning, and Transformers in time-series models, and how to perform an "X-ray" inspection of AI black-box models using techniques like SHAP. Once the black box’s behavior is explained, we can trust and improve it.

...

There are many more new technologies to introduce. However, tall buildings rise from the ground. Beneath these flashy "superstructures," the **robustness and engineering efficiency of the Python code itself** are the keys to determining whether a system can run stably over the long term—the invisible foundation of quantitative systems.

As the first article in this series, this piece will take you deep into uv and Pydantic 2.0—two seemingly basic yet revolutionary tools—to see how they pave the way for quantitative engineering in 2026.

## 2. UV: The Barbarian at Poetry’s Gate

For a long time, Python’s toolchain was fragmented: we used `pyenv` to manage versions, `venv` to create environments, `pip` to install packages, and `pip-tools` to lock dependencies.

In 2019, Sébastien Eustace released the first official, stable version of Poetry, unifying dependency management, virtual environments, and package building. Poetry’s emergence was epoch-making. In our book *Python High-Performance Programming Practices*, we dedicated a chapter to it, sharing how its dependency management saved my life.

Since then, in every Python project I’ve built, I have always used Poetry to manage environments and dependencies.

**UV’s arrival ended all that.**

Uv is produced by Astral (the developers of Ruff) and built using Rust. Upon its release, it quickly became Poetry’s most formidable competitor due to its high efficiency and zero-dependency nature.

Uv surpasses Poetry in two aspects. First, it is an OS-level tool that does not depend on Python, achieving "self-bootstrapping." You can install any Python version and build a virtual environment even if no Python is installed on the machine. This is something Poetry and venv cannot do.

Secondly, it is faster. uv improves speed in two directions. First, its dependency resolution speed exceeds Poetry’s. uv adopts an optimized version of the PubGrub algorithm, combined with Rust’s high performance, to resolve complex dependency conflicts in milliseconds.

Of course, this assumes that all dependent libraries have been downloaded and cached in the system.

Like other languages, Python has a central repository for libraries, known as PyPI (Python Package Index). However, unlike other languages, due to historical reasons, this central repository only stores Python library artifacts, not the metadata of the artifacts (especially dependency information) separately. This dependency information can only be analyzed after the artifacts are fully downloaded and unpacked. When dealing with large Python libraries and traversing many versions to find dependencies, this process depends on network download speeds. In such cases, uv’s speed advantage is less pronounced.

The second key to its speed is **zero-copy**. When installing dependencies, uv does not copy any files into the virtual environment; instead, it creates hard links (Linux/Windows) or Copy-on-Write (macOS). This means you can share the same dependency across multiple projects without occupying extra space. Moreover, since no files are copied, the installation speed is naturally significantly improved.

!!! tip
    You might not know what we are talking about. If so, you really need to understand the concept of Python virtual environments and start using them immediately! It will save your time and save your life.

Of course, compared to Poetry, uv is not yet perfect. uv is newer, and its features are currently not as comprehensive as Poetry’s, especially its build backend capabilities, which are weaker than Poetry’s. However, since we are discussing 2026, perhaps after the New Year, support for compiling C, C++, or Rust extension packages will be fully resolved, providing a consistent experience similar to Rust’s Cargo.

Let us look forward to Python’s Cargo moment.

## 3. Pydantic 2.0: The "Lingua Franca" of the Agent Era

If UV solves the "how to run" problem, Pydantic 2.0 solves the "what to run" problem.

The most expensive bugs in quantitative development are often not wrong algorithms, but data "quietly morphing" across different software sources:

- Market data gateways send `dict`s, where fields are named `last` today and `last_price` tomorrow.
- Trade reports have `price` occasionally as a string and occasionally as a float.
- Timestamps are sometimes in seconds, sometimes in milliseconds; time zones are sometimes local, sometimes UTC.

The commonality of these issues is that they do not immediately throw errors but will push you off a cliff during backtest statistics, risk control thresholds, or the final moment of live trading.

Quantitative systems are inherently multi-module collaborations: collection, storage, cleaning, features, signals, trading, risk control, and monitoring. The more module boundaries there are, the less reliable verbal agreements become.

To prevent such issues, we have exhausted various methods: static type checking via typing and linting, unit tests, and various runtime validations to ensure type correctness.

### 3.1. Pydantic’s Data Validation

But Pydantic makes validation concise, elegant, and standardized. It provides common, standardized data validators, such as `gt`, `le`, email addresses, URLs, etc. These standardized validations ensure correctness and are faster.

For example, when we receive a tick data packet, we expect it to contain the following fields:

- `symbol`: Stock code, string
- `ts`: Time, `datetime.datetime` type
- `price`: Latest price, must be a positive float
- `volume`: Volume, must be a non-negative integer

However, when we obtain data from market software, the received `price` might be a string (e.g., from AkShare), and the time might be a Unix timestamp or a string. Moreover, this Unix timestamp could be in seconds or milliseconds.

Through Pydantic, we can not only reject erroneous data but also salvage data that is non-standard but practically usable (after all, if the whole world is wrong, your only option is to join them!).

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

This code requires that the input data’s `volume` be non-negative and `price` be positive (greater than zero). If the input `ts` is an integer, it can automatically identify whether it is in seconds or milliseconds.

Now, **the moment Tick data enters the system, you have eliminated risks such as seconds/milliseconds, time zones, and extra fields all at once.**

### 3.2. Aliases and Format Conversion

Suppose you are building a trading system where the live trading API uses Xuntou’s QMT. You need to save the returned `XtOrder` to the database. Obviously, you could directly use all fields of `XtOrder` as table fields and require the client to pass an `Order` that is exactly the `XtOrder` model when placing orders.

This is not a problem. But what if you suddenly think that one day you might switch to a different provider, whose `Order` definition would be different? So, you want to define your own more generic `Order` model and use it throughout the system until the order is submitted to `xtquant` (Xuntou’s live trading API SDK), where it is converted to the `XtOrder` model. This is another application of Pydantic.

Assume our own `Order` model is defined as follows:

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

The parameters accepted by Xuntou’s trading API are as follows:

```python
order_stock(account, stock_code, order_volume, price_type, price, ...)
```

Which corresponds to the order type:

```python
class XtOrderType:
    stock_code: str
    price_type: int
    order_volume: int
    price: float
    ...
```

When placing an order, we need to convert `asset` to `stock_code`, `volume` to `order_volume`, and `bid_type` to `price_type`, and the values on both sides need to be converted.

Additionally, `xtquant` allows passing some information via `order_remark`. When the order status changes and `XtOrder` is returned, this information will also be included. To facilitate tracking order status, we want to use the `order_remark` field to pass our own `oid` to `xtquant`. This way, when the order succeeds and `xtquant` returns, we can find the order in our system.

All of this can be accomplished through Pydantic.

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

In comment ①, we allow the `Order` to be constructed using the original field names. You will soon see its utility in comment ④ below.

In comment ②, we set default values via `default_factory`. This ensures that when we create an `Order` instance, if `oid` is not explicitly passed, it automatically generates a unique string.

In comment ③, we use a `before` type `field_validator` to remap the value of the `bid_type` field to values supported by `xtquant`.

After defining `Order` and `XtOrderType`, converting from our system’s `Order` to `XtOrderType` becomes effortless:

```python
order = Order(stock_code="000001.SZ", bid_type=BidType.FIXED, price=10, volume=101) # ④
order_dict = order.model_dump(by_alias=True) #⑤
xt_order = XtOrderType(**order_dict) # ⑥
```

In comment ④, when constructing `Order`, we use both the original field names, such as `bid_type` and `volume`, and the aliases (i.e., the field names in `XtOrderType`), such as `stock_code`. By specifying `populate_by_name=True`, Pydantic allows this *mixed* mode.

In comment ⑤, we convert the `Order` instance to a dictionary. Here, we pass the argument `by_alias=True`, indicating that the converted field names will use aliases. Now, we have obtained an order dictionary for the `xtquant` system.

In comment ⑥, we expand this dictionary using `**order_dict` to construct an `XtOrderType` instance. This triggers the field validation in comment 3, thereby converting `Fixed` in `bid_type` to `20` (assuming this is the constant for fixed-price orders in `xtquant`).

By using Pydantic, do you no longer need to fear data conversion between different systems? The methods introduced here are clean and tidy. More importantly, they are all concentrated in one place.

### 3.3. From Model to Database Table

If you prefer managing database schemas in a SQLAlchemy-like manner but do not want to use SQLAlchemy entirely (after all, switching the database from SQLite to Oracle may never happen in your lifetime), you can use `sqlite_utils` and the following approach to handle data schemas concisely and reliably.

We will dedicate a future episode to discussing why you should use `sqlite_utils` in 2026. Here, we only briefly introduce the part related to Pydantic—creating database tables.

We have already defined various data models. Why not directly create database tables through these Models? In fact, Pydantic has considered this, requiring only minimal changes:

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

As you can see, we only added the `json_schema_extra` parameter, which can specify indexes, primary keys, and data types. In comment ⑥, we specifically specified the `sql_type` for the `side` field as `INTEGER`, because it is an Enum type that the database cannot understand directly.

Then, we define a helper function to extract the schema from the model, which can be used to create table structures:

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

Note the code at comment ⑦. With this declaration, we actually do not need to specially declare the `sql_type` for the `side` field. Because `OrderSide` is an `IntEnum`, it will be automatically converted to `int` here. This way, our code can be more concise, essentially requiring only the specification of primary keys and indexes.

I have a love-hate relationship with SQLAlchemy. I like interacting with databases in pure Python, but it is indeed somewhat bloated, causes performance degradation, and has a certain learning curve. If you share my thoughts, you might consider using Pydantic, `sqlite-utils`, and the simple encapsulation here to build your database applications.

Once again, we will introduce `sqlite-utils` in subsequent articles.

If there is one regret I have left after completing the book *Python High-Performance Programming Practices*, it is that Pydantic was not given a place in the book—data validation should occupy the same important position as typing, linting, and unit tests in improving software quality.

However, it may be better to introduce Pydantic 2 at the end of 2025, as it is now developed in Rust and has undergone significant improvements and refactoring. If I had introduced Pydantic before the publication of that book, I would inevitably have introduced many features that are now deprecated.
