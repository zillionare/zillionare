import datetime
import sys
import time
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

import numpy as np
import pandas as pd
import polars as pl
import quantstats as qs
from helper import fetch_bars, resample_to_month
from loguru import logger


class StrategyAnalyzer:
    """策略分析器，通过代理模式集成QuantStats的分析功能"""
    def __init__(self, strategy_returns: pd.Series, benchmark_returns: Optional[pd.Series] = None):
        """
        初始化分析器
        
        参数:
            strategy_returns: 策略收益率序列（索引为时间）
            benchmark_returns: 基准收益率序列（可选）
        """
        self.strategy_returns = self._validate_returns(strategy_returns, "策略收益率")
        self.benchmark_returns = self._validate_returns(benchmark_returns, "基准收益率") if benchmark_returns is not None else None
        
        # 初始化QuantStats代理方法
        self._setup_proxy_methods()
    
    def _validate_returns(self, returns: pd.Series, name: str) -> pd.Series:
        """验证收益率序列的有效性"""
        if not isinstance(returns, pd.Series):
            raise TypeError(f"{name}必须是pandas Series类型")
        if returns.index.inferred_type not in ['datetime64', 'timedelta64', 'date', 'period']:
            raise ValueError(f"{name}的索引必须是时间类型，当前类型: {returns.index.inferred_type}")
        if returns.isna().any():
            raise ValueError(f"{name}中包含缺失值，请先处理")
        return returns
    
    def _setup_proxy_methods(self) -> None:
        """动态设置QuantStats的代理方法"""
        # 核心指标代理方法
        self.sharpe = lambda: qs.stats.sharpe(self.strategy_returns)
        self.max_drawdown = lambda: qs.stats.max_drawdown(self.strategy_returns)
        self.cagr = lambda: qs.stats.cagr(self.strategy_returns)
        self.alpha = lambda: qs.stats.information_ratio(self.strategy_returns, self.benchmark_returns) if self.benchmark_returns is not None else None
        self.beta = lambda: qs.stats.volatility(self.strategy_returns) if self.benchmark_returns is not None else None
        
        # 报告生成代理方法
        def generate_html_report(output: str = "strategy_report.html", title: str = "策略绩效报告"):
            """生成HTML格式的完整报告"""
            qs.reports.html(
                self.strategy_returns,
                benchmark=self.benchmark_returns,
                output=output,
                title=title
            )
        
        def generate_tear_sheet():
            """生成简要的绩效分析摘要（适用于Jupyter Notebook）"""
            qs.reports.basic(
                self.strategy_returns,
                benchmark=self.benchmark_returns,
                title="策略绩效分析"
            )
        
        def plot_returns():
            """绘制策略累计收益率曲线"""
            qs.plots.returns(self.strategy_returns)
        
        def plot_drawdown():
            """绘制最大回撤曲线"""
            qs.plots.drawdown(self.strategy_returns)
        
        # 绑定代理方法到当前实例
        self.generate_html_report = generate_html_report
        self.generate_tear_sheet = generate_tear_sheet
        self.plot_returns = plot_returns
        self.plot_drawdown = plot_drawdown
    
    def get_core_metrics(self) -> pd.DataFrame:
        """获取核心绩效指标汇总"""
        metrics = {
            "年化收益率": self.cagr(),
            "夏普比率": self.sharpe(),
            "最大回撤": self.max_drawdown(),
        }
        
        # 如果有基准数据，添加超额收益指标
        if self.benchmark_returns is not None:
            metrics.update({
                "阿尔法(α)": self.alpha(),
                "贝塔(β)": self.beta(),
                "信息比率": qs.stats.information_ratio(self.strategy_returns, self.benchmark_returns)
            })
        
        return pd.DataFrame(list(metrics.items()), columns=["指标", "值"])
    
