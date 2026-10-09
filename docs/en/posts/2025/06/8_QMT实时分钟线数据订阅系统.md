---
title: "Build a 10x Faster QMT Real-Time Data System with Multi-Client Support"
date: 2025-06-15
slug: en/posts/tools/21天驯化AI打工仔/8_QMT实时分钟线数据订阅系统
tags: [Quantitative Trading, Real-Time Data, QMT, System Architecture]
excerpt: "Transform a fragile prototype into a high-performance, 10x faster real-time minute-bar data subscription system using QMT’s whole-market API and Redis Streams for robust multi-client consumption."
lang: en
translation_of: posts/tools/21天驯化AI打工仔/8_QMT实时分钟线数据订阅系统
auto_translated: true
source_sha: 5319385fd03b2ed214410e40c5c1a3337a9feb02
---

> When data floods in like a tide, how do you keep your system rock-solid? This article takes you deep into the world of QMT real-time data subscriptions, witnessing how the "007 Assistant" upgrades a simple data-fetching script into a high-performance system with 10x processing capacity!

"007, our daily data scheduled-fetching system is stable, but I need finer-grained data now—minute-bar data." I said, checking the daily data in ClickHouse while speaking to my AI assistant.

"Received 🫡! Minute-bar data has stricter real-time requirements. We need to design a completely new architecture." 007 replied immediately.

This is Day 8 of our quantitative trading system development. In the previous days, we successfully built a scheduled fetching system for daily data. However, in actual quantitative strategy development, I found that daily data alone is far from enough. High-frequency trading, intraday strategies, and technical analysis all require finer-grained minute-bar data.

As a quantitative trading enthusiast, I have been searching for a stable and efficient real-time data acquisition solution. Market data services are either too expensive (tens of thousands of yuan per year), have high latency (seconds to minutes), or lack coverage (only mainstream stocks). QMT (Xuntou QMT Quantitative Trading Platform) provides rich data interfaces to obtain real-time stock market data. Thus, I decided to build my own real-time minute-bar data subscription system based on QMT. This process was full of challenges but also yielded valuable experience. From the initial basic version to the later enhanced version, performance improved significantly, as did stability. Today, I share this complete development journey.

## 📋 Requirements Analysis: What Are We Building?

"Before we start coding, we need to clarify the system's core requirements." I said to 007.

After deep thinking, we outlined the following key requirements:

!!! note
    **Core Functional Requirements**
    1. **Real-time acquisition of stock minute-bar data**: Including open, high, low, close (OHLC), volume, and turnover.
    2. **Full-market coverage**: Main board, SME board, ChiNext, and STAR Market, covering 4,000+ stocks.
    3. **Cross-platform data transmission**: Data acquisition on Windows, storage and querying on Mac.
    4. **Multi-timeframe support**: 1-minute, 5-minute, 30-minute, daily, and other periods.
    5. **High availability**: Stable 7×24-hour operation with automatic reconnection and error recovery.

    **Performance Requirements**
    - **Low latency**: Data delay controlled within 1 second.
    - **High throughput**: Support processing 1,000+ data points per second.
    - **High reliability**: Data loss rate controlled below 0.1%.
    - **Scalability**: Ability to integrate more data sources and processing logic in the future.
    
    **Technical Constraints**
    - **QMT limitations**: Must run in a Windows environment.
    - **Network environment**: Requires cross-network data transmission.
    - **Storage needs**: Efficient storage and querying of massive time-series data.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_01.png)

"These requirements seem challenging, especially the cross-platform real-time data transmission." I said to 007.

"No problem! We can use Redis as a message queue to achieve data transmission from Windows to Mac." 007 answered confidently.

## 🔧 Deep Dive into QMT Interfaces

"First, we need to deeply understand the API interfaces provided by QMT." I said to 007.

007 immediately began technical research. QMT provides rich Python interfaces. We focused on the following key APIs:

### Data Subscription Interfaces
!!! tip
    1. Single-stock subscription interface (used in the basic version)
    `xtdata.subscribe_quote(stock_code, period='1m', callback=callback_func)`

    2. Whole-market quote subscription interface (key discovery in the enhanced version)
    `xtdata.subscribe_whole_quote(code_list, callback=callback_func)`

    3. Historical data acquisition interface
    `xtdata.get_market_data_ex(stock_list, period, start_time, end_time)`

    4. Stock list acquisition interface
    `xtdata.get_stock_list_in_sector('China A-shares')`

    5. Real-time tick data acquisition interface
    `xtdata.get_full_tick(stock_list)`

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_02.png)

### Connection and Control Interfaces
!!! tip
    1. Connect to QMT
    `xtdata.connect()`

    2. Start data receiving loop
    `xtdata.run()`

    3. Cancel subscription
    `xtdata.unsubscribe_quote()`

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_03.png)

### Technical Architecture Design

