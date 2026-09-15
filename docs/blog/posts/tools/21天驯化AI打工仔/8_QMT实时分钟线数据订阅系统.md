---
title: "21 天驯化 AI 打工仔: QMT 实时分笔数据订阅系统与多 Client 问题"
date: 2025-06-15
categories: tools
tags:
    - augment
    - tools
    - qmt
    - redis
excerpt: "当数据如潮水般涌来，如何让系统稳如磐石？本文带你深入 QMT 实时数据订阅的世界，见证 007 助手如何将一个简单的数据获取程序，升级为处理能力提升 10 倍的高性能系统！"
---

> 当数据如潮水般涌来，如何让系统稳如磐石？本文带你深入 QMT 实时数据订阅的世界，见证 007 助手如何将一个简单的数据获取程序，升级为处理能力提升 10 倍的高性能系统！

"007，我们的日线数据定时获取系统已经很稳定了，但现在我需要更细粒度的数据——分钟线数据。"我一边查看着 ClickHouse 中的日线数据，一边对我的 AI 助手说道。

"收到🫡！分钟线数据的实时性要求更高，我们需要设计一个全新的架构。"007 立刻回应道。

这是我们量化交易系统开发的第 8 天。前面几天，我们已经成功搭建了日线数据的定时获取系统，但在实际量化策略开发中，我发现仅有日线数据是远远不够的。高频交易、日内策略、技术分析等都需要更细粒度的分钟线数据。

作为一个量化交易爱好者，我一直在寻找一个稳定、高效的实时数据获取方案。市面上的数据服务要么太贵（动辄几万元一年），要么延迟太高（几秒甚至几分钟），要么覆盖面不够（只有主流股票）。QMT（迅投 QMT 量化交易平台）提供了丰富的数据接口，可以获取实时的股票行情数据。于是，我决定基于 QMT 搭建一套属于自己的实时分钟线数据订阅系统。这个过程充满了挑战，也收获了很多经验。从最初的基础版到后来的增强版，性能大幅提升，稳定性也大幅改善。今天就来分享一下这个完整的开发历程。

## 📋 需求分析：我们要做什么

"在开始编码之前，我们需要明确系统的核心需求。"我对 007 说道。

经过深入思考，我们梳理出了以下关键需求：

!!! note
    **核心功能需求**
    1. **实时获取股票分钟线数据**：包括开高低收、成交量、成交额等基础数据
    2. **支持全市场股票**：A 股主板、中小板、创业板、科创板，覆盖 4000+ 只股票
    3. **跨平台数据传输**：Windows 端获取数据，Mac 端存储和查询
    4. **多时间周期支持**：1 分钟、5 分钟、30 分钟、日线等多种周期
    5. **高可用性**：7×24 小时稳定运行，自动重连和错误恢复

    **性能要求**
    - **低延迟**：数据延迟控制在 1 秒以内
    - **高吞吐**：支持每秒处理 1000+ 条数据
    - **高可靠性**：数据丢失率控制在 0.1% 以下
    - **可扩展性**：后续可以接入更多数据源和处理逻辑
    
    **技术约束**
    - **QMT 限制**：只能在 Windows 环境运行
    - **网络环境**：需要跨网络传输数据
    - **存储需求**：海量时序数据的高效存储和查询

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_01.png)

"这些需求看起来很有挑战性，特别是跨平台的实时数据传输。"我对 007 说道。

"没问题！我们可以用 Redis 作为消息队列，实现 Windows 到 Mac 的数据传输。"007 信心满满地回答。

## 🔧 QMT 接口深度调研

"首先我们需要深入了解 QMT 提供的 API 接口。"我对 007 说道。

007 立刻开始了技术调研，QMT 提供了丰富的 Python 接口，我们重点研究了以下几个关键 API：