class Moonshot:
    """量化回测框架类
    
    实现股票筛选、回测和报告功能
    """
    
    def __init__(self, daily_bars:pd.DataFrame):
        """初始化Moonshot实例
        
        Args:
            daily_bars: 列字段包含date, asset以及open, close的已复权数据，其中date必须为datetime.date类型
        """
        self.data: pd.DataFrame = resample_to_month(daily_bars, open='first', close='last')
        self.data['flag'] = 1

        self.strategy_returns: Optional[pd.Series] = None
        self.benchmark_returns: Optional[pd.Series] = None
        self.analyzer: StrategyAnalyzer|None = None

        
    def append_factor(self, data: pd.DataFrame, factor_col: str, resample_method: str|None=None) -> None:
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
            assert ('date' in data.columns and 'asset' in data.columns), "缺少'date'/'asset'列"
            factor_data = resample_to_month(data, **{factor_col: resample_method})
        else:
            factor_data = data[[factor_col]]

        self.data = self.data.join(factor_data, how='left')
    
    def load_dividend_yield(self, start: datetime.date, end: datetime.date) -> None:
        """从本地parquet文件加载股息率数据并添加到self.data中
        
        数据来源：data_home / "Dividenddata" / "THSDividenddata" / "Dividend.parquet"
        """
        cache_file = data_home / "dv_ttm.parquet"
        
        if not cache_file.exists():
            logger.warning("股息率数据无缓存，需要重新下载: {cache_file}")
        else:
            df = pd.read_parquet(cache_file)
    
        dividend = dividend.rename(columns={'time': 'date', 'ts_code': 'asset'})
        
        # 确保date列是datetime类型
        if not pd.api.types.is_datetime64_any_dtype(dividend['date']):
            dividend['date'] = pd.to_datetime(dividend['date'])
        
        if 'dividend_rate_ttm' not in dividend.columns:
            raise ValueError("警告：未找到dividend_rate_ttm列")
                    
        self.append_factor(dividend, 'dividend_rate_ttm', resample_method='last')
        
        # 重命名列为标准的dividend_yield
        self.data = self.data.rename(columns={'dividend_rate_ttm': 'dividend_yield'})
    
    def screen(self, screen_method, **kwargs) -> 'Moonshot':
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
            logger.info(f"{screen_method.__name__} 筛选结果：\n{self.data[self.data['flag'] == 1]}")

            # 当月选股，下月开仓
            flags = flags.groupby(level='asset').shift(1).fillna(0).astype(int)
            
            # 与现有flag进行逻辑与运算
            self.data['flag'] = self.data['flag'] & flags
        else:
            raise ValueError("screen_method 必须是可调用对象")

        return self
    
    def continuous_dividend_screen(self, min_years: int = 2, lookback_years: int = 3) -> pd.Series:
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
        required_columns = ['ts_code', 'end_date', 'dividPlanAnnounceDate']
        missing_columns = [col for col in required_columns if col not in df_dividend.columns]
        if missing_columns:
            raise ValueError(f"分红数据缺少必要字段: {missing_columns}")
        
        # 转换日期字段
        df_dividend['end_date'] = pd.to_datetime(df_dividend['end_date'])
        df_dividend['dividPlanAnnounceDate'] = pd.to_datetime(df_dividend['dividPlanAnnounceDate'])
        df_dividend['year'] = df_dividend['end_date'].dt.year
        
        # 如果有现金分红字段，只考虑现金分红大于0的记录
        if 'cash_div' in df_dividend.columns:
            df_dividend = df_dividend[df_dividend['cash_div'] > 0]
        
        # 获取所有调仓日期
        rebalance_dates = self.data.index.get_level_values('month').unique()
        
        # 初始化结果Series
        continuous_flags = pd.Series(0, index=self.data.index, name='continuous_dividend_flag')
        
        for rebalance_date in rebalance_dates:
            # 转换为datetime
            if isinstance(rebalance_date, pd.Period):
                current_date = rebalance_date.to_timestamp()
            else:
                current_date = pd.to_datetime(rebalance_date)
            
            # 时间范围筛选
            lookback_date = current_date - pd.DateOffset(years=lookback_years)
            df_period = df_dividend[
                (df_dividend['dividPlanAnnounceDate'] >= lookback_date) & 
                (df_dividend['dividPlanAnnounceDate'] <= current_date)
            ].copy()
            
            # 去重：同一股票同一年只保留一条记录
            df_period = df_period.sort_values(['ts_code', 'year', 'dividPlanAnnounceDate'])
            df_period = df_period.drop_duplicates(subset=['ts_code', 'year'], keep='last')
            
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
    
    def _check_continuous_dividend(self, df_dividend: pd.DataFrame, 
                                 current_date: pd.Timestamp, 
                                 min_years: int) -> List[str]:
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
        
        for ts_code, group in df_dividend.groupby('ts_code'):
            years = sorted(group['year'].unique())
            
            # 至少要有min_years年的分红记录
            if len(years) < min_years:
                continue
                
            # 最新分红年份不能太久远（不超过2年前）
            if max(years) < (current_year - 2):
                continue
                
            # 检查是否存在连续的年份
            has_continuous = False
            for i in range(len(years) - min_years + 1):
                consecutive_years = years[i:i + min_years]
                # 检查这min_years年是否连续
                if all(consecutive_years[j+1] - consecutive_years[j] == 1 
                      for j in range(len(consecutive_years)-1)):
                    has_continuous = True
                    break
            
            if has_continuous:
                continuous_stocks.append(ts_code)
        
        return continuous_stocks
    
    def calculate_returns(self)->'Moonshot':
        """计算策略收益率和基准收益率（向量化实现）
        
        使用向量化操作计算：
        1. 策略收益：每月flag=1的股票的等权平均收益
        2. 基准收益：每月所有股票的等权平均收益
        """
        if self.data is None or self.data.empty:
            raise ValueError("警告：数据为空，无法计算收益率")
                
        # 计算所有股票的月收益率 (close - open) / open
        self.data['monthly_return'] = (self.data['close'] - self.data['open']) / self.data['open']
        
        # 按月分组计算策略收益（flag=1的股票等权平均）
        def calculate_strategy_return(group):
            selected = group[group.get('flag', 0) == 1]
            if len(selected) > 0:
                return selected['monthly_return'].mean()
            else:
                return 0.0
        
        # 向量化计算策略收益
        strategy_returns = self.data.groupby(level='month').apply(calculate_strategy_return)
        strategy_returns.name = 'strategy_returns'

        # 向量化计算基准收益（所有股票等权平均）
        benchmark_returns = self.data.groupby(level='month')['monthly_return'].mean()
        benchmark_returns.name = 'benchmark_returns'

        # 将PeriodIndex转换为DatetimeIndex以兼容QuantStats
        if isinstance(strategy_returns.index, pd.PeriodIndex):
            strategy_returns.index = strategy_returns.index.to_timestamp()
        if isinstance(benchmark_returns.index, pd.PeriodIndex):
            benchmark_returns.index = benchmark_returns.index.to_timestamp()

        # 存储结果
        self.strategy_returns = strategy_returns
        self.benchmark_returns = benchmark_returns
        
        self.analyzer = StrategyAnalyzer(
            strategy_returns=self.strategy_returns,
            benchmark_returns=self.benchmark_returns
        )

        return self


    def report(self, output: str = "strategy_report.html", title: str = "策略绩效报告"):
        """生成策略报告
        
        Args:
            output: 报告输出路径，默认为"strategy_report.html"
            title: 报告标题，默认为"策略绩效报告"
        """
        if self.analyzer is None:
            raise ValueError("请先调用calculate_returns方法计算收益率")
        
        self.analyzer.generate_html_report(output=output, title=title)
        
        return self


if __name__ == '__main__':

    import sys
    from pathlib import Path

    startup_file = Path("~/courses/blog/.startup/").expanduser()
    sys.path.append(str(startup_file))
    from helper import (ParquetUnifiedStorage, dividend_yield_screen,
                        fetch_bars, fetch_dv_ttm)
    from startup import data_home, load_bars, pro_api


    start = datetime.date(2018, 1, 1)
    end = datetime.date(2023, 12, 31)

    bars_store = ParquetUnifiedStorage(store_path=data_home / "rw/bars.parquet", fetch_data_func=fetch_bars)

    barss = bars_store.load_data(start, end)
    ms = Moonshot(barss)

    dv_store = ParquetUnifiedStorage(store_path=data_home / "rw/dv_ttm.parquet", fetch_data_func=fetch_dv_ttm)

    dv_ttm = dv_store.load_data(start, end)
    
    ms.append_factor(dv_ttm, "dv_ttm", resample_method = 'last')
    # 添加股息率筛选器
    (ms.screen(dividend_yield_screen, data = ms.data, n=500)
       .calculate_returns()
       .report())
