---
title: "SQLite + sqlite-utils: Building High-Concurrency Quant Trading DBs"
date: 2026-01-01
slug: en/posts/tools/2026十大量化技术/sqlite
tags: [SQLite, Quant Infrastructure, Database Optimization, Python]
excerpt: "Unlock SQLite’s WAL mode and sqlite-utils to build lightweight, high-performance trading databases. Learn Pythonic data handling, concurrent access, and ORM-free workflows for 2026 quant infrastructure."
lang: en
translation_of: posts/tools/2026十大量化技术/sqlite
auto_translated: true
source_sha: f5cf930b08fdad06649c640c32f5a0594f0e6ca3
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/153f985ba06d4a909bd17e097d904b20_3_with_two_logo.jpg"
---

Many people (including myself) hold a misconception about SQLite: first, it’s a toy; second, it’s unsuitable for production environments.

In reality, SQLite is an exceptional database. In 2025, it ranked second only to PostgreSQL in popularity and remains the most widely used database globally.

<div style='width:90%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/153f985ba06d4a909bd17e097d904b20_3_with_two_logo.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

---

Quantitative traders should use tools suited for quant tasks. SQLite is a precise Swiss Army knife: compact, flexible, and powerful. However, for quant developers, there is one scenario where SQLite shines: it requires no installation or configuration, supports Pythonic development, and delivers excellent performance.

This scenario is using SQLite as a **trading database** for quantitative programs.

Until recently, I operated SQLite directly via Python’s built-in `sqlite3` module. Recently, I discovered the `sqlite-utils` library, which grants unprecedented expressiveness in the most concise manner possible.

Therefore, I have decided to feature SQLite/sqlite-utils as the second installment of the 2026 Quant Tech Stack series.

## The Performance Silver Bullet: WAL Mode

As a trading database, it primarily stores order records, trade records, daily holdings, and daily asset tables. Among these, order records constitute the largest data volume because we must log both order submissions and cancellations.

---

According to new quantitative trading regulations, order submissions are capped at 300 per second and 20,000 per day. This is not a high-pressure requirement; SQLite can handle it with ease.

More critical than performance pressure is the need to support **concurrent read-write operations**. When an order is submitted, it often does not execute immediately, and we cannot wait indefinitely for its execution status. Therefore, execution status is typically notified via callbacks, which are often scheduled in other threads.

!!! question
    Can multiple processes open the same SQLite database for concurrent read-write operations?

You might receive the following answer:

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251231110246.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

---

In fact, SQLite has supported **multi-process concurrent read-write operations** since 2010, and users do not need to manage locks manually. However, SQLite operates in two modes: "delete" and "WAL". SQLite’s default option has always been "delete" mode, which does not support concurrency. This has led many to mistakenly believe that SQLite cannot support concurrent read-write operations.

According to tests and official documentation, enabling WAL mode improves performance in almost all scenarios. So why is "delete" still the default? The SQLite team adheres to a culture of minimalism, aiming for a single-file database. Enabling WAL mode creates three data files, and they worry some users might find this confusing.

In WAL mode, the other two files are `.shm` and `.wal`. SQLite stores lock information in the `.shm` file—a shared memory file. In WAL mode, reads access stable data from the main database without locking. Writes lock the `.wal` file first, and only briefly lock the main database during the final merge.

---

Therefore, in WAL mode, SQLite’s lock granularity is finer than in "delete" mode. Consequently, even in single-process read-write scenarios, performance is slightly better (about 5%).

!!! tip
    Lock granularity is key to database performance in many concurrent scenarios. PostgreSQL outperforms SQLite in high-concurrency read-write operations because its lock granularity, based on MVCC technology, is much finer.

If WAL mode is enabled, SQLite can process a single transaction in less than 0.1ms. This means SQLite can handle at least 10,000 transactions per second, making it fully capable of serving as a trading database. Furthermore, since it does not require network interfaces, its latency may even be lower than that of network-based databases.

To enable concurrent read-write access from multiple processes, you must enable WAL mode as follows:

```python
import sqlite3

conn = sqlite3.connect(path/to/sqlite.db)
conn.execute("PRAGMA journal_mode = WAL;")
```

---

Clearly, this is not very Pythonic. If we use `sqlite-utils`, we can enable WAL mode directly like this:

```python
import sqlite_utils as su

db = su.Database(path/to/sqlite.db)
db.enable_wal()
db.journal_mode # Displays as 'wal'
```

Returning to the multi-threaded read-write issue: SQLite supports concurrent read-write operations after enabling WAL mode. However, if you share a `connection` object across threads, you still need to add locking mechanisms. In such cases, we can introduce a thread-local wrapper:

```python
import threading

@singleton
class TradeDB:
    def __init__(self):
        # Each thread has its own database connection
        self._thread_local = threading.local()
        self.db_path: str = ""
        self._initialized = False
    
    def init(self, db_path: str):
        if self._initialized:
            return
```

---

```python
    def init(self, db_path: str):
        if self._initialized:
            return
        # Initialize database connection
        self.db_path = db_path

        conn = sqlite3.connect(db_path)
        db = su.Database(conn)
        
        # Enable WAL mode to improve concurrent read performance
        if db_path != ":memory:":
            db.enable_wal()
        
        # Initialize table structure
        self._init_tables(db)
        conn.close()
        self._initialized = True

    @property
    def db(self)->su.Database:
        """Get the database connection for the current thread"""
        if not hasattr(self._thread_local, "conn"):
            conn = sqlite3.connect(self.db_path, check_same_thread=True)

            self._thread_local.conn = conn
            self._thread_local.db = su.Database(conn)

        return self._thread_local.db
```

---

```python
    def __getitem__(self, table_name) -> su.db.Table:
        """Proxy to get table object"""
        return self.db[table_name]  # type: ignore

db = TradeDB()
db.init(path/to/sqlite.db)
db["users"].insert({"id": 1, "name": "Quantide"})
```

Through this wrapper, we expose a global, unique `db` object that can be used across multiple threads without explicit locking. This is achieved by using Thread Local Storage (TLS) to maintain an independent database connection for each thread.

By overriding the `__getitem__` method, we proxy table access to the database connection of the current thread, allowing you to perform database operations using the exact same methods documented in the `sqlite-utils` documentation.

## Semi-ORM

In Python, database operations can be performed using native SQL or ORM approaches. Native methods offer high performance but require familiarity with SQL syntax and are difficult to refactor. ORM methods allow database operations using Pythonic syntax. A representative example is SQLAlchemy.

---

However, SQLAlchemy has its own issues: it is too comprehensive and complex. For simple, exploratory applications, using SQLAlchemy feels cumbersome.

This is why many people choose `sqlite-utils`. It solves the following problems:

1. It is a semi-ORM, allowing Pythonic database operations without the verbosity of SQLAlchemy.
2. SQLite is only a database engine without data management tools. To know which tables exist in a SQLite database or their data structure, you must programmatically read them. `sqlite-utils` provides this capability via its CLI.

!!! tip
    Another tool for managing SQLite databases is through notebooks, combined with the `sqlite-utils` library or `jupysql`. The prerequisite is still enabling WAL mode for the database to share it across multiple processes.

In SQLAlchemy, to retrieve data, you must first learn how to define schemas:

---

```python
# 1. Define engine
engine = create_engine('sqlite:///data.db')
Base = declarative_base()

# 2. Define model
class Tick(Base):
    __tablename__ = 'ticks'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    # If a 'volume' field is added tomorrow, you must modify the code and perform database migrations (Alembic)

# 3. Create table
Base.metadata.create_all(engine)

# 4. Insert
session.add(Tick(symbol='AAPL', price=100.0))
session.commit()
```

Here, we introduce types like `Base`, `Column`, `String`, `Float`, `Integer`, and we must also know the usage of the magic string `__tablename__`.

In `sqlite-utils`, everything is much simpler:

```python
import sqlite_utils as su

db = su.Database(":memory:") # ❶
```

---

```python
import sqlite_utils as su

db = su.Database(":memory:") # ❶
db["users"].insert_all([{"id": 1, "name": "Fred"}, 
                        {"id": 2, "name": "Wilma"}
                        ]) # ❷
print(db.tables) # ❸
print(db["users"].columns) # ❹
list(db["users"].rows) # ❺
```

It’s incredible! **You don’t need to define table structures** to insert data directly!

In the first line, we create an in-memory database and establish a connection. If a filename is passed, a disk-based database file is created.

In the second line, we reference a table named `users` that doesn’t yet exist via `db["users"]` and directly insert two records.

In the third line, we print all tables in the current database; `users` now exists.

In the fourth line, we print the column fields of the `users` table, which `sqlite-utils` automatically determines and creates.

---

In the fifth line, we print all data in the `users` table.

`sqlite-utils` cleverly borrows the syntax of **document databases** (like MongoDB), making database operations exceptionally simple. This approach might involve adding new fields or changing field definitions. However, if your data belongs in SQLite, adding or modifying field definitions is rare. So why not skip the cumbersome table structure definition and let `sqlite-utils` handle everything?

!!! tip
    You might wonder: if we insert a new object containing 'gender' and 'age' fields after line 5, how does `sqlite-utils` handle it? Internally, `sqlite-utils` detects structural changes and automatically calls the `transform` method to define the new table structure and migrate data. See the image below.
    ![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/12/20251231153523.png)

---

Of course, we encourage explicitly defining table structures to improve performance and add data validation capabilities. Besides the `pydantic` models method introduced in the previous article, if you are already familiar with `dataclasses`, we can introduce a manual ORM approach based on `dataclasses` that is easier to learn.

## Defining Entity-Relationship Mappings with Dataclass

The `sqlite-utils` example just demonstrated how to read data directly from the database without defining table structures. This is convenient for exploratory data analysis.

In practical applications, we prefer explicitly defining table structures and adding data type validation and conversion capabilities, making the code for upper-layer callers simpler and more consistent. This is where `dataclass` comes into play.

```python
from dataclasses import dataclass, asdict, fields
import types
import sqlite_utils as su
from enum import IntEnum
import datetime
```

---

```python
def _dataclass_to_schema(model) -> dict:
    """Class method: Parse the current dataclass into a schema dictionary compatible with sqlite-utils"""
    schema = {}

    for f in fields(model):
        if f.type in (str, int, float, bool):
            schema[f.name] = f.type
        # Handle all union types (Union[A, B] and A | B syntax)
        elif (
            hasattr(f.type, "__origin__") and f.type.__origin__ is Union
        ) or isinstance(f.type, types.UnionType):
            # Extract non-None types
            non_none_types = [t for t in f.type.__args__ if t is not type(None)]
            if non_none_types:
                base_type = non_none_types[0]
                schema[f.name] = (
                    base_type if base_type in (str, int, float, bool) else str
                )
            else:
                schema[f.name] = str
        elif isinstance(f.type, type) and issubclass(f.type, IntEnum):
            schema[f.name] = int
        else:
            schema[f.name] = str
    return schema
```

---

```python
def create_tables(db: su.Database, model):
    """Initialize table structure
    
    In sqlite-utils, creating table structures is not mandatory; but it prevents sqlite-utils from accurately judging types.
    """
    table = model.__table__
    pk = model.__pk__

    t: su.db.Table = db[table] # type: ignore
    t.create(_dataclass_to_schema(model), pk=pk)

    if model.__indices__ is not None:
        indexes, is_unique = model.__indices__
        t.create_index(indexes, unique=is_unique)

class Gender(IntEnum):
    MALE = 1
    FEMALE = 2

@dataclass
class User:
    # ❶ Use magic fields to provide metadata for subsequent table creation
    __table__ = "users"
    __pk__ = "id"
    __indices__ = (["name"], False)

    id: int
    name: str
    birth: datetime.date
    gender: Gender

```

---

```python
    def __post_init__(self):
        # ❷ SQLite has no time type; time is generally stored as strings.
        if isinstance(self.birth, str):
            self.birth = datetime.date.fromisoformat(self.birth)
        # ❸ SQLite has no enum type; integer enums are generally stored as integers, other enums as strings.
        if isinstance(self.gender, int):
            self.gender = Gender(self.gender)

user = User(id=1, name="Alice", birth=datetime.date(2020, 1, 1), gender=Gender.FEMALE)
db = su.Database(memory=True)

create_tables(db, User) # ❹ Explicitly create table -- declare primary key, indexes, etc.
db["users"].insert(asdict(user))

# Display the just-inserted record ❺
user_from_db = User(**list(db["users"].rows)[0])
user_from_db
```

Here are a few tips.

First, we convert type declarations into database fields (unlike SQLAlchemy, which requires explicit declaration). This is very Pythonic. In the `_dataclass_to_schema` method, we extract the types of all fields in the `User` class (excluding magic fields). If it is a union type, we find the first non-None type as the field type, then map them to database field types. Of course, due to limited database field types, most data types are mapped to `TEXT`.

---

Second, we use magic fields like `__table__`, `__pk__`, and `__indices__` to provide metadata for table creation. This resembles SQLAlchemy but uses only standard, built-in syntax, appearing much more concise.

Third, some Python data types are mapped to integers and strings in the database. Data retrieved from the database will also be strings and integers, but they actually correspond to `datetime` or `Enum` types. In databases supporting complex data types, the database connection driver automatically performs these conversions.

Neither the built-in `sqlite` module nor `sqlite-utils` does this. However, this conversion is very easy to implement ourselves. As shown in comments ❷ and ❸, we achieve this via the `__post_init__` method.

In comment ❹, we explicitly create the table, declaring the primary key and indexes. If we don’t do this, the subsequent insertion statement will fail because `sqlite-utils` cannot map the `Gender` type to a database field.

<p style="text-align:right;color: red;font-size: 36px"> To be continued</p>
---

Fourth, when saving a Python object, if it is a `dataclass` class, we can save it using a method like `db["users"].insert(asdict(user))`. `asdict` is a method in `dataclasses` used to convert a dataclass to a dictionary, which `sqlite-utils` then converts to a row in the table and inserts into the database.

Comment ❺ demonstrates a method for reading database records via `rows`. It is an iterator; to get a specific element, we must first convert it to a list and then access it via index. The resulting data is also a dictionary, which can be converted to a `User` object via `User(**dict)`. **During this conversion process**, the `__post_init__` method is called, converting `birth` from a string in the database to a Python date object, and `gender` from an integer to an Enum type.

This part shares conceptual similarities with the Pydantic section introduced in the previous article of this series, except we use `dataclasses` to pair with `sqlite-utils`.

In places where built-in syntax can be used, I prefer **using only built-in syntax, without third-party libraries**. Do not add entities unless necessary.

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/202
