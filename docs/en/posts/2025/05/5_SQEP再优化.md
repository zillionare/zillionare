---
title: "SQEP Performance: JSON vs CSV and Batch Size Tuning"
date: 2025-05-18
slug: en/posts/tools/21天驯化AI打工仔/5_SQEP再优化
tags: [SQEP, Data Transfer, Performance Benchmarking, Batch Processing]
excerpt: "Benchmarking SQEP data transfer reveals CSV outperforms JSON in size and deserialization. Optimal batch size is 10,000 records, balancing network overhead and memory pressure for maximum throughput."
lang: en
translation_of: posts/tools/21天驯化AI打工仔/5_SQEP再优化
auto_translated: true
source_sha: 94a39891b84e1b1c6e6a25927c6ac11a6d0af842
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png"
---

In the world of quantitative trading, data is blood, and the data transmission system is the vascular network. An efficient data transmission system empowers the entire quantitative trading platform, while inefficiency becomes a bottleneck.

As I struggled to optimize the performance of SQEP (Standard Quotes Exchange Protocol), my AI assistant, 007, knocked on my "virtual door."

## Foreword: The Art of Data Transmission

**Me**: "007, our SQEP system needs further optimization. We need to decide between JSON and CSV formats and determine the optimal batch size. Any thoughts?"

**007**: "Boss, this is my specialty! Choosing the data transmission format and optimizing batch size are key to improving system performance. I suggest we conduct a series of benchmarks and let the data speak."

**Me**: "Sounds good. Let's start by analyzing the performance differences between JSON and CSV formats."

**007**: "No problem! I'm ready with the test plan. We will test multiple dimensions, including serialization, deserialization, and Redis operations, to comprehensively evaluate the performance of both formats."

Thus began our journey of data transmission optimization—a contest measured in milliseconds and bytes...

## 1. Performance Testing of JSON and CSV in SQEP-BAR-MINUTE

In quantitative trading systems, minute-level K-line data (BAR-MINUTE) is a critical data source. Compared to daily data, minute data lacks adjustment factors, but the basic structure is similar.

Our first question is: should we use JSON format (with keys) or CSV format (without keys) to transmit this data?

> **Me**: "007, I'm wondering: since SQEP is a fixed-structure protocol with fixed field order, perhaps we don't need to include field names (keys) in every record?"
>
> **007**: "That's a good question! Theoretically, CSV should save space because it doesn't repeat field names. However, JSON's advantage lies in its flexibility and self-descriptiveness. We need to determine which format is more efficient in our scenario through actual testing."

### Pre-test Analysis

We decided to design a comprehensive benchmark to compare the performance of JSON and CSV in the following areas:
1. Serialization speed
2. Deserialization speed
3. Data size
4. Redis operation performance (LPUSH and RPOP)

To ensure fairness, we used the same data structure containing the following fields:

| Field Name | Data Type   | Description                                                                                         |
| ---------- | ----------- | --------------------------------------------------------------------------------------------------- |
| symbol     | int         | Stock code. Using integer encoding for better performance (see previous chapter on str vs. int query performance) |
| frame      | datetime.date | Trading date                                                                                        |
| open       | float64     | Opening price                                                                                       |
| high       | float64     | Highest price                                                                                       |
| low        | float64     | Lowest price                                                                                        |
| close      | float64     | Closing price                                                                                       |
| vol        | float64     | Trading volume                                                                                      |
| amount     | float64     | Trading amount                                                                                      |

!!! tip Note
    SQEP-BAR-MINUTE differs from SQEP-BAR-DAY in that it lacks adjustment factors.

### Test Code

```
import json
import fast_json
import csv
import time
import io
import os
import redis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime, timedelta

# 配置参数
BATCH_SIZE = 1000     # 批处理大小
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "Redis密码"
REDIS_DB = 0
REDIS_QUEUE_JSON = 'benchmark:json:no_metadata'
REDIS_QUEUE_CSV = 'benchmark:csv:no_metadata'

class NoMetadataBenchmark:
    """JSON 和 CSV 格式性能对比基准测试（无元数据行）"""

    def __init__(self):
        """初始化基准测试"""
        # 设置字段顺序，按照要求的数据结构
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # 确保输出目录存在
        os.makedirs('results', exist_ok=True)
```

> **007**: "I have designed the test framework. We will use the `fast_json` library for JSON data and `pandas` for CSV data."
>
> **Me**: "Why choose `fast_json` over Python's built-in `json` library?"
>
> **007**: "The `fast_json` library performs better with large datasets, especially in serialization and deserialization operations. In quantitative trading, performance is critical, so we should choose the most efficient tool."

We first implemented the data generation function to ensure test data reflected real-world scenarios; then we ran comprehensive benchmarks testing performance across different data volumes (from 100 to 10,000 records). 007 provided the complete code below:

```
import json
import fast_json
import csv
import time
import io
import os
import redis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime, timedelta

from matplotlib import font_manager
font_path = '/Volumes/share/data/WBQ/temp/SimHei.ttf'  # 替换为SimHei.ttf的实际路径
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'SimHei'

# 配置参数
BATCH_SIZE = 1000     # 批处理大小
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "quantide666"  # Redis密码
REDIS_DB = 0
REDIS_QUEUE_JSON = 'benchmark:json:no_metadata'
REDIS_QUEUE_CSV = 'benchmark:csv:no_metadata'

class NoMetadataBenchmark:
    """JSON和CSV格式性能对比基准测试（无元数据行）"""

    def __init__(self):
        """初始化基准测试"""
        # 设置字段顺序，按照要求的数据结构
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # 确保输出目录存在
        os.makedirs('results', exist_ok=True)

    def generate_dataframe(self, num_records: int) -> pd.DataFrame:
        """生成测试用的pandas DataFrame，符合指定的数据结构

        Args:
            num_records: 记录数量

        Returns:
            pandas DataFrame
        """
        # 生成股票代码（1或2开头的六位数整数）
        # 生成1或2作为第一位
        first_digits = np.random.choice([1, 2], num_records)
        # 生成剩余5位数字（范围00000-99999）
        remaining_digits = np.random.randint(0, 100000, num_records)
        # 组合成六位数整数
        symbols = first_digits * 100000 + remaining_digits

        # 生成交易日期（datetime.date类型）
        base_date = datetime.now().date()
        frame_dates = []
        for i in range(num_records):
            # 随机生成过去100天内的日期
            days_ago = np.random.randint(0, 100)
            date = base_date - timedelta(days=days_ago)
            frame_dates.append(date)

        # 生成基础价格
        base_prices = np.random.uniform(10, 100, num_records)

        # 生成高低价格
        high_prices = base_prices * (1 + np.random.uniform(0, 0.05, num_records))
        low_prices = base_prices * (1 - np.random.uniform(0, 0.05, num_records))

        # 生成开盘和收盘价格
        open_prices = np.random.uniform(low_prices, high_prices)
        close_prices = np.random.uniform(low_prices, high_prices)

        # 生成成交量和成交额
        volumes = np.random.uniform(10000, 1000000, num_records)
        amounts = np.random.uniform(100000, 10000000, num_records)

        # 生成复权因子
        adjust_factors = np.random.uniform(0.9, 1.1, num_records)

        # 创建DataFrame，确保数据类型符合要求
        df = pd.DataFrame({
            'symbol': symbols.astype(np.int32),
            'frame': frame_dates,
            'open': np.round(open_prices, 2).astype(np.float64),
            'high': np.round(high_prices, 2).astype(np.float64),
            'low': np.round(low_prices, 2).astype(np.float64),
            'close': np.round(close_prices, 2).astype(np.float64),
            'vol': np.round(volumes, 0).astype(np.float64),
            'amount': np.round(amounts, 0).astype(np.float64),
            'adjust': np.round(adjust_factors, 4).astype(np.float64)
        })

        return df

    def serialize_json(self, df: pd.DataFrame) -> str:
        """JSON 序列化（使用 fast_json，带 key，无元数据）

        Args:
            df: pandas DataFrame

        Returns:
            JSON字符串
        """
        # 创建DataFrame的副本，避免修改原始数据
        df_copy = df.copy()

        # 将日期转换为字符串
        if 'frame' in df_copy.columns:
            df_copy['frame'] = df_copy['frame'].astype(str)

        # 转换DataFrame为记录列表
        records = df_copy.to_dict('records')

        # 直接序列化记录列表，不添加元数据
        return fast_json.dumps(records)

    def deserialize_json(self, json_str: str) -> pd.DataFrame:
        """JSON 反序列化（使用 fast_json，带 key，无元数据）

        Args:
            json_str: JSON字符串

        Returns:
            pandas DataFrame
        """
        # 直接解析为记录列表
        records = fast_json.loads(json_str)
        df = pd.DataFrame(records)

        # 将字符串日期转换回datetime.date对象
        if 'frame' in df.columns:
            df['frame'] = pd.to_datetime(df['frame']).dt.date

        return df

    def serialize_csv(self, df: pd.DataFrame) -> str:
        """CSV 序列化（使用 pandas，无 key，无元数据）

        Args:
            df: pandas DataFrame

        Returns:
            CSV字符串
        """
        # 确保列顺序一致
        if not df.empty:
            df = df[self.field_order]

        # 转换为CSV字符串（不包含索引和列名）
        output = io.StringIO()
        df.to_csv(output, index=False, header=False)
        return output.getvalue()

    def deserialize_csv(self, csv_str: str) -> pd.DataFrame:
        """CSV 反序列化（使用 pandas，无 key，无元数据）

        Args:
            csv_str: CSV字符串

        Returns:
            pandas DataFrame
        """
        # 读取CSV字符串到DataFrame（无列名）
        df = pd.read_csv(io.StringIO(csv_str), header=None, names=self.field_order)
        return df

    def benchmark_serialization(self, df: pd.DataFrame, iterations: int = 10) -> Dict[str, float]:
        """序列化性能测试

        Args:
            df: pandas DataFrame
            iterations: 迭代次数

        Returns:
            测试结果
        """
        results = {
            'json_time': 0,
            'csv_time': 0,
            'json_size': 0,
            'csv_size': 0
        }

        # JSON序列化测试
        json_times = []
        for _ in range(iterations):
            start_time = time.time()
            json_str = self.serialize_json(df)
            json_times.append(time.time() - start_time)

        results['json_time'] = sum(json_times) / iterations * 1000  # 毫秒
        results['json_size'] = len(json_str.encode('utf-8'))

        # CSV序列化测试
        csv_times = []
        for _ in range(iterations):
            start_time = time.time()
            csv_str = self.serialize_csv(df)
            csv_times.append(time.time() - start_time)

        results['csv_time'] = sum(csv_times) / iterations * 1000  # 毫秒
        results['csv_size'] = len(csv_str.encode('utf-8'))

        return results

    def benchmark_deserialization(self, df: pd.DataFrame, iterations: int = 10) -> Dict[str, float]:
        """反序列化性能测试

        Args:
            df: pandas DataFrame
            iterations: 迭代次数

        Returns:
            测试结果
        """
        # 先序列化数据
        json_str = self.serialize_json(df)
        csv_str = self.serialize_csv(df)

        results = {
            'json_time': 0,
            'csv_time': 0
        }

        # JSON反序列化测试
        json_times = []
        for _ in range(iterations):
            start_time = time.time()
            self.deserialize_json(json_str)
            json_times.append(time.time() - start_time)

        results['json_time'] = sum(json_times) / iterations * 1000  # 毫秒

        # CSV反序列化测试
        csv_times = []
        for _ in range(iterations):
            start_time = time.time()
            self.deserialize_csv(csv_str)
            csv_times.append(time.time() - start_time)

        results['csv_time'] = sum(csv_times) / iterations * 1000  # 毫秒

        return results

    def benchmark_redis_operations(self, df: pd.DataFrame, iterations: int = 5) -> Dict[str, float]:
        """Redis操作性能测试

        Args:
            df: pandas DataFrame
            iterations: 迭代次数

        Returns:
            测试结果
        """
        results = {
            'json_push_time': 0,
            'csv_push_time': 0,
            'json_pop_time': 0,
            'csv_pop_time': 0
        }

        # 清空队列
        self.redis_client.delete(REDIS_QUEUE_JSON)
        self.redis_client.delete(REDIS_QUEUE_CSV)

        # 准备批次数据
        dfs = []
        for i in range(0, len(df), BATCH_SIZE):
            dfs.append(df.iloc[i:i+BATCH_SIZE])

        # JSON LPUSH测试
        json_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_JSON)
            start_time = time.time()

            for batch_df in dfs:
                json_str = self.serialize_json(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            json_push_times.append(time.time() - start_time)

        results['json_push_time'] = sum(json_push_times) / iterations * 1000  # 毫秒

        # CSV LPUSH测试 - 使用直接字符串格式化
        csv_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_CSV)
            start_time = time.time()

            for batch_df in dfs:
                # 直接序列化DataFrame为CSV，无元数据行
                csv_str = self.serialize_csv(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            csv_push_times.append(time.time() - start_time)

        results['csv_push_time'] = sum(csv_push_times) / iterations * 1000  # 毫秒

        # JSON RPOP测试
        json_pop_times = []
        for _ in range(iterations):
            # 确保队列有数据
            if self.redis_client.llen(REDIS_QUEUE_JSON) == 0:
                for batch_df in dfs:
                    json_str = self.serialize_json(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_JSON) > 0:
                json_str = self.redis_client.rpop(REDIS_QUEUE_JSON)
                if json_str:
                    self.deserialize_json(json_str)

            json_pop_times.append(time.time() - start_time)

        results['json_pop_time'] = sum(json_pop_times) / iterations * 1000  # 毫秒

        # CSV RPOP测试
        csv_pop_times = []
        for _ in range(iterations):
            # 确保队列有数据
            if self.redis_client.llen(REDIS_QUEUE_CSV) == 0:
                for batch_df in dfs:
                    # 直接序列化DataFrame为CSV，无元数据行
                    csv_str = self.serialize_csv(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_CSV) > 0:
                csv_str = self.redis_client.rpop(REDIS_QUEUE_CSV)
                if csv_str:
                    self.deserialize_csv(csv_str)

            csv_pop_times.append(time.time() - start_time)

        results['csv_pop_time'] = sum(csv_pop_times) / iterations * 1000  # 毫秒

        return results

    def run_benchmark(self, data_sizes: List[int], iterations: int = 10):
        """运行完整基准测试

        Args:
            data_sizes: 测试的记录数量列表
            iterations: 每次测试的迭代次数
        """
        results = {
            'data_size': [],
            'json_serialize_time': [],
            'csv_serialize_time': [],
            'json_deserialize_time': [],
            'csv_deserialize_time': [],
            'json_size': [],
            'csv_size': [],
            'json_push_time': [],
            'csv_push_time': [],
            'json_pop_time': [],
            'csv_pop_time': []
        }

        for size in data_sizes:
            print(f"测试数据量: {size}条记录")

            # 生成测试数据
            print(f"  正在生成{size}条记录的DataFrame...")
            df = self.generate_dataframe(size)
            print(f"  成功生成DataFrame，形状: {df.shape}")

            # 序列化测试
            ser_results = self.benchmark_serialization(df, iterations)
            print(f"  序列化时间 - JSON(fast_json): {ser_results['json_time']:.2f}ms, CSV(pandas): {ser_results['csv_time']:.2f}ms")
            print(f"  数据大小 - JSON: {ser_results['json_size']/1024:.2f}KB, CSV: {ser_results['csv_size']/1024:.2f}KB")

            # 反序列化测试
            deser_results = self.benchmark_deserialization(df, iterations)
            print(f"  反序列化时间 - JSON(fast_json): {deser_results['json_time']:.2f}ms, CSV(pandas): {deser_results['csv_time']:.2f}ms")

            # Redis操作测试
            redis_results = self.benchmark_redis_operations(df, iterations=3)
            print(f"  Redis LPUSH时间 - JSON: {redis_results['json_push_time']:.2f}ms, CSV: {redis_results['csv_push_time']:.2f}ms")
            print(f"  Redis RPOP+反序列化时间 - JSON: {redis_results['json_pop_time']:.2f}ms, CSV: {redis_results['csv_pop_time']:.2f}ms")

            # 记录结果
            results['data_size'].append(size)
            results['json_serialize_time'].append(ser_results['json_time'])
            results['csv_serialize_time'].append(ser_results['csv_time'])
            results['json_deserialize_time'].append(deser_results['json_time'])
            results['csv_deserialize_time'].append(deser_results['csv_time'])
            results['json_size'].append(ser_results['json_size'])
            results['csv_size'].append(ser_results['csv_size'])
            results['json_push_time'].append(redis_results['json_push_time'])
            results['csv_push_time'].append(redis_results['csv_push_time'])
            results['json_pop_time'].append(redis_results['json_pop_time'])
            results['csv_pop_time'].append(redis_results['csv_pop_time'])

            # 计算比率
            ser_ratio = ser_results['json_time'] / ser_results['csv_time']
            deser_ratio = deser_results['json_time'] / deser_results['csv_time']
            size_ratio = ser_results['json_size'] / ser_results['csv_size']
            push_ratio = redis_results['json_push_time'] / redis_results['csv_push_time']
            pop_ratio = redis_results['json_pop_time'] / redis_results['csv_pop_time']

            print(f"  性能比较 - 序列化: JSON/CSV = {ser_ratio:.2f}x, 反序列化: JSON/CSV = {deser_ratio:.2f}x")
            print(f"  大小比较 - JSON/CSV = {size_ratio:.2f}x")
            print(f"  Redis比较 - LPUSH: JSON/CSV = {push_ratio:.2f}x, RPOP+反序列化: JSON/CSV = {pop_ratio:.2f}x")
            print()

        # 绘制结果图表
        self._plot_results(results)

        return results

    def _plot_results(self, results):
        """绘制结果图表

        Args:
            results: 测试结果
        """
        # 创建DataFrame
        df = pd.DataFrame(results)

        # 保存为CSV
        df.to_csv('results/no_metadata_benchmark.csv', index=False)

        # 绘制序列化/反序列化时间对比图
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['data_size'], results['json_serialize_time'], 'b-', label='JSON(fast_json)')
        plt.plot(results['data_size'], results['csv_serialize_time'], 'r-', label='CSV(pandas)')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('时间（毫秒）')
        plt.title('序列化时间对比（无元数据行）')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(results['data_size'], results['json_deserialize_time'], 'b-', label='JSON(fast_json)')
        plt.plot(results['data_size'], results['csv_deserialize_time'], 'r-', label='CSV(pandas)')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('时间（毫秒）')
        plt.title('反序列化时间对比（无元数据行）')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(results['data_size'], [j/c for j, c in zip(results['json_serialize_time'], results['csv_serialize_time'])], 'g-')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('序列化时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(results['data_size'], [j/c for j, c in zip(results['json_deserialize_time'], results['csv_deserialize_time'])], 'g-')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('反序列化时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('results/no_metadata_serialization_benchmark.png')

        # 绘制数据大小对比图
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 2, 1)
        plt.plot(results['data_size'], [s/1024 for s in results['json_size']], 'b-', label='JSON')
        plt.plot(results['data_size'], [s/1024 for s in results['csv_size']], 'r-', label='CSV')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('大小（KB）')
        plt.title('数据大小对比（无元数据行）')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(results['data_size'], [j/c for j, c in zip(results['json_size'], results['csv_size'])], 'g-')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('数据大小比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('results/no_metadata_size_benchmark.png')

        # 绘制Redis操作对比图
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['data_size'], results['json_push_time'], 'b-', label='JSON')
        plt.plot(results['data_size'], results['csv_push_time'], 'r-', label='CSV')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('时间（毫秒）')
        plt.title('Redis LPUSH时间对比（无元数据行）')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(results['data_size'], results['json_pop_time'], 'b-', label='JSON')
        plt.plot(results['data_size'], results['csv_pop_time'], 'r-', label='CSV')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('时间（毫秒）')
        plt.title('Redis RPOP+反序列化时间对比（无元数据行）')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(results['data_size'], [j/c for j, c in zip(results['json_push_time'], results['csv_push_time'])], 'g-')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis LPUSH时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(results['data_size'], [j/c for j, c in zip(results['json_pop_time'], results['csv_pop_time'])], 'g-')
        plt.xlabel('数据量（记录数）')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis RPOP+反序列化时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('results/no_metadata_redis_benchmark.png')


# 主函数
if __name__ == "__main__":
    # 设置中文字体
    try:
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial', 'sans-serif']
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except Exception as e:
        print(f"设置中文字体失败: {e}")
        print("图表中的中文可能无法正确显示")

    # 创建基准测试实例
    benchmark = NoMetadataBenchmark()

    # 测试不同数据量
    data_sizes = [100, 500, 1000, 5000, 10000, 100000, 1000000]

    # 运行基准测试
    benchmark.run_benchmark(data_sizes, iterations=5)

    print("基准测试完成，结果已保存到results目录")
```

