"""基础的数据存储和缓存类。在提供了 fetcher 方法的前提下，能够自动从数据源获取数据，从而使得应用层无须操心本地数据是否全面。

需要与一个日历类一起使用。日历类的作用是，协助 fetcher 数据是否有缺失，是否要从远程获取。一般使用 alpha.data.models.calendar；但如果要处理的是财数据（或者任何在非交易日可能发布的数据，则子类需要将日历改写为自然日历，以使得 Calendar.get_trade_dates能返回自然日历。

本模块使用 polars 来加速读写和运算。但数据输入和输出的接口仍使用 pandas.DataFrame.
"""

import datetime
from pathlib import Path

import pandas as pd
import polars as pl
from loguru import logger
from typing import Callable
import pytz
from fetchers import fetch_calendar, fetch_bars_ext
from helper import qfq_adjustment, hfq_adjustment


epoch = datetime.date(2005, 1, 1)


class CalendarModel:
    """日历模型"""

    def __init__(self, path: str):
        self._path: Path | None = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)

        self._data = pd.DataFrame(columns=["is_open", "prev"])
        self.load(path)

    @property
    def end(self) -> datetime.date:
        return self._data.index[-1]

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def path(self) -> Path:
        """日历文件路径"""
        if self._path is None:
            raise ValueError("日历文件路径未指定")
        return self._path

    def load(self, path: str | None = None) -> None:
        """加载日历数据。如果指定文件不存在，则从tushare获取"""
        if path is not None:
            parent = Path(path).parent
            parent.mkdir(parents=True, exist_ok=True)
            logger.info("Calendar 将从 {}处加载数据", path)
            self._path = Path(path)

        if not self.path.exists():
            df = fetch_calendar(epoch)
            self.save(df)
            return

        # 日历已存在
        try:
            self._data = pd.read_parquet(self.path)
        except Exception as e:
            logger.warning("Calendar 读取日历数据失败，重新从服务器获取")
            logger.exception(e)
            df = fetch_calendar(epoch)
            self.save(df)

    def update(self) -> None:
        """更新日历"""
        df = fetch_calendar(epoch)
        self.save(df)

    def save(self, calendar_data: pd.DataFrame) -> None:
        """一次性写入整个trade_calendar表的数据（会先清空表）

        Args:
            calendar_data: 索引为 date, 字段 is_open, prev
        """
        self._data = calendar_data
        self._data.to_parquet(self.path)

    def get_trade_dates(
        self, start: datetime.date, end: datetime.date
    ) -> list[datetime.date]:
        """获取指定日期范围内所有的交易日

        Args:
            start: 开始日期（包含）
            end: 结束日期（包含）

        Returns:
            List[datetime.date]: 指定范围内所有交易日的列表，按日期升序排列

        Raises:
            ValueError: 如果start > end则抛出异常
        """
        if start > end:
            raise ValueError(f"开始日期 {start} 不能大于结束日期 {end}")

        df = self._data
        mask = (df.index >= start) & (df.index <= end) & (df.is_open == 1)
        return df[mask].index.tolist()

    def is_trade_date(self, date: datetime.date) -> bool:
        """判断给定日期是否是交易日

        Args:
            date: 需要判断的日期

        Returns:
            bool: 如果是交易日则返回True，否则返回False

        Raises:
            ValueError: 如果查询日期不在交易日历中则抛出异常
        """
        df = self._data

        if date in df.index:
            return (df.loc[date, "is_open"] == 1).item()  # type: ignore

        raise ValueError(f"{date} 不在交易日历中")

    def prev_trade_day(self, date: datetime.date) -> datetime.date:
        """指定日期的前一交易日

        Args:
            date (datetime.date): 指定日期

        Returns:
            datetime.date: 返回前一个交易日

        Raises:
            ValueError: 如果查询日期不在交易日历中，则抛出异常
        """
        if date in self._data.index:
            return self._data.loc[date, "prev"]  # type: ignore

        raise ValueError(f"{date} 不在交易日历中")

    def get_next_trade_day(self, date: datetime.date) -> datetime.date:
        """获取指定日期之后的下一个交易日

        Args:
            date: 起始日期

        Returns:
            datetime.date: 下一个交易日
        """
        mask = (self._data.index > date) & (self._data.is_open == 1)

        selected = self._data[mask]
        if len(selected) > 0:
            return selected.index[0]

        raise ValueError(f"{date} 之后没有交易日")

    def floor(
        self, date: datetime.date, now: datetime.time = datetime.time(hour=16)
    ) -> datetime.date:
        """获取到指定日期时，最后一个已结束的交易日

        如果在交易日盘中运行，则返回前一个交易日（不一定是前一个日历日）。
        如果是交易日盘后运行，则返回当日。
        如果在非交易日运行，则返回前一个交易日

        Args:
            date (datetime.date): 判断日期
            now (datetime.time): 判断交易日的时间。默认为盘后。
        """
        if self.is_trade_date(date):
            if now.hour >= 15:
                return date
            else:
                # 不能用 prev_trade_day, tushare 的方法不正确
                return self._data.query("index < @date and is_open == 1").index[-1]

        return self._data.query("index < @date and is_open == 1").index[-1]

    def ceil(self, date: datetime.date) -> datetime.date:
        """获取大于等于指定日期的交易日

        如果 date 为非交易日，则返回下一交易日。否则返回 date 本身。
        """
        if self.is_trade_date(date):
            return date
        else:
            return self.get_next_trade_day(date)

    def delta(
        self,
        date1: datetime.date,
        date2: datetime.date,
        now: datetime.time = datetime.time(hour=16),
    ) -> int:
        """计算两个日期之间的相差多少个交易日

        如果两者相等，则返回零。
        Args:
            date1 (datetime.date): 起始日期
            date2 (datetime.date): 结束日期
        """
        trade_dt_1 = self.floor(date1, now)
        trade_dt_2 = self.floor(date2, now)

        if trade_dt_1 < trade_dt_2:
            dates = self._data.query(
                "index >= @trade_dt_1 and index <= @trade_dt_2 and is_open==1"
            )
            return len(dates) - 1

        if trade_dt_1 > trade_dt_2:
            dates = self._data.query(
                "index >= @trade_dt_2 and index <= @trade_dt_1 and is_open==1"
            )
            return 1 - len(dates)

        return 0

    def shift(self, date: datetime.date, n: int) -> datetime.date:
        """将指定日期前后移动 n 个交易日

        n 为正数时，返回 date 之后的第 n 个交易日。
        n 为负数时，返回 date 之前的第 n 个交易日。
        """
        trade_date = self.floor(date)

        if n == 0:
            return trade_date

        elif n > 0:
            dates = self._data.query("index >= @trade_date and is_open==1").index
            return dates[min(n, len(dates) - 1)]

        else:
            dates = self._data.query("index < @trade_date and is_open==1").index
            return dates[max(n, -len(dates))]