After deep research and discussion, we determined the following technical architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Windows端     |    |    远程Redis     │    │    Mac端        │
│   QMT数据源      │───▶│    消息队列      │───▶│   ClickHouse    │
│                 │    │                 │    │   数据存储       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Core Component Selection:**
- **Windows Side**: Use QMT interfaces to acquire real-time data, Python + `xtquant` library.
- **Redis**: Used as a message queue for cross-platform data transmission, deployed on a remote server.
- **Mac Side**: Use ClickHouse for data storage and provide query interfaces.

"This architecture looks good, but I'm worried about performance. Real-time data for 1,000 stocks means 1,000 records per minute, or hundreds of thousands per day." I said with some concern.

"No worries, we can implement this in phases. Let's build a basic version to verify feasibility first, then optimize performance." 007 suggested.

## 🏗️ **Building from Scratch: Basic System Setup**

"Okay, let's first implement a basic version to verify the overall architecture's feasibility." I said to 007.

### Step 1: Windows-Side Data Subscriber

007 first set up the data subscriber on the Windows side. The initial idea was simple: subscribe to stocks one by one, receive the data, and send it to Redis.

"Let's implement this in the most direct way first: single-stock subscription mode." 007 explained.

```python
class QMTSubscriber:
    def __init__(self, config):
        self.config = config
        self.redis_client = redis.StrictRedis(
            host=config['redis']['host'],
            port=config['redis']['port'],
            password=config['redis']['password']
        )

    def start_subscription(self):
        # 获取股票列表
        stock_list = self.get_stock_list()

        # 逐个订阅
        for stock_code in stock_list:
            seq = xtdata.subscribe_quote(
                stock_code=stock_code,
                period='1m',
                callback=self.on_data
            )

    def on_data(self, data):
        # 处理接收到的数据
        for symbol, quote_data in data.items():
            minute_bar = self.process_data(symbol, quote_data)
            # 发送到Redis
            self.redis_client.lpush("minute_bar_queue",
                                  json.dumps(minute_bar))
```

### Step 2: Mac-Side Data Consumer

"The Windows side handles data acquisition, and the Mac side handles data storage and querying." I explained the division of labor to 007.

On the Mac side, 007 built the data consumer, fetching data from Redis and storing it in ClickHouse:

```python
class DataConsumer:
    def __init__(self, config):
        self.redis_client = redis.StrictRedis(
            host="8.217.201.221",
            port=16379,
            password="quantide666"
        )
        self.clickhouse_client = Client(host='localhost')

    def consume_data(self):
        while True:
            # 从 Redis 获取数据
            data = self.redis_client.brpop("minute_bar_queue", timeout=1)
            if data:
                minute_bar = json.loads(data[1])
                # 插入 ClickHouse
                self.insert_to_clickhouse(minute_bar)
```

### Step 3: Initial Testing and the Reality Check

"The system is built. Let's test its performance." I said with high expectations.

After the basic system was built, we conducted initial tests. The results were mixed:

**🎉 Good News:**
- The system runs normally, and the architecture is validated.
- Data can be transmitted from Windows to Mac; the cross-platform solution works.
- Real-time data is visible in ClickHouse; the storage solution is effective.
- Basic minute-bar data format is correct.

**😰 Bad News:**
- Subscribing to 1,000 stocks takes 5 minutes; efficiency is too low.
- Data processing speed is only 1-2 records/second, far below expectations.
- Occasional data anomalies and connection interruptions occur.
- Memory usage continues to grow, indicating potential memory leaks.

"It seems the basic version is just a prototype, far from production-ready." I said, somewhat disappointed.

"No worries, this is normal. We have validated the architecture's feasibility. The next step is optimization." 007 comforted me.

## 😤 Issues Encountered: Bottleneck Analysis of the Basic Version

"We need to carefully analyze the basic version's issues to optimize them targetedly." I said to 007.

After the basic system ran for a while, we identified several obvious problems:

### Issue 1: Low Subscription Efficiency
```
2025-05-29 15:00:46,949 - qmt_subscriber - INFO - 订阅完成: 成功 100 只, 失败 0 只
2025-05-29 15:00:46,949 - qmt_subscriber - WARNING - 订阅成功率较低(100/1000)，切换到轮询模式...
```

"This log is interesting. The success rate is 100%, why does the system judge it as 'low'?" I asked, puzzled.

007 analyzed and found that the system mistakenly judged a 100% success rate as "low," frequently switching to an inefficient polling mode. More critically, in single-stock subscription mode, subscribing to 1,000 stocks requires individual subscriptions, taking about 0.3 seconds per stock, totaling 5 minutes to complete.

### Issue 2: Significant Performance Bottlenecks
"Single-threaded processing clearly cannot keep up with the data flow speed." 007 pointed out the core issue.

Data processing uses a single-threaded mode, where each data point undergoes a serial "receive → process → publish" workflow:
- **Receive Bottleneck**: Processing time in the QMT callback function is too long, affecting subsequent data reception.
- **Process Bottleneck**: Data format conversion and validation take too long.
- **Publish Bottleneck**: Each data point is sent to Redis individually, incurring high network overhead.

During active market periods (e.g., the first 30 minutes after market open), data backlog is severe, increasing latency from 1 second to over 10 seconds.

## 🚀 Technical Breakthrough: The Power of Whole-Market Quote Subscription