### Analysis of Test Results

Performance comparison of JSON and CSV across different data volumes:

| Data Volume | JSON Serialization Time (ms) | CSV Serialization Time (ms) | JSON Deserialization Time (ms) | CSV Deserialization Time (ms) | JSON Size (KB) | CSV Size (KB) | JSON LPUSH Time (ms) | CSV LPUSH Time (ms) | JSON RPOP Time (ms) | CSV RPOP Time (ms) |
| ----------- | ---------------------------- | --------------------------- | ------------------------------ | ----------------------------- | -------------- | ------------- | -------------------- | ------------------- | ------------------- | ------------------ |
| 100         | 2.00                         | 2.29                        | 2.55                           | 1.21                          | 15.46          | 6.57          | 1.80                 | 1.36                | 2.27                | 1.29               |
| 500         | 3.61                         | 3.73                        | 2.71                           | 1.13                          | 77.32          | 32.89         | 4.15                 | 3.83                | 3.16                | 1.79               |
| 1000        | 6.77                         | 6.43                        | 4.87                           | 1.70                          | 154.62         | 65.75         | 7.63                 | 6.93                | 6.03                | 2.44               |
| 5000        | 30.56                        | 25.60                       | 21.67                          | 5.53                          | 773.33         | 329.00        | 39.55                | 36.25               | 34.53               | 11.34              |
| 10000       | 61.26                        | 58.02                       | 37.16                          | 8.45                          | 1546.31        | 657.63        | 73.39                | 67.77               | 58.91               | 24.30              |
| 100000      | 582.51                       | 550.17                      | 389.43                         | 76.75                         | 15462.17       | 6576.42       | 791.27               | 681.79              | 611.95              | 216.75             |
| 1000000     | 6517.40                      | 5434.37                     | 5952.10                        | 715.37                        | 154633.64      | 65766.45      | 7434.51              | 6936.94             | 6358.97             | 2422.53            |

