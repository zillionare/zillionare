# 21 天驯化 AI 打工仔：开发量化交易系统（五） SQEP 的性能再优化

## 前言：数据传输的艺术

在量化交易的世界里，数据就像是血液，而数据传输系统则是血管。一个高效的数据传输系统可以让整个量化交易平台如虎添翼，而低效的数据传输则会成为整个系统的瓶颈。

当我正为 SQEP（Standard Quotes Exchange Protocol）的性能优化绞尽脑汁时，我的 AI 助手 007 敲了敲我的"虚拟门"。

**我**：「007，我们的 SQEP 系统需要进一步优化了。我们需要决定是使用 JSON 还是 CSV 格式，还要确定最佳的批处理大小。你有什么想法吗？」

**007**：「BOSS，这正是我的专长！数据传输格式的选择和批处理大小的优化是提升系统性能的关键。我建议我们进行一系列基准测试，用数据说话。」

**我**：「听起来不错。那我们就从分析 JSON 和 CSV 格式的性能差异开始吧。」

**007**：「没问题！我已经准备好了测试方案。我们将测试序列化、反序列化、Redis 操作等多个维度，全方位评估两种格式的性能。」

于是，我们开始了这场数据传输优化之旅，一场关于毫秒和字节的较量...

## 1. SQEP-BAR-MINITE 的 JSON 和 CSV 性能测试

在量化交易系统中，分钟级别的 K 线数据（BAR-MINUTE）是非常重要的数据源。与日线数据相比，分钟线数据没有复权因子，但基本结构相似。

我们面临的第一个问题是：应该使用 JSON 格式（带 key）还是 CSV 格式（不带 key）来传输这些数据？

> **我**：「007，我在想，既然 SQEP 是一个固定结构的协议，字段顺序是固定的，那么也许我们不需要在每条记录中都带上字段名（key）？」
>
> **007**：「这是个好问题！从理论上讲，CSV 格式应该更节省空间，因为它不需要重复存储字段名。但 JSON 的优势在于它的灵活性和自描述性。我们需要通过实际测试来确定哪种格式在我们的场景中更高效。」

### 测试前的分析

我们决定设计一个全面的基准测试，比较 JSON 和 CSV 在以下几个方面的性能：
1. 序列化速度
2. 反序列化速度
3. 数据大小
4. Redis 操作性能（LPUSH 和 RPOP）

为了确保测试的公平性，我们使用相同的数据结构，包含以下字段：

| 字段名 | 数据类型 | 说明 |
|-------|---------|------|
| symbol | int | 股票代码。使用整型编码以提高性能（关于 str 和 int 类型在查询性能上的差异，可以回顾上一章节） |
| frame | datetime.date | 交易日期 |
| open | float64 | 开盘价 |
| high | float64 | 最高价 |
| low | float64 | 最低价 |
| close | float64 | 收盘价 |
| vol | float64 | 成交量 |
| amount | float64 | 成交额 |

!!! tip 注意
    SQEP-BAR-MINITE 相比较于 SQEP-BAR-DAY，没有复权因子。

### 测试代码

```python
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

> **007**：「我已经设计好了测试框架，我们将使用 fast_json 库处理 JSON 数据，使用 pandas 处理 CSV 数据。」
>
> **我**：「为什么选择 fast_json 而不是 Python 内置的 json 库？」
>
> **007**：「fast_json 库在处理大量数据时性能更好，特别是在序列化和反序列化操作上。在量化交易系统中，性能是关键，所以我们应该选择最高效的工具。」

我们首先实现了数据生成函数，确保测试数据符合实际场景；然后运行了全面的基准测试，测试了不同数据量（从 100 条到 10000 条记录）下的性能表现，007 提供的完整代码如下：

```python
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

### 测试结果分析

JSON 和 CSV 在不同数据量下的性能对比：