### 数据订阅相关接口
!!! tip
    1. 单股订阅接口（基础版使用）
    `xtdata.subscribe_quote(stock_code, period='1m', callback=callback_func)`

    2. 全推行情订阅接口（增强版的关键发现）
    `xtdata.subscribe_whole_quote(code_list, callback=callback_func)`

    3. 历史数据获取接口
    `xtdata.get_market_data_ex(stock_list, period, start_time, end_time)`

    4. 股票列表获取接口
    `xtdata.get_stock_list_in_sector('沪深A股')`

    5. 实时 tick 数据获取接口
    `xtdata.get_full_tick(stock_list)`

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_02.png)

### 连接和控制接口
!!! tip
    1. 连接 QMT
    `xtdata.connect()`

    2. 启动数据接收循环
    `xtdata.run()`

    3. 取消订阅
    `xtdata.unsubscribe_quote()`

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_03.png)

### 技术架构设计

经过深入调研和讨论，我们确定了以下技术架构：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Windows端     |    |    远程Redis     │    │    Mac端        │
│   QMT数据源      │───▶│    消息队列      │───▶│   ClickHouse    │
│                 │    │                 │    │   数据存储       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**核心组件选择：**
- **Windows 端**：使用 QMT 接口获取实时数据，Python + xtquant 库
- **Redis**：作为消息队列，实现跨平台数据传输，部署在远程服务器
- **Mac 端**：使用 ClickHouse 存储数据，提供查询接口

"这个架构看起来不错，但我担心性能问题。1000 只股票的实时数据，每分钟就是 1000 条记录，一天就是几十万条数据。"我有些担心地说道。

"没关系，我们可以分阶段实现。先做一个基础版验证可行性，然后再优化性能。"007 建议道。

## 🏗️ **从零开始：基础版系统搭建**

"好，我们先实现一个基础版本，验证整体架构的可行性。"我对 007 说道。

### 第一步：Windows 端数据订阅器

007 首先在 Windows 端搭建了数据订阅器。最初的想法很简单：逐个订阅股票，接收数据后发送到 Redis。

"我们先用最直接的方式实现，单股订阅模式。"007 解释道。

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

### 第二步：Mac 端数据消费器

"Windows 端负责数据获取，Mac 端负责数据存储和查询。"我对 007 说明了分工。

在 Mac 端，007 搭建了数据消费器，从 Redis 获取数据并存储到 ClickHouse：

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

### 第三步：初步测试与现实的冲击

"系统搭建完成，我们来测试一下效果。"我满怀期待地说道。

基础版系统搭建完成后，我们进行了初步测试。结果让人喜忧参半：

**🎉 好消息**：
- 系统能够正常运行，架构验证成功
- 数据能够从 Windows 传输到 Mac，跨平台方案可行
- ClickHouse 中能够看到实时数据，存储方案有效
- 基本的分钟线数据格式正确

**😰 坏消息**：
- 订阅 1000 只股票需要 5 分钟，效率太低
- 数据处理速度只有 1-2 条/秒，远低于预期
- 偶尔出现数据异常和连接中断
- 内存使用量持续增长，存在内存泄漏

"看来基础版只能算是一个原型，距离生产环境还有很大差距。"我有些失望地说道。

"没关系，这是正常的。我们已经验证了架构的可行性，接下来就是优化的问题了。"007 安慰道。

## 😤 遇到的问题：基础版的瓶颈分析

"我们需要仔细分析基础版的问题，才能有针对性地优化。"我对 007 说道。

在基础版系统运行了一段时间后，我们发现了几个明显的问题：

### 问题 1：订阅效率低下
```
2025-05-29 15:00:46,949 - qmt_subscriber - INFO - 订阅完成: 成功 100 只, 失败 0 只
2025-05-29 15:00:46,949 - qmt_subscriber - WARNING - 订阅成功率较低(100/1000)，切换到轮询模式...
```

"这个日志很有意思，明明成功率是 100%，为什么系统判断为'较低'？"我疑惑地问道。

007 分析后发现：系统误判 100% 的成功率为"较低"，频繁切换到低效的轮询模式。更要命的是，单股订阅模式下，1000 只股票需要逐个订阅，每只股票耗时约 0.3 秒，总计需要 5 分钟才能完成订阅。