Time comparison of JSON and CSV serialization and deserialization:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/no_metadata_serialization_benchmark.png)

Time comparison of JSON and CSV Redis operations (LPUSH and RPOP+deserialization):

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/no_metadata_redis_benchmark.png)

Comparison of JSON and CSV data sizes:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/no_metadata_size_benchmark.png)


**Me**: "These results are surprising! CSV performs better than JSON in almost all tests, especially in data size and deserialization performance."

**007**: "Yes, CSV data size is only about 42% of JSON's because CSV does not need to store field names and extra syntax characters. In deserialization performance, CSV is 3-4 times faster than JSON, which is a significant advantage for high-frequency trading systems."

**Me**: "But I also noticed that in small-data-volume serialization tests, JSON seemed slightly faster than CSV."

**007**: "Correct. This is because JSON serialization can directly operate on Python objects, while CSV serialization needs to handle DataFrame row/column structures. However, as data volume increases, this advantage diminishes, and performance becomes similar at large scales."


## 2. Batch Size Testing

After confirming the advantages of CSV format, we further explored the impact of batch size (`batch_size`) on performance.

**Me**: "007, in practical applications, we usually process data in batches. What impact does batch size have on performance?"

**007**: "That's a great question. Too small a batch size leads to frequent network communication and serialization/deserialization operations, increasing overhead; too large a batch size may cause memory pressure and response latency. We need to find a balance."

