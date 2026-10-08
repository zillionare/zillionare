---
title: "SQEP Performance Optimization: 21 Days to Tame the AI Workforce"
date: 2025-05-18
slug: en/posts/tools/21天驯化AI打工仔/5_SQEP再优化
tags: [Quantitative Trading, System Optimization, Data Serialization, SQEP]
excerpt: "Optimizing data transmission in quantitative trading is critical. This article details benchmarking JSON vs. CSV formats and batch sizes for SQEP to eliminate bottlenecks."
lang: en
translation_of: posts/tools/21天驯化AI打工仔/5_SQEP再优化
auto_translated: true
source_sha: 94a39891b84e1b1c6e6a25927c6ac11a6d0af842
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png"
---

In the world of quantitative trading, data is the blood, and the data transmission system is the vascular network. An efficient data transmission system empowers the entire quantitative trading platform, whereas inefficiency becomes a critical bottleneck.

As I was struggling to optimize the performance of SQEP (Standard Quotes Exchange Protocol), my AI assistant, 007, knocked on my "virtual door."

## Preface: The Art of Data Transmission

**Me**: "007, our SQEP system requires further optimization. We need to decide between JSON and CSV formats and determine the optimal batch size. Do you have any suggestions?"

**007**: "Boss, that’s my specialty! Choosing the data transmission format and optimizing batch sizes are key to enhancing system performance. I recommend we conduct a series of benchmarks and let the data speak."

**Me**: "Sounds good. Let’s start by analyzing the performance differences between JSON and CSV formats."

**007**: "No problem! I’ve prepared the test plan. We will evaluate multiple dimensions, including serialization, deserialization, and Redis operations, to comprehensively assess the performance of both formats."

Thus began our journey of data transmission optimization—a battle measured in milliseconds and bytes...

# JSON vs CSV: Benchmarks for Minute-Level K-Line Data

Benchmarking JSON and CSV formats for minute-level K-line data in quantitative trading systems reveals CSV’s superior efficiency in size and deserialization speed.

Tags: Quantitative Trading, Data Serialization, Performance Benchmarking, Redis

## 1. SQEP-BAR-MINUTE JSON and CSV Performance Tests

In quantitative trading systems, minute-level K-line data (BAR-MINUTE) is a critical data source. Compared to daily data, minute bars lack adjustment factors, but their basic structure remains similar.

Our first question is: Should we use JSON format (with keys) or CSV format (without keys) to transmit this data?

> **Me**: "007, I’m wondering, since SQEP is a fixed-structure protocol with a fixed field order, maybe we don’t need to include field names (keys) in every record?"
>
> **007**: "That’s a great question! Theoretically, CSV should save more space because it doesn’t repeat field names. However, JSON’s advantage lies in its flexibility and self-descriptiveness. We need to determine which format is more efficient in our specific scenario through practical testing."

### Pre-Test Analysis

We decided to design a comprehensive benchmark to compare the performance of JSON and CSV across several dimensions:
1. Serialization speed
2. Deserialization speed
3. Data size
4. Redis operation performance (LPUSH and RPOP)

To ensure fairness, we used the same data structure containing the following fields:

| Field Name | Data Type | Description                                                                                         |
| ---------- | --------- | --------------------------------------------------------------------------------------------------- |
| symbol     | int       | Stock code. Integer encoding is used to improve performance (see previous chapter on str vs. int).    |
| frame      | datetime.date | Trading date                                                                                      |
| open       | float64   | Opening price                                                                                       |
| high       | float64   | Highest price                                                                                       |
| low        | float64   | Lowest price                                                                                        |
| close      | float64   | Closing price                                                                                       |
| vol        | float64   | Trading volume                                                                                      |
| amount     | float64   | Trading amount                                                                                      |

!!! tip Note
    SQEP-BAR-MINUTE does not include adjustment factors compared to SQEP-BAR-DAY.

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

# Configuration parameters
BATCH_SIZE = 1000     # Batch size
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "RedisPassword"
REDIS_DB = 0
REDIS_QUEUE_JSON = 'benchmark:json:no_metadata'
REDIS_QUEUE_CSV = 'benchmark:csv:no_metadata'

class NoMetadataBenchmark:
    """Performance comparison benchmark for JSON and CSV formats (no metadata row)"""

    def __init__(self):
        """Initialize the benchmark"""
        # Set field order according to the required data structure
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # Ensure output directory exists
        os.makedirs('results', exist_ok=True)