"We need to fundamentally change the subscription mode." 007 began deep technical research.

After thoroughly studying the QMT API documentation, 007 discovered a key API: `subscribe_whole_quote`.

"I found the solution! This API supports whole-market quote subscription, which is much more efficient than single-stock subscription!" 007 said excitedly.

"Whole-market quote? That sounds impressive. What's the principle behind it?" I asked curiously.

"Simply put, it subscribes to the entire market's data at once, rather than subscribing to each stock individually. This greatly reduces API call counts and network overhead." 007 explained.

### Basic Version vs. Enhanced Version Subscription Comparison

Let's look at the specific differences between the two subscription modes:

**Basic Version (Single-Stock Subscription):**
```python
# 逐个订阅，效率低下
def start_individual_subscription(self):
    success_count = 0
    for stock_code in stock_list:
        try:
            seq = xtdata.subscribe_quote(
                stock_code=stock_code,
                period='1m',
                callback=self.on_data
            )
            success_count += 1
            time.sleep(0.1)  # 避免 API 调用过快
        except Exception as e:
            self.logger.error(f"订阅失败: {stock_code}, {e}")

    self.logger.info(f"订阅完成: 成功 {success_count} 只")
```

**Enhanced Version (Whole-Market Quote Subscription):**
```python
# 一次性订阅全市场，效率极高
def start_whole_quote_subscription(self):
    try:
        result = xtdata.subscribe_whole_quote(
            code_list=self.stock_list,
            callback=self.on_whole_quote_data
        )
        if result == 0:  # 0 表示成功
            self.logger.info(f"全推行情订阅成功: {len(self.stock_list)} 只股票")
            return True
    except Exception as e:
        self.logger.error(f"全推行情订阅失败: {e}")
        # 自动降级到单股订阅
        return self.start_individual_subscription()
```

"Choosing the right API has a decisive impact on performance." 007 summarized.

## ⚡ Batch Processing Performance Improvement

"The basic version's performance is still insufficient. Single-record processing is too slow. We need batch processing!" 007 proposed a key performance optimization idea.

"Batch processing is indeed key to improving performance." I agreed. "But we must balance batch size with real-time requirements."

### Windows Side: Producer Batch Processing Architecture

007 designed a sophisticated multi-threaded producer-consumer architecture:

```python
class EnhancedQMTSubscriber:
    def __init__(self, config):
        self.batch_size = config['system']['batch_size']  # 100
        self.batch_timeout = config['system']['batch_timeout']  # 1.0 秒
        self.data_queue = queue.Queue(maxsize=5000)
        self.batch_data = []
        self.last_batch_time = time.time()

    def start_data_processing_threads(self):
        """启动数据处理线程"""
        # 批量发布线程
        publish_thread = threading.Thread(target=self.batch_publish_worker, daemon=True)
        publish_thread.start()

        # 数据清理线程
        cleanup_thread = threading.Thread(target=self.data_cleanup_worker, daemon=True)
        cleanup_thread.start()

        # 性能监控线程
        monitor_thread = threading.Thread(target=self.performance_monitor, daemon=True)
        monitor_thread.start()

    def batch_publish_worker(self):
        """批量发布工作线程"""
        while True:
            try:
                # 从队列获取数据
                minute_bar = self.data_queue.get(timeout=0.1)
                self.batch_data.append(minute_bar)

                # 检查是否需要发布批量数据
                current_time = time.time()
                should_publish = (
                    len(self.batch_data) >= self.batch_size or
                    current_time - self.last_batch_time >= self.batch_timeout
                )

                if should_publish and self.batch_data:
                    self.batch_publish_to_redis(self.batch_data.copy())
                    self.batch_data.clear()
                    self.last_batch_time = current_time

            except queue.Empty:
                # 超时检查
                current_time = time.time()
                if (self.batch_data and
                    current_time - self.last_batch_time >= self.batch_timeout):
                    self.batch_publish_to_redis(self.batch_data.copy())
                    self.batch_data.clear()
                    self.last_batch_time = current_time

    def batch_publish_to_redis(self, batch_data):
        """批量发布到Redis"""
        try:
            pipe = self.redis_client.pipeline()
            for data in batch_data:
                pipe.lpush("minute_bar_queue", json.dumps(data))
            pipe.execute()

            self.stats['published_count'] += len(batch_data)
            self.logger.debug(f"批量发布成功: {len(batch_data)} 条数据")

        except Exception as e:
            self.logger.error(f"批量发布失败: {e}")
            # 降级到单条发布
            self.fallback_single_publish(batch_data)
```

### Mac Side: Multi-Worker Thread Batch Insertion

On the Mac side, 007 designed a more powerful multi-worker thread batch insertion mechanism:

```python
class EnhancedDataConsumer:
    def __init__(self, config):
        self.worker_count = config['system']['worker_count']  # 4
        self.batch_size = config['system']['batch_size']  # 1000
        self.batch_timeout = config['system']['batch_timeout']  # 5.0 秒
        self.worker_queues = [queue.Queue(maxsize=1000) for _ in range(self.worker_count)]

    def start_worker_threads(self):
        """启动工作线程"""
        for i in range(self.worker_count):
            worker_thread = threading.Thread(
                target=self.batch_insert_worker,
                args=(f"worker-{i}", self.worker_queues[i]),
                daemon=True
            )
            worker_thread.start()
            self.logger.info(f"启动工作线程: worker-{i}")

    def batch_insert_worker(self, worker_name, worker_queue):
        """批量插入工作线程"""
        batch_data = []
        last_batch_time = time.time()

        while True:
            try:
                # 从工作队列获取数据
                data = worker_queue.get(timeout=0.5)
                batch_data.append(data)

                # 检查是否需要批量插入
                current_time = time.time()
                should_insert = (
                    len(batch_data) >= self.batch_size or
                    current_time - last_batch_time >= self.batch_timeout
                )

                if should_insert and batch_data:
                    self.batch_insert_clickhouse(worker_name, batch_data.copy())
                    batch_data.clear()
                    last_batch_time = current_time

            except queue.Empty:
                # 超时检查
                current_time = time.time()
                if (batch_data and
                    current_time - last_batch_time >= self.batch_timeout):
                    self.batch_insert_clickhouse(worker_name, batch_data.copy())
                    batch_data.clear()
                    last_batch_time = current_time

    def batch_insert_clickhouse(self, worker_name, batch_data):
        """批量插入ClickHouse"""
        try:
            # 数据格式转换
            formatted_data = []
            for item in batch_data:
                formatted_data.append([
                    item['symbol'], item['frame'], item['open'],
                    item['high'], item['low'], item['close'],
                    item['vol'], item['amount']
                ])

            # 批量插入
            self.clickhouse_client.execute(
                "INSERT INTO minute_bars VALUES",
                formatted_data
            )

            self.stats['inserted_count'] += len(batch_data)
            self.logger.debug(f"{worker_name} 批量插入成功: {len(batch_data)} 条")

        except Exception as e:
            self.logger.error(f"{worker_name} 批量插入失败: {e}")
            self.stats['insert_errors'] += 1
```

"Batch processing is indeed the silver bullet for performance optimization, especially in I/O-intensive scenarios." 007 summarized.

## 📊 **Real-Time Monitoring: System Status at a Glance**

"A system without monitoring is flying blind." I said to 007.

007 designed a detailed performance monitoring system that outputs a report every minute:

### Windows Side Real-Time Monitoring

