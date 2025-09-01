#!/usr/bin/env python3
"""
UBL因子分析实现
基于东吴证券研报《上下影线，蜡烛好还是威廉好？》
实现UBL因子并使用alphalens进行回测分析
"""

import datetime
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# 添加startup.py路径
sys.path.insert(0, os.path.expanduser("./scripts"))
from data import *


def calculate_upper_shadow(bars):
    """
    计算上影线比率
    上影线 = high - max(open, close)
    归一化：上影线 / (high - low)
    """
    high = bars["high"]
    low = bars["low"]
    open_price = bars["open"]
    close = bars["close"]

    upper_shadow = high - np.maximum(open_price, close)
    # 避免除零错误
    range_hl = high - low + 1e-7

    return upper_shadow / range_hl


def calculate_lower_shadow(bars):
    """
    计算下影线比率
    下影线 = min(open, close) - low
    归一化：下影线 / (high - low)
    """
    high = bars["high"]
    low = bars["low"]
    open_price = bars["open"]
    close = bars["close"]

    lower_shadow = np.minimum(open_price, close) - low
    # 避免除零错误
    range_hl = high - low + 1e-7

    return lower_shadow / range_hl


def calculate_williams_r_up(bars):
    """
    计算威廉指标上部分
    WR_up = (high - close) / (high - low)
    """
    high = bars["high"]
    low = bars["low"]
    close = bars["close"]

    wr_up = (high - close) / (high - low + 1e-7)
    return wr_up


def calculate_williams_r_down(bars):
    """
    计算威廉指标下部分
    WR_down = (close - low) / (high - low)
    """
    high = bars["high"]
    low = bars["low"]
    close = bars["close"]

    wr_down = (close - low) / (high - low + 1e-7)
    return wr_down


def calculate_ubl_factor(bars, lookback_period=20):
    """
    计算UBL因子

    Args:
        bars: 包含OHLC数据的DataFrame
        lookback_period: 回看周期

    Returns:
        UBL因子值的Series
    """
    # 计算各个组成部分
    upper_shadow = calculate_upper_shadow(bars)
    lower_shadow = calculate_lower_shadow(bars)
    wr_up = calculate_williams_r_up(bars)
    wr_down = calculate_williams_r_down(bars)

    # 转换为DataFrame便于滚动计算
    df = pd.DataFrame(
        {
            "upper_shadow": upper_shadow,
            "lower_shadow": lower_shadow,
            "wr_up": wr_up,
            "wr_down": wr_down,
        }
    )

    # 计算滚动均值
    rolling_upper_shadow = df["upper_shadow"].rolling(window=lookback_period).mean()
    rolling_lower_shadow = df["lower_shadow"].rolling(window=lookback_period).mean()
    rolling_wr_up = df["wr_up"].rolling(window=lookback_period).mean()
    rolling_wr_down = df["wr_down"].rolling(window=lookback_period).mean()

    # UBL因子组合（根据研报，上影线和WR_up为负向因子，下影线和WR_down为正向因子）
    ubl_factor = (rolling_lower_shadow + rolling_wr_down) - (
        rolling_upper_shadow + rolling_wr_up
    )

    return ubl_factor


