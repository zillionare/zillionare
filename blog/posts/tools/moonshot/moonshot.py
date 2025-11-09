import datetime
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

import numpy as np
import pandas as pd
import polars as pl
import quantstats.reports
import quantstats.stats
from helper import resample_to_month
from loguru import logger


class Moonshot:
    """量化回测框架类

    实现股票筛选、回测和报告功能
    """

    def __init__(self, daily_bars: pd.DataFrame):
        """初始化Moonshot实例

        Args:
            daily_bars: 列字段包含date, asset以及open, close的已复权数据，其中date必须为datetime.date类型
        """
        self.data: pd.DataFrame = resample_to_month(
            daily_bars, open="first", close="last"
        )
        self.data["flag"] = 1

        self.strategy_returns: Optional[pd.Series] = None
        self.benchmark_returns: Optional[pd.Series] = None

    def append_factor(
        self, data: pd.DataFrame, factor_col: str, resample_method: str | None = None
    ) -> None:
        """将因子数据添加到回测数据(即self.data)中。

        如果resample_method参数不为None, 则需要重采样为月频，并且使用resample_method指定的方法。否则，认为因子已经是月频的，且以'month', 'asset'为索引 ，将直接添加到回测数据中。

        使用本方法，一次只能添加一个因子。

        Args:
            data: 因子数据，需包含'date'和'asset'列
            factor_col: 因子列名
            resample_method: 如果需要对因子重采样，此列为重采样方法。
        """
        # 检查必需的列是否存在
        if factor_col not in data.columns:
            raise ValueError(f"因子数据中不存在列: {factor_col}")

        if resample_method is not None:
            assert (
                "date" in data.columns and "asset" in data.columns
            ), "缺少'date'/'asset'列"
            factor_data = resample_to_month(data, **{factor_col: resample_method})
        else:
            factor_data = data[[factor_col]]

        self.data = self.data.join(factor_data, how="left")

    def load_dividend_yield(self, start: datetime.date, end: datetime.date) -> None:
        """从本地parquet文件加载股息率数据并添加到self.data中

        数据来源：data_home / "Dividenddata" / "THSDividenddata" / "Dividend.parquet"
        """
        cache_file = data_home / "dv_ttm.parquet"

        if not cache_file.exists():
            logger.warning("股息率数据无缓存，需要重新下载: {cache_file}")
        else:
            df = pd.read_parquet(cache_file)

        dividend = dividend.rename(columns={"time": "date", "ts_code": "asset"})

        # 确保date列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(dividend["date"]):
            dividend["date"] = pd.to_datetime(dividend["date"])

        if "dividend_rate_ttm" not in dividend.columns:
            raise ValueError("警告：未找到dividend_rate_ttm列")

        self.append_factor(dividend, "dividend_rate_ttm", resample_method="last")

        # 重命名列为标准的dividend_yield
        self.data = self.data.rename(columns={"dividend_rate_ttm": "dividend_yield"})

    def screen(self, screen_method, **kwargs) -> "Moonshot":
        """应用股票筛选器

        Args:
            screen_method: 筛选方法（可调用对象）
            **kwargs: 筛选器参数

        Returns:
            Moonshot: 返回自身以支持链式调用
        """
        if self.data is None or self.data.empty:
            raise ValueError("警告：数据为空，无法应用筛选器")

        if callable(screen_method):
            flags = screen_method(**kwargs)

            # 当月选股，下月开仓
            flags = flags.groupby(level="asset").shift(1).fillna(0).astype(int)

            # 与现有flag进行逻辑与运算
            self.data["flag"] = self.data["flag"] & flags
        else:
            raise ValueError("screen_method 必须是可调用对象")

        return self

    def continuous_dividend_screen(
        self, min_years: int = 2, lookback_years: int = 3
    ) -> pd.Series:
        """连续分红筛选方法

        筛选在指定时间范围内连续分红的股票

        Args:
            min_years: 最少连续分红年数，默认2年
            lookback_years: 回看年数，默认3年

        Returns:
            pd.Series: 筛选标记，1表示符合条件，0表示不符合
        """
        logger.info(f"开始进行连续{min_years}年分红筛选...")

        # 加载分红数据
        dividend_file = data_home / "Dividenddata" / "dividenddata.parquet"

        if not dividend_file.exists():
            raise FileNotFoundError(f"分红数据文件不存在: {dividend_file}")

        # 读取分红数据
        df_dividend = pd.read_parquet(dividend_file)

        # 确保必要字段存在
        required_columns = ["ts_code", "end_date", "dividPlanAnnounceDate"]
        missing_columns = [
            col for col in required_columns if col not in df_dividend.columns
        ]
        if missing_columns:
            raise ValueError(f"分红数据缺少必要字段: {missing_columns}")

        # 转换日期字段
        df_dividend["end_date"] = pd.to_datetime(df_dividend["end_date"])
        df_dividend["dividPlanAnnounceDate"] = pd.to_datetime(
            df_dividend["dividPlanAnnounceDate"]
        )
        df_dividend["year"] = df_dividend["end_date"].dt.year

        # 如果有现金分红字段，只考虑现金分红大于0的记录
        if "cash_div" in df_dividend.columns:
            df_dividend = df_dividend[df_dividend["cash_div"] > 0]

        # 获取所有调仓日期
        rebalance_dates = self.data.index.get_level_values("month").unique()

        # 初始化结果Series
        continuous_flags = pd.Series(
            0, index=self.data.index, name="continuous_dividend_flag"
        )

        for rebalance_date in rebalance_dates:
            # 转换为datetime
            if isinstance(rebalance_date, pd.Period):
                current_date = rebalance_date.to_timestamp()
            else:
                current_date = pd.to_datetime(rebalance_date)

            # 时间范围筛选
            lookback_date = current_date - pd.DateOffset(years=lookback_years)
            df_period = df_dividend[
                (df_dividend["dividPlanAnnounceDate"] >= lookback_date)
                & (df_dividend["dividPlanAnnounceDate"] <= current_date)
            ].copy()

            # 去重：同一股票同一年只保留一条记录
            df_period = df_period.sort_values(
                ["ts_code", "year", "dividPlanAnnounceDate"]
            )
            df_period = df_period.drop_duplicates(
                subset=["ts_code", "year"], keep="last"
            )

            # 筛选连续分红股票
            continuous_stocks = self._check_continuous_dividend(
                df_period, current_date, min_years
            )

            # 更新当期标记
            current_assets = self.data.loc[rebalance_date].index
            for asset in current_assets:
                if asset in continuous_stocks:
                    continuous_flags.loc[(rebalance_date, asset)] = 1

        logger.info(f"连续{min_years}年分红筛选完成")
        return continuous_flags

    def _check_continuous_dividend(
        self, df_dividend: pd.DataFrame, current_date: pd.Timestamp, min_years: int
    ) -> List[str]:
        """检查连续分红条件的辅助方法

        Args:
            df_dividend: 分红数据DataFrame
            current_date: 当前调仓日期
            min_years: 最少连续分红年数

        Returns:
            List[str]: 符合连续分红条件的股票代码列表
        """
        continuous_stocks = []
        current_year = current_date.year

        for ts_code, group in df_dividend.groupby("ts_code"):
            years = sorted(group["year"].unique())

            # 至少要有min_years年的分红记录
            if len(years) < min_years:
                continue

            # 最新分红年份不能太久远（不超过2年前）
            if max(years) < (current_year - 2):
                continue

            # 检查是否存在连续的年份
            has_continuous = False
            for i in range(len(years) - min_years + 1):
                consecutive_years = years[i : i + min_years]
                # 检查这min_years年是否连续
                if all(
                    consecutive_years[j + 1] - consecutive_years[j] == 1
                    for j in range(len(consecutive_years) - 1)
                ):
                    has_continuous = True
                    break

            if has_continuous:
                continuous_stocks.append(ts_code)

        return continuous_stocks

    def calculate_returns(self, long_only:bool) -> "Moonshot":
        """基于flag计算策略收益

        Args:
            long_only: 是否只做多

        Returns:
            pd.Series: 策略收益序列
        """
        self.benchmark_returns = self._calculate_benchmark_returns()

        data_with_flag = self.data.copy()
        # 当月的收益，归因到上月的因子
        flag = data_with_flag["flag"]
        data_with_flag["flag"] = flag.groupby(level="asset").shift(1)

        # 计算月度收益 (MOM)
        data_with_flag["mom_returns"] = data_with_flag.groupby(level="asset")[
            "close"
        ].pct_change()

        # 计算COO收益 (Close/Open-1)
        data_with_flag["coo_returns"] = (
            data_with_flag["close"] / data_with_flag["open"] - 1
        )

        # 计算is_new标记
        prev = data_with_flag.groupby("asset")["flag"].shift(1)
        prev = prev.where(prev.abs() == 1, 0)

        # 判断新开仓
        data_with_flag["is_new"] = (
            (data_with_flag["flag"].abs() == 1) & (data_with_flag["flag"] != prev)
        ).astype(bool)

        # 获取所有月份并排序
        months = sorted(data_with_flag.index.get_level_values("month").unique())

        # 计算每月收益
        monthly_returns = []

        divider = 1 if long_only else 2
        for month in months:
            month_data = data_with_flag.loc[month]

            # 计算多头收益
            long_returns = self._calculate_position_returns(month_data, position_type=1)

            # 计算空头收益
            if long_only:
                short_returns = 0
            else:
                short_returns = self._calculate_position_returns(
                    month_data, position_type=-1
                )

            # 组合收益
            monthly_returns.append((long_returns + short_returns) / divider)

        # 创建收益率序列
        self.strategy_returns = pd.Series(monthly_returns, index=months)

        return self

    def _calculate_benchmark_returns(self) -> pd.Series:
        """计算基准收益（买入并持有策略）

        第一个月收益是 close/open-1，此后每月为 close/prev(close)-1。因此返回的收益序列长度与 month 索引等长，很好地反映了作为基准，买入并持有的收益。

        Returns:
            pd.Series: 基准收益序列，以月为单位
        """        
        # 计算第一个月的收益率
        first_month_returns = (
            (self.data["close"] / self.data["open"] - 1)
            .groupby(level="asset")
            .first()
            .mean()
        )

        # 后续使用 close
        prices = self.data["close"].unstack(level="asset")
        returns = prices.pct_change().mean(axis=1)
        returns.iloc[0] = first_month_returns

        return returns

    def _calculate_position_returns(
        self, month_data: pd.DataFrame, position_type: int
    ) -> float:
        """计算特定持仓类型的收益

        Args:
            month_data: 当月数据，包含flag, mom_returns, coo_returns, is_new列
            position_type: 持仓类型，1表示多头，-1表示空头

        Returns:
            float: 该持仓类型的平均收益
        """
        assert position_type in [1, -1], "position_type参数只能为1(多）或-1（空）"

        # 筛选符合条件的资产
        position_assets = month_data[month_data["flag"] == position_type]

        if position_assets.empty:
            return 0

        # 分离新买入和继续持有的资产
        new_assets = position_assets[position_assets["is_new"]]
        old_assets = position_assets[~position_assets["is_new"]]

        # 计算收益
        total_return = 0
        total_assets = len(position_assets)

        # 新买入资产的COO收益
        if not new_assets.empty:
            total_return += new_assets["coo_returns"].sum()

        # 继续持有资产的MOM收益
        if not old_assets.empty:
            total_return += old_assets["mom_returns"].sum()

        average_return = total_return / total_assets if total_assets > 0 else 0

        return average_return * position_type
    
    def report(
        self,
        kind: Literal["html", "full", "basic", "metrics", "plots"] = "html",
        benchmark = None,
        **kwargs,
    ):
        """生成回测报告

        Args:
            strategy: 策略收益序列
            benchmark: 基准收益序列
            kind: 报告类型,参见 quantstats.report
        """
        strategy = self.strategy_returns.to_timestamp()
        if benchmark is None:
            benchmark = self.benchmark_returns.to_timestamp()

        func = getattr(quantstats.reports, kind)
        return func(strategy, benchmark, **kwargs)

    def get_core_metrics(
        self, rf=0,
        benchmark = None
    ) -> dict:
        """返回核心评估指标

        Args:
            strategy (pd.Series): 策略收益，由 run 方法返回
            benchmark (pd.Series): 基准收益，由 run 方法返回

        Returns:
            dict: 评估指标
        """
        strategy = self.strategy_returns.to_timestamp()
        if benchmark is None:
            benchmark = self.benchmark_returns.to_timestamp()

        nv = (1 + strategy).cumprod() - 1
        metrics = {
            "cagr": quantstats.stats.cagr(strategy, rf=rf, periods=12),
            "sharpe": quantstats.stats.sharpe(strategy, rf=rf, periods=12),
            "mdd": quantstats.stats.max_drawdown(nv),
            "sortino": quantstats.stats.sortino(strategy, rf=rf, periods=12),
            "calmar": quantstats.stats.calmar(strategy),
            "win_rate": quantstats.stats.win_rate(strategy),
        }

        # 如果有基准数据，添加超额收益指标
        metrics.update(
            {
                "alpha": self.alpha(
                    periods=12,
                    benchmark = benchmark
                ),
                "beta": self.beta(
                    periods=12,
                    benchmark = benchmark
                ),
            }
        )

        return metrics
    
    def alpha(
        self, periods=12,
        benchmark = None
    ) -> float:
        """quantstats 没有直接定义 alpha/beta，需要通过 greeks 来调用

        !!! warning:
            quantstats 中的 alpha 年化方法并不准确，但为了保持数据一致性，
            我们仍然使用该方法。因为在它的 report 中，也会出现 alpha
        """
        strategy = self.strategy_returns.to_timestamp()
        if benchmark is None:
            benchmark = self.benchmark_returns.to_timestamp()

        greeks = quantstats.stats.greeks(
            strategy, benchmark, periods, prepare_returns=False
        )

        return greeks.to_dict().get("alpha", 0)  # type: ignore

    def beta(
        self, periods=12,
        benchmark=None
    ) -> float:
        """quantstats 没有直接定义 alpha/beta，需要通过 greeks 来调用"""
        strategy = self.strategy_returns.to_timestamp()
        if benchmark is None:
            benchmark = self.benchmark_returns.to_timestamp()

        greeks = quantstats.stats.greeks(
            strategy, benchmark, periods, prepare_returns=False
        )

        return greeks.to_dict().get("beta", 0)  # type: ignore