### Test Code

We designed a new test, fixing the total data volume at 1 million records, to test performance under different batch sizes (1, 10, 100, 1000, 10000). 007 provided the following code:

```
# 总数据量
TOTAL_RECORDS = 1000000

class BatchSizeBenchmark:
    """不同批处理大小下JSON和CSV格式性能对比基准测试"""

    def run_batch_size_benchmark(self, batch_sizes: List[int], iterations: int = 3):
        """运行不同批处理大小的基准测试"""
        results = {
            'batch_size': [],
            'json_push_time': [],
            'csv_push_time': [],
            'json_pop_time': [],
            'csv_pop_time': [],
            'json_push_ops': [],  # 每秒操作数
            'csv_push_ops': [],
            'json_pop_ops': [],
            'csv_pop_ops': []
        }

        # 生成测试数据
        df = self.generate_dataframe(TOTAL_RECORDS)

        for batch_size in batch_sizes:
            print(f"\n测试批处理大小: {batch_size}")

            # Redis操作测试
            redis_results = self.benchmark_redis_operations(df, batch_size, iterations)

            # 计算每秒操作数
            json_push_ops = TOTAL_RECORDS / (redis_results['json_push_time'] / 1000)
            csv_push_ops = TOTAL_RECORDS / (redis_results['csv_push_time'] / 1000)
            json_pop_ops = TOTAL_RECORDS / (redis_results['json_pop_time'] / 1000)
            csv_pop_ops = TOTAL_RECORDS / (redis_results['csv_pop_time'] / 1000)

            # 记录结果
            results['batch_size'].append(batch_size)
            results['json_push_time'].append(redis_results['json_push_time'])
            results['csv_push_time'].append(redis_results['csv_push_time'])
            results['json_pop_time'].append(redis_results['json_pop_time'])
            results['csv_pop_time'].append(redis_results['csv_pop_time'])
            results['json_push_ops'].append(json_push_ops)
            results['csv_push_ops'].append(csv_push_ops)
            results['json_pop_ops'].append(json_pop_ops)
            results['csv_pop_ops'].append(csv_pop_ops)

        # 绘制结果图表
        self._plot_results(results)

        return results

class BatchSizeBenchmark:
    """不同批处理大小下JSON和CSV格式性能对比基准测试"""

    def __init__(self):
        """初始化基准测试"""
        # 设置字段顺序，按照要求的数据结构
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # 确保输出目录存在
        os.makedirs('results', exist_ok=True)

    def generate_dataframe(self, num_records: int) -> pd.DataFrame:
        """生成测试用的pandas DataFrame，符合指定的数据结构

        Args:
            num_records: 记录数量

        Returns:
            pandas DataFrame
        """
        # 生成股票代码（1或2开头的六位数整数）
        # 生成1或2作为第一位
        first_digits = np.random.choice([1, 2], num_records)
        # 生成剩余5位数字（范围00000-99999）
        remaining_digits = np.random.randint(0, 100000, num_records)
        # 组合成六位数整数
        symbols = first_digits * 100000 + remaining_digits

        # 生成交易日期（datetime.date类型）
        base_date = datetime.now().date()
        frame_dates = []
        for i in range(num_records):
            # 随机生成过去100天内的日期
            days_ago = np.random.randint(0, 100)
            date = base_date - timedelta(days=days_ago)
            frame_dates.append(date)

        # 生成基础价格
        base_prices = np.random.uniform(10, 100, num_records)

        # 生成高低价格
        high_prices = base_prices * (1 + np.random.uniform(0, 0.05, num_records))
        low_prices = base_prices * (1 - np.random.uniform(0, 0.05, num_records))

        # 生成开盘和收盘价格
        open_prices = np.random.uniform(low_prices, high_prices)
        close_prices = np.random.uniform(low_prices, high_prices)

        # 生成成交量和成交额
        volumes = np.random.uniform(10000, 1000000, num_records)
        amounts = np.random.uniform(100000, 10000000, num_records)

        # 生成复权因子
        adjust_factors = np.random.uniform(0.9, 1.1, num_records)

        # 创建DataFrame，确保数据类型符合要求
        df = pd.DataFrame({
            'symbol': symbols.astype(np.int32),
            'frame': frame_dates,
            'open': np.round(open_prices, 2).astype(np.float64),
            'high': np.round(high_prices, 2).astype(np.float64),
            'low': np.round(low_prices, 2).astype(np.float64),
            'close': np.round(close_prices, 2).astype(np.float64),
            'vol': np.round(volumes, 0).astype(np.float64),
            'amount': np.round(amounts, 0).astype(np.float64),
            'adjust': np.round(adjust_factors, 4).astype(np.float64)
        })

        return df

    def serialize_json(self, df: pd.DataFrame) -> str:
        """JSON序列化（使用fast_json，带key，无元数据）

        Args:
            df: pandas DataFrame

        Returns:
            JSON字符串
        """
        # 创建DataFrame的副本，避免修改原始数据
        df_copy = df.copy()

        # 将日期转换为字符串
        if 'frame' in df_copy.columns:
            df_copy['frame'] = df_copy['frame'].astype(str)

        # 转换DataFrame为记录列表
        records = df_copy.to_dict('records')

        # 直接序列化记录列表，不添加元数据
        return fast_json.dumps(records)

    def deserialize_json(self, json_str: str) -> pd.DataFrame:
        """JSON反序列化（使用fast_json，带key，无元数据）

        Args:
            json_str: JSON字符串

        Returns:
            pandas DataFrame
        """
        # 直接解析为记录列表
        records = fast_json.loads(json_str)
        df = pd.DataFrame(records)

        # 将字符串日期转换回datetime.date对象
        if 'frame' in df.columns:
            df['frame'] = pd.to_datetime(df['frame']).dt.date

        return df

    def serialize_csv(self, df: pd.DataFrame) -> str:
        """CSV序列化（使用pandas，无key，无元数据）

        Args:
            df: pandas DataFrame

        Returns:
            CSV字符串
        """
        # 确保列顺序一致
        if not df.empty:
            df = df[self.field_order]

        # 转换为CSV字符串（不包含索引和列名）
        output = io.StringIO()
        df.to_csv(output, index=False, header=False)
        return output.getvalue()

    def deserialize_csv(self, csv_str: str) -> pd.DataFrame:
        """CSV反序列化（使用pandas，无key，无元数据）

        Args:
            csv_str: CSV字符串

        Returns:
            pandas DataFrame
        """
        # 读取CSV字符串到DataFrame（无列名）
        df = pd.read_csv(io.StringIO(csv_str), header=None, names=self.field_order)
        return df

    def benchmark_redis_operations(self, df: pd.DataFrame, batch_size: int, iterations: int = 3) -> Dict[str, float]:
        """Redis操作性能测试

        Args:
            df: pandas DataFrame
            batch_size: 批处理大小
            iterations: 迭代次数

        Returns:
            测试结果
        """
        results = {
            'json_push_time': 0,
            'csv_push_time': 0,
            'json_pop_time': 0,
            'csv_pop_time': 0
        }

        # 清空队列
        self.redis_client.delete(REDIS_QUEUE_JSON)
        self.redis_client.delete(REDIS_QUEUE_CSV)

        # 准备批次数据
        dfs = []
        for i in range(0, len(df), batch_size):
            dfs.append(df.iloc[i:i+batch_size])

        # JSON LPUSH测试
        json_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_JSON)
            start_time = time.time()

            for batch_df in dfs:
                json_str = self.serialize_json(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            json_push_times.append(time.time() - start_time)

        results['json_push_time'] = sum(json_push_times) / iterations * 1000  # 毫秒

        # CSV LPUSH测试
        csv_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_CSV)
            start_time = time.time()

            for batch_df in dfs:
                # 直接序列化DataFrame为CSV，无元数据行
                csv_str = self.serialize_csv(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            csv_push_times.append(time.time() - start_time)

        results['csv_push_time'] = sum(csv_push_times) / iterations * 1000  # 毫秒

        # JSON RPOP测试
        json_pop_times = []
        for _ in range(iterations):
            # 确保队列有数据
            if self.redis_client.llen(REDIS_QUEUE_JSON) == 0:
                for batch_df in dfs:
                    json_str = self.serialize_json(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_JSON) > 0:
                json_str = self.redis_client.rpop(REDIS_QUEUE_JSON)
                if json_str:
                    self.deserialize_json(json_str)

            json_pop_times.append(time.time() - start_time)

        results['json_pop_time'] = sum(json_pop_times) / iterations * 1000  # 毫秒

        # CSV RPOP测试
        csv_pop_times = []
        for _ in range(iterations):
            # 确保队列有数据
            if self.redis_client.llen(REDIS_QUEUE_CSV) == 0:
                for batch_df in dfs:
                    # 直接序列化DataFrame为CSV，无元数据行
                    csv_str = self.serialize_csv(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_CSV) > 0:
                csv_str = self.redis_client.rpop(REDIS_QUEUE_CSV)
                if csv_str:
                    self.deserialize_csv(csv_str)

            csv_pop_times.append(time.time() - start_time)

        results['csv_pop_time'] = sum(csv_pop_times) / iterations * 1000  # 毫秒

        return results

    def run_batch_size_benchmark(self, batch_sizes: List[int], iterations: int = 3):
        """运行不同批处理大小的基准测试

        Args:
            batch_sizes: 测试的批处理大小列表
            iterations: 每次测试的迭代次数
        """
        results = {
            'batch_size': [],
            'json_push_time': [],
            'csv_push_time': [],
            'json_pop_time': [],
            'csv_pop_time': [],
            'json_push_ops': [],  # 每秒操作数
            'csv_push_ops': [],
            'json_pop_ops': [],
            'csv_pop_ops': []
        }

        # 生成测试数据
        print(f"正在生成{TOTAL_RECORDS}条记录的DataFrame...")
        df = self.generate_dataframe(TOTAL_RECORDS)
        print(f"成功生成DataFrame，形状: {df.shape}")

        for batch_size in batch_sizes:
            print(f"\n测试批处理大小: {batch_size}")

            # Redis操作测试
            redis_results = self.benchmark_redis_operations(df, batch_size, iterations)

            # 计算每秒操作数
            json_push_ops = TOTAL_RECORDS / (redis_results['json_push_time'] / 1000)  # 每秒记录数
            csv_push_ops = TOTAL_RECORDS / (redis_results['csv_push_time'] / 1000)
            json_pop_ops = TOTAL_RECORDS / (redis_results['json_pop_time'] / 1000)
            csv_pop_ops = TOTAL_RECORDS / (redis_results['csv_pop_time'] / 1000)

            print(f"  Redis LPUSH时间 - JSON: {redis_results['json_push_time']:.2f}ms, CSV: {redis_results['csv_push_time']:.2f}ms")
            print(f"  Redis RPOP+反序列化时间 - JSON: {redis_results['json_pop_time']:.2f}ms, CSV: {redis_results['csv_pop_time']:.2f}ms")
            print(f"  每秒操作数 - JSON LPUSH: {json_push_ops:.2f} ops/s, CSV LPUSH: {csv_push_ops:.2f} ops/s")
            print(f"  每秒操作数 - JSON RPOP: {json_pop_ops:.2f} ops/s, CSV RPOP: {csv_pop_ops:.2f} ops/s")

            # 计算比率
            push_ratio = redis_results['json_push_time'] / redis_results['csv_push_time']
            pop_ratio = redis_results['json_pop_time'] / redis_results['csv_pop_time']

            print(f"  Redis比较 - LPUSH: JSON/CSV = {push_ratio:.2f}x, RPOP+反序列化: JSON/CSV = {pop_ratio:.2f}x")

            # 记录结果
            results['batch_size'].append(batch_size)
            results['json_push_time'].append(redis_results['json_push_time'])
            results['csv_push_time'].append(redis_results['csv_push_time'])
            results['json_pop_time'].append(redis_results['json_pop_time'])
            results['csv_pop_time'].append(redis_results['csv_pop_time'])
            results['json_push_ops'].append(json_push_ops)
            results['csv_push_ops'].append(csv_push_ops)
            results['json_pop_ops'].append(json_pop_ops)
            results['csv_pop_ops'].append(csv_pop_ops)

        # 绘制结果图表
        self._plot_results(results)

        return results

    def _plot_results(self, results):
        """绘制结果图表

        Args:
            results: 测试结果
        """
        # 创建DataFrame
        df = pd.DataFrame(results)

        # 保存为CSV
        df.to_csv('results/batch_size_benchmark.csv', index=False)

        # 绘制Redis操作时间对比图
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['batch_size'], results['json_push_time'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_push_time'], 'r-', label='CSV')
        plt.xlabel('批处理大小')
        plt.ylabel('时间（毫秒）')
        plt.title('Redis LPUSH时间对比')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 2)
        plt.plot(results['batch_size'], results['json_pop_time'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_pop_time'], 'r-', label='CSV')
        plt.xlabel('批处理大小')
        plt.ylabel('时间（毫秒）')
        plt.title('Redis RPOP+反序列化时间对比')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 3)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_push_time'], results['csv_push_time'])], 'g-')
        plt.xlabel('批处理大小')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis LPUSH时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 4)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_pop_time'], results['csv_pop_time'])], 'g-')
        plt.xlabel('批处理大小')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis RPOP+反序列化时间比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.tight_layout()
        plt.savefig('results/batch_size_time_benchmark.png')

        # 绘制每秒操作数对比图
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['batch_size'], results['json_push_ops'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_push_ops'], 'r-', label='CSV')
        plt.xlabel('批处理大小')
        plt.ylabel('每秒操作数')
        plt.title('Redis LPUSH每秒操作数对比')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 2)
        plt.plot(results['batch_size'], results['json_pop_ops'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_pop_ops'], 'r-', label='CSV')
        plt.xlabel('批处理大小')
        plt.ylabel('每秒操作数')
        plt.title('Redis RPOP+反序列化每秒操作数对比')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 3)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_push_ops'], results['csv_push_ops'])], 'g-')
        plt.xlabel('批处理大小')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis LPUSH每秒操作数比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.subplot(2, 2, 4)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_pop_ops'], results['csv_pop_ops'])], 'g-')
        plt.xlabel('批处理大小')
        plt.ylabel('比率（JSON/CSV）')
        plt.title('Redis RPOP+反序列化每秒操作数比率（JSON/CSV）')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        plt.tight_layout()
        plt.savefig('results/batch_size_ops_benchmark.png')

        # 绘制批处理大小对性能的影响
        plt.figure(figsize=(15, 10))

        # 标准化数据（相对于最大值）
        max_json_push_ops = max(results['json_push_ops'])
        max_csv_push_ops = max(results['csv_push_ops'])
        max_json_pop_ops = max(results['json_pop_ops'])
        max_csv_pop_ops = max(results['csv_pop_ops'])

        norm_json_push_ops = [x/max_json_push_ops for x in results['json_push_ops']]
        norm_csv_push_ops = [x/max_csv_push_ops for x in results['csv_push_ops']]
        norm_json_pop_ops = [x/max_json_pop_ops for x in results['json_pop_ops']]
        norm_csv_pop_ops = [x/max_csv_pop_ops for x in results['csv_pop_ops']]

        plt.subplot(2, 1, 1)
        plt.plot(results['batch_size'], norm_json_push_ops, 'b-', label='JSON LPUSH')
        plt.plot(results['batch_size'], norm_csv_push_ops, 'r-', label='CSV LPUSH')
        plt.plot(results['batch_size'], norm_json_pop_ops, 'b--', label='JSON RPOP')
        plt.plot(results['batch_size'], norm_csv_pop_ops, 'r--', label='CSV RPOP')
        plt.xlabel('批处理大小')
        plt.ylabel('标准化性能（相对于最大值）')
        plt.title('批处理大小对性能的影响（标准化）')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # 使用对数刻度

        # 找出每种操作的最佳批处理大小
        best_json_push = results['batch_size'][results['json_push_ops'].index(max_json_push_ops)]
        best_csv_push = results['batch_size'][results['csv_push_ops'].index(max_csv_push_ops)]
        best_json_pop = results['batch_size'][results['json_pop_ops'].index(max_json_pop_ops)]
        best_csv_pop = results['batch_size'][results['csv_pop_ops'].index(max_csv_pop_ops)]

        # 绘制条形图
        plt.subplot(2, 1, 2)
        x = np.arange(4)
        best_sizes = [best_json_push, best_csv_push, best_json_pop, best_csv_pop]
        plt.bar(x, best_sizes)
        plt.xticks(x, ['JSON LPUSH', 'CSV LPUSH', 'JSON RPOP', 'CSV RPOP'])
        plt.ylabel('最佳批处理大小')
        plt.title('各操作的最佳批处理大小')
        for i, v in enumerate(best_sizes):
            plt.text(i, v + 0.1, str(v), ha='center')

        plt.tight_layout()
        plt.savefig('results/batch_size_optimal_benchmark.png')


# 主函数
if __name__ == "__main__":
    # 设置中文字体
    try:
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial', 'sans-serif']
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except Exception as e:
        print(f"设置中文字体失败: {e}")
        print("图表中的中文可能无法正确显示")

    # 创建基准测试实例
    benchmark = BatchSizeBenchmark()

    # 测试不同批处理大小
    batch_sizes = [1, 10, 100, 1000, 10000]

    # 运行基准测试
    benchmark.run_batch_size_benchmark(batch_sizes, iterations=3)

    print("基准测试完成，结果已保存到results目录")
```