def prepare_factor_data(start_date, end_date, universe_size=100):
    """
    准备因子数据和价格数据

    Args:
        start_date: 开始日期
        end_date: 结束日期
        universe_size: 股票池大小

    Returns:
        factor_data: 因子数据 (MultiIndex: date, asset)
        prices: 价格数据 (Index: date, Columns: asset)
    """
    print(f"Loading data from {start_date} to {end_date} for {universe_size} stocks...")

    # 加载数据
    bars_data = load_bars(start_date, end_date, universe_size)

    print(f"Loaded data shape: {bars_data.shape}")
    print(
        f"Date range: {bars_data.index.get_level_values('date').min()} to {bars_data.index.get_level_values('date').max()}"
    )
    print(
        f"Number of assets: {len(bars_data.index.get_level_values('asset').unique())}"
    )

    # 准备因子数据
    factor_data = []
    prices_data = []

    # 按资产分组计算因子
    for asset in bars_data.index.get_level_values("asset").unique():
        asset_data = bars_data.xs(asset, level="asset")

        if len(asset_data) < 30:  # 确保有足够的数据
            continue

        # 计算UBL因子
        ubl_values = calculate_ubl_factor(asset_data, lookback_period=20)

        # 创建因子DataFrame
        factor_df = pd.DataFrame(
            {"date": asset_data.index, "asset": asset, "factor": ubl_values}
        )
        factor_df = factor_df.dropna()

        # 创建价格DataFrame
        price_df = pd.DataFrame(
            {"date": asset_data.index, "asset": asset, "price": asset_data["close"]}
        )

        factor_data.append(factor_df)
        prices_data.append(price_df)

    # 合并数据
    if not factor_data:
        raise ValueError("No valid factor data generated")

    factor_combined = pd.concat(factor_data, ignore_index=True)
    prices_combined = pd.concat(prices_data, ignore_index=True)

    # 转换为alphalens需要的格式
    # 因子数据：MultiIndex (date, asset)
    factor_series = factor_combined.set_index(["date", "asset"])["factor"]

    # 价格数据：pivot表格式 (date为index, asset为columns)
    prices_pivot = prices_combined.pivot(index="date", columns="asset", values="price")

    print(f"Factor data shape: {factor_series.shape}")
    print(f"Prices data shape: {prices_pivot.shape}")

    return factor_series, prices_pivot


def run_alphalens_analysis(factor_data, prices, periods=(1, 5, 10)):
    """
    运行alphalens分析

    Args:
        factor_data: 因子数据
        prices: 价格数据
        periods: 持有期
    """
    try:
        from alphalens.performance import factor_alpha_beta, mean_return_by_quantile
        from alphalens.plotting import plot_quantile_returns_bar
        from alphalens.tears import create_full_tear_sheet
        from alphalens.utils import get_clean_factor_and_forward_returns
    except ImportError:
        print(
            "Error: alphalens not installed. Please install with: pip install alphalens-reloaded"
        )
        return

    print("Running alphalens analysis...")

    # 获取清洗后的因子数据和前向收益
    try:
        clean_factor_data = get_clean_factor_and_forward_returns(
            factor_data,
            prices,
            quantiles=5,  # 分为5个分位数
            periods=periods,
            max_loss=0.35,  # 最大缺失值比例
            zero_aware=False,
        )

        print(f"Clean factor data shape: {clean_factor_data.shape}")
        print("\nFactor data summary:")
        print(clean_factor_data.head())

        # 创建完整的分析报告
        print("\nGenerating full tear sheet...")
        create_full_tear_sheet(clean_factor_data, long_short=True, group_neutral=False)

        # 计算分位数收益
        print("\nCalculating quantile returns...")
        mean_returns = mean_return_by_quantile(clean_factor_data)
        print(mean_returns[0])

        # 计算alpha和beta
        print("\nCalculating alpha and beta...")
        alpha, beta = factor_alpha_beta(clean_factor_data)
        print(f"Alpha: {alpha}")
        print(f"Beta: {beta}")

        return clean_factor_data

    except Exception as e:
        print(f"Error in alphalens analysis: {e}")
        return None


def main():
    """主函数"""
    # 设置参数
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    universe_size = 50  # 使用较小的股票池进行测试

    try:
        # 准备数据
        factor_data, prices = prepare_factor_data(start_date, end_date, universe_size)

        # 运行alphalens分析
        clean_factor_data = run_alphalens_analysis(factor_data, prices)

        if clean_factor_data is not None:
            print("\nUBL Factor Analysis completed successfully!")
            print(f"Analysis period: {start_date} to {end_date}")
            print(f"Universe size: {universe_size}")
            print(f"Factor data points: {len(factor_data)}")
        else:
            print("Analysis failed.")

    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