### 问题 2：性能瓶颈明显
"单线程处理明显跟不上数据流的速度。"007 指出了核心问题。

数据处理采用单线程模式，每条数据都要经历"接收→处理→发布"的串行流程：
- **接收瓶颈**：QMT 回调函数中处理时间过长，影响后续数据接收
- **处理瓶颈**：数据格式转换和验证耗时较长
- **发布瓶颈**：每条数据单独发送到 Redis，网络开销大

在市场活跃时段（如开盘前 30 分钟），数据积压严重，延迟从 1 秒增加到 10 秒以上。

## 🚀 技术突破：全推行情订阅的威力
"我们需要从根本上改变订阅模式。"007 开始了深度技术调研。

经过深入研究 QMT API 文档，007 发现了一个关键的 API：`subscribe_whole_quote`。

"我找到了解决方案！这个 API 支持全推行情订阅，比单股订阅效率高得多！"007 兴奋地说。

"全推行情？这听起来很厉害，具体是什么原理？"我好奇地问道。

"简单来说，就是一次性订阅全市场的数据，而不是逐个订阅每只股票。这样可以大大减少 API 调用次数和网络开销。"007 解释道。

### 基础版 vs 增强版订阅对比

让我们来看看两种订阅模式的具体差异：

**基础版（单股订阅）：**
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

**增强版（全推行情订阅）：**
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

"选择合适的 API 对性能的影响是决定性的。"007 总结道。

## ⚡ 批量处理性能提升

"基础版性能还是不够。单条处理太慢了，我们需要批量处理！"007 提出了关键的性能优化思路。

"批量处理确实是提升性能的关键。"我赞同道，"但要注意平衡批量大小和实时性。"

### Windows 端：生产者批量处理架构

007 设计了一个精巧的生产者-消费者模式的多线程架构：

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

### Mac 端：多工作线程批量插入

在 Mac 端，007 设计了更强大的多工作线程批量插入机制：

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

"批量处理确实是性能优化的银弹，特别是在 I/O 密集型场景中。"007 总结道。

## 📊 **实时监控：系统状态一目了然**

"没有监控的系统是盲飞。"我对 007 说。

007 设计了详细的性能监控系统，每分钟输出一次报告：

### Windows 端实时监控

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
    为什么日志中的成功率不是100%呢？

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_12.png)

007给出了以下回答。

在我们的程序中，有检测数据完整性的验证逻辑：
```python
def validate_minute_bar_data(self, minute_bar: Dict) -> bool:
    # 检查必要字段存在性
    required_fields = ['symbol', 'open', 'high', 'low', 'close', 'vol']
    for field in required_fields:
        if field not in minute_bar or minute_bar[field] is None:
            return False
```
如果QMT返回的某些股票数据缺少必要字段或字段值为None，这些数据会被过滤掉，不会发布到Redis。在 `build_minute_bar` 函数中，如果QMT返回的数据格式异常、数据类型转换失败或其他构建过程中的异常都会导致数据不被发布。此外，从日志中可以看到“缓冲区: 12条”，说明还有12条数据在等待发布，这些数据已经被“接收”计数，但还没有被“发布”到Redis，会在下次批量发布或程序停止时才发布。

由于统计是实时计算的，在某个时间点（例如 09:34:05）：
- 接收计数：10972 条（已处理的股票数据）
- 发布计数：10960 条（已成功发布到 Redis）
- 差异：12 条（主要是缓冲区中的数据）

总结：99.9% 的成功率是正常的，主要原因是缓冲区中有少量数据还未发布，以及极少数数据因完整性验证失败被过滤。这个成功率表明系统运行良好，数据质量控制有效。

### Mac 端实时监控

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

## 🛠️ **开发过程中的技术挑战**

### 挑战 1：QMT API 的兼容性问题

在测试全推行情订阅时，我们遇到了 API 兼容性问题：

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

007 机智地设计了降级机制：如果全推行情订阅失败，自动切换到单股订阅模式，确保系统的鲁棒性。