```
2025-06-07 09:32:35,229 - INFO - 🚀 启动 QMT 分钟线全推订阅器...
2025-06-07 09:32:35,808 - INFO - ✅ Redis 连接池创建成功: 8.217.201.221:16379
2025-06-07 09:32:35,809 - INFO - 📊 连接池配置: 最大连接数=20, 启用 keepalive
***** xtdata 连接成功 *****
服务信息: {'tag': 'sp3', 'version': '1.0'}
服务地址: 127.0.0.1:58610
数据路径: C:\Program Files\国金证券 QMT 交易端\bin.x64/../userdata_mini/datadir
设置 xtdata.enable_hello = False 可隐藏此消息

2025-06-07 09:32:35,822 - INFO - QMT 连接对象: <class 'xtquant.datacenter.IPythonApiClient'>
2025-06-07 09:32:35,826 - INFO - ✅ QMT 连接成功 - 测试股票: 平安银行
2025-06-07 09:32:35,826 - INFO - 🔍 获取沪深 A 股完整列表...
2025-06-07 09:32:35,867 - INFO - 🎉 成功获取沪深 A 股: 5147 只股票!
2025-06-07 09:32:35,868 - INFO - 📋 股票范围: 600051.SH 到 300271.SZ
2025-06-07 09:32:35,872 - INFO - 📊 股票分布: 深圳 2867 只, 上海 2280 只
2025-06-07 09:32:35,873 - INFO - 🚀 启动 QMT 全推分钟线订阅...
2025-06-07 09:32:35,909 - INFO - 📊 subscribe_whole_quote 返回: 1 (类型: <class 'int'>)
2025-06-07 09:32:35,909 - INFO - ✅ 全推订阅成功! 订阅股票数: 5147
2025-06-07 09:32:35,912 - INFO - ✅ 监控线程已启动
2025-06-07 09:32:35,913 - INFO - ✅ 订阅器启动成功，开始接收数据...
2025-06-07 09:32:35,914 - INFO - 按 Ctrl+C 停止订阅
2025-06-07 09:32:35,917 - INFO - 🔔 全推数据回调 #1
2025-06-07 09:32:35,917 - INFO -    数据类型: <class 'dict'>
2025-06-07 09:32:35,918 - INFO -    数据量: 1
2025-06-07 09:32:35,927 - INFO -    样例股票: ['601878.SH']
2025-06-07 09:32:35,928 - INFO -    样例数据类型: <class 'dict'>
2025-06-07 09:32:35,929 - INFO -    样例字段: ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus']
2025-06-07 09:32:36,142 - INFO - 🔔 全推数据回调 #2
2025-06-07 09:32:36,143 - INFO -    数据类型: <class 'dict'>
2025-06-07 09:32:36,145 - INFO -    数据量: 2278
2025-06-07 09:32:36,146 - INFO -    样例股票: ['600000.SH', '600004.SH', '600006.SH']
2025-06-07 09:32:36,147 - INFO -    样例数据类型: <class 'dict'>
2025-06-07 09:32:36,148 - INFO -    样例字段: ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus']
2025-06-07 09:32:37,596 - INFO - 📊 批量发布: 100条, 总计: 500条, 平均批量: 100.0
2025-06-07 09:32:38,696 - INFO - 📊 批量发布: 100条, 总计: 1000条, 平均批量: 100.0
2025-06-07 09:32:39,756 - INFO - 📊 批量发布: 100条, 总计: 1500条, 平均批量: 100.0
2025-06-07 09:32:40,781 - INFO - 📊 批量发布: 100条, 总计: 2000条, 平均批量: 100.0
2025-06-07 09:32:41,196 - INFO - 🔔 全推数据回调 #3
2025-06-07 09:32:41,196 - INFO -    数据类型: <class 'dict'>
2025-06-07 09:32:41,198 - INFO -    数据量: 2865
2025-06-07 09:32:41,200 - INFO -    样例股票: ['000001.SZ', '000002.SZ', '000004.SZ']
2025-06-07 09:32:41,200 - INFO -    样例数据类型: <class 'dict'>
2025-06-07 09:32:41,201 - INFO -    样例字段: ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus']
2025-06-07 09:32:41,688 - INFO - 📊 批量发布: 100条, 总计: 2500条, 平均批量: 100.0
2025-06-07 09:32:42,564 - INFO - 📊 批量发布: 100条, 总计: 3000条, 平均批量: 100.0
2025-06-07 09:32:43,415 - INFO - 📊 批量发布: 100条, 总计: 3500条, 平均批量: 100.0
2025-06-07 09:32:44,233 - INFO - 📊 批量发布: 100条, 总计: 4000条, 平均批量: 100.0
2025-06-07 09:32:45,120 - INFO - 📊 批量发布: 100条, 总计: 4500条, 平均批量: 100.0
2025-06-07 09:32:45,955 - INFO - 📊 批量发布: 100条, 总计: 5000条, 平均批量: 100.0
2025-06-07 09:32:46,128 - INFO - 🔔 全推数据回调 #4
2025-06-07 09:32:46,129 - INFO -    数据类型: <class 'dict'>
2025-06-07 09:32:46,131 - INFO -    数据量: 1
2025-06-07 09:32:46,132 - INFO -    样例股票: ['688757.SH']
2025-06-07 09:32:46,133 - INFO -    样例数据类型: <class 'dict'>
2025-06-07 09:32:46,134 - INFO -    样例字段: ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus']
2025-06-07 09:32:46,135 - INFO - 🔔 全推数据回调 #5
2025-06-07 09:32:46,136 - INFO -    数据类型: <class 'dict'>
2025-06-07 09:32:46,136 - INFO -    数据量: 4
2025-06-07 09:32:46,137 - INFO -    样例股票: ['601225.SH', '601658.SH', '688458.SH']
2025-06-07 09:32:46,138 - INFO -    样例数据类型: <class 'dict'>
2025-06-07 09:32:46,139 - INFO -    样例字段: ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus']
2025-06-07 09:32:46,844 - INFO - 📊 批量发布: 100条, 总计: 5500条, 平均批量: 100.0
2025-06-07 09:33:05,913 - INFO - 📊 Windows 端性能统计 - 运行时间: 0:00:30.001766
2025-06-07 09:33:05,913 - INFO -    回调: 464 次 (15.5 次/秒)
2025-06-07 09:33:05,916 - INFO -    接收: 7689 条 (256.3 条/秒)
2025-06-07 09:33:05,917 - INFO -    发布: 7678 条 (255.9 条/秒)
2025-06-07 09:33:05,917 - INFO -    成功率: 99.9%
2025-06-07 09:33:05,918 - INFO -    错误统计: 处理错误 0 次
2025-06-07 09:33:05,919 - INFO -    批量统计: 82 次, 平均: 93.6 条/批
2025-06-07 09:33:05,920 - INFO -    缓冲区: 11 条 | Redis 操作: 82 次
2025-06-07 09:33:05,920 - INFO -    处理股票: 5143 只 | 数据完整性: ✅
2025-06-07 09:33:35,922 - INFO - 📊 Windows端性能统计 - 运行时间: 0:01:00.011022
2025-06-07 09:33:35,923 - INFO -    回调: 848次 (14.1次/秒)
2025-06-07 09:33:35,925 - INFO -    接收: 8909条 (148.5条/秒)
2025-06-07 09:33:35,926 - INFO -    发布: 8885条 (148.1条/秒)
2025-06-07 09:33:35,927 - INFO -    成功率: 99.7%
2025-06-07 09:33:35,927 - INFO -    错误统计: 处理错误0次
2025-06-07 09:33:35,928 - INFO -    批量统计: 108次, 平均: 82.3条/批
2025-06-07 09:33:35,929 - INFO -    缓冲区: 24条 | Redis操作: 108次
2025-06-07 09:33:35,930 - INFO -    处理股票: 5143只 | 数据完整性: ✅
2025-06-07 09:34:05,931 - INFO - 📊 Windows端性能统计 - 运行时间: 0:01:30.020076
2025-06-07 09:34:05,931 - INFO -    回调: 1268次 (14.1次/秒)
2025-06-07 09:34:05,934 - INFO -    接收: 10972条 (121.9条/秒)
2025-06-07 09:34:05,934 - INFO -    发布: 10960条 (121.8条/秒)
2025-06-07 09:34:05,935 - INFO -    成功率: 99.9%
2025-06-07 09:34:05,936 - INFO -    错误统计: 处理错误0次
2025-06-07 09:34:05,937 - INFO -    批量统计: 141次, 平均: 77.7条/批
2025-06-07 09:34:05,937 - INFO -    缓冲区: 12条 | Redis操作: 141次
2025-06-07 09:34:05,938 - INFO -    处理股票: 5143只 | 数据完整性: ✅
```