| 数据量 | JSON序列化时间(ms) | CSV序列化时间(ms) | JSON反序列化时间(ms) | CSV反序列化时间(ms) | JSON大小(KB) | CSV大小(KB) | JSON LPUSH时间(ms) | CSV LPUSH时间(ms) | JSON RPOP时间(ms) | CSV RPOP时间(ms) |
|-------|-----------------|-----------------|-------------------|-------------------|------------|------------|------------------|------------------|------------------|------------------|
| 100   | 2.00            | 2.29            | 2.55              | 1.21              | 15.46      | 6.57       | 1.80             | 1.36             | 2.27             | 1.29             |
| 500   | 3.61            | 3.73            | 2.71              | 1.13              | 77.32      | 32.89      | 4.15             | 3.83             | 3.16             | 1.79             |
| 1000  | 6.77            | 6.43            | 4.87              | 1.70              | 154.62     | 65.75      | 7.63             | 6.93             | 6.03             | 2.44             |
| 5000  | 30.56           | 25.60           | 21.67             | 5.53              | 773.33     | 329.00     | 39.55            | 36.25            | 34.53            | 11.34            |
| 10000 | 61.26           | 58.02           | 37.16             | 8.45              | 1546.31    | 657.63     | 73.39            | 67.77            | 58.91            | 24.30            |
| 100000| 582.51          | 550.17          | 389.43            | 76.75             | 15462.17   | 6576.42    | 791.27           | 681.79           | 611.95           | 216.75           |
| 1000000| 6517.40        | 5434.37         | 5952.10           | 715.37            | 154633.64  | 65766.45   | 7434.51          | 6936.94          | 6358.97          | 2422.53          |

JSON 和 CSV 序列化和反序列化的时间对比图：

