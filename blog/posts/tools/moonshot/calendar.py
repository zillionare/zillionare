"""日历存储模块

负责日历数据的存储和更新。
"""

import datetime
import pandas as pd
from pathlib import Path
from loguru import logger
import tushare as ts

epoch = datetime.date(2005, 1, 1)


def fetch_calendar(start: datetime.date) -> pd.DataFrame:
    """从tushare获取交易日历，并保存到SQLite数据库

    Returns:
        包含交易日历的DataFrame
    """
    logger.info(f"获取从 {start} 起的交易日历")

    pro = ts.pro_api()

    # 获取交易日历数据
    df = pro.trade_cal(exchange="SSE", start_date=epoch.strftime("%Y%m%d"))

    if df is None or df.empty:
        logger.warning("没有获取到交易日历数据")
        return pd.DataFrame()

    # 转换日期格式
    df["date"] = pd.to_datetime(df["cal_date"], format="%Y%m%d").dt.date
    df["prev"] = pd.to_datetime(df["pretrade_date"], format="%Y%m%d").dt.date

    df = df.sort_values("date").set_index("date")
    return df[["is_open", "prev"]]


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