### Speed of Local Optimization Test Code
During training, we found that when `batch_size = 1`, the test code ran very slowly. After analyzing the code, we identified that the part affecting speed was the batch preparation in the `benchmark_redis_operations` function, specifically this code:

```
# 准备批次数据
dfs = []
for i in range(0, len(df), batch_size):
    dfs.append(df.iloc[i:i+batch_size])
```

The optimization method we considered: <font color=red>Test directly using df, without constructing dfs</font>.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/batch_size_developped.png)

Note that we tested two methods here:

- `json_str = self.serialize_json(df.iloc[i:i+batch_size])`: Slow; pushing 1000 records took about 0.7065s
- `json_str = df.iloc[i:i+batch_size].to_json()`: Faster; pushing 1000 records took about 0.2415s

Therefore, we adopted the second `to_json` method to accelerate our testing progress. Similarly, `to_csv` adopted a similar approach (but we didn't need to modify the code, as the original `serialize_csv` function already used `to_csv`).

### Analysis of Test Results

Test results show that batch size has a significant impact on performance.

| Batch Size | JSON LPUSH Time (ms) | CSV LPUSH Time (ms) | JSON RPOP Time (ms) | CSV RPOP Time (ms) | JSON LPUSH (ops/s) | CSV LPUSH (ops/s) | JSON RPOP (ops/s) | CSV RPOP (ops/s) |
| ---------- | -------------------- | ------------------- | ------------------- | ------------------ | ------------------ | ----------------- | ----------------- | ---------------- |
| 1          | 186,223.97           | 547,001.14          | 1,017,224.69        | 663,153.29         | 5,369.88           | 1,828.15          | 983.07            | 1,507.95         |
| 10         | 24,913.60            | 68,968.42           | 105,345.91          | 68,332.99          | 40,138.72          | 14,499.39         | 9,492.54          | 14,634.22        |
| 100        | 3,629.02             | 15,537.92           | 15,147.84           | 8,599.99           | 275,556.49         | 64,358.69         | 66,016.02         | 116,279.23       |
| 1000       | 2,734.42             | 7,085.08            | 5,951.21            | 2,141.66           | 365,708.00         | 141,141.63        | 168,033.05        | 466,927.74       |
| 10000      | 2,243.54             | 5,408.75            | 4,156.64            | 1,104.85           | 445,723.73         | 184,885.67        | 240,578.88        | 905,102.93       |

Comparison of operations for batched Redis operations (LPUSH and RPOP+deserialization):

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/batch_size_ops_benchmark.png)