![](https://images.jieyu.ai/images/2025/05/no_metadata_serialization_benchmark.png)

JSON 和 CSV Redis 操作（LPUSH 和 RPOP+反序列化）的时间对比图：

![](https://images.jieyu.ai/images/2025/05/no_metadata_redis_benchmark.png)

JSON 和 CSV 数据大小的对比图：

![](https://images.jieyu.ai/images/2025/05/no_metadata_size_benchmark.png)


**我**：「这些结果真是令人惊讶！CSV 在几乎所有测试中都表现得比 JSON 好，特别是在数据大小和反序列化性能方面。」

**007**：「是的，CSV 格式的数据大小只有 JSON 的约 42%，这是因为 CSV 不需要存储字段名和额外的语法字符。在反序列化性能上，CSV 比 JSON 快 3-4 倍，这对于高频交易系统来说是非常显著的优势。」

**我**：「但我也注意到，在小数据量的序列化测试中，JSON 似乎略快于 CSV。」

**007**：「没错，这是因为 JSON 序列化可以直接操作 Python 对象，而 CSV 序列化需要处理 DataFrame 的行列结构。但随着数据量增加，这种优势逐渐减弱，在大数据量下两者性能接近。」


## 2. batch_size 测试

在确定了 CSV 格式的优势后，我们进一步探索了批处理大小（`batch_size`）对性能的影响。

**我**：「007，在实际应用中，我们通常会批量处理数据。批处理大小会对性能产生什么影响？」

**007**：「这是个很好的问题。批处理大小太小会导致频繁的网络通信和序列化/反序列化操作，增加开销；批处理大小太大则可能导致内存压力和响应延迟。我们需要找到一个平衡点。」

### 测试代码

我们设计了一个新的测试，固定总数据量为 100 万条记录，测试不同批处理大小（1、10、100、1000、10000）下的性能表现，007 提供的代码如下：

```python
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

### 局部优化测试代码的运行速度
在训练过程中，我们发现 `batch_size = 1` 时，测试代码运行的速度会非常慢。经过对代码的解读，主要影响到运行速度的是代码中的 `benchmark_redis_operations` 函数的准备批次数据的部分，具体是下面的代码：

```python
# 准备批次数据
dfs = []
for i in range(0, len(df), batch_size):
    dfs.append(df.iloc[i:i+batch_size])
```

我们考虑到的优化方法：<font color=red>直接使用 df 进行测试，不再构造 dfs</font>。

![](https://images.jieyu.ai/images/2025/05/batch_size_developped.png)

注意到，这里我们测试了两种方法：

- `json_str = self.serialize_json(df.iloc[i:i+batch_size])` ：速度慢，推送 1000 条的时间约为 0.7065s
- `json_str = df.iloc[i:i+batch_size].to_json()`：速度较快，推送 1000 条的时间约为 0.2415s

所以我们采用了第二种 `to_json` 的方式来加速我们的测试进度。同理，`to_csv` 也采用了类似的方式（但是我们不用修改代码，因为原代码 `serialize_csv` 函数中已经使用了 `to_csv` ）。

### 测试结果分析

测试结果显示，批处理大小对性能有显著影响。

| 批处理大小 | JSON LPUSH时间(ms) | CSV LPUSH时间(ms) | JSON RPOP时间(ms) | CSV RPOP时间(ms) | JSON LPUSH(ops/s) | CSV LPUSH(ops/s) | JSON RPOP(ops/s) | CSV RPOP(ops/s) |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|-----------------|
| 1        | 186,223.97       | 547,001.14       | 1,017,224.69     | 663,153.29       | 5,369.88         | 1,828.15         | 983.07           | 1,507.95        |
| 10       | 24,913.60        | 68,968.42        | 105,345.91       | 68,332.99        | 40,138.72        | 14,499.39        | 9,492.54         | 14,634.22       |
| 100      | 3,629.02         | 15,537.92        | 15,147.84        | 8,599.99         | 275,556.49       | 64,358.69        | 66,016.02        | 116,279.23      |
| 1000     | 2,734.42         | 7,085.08         | 5,951.21         | 2,141.66         | 365,708.00       | 141,141.63       | 168,033.05       | 466,927.74      |
| 10000    | 2,243.54         | 5,408.75         | 4,156.64         | 1,104.85         | 445,723.73       | 184,885.67       | 240,578.88       | 905,102.93      |

批处理的 Redis 操作（LPUSH 和 RPOP+反序列化）的操作数对比：

![](https://images.jieyu.ai/images/2025/05/batch_size_ops_benchmark.png)

批处理的 Redis 操作（LPUSH 和 RPOP+反序列化）的时间对比：

![](https://images.jieyu.ai/images/2025/05/batch_size_time_benchmark.png)

批处理大小对性能的影响：

![](https://images.jieyu.ai/images/2025/05/batch_size_optimal_benchmark.png)

> **007**：「从测试结果来看，批处理大小为 <font color=red>10000</font> 时，系统性能达到最佳。这是因为这个大小在网络通信开销和内存压力之间取得了良好的平衡。」
>
> **我**：「有趣的是，当批处理大小超过 <font color=red>10000</font> 后，性能开始下降。这可能是因为太大的批处理会增加内存压力和序列化/反序列化的时间。」
>
> **007**：「是的，而且我们还发现，无论批处理大小如何，CSV 格式在所有测试中都保持了对 JSON 的性能优势，特别是在读取操作（RPOP+反序列化）方面。」


## 总结：数据传输的艺术与科学

通过这一系列的测试和优化，我和 007 一起深入探索了数据传输的艺术与科学。我们的发现可以总结为以下几点：

1. **格式选择**：在固定结构的数据传输场景中，CSV 格式比 JSON 更高效，特别是在数据大小和反序列化性能方面。

2. **批处理大小**：批处理大小对性能有显著影响，在我们的测试中，<font color=red>10000</font> 条记录的批处理大小提供了最佳性能。

> **我**：「007，这次的优化真的让我大开眼界。数据传输看似简单，实际上蕴含着丰富的优化空间。」
>
> **007**：「是的，Boss。在量化交易系统中，毫秒级的性能提升可能意味着巨大的竞争优势。通过选择合适的数据格式和批处理大小，我们可以显著提升系统性能。」
>
> **我**：「而且，我们的发现不仅适用于 SQEP，也可以应用到其他需要高效数据传输的系统中。」
>
> **007**：「没错！数据传输的优化是一门艺术，也是一门科学。它需要理论分析，也需要实际测试。通过两者的结合，我们找到了最适合我们系统的解决方案。」

在量化交易的世界里，性能就是金钱。通过这次 SQEP 的再优化，我们不仅提升了系统性能，也加深了对数据传输本质的理解。正如 007 所说，这是一场关于毫秒和字节的较量，而我们，已经找到了制胜之道。

![](https://images.jieyu.ai/images/2025/05/quantide3.jpg)