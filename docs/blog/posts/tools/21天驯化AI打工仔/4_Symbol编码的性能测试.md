---
title: 21天驯化AI打工仔 - 如何存储10亿个Symbol?
slug: Taming-the-AI-Worker-in-21-Days-4
date: 2025-05-14
category: tools
motto: You only live once, but if you do it right, once is enough
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514202750.png
tags: 
    - tools
    - programming
---

现在，我们需要设计一种通用的数据交换格式（Standard Quotes Exchange Protocol, SQEP）。这种格式的工作原理是：由数据生产者（因为只有生产者才了解原始数据的具体格式）将数据转换为这种标准格式，然后再将其推送到Redis中供消费者使用。

---

## 前言
第一天，我们讨论了如何从Tushare获取OHLC(开盘价、最高价、最低价、收盘价)数据和调整因子(adj_factor)。当时我们存储的数据结构如下：

```python
{
    "timestamp": "时间戳",
    "ts_code": "股票代码",
    "ohlc": {
        "ts_code": "股票代码",
        "open": "开盘价",
        "high": "最高价",
        "low": "最低价",
        "close": "收盘价",
        "vol": "成交量"
    }, 
    "adj_factor": {
        "ts_code": "股票代码",
        "trade_date": "交易日期",
        "adj_factor": "复权因子"
    }
}
```

现在，我们需要设计一种通用的数据交换格式（Standard Quotes Exchange Protocol, SQEP）。这种格式的工作原理是：由数据生产者（因为只有生产者才了解原始数据的具体格式）将数据转换为这种标准格式，然后再将其推送到Redis中供消费者使用。

## 1. SQEP-BAR-DAY 日线场景下的数据交换格式

SQEP-BAR-DAY 是标准行情交换协议(Standard Quotes Exchange Protocol)中用于日线数据的格式规范。该格式设计用于在不同系统组件间高效传输和处理股票日线数据，确保数据的一致性和互操作性。

### 1.1. 字段定义

SQEP-BAR-DAY 包含以下标准字段：

| 字段名     | 数据类型      | 说明                                 |
| ---------- | ------------- | ------------------------------------ |
| symbol     | str/int       | 股票代码。推荐使用整型编码以提高性能 |
| frame      | datetime.date | 交易日期                             |
| open       | float64       | 开盘价                               |
| high       | float64       | 最高价                               |
| low        | float64       | 最低价                               |
| close      | float64       | 收盘价                               |
| vol        | float64       | 成交量                               |
| amount     | float64       | 成交额                               |
| adjust     | float64       | 复权因子                             |
| st         | bool          | 是否为ST股票（可选扩展字段）         |
| buy_limit  | float64       | 涨停价（可选扩展字段）               |
| sell_limit | float64       | 跌停价（可选扩展字段）               |

### 1.2. 编码约定

1. **字段命名**：使用`frame`而非`date`或`timestamp`，因为后两者在某些数据库中不适合作为列名。

2. **股票代码编码**：为提高查询性能，推荐将字符串格式的股票代码转换为整型：
   - 上海证券交易所：000001.SH → 1000001
   - 深圳证券交易所：000001.SZ → 2000001
   
   这种编码方式最多可支持9个不同交易所（数字1-9，0不能用作前缀）。

### 1.3. 使用场景

SQEP-BAR-DAY 主要应用于：

1. 数据生产者（如Tushare、QMT等数据源）将原始数据转换为标准格式
2. 通过Redis等中间件在系统组件间传输
3. 数据消费者（如分析引擎、回测系统）处理标准格式数据
4. 存储到ClickHouse等时序数据库中进行长期保存

### 1.4. 007 的代码实现

既然规定好了日线场景下的数据交换格式，就可以让 007 设计代码实现了。

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_01.png)

007 为我们提供了两个代码文件（`sqep_bar_day_producer.py`和`sqep_bar_day_consumer.py`），简单修改后可以正常运行。

```python
import redis
import tushare as ts
import json
from datetime import datetime
from typing import List, Dict, Tuple, Any, Union

# Tushare和Redis配置
TUSHARE_TOKEN = "YOUR TOKEN"
REDIS_HOST = "Your Redis Host"
REDIS_PORT = 6379
REDIS_PASSWORD = "Redis Password"  # 添加Redis密码
REDIS_QUEUE_NAME = "sqep_bar_day_queue"

# 初始化连接
pro = ts.pro_api(TUSHARE_TOKEN)
redis_client = redis.StrictRedis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD,  # 使用密码进行身份验证
    decode_responses=True
)

def encode_symbol(symbol: str) -> int:
    """将字符串格式的股票代码转换为整型编码
    
    Args:
        symbol: 股票代码，如 '000001.SZ' 或 '600519.SH'
        
    Returns:
        整型编码的股票代码，如 2000001 或 1600519
    """
    code, exchange = symbol.split('.')
    code = code.lstrip('0')  # 移除前导零，但保留至少一位数字
    if not code:
        code = '0'
        
    if exchange.upper() == 'SH':
        prefix = '1'
    elif exchange.upper() == 'SZ':
        prefix = '2'
    else:
        raise ValueError(f"不支持的交易所: {exchange}")
        
    return int(prefix + code)

def fetch_daily_data(ts_code: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """获取日线数据并转换为SQEP-BAR-DAY格式
    
    Args:
        ts_code: 股票代码
        start_date: 开始日期，格式为YYYYMMDD
        end_date: 结束日期，格式为YYYYMMDD
        
    Returns:
        SQEP-BAR-DAY格式的数据列表
    """
    try:
        # 获取OHLC数据
        df_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        # 获取复权因子
        df_adj = pro.adj_factor(ts_code=ts_code, start_date=start_date, end_date=end_date)
        adj_dict = {row['trade_date']: row['adj_factor'] for _, row in df_adj.iterrows()}
        
        # 获取涨跌停价格（如果有高级API权限）
        try:
            df_limit = pro.limit_list(ts_code=ts_code, start_date=start_date, end_date=end_date)
            limit_dict = {row['trade_date']: (row['up_limit'], row['down_limit']) 
                         for _, row in df_limit.iterrows()}
        except:
            limit_dict = {}
        
        # 获取ST状态（如果有高级API权限）
        try:
            df_namechange = pro.namechange(ts_code=ts_code, start_date=start_date, end_date=end_date)
            st_dict = {row['start_date']: '*' in row['name'] or 'ST' in row['name'] 
                      for _, row in df_namechange.iterrows()}
        except:
            st_dict = {}
        
        # 转换为SQEP-BAR-DAY格式
        sqep_data = []
        for _, row in df_daily.iterrows():
            trade_date = row['trade_date']
            
            # 转换日期格式
            frame = datetime.strptime(trade_date, '%Y%m%d').date().isoformat()
            
            # 转换股票代码
            symbol = encode_symbol(ts_code)
            
            # 创建基本SQEP记录
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
            
            # 添加可选字段（如果存在）
            if trade_date in limit_dict:
                sqep_record['buy_limit'] = float(limit_dict[trade_date][0])
                sqep_record['sell_limit'] = float(limit_dict[trade_date][1])
                
            if trade_date in st_dict:
                sqep_record['st'] = st_dict[trade_date]
                
            sqep_data.append(sqep_record)
            
        return sqep_data
    
    except Exception as e:
        print(f"获取日线数据失败: {str(e)}")
        return []

def produce_sqep_data(ts_code_list: List[str], date_range: Tuple[str, str]):
    """生产SQEP-BAR-DAY数据并推送到Redis
    
    Args:
        ts_code_list: 股票代码列表
        date_range: 日期范围元组 (start_date, end_date)
    """
    start_date, end_date = date_range
    
    for ts_code in ts_code_list:
        # 获取并转换数据
        sqep_data = fetch_daily_data(ts_code, start_date, end_date)
        
        if not sqep_data:
            print(f"未获取到 {ts_code} 的数据")
            continue
        
        # 创建数据包
        data_package = {
            "timestamp": datetime.now().isoformat(),
            "source": "tushare",
            "data_type": "SQEP-BAR-DAY",
            "records": sqep_data
        }
        
        # 推送到Redis
        redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(data_package))
        print(f"已推送SQEP-BAR-DAY数据: {ts_code} - {start_date}至{end_date} ({len(sqep_data)}条)")

if __name__ == "__main__":
    # 示例参数
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

# 配置参数
REDIS_HOST = "8.217.201.221"
REDIS_PORT = 16379
REDIS_PASSWORD = "quantide666"  # 添加Redis密码
REDIS_QUEUE_NAME = "sqep_bar_day_queue"

CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DB = "default"

# 初始化 Redis 和 ClickHouse 客户端
redis_client = redis.StrictRedis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD,  # 使用密码进行身份验证
    decode_responses=True
)
clickhouse_client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DB)

def create_sqep_table_if_not_exists():
    """创建SQEP-BAR-DAY表（如果不存在）"""
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
    print("已确保SQEP-BAR-DAY表存在")

def decode_symbol(encoded_symbol: int) -> str:
    """将整型编码的股票代码转换回字符串格式
    
    Args:
        encoded_symbol: 整型编码的股票代码，如 2000001
        
    Returns:
        字符串格式的股票代码，如 '000001.SZ'
    """
    encoded_str = str(encoded_symbol)
    prefix = encoded_str[0]
    code = encoded_str[1:]
    
    # 补齐6位数字
    code = code.zfill(6)
    
    if prefix == '1':
        exchange = 'SH'
    elif prefix == '2':
        exchange = 'SZ'
    else:
        raise ValueError(f"不支持的交易所前缀: {prefix}")
        
    return f"{code}.{exchange}"

def insert_to_clickhouse(data_package: Dict[str, Any]):
    """将SQEP-BAR-DAY数据插入到ClickHouse
    
    Args:
        data_package: 包含SQEP-BAR-DAY记录的数据包
    """
    records = data_package["records"]
    if not records:
        return 0
    
    # 准备插入数据
    values = []
    for record in records:
        # 准备基本字段
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
    
    # 执行插入
    query = """
    INSERT INTO sqep_bar_day (
        symbol, frame, open, high, low, close, vol, amount, adjust, st, buy_limit, sell_limit
    ) VALUES
    """
    
    clickhouse_client.execute(query, values)
    return len(values)

def consume_sqep_data():
    """消费SQEP-BAR-DAY数据"""
    # 确保表存在
    create_sqep_table_if_not_exists()
    
    print("启动SQEP-BAR-DAY数据消费者，等待队列数据...")
    while True:
        try:
            # 阻塞式获取队列数据
            result = redis_client.brpop(REDIS_QUEUE_NAME, timeout=1)
            if result is None:
                # 如果没有获取到数据，说明队列为空，退出循环
                print("Redis队列为空，停止消费数据。")
                break
            
            _, json_data = result
            data_package = json.loads(json_data)
            
            # 检查数据类型
            if data_package.get("data_type") != "SQEP-BAR-DAY":
                print(f"跳过非SQEP-BAR-DAY数据: {data_package.get('data_type')}")
                continue
            
            # 插入数据
            inserted_count = insert_to_clickhouse(data_package)
            
            # 获取第一条记录的股票代码用于显示
            if data_package["records"]:
                first_symbol = data_package["records"][0]["symbol"]
                symbol_str = decode_symbol(first_symbol)
                print(f"成功插入SQEP-BAR-DAY数据: {symbol_str} ({inserted_count}条)")
            else:
                print("数据包中没有记录")
                
        except Exception as e:
            print(f"数据处理异常: {str(e)}")
            continue

def query_sqep_data(symbol: str, start_date: str, end_date: str):
    """查询SQEP-BAR-DAY数据
    
    Args:
        symbol: 股票代码，如 '000001.SZ'
        start_date: 开始日期，格式为YYYY-MM-DD
        end_date: 结束日期，格式为YYYY-MM-DD
        
    Returns:
        查询结果列表
    """
    # 编码股票代码
    code, exchange = symbol.split('.')
    code = code.lstrip('0')
    if not code:
        code = '0'
        
    if exchange.upper() == 'SH':
        prefix = '1'
    elif exchange.upper() == 'SZ':
        prefix = '2'
    else:
        raise ValueError(f"不支持的交易所: {exchange}")
        
    encoded_symbol = int(prefix + code)
    
    # 执行查询
    query = f"""
    SELECT 
        symbol, frame, open, high, low, close, vol, amount, adjust, 
        st, buy_limit, sell_limit
    FROM sqep_bar_day
    WHERE symbol = {encoded_symbol} AND frame BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY frame
    """
    
    result = clickhouse_client.execute(query)
    
    # 转换结果
    columns = [
        'symbol', 'frame', 'open', 'high', 'low', 'close', 'vol', 
        'amount', 'adjust', 'st', 'buy_limit', 'sell_limit'
    ]
    
    return [dict(zip(columns, row)) for row in result]

if __name__ == "__main__":
    consume_sqep_data()
```

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_04.png)



### 1.5. 股票代码编码方式对查询的性能测试

接下来，我们将设计一个实验来测试股票代码编码方式对查询性能的影响。这个实验将比较字符串格式和整型编码格式在不同数据量下的查询性能差异。007 很 nice 地帮助我设计了一个实验方案：

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_05.png)

#### 1.5.1. 测试方案
```python
import time
import random
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from typing import List, Tuple
import os

from matplotlib import font_manager
font_path = 'SimHei.ttf'  # 替换为SimHei.ttf的实际路径
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'SimHei'

class SymbolEncodingBenchmark:
    """股票代码编码方式性能测试"""
    
    def __init__(self, db_path="symbol_benchmark.db"):
        """初始化基准测试
        
        Args:
            db_path: SQLite数据库文件路径
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # 创建测试表
        self._create_tables()
        
    def _create_tables(self):
        """创建测试表"""
        # 字符串格式表
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bar_day_str (
            symbol TEXT,
            frame TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            vol REAL,
            amount REAL,
            adjust REAL,
            PRIMARY KEY (symbol, frame)
        )
        """)
        
        # 整型编码表
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bar_day_int (
            symbol INTEGER,
            frame TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            vol REAL,
            amount REAL,
            adjust REAL,
            PRIMARY KEY (symbol, frame)
        )
        """)
        
        # 创建索引
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_str_symbol ON bar_day_str (symbol)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_int_symbol ON bar_day_int (symbol)")
        
        self.conn.commit()
    
    @staticmethod
    def encode_symbol(symbol: str) -> int:
        """将字符串格式的股票代码转换为整型编码"""
        code, exchange = symbol.split('.')
        code = code.lstrip('0')  # 移除前导零
        if not code:
            code = '0'
            
        if exchange.upper() == 'SH':
            prefix = '1'
        elif exchange.upper() == 'SZ':
            prefix = '2'
        else:
            raise ValueError(f"不支持的交易所: {exchange}")
            
        return int(prefix + code)
    
    def generate_test_data(self, num_symbols: int, days_per_symbol: int) -> pd.DataFrame:
        """生成测试数据
        
        Args:
            num_symbols: 股票数量
            days_per_symbol: 每只股票的交易日数量
            
        Returns:
            包含测试数据的DataFrame
        """
        # 生成股票代码
        sh_symbols = [f"{str(i).zfill(6)}.SH" for i in range(num_symbols // 2)]
        sz_symbols = [f"{str(i).zfill(6)}.SZ" for i in range(num_symbols // 2)]
        symbols = sh_symbols + sz_symbols
        
        # 生成日期范围
        start_date = pd.Timestamp('2020-01-01')
        dates = [start_date + pd.Timedelta(days=i) for i in range(days_per_symbol)]
        
        # 生成数据
        data = []
        for symbol in symbols:
            for date in dates:
                open_price = random.uniform(10, 100)
                high = open_price * random.uniform(1, 1.1)
                low = open_price * random.uniform(0.9, 1)
                close = random.uniform(low, high)
                
                data.append({
                    'symbol': symbol,
                    'frame': date.strftime('%Y-%m-%d'),
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'close': close,
                    'vol': random.uniform(10000, 1000000),
                    'amount': random.uniform(1000000, 100000000),
                    'adjust': random.uniform(0.8, 1.2)
                })
        
        return pd.DataFrame(data)
    
    def load_test_data(self, df: pd.DataFrame):
        """加载测试数据到数据库
        
        Args:
            df: 包含测试数据的DataFrame
        """
        # 清空表
        self.cursor.execute("DELETE FROM bar_day_str")
        self.cursor.execute("DELETE FROM bar_day_int")
        
        # 插入字符串格式数据
        for _, row in df.iterrows():
            self.cursor.execute(
                "INSERT INTO bar_day_str VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    row['symbol'],
                    row['frame'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close'],
                    row['vol'],
                    row['amount'],
                    row['adjust']
                )
            )
        
        # 插入整型编码数据
        for _, row in df.iterrows():
            encoded_symbol = self.encode_symbol(row['symbol'])
            self.cursor.execute(
                "INSERT INTO bar_day_int VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    encoded_symbol,
                    row['frame'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close'],
                    row['vol'],
                    row['amount'],
                    row['adjust']
                )
            )
        
        self.conn.commit()
    
    def run_query_benchmark(self, num_queries: int) -> Tuple[List[float], List[float]]:
        """运行查询基准测试
        
        Args:
            num_queries: 查询次数
            
        Returns:
            字符串格式和整型编码的查询时间列表
        """
        # 获取所有股票代码
        self.cursor.execute("SELECT DISTINCT symbol FROM bar_day_str")
        str_symbols = [row[0] for row in self.cursor.fetchall()]
        
        self.cursor.execute("SELECT DISTINCT symbol FROM bar_day_int")
        int_symbols = [row[0] for row in self.cursor.fetchall()]
        
        # 运行查询测试
        str_times = []
        int_times = []
        
        for _ in range(num_queries):
            # 随机选择一个股票代码
            str_symbol = random.choice(str_symbols)
            int_symbol = self.encode_symbol(str_symbol)
            
            # 测试字符串格式查询
            start_time = time.time()
            self.cursor.execute(
                "SELECT * FROM bar_day_str WHERE symbol = ?",
                (str_symbol,)
            )
            results = self.cursor.fetchall()
            str_times.append(time.time() - start_time)
            
            # 测试整型编码查询
            start_time = time.time()
            self.cursor.execute(
                "SELECT * FROM bar_day_int WHERE symbol = ?",
                (int_symbol,)
            )
            results = self.cursor.fetchall()
            int_times.append(time.time() - start_time)
        
        return str_times, int_times
    
    def run_range_query_benchmark(self, num_queries: int) -> Tuple[List[float], List[float]]:
        """运行范围查询基准测试
        
        Args:
            num_queries: 查询次数
            
        Returns:
            字符串格式和整型编码的查询时间列表
        """
        # 获取所有交易所
        exchanges = ['SH', 'SZ']
        
        # 运行查询测试
        str_times = []
        int_times = []
        
        for _ in range(num_queries):
            # 随机选择一个交易所
            exchange = random.choice(exchanges)
            
            # 测试字符串格式查询
            start_time = time.time()
            self.cursor.execute(
                "SELECT * FROM bar_day_str WHERE symbol LIKE ?",
                (f"%.{exchange}",)
            )
            results = self.cursor.fetchall()
            str_times.append(time.time() - start_time)
            
            # 测试整型编码查询
            prefix = 1 if exchange == 'SH' else 2
            start_time = time.time()
            self.cursor.execute(
                "SELECT * FROM bar_day_int WHERE symbol >= ? AND symbol < ?",
                (prefix * 1000000, (prefix + 1) * 1000000)
            )
            results = self.cursor.fetchall()
            int_times.append(time.time() - start_time)
        
        return str_times, int_times
    
    def run_full_benchmark(self, data_sizes: List[int], days_per_symbol: int = 252, num_queries: int = 100):
        """运行完整基准测试
        
        Args:
            data_sizes: 测试的股票数量列表
            days_per_symbol: 每只股票的交易日数量
            num_queries: 每次测试的查询次数
        """
        results = {
            'data_size': [],
            'str_query_avg': [],
            'int_query_avg': [],
            'str_range_avg': [],
            'int_range_avg': []
        }
        
        for size in data_sizes:
            print(f"测试数据量: {size}只股票 × {days_per_symbol}天 = {size * days_per_symbol}条记录")
            
            # 生成并加载测试数据
            df = self.generate_test_data(size, days_per_symbol)
            self.load_test_data(df)
            
            # 运行查询测试
            str_times, int_times = self.run_query_benchmark(num_queries)
            str_range_times, int_range_times = self.run_range_query_benchmark(num_queries)
            
            # 记录结果
            results['data_size'].append(size * days_per_symbol)
            results['str_query_avg'].append(np.mean(str_times) * 1000)  # 转换为毫秒
            results['int_query_avg'].append(np.mean(int_times) * 1000)
            results['str_range_avg'].append(np.mean(str_range_times) * 1000)
            results['int_range_avg'].append(np.mean(int_range_times) * 1000)
            
            print(f"  单条查询 - 字符串格式: {results['str_query_avg'][-1]:.2f}ms, 整型编码: {results['int_query_avg'][-1]:.2f}ms")
            print(f"  范围查询 - 字符串格式: {results['str_range_avg'][-1]:.2f}ms, 整型编码: {results['int_range_avg'][-1]:.2f}ms")
            print(f"  性能提升 - 单条查询: {(results['str_query_avg'][-1] / results['int_query_avg'][-1]):.2f}x, 范围查询: {(results['str_range_avg'][-1] / results['int_range_avg'][-1]):.2f}x")
            print()
        
        # 绘制结果图表
        self._plot_results(results)
        
        return results
    
    def _plot_results(self, results: dict):
        """绘制测试结果图表
        
        Args:
            results: 测试结果字典
        """
        plt.figure(figsize=(15, 10))
        
        # 单条查询性能对比
        plt.subplot(2, 2, 1)
        plt.plot(results['data_size'], results['str_query_avg'], 'o-', label='字符串格式')
        plt.plot(results['data_size'], results['int_query_avg'], 'o-', label='整型编码')
        plt.title('单条查询性能对比')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('平均查询时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        # 范围查询性能对比
        plt.subplot(2, 2, 2)
        plt.plot(results['data_size'], results['str_range_avg'], 'o-', label='字符串格式')
        plt.plot(results['data_size'], results['int_range_avg'], 'o-', label='整型编码')
        plt.title('范围查询性能对比')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('平均查询时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        # 性能提升比例
        plt.subplot(2, 2, 3)
        speedup_query = [s / i for s, i in zip(results['str_query_avg'], results['int_query_avg'])]
        speedup_range = [s / i for s, i in zip(results['str_range_avg'], results['int_range_avg'])]
        plt.plot(results['data_size'], speedup_query, 'o-', label='单条查询')
        plt.plot(results['data_size'], speedup_range, 'o-', label='范围查询')
        plt.title('整型编码性能提升比例')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('性能提升 (倍)')
        plt.legend()
        plt.grid(True)
        
        # 查询时间与数据量的关系
        plt.subplot(2, 2, 4)
        plt.loglog(results['data_size'], results['str_query_avg'], 'o-', label='字符串-单条')
        plt.loglog(results['data_size'], results['int_query_avg'], 'o-', label='整型-单条')
        plt.loglog(results['data_size'], results['str_range_avg'], 'o-', label='字符串-范围')
        plt.loglog(results['data_size'], results['int_range_avg'], 'o-', label='整型-范围')
        plt.title('查询时间与数据量关系 (对数坐标)')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('平均查询时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('symbol_encoding_benchmark.png')
        plt.close()
    
    def cleanup(self):
        """清理测试资源"""
        self.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


if __name__ == "__main__":
    # 运行基准测试
    benchmark = SymbolEncodingBenchmark()
    
    # 测试不同数据量
    data_sizes = [100, 500, 1000, 2000, 5000]
    results = benchmark.run_full_benchmark(data_sizes)
    
    # 输出总结
    print("测试总结:")
    print(f"数据量范围: {min(results['data_size'])} - {max(results['data_size'])}条记录")
    print(f"单条查询平均性能提升: {np.mean([s / i for s, i in zip(results['str_query_avg'], results['int_query_avg'])]):.2f}倍")
    print(f"范围查询平均性能提升: {np.mean([s / i for s, i in zip(results['str_range_avg'], results['int_range_avg'])]):.2f}倍")
    
    # 清理资源
    benchmark.cleanup()
    
    print("\n测试完成，结果已保存到 symbol_encoding_benchmark.png")
```

1. 测试环境
    - 使用SQLite数据库作为测试平台（易于部署且无需额外配置）
    - 创建两个表：`bar_day_str`（字符串格式）和 `bar_day_int`（整型编码）
    - 为两个表的 `symbol` 字段创建索引，确保公平比较
2. 测试数据
    - 生成不同数量的股票代码（上交所和深交所各半）
    - 为每只股票生成多天的交易数据
    - 数据量从小到大逐步增加（100到5000只股票）
3. 测试场景
    - 单条查询：根据特定股票代码查询所有交易记录
    - 范围查询：查询特定交易所的所有股票记录
4. 性能指标
    - 查询响应时间（毫秒）
    - 性能提升比例（字符串格式时间/整型编码时间）
5. 结果分析
    - 绘制四个图表展示测试结果：
      1. 单条查询性能对比
      2. 范围查询性能对比
      3. 整型编码性能提升比例
      4. 查询时间与数据量关系（对数坐标）

#### 1.5.2.  测试结果
运行 007 的测试方案，可以得到如下的股票代码编码方式性能测试结果。

##### 1.5.2.1. 测试数据概览

| 数据量 | 股票数量 | 每只股票天数 | 总记录数  |
| ------ | -------- | ------------ | --------- |
| 小     | 100      | 252          | 25,200    |
| 中小   | 500      | 252          | 126,000   |
| 中     | 1,000    | 252          | 252,000   |
| 中大   | 2,000    | 252          | 504,000   |
| 大     | 5,000    | 252          | 1,260,000 |

##### 1.5.2.2. 查询性能对比

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_06.png)

| 数据量(记录数) | 单条查询时间(ms) |              | 性能提升  | 范围查询时间(ms) |              | 性能提升   |
| -------------- | ---------------- | ------------ | --------- | ---------------- | ------------ | ---------- |
|                | **字符串格式**   | **整型编码** | **倍数**  | **字符串格式**   | **整型编码** | **倍数**   |
| 25,200         | 0.14             | 0.13         | 1.04x     | 7.68             | 0.42         | 18.34x     |
| 126,000        | 0.14             | 0.13         | 1.05x     | 37.34            | 2.30         | 16.24x     |
| 252,000        | 0.14             | 0.14         | 1.03x     | 76.20            | 4.95         | 15.39x     |
| 504,000        | 0.16             | 0.19         | 0.83x     | 148.13           | 10.05        | 14.73x     |
| 1,260,000      | 0.19             | 0.28         | 0.70x     | 377.34           | 24.71        | 15.27x     |
| **平均**       | -                | -            | **0.93x** | -                | -            | **15.99x** |

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/symbol_performance.png)

##### 1.5.2.3. 结果分析

1. **单条查询性能**：
   - 在小到中等数据量(25,200-252,000条)下，整型编码略优于字符串格式(1.03x-1.05x)
   - 在较大数据量(504,000-1,260,000条)下，字符串格式反而略优于整型编码(0.70x-0.83x)
   - 整体来看，单条查询的性能差异不显著，平均提升为0.93倍

2. **范围查询性能**：
   - 在所有数据量级下，整型编码都显著优于字符串格式
   - 性能提升倍数在 <span style="color:red">14.73x-18.34x</span> 之间
   - 平均性能提升达到 <span style="color:red">15.99</span> 倍

3. **随数据量增长的趋势**：
   - 单条查询：随着数据量增加，整型编码的相对优势逐渐减弱
   - 范围查询：整型编码的巨大优势在各数据量级下保持稳定

##### 1.5.2.4. 结论

1. **对于单条查询**：两种编码方式性能相近，在实际应用中差异不明显
2. **对于范围查询**：整型编码提供了显著的性能优势，平均快约16倍
3. **推荐使用场景**：
   - 如果系统中范围查询较为频繁（如按交易所筛选股票），强烈推荐使用整型编码
   - 如果系统主要进行单条查询，编码方式的选择影响不大，可以根据其他因素决定

4. **其他考虑因素**：
   - 整型编码节省存储空间
   - 整型编码便于进行数值运算和比较
   - 字符串格式更直观，调试时更容易理解


## 2. SQEP-BAR-MINITE 分钟线场景下的数据交换格式
同上，但没有复权因子。这样，无论将来我们从哪个数据源获得的数据，消费者一端的代码都不需要更改。这里，我和 007 将设计一个性能测试方案，比较JSON(带key)和CSV(不带key)两种数据交换格式的性能差异。

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_07.png)

### 2.1. 测试方案
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
font_path = 'SimHei.ttf'  # 替换为SimHei.ttf的实际路径
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'SimHei'

class DataFormatBenchmark:
    """SQEP数据格式性能测试：JSON vs CSV"""
    
    def __init__(self):
        """初始化基准测试"""
        # 定义SQEP-BAR-DAY字段顺序（CSV格式需要）
        self.field_order = [
            'symbol', 'frame', 'open', 'high', 'low', 
            'close', 'vol', 'amount', 'adjust'
        ]
    
    def generate_test_data(self, num_records: int) -> List[Dict[str, Any]]:
        """生成测试数据
        
        Args:
            num_records: 记录数量
            
        Returns:
            包含测试数据的记录列表
        """
        data = []
        
        # 生成股票代码 - 确保至少有1只股票
        num_symbols = max(1, min(num_records // 252, 5000))
        symbols = []
        for i in range(num_symbols):
            exchange = 'SH' if i % 2 == 0 else 'SZ'
            symbols.append(f"{str(i).zfill(6)}.{exchange}")
        
        # 生成日期范围 - 确保至少有1天
        days_needed = max(1, num_records // len(symbols))
        start_date = pd.Timestamp('2020-01-01')
        dates = [start_date + pd.Timedelta(days=i) for i in range(min(days_needed, 365))]
        
        # 生成数据
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
        """将数据编码为JSON格式
        
        Args:
            data: 记录列表
            
        Returns:
            JSON字符串
        """
        return json.dumps({
            "timestamp": pd.Timestamp.now().isoformat(),
            "source": "benchmark",
            "data_type": "SQEP-BAR-DAY",
            "records": data
        })
    
    def decode_json(self, json_str: str) -> List[Dict[str, Any]]:
        """将JSON字符串解码为数据
        
        Args:
            json_str: JSON字符串
            
        Returns:
            记录列表
        """
        data = json.loads(json_str)
        return data["records"]
    
    def encode_csv(self, data: List[Dict[str, Any]]) -> str:
        """将数据编码为CSV格式
        
        Args:
            data: 记录列表
            
        Returns:
            CSV字符串
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入元数据行
        writer.writerow([
            pd.Timestamp.now().isoformat(),
            "benchmark",
            "SQEP-BAR-DAY",
            len(data)
        ])
        
        # 写入数据行
        for record in data:
            row = [record[field] for field in self.field_order]
            writer.writerow(row)
        
        return output.getvalue()
    
    def decode_csv(self, csv_str: str) -> List[Dict[str, Any]]:
        """将CSV字符串解码为数据
        
        Args:
            csv_str: CSV字符串
            
        Returns:
            记录列表
        """
        input_file = io.StringIO(csv_str)
        reader = csv.reader(input_file)
        
        # 读取元数据行
        metadata = next(reader)
        timestamp, source, data_type, num_records = metadata
        
        # 读取数据行
        records = []
        for row in reader:
            record = {field: value for field, value in zip(self.field_order, row)}
            
            # 转换数据类型
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
        """运行编码基准测试
        
        Args:
            data: 测试数据
            num_iterations: 迭代次数
            
        Returns:
            JSON和CSV的平均编码时间（毫秒）
        """
        json_times = []
        csv_times = []
        
        for _ in range(num_iterations):
            # 测试JSON编码
            start_time = time.time()
            json_str = self.encode_json(data)
            json_times.append(time.time() - start_time)
            
            # 测试CSV编码
            start_time = time.time()
            csv_str = self.encode_csv(data)
            csv_times.append(time.time() - start_time)
        
        # 计算平均时间（毫秒）
        json_avg = np.mean(json_times) * 1000
        csv_avg = np.mean(csv_times) * 1000
        
        return json_avg, csv_avg
    
    def run_decoding_benchmark(self, data: List[Dict[str, Any]], num_iterations: int = 100) -> Tuple[float, float]:
        """运行解码基准测试
        
        Args:
            data: 测试数据
            num_iterations: 迭代次数
            
        Returns:
            JSON和CSV的平均解码时间（毫秒）
        """
        # 先编码数据
        json_str = self.encode_json(data)
        csv_str = self.encode_csv(data)
        
        json_times = []
        csv_times = []
        
        for _ in range(num_iterations):
            # 测试JSON解码
            start_time = time.time()
            self.decode_json(json_str)
            json_times.append(time.time() - start_time)
            
            # 测试CSV解码
            start_time = time.time()
            self.decode_csv(csv_str)
            csv_times.append(time.time() - start_time)
        
        # 计算平均时间（毫秒）
        json_avg = np.mean(json_times) * 1000
        csv_avg = np.mean(csv_times) * 1000
        
        return json_avg, csv_avg
    
    def measure_size(self, data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """测量编码后的数据大小
        
        Args:
            data: 测试数据
            
        Returns:
            JSON和CSV的字节大小
        """
        json_str = self.encode_json(data)
        csv_str = self.encode_csv(data)
        
        return len(json_str.encode('utf-8')), len(csv_str.encode('utf-8'))
    
    def run_full_benchmark(self, data_sizes: List[int], num_iterations: int = 100):
        """运行完整基准测试
        
        Args:
            data_sizes: 测试的记录数量列表
            num_iterations: 每次测试的迭代次数
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
            print(f"测试数据量: {size}条记录")
            
            # 生成测试数据
            data = self.generate_test_data(size)
            
            # 运行编码测试
            json_encode_time, csv_encode_time = self.run_encoding_benchmark(data, num_iterations)
            
            # 运行解码测试
            json_decode_time, csv_decode_time = self.run_decoding_benchmark(data, num_iterations)
            
            # 测量数据大小
            json_size, csv_size = self.measure_size(data)
            
            # 记录结果
            results['data_size'].append(size)
            results['json_encode_time'].append(json_encode_time)
            results['csv_encode_time'].append(csv_encode_time)
            results['json_decode_time'].append(json_decode_time)
            results['csv_decode_time'].append(csv_decode_time)
            results['json_size'].append(json_size)
            results['csv_size'].append(csv_size)
            
            print(f"  编码时间 - JSON: {json_encode_time:.2f}ms, CSV: {csv_encode_time:.2f}ms")
            print(f"  解码时间 - JSON: {json_decode_time:.2f}ms, CSV: {csv_decode_time:.2f}ms")
            print(f"  数据大小 - JSON: {json_size/1024:.2f}KB, CSV: {csv_size/1024:.2f}KB")
            print(f"  性能比较 - 编码: JSON/CSV = {json_encode_time/csv_encode_time:.2f}x, 解码: JSON/CSV = {json_decode_time/csv_decode_time:.2f}x")
            print(f"  大小比较 - JSON/CSV = {json_size/csv_size:.2f}x")
            print()
        
        # 绘制结果图表
        self._plot_results(results)
        
        return results
    
    def _plot_results(self, results: dict):
        """绘制测试结果图表
        
        Args:
            results: 测试结果字典
        """
        plt.figure(figsize=(15, 12))
        
        # 编码时间对比
        plt.subplot(3, 2, 1)
        plt.plot(results['data_size'], results['json_encode_time'], 'o-', label='JSON')
        plt.plot(results['data_size'], results['csv_encode_time'], 'o-', label='CSV')
        plt.title('编码时间对比')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('平均编码时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        # 解码时间对比
        plt.subplot(3, 2, 2)
        plt.plot(results['data_size'], results['json_decode_time'], 'o-', label='JSON')
        plt.plot(results['data_size'], results['csv_decode_time'], 'o-', label='CSV')
        plt.title('解码时间对比')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('平均解码时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        # 数据大小对比
        plt.subplot(3, 2, 3)
        plt.plot(results['data_size'], [s/1024 for s in results['json_size']], 'o-', label='JSON')
        plt.plot(results['data_size'], [s/1024 for s in results['csv_size']], 'o-', label='CSV')
        plt.title('数据大小对比')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('数据大小 (KB)')
        plt.legend()
        plt.grid(True)
        
        # 性能比率
        plt.subplot(3, 2, 4)
        encode_ratio = [j/c for j, c in zip(results['json_encode_time'], results['csv_encode_time'])]
        decode_ratio = [j/c for j, c in zip(results['json_decode_time'], results['csv_decode_time'])]
        size_ratio = [j/c for j, c in zip(results['json_size'], results['csv_size'])]
        
        plt.plot(results['data_size'], encode_ratio, 'o-', label='编码时间比 (JSON/CSV)')
        plt.plot(results['data_size'], decode_ratio, 'o-', label='解码时间比 (JSON/CSV)')
        plt.plot(results['data_size'], size_ratio, 'o-', label='大小比 (JSON/CSV)')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.title('JSON/CSV 性能比率')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('比率 (JSON/CSV)')
        plt.legend()
        plt.grid(True)
        
        # 编码+解码总时间
        plt.subplot(3, 2, 5)
        json_total = [e + d for e, d in zip(results['json_encode_time'], results['json_decode_time'])]
        csv_total = [e + d for e, d in zip(results['csv_encode_time'], results['csv_decode_time'])]
        plt.plot(results['data_size'], json_total, 'o-', label='JSON')
        plt.plot(results['data_size'], csv_total, 'o-', label='CSV')
        plt.title('总处理时间 (编码+解码)')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('总时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        # 对数坐标下的性能
        plt.subplot(3, 2, 6)
        plt.loglog(results['data_size'], results['json_encode_time'], 'o-', label='JSON编码')
        plt.loglog(results['data_size'], results['csv_encode_time'], 'o-', label='CSV编码')
        plt.loglog(results['data_size'], results['json_decode_time'], 'o-', label='JSON解码')
        plt.loglog(results['data_size'], results['csv_decode_time'], 'o-', label='CSV解码')
        plt.title('性能随数据量变化 (对数坐标)')
        plt.xlabel('数据量 (记录数)')
        plt.ylabel('时间 (毫秒)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('data_format_benchmark.png')
        plt.close()


if __name__ == "__main__":
    # 运行基准测试
    benchmark = DataFormatBenchmark()
    
    # 测试不同数据量
    data_sizes = [100, 500, 1000, 5000, 10000, 50000]
    results = benchmark.run_full_benchmark(data_sizes)
    
    # 输出总结
    print("测试总结:")
    print(f"数据量范围: {min(results['data_size'])} - {max(results['data_size'])}条记录")
    
    # 计算平均比率
    avg_encode_ratio = np.mean([j/c for j, c in zip(results['json_encode_time'], results['csv_encode_time'])])
    avg_decode_ratio = np.mean([j/c for j, c in zip(results['json_decode_time'], results['csv_decode_time'])])
    avg_size_ratio = np.mean([j/c for j, c in zip(results['json_size'], results['csv_size'])])
    
    print(f"编码时间比率 (JSON/CSV): {avg_encode_ratio:.2f}x")
    print(f"解码时间比率 (JSON/CSV): {avg_decode_ratio:.2f}x")
    print(f"数据大小比率 (JSON/CSV): {avg_size_ratio:.2f}x")
    
    print("\n测试完成，结果已保存到 data_format_benchmark.png")
```
这个性能测试方案全面比较了JSON(带key)和CSV(不带key)两种数据交换格式在不同数据量下的性能差异。主要测试内容包括：
1. 测试内容
  测试方案包含三个主要方面的比较：
    - 编码性能：将数据结构转换为字符串的速度
    - 解码性能：将字符串解析回数据结构的速度
    - 数据大小：编码后的数据占用空间
2. 测试数据
    - 生成不同数量的SQEP-BAR-DAY记录（从100到50,000条）
    - 每条记录包含完整的股票日线数据字段
    - 数据内容模拟真实交易数据
3. 数据格式实现
   1) JSON格式：
      - 包含完整的字段名（键）
      - 使用标准JSON结构，包含元数据和记录数组
      - 示例：
      ```json
      {
        "timestamp": "2023-05-01T12:00:00",
        "source": "benchmark",
        "data_type": "SQEP-BAR-DAY",
        "records": [
            {
            "symbol": "000001.SZ",
            "frame": "2023-05-01",
            "open": 10.5,
            "high": 11.2,
            "low": 10.3,
            "close": 11.0,
            "vol": 123456,
            "amount": 1234567,
            "adjust": 1.0
            },
            ...
        ]
        }
      ```
    2) CSV格式：
         - 不包含字段名，依赖固定的字段顺序
         - 第一行包含元数据（时间戳、来源、数据类型、记录数）
         - 后续每行是一条记录
         - 示例：
         ```
         2023-05-01T12:00:00,benchmark,SQEP-BAR-DAY,1000
         000001.SZ,2023-05-01,10.5,11.2,10.3,11.0,123456,1234567,1.0
         ...
         ```
4. 测试指标
    - 编码时间：将数据结构转换为字符串的平均时间（毫秒）
    - 解码时间：将字符串解析回数据结构的平均时间（毫秒）
    - 数据大小：编码后的字符串大小（字节/KB）
    - 性能比率：JSON/CSV的比值，表示相对性能差异


### 2.2. 测试结果

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/4_08.png)

| 数据量(记录数) | JSON编码时间(ms) | CSV编码时间(ms) | JSON解码时间(ms) | CSV解码时间(ms) | JSON大小(KB) | CSV大小(KB) | 编码比率(JSON/CSV) | 解码比率(JSON/CSV) | 大小比率(JSON/CSV) |
| -------------- | ---------------- | --------------- | ---------------- | --------------- | ------------ | ----------- | ------------------ | ------------------ | ------------------ |
| 100            | 0.13             | 0.14            | 0.07             | 0.09            | 16.16        | 7.12        | 0.96x              | 0.71x              | 2.27x              |
| 500            | 0.47             | 0.51            | 0.24             | 0.34            | 58.67        | 25.82       | 0.93x              | 0.69x              | 2.27x              |
| 1,000          | 1.42             | 1.55            | 0.75             | 0.94            | 160.47       | 70.67       | 0.91x              | 0.81x              | 2.27x              |
| 5,000          | 6.86             | 7.06            | 3.35             | 4.80            | 802.26       | 353.26      | 0.97x              | 0.70x              | 2.27x              |
| 10,000         | 13.23            | 13.94           | 6.69             | 9.67            | 1,602.63     | 705.58      | 0.95x              | 0.69x              | 2.27x              |
| 50,000         | 66.37            | 70.23           | 34.55            | 48.12           | 8,009.18     | 3,526.28    | 0.95x              | 0.72x              | 2.27x              |
| 平均           | -                | -               | -                | -               | -            | -           | 0.95x              | 0.72x              | 2.27x              |

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/data_format_benchmark.png)

#### 2.2.3. 结果分析
1. 编码性能
    JSON编码在所有测试数据量下都略快于CSV编码，平均快约5%（0.95x）
2. 解码性能
    JSON解码明显快于CSV解码，平均快约28%（0.72x）
3. 数据大小
    JSON格式的数据大小始终是CSV格式的2.27倍

## 总结
在这一章的探索中，我和我的AI助手007一起深入研究了量化交易系统中数据交换格式的性能问题。这次"数据格式大PK"不仅让我们获得了宝贵的技术数据，更展示了人机协作的无限可能！

007不愧是"码力全开"的得力助手，它不仅设计了全面的测试方案，还在遇到除零错误时迅速提供了解决方案。通过我们的共同努力，成功对比了JSON和CSV两种格式在不同数据量下的表现：JSON在处理速度上略胜一筹，而CSV在存储效率上更具优势。

这次测试不仅是技术上的突破，更是我们21天驯化AI打工仔挑战的又一个里程碑！正如测试数据一样，我们的合作也在不断扩展规模，从100条记录到50,000条记录，效率始终保持稳定，这正是我们合作的真实写照！

正如007所说："数据是一切开始的基础"，而我们的合作则是创新的源泉。期待在接下来的SQEP扩展格式探索中，继续与007携手并进，为量化交易系统注入更多智慧的火花！

下一步：SQEP扩展格式探索之旅
接下来，我和007将继续我们的冒险，探索SQEP的两个重要扩展格式：
1. SQEP-ST：专为特殊处理（ST）股票设计的数据格式
    - 这些特殊股票信息虽然稀疏，但对投资决策至关重要
    - 我们将巧妙地将ST信息整合到现有的SQEP-BAR-DAY表中
    - 通过布尔型st字段，让系统能够快速识别特殊股票
2. 涨跌停信息：交易限制的关键指标
   - 添加buy_limit和sell_limit字段，为回测系统提供精确的交易约束
   - 这些信息将帮助我们模拟真实市场中的交易规则
   - 确保回测结果更加贴近实际交易环境

有了这些扩展，我们的量化交易系统将更加完善，能够应对更复杂的市场情况。正如007所展示的那样，只要思路清晰、方法得当，即使是复杂的数据处理问题也能迎刃而解！让我们继续这场激动人心的21天挑战，用数据和智慧创造更多可能！