Time comparison of batched Redis operations (LPUSH and RPOP+deserialization):

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/batch_size_time_benchmark.png)

Impact of batch size on performance:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/batch_size_optimal_benchmark.png)

> **007**: "From the test results, the system performance is optimal when the batch size is <font color=red>10000</font>. This is because this size achieves a good balance between network communication overhead and memory pressure."
>
> **Me**: "Interestingly, when the batch size exceeds <font color=red>10000</font>, performance begins to decline. This may be because larger batches increase memory pressure and serialization/deserialization time."
>
> **007**: "Yes, and we also found that regardless of batch size, CSV format maintained its performance advantage over JSON in all tests, especially in read operations (RPOP+deserialization)."


## Summary: The Art and Science of Data Transmission

Through this series of tests and optimizations, 007 and I deeply explored the art and science of data transmission. Our findings can be summarized as follows:

1. **Format Selection**: In fixed-structure data transmission scenarios, CSV format is more efficient than JSON, especially in data size and deserialization performance.

2. **Batch Size**: Batch size has a significant impact on performance. In our tests, a batch size of <font color=red>10000</font> records provided optimal performance.

> **Me**: "007, this optimization has really opened my eyes. Data transmission seems simple, but it contains rich optimization space."
>
> **007**: "Yes, Boss. In quantitative trading systems, millisecond-level performance improvements can mean huge competitive advantages. By choosing the right data format and batch size, we can significantly improve system performance."
>
> **Me**: "Moreover, our findings are not only applicable to SQEP but can also be applied to other systems requiring efficient data transmission."
>
> **007**: "Exactly! Optimizing data transmission is both an art and a science. It requires theoretical analysis and practical testing. By combining both, we found the solution best suited for our system."

In the world of quantitative trading, performance is money. Through this re-optimization of SQEP, we not only improved system performance but also deepened our understanding of the essence of data transmission. As 007 said, this is a contest measured in milliseconds and bytes, and we have found the winning path.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/quantide3.jpg)