class ParquetUnifiedStorage:
    """基于Parquet文件的统一数据存储类。

    被存储的数据必须有使用"asset" 和 "date"的组合作为惟一的键值，以区分数据。

    在内部使用扁平的 polars.DataFrame 来管理数据 (lazy模式)。传入和返回数据一般为 pd.DataFrame。

    获取数据的主要方法是 get_with_fetch, get, get_by_date. get_with_fetch 在数据不存在时，会调用 fetch_data_func 获取数据并保存； get, get_by_date 则不会。

    更新数据的主要方法是 fetch 和 append_data。
    """

    def __init__(
        self, store_path: str | Path, calendar, fetch_data_func: Callable | None = None
    ):
        self._id_cols = ["date", "asset"]
        self._file_path = Path(store_path)
        self._calendar = calendar
        self._fetch_data_func = fetch_data_func
        self._start_date: datetime.date | None = None
        self._end_date: datetime.date | None = None
        self._dates: list[datetime.date] = []
        try:
            self._load_date_range()
        except Exception as e:
            logger.exception(e)

        # make sure directory exists
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        return f"{self._file_path.stem}[{self.start}-{self.end}]"

    def __len__(self) -> int:
        try:
            return pl.scan_parquet(self._file_path).select(pl.len()).collect().item()
        except FileNotFoundError:
            return 0

    def default_error_handler(self, errors: list[list]):
        """默认错误处理函数"""
        pass

    def _load_date_range(self):
        """从文件中加载日期范围并缓存"""
        if not Path(self._file_path).exists():
            self._start_date = None
            self._end_date = None
            return

        self._dates = (
            pl.scan_parquet(self._file_path)
            .select(pl.col("date").unique())
            .sort("date")
            .collect()["date"]
            .to_list()
        )

        if len(self._dates):
            self._start_date = self._dates[0]
            self._end_date = self._dates[-1]
        else:
            self._start_date = None
            self._end_date = None

    def _update_date_range(self, dates: list[datetime.date]):
        """在添加增量数据之后，更新本 store 的日期范围"""
        self._dates = sorted(set(dates + self._dates))
        self._start_date = self._dates[0]
        self._end_date = self._dates[-1]

    def fetch(
        self, start: datetime.date, end: datetime.date, call_direct: bool = False
    ) -> None:
        """下载数据并保存到本 store 中"""
        if call_direct:
            assert self._fetch_data_func is not None
            df = self._fetch_data_func(start, end)
            self.append_data(df)
            return

        start = self._calendar.ceil(start)
        end = self._calendar.floor(end)

        expected_dates = self._calendar.get_trade_dates(start, end)
        missing_dates = set(expected_dates) - set(self._dates)
        if len(missing_dates) == 0:
            return

        if self._fetch_data_func is None:
            raise ValueError("缓存中没有足够的数据，且未提供fetch_data_func方法")

        df = self._fetch_data_func(missing_dates)

        self.append_data(df)

    def get_and_fetch(
        self, start: datetime.date, end: datetime.date, call_direct: bool = False
    ) -> pd.DataFrame:
        """根据指定的日期范围加载数据。

        如果本地缓存中包含完整的数据，则从缓存中加载；
        如果数据不足，则调用fetch_data_func方法获取数据。

        Args:
            start: 开始日期
            end: 结束日期

        Returns:
            DataFrame: 包含指定日期范围内数据的DataFrame

        Raises:
            ValueError: 如果未提供fetch_data_func且缓存中没有足够数据
        """
        self.fetch(start, end, call_direct)

        return self.get(start=start, end=end)

    def update(self) -> None:
        """更新数据到最新的交易日

        从当前存储的最后日期开始，更新到最近的交易日。
        如果存储为空，则从一个默认的起始日期开始。
        """
        start = self.end or self._calendar.epoch

        now = datetime.datetime.now(tz=TZ)
        end = self._calendar.floor(now.date(), now.time())

        logger.info("开始更新日线数据: {} 到 {}", start, end)

        self.fetch(start, end)

        logger.info("日线数据更新完成")

    def append_data(self, df: pd.DataFrame) -> None:
        """追加数据到Parquet文件

        如果新数据与现有数据有重叠，会自动去重，保留最新的数据。
        数据在写入前会按 date 和 asset 排序，以优化查询性能。

        Args:
            df: 要追加的数据
        """
        if df is None or df.empty:
            return

        if len(self._dates) == 0:
            write_index = df.index.name is not None
            df.to_parquet(self._file_path, index=write_index)
            self._update_date_range(df["date"].unique().tolist())
            return

        incremental = pl.from_pandas(df).lazy()
        base = pl.scan_parquet(self._file_path)

        combined = pl.concat([base, incremental])
        deduped = combined.unique(subset=self._id_cols, keep="last").sort(self._id_cols)

        dates = deduped.select(pl.col("date").unique()).collect()["date"]
        self._update_date_range(dates.to_list())

        sorted_df = deduped.sort(by=self._id_cols)

        # 写入文件
        sorted_df.collect().write_parquet(self._file_path, compression="lz4")

    @property
    def start(self) -> datetime.date | None:
        """获取数据起始日期"""
        return self._start_date

    @property
    def end(self) -> datetime.date | None:
        """获取数据终止日期"""
        return self._end_date

    @property
    def total_dates(self) -> int:
        return len(self._dates)

    @property
    def size(self) -> int:
        return len(self)

    def get(
        self,
        assets: list[str] | None = None,
        start: datetime.date | None = None,
        end: datetime.date | None = None,
    ) -> pd.DataFrame:
        """查询在[start, end]间 asset 列在 assets 中的记录

        Args:
            assets: 资产代码列表(可选)
            start: 开始日期（可选）
            end: 结束日期（可选）

        Returns:
            DataFrame: 查询结果
        """
        lazy_df = pl.scan_parquet(self._file_path)

        filters = []

        if assets is not None:
            if isinstance(assets, str):
                assets = [assets]
            filters.append(pl.col("asset").is_in(assets))

        if start is not None:
            filters.append(pl.col("date") >= start)

        if end is not None:
            filters.append(pl.col("date") <= end)

        if filters:
            df = lazy_df.filter(pl.all_horizontal(filters)).collect().to_pandas()
        else:
            df = lazy_df.collect().to_pandas()

        df["date"] = df["date"].dt.date
        return df

    def get_by_date(self, date: datetime.date) -> pd.DataFrame:
        """查询截面数据"""
        df = (
            pl.scan_parquet(self._file_path)
            .filter(pl.col("date") == date)
            .collect()
            .to_pandas()
        )

        df["date"] = df["date"].dt.date
        return df


