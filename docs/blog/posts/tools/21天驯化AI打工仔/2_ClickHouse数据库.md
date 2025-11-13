---
title: 21天驯化AI打工仔 - 开发量化交易系统
slug: Taming-the-AI-Worker-in-21-Days-2
date: 2025-05-11
category: tools
motto: You only live once, but if you do it right, once is enough
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png
tags: 
    - tools
    - programming
---

今天是第二天，我计划实现如下任务：
1. 安装 ClickHouse 和 DBeaver
2. 创建 ClickHouse 数据表
3. 修改 Redis 消息队列代码以支持 ClickHouse 存储

我唤醒了 007，它今天是要陪我一起战斗代码的。

---

## 1. 安装 ClickHouse 和 DBeaver
我使用的是 mac 系统，电脑里还没有安装 ClickHouse 和 DBeaver，所以我首先需要安装它们。

### 1.1. 安装 ClickHouse
> **我：007！给我一个ClickHouse mac 系统的安装教程。**
>
> **007：收到！以下是您需要的 ClickHouse 的安装教程！**

ClickHouse 是一个用于联机分析（OLAP）的列式数据库管理系统（DBMS），最早由俄罗斯 IT 公司 Yandex 为 Yandex.Metrica 网络分析服务开发，于 2016 年基于宽松式的 Apache2.0 许可证发布。

<!--
!!! note ClickHouse 的优势
    - **高性能查询**：采用列式存储和多线程并行计算，在处理 TB 级别大数据量时，能实现秒级查询响应，高并发、复杂的 OLAP 查询处理能力出色。
    - **实时数据处理**：支持数据的实时插入和查询，可对实时数据进行分析与监控，适用于实时处理和查询大量数据的场景。
    - **数据压缩高效**：提供多种压缩算法，能在不影响查询速度的前提下，大幅降低数据存储空间需求，节省存储成本，提高数据读取效率。
    - **可扩展性强**：分布式架构，可通过添加节点实现计算和存储能力的水平扩展，无论是单台服务器数据处理，还是跨多台机器的分布式数据处理，都能高效运行。
    - **丰富的 SQL 功能**：支持标准 SQL 查询，有丰富的函数、窗口函数和多种数据类型，方便数据分析人员和开发者上手。
    - **并发读写性能好**：支持 MVCC 机制，数据更新和插入时，查询不会被锁住，保证系统高性能。
    - **分区与分片功能**：允许对数据进行水平分区和分片，将数据划分到不同节点或磁盘存储，提升查询效率和并行处理能力。
-->

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_01.png)

于是，我使唤 007 给我一个 Mac 系统安装 ClickHouse 的教程，它对此表示非常容易，于是，我按照下面的步骤进行安装。

