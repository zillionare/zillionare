---
title: "How to Store 1B Symbols: SQEP Protocol & Encoding Benchmarks"
date: 2025-05-14
slug: en/posts/tools/21天驯化AI打工仔/4_Symbol编码的性能测试
tags: [Data Engineering, Quant Infrastructure, Database Optimization, SQEP]
excerpt: "Designing a universal data exchange format (SQEP) and optimizing stock code encoding can significantly boost query performance. This article details the protocol, implementation, and benchmarking results for high-frequency quant systems."
lang: en
translation_of: posts/tools/21天驯化AI打工仔/4_Symbol编码的性能测试
auto_translated: true
source_sha: a18a2da6e97347245460b3a55f564b1f9cb8fb7f
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png"
---

Now, we need to design a universal data exchange format, the Standard Quotes Exchange Protocol (SQEP). The workflow is straightforward: data producers (who understand the raw data formats best) convert data into this standard format and push it to Redis for consumers to process.

---

## Preface
On Day 1, we discussed how to fetch OHLC (Open, High, Low, Close) data and adjustment factors (`adj_factor`) from Tushare. At that time, our stored data structure looked like this:

```python
{
    "timestamp": "Timestamp",
    "ts_code": "Stock Code",
    "ohlc": {
        "ts_code": "Stock Code",
        "open": "Open Price",
        "high": "High Price",
        "low": "Low Price",
        "close": "Close Price",
        "vol": "Volume"
    }, 
    "adj_factor": {
        "ts_code": "Stock Code",
        "trade_date": "Trade Date",
        "adj_factor": "Adjustment Factor"
    }
}
```

Now, we need to design a universal data exchange format, the Standard Quotes Exchange Protocol (SQEP). The workflow is straightforward: data producers (who understand the raw data formats best) convert data into this standard format and push it to Redis for consumers to process.

## 1. SQEP-BAR-DAY Data Exchange Format for Daily Data

SQEP-BAR-DAY is the format specification within the Standard Quotes Exchange Protocol (SQEP) for daily stock data. It is designed for efficient transmission and processing of daily stock data across different system components, ensuring data consistency and interoperability.

### 1.1. Field Definitions

SQEP-BAR-DAY includes the following standard fields:

| Field Name | Data Type | Description |
| ---------- | ------------- | ------------------------------------ |
| symbol     | str/int       | Stock code. Integer encoding is recommended for performance. |
| frame      | datetime.date | Trade date                             |
| open       | float64       | Open price                               |
| high       | float64       | High price                               |
| low        | float64       | Low price                               |
| close      | float64       | Close price                               |
| vol        | float64       | Volume                               |
| amount     | float64       | Turnover (Amount)                               |
| adjust     | float64       | Adjustment factor                             |
| st         | bool          | Whether it is an ST stock (optional extension)         |
| buy_limit  | float64       | Price limit up (optional extension)               |
| sell_limit | float64       | Price limit down (optional extension)               |

### 1.2. Encoding Conventions

1. **Field Naming**: Use `frame` instead of `date` or `timestamp`, as the latter two may not be suitable as column names in certain databases.

2. **Stock Code Encoding**: To improve query performance, it is recommended to convert string-format stock codes to integers:
   - Shanghai Stock Exchange: 000001.SH → 1000001
   - Shenzhen Stock Exchange: 000001.SZ → 2000001
   
   This encoding method can support up to 9 different exchanges (digits 1-9, with 0 not usable as a prefix).

### 1.3. Use Cases

SQEP-BAR-DAY is primarily applied in:

1. Data producers (such as Tushare, QMT, etc.) converting raw data into a standard format.
2. Transmission between system components via middleware like Redis.
3. Data consumers (such as analysis engines, backtesting systems) processing standard format data.
4. Storing data in time-series databases like ClickHouse for long-term preservation.

### 1.4. Code Implementation by 007

With the data exchange format for daily data defined, 007 can now design the code implementation.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_01.png)

007 has provided two code files (`sqep_bar_day_producer.py` and `sqep_bar_day_consumer.py`), which can run normally after minor modifications.

```python
import redis
import tushare as ts
import json
from datetime import datetime
from typing import List, Dict, Tuple, Any, Union

# Tushare and Redis Configuration
TUSHARE_TOKEN = "YOUR TOKEN"
REDIS_HOST = "Your Redis Host"
REDIS_PORT = 6379
REDIS_PASSWORD = "Redis Password"  # Added Redis password
REDIS_QUEUE_NAME = "sqep_bar_day_queue"

# Initialize connections
pro = ts.pro_api(TUSHARE_TOKEN)
redis_client = redis.StrictRedis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD,  # Use password for authentication
    decode_responses=True
)

def encode_symbol(symbol: str) -> int:
    """Convert string-format stock code to integer encoding
    
    Args:
        symbol: Stock code, e.g., '000001.SZ' or '600519.SH'
        
    Returns:
        Integer-encoded stock code, e.g., 2000001 or 1600519
    """
    code, exchange = symbol.split('.')
    code = code.lstrip('0')  # Remove leading zeros, but keep at least one digit
    if not code:
        code = '0'
        
    if exchange.upper() == 'SH':
        prefix = '1'
    elif exchange.upper() == 'SZ':
        prefix = '2'
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")
        
    return int(prefix + code)

def fetch_daily_data(ts_code: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Fetch daily data and convert to SQEP-BAR-DAY format
    
    Args:
        ts_code: Stock code
        start_date: Start date, format YYYYMMDD
        end_date: End date, format YYYYMMDD
        
    Returns:
        List of data in SQEP-BAR-DAY format
    """
    try:
        # Fetch OHLC data
        df_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        # Fetch adjustment factors
        df_adj = pro.adj_factor(ts_code=ts_code, start_date=start_date, end_date=end_date)
        adj_dict = {row['trade_date']: row['adj_factor'] for _, row in df_adj.iterrows()}
        
        # Fetch price limits (if advanced API permissions are available)
        try:
            df_limit = pro.limit_list(ts_code=ts_code, start_date=start_date, end_date=end_date)
            limit_dict = {row['trade_date']: (row['up_limit'], row['down_limit']) 
                         for _, row in df_limit.iterrows()}
        except:
            limit_dict = {}
        
        # Fetch ST status (if advanced API permissions are available)
        try:
            df_namechange = pro.namechange(ts_code=ts_code, start_date=start_date, end_date=end_date)
            st_dict = {row['start_date']: '*' in row['name'] or 'ST' in row['name'] 
                      for _, row in df_namechange.iterrows()}
        except:
            st_dict = {}
        
        # Convert to SQEP-BAR-DAY format
        sqep_data = []
        for _, row in df_daily.iterrows():
            trade_date = row['trade_date']
            
            # Convert date format
            frame = datetime.strptime(trade_date, '%Y%m%d').date().isoformat()
            
            # Convert stock code
            symbol = encode_symbol(ts_code)
            
            # Create basic SQEP record
            sqep_record = {
                'symbol': symbol,
                'frame': frame,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'vol': float(row['vol']),
                'amount': float(row.get('amount', 0)),
                'adjust': float(adj_dict.get(trade_date, 1.0))
            }
            
            # Add optional fields (if available)
            if trade_date in limit_dict:
                sqep_record['buy_limit'] = float(limit_dict[trade_date][0])
                sqep_record['sell_limit'] = float(limit_dict[trade_date][1])
                
            if trade_date in st_dict:
                sqep_record['st'] = st_dict[trade_date]
                
            sqep_data.append(sqep_record)
            
        return sqep_data
    
    except Exception as e:
        print(f"Failed to fetch daily data: {str(e)}")
        return []

def produce_sqep_data(ts_code_list: List[str], date_range: Tuple[str, str]):
    """Produce SQEP-BAR-DAY data and push to Redis
    
    Args:
        ts_code_list: List of stock codes
        date_range: Date range tuple (start_date, end_date)
    """
    start_date, end_date = date_range
    
    for ts_code in ts_code_list:
        # Fetch and convert data
        sqep_data = fetch_daily_data(ts_code, start_date, end_date)
        
        if not sqep_data:
            print(f"No data fetched for {ts_code}")
            continue
        
        # Create data package
        data_package = {
            "timestamp": datetime.now().isoformat(),
            "source": "tushare",
            "data_type": "SQEP-BAR-DAY",
            "records": sqep_data
        }
        
        # Push to Redis
        redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(data_package))
        print(f"Pushed SQEP-BAR-DAY data: {ts_code} - {start_date} to {end_date} ({len(sqep_data)} records)")

if __name__ == "__main__":
    # Example parameters
    STOCK_CODES = ["000001.SZ", "600519.SH"]
    DATE_RANGE = ("20230101", "20231231")
    
    produce_sqep_data(STOCK_CODES, DATE_RANGE)
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_02.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_03.png)

```python
import redis
import json
from clickhouse_driver import Client
from datetime import datetime
from typing import Dict, List, Any

# Configuration Parameters
REDIS_HOST = "8.217.201.221"
REDIS_PORT = 16379
REDIS_PASSWORD = "quantide666"  # Added Redis password
REDIS_QUEUE_NAME = "sqep_bar_day_queue"

CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DB = "default"

# Initialize Redis and ClickHouse clients
redis_client = redis.StrictRedis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD,  # Use password for authentication
    decode_responses=True
)
clickhouse_client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DB)

def create_sqep_table_if_not_exists():
    """Create SQEP-BAR-DAY table if it does not exist"""
    query = """
    CREATE TABLE IF NOT EXISTS sqep_bar_day (
        symbol Int32,
        frame Date,
        open Float64,
        high Float64,
        low Float64,
        close Float64,
        vol Float64,
        amount Float64,
        adjust Float64,
        st UInt8 DEFAULT 0,
        buy_limit Float64 DEFAULT 0,
        sell_limit Float64 DEFAULT 0
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(frame)
    ORDER BY (symbol, frame);
    """
    clickhouse_client.execute(query)
    print("Ensured SQEP-BAR-DAY table exists")

def decode_symbol(encoded_symbol: int) -> str:
    """Convert integer-encoded stock code back to string format
    
    Args:
        encoded_symbol: Integer-encoded stock code, e.g., 2000001
        
    Returns:
        String-format stock code, e.g., '000001.SZ'
    """
    encoded_str = str(encoded_symbol)
    prefix = encoded_str[0]
    code = encoded_str[1:]
    
    # Pad with zeros to 6 digits
    code = code.zfill(6)
    
    if prefix == '1':
        exchange = 'SH'
    elif prefix == '2':
        exchange = 'SZ'
    else:
        raise ValueError(f"Unsupported exchange prefix: {prefix}")
        
    return f"{code}.{exchange}"

def insert_to_clickhouse(data_package: Dict[str, Any]):
    """Insert SQEP-BAR-DAY data into ClickHouse
    
    Args:
        data_package: Data package containing SQEP-BAR-DAY records
    """
    records = data_package["records"]
    if not records:
        return 0
    
    # Prepare insertion data
    values = []
    for record in records:
        # Prepare basic fields
        row = (
            record["symbol"],
            datetime.fromisoformat(record["frame"]).date(),
            record["open"],
            record["high"],
            record["low"],
            record["close"],
            record["vol"],
            record["amount"],
            record["adjust"],
            int(record.get("st", False)),
            record.get("buy_limit", 0.0),
            record.get("sell_limit", 0.0)
        )
        values.append(row)
    
    # Execute insertion
    query = """
    INSERT INTO sqep_bar_day (
        symbol, frame, open, high, low, close, vol, amount, adjust, st, buy_limit, sell_limit
    ) VALUES
    """
    
    clickhouse_client.execute(query, values)
    return len(values)

def consume_sqep_data():
    """Consume SQEP-BAR-DAY data"""
    # Ensure table exists
    create_sqep_table_if_not_exists()
    
    print("Starting SQEP-BAR-DAY data consumer, waiting for queue data...")
    while True:
        try:
            # Blocking fetch queue data
            result = redis_client.brpop(REDIS_QUEUE_NAME, timeout=1)
            if result is None:
                # If no data fetched, queue is empty, exit loop
                print("Redis queue is empty, stopping data consumption.")
                break
            
            _, json_data = result
            data_package = json.loads(json_data)
            
            # Check data type
            if data_package.get("data_type") != "SQEP-BAR-DAY":
                print(f"Skipping non-SQEP-BAR-DAY data: {data_package.get('data_type')}")
                continue
            
            # Insert data
            inserted_count = insert_to_clickhouse(data_package)
            
            # Get the stock code of the first record for display
            if data_package["records"]:
                first_symbol = data_package["records"][0]["symbol"]
                symbol_str = decode_symbol(first_symbol)
                print(f"Successfully inserted SQEP-BAR-DAY data: {symbol_str} ({inserted_count} records)")
            else:
                print("No records in data package")
                
        except Exception as e:
            print(f"Data processing exception: {str(e)}")
            continue

def query_sqep_data(symbol: str, start_date: str, end_date: str):
    """Query SQEP-BAR-DAY data
    
    Args:
        symbol: Stock code, e.g., '000001.SZ'
        start_date: Start date, format YYYY-MM-DD
        end_date: End date, format YYYY-MM-DD
        
    Returns:
        List of query results
    """
    # Encode stock code
    code, exchange = symbol.split('.')
    code = code.lstrip('0')
    if not code:
        code = '0'
        
    if exchange.upper() == 'SH':
        prefix = '1'
    elif exchange.upper() == 'SZ':
        prefix = '2'
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")
        
    encoded_symbol = int(prefix + code)
    
    # Execute query
    query = f"""
    SELECT 
        symbol, frame, open, high, low, close, vol, amount, adjust, 
        st, buy_limit, sell_limit
    FROM sqep_bar_day
    WHERE symbol = {encoded_symbol} AND frame BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY frame
    """
    
    result = clickhouse_client.execute(query)
    
    # Convert results
    columns = [
        'symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 
        'amount', 'adjust', 'st', 'buy_limit', 'sell_limit'
    ]
    
    return [dict(zip(columns, row)) for row in result]

if __name__ == "__main__":
    consume_sqep_data()
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_04.png)



### 1.5. Performance Testing of Stock Code Encoding Methods on Queries

Next, we will design an experiment to test the impact of stock code encoding methods on query performance. This experiment will compare the query performance differences between string format and integer-encoded format under different data volumes.

# JSON vs CSV: Benchmarking Data Exchange for SQEP-BAR-MINITE

Benchmarking JSON and CSV formats for SQEP-BAR-MINITE data reveals JSON’s superior decoding speed and ease of use, despite a consistent ~2.3x size overhead compared to CSV.

factor-investing, quantitative-trading, data-engineering, benchmarking

## 2. Data Exchange Formats for SQEP-BAR-MINITE Minute Bars

As with the previous section, this format excludes adjustment factors. This design ensures that consumer-side code remains unchanged regardless of the data source used in the future. Here, 007 and I design a performance test to compare the performance differences between two data exchange formats: JSON (with keys) and CSV (without keys).

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_07.png)

### 2.1. Test Methodology

```python
import time
import json
import csv
import io
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple
import os

from matplotlib import font_manager
font_path = 'SimHei.ttf'  # Replace with the actual path to SimHei.ttf
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'SimHei'

class DataFormatBenchmark:
    """SQEP Data Format Performance Test: JSON vs CSV"""
    
    def __init__(self):
        """Initialize benchmark"""
        # Define SQEP-BAR-DAY field order (required for CSV format)
        self.field_order = [
            'symbol', 'frame', 'open', 'high', 'low', 
            'close', 'vol', 'amount', 'adjust'
        ]
    
    def generate_test_data(self, num_records: int) -> List[Dict[str, Any]]:
        """Generate test data
        
        Args:
            num_records: Number of records
            
        Returns:
            List of records containing test data
        """
        data = []
        
        # Generate stock codes - ensure at least 1 stock
        num_symbols = max(1, min(num_records // 252, 5000))
        symbols = []
        for i in range(num_symbols):
            exchange = 'SH' if i % 2 == 0 else 'SZ'
            symbols.append(f"{str(i).zfill(6)}.{exchange}")
        
        # Generate date range - ensure at least 1 day
        days_needed = max(1, num_records // len(symbols))
        start_date = pd.Timestamp('2020-01-01')
        dates = [start_date + pd.Timedelta(days=i) for i in range(min(days_needed, 365))]
        
        # Generate data
        for symbol in symbols:
            for date in dates:
                if len(data) >= num_records:
                    break
                    
                open_price = random.uniform(10, 100)
                high = open_price * random.uniform(1, 1.1)
                low = open_price * random.uniform(0.9, 1)
                close = random.uniform(low, high)
                
                data.append({
                    'symbol': symbol,
                    'frame': date.strftime('%Y-%m-%d'),
                    'open': round(open_price, 2),
                    'high': round(high, 2),
                    'low': round(low, 2),
                    'close': round(close, 2),
                    'vol': round(random.uniform(10000, 1000000), 0),
                    'amount': round(random.uniform(1000000, 100000000), 0),
                    'adjust': round(random.uniform(0.8, 1.2), 4)
                })
        
        return data[:num_records]
    
    def encode_json(self, data: List[Dict[str, Any]]) -> str:
        """Encode data as JSON format
        
        Args:
            data: List of records
            
        Returns:
            JSON string
        """
        return json.dumps({
            "timestamp": pd.Timestamp.now().isoformat(),
            "source": "benchmark",
            "data_type": "SQEP-BAR-DAY",
            "records": data
        })
    
    def decode_json(self, json_str: str) -> List[Dict[str, Any]]:
        """Decode JSON string to data
        
        Args:
            json_str: JSON string
            
        Returns:
            List of records
        """
        data = json.loads(json_str)
        return data["records"]
    
    def encode_csv(self, data: List[Dict[str, Any]]) -> str:
        """Encode data as CSV format
        
        Args:
            data: List of records
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write metadata row
        writer.writerow([
            pd.Timestamp.now().isoformat(),
            "benchmark",
            "SQEP-BAR-DAY",
            len(data)
        ])
        
        # Write data rows
        for record in data:
            row = [record[field] for field in self.field_order]
            writer.writerow(row)
        
        return output.getvalue()
    
    def decode_csv(self, csv_str: str) -> List[Dict[str, Any]]:
        """Decode CSV string to data
        
        Args:
            csv_str: CSV string
            
        Returns:
            List of records
        """
        input_file = io.StringIO(csv_str)
        reader = csv.reader(input_file)
        
        # Read metadata row
        metadata = next(reader)
        timestamp, source, data_type, num_records = metadata
        
        # Read data rows
        records = []
        for row in reader:
            record = {field: value for field, value in zip(self.field_order, row)}
            
            # Convert data types
            record['open'] = float(record['open'])
            record['high'] = float(record['high'])
            record['low'] = float(record['low'])
            record['close'] = float(record['close'])
            record['vol'] = float(record['vol'])
            record['amount'] = float(record['amount'])
            record['adjust'] = float(record['adjust'])
            
            records.append(record)
        
        return records
    
    def run_encoding_benchmark(self, data: List[Dict[str, Any]], num_iterations: int = 100) -> Tuple[float, float]:
        """Run encoding benchmark
        
        Args:
            data: Test data
            num_iterations: Number of iterations
            
        Returns:
            Average encoding time (milliseconds) for JSON and CSV
        """
        json_times = []
        csv_times = []
        
        for _ in range(num_iterations):
            # Test JSON encoding
            start_time = time.time()
            json_str = self.encode_json(data)
            json_times.append(time.time() - start_time)
            
            # Test CSV encoding
            start_time = time.time()
            csv_str = self.encode_csv(data)
            csv_times.append(time.time() - start_time)
        
        # Calculate average time (milliseconds)
        json_avg = np.mean(json_times) * 1000
        csv_avg = np.mean(csv_times) * 1000
        
        return json_avg, csv_avg
    
    def run_decoding_benchmark(self, data: List[Dict[str, Any]], num_iterations: int = 100) -> Tuple[float, float]:
        """Run decoding benchmark
        
        Args:
            data: Test data
            num_iterations: Number of iterations
            
        Returns:
            Average decoding time (milliseconds) for JSON and CSV
        """
        # Encode data first
        json_str = self.encode_json(data)
        csv_str = self.encode_csv(data)
        
        json_times = []
        csv_times = []
        
        for _ in range(num_iterations):
            # Test JSON decoding
            start_time = time.time()
            self.decode_json(json_str)
            json_times.append(time.time() - start_time)
            
            # Test CSV decoding
            start_time = time.time()
            self.decode_csv(csv_str)
            csv_times.append(time.time() - start_time)
        
        # Calculate average time (milliseconds)
        json_avg = np.mean(json_times) * 1000
        csv_avg = np.mean(csv_times) * 1000
        
        return json_avg, csv_avg
    
    def measure_size(self, data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """Measure encoded data size
        
        Args:
            data: Test data
            
        Returns:
            Byte size of JSON and CSV
        """
        json_str = self.encode_json(data)
        csv_str = self.encode_csv(data)
        
        return len(json_str.encode('utf-8')), len(csv_str.encode('utf-8'))
    
    def run_full_benchmark(self, data_sizes: List[int], num_iterations: int = 100):
        """Run full benchmark
        
        Args:
            data_sizes: List of record counts to test
            num_iterations: Number of iterations per test
        """
        results = {
            'data_size': [],
            'json_encode_time': [],
            'csv_encode_time': [],
            'json_decode_time': [],
            'csv_decode_time': [],
            'json_size': [],
            'csv_size': []
        }
        
        for size in data_sizes:
            print(f"Testing data volume: {size} records")
            
            # Generate test data
            data = self.generate_test_data(size)
            
            # Run encoding test
            json_encode_time, csv_encode_time = self.run_encoding_benchmark(data, num_iterations)
            
            # Run decoding test
            json_decode_time, csv_decode_time = self.run_decoding_benchmark(data, num_iterations)
            
            # Measure data size
            json_size, csv_size = self.measure_size(data)
            
            # Record results
            results['data_size'].append(size)
            results['json_encode_time'].append(json_encode_time)
            results['csv_encode_time'].append(csv_encode_time)
            results['json_decode_time'].append(json_decode_time)
            results['csv_decode_time'].append(csv_decode_time)
            results['json_size'].append(json_size)
            results['csv_size'].append(csv_size)
            
            print(f"  Encoding Time - JSON: {json_encode_time:.2f}ms, CSV: {csv_encode_time:.2f}ms")
            print(f"  Decoding Time - JSON: {json_decode_time:.2f}ms, CSV: {csv_decode_time:.2f}ms")
            print(f"  Data Size - JSON: {json_size/1024:.2f}KB, CSV: {csv_size/1024:.2f}KB")
            print(f"  Performance Comparison - Encoding: JSON/CSV = {json_encode_time/csv_encode_time:.2f}x, Decoding: JSON/CSV = {json_decode_time/csv_decode_time:.2f}x")
            print(f"  Size Comparison - JSON/CSV = {json_size/csv_size:.2f}x")
            print()
        
        # Plot result charts
        self._plot_results(results)
        
        return results
    
    def _plot_results(self, results: dict):
        """Plot test result charts
        
        Args:
            results: Dictionary of test results
        """
        plt.figure(figsize=(15, 12))
        
        # Encoding Time Comparison
        plt.subplot(3, 2, 1)
        plt.plot(results['data_size'], results['json_encode_time'], 'o-', label='JSON')
        plt.plot(results['data_size'], results['csv_encode_time'], 'o-', label='CSV')
        plt.title('Encoding Time Comparison')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Average Encoding Time (ms)')
        plt.legend()
        plt.grid(True)
        
        # Decoding Time Comparison
        plt.subplot(3, 2, 2)
        plt.plot(results['data_size'], results['json_decode_time'], 'o-', label='JSON')
        plt.plot(results['data_size'], results['csv_decode_time'], 'o-', label='CSV')
        plt.title('Decoding Time Comparison')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Average Decoding Time (ms)')
        plt.legend()
        plt.grid(True)
        
        # Data Size Comparison
        plt.subplot(3, 2, 3)
        plt.plot(results['data_size'], [s/1024 for s in results['json_size']], 'o-', label='JSON')
        plt.plot(results['data_size'], [s/1024 for s in results['csv_size']], 'o-', label='CSV')
        plt.title('Data Size Comparison')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Data Size (KB)')
        plt.legend()
        plt.grid(True)
        
        # Performance Ratios
        plt.subplot(3, 2, 4)
        encode_ratio = [j/c for j, c in zip(results['json_encode_time'], results['csv_encode_time'])]
        decode_ratio = [j/c for j, c in zip(results['json_decode_time'], results['csv_decode_time'])]
        size_ratio = [j/c for j, c in zip(results['json_size'], results['csv_size'])]
        
        plt.plot(results['data_size'], encode_ratio, 'o-', label='Encoding Time Ratio (JSON/CSV)')
        plt.plot(results['data_size'], decode_ratio, 'o-', label='Decoding Time Ratio (JSON/CSV)')
        plt.plot(results['data_size'], size_ratio, 'o-', label='Size Ratio (JSON/CSV)')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.title('JSON/CSV Performance Ratios')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Ratio (JSON/CSV)')
        plt.legend()
        plt.grid(True)
        
        # Total Processing Time (Encoding + Decoding)
        plt.subplot(3, 2, 5)
        json_total = [e + d for e, d in zip(results['json_encode_time'], results['json_decode_time'])]
        csv_total = [e + d for e, d in zip(results['csv_encode_time'], results['csv_decode_time'])]
        plt.plot(results['data_size'], json_total, 'o-', label='JSON')
        plt.plot(results['data_size'], csv_total, 'o-', label='CSV')
        plt.title('Total Processing Time (Encoding + Decoding)')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Total Time (ms)')
        plt.legend()
        plt.grid(True)
        
        # Performance on Log Scale
        plt.subplot(3, 2, 6)
        plt.loglog(results['data_size'], results['json_encode_time'], 'o-', label='JSON Encoding')
        plt.loglog(results['data_size'], results['csv_encode_time'], 'o-', label='CSV Encoding')
        plt.loglog(results['data_size'], results['json_decode_time'], 'o-', label='JSON Decoding')
        plt.loglog(results['data_size'], results['csv_decode_time'], 'o-', label='CSV Decoding')
        plt.title('Performance vs Data Volume (Log Scale)')
        plt.xlabel('Data Volume (Record Count)')
        plt.ylabel('Time (ms)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('data_format_benchmark.png')
        plt.close()


if __name__ == "__main__":
    # Run benchmark
    benchmark = DataFormatBenchmark()
    
    # Test different data volumes
    data_sizes = [100, 500, 1000, 5000, 10000, 50000]
    results = benchmark.run_full_benchmark(data_sizes)
    
    # Output summary
    print("Test Summary:")
    print(f"Data Volume Range: {min(results['data_size'])} - {max(results['data_size'])} records")
    
    # Calculate average ratios
    avg_encode_ratio = np.mean([j/c for j, c in zip(results['json_encode_time'], results['csv_encode_time'])])
    avg_decode_ratio = np.mean([j/c for j, c in zip(results['json_decode_time'], results['csv_decode_time'])])
    avg_size_ratio = np.mean([j/c for j, c in zip(results['json_size'], results['csv_size'])])
    
    print(f"Encoding Time Ratio (JSON/CSV): {avg_encode_ratio:.2f}x")
    print(f"Decoding Time Ratio (JSON/CSV): {avg_decode_ratio:.2f}x")
    print(f"Data Size Ratio (JSON/CSV): {avg_size_ratio:.2f}x")
    
    print("\nTest complete. Results saved to data_format_benchmark.png")
```

This performance testing scheme comprehensively compares the performance differences between JSON (with keys) and CSV (without keys) data exchange formats across different data volumes. The main test contents include:

1. **Test Content**
   The testing scheme includes three main comparative aspects:
   - **Encoding Performance**: The speed of converting data structures into strings.
   - **Decoding Performance**: The speed of parsing strings back into data structures.
   - **Data Size**: The space occupied by the encoded data.

2. **Test Data**
   - Generate SQEP-BAR-DAY records of varying quantities (from 100 to 50,000 records).
   - Each record contains complete daily stock data fields.
   - Data content simulates real trading data.

3. **Data Format Implementation**
   1) **JSON Format**:
      - Contains complete field names (keys).
      - Uses standard JSON structure, including metadata and a record array.
      - Example:
      ```json
      {
        "timestamp": "2023-05-01T12:00:00",
        "source": "benchmark",
        "data_type": "SQEP-B

# SQEP Format Performance: JSON vs. CSV in Quant Systems

This article details a comparative performance analysis of JSON and CSV data formats in quantitative trading systems, highlighting the efficiency gains and storage trade-offs observed during a 21-day AI collaboration challenge.

## Summary

In this chapter, my AI assistant, 007, and I delved into the performance implications of data exchange formats within quantitative trading systems. This "Data Format Showdown" not only yielded critical technical benchmarks but also demonstrated the boundless potential of human-AI collaboration.

007 proved to be an indispensable partner, operating at full capacity. It designed a comprehensive testing protocol and swiftly resolved a division-by-zero error when it arose. Through our joint efforts, we successfully benchmarked JSON and CSV across varying data volumes: JSON demonstrated a slight edge in processing speed, while CSV offered superior storage efficiency.

This test represents a significant technical milestone and another achievement in our 21-day challenge to train our AI assistant. Much like the test data, our collaboration scales seamlessly—from 100 records to 50,000—maintaining consistent efficiency. This stability mirrors the robustness of our partnership.

As 007 aptly stated, "Data is the foundation of everything," and our collaboration is the source of innovation. Looking ahead to the SQEP extended format exploration, we look forward to continuing our work with 007, injecting more intelligence into quantitative trading systems.

## Next Steps: Exploring SQEP Extended Formats

Moving forward, 007 and I will continue our exploration of two critical extended formats for SQEP:

1.  **SQEP-ST: Data Format for Special Treatment (ST) Stocks**
    *   While information on ST stocks is sparse, it is crucial for investment decisions.
    *   We will intelligently integrate ST data into the existing SQEP-BAR-DAY table.
    *   By introducing a boolean `st` field, the system can rapidly identify special treatment stocks.

2.  **Price Limit Information: Key Indicators for Trading Constraints**
    *   We will add `buy_limit` and `sell_limit` fields to provide precise trading constraints for the backtest engine.
    *   This data enables us to simulate real-world trading rules accurately.
    *   Ensuring backtest results closely mirror live trading environments.

With these extensions, our quantitative trading system will become more robust, capable of handling more complex market scenarios. As 007 has demonstrated, clear logic and appropriate methods can solve even complex data processing challenges. Let us continue this exciting 21-day challenge, creating new possibilities through data and intelligence.