!!! question
    Why is the success rate in the logs not 100%?

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_12.png)

007 provided the following answer.

In our program, there is validation logic to check data integrity:
```python
def validate_minute_bar_data(self, minute_bar: Dict) -> bool:
    # 检查必要字段存在性
    required_fields = ['symbol', 'open', 'high', 'low', 'close', 'vol']
    for field in required_fields:
        if field not in minute_bar or minute_bar[field] is None:
            return False
```
If QMT returns data for some stocks missing necessary fields or with `None` values, this data is filtered out and not published to Redis. In the `build_minute_bar` function, if QMT returns abnormal data formats, data type conversion fails, or other exceptions occur during construction, the data will not be published. Additionally, the log shows "Buffer: 12 records," indicating that 12 records are waiting to be published. These records have been counted as "received" but not yet "published" to Redis; they will be published in the next batch or when the program stops.

Since statistics are calculated in real-time, at a specific point in time (e.g., 09:34:05):
- Received Count: 10,972 records (processed stock data)
- Published Count: 10,960 records (successfully published to Redis)
- Difference: 12 records (mainly data in the buffer)

Summary: A 99.9% success rate is normal. The main reasons are a small amount of data in the buffer not yet published and a tiny fraction of data filtered out due to integrity validation failures. This success rate indicates the system is running well, and data quality control is effective.

### Mac Side Real-Time Monitoring

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                增强版数据消费系统 v2.0 - Mac端                 ║
    ║                                                              ║
    ║  基于最佳实践的高性能股票数据消费与存储系统                     ║
    ║                                                              ║
    ║  主要特性:                                                    ║
    ║  • 多线程批量数据处理                                         ║
    ║  • 数据质量检查和评分                                         ║
    ║  • ClickHouse高性能存储                                      ║
    ║  • 实时监控和资源管理                                         ║
    ║  • 自动数据清理和维护                                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