1. 下载 ClickHouse：前往 [ClickHouse 官方网站](https://clickhouse.com/docs/install) 下载适用于 Mac 系统的安装包。也可以使用 `curl` 实现快速安装：
    `curl https://clickhouse.com/ | sh`
2. 可以通过 Homebrew 安装 ClickHouse：
    `brew install clickhouse`
3. 启动服务器：打开终端，导航到解压后的目录，执行 `./clickhouse - server` 命令启动 ClickHouse 服务器。若要在后台启动服务器，可使用 `./clickhouse - server --daemon` 命令。服务器启动后，会监听默认端口 9000。
4. 启动客户端：打开终端，导航到解压后的目录，执行 `./clickhouse - client` 命令启动 ClickHouse 客户端。若要在后台启动客户端，可使用 `./clickhouse - client --daemon` 命令。客户端启动后，你可以使用 SQL 语句与 ClickHouse 进行交互。

### 1.2. 安装 DBeaver
为了方便管理 ClickHouse 数据库，我计划安装 DBeaver。

> **我：007！再给我一个DBeaver mac 系统的安装教程。**
>
> **007：收到！以下是您需要的 DBeaver 的安装教程！**

DBeaver 是一个通用数据库管理工具和 SQL 客户端，支持多种数据库，其中包括 ClickHouse。通过 DBeaver，用户可以使用 JDBC 驱动与 ClickHouse 建立连接，从而实现对 ClickHouse 数据库的访问和操作。用户只需在 DBeaver 中配置 ClickHouse 的连接参数，如主机地址、端口、用户名和密码等，就可以方便地连接到 ClickHouse 数据库，进行各种数据库操作。

1. 安装 [DBeaver](https://dbeaver.io/) 并连接 ClickHouse
2. 下载并安装 DBeaver。
3. 打开 DBeaver，点击 *Database > New Database Connection*。
4. 搜索并选择 ClickHouse，填写连接信息（默认端口为 9000）。
5. 测试连接，确保成功。

## 2. 创建 ClickHouse 数据表

> **我：007！给我一个 ClickHouse 表，用于存储 OHLC 数据。**
>
> **007：收到！在 DBeaver 中，执行以下 SQL 创建存储 OHLC 数据的表。**

```sql
CREATE TABLE ohlc_data (
    ts_code String,
    trade_date Date,
    open Float32,
    high Float32,
    low Float32,
    close Float32,
    vol Float32
) ENGINE = MergeTree()
ORDER BY (ts_code, trade_date);
```

按照 007 的指示，我创建了一个名为 `ohlc_data` 的表，用于存储 OHLC 数据。

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_03.png)

## 3. 修改 Redis 消息队列代码以支持 ClickHouse 存储

我现在安装好了所需要的数据库软件，在第一天到基础上，我需要更新 `data_consumer.py` 代码，将数据存储到 ClickHouse 数据库。007 听令！

007 说这个任务它承包了，于是给了我第二版的`data_consumer.py` 代码。
```python
import redis
import json
from clickhouse_driver import Client

# 配置参数
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_QUEUE_NAME = "tushare_data_queue"

CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DB = "default"

# 初始化 Redis 和 ClickHouse 客户端
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
clickhouse_client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DB)

def insert_to_clickhouse(data):
    """将数据插入到 ClickHouse"""
    query = """
    INSERT INTO ohlc_data (ts_code, trade_date, open, high, low, close, vol)
    VALUES
    """
    values = [
        (
            record["ts_code"],
            record["trade_date"],
            record["open"],
            record["high"],
            record["low"],
            record["close"],
            record["vol"]
        )
        for record in data
    ]
    clickhouse_client.execute(query, values)

def consume_data():
    """数据消费主函数"""
    print("启动数据消费者，等待队列数据...")
    while True:
        try:
            # 阻塞式获取队列数据
            _, json_data = redis_client.brpop(REDIS_QUEUE_NAME, timeout=30)
            if json_data:
                data_package = json.loads(json_data)
                ohlc_data = data_package["ohlc_data"]
                insert_to_clickhouse(ohlc_data)
                print(f"成功插入数据: {len(ohlc_data)} 条")
        except Exception as e:
            print(f"数据处理异常: {str(e)}")
            continue

if __name__ == "__main__":
    consume_data()
```

我尝试运行 `data_consumer.py`，但程序报错如下：
```
(course) quantide@Mac note % python data_consumer.py 
启动数据消费者，等待队列数据... 
数据处理异常: 'str' object has no attribute 'year'
数据处理异常: 'str' object has no attribute 'year'
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_04.png)

007（委屈但诚恳）：根据错误信息 数据处理异常: `'str' object has no attribute 'year'`，问题可能出在 `trade_date` 字段的处理上。`trade_date` 是一个字符串（例如 `"20230101"`），而 ClickHouse 需要 `Date` 类型的数据。在插入数据时，ClickHouse 的 `Date` 类型需要一个有效的日期格式（如 `YYYY-MM-DD`）。

我们需要将 `trade_date` 从字符串格式转换为 `YYYY-MM-DD` 格式：
```python
from datetime import datetime

# ...  源代码见上一章节。

def insert_to_clickhouse(data):
    """将数据插入到 ClickHouse"""
    query = """
    INSERT INTO ohlc_data (ts_code, trade_date, open, high, low, close, vol)
    VALUES
    """
    values = [
        (
            record["ts_code"],
            # 将 trade_date 字符串转换为日期类型
            datetime.strptime(record["trade_date"], "%Y%m%d").date(),
            record["open"],
            record["high"],
            record["low"],
            record["close"],
            record["vol"]
        )
        for record in data
    ]
    clickhouse_client.execute(query, values)
```

在此基础上，我希望让 `data_consumer.py` 在将 `Redis` 里的数据传送到 ClickHouse 之后停止运行，可在 `Redis` 队列没有数据时，终止循环。

```python
# ...  源代码见上一章节。

def consume_data():
    """数据消费主函数"""
    print("启动数据消费者，等待队列数据...")
    while True:
        try:
            # 阻塞式获取队列数据
            result = redis_client.brpop(REDIS_QUEUE_NAME, timeout=1)
            if result is None:
                # 如果没有获取到数据，说明队列为空，退出循环
                print("Redis 队列为空，停止消费数据。")
                break
            _, json_data = result
            data_package = json.loads(json_data)
            ohlc_data = data_package["ohlc_data"]
            insert_to_clickhouse(ohlc_data)
            print(f"成功插入数据: {len(ohlc_data)} 条")
        except Exception as e:
            print(f"数据处理异常: {str(e)}")
            continue
```

007 在修改后，还“贴心”地给出了代码解释：
- **brpop 函数的 timeout 参数**：把 brpop 函数的 timeout 参数设定为 1 秒，这意味着如果在 1 秒内没有从队列中获取到数据，brpop 函数就会返回 None。
- **队列为空的判断**：在 while 循环里，检查 brpop 函数的返回值。若返回值为 None，就表明队列是空的，此时使用 break 语句退出循环，从而停止程序的运行。

这样，当 Redis 队列中的数据全部被处理完之后，程序就会自动停止。

经过上述修改，`data_consumer.py` 现在可以成功将数据从 Redis 队列传送到 ClickHouse 数据库。

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_05.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_06.png)