```

> **007**: "I’ve designed the test framework. We will use the `fast_json` library for JSON data and `pandas` for CSV data."
>
> **Me**: "Why choose `fast_json` over Python’s built-in `json` library?"
>
> **007**: "The `fast_json` library performs better with large datasets, especially in serialization and deserialization operations. In quantitative trading systems, performance is key, so we should choose the most efficient tool."

We first implemented the data generation function to ensure test data matches real-world scenarios; then we ran comprehensive benchmarks testing performance across different data volumes (from 100 to 10,000 records). 007 provided the complete code below:

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
font_path = '/Volumes/share/data/WBQ/temp/SimHei.ttf'  # Replace with actual path to SimHei.ttf
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'SimHei'

# Configuration parameters
BATCH_SIZE = 1000     # Batch size
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "quantide666"  # Redis password
REDIS_DB = 0
REDIS_QUEUE_JSON = 'benchmark:json:no_metadata'
REDIS_QUEUE_CSV = 'benchmark:csv:no_metadata'

class NoMetadataBenchmark:
    """Performance comparison benchmark for JSON and CSV formats (no metadata row)"""

    def __init__(self):
        """Initialize the benchmark"""
        # Set field order according to the required data structure
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # Ensure output directory exists
        os.makedirs('results', exist_ok=True)

    def generate_dataframe(self, num_records: int) -> pd.DataFrame:
        """Generate test pandas DataFrame conforming to the specified data structure

        Args:
            num_records: Number of records

        Returns:
            pandas DataFrame
        """
        # Generate stock codes (six-digit integers starting with 1 or 2)
        # Generate 1 or 2 as the first digit
        first_digits = np.random.choice([1, 2], num_records)
        # Generate remaining 5 digits (range 00000-99999)
        remaining_digits = np.random.randint(0, 100000, num_records)
        # Combine into six-digit integers
        symbols = first_digits * 100000 + remaining_digits

        # Generate trading dates (datetime.date type)
        base_date = datetime.now().date()
        frame_dates = []
        for i in range(num_records):
            # Randomly generate dates within the past 100 days
            days_ago = np.random.randint(0, 100)
            date = base_date - timedelta(days=days_ago)
            frame_dates.append(date)

        # Generate base prices
        base_prices = np.random.uniform(10, 100, num_records)

        # Generate high and low prices
        high_prices = base_prices * (1 + np.random.uniform(0, 0.05, num_records))
        low_prices = base_prices * (1 - np.random.uniform(0, 0.05, num_records))

        # Generate opening and closing prices
        open_prices = np.random.uniform(low_prices, high_prices)
        close_prices = np.random.uniform(low_prices, high_prices)

        # Generate trading volume and amount
        volumes = np.random.uniform(10000, 1000000, num_records)
        amounts = np.random.uniform(100000, 10000000, num_records)

        # Generate adjustment factors
        adjust_factors = np.random.uniform(0.9, 1.1, num_records)

        # Create DataFrame, ensuring data types meet requirements
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
        """JSON serialization (using fast_json, with keys, no metadata)

        Args:
            df: pandas DataFrame

        Returns:
            JSON string
        """
        # Create a copy of the DataFrame to avoid modifying the original data
        df_copy = df.copy()

        # Convert dates to strings
        if 'frame' in df_copy.columns:
            df_copy['frame'] = df_copy['frame'].astype(str)

        # Convert DataFrame to list of records
        records = df_copy.to_dict('records')

        # Serialize record list directly, without adding metadata
        return fast_json.dumps(records)

    def deserialize_json(self, json_str: str) -> pd.DataFrame:
        """JSON deserialization (using fast_json, with keys, no metadata)

        Args:
            json_str: JSON string

        Returns:
            pandas DataFrame
        """
        # Parse directly into list of records
        records = fast_json.loads(json_str)
        df = pd.DataFrame(records)

        # Convert string dates back to datetime.date objects
        if 'frame' in df.columns:
            df['frame'] = pd.to_datetime(df['frame']).dt.date

        return df

    def serialize_csv(self, df: pd.DataFrame) -> str:
        """CSV serialization (using pandas, no keys, no metadata)

        Args:
            df: pandas DataFrame

        Returns:
            CSV string
        """
        # Ensure consistent column order
        if not df.empty:
            df = df[self.field_order]

        # Convert to CSV string (excluding index and column names)
        output = io.StringIO()
        df.to_csv(output, index=False, header=False)
        return output.getvalue()

    def deserialize_csv(self, csv_str: str) -> pd.DataFrame:
        """CSV deserialization (using pandas, no keys, no metadata)

        Args:
            csv_str: CSV string

        Returns:
            pandas DataFrame
        """
        # Read CSV string into DataFrame (no column names)
        df = pd.read_csv(io.StringIO(csv_str), header=None, names=self.field_order)
        return df

    def benchmark_serialization(self, df: pd.DataFrame, iterations: int = 10) -> Dict[str, float]:
        """Serialization performance test

        Args:
            df: pandas DataFrame
            iterations: Number of iterations

        Returns:
            Test results
        """
        results = {
            'json_time': 0,
            'csv_time': 0,
            'json_size': 0,
            'csv_size': 0
        }

        # JSON serialization test
        json_times = []
        for _ in range(iterations):
            start_time = time.time()
            json_str = self.serialize_json(df)
            json_times.append(time.time() - start_time)

        results['json_time'] = sum(json_times) / iterations * 1000  # milliseconds
        results['json_size'] = len(json_str.encode('utf-8'))

        # CSV serialization test
        csv_times = []
        for _ in range(iterations):
            start_time = time.time()
            csv_str = self.serialize_csv(df)
            csv_times.append(time.time() - start_time)

        results['csv_time'] = sum(csv_times) / iterations * 1000  # milliseconds
        results['csv_size'] = len(csv_str.encode('utf-8'))

        return results

    def benchmark_deserialization(self, df: pd.DataFrame, iterations: int = 10) -> Dict[str, float]:
        """Deserialization performance test

        Args:
            df: pandas DataFrame
            iterations: Number of iterations

        Returns:
            Test results
        """
        # Serialize data first
        json_str = self.serialize_json(df)
        csv_str = self.serialize_csv(df)

        results = {
            'json_time': 0,
            'csv_time': 0
        }

        # JSON deserialization test
        json_times = []
        for _ in range(iterations):
            start_time = time.time()
            self.deserialize_json(json_str)
            json_times.append(time.time() - start_time)

        results['json_time'] = sum(json_times) / iterations * 1000  # milliseconds

        # CSV deserialization test
        csv_times = []
        for _ in range(iterations):
            start_time = time.time()
            self.deserialize_csv(csv_str)
            csv_times.append(time.time() - start_time)

        results['csv_time'] = sum(csv_times) / iterations * 1000  # milliseconds

        return results

    def benchmark_redis_operations(self, df: pd.DataFrame, iterations: int = 5) -> Dict[str, float]:
        """Redis operation performance test

        Args:
            df: pandas DataFrame
            iterations: Number of iterations

        Returns:
            Test results
        """
        results = {
            'json_push_time': 0,
            'csv_push_time': 0,
            'json_pop_time': 0,
            'csv_pop_time': 0
        }

        # Clear queues
        self.redis_client.delete(REDIS_QUEUE_JSON)
        self.redis_client.delete(REDIS_QUEUE_CSV)

        # Prepare batch data
        dfs = []
        for i in range(0, len(df), BATCH_SIZE):
            dfs.append(df.iloc[i:i+BATCH_SIZE])

        # JSON LPUSH test
        json_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_JSON)
            start_time = time.time()

            for batch_df in dfs:
                json_str = self.serialize_json(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            json_push_times.append(time.time() - start_time)

        results['json_push_time'] = sum(json_push_times) / iterations * 1000  # milliseconds

        # CSV LPUSH test - using direct string formatting
        csv_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_CSV)
            start_time = time.time()

            for batch_df in dfs:
                # Serialize DataFrame directly to CSV, no metadata row
                csv_str = self.serialize_csv(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            csv_push_times.append(time.time() - start_time)

        results['csv_push_time'] = sum(csv_push_times) / iterations * 1000  # milliseconds

        # JSON RPOP test
        json_pop_times = []
        for _ in range(iterations):
            # Ensure queue has data
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

        results['json_pop_time'] = sum(json_pop_times) / iterations * 1000  # milliseconds

        # CSV RPOP test
        csv_pop_times = []
        for _ in range(iterations):
            # Ensure queue has data
            if self.redis_client.llen(REDIS_QUEUE_CSV) == 0:
                for batch_df in dfs:
                    # Serialize DataFrame directly to CSV, no metadata row
                    csv_str = self.serialize_csv(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_CSV) > 0:
                csv_str = self.redis_client.rpop(REDIS_QUEUE_CSV)
                if csv_str:
                    self.deserialize_csv(csv_str)

            csv_pop_times.append(time.time() - start_time)

        results['csv_pop_time'] = sum(csv_pop_times) / iterations * 1000  # milliseconds

        return results

    def run_benchmark(self, data_sizes: List[int], iterations: int = 10):
        """Run complete benchmark test

        Args:
            data_sizes: List of record counts to test
            iterations: Number of iterations per test
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
            print(f"Testing data volume: {size} records")

            # Generate test data
            print(f"  Generating DataFrame for {size} records...")
            df = self.generate_dataframe(size)
            print(f"  Successfully generated DataFrame, shape: {df.shape}")

            # Serialization test
            ser_results = self.benchmark_serialization(df, iterations)
            print(f"  Serialization time - JSON(fast_json): {ser_results['json_time']:.2f}ms, CSV(pandas): {ser_results['csv_time']:.2f}ms")
            print(f"  Data size - JSON: {ser_results['json_size']/1024:.2f}KB, CSV: {ser_results['csv_size']/1024:.2f}KB")

            # Deserialization test
            deser_results = self.benchmark_deserialization(df, iterations)
            print(f"  Deserialization time - JSON(fast_json): {deser_results['json_time']:.2f}ms, CSV(pandas): {deser

# Optimizing Batch Size for High-Throughput Quant Data Pipelines

Benchmarking batch sizes reveals that 10,000 records optimize throughput, balancing network latency and memory pressure while CSV consistently outperforms JSON in serialization efficiency.

## 2. Batch Size Testing

Having established the advantages of CSV format, we further explored the impact of batch size (`batch_size`) on performance.

**Me**: "007, in practical applications, we typically process data in batches. How does batch size affect performance?"

**007**: "That’s an excellent question. If the batch size is too small, frequent network communication and serialization/deserialization operations increase overhead. If it’s too large, it may cause memory pressure and response latency. We need to find a balance."

### Test Code

We designed a new test fixing the total data volume at 1 million records, testing performance under different batch sizes (1, 10, 100, 1,000, 10,000). The code provided by 007 is as follows:

```python
# Total data volume
TOTAL_RECORDS = 1000000

class BatchSizeBenchmark:
    """Benchmark comparing JSON and CSV format performance under different batch sizes"""

    def run_batch_size_benchmark(self, batch_sizes: List[int], iterations: int = 3):
        """Run benchmarks for different batch sizes"""
        results = {
            'batch_size': [],
            'json_push_time': [],
            'csv_push_time': [],
            'json_pop_time': [],
            'csv_pop_time': [],
            'json_push_ops': [],  # Operations per second
            'csv_push_ops': [],
            'json_pop_ops': [],
            'csv_pop_ops': []
        }

        # Generate test data
        df = self.generate_dataframe(TOTAL_RECORDS)

        for batch_size in batch_sizes:
            print(f"\nTesting batch size: {batch_size}")

            # Redis operation tests
            redis_results = self.benchmark_redis_operations(df, batch_size, iterations)

            # Calculate operations per second
            json_push_ops = TOTAL_RECORDS / (redis_results['json_push_time'] / 1000)
            csv_push_ops = TOTAL_RECORDS / (redis_results['csv_push_time'] / 1000)
            json_pop_ops = TOTAL_RECORDS / (redis_results['json_pop_time'] / 1000)
            csv_pop_ops = TOTAL_RECORDS / (redis_results['csv_pop_time'] / 1000)

            # Record results
            results['batch_size'].append(batch_size)
            results['json_push_time'].append(redis_results['json_push_time'])
            results['csv_push_time'].append(redis_results['csv_push_time'])
            results['json_pop_time'].append(redis_results['json_pop_time'])
            results['csv_pop_time'].append(redis_results['csv_pop_time'])
            results['json_push_ops'].append(json_push_ops)
            results['csv_push_ops'].append(csv_push_ops)
            results['json_pop_ops'].append(json_pop_ops)
            results['csv_pop_ops'].append(csv_pop_ops)

        # Plot results
        self._plot_results(results)

        return results

class BatchSizeBenchmark:
    """Benchmark comparing JSON and CSV format performance under different batch sizes"""

    def __init__(self):
        """Initialize benchmark"""
        # Set field order according to required data structure
        self.field_order = ['symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 'amount', 'adjust']
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        # Ensure output directory exists
        os.makedirs('results', exist_ok=True)

    def generate_dataframe(self, num_records: int) -> pd.DataFrame:
        """Generate pandas DataFrame for testing, conforming to specified data structure

        Args:
            num_records: Number of records

        Returns:
            pandas DataFrame
        """
        # Generate stock codes (six-digit integers starting with 1 or 2)
        # Generate 1 or 2 as the first digit
        first_digits = np.random.choice([1, 2], num_records)
        # Generate remaining 5 digits (range 00000-99999)
        remaining_digits = np.random.randint(0, 100000, num_records)
        # Combine into six-digit integers
        symbols = first_digits * 100000 + remaining_digits

        # Generate trading dates (datetime.date type)
        base_date = datetime.now().date()
        frame_dates = []
        for i in range(num_records):
            # Randomly generate dates within the past 100 days
            days_ago = np.random.randint(0, 100)
            date = base_date - timedelta(days=days_ago)
            frame_dates.append(date)

        # Generate base prices
        base_prices = np.random.uniform(10, 100, num_records)

        # Generate high and low prices
        high_prices = base_prices * (1 + np.random.uniform(0, 0.05, num_records))
        low_prices = base_prices * (1 - np.random.uniform(0, 0.05, num_records))

        # Generate open and close prices
        open_prices = np.random.uniform(low_prices, high_prices)
        close_prices = np.random.uniform(low_prices, high_prices)

        # Generate volume and amount
        volumes = np.random.uniform(10000, 1000000, num_records)
        amounts = np.random.uniform(100000, 10000000, num_records)

        # Generate adjustment factors
        adjust_factors = np.random.uniform(0.9, 1.1, num_records)

        # Create DataFrame, ensuring data types meet requirements
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
        """JSON serialization (using fast_json, with keys, no metadata)

        Args:
            df: pandas DataFrame

        Returns:
            JSON string
        """
        # Create a copy of DataFrame to avoid modifying original data
        df_copy = df.copy()

        # Convert dates to strings
        if 'frame' in df_copy.columns:
            df_copy['frame'] = df_copy['frame'].astype(str)

        # Convert DataFrame to list of records
        records = df_copy.to_dict('records')

        # Serialize record list directly, without adding metadata
        return fast_json.dumps(records)

    def deserialize_json(self, json_str: str) -> pd.DataFrame:
        """JSON deserialization (using fast_json, with keys, no metadata)

        Args:
            json_str: JSON string

        Returns:
            pandas DataFrame
        """
        # Parse directly into list of records
        records = fast_json.loads(json_str)
        df = pd.DataFrame(records)

        # Convert string dates back to datetime.date objects
        if 'frame' in df.columns:
            df['frame'] = pd.to_datetime(df['frame']).dt.date

        return df

    def serialize_csv(self, df: pd.DataFrame) -> str:
        """CSV serialization (using pandas, no keys, no metadata)

        Args:
            df: pandas DataFrame

        Returns:
            CSV string
        """
        # Ensure consistent column order
        if not df.empty:
            df = df[self.field_order]

        # Convert to CSV string (excluding index and column names)
        output = io.StringIO()
        df.to_csv(output, index=False, header=False)
        return output.getvalue()

    def deserialize_csv(self, csv_str: str) -> pd.DataFrame:
        """CSV deserialization (using pandas, no column names)

        Args:
            csv_str: CSV string

        Returns:
            pandas DataFrame
        """
        # Read CSV string into DataFrame (no column names)
        df = pd.read_csv(io.StringIO(csv_str), header=None, names=self.field_order)
        return df

    def benchmark_redis_operations(self, df: pd.DataFrame, batch_size: int, iterations: int = 3) -> Dict[str, float]:
        """Redis operation performance test

        Args:
            df: pandas DataFrame
            batch_size: Batch size
            iterations: Number of iterations

        Returns:
            Test results
        """
        results = {
            'json_push_time': 0,
            'csv_push_time': 0,
            'json_pop_time': 0,
            'csv_pop_time': 0
        }

        # Clear queues
        self.redis_client.delete(REDIS_QUEUE_JSON)
        self.redis_client.delete(REDIS_QUEUE_CSV)

        # Prepare batch data
        dfs = []
        for i in range(0, len(df), batch_size):
            dfs.append(df.iloc[i:i+batch_size])

        # JSON LPUSH test
        json_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_JSON)
            start_time = time.time()

            for batch_df in dfs:
                json_str = self.serialize_json(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_JSON, json_str)

            json_push_times.append(time.time() - start_time)

        results['json_push_time'] = sum(json_push_times) / iterations * 1000  # milliseconds

        # CSV LPUSH test
        csv_push_times = []
        for _ in range(iterations):
            self.redis_client.delete(REDIS_QUEUE_CSV)
            start_time = time.time()

            for batch_df in dfs:
                # Serialize DataFrame directly to CSV, no metadata rows
                csv_str = self.serialize_csv(batch_df)
                self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            csv_push_times.append(time.time() - start_time)

        results['csv_push_time'] = sum(csv_push_times) / iterations * 1000  # milliseconds

        # JSON RPOP test
        json_pop_times = []
        for _ in range(iterations):
            # Ensure queue has data
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

        results['json_pop_time'] = sum(json_pop_times) / iterations * 1000  # milliseconds

        # CSV RPOP test
        csv_pop_times = []
        for _ in range(iterations):
            # Ensure queue has data
            if self.redis_client.llen(REDIS_QUEUE_CSV) == 0:
                for batch_df in dfs:
                    # Serialize DataFrame directly to CSV, no metadata rows
                    csv_str = self.serialize_csv(batch_df)
                    self.redis_client.lpush(REDIS_QUEUE_CSV, csv_str)

            start_time = time.time()

            while self.redis_client.llen(REDIS_QUEUE_CSV) > 0:
                csv_str = self.redis_client.rpop(REDIS_QUEUE_CSV)
                if csv_str:
                    self.deserialize_csv(csv_str)

            csv_pop_times.append(time.time() - start_time)

        results['csv_pop_time'] = sum(csv_pop_times) / iterations * 1000  # milliseconds

        return results

    def run_batch_size_benchmark(self, batch_sizes: List[int], iterations: int = 3):
        """Run benchmarks for different batch sizes

        Args:
            batch_sizes: List of batch sizes to test
            iterations: Number of iterations per test
        """
        results = {
            'batch_size': [],
            'json_push_time': [],
            'csv_push_time': [],
            'json_pop_time': [],
            'csv_pop_time': [],
            'json_push_ops': [],  # Operations per second
            'csv_push_ops': [],
            'json_pop_ops': [],
            'csv_pop_ops': []
        }

        # Generate test data
        print(f"Generating DataFrame with {TOTAL_RECORDS} records...")
        df = self.generate_dataframe(TOTAL_RECORDS)
        print(f"Successfully generated DataFrame, shape: {df.shape}")

        for batch_size in batch_sizes:
            print(f"\nTesting batch size: {batch_size}")

            # Redis operation tests
            redis_results = self.benchmark_redis_operations(df, batch_size, iterations)

            # Calculate operations per second
            json_push_ops = TOTAL_RECORDS / (redis_results['json_push_time'] / 1000)  # Records per second
            csv_push_ops = TOTAL_RECORDS / (redis_results['csv_push_time'] / 1000)
            json_pop_ops = TOTAL_RECORDS / (redis_results['json_pop_time'] / 1000)
            csv_pop_ops = TOTAL_RECORDS / (redis_results['csv_pop_time'] / 1000)

            print(f"  Redis LPUSH time - JSON: {redis_results['json_push_time']:.2f}ms, CSV: {redis_results['csv_push_time']:.2f}ms")
            print(f"  Redis RPOP+Deserialization time - JSON: {redis_results['json_pop_time']:.2f}ms, CSV: {redis_results['csv_pop_time']:.2f}ms")
            print(f"  Operations per second - JSON LPUSH: {json_push_ops:.2f} ops/s, CSV LPUSH: {csv_push_ops:.2f} ops/s")
            print(f"  Operations per second - JSON RPOP: {json_pop_ops:.2f} ops/s, CSV RPOP: {csv_pop_ops:.2f} ops/s")

            # Calculate ratios
            push_ratio = redis_results['json_push_time'] / redis_results['csv_push_time']
            pop_ratio = redis_results['json_pop_time'] / redis_results['csv_pop_time']

            print(f"  Redis comparison - LPUSH: JSON/CSV = {push_ratio:.2f}x, RPOP+Deserialization: JSON/CSV = {pop_ratio:.2f}x")

            # Record results
            results['batch_size'].append(batch_size)
            results['json_push_time'].append(redis_results['json_push_time'])
            results['csv_push_time'].append(redis_results['csv_push_time'])
            results['json_pop_time'].append(redis_results['json_pop_time'])
            results['csv_pop_time'].append(redis_results['csv_pop_time'])
            results['json_push_ops'].append(json_push_ops)
            results['csv_push_ops'].append(csv_push_ops)
            results['json_pop_ops'].append(json_pop_ops)
            results['csv_pop_ops'].append(csv_pop_ops)

        # Plot results
        self._plot_results(results)

        return results

    def _plot_results(self, results):
        """Plot result charts

        Args:
            results: Test results
        """
        # Create DataFrame
        df = pd.DataFrame(results)

        # Save as CSV
        df.to_csv('results/batch_size_benchmark.csv', index=False)

        # Plot Redis operation time comparison
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        plt.plot(results['batch_size'], results['json_push_time'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_push_time'], 'r-', label='CSV')
        plt.xlabel('Batch Size')
        plt.ylabel('Time (ms)')
        plt.title('Redis LPUSH Time Comparison')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # Use logarithmic scale

        plt.subplot(2, 2, 2)
        plt.plot(results['batch_size'], results['json_pop_time'], 'b-', label='JSON')
        plt.plot(results['batch_size'], results['csv_pop_time'], 'r-', label='CSV')
        plt.xlabel('Batch Size')
        plt.ylabel('Time (ms)')
        plt.title('Redis RPOP+Deserialization Time Comparison')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')  # Use logarithmic scale

        plt.subplot(2, 2, 3)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_push_time'], results['csv_push_time'])], 'g-')
        plt.xlabel('Batch Size')
        plt.ylabel('Ratio (JSON/CSV)')
        plt.title('Redis LPUSH Time Ratio (JSON/CSV)')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # Use logarithmic scale

        plt.subplot(2, 2, 4)
        plt.plot(results['batch_size'], [j/c for j, c in zip(results['json_pop_time'], results['csv_pop_time'])], 'g-')
        plt.xlabel('Batch Size')
        plt.ylabel('Ratio (JSON/CSV)')
        plt.title('Redis RPOP+Deserialization Time Ratio (JSON/CSV)')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.grid(True)
        plt.xscale('log')  # Use logarithmic scale

        plt.tight_layout()
        plt.savefig('results/batch_size_time_benchmark.png')

        # Plot operations per second comparison
        plt.figure(figsize=(15,

# SQEP Data Transfer: Balancing Art and Science

Optimizing SQEP’s data transfer via format selection and batch sizing reveals critical performance gains. This case study demonstrates how precise engineering choices drive competitive advantages in quantitative trading systems.

**Tags:** Data Engineering, Quantitative Trading, System Optimization, Performance Tuning

## Conclusion: The Art and Science of Data Transfer

Through this series of tests and optimizations, 007 and I have delved into the art and science of data transfer. Our findings can be summarized as follows:

1. **Format Selection:** In scenarios involving structured data transmission, CSV is more efficient than JSON, particularly regarding data size and deserialization performance.

2. **Batch Size:** Batch size significantly impacts performance. Our tests indicated that a batch size of <font color=red>10,000</font> records yielded optimal performance.

> **Me:** "007, these optimizations have truly opened my eyes. Data transfer seems simple, but it holds substantial room for optimization."
>
> **007:** "Indeed, Boss. In quantitative trading systems, millisecond-level performance gains can translate into significant competitive advantages. By selecting the appropriate data format and batch size, we can substantially enhance system performance."
>
> **Me:** "Moreover, our findings are not limited to SQEP; they can be applied to other systems requiring efficient data transmission."
>
> **007:** "Exactly! Optimizing data transfer is both an art and a science. It requires theoretical analysis as well as practical testing. By combining both, we identified the solution best suited for our system."

In the world of quantitative trading, performance equals money. Through this re-optimization of SQEP, we have not only improved system performance but also deepened our understanding of the essence of data transfer. As 007 noted, this is a contest measured in milliseconds and bytes—and we have found the winning strategy.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/quantide3.jpg)