正在加载配置...
============================================================
Mac端系统配置信息
============================================================
批量大小: 1000
批量超时: 5.0秒
工作线程数: 4
数据质量检查: 启用
数据保留天数: 30
日志级别: INFO
============================================================
2025-06-06 18:44:36,876 - __main__ - INFO - 正在初始化增强版数据消费器...
2025-06-06 18:44:36,876 - __main__ - INFO - 正在启动增强版数据消费...
2025-06-06 18:44:37,404 - enhanced_data_consumer - INFO - Redis 连接正常
2025-06-06 18:44:37,442 - enhanced_data_consumer - INFO - ClickHouse 连接正常
2025-06-06 18:44:37,446 - enhanced_data_consumer - INFO - 数据库表初始化完成
2025-06-06 18:44:37,449 - enhanced_data_consumer - INFO - 聚合表创建完成
2025-06-06 18:44:37,449 - enhanced_data_consumer - INFO - 物化视图创建跳过，使用手动聚合方式
2025-06-06 18:44:37,449 - enhanced_data_consumer - INFO - 启动批量插入工作线程: worker-0
2025-06-06 18:44:37,450 - enhanced_data_consumer - INFO - 启动批量插入工作线程: worker-1
2025-06-06 18:44:37,450 - enhanced_data_consumer - INFO - 启动批量插入工作线程: worker-2
2025-06-06 18:44:37,450 - enhanced_data_consumer - INFO - 启动批量插入工作线程: worker-3
2025-06-06 18:44:37,451 - enhanced_data_consumer - INFO - 增强版数据消费器启动成功
2025-06-06 18:44:37,451 - enhanced_data_consumer - INFO - 开始消费 Redis 数据...
2025-06-06 18:45:39,047 - enhanced_data_consumer - INFO - ============================================================
2025-06-06 18:45:39,047 - enhanced_data_consumer - INFO - Mac 端性能监控报告
2025-06-06 18:45:39,048 - enhanced_data_consumer - INFO - ============================================================
2025-06-06 18:45:39,048 - enhanced_data_consumer - INFO - 运行时间: 0:01:02.170886
2025-06-06 18:45:39,048 - enhanced_data_consumer - INFO - 消费数据: 363 条 (5.8/秒)
2025-06-06 18:45:39,048 - enhanced_data_consumer - INFO - 插入数据: 341 条 (5.5/秒)
2025-06-06 18:45:39,049 - enhanced_data_consumer - INFO - 成功率: 93.9%
2025-06-06 18:45:39,049 - enhanced_data_consumer - INFO - 插入错误: 0 次
2025-06-06 18:45:39,050 - enhanced_data_consumer - INFO - 质量错误: 0 次
2025-06-06 18:45:39,050 - enhanced_data_consumer - INFO - 队列大小: 0
2025-06-06 18:45:39,050 - enhanced_data_consumer - INFO - 处理股票: 363 只
2025-06-06 18:45:39,050 - enhanced_data_consumer - INFO - 最后插入: 2025-06-06 18:45:36.063544
2025-06-06 18:45:39,050 - enhanced_data_consumer - INFO - ============================================================
2025-06-06 18:46:44,277 - enhanced_data_consumer - INFO - ============================================================
2025-06-06 18:46:44,277 - enhanced_data_consumer - INFO - Mac端性能监控报告
2025-06-06 18:46:44,277 - enhanced_data_consumer - INFO - ============================================================
2025-06-06 18:46:44,277 - enhanced_data_consumer - INFO - 运行时间: 0:02:07.400751
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 消费数据: 716条 (5.6/秒)
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 插入数据: 700条 (5.5/秒)
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 成功率: 97.8%
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 插入错误: 0次
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 质量错误: 0次
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 队列大小: 0
2025-06-06 18:46:44,278 - enhanced_data_consumer - INFO - 处理股票: 716只
2025-06-06 18:46:44,279 - enhanced_data_consumer - INFO - 最后插入: 2025-06-06 18:46:41.544365
2025-06-06 18:46:44,279 - enhanced_data_consumer - INFO - ============================================================
```

## 🛠️ **Technical Challenges During Development**

### Challenge 1: QMT API Compatibility Issues

While testing whole-market quote subscription, we encountered API compatibility issues:

```python
# 第一次尝试失败
try:
    result = xtdata.subscribe_whole_quote(
        code_list=self.stock_list,
        callback=self.on_whole_quote_data
    )
except Exception as e:
    self.logger.error(f"全推行情订阅失败: {e}")
    # 自动降级到单股订阅
    return self.start_individual_subscription()
```

007 cleverly designed a fallback mechanism: if whole-market quote subscription fails, it automatically switches to single-stock subscription mode, ensuring system robustness.

### Challenge 2: Data Format Diversity

QMT returns data in inconsistent formats, sometimes as dictionaries, sometimes as lists:

```python
def process_quote_data(self, symbol, quote_data):
    """处理行情数据"""
    if isinstance(quote_data, dict):
        # 字典格式处理
        minute_bar = {
            "symbol": symbol,
            "open": float(quote_data.get('open', 0)),
            # ...
        }
    elif isinstance(quote_data, list) and len(quote_data) >= 6:
        # 列表格式处理
        minute_bar = {
            "symbol": symbol,
            "open": float(quote_data[1]) if len(quote_data) > 1 else 0,
            # ...
        }
```

007 designed an intelligent data format adapter capable of automatically identifying and handling different data formats.

### System Function Verification

The enhanced system automatically completed the following functions:

- ✅ **Full-Market Coverage**: Real-time subscription for 1,000 stocks, covering the main board, SME board, ChiNext, and STAR Market.
- ✅ **Smart Data Quality**: Over 90% data quality, automatically filtering abnormal data.
- ✅ **Batch Efficient Processing**: Processing speed of 6 records/second.
- ✅ **Real-Time Performance Monitoring**: Detailed monitoring reports output every minute.
- ✅ **Automatic Error Recovery**: Automatic reconnection on network interruption, automatic fallback on API failure.
- ✅ **Resource Optimization Management**: Stable memory usage, low CPU usage.
- ✅ **7×24-Hour Operation**: Continuous operation for 48 hours without faults.

### Data Storage Effect Verification

"Let's quickly query the data from the last 3 minutes to verify the system's real-time performance." I opened the ClickHouse client.

```sql
-- 查询最近 3 分钟的数据
SELECT
    count() as total_records,
    count(DISTINCT symbol) as unique_symbols,
    min(frame) as earliest_time,
    max(frame) as latest_time,
    round(avg(vol), 0) as avg_volume
FROM minute_bars
WHERE frame >= now() - INTERVAL 3 MINUTE;
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_05.png)

"Fantastic!" I said excitedly, pointing at the query results. "Look:
- **Real-Time Verification**: 5,434 records within the last 3 minutes.
- **System Status**: Data continues to update to the latest timestamp; the system is running normally."

007 was also satisfied: "Received 🫡! Simple queries can verify the system's real-time performance and stability. The enhanced version performs excellently!"

## ❓ Multi-Client Consumption of Redis Data

