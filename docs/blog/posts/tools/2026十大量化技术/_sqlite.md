---
title: 
date: 
img:
excerpt:
categories:
tags:
---

sqlite wal 模式下，一次 io 只需要 ms, 而量化新规要求每秒报单不超过300次。sqlite-utils 和 fastlite 增强了它的易用性。

```Python
@singleton
class TradeDB:
    def __init__(self):
        # 每个线程都有自己的数据库连接
        self._thread_local = threading.local()
        self.db_path: str = ""
        self._initialized = False
    
    def init(self, db_path: str):
        if self._initialized:
            return
        
        # 初始化数据库连接
        self.db_path = db_path

        conn = sqlite3.connect(db_path)
        db = su.Database(conn)
        
        # 启用 WAL 模式提高并发读性能
        if db_path != ":memory:":
            db.enable_wal()
        
        # 初始化表结构
        self._init_tables(db)
        conn.close()
        self._initialized = True

    @property
    def db(self)->su.Database:
        """获取当前线程的数据库连接"""
        if not self._initialized:
            raise RuntimeError("TradeDB has not been initialized. Call init(db_path) first.")

        if not hasattr(self._thread_local, "conn"):
            conn = sqlite3.connect(self.db_path, check_same_thread=True)

            self._thread_local.conn = conn
            self._thread_local.db = su.Database(conn)

        return self._thread_local.db
    def _init_tables(self, db: su.Database):
        """初始化表结构
        
        在 sqlite_utils 中，创建表结构并非必须；但会导致sqlite-utils 无法准确判断类型。
        """
        for model in [OrderModel, TradeModel, AssetModel, PositionModel]:
            table = model.__table_name__
            pk = model.__pk__

            t: su.db.Table = db[table] # type: ignore
            t.create(model.to_db_schema(), pk=pk)

            if model.__indexes__ is not None:
                indexes, is_unique = model.__indexes__
                t.create_index(indexes, unique=is_unique)
```

通过以下方式声明 dataclass model, 一个极简、极易上手的 ORM 就完成了：

```Python
def _dataclass_to_schema(cls) -> dict:
    """类方法：解析当前 dataclass 为 fastlite 兼容的 schema 字典"""
    schema = {}

    for f in fields(cls):
        if f.type is uuid.UUID:
            schema[f.name] = str
        elif f.type in (str, int, float, bool):
            schema[f.name] = f.type
        elif getattr(f.type, "__origin__", None) is type(None) or (
            hasattr(f.type, "__args__") and type(None) in f.type.__args__
        ):
            base_type = [t for t in f.type.__args__ if t is not type(None)][0]
            schema[f.name] = base_type if base_type in (str, int, float, bool) else str
        else:
            schema[f.name] = str
    return schema

def db_model(table_name: str, pk: str, indexes:tuple[list[str], bool]):
    def wrapper(cls: Type[T])->Type[T]:
        setattr(cls, "__table_name__", table_name)
        setattr(cls, "__pk__", pk)
        setattr(cls, "__indexes__", indexes or []) # 例如 (["qtoid", "foid"], True)

        if not hasattr(cls, 'to_db_schema'):
            @classmethod
            def to_db_schema(cls_inner):
                return _dataclass_to_schema(cls_inner)
            
            cls.to_db_schema = to_db_schema
        return cls
    return wrapper


@db_model("orders", "qtoid", (["qtoid", "tm"], True))
@dataclass
class OrderModel:
    asset: str                              # 资产代码
    side: OrderSide
    shares: float|int                       # 委托数量。调用者需要保证符合交易要求
    price: float
    bid_type: BidType                       # 委托类型，比如限价单、市价单  
    tm: datetime.datetime|None = None       # 下单时间

    foid: str|None = None                   # 代理(比如QMT)指定的 id，透传，一般用以查错
    cid: str|None = None                    # 券商柜台合约 id
    status: OrderStatus = OrderStatus.UNREPORTED # 委托状态，比如未报、待报、已报、部成等
    status_msg: str = ""                    # 委托状态描述，比如废单原因

    # 本委托 ID, pk
    qtoid: str = field(default_factory=lambda: "qtide-" + uuid.uuid4().hex[:16])
    strategy: str = ""                   # 策略名称

    @classmethod
    def to_db_schema(cls)->dict:
        schema = _dataclass_to_schema(cls)

        # 修正无法自动转换的类型
        schema["status"] = int
        schema["bid_type"] = int
        schema["foid"] = str
        return schema
    
    def __post_init__(self):
        if isinstance(self.status, int):
            self.status = OrderStatus(self.status)
        if isinstance(self.bid_type, int):
            self.bid_type = BidType(self.bid_type)
        if isinstance(self.side, int):
            self.side = OrderSide(self.side)
```