# if __name__ == "__main__":

#     import sys
#     from pathlib import Path

#     startup_file = Path("~/courses/blog/.startup/").expanduser()
#     sys.path.append(str(startup_file))
#     from docs.blog.posts.tools.moonshot.helper import (
#         ParquetUnifiedStorage,
#         dividend_yield_screen,
#     )
#     from fetchers import fetch_bars, fetch_dv_ttm, fetch_fina_audit

#     if Path("/data").exists():
#         data_home = Path("/data")
#     else:
#         data_home = Path("~/workspace/data/").expanduser()

#     start = datetime.date(2018, 1, 1)
#     end = datetime.date(2023, 12, 31)

#     bars_store = ParquetUnifiedStorage(
#         store_path=data_home / "rw/bars.parquet", fetch_data_func=fetch_bars
#     )

#     barss = bars_store.load_data(start, end)
#     ms = Moonshot(barss)

#     dv_store = ParquetUnifiedStorage(
#         store_path=data_home / "rw/dv_ttm.parquet", fetch_data_func=fetch_dv_ttm
#     )

#     dv_ttm = dv_store.load_data(start, end)

#     ms.append_factor(dv_ttm, "dv_ttm", resample_method="last")
#     # 添加股息率筛选器
#     (ms.screen(dividend_yield_screen, data=ms.data, n=500).calculate_returns().report())