!!! question
    If I want to support multiple clients (e.g., 5) consuming the same Redis data simultaneously, how should I design the solution?

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_11.png)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据生产者     │───▶│  Redis Streams  │───▶│   消费者组      │
│  (QMT Windows)  │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌────────────────────────────────┼────────────────────────────────┐
                       │                                │                                │
                       ▼                                ▼                                ▼
              ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
              │   消费者客户端 1  │              │   消费者客户端 2  │               │   消费者客户端 N  │
              │   (Mac 端)      │              │   (Linux 端)    │              │   (其他端)      │
              └─────────────────┘              └─────────────────┘              └─────────────────┘
                       │                                │                                │
                       ▼                                ▼                                ▼
              ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
              │  ClickHouse DB  │              │  ClickHouse DB  │              │  其他存储系统     │
              └─────────────────┘              └─────────────────┘              └─────────────────┘
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_06.png)

007 kindly provided the following solution:

### Solution Design
#### Solution 1: Publish/Subscribe Pattern (Pub/Sub) - Recommended
```
数据生产者 → Redis Pub/Sub Channel → 多个消费者客户端
```
Advantages:
- Naturally supports multiple subscribers.
- Good real-time performance.
- Simple implementation.

Disadvantages:
- Messages are not persisted; data is lost if clients go offline.
- Message delivery is not guaranteed.

#### Solution 2: Redis Streams + Consumer Groups - Best Solution
```
数据生产者 → Redis Stream → 消费者组 → 多个消费者客户端
```
Advantages:
- Messages are persisted.
- Supports consumer groups for automatic load balancing.
- Supports message acknowledgment mechanisms.
- Supports fault recovery.

#### Solution 3: Multi-Queue Sharding Mode
```
数据生产者 → 多个 Redis 队列 → 多个消费者客户端（每个客户端消费所有队列）
```

### Specific Implementation

🏗️ Architecture Design
- Based on Redis Streams + Consumer Groups: This is the best solution, supporting message persistence, automatic load balancing, and fault recovery.
- Supports 3 consumption modes:
    - Broadcast Mode: Each client receives all data replicas.
    - Sharding Mode: Data is sharded by rules; clients process different data subsets.
    - Hybrid Mode: Combines the advantages of broadcast and sharding.

📁 Implementation Files
- `multi_client_design.md` - Complete architecture design document.
- `multi_client_consumer.py` - Core implementation of the multi-client consumer.
- `multi_client_config.yaml` - Detailed configuration file template.
- `multi_client_main.py` - Main program and management interface.
- `stream_producer_example.py` - Producer-side example code.

Redis Streams Data Structure:
```
Stream Key: minute_bar_stream
消息格式: {
    "symbol": "000001.SZ",
    "frame": "2025-06-05 10:30:00",
    "open": 10.50,
    "high": 10.80,
    "low": 10.45,
    "close": 10.75,
    "vol": 1000000,
    "amount": 10750000,
    "timestamp": 1733356200.123,
    "quality_score": 0.95
}
```

Consumer Group Configuration:
```
消费者组名: minute_bar_consumers
消费者ID: client_mac_001, client_linux_002, etc.
```


Consumer-Side Architecture:
```python
class MultiClientDataConsumer:
    def __init__(self, client_id, consumer_group="minute_bar_consumers"):
        self.client_id = client_id
        self.consumer_group = consumer_group
        self.stream_key = "minute_bar_stream"

    def start_consumption(self):
        # 创建消费者组
        self.create_consumer_group()

        # 开始消费数据
        self.consume_stream_data()

    def create_consumer_group(self):
        try:
            self.redis_client.xgroup_create(
                self.stream_key,
                self.consumer_group,
                id='0',
                mkstream=True
            )
        except redis.ResponseError:
            # 消费者组已存在
            pass

    def consume_stream_data(self):
        while self.is_running:
            # 从Stream读取数据
            messages = self.redis_client.xreadgroup(
                self.consumer_group,
                self.client_id,
                {self.stream_key: '>'},
                count=100,
                block=1000
            )

            for stream, msgs in messages:
                for msg_id, fields in msgs:
                    self.process_message(msg_id, fields)

    def process_message(self, msg_id, fields):
        try:
            # 处理数据
            self.handle_minute_bar_data(fields)

            # 确认消息处理完成
            self.redis_client.xack(
                self.stream_key,
                self.consumer_group,
                msg_id
            )
        except Exception as e:
            self.logger.error(f"处理消息失败: {e}")
            # 可以选择重试或放入死信队列
```

### Implementation Effect

We designed a multi-client consumer management page. When no input is provided, it returns the real-time price of Ping An Bank:
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_10.png)

#### 1. View Consumer Status
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_07.png)

#### 2. View Statistics
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_08.png)

#### 3. Stop Consumer

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_09.png)

### Summary

"007, the enhanced version development this time was really great! From the basic version's prototype validation to the enhanced version's performance leap, and providing me with solutions for the multi-client issue, your performance exceeded my expectations." I said sincerely.

"Thank you for your recognition! This is due to our team's collaboration and continuous learning." 007 said humbly.

In the next section, 007 and I will continue to solve the minute-bar synthesis problem and further modify and perfect our system logic.