class Bars:
    def __init__(self):
        self._store: ParquetUnifiedStorage | None = None

    @property
    def store(self) -> ParquetUnifiedStorage:
        if self._store is None:
            raise RuntimeError("bars store 未初始化")
        return self._store

    def connect(self, store_path: str) -> None:
        if self._store is not None:
            logger.warning("重加载 bars store")

        calendar = Path(store_path).parent / "calendar.parquet"
        self._store = ParquetUnifiedStorage(
            store_path, CalendarModel(calendar), fetch_bars_ext
        )

    def __getattr__(self, name: str):
        if name in ("start", "end", "total_dates", "size"):
            return getattr(self.store, name)

    def get_bars_in_range(
        self,
        start: datetime.date,
        end: datetime.date | None = None,
        assets: list[str] | None = None,
        adjust: str = "qfq",
    ) -> pd.DataFrame:
        """获取日线数据并进行复权。

        参数：
            assets: 需要获取的股票列表
            start: 开始日期
            end: 结束日期，默认为 None，表示获取缓存中最后一个交易日
            adjust: 复权方式，默认为 "qfq", None 表示不复权, "hfq"表示后复权。
        """
        data = self.store.get(assets, start, end)

        if adjust == "qfq":
            data = qfq_adjustment(data)
        elif adjust == "hfq":
            data = hfq_adjustment(data)

        return data

    def get_bars(
        self,
        n: int,
        end: datetime.date | None = None,
        assets: list[str] | None = None,
        adjust: str = "qfq",
    ) -> pd.DataFrame:
        """获取最近 n 个交易日的行情数据

        Args:
            n (int): 最近 n 个交易日
            end (datetime.date | None, optional): 结束日期，默认为 None，表示获取缓存中最后一个交易日。 Defaults to None.
            assets (list[str] | None, optional): 获取指定股票的行情数据，默认为 None，表示获取所有股票。 Defaults to None.
            adjust (str, optional): 调整方式，默认为 "qfq"，表示前复权。可选值有 "qfq"、"hfq"、"none"。 Defaults to "qfq".
        """
        assert self._calendar is not None
        end_date = self._calendar.floor(end or datetime.date.today(), now().time())
        start_date = self._calendar.shift(end_date, -n + 1)

        return self.get_bars_in_range(start_date, end_date, assets, adjust)
