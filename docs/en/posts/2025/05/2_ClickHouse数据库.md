---
title: "Day 2: Deploying ClickHouse for Quant Data Storage"
date: 2025-05-11
slug: en/posts/tools/21天驯化AI打工仔/2_ClickHouse数据库
tags: [ClickHouse, Quantitative Trading, Data Engineering, Python]
excerpt: "Day 2 of building a quantitative trading system: installing ClickHouse and DBeaver, creating OHLC tables, and fixing Redis-to-ClickHouse data ingestion errors."
lang: en
translation_of: posts/tools/21天驯化AI打工仔/2_ClickHouse数据库
auto_translated: true
source_sha: fe376ec20a4a11eef1aebc89f86a86bb6fbf24de
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png"
---

Today is Day 2. My plan is to execute the following tasks:
1. Install ClickHouse and DBeaver
2. Create ClickHouse data tables
3. Modify the Redis message queue code to support ClickHouse storage

I’ve awakened "007" (my AI assistant) to help me tackle the code today.

---

## 1. Install ClickHouse and DBeaver
I’m using macOS, and neither ClickHouse nor DBeaver is currently installed. Therefore, my first step is to install both.

### 1.1. Install ClickHouse
> **Me: 007! Give me a tutorial for installing ClickHouse on macOS.**
>
> **007: Received! Here is the ClickHouse installation tutorial you requested!**

ClickHouse is a column-oriented database management system (DBMS) for online analytical processing (OLAP). It was originally developed by the Russian IT company Yandex for its Yandex.Metrica web analytics service and released in 2016 under the permissive Apache 2.0 license.

<!--
!!! note Advantages of ClickHouse
    - **High-Performance Queries**: Utilizes columnar storage and multi-threaded parallel computing. It delivers second-level query responses for TB-scale big data, excelling in high-concurrency and complex OLAP queries.
    - **Real-Time Data Processing**: Supports real-time data insertion and querying, enabling analysis and monitoring of live data, suitable for scenarios requiring real-time processing of large data volumes.
    - **Efficient Data Compression**: Offers various compression algorithms that significantly reduce storage requirements without compromising query speed, lowering storage costs and improving read efficiency.
    - **Strong Scalability**: Features a distributed architecture that allows horizontal scaling of compute and storage by adding nodes. It runs efficiently whether processing data on a single server or across multiple machines.
    - **Rich SQL Functionality**: Supports standard SQL queries with a rich set of functions, window functions, and data types, making it easy for data analysts and developers to get started.
    - **High Concurrency Read/Write Performance**: Supports MVCC (Multi-Version Concurrency Control), ensuring that queries are not blocked during data updates or insertions, maintaining high system performance.
    - **Partitioning and Sharding**: Allows horizontal partitioning and sharding of data, distributing it across different nodes or disks to improve query efficiency and parallel processing capabilities.
-->

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_01.png)

I then asked 007 for a macOS installation tutorial for ClickHouse. It deemed the process straightforward, so I followed these steps:

1. **Download ClickHouse**: Visit the [ClickHouse official website](https://clickhouse.com/docs/install) to download the macOS installer. Alternatively, use `curl` for a quick installation:
    `curl https://clickhouse.com/ | sh`
2. **Install via Homebrew**:
    `brew install clickhouse`
3. **Start the Server**: Open the terminal, navigate to the extracted directory, and run `./clickhouse-server` to start the ClickHouse server. To run it in the background, use `./clickhouse-server --daemon`. Once started, the server listens on the default port 9000.
4. **Start the Client**: Open the terminal, navigate to the extracted directory, and run `./clickhouse-client` to start the ClickHouse client. To run it in the background, use `./clickhouse-client --daemon`. Once started, you can interact with ClickHouse using SQL statements.

### 1.2. Install DBeaver
To manage the ClickHouse database more efficiently, I plan to install DBeaver.

> **Me: 007! Give me a tutorial for installing DBeaver on macOS.**
>
> **007: Received! Here is the DBeaver installation tutorial you requested!**

DBeaver is a universal database management tool and SQL client that supports multiple databases, including ClickHouse. Through DBeaver, users can connect to ClickHouse using JDBC drivers to access and manipulate the database. By configuring connection parameters in DBeaver—such as host address, port, username, and password—you can easily connect to the ClickHouse database and perform various operations.

1. Install [DBeaver](https://dbeaver.io/) and connect to ClickHouse.
2. Download and install DBeaver.
3. Open DBeaver and click *Database > New Database Connection*.
4. Search for and select ClickHouse, then enter the connection details (default port is 9000).
5. Test the connection to ensure it succeeds.

## 2. Create ClickHouse Data Table

> **Me: 007! Give me a ClickHouse table schema to store OHLC data.**
>
> **007: Received! In DBeaver, execute the following SQL to create a table for storing OHLC data.**

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

Following 007’s instructions, I created a table named `ohlc_data` to store OHLC (Open, High, Low, Close) data.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_03.png)

## 3. Modify Redis Message Queue Code to Support ClickHouse Storage

With the required database software installed, I need to update `data_consumer.py` from Day 1 to store data in ClickHouse. 007, take command!

007 took on this task and provided me with the second version of the `data_consumer.py` code:

```python
import redis
import json
from clickhouse_driver import Client

# Configuration parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_QUEUE_NAME = "tushare_data_queue"

CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DB = "default"

# Initialize Redis and ClickHouse clients
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
clickhouse_client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DB)

def insert_to_clickhouse(data):
    """Insert data into ClickHouse"""
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
    """Main data consumption function"""
    print("Starting data consumer, waiting for queue data...")
    while True:
        try:
            # Blocking retrieval of queue data
            _, json_data = redis_client.brpop(REDIS_QUEUE_NAME, timeout=30)
            if json_data:
                data_package = json.loads(json_data)
                ohlc_data = data_package["ohlc_data"]
                insert_to_clickhouse(ohlc_data)
                print(f"Successfully inserted data: {len(ohlc_data)} records")
        except Exception as e:
            print(f"Data processing error: {str(e)}")
            continue

if __name__ == "__main__":
    consume_data()
```

I attempted to run `data_consumer.py`, but the program threw the following error:

```
(course) quantide@Mac note % python data_consumer.py 
Starting data consumer, waiting for queue data... 
Data processing error: 'str' object has no attribute 'year'
Data processing error: 'str' object has no attribute 'year'
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_04.png)

007 (looking aggrieved but sincere): Based on the error message `Data processing error: 'str' object has no attribute 'year'`, the issue likely lies in the handling of the `trade_date` field. `trade_date` is a string (e.g., `"20230101"`), but ClickHouse expects a `Date` type. When inserting data, ClickHouse’s `Date` type requires a valid date format (e.g., `YYYY-MM-DD`).

We need to convert `trade_date` from a string format to `YYYY-MM-DD`:

```python
from datetime import datetime

# ... Source code from previous section.

def insert_to_clickhouse(data):
    """Insert data into ClickHouse"""
    query = """
    INSERT INTO ohlc_data (ts_code, trade_date, open, high, low, close, vol)
    VALUES
    """
    values = [
        (
            record["ts_code"],
            # Convert trade_date string to date type
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

Building on this, I want `data_consumer.py` to stop running after transferring data from `Redis` to ClickHouse. Specifically, it should terminate the loop when the `Redis` queue is empty.

```python
# ... Source code from previous section.

def consume_data():
    """Main data consumption function"""
    print("Starting data consumer, waiting for queue data...")
    while True:
        try:
            # Blocking retrieval of queue data
            result = redis_client.brpop(REDIS_QUEUE_NAME, timeout=1)
            if result is None:
                # If no data is retrieved, the queue is empty; exit the loop
                print("Redis queue is empty, stopping data consumption.")
                break
            _, json_data = result
            data_package = json.loads(json_data)
            ohlc_data = data_package["ohlc_data"]
            insert_to_clickhouse(ohlc_data)
            print(f"Successfully inserted data: {len(ohlc_data)} records")
        except Exception as e:
            print(f"Data processing error: {str(e)}")
            continue
```

After the modification, 007 "thoughtfully" provided an explanation of the code:
- **`brpop` function `timeout` parameter**: Setting the `timeout` parameter of the `brpop` function to 1 second means that if no data is retrieved from the queue within 1 second, the `brpop` function returns `None`.
- **Empty queue check**: Inside the `while` loop, we check the return value of the `brpop` function. If it returns `None`, indicating the queue is empty, we use the `break` statement to exit the loop, thereby stopping the program.

This way, the program automatically stops once all data in the Redis queue has been processed.

After the above modifications, `data_consumer.py` can now successfully transfer data from the Redis queue to the ClickHouse database.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_05.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/04/2_06.png)