### 挑战 2：数据格式的多样性

QMT 返回的数据格式并不统一，有时是字典，有时是列表：

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

007 设计了智能的数据格式适配器，能够自动识别和处理不同的数据格式。

### 系统功能验证

增强版系统自动完成了以下功能：

- ✅ **全市场覆盖**：1000 只股票实时订阅，覆盖主板、中小板、创业板、科创板
- ✅ **智能数据质量**：90% 以上的数据质量，自动过滤异常数据
- ✅ **批量高效处理**：6 条/秒的处理速度
- ✅ **实时性能监控**：每分钟输出详细监控报告
- ✅ **自动错误恢复**：网络中断自动重连，API 失败自动降级
- ✅ **资源优化管理**：内存使用稳定，CPU 使用率低
- ✅ **7×24 小时运行**：连续运行 48 小时无故障

### 数据存储效果验证

"让我们快速查询一下最近 3 分钟的数据，验证系统的实时性。"我打开 ClickHouse 客户端。

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

"太棒了！"我兴奋地指着查询结果，"你看：
- **实时性验证**：最近 3 分钟内有 5434 条记录
- **系统状态**：数据持续更新到最新时间，系统运行正常"

007 也很满意："收到🫡！简单的查询就能验证系统的实时性和稳定性，增强版表现优异！"

## ❓多 client 消费 Redis 的数据

!!! question
    如果我希望支持多个客户端（例如 5 个）同时消费相同的 Redis 数据，应该怎么设计方案呢？

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

007 非常贴心地给出了以下的方案：

### 方案设计
#### 方案一：发布/订阅模式（Pub/Sub）- 推荐
```
数据生产者 → Redis Pub/Sub Channel → 多个消费者客户端
```
优点：
- 天然支持多个订阅者
- 实时性好
- 实现简单

缺点：
- 消息不持久化，客户端离线时会丢失数据
- 无法保证消息送达

#### 方案二：Redis Streams + 消费者组 - 最佳方案
```
数据生产者 → Redis Stream → 消费者组 → 多个消费者客户端
```
优点：
- 消息持久化
- 支持消费者组，自动负载均衡
- 支持消息确认机制
- 支持故障恢复

#### 方案三：多队列分片模式
```
数据生产者 → 多个 Redis 队列 → 多个消费者客户端（每个客户端消费所有队列）
```

### 具体实现

🏗️ 架构设计
- 基于 Redis Streams + 消费者组：这是最佳方案，支持消息持久化、自动负载均衡和故障恢复
- 支持 3 种消费模式：
    - 广播模式：每个客户端接收所有数据副本
    - 分片模式：数据按规则分片，客户端处理不同数据子集
    - 混合模式：结合广播和分片的优势

📁 实现文件
- `multi_client_design.md` - 完整的架构设计文档
- `multi_client_consumer.py` - 多客户端消费器核心实现
- `multi_client_config.yaml` - 详细的配置文件模板
- `multi_client_main.py` - 主程序和管理界面
- `stream_producer_example.py` - 生产者端示例代码

Redis Streams 数据结构：
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

消费者组配置：
```
消费者组名: minute_bar_consumers
消费者ID: client_mac_001, client_linux_002, etc.
```


消费者端的架构：
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

### 实现效果

我们设计了一个多客户端消费器管理页面，在没有任何输入的时候会返回平安银行的实时价格：
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_10.png)

#### 1. 查看消费者状态
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_07.png)

#### 2. 查看统计信息
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_08.png)

#### 3. 停止消费者

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/8_09.png)

### 总结

"007，这次的增强版开发真的很棒！从基础版的原型验证到增强版的性能飞跃，并且给我提供了多 Client 问题的方案，你的表现超出了我的预期。"我由衷地赞叹。

"谢谢你的认可！这得益于我们团队的合作和不断的学习。"007 谦虚地说。

下一节，我和 007 将继续解决分钟线合成的问题，并且对我们的系统逻辑进一步修改和完善。
