#!/usr/bin/env python3
"""
UBL因子测试脚本
简化版本，用于验证因子计算逻辑
"""

import datetime
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def generate_sample_data(n_days=252, n_assets=10):
    """
    生成模拟的OHLC数据用于测试
    """
    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", periods=n_days, freq="D")
    assets = [f"STOCK_{i:03d}" for i in range(n_assets)]

    all_data = []

    for asset in assets:
        # 生成价格序列
        base_price = 100
        returns = np.random.normal(0, 0.02, n_days)
        prices = base_price * np.exp(np.cumsum(returns))

        # 生成OHLC数据
        close = prices
        open_price = np.roll(close, 1)
        open_price[0] = base_price

        # 添加一些随机波动来生成high和low
        volatility = np.random.uniform(0.01, 0.03, n_days)
        high = np.maximum(open_price, close) * (1 + volatility)
        low = np.minimum(open_price, close) * (1 - volatility)

        # 确保价格关系正确
        high = np.maximum(high, np.maximum(open_price, close))
        low = np.minimum(low, np.minimum(open_price, close))

        volume = np.random.randint(1000000, 10000000, n_days)

        df = pd.DataFrame(
            {
                "date": dates,
                "asset": asset,
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
            }
        )

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)
    return result.set_index(["date", "asset"])


def calculate_upper_shadow(bars):
    """计算上影线比率"""
    high = bars["high"]
    low = bars["low"]
    open_price = bars["open"]
    close = bars["close"]

    upper_shadow = high - np.maximum(open_price, close)
    range_hl = high - low + 1e-7

    return upper_shadow / range_hl


def calculate_lower_shadow(bars):
    """计算下影线比率"""
    high = bars["high"]
    low = bars["low"]
    open_price = bars["open"]
    close = bars["close"]

    lower_shadow = np.minimum(open_price, close) - low
    range_hl = high - low + 1e-7

    return lower_shadow / range_hl


def calculate_williams_r_up(bars):
    """计算威廉指标上部分"""
    high = bars["high"]
    low = bars["low"]
    close = bars["close"]

    wr_up = (high - close) / (high - low + 1e-7)
    return wr_up


def calculate_williams_r_down(bars):
    """计算威廉指标下部分"""
    high = bars["high"]
    low = bars["low"]
    close = bars["close"]

    wr_down = (close - low) / (high - low + 1e-7)
    return wr_down


def calculate_ubl_factor(bars, lookback_period=20):
    """计算UBL因子"""
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

    # UBL因子组合
    ubl_factor = (rolling_lower_shadow + rolling_wr_down) - (
        rolling_upper_shadow + rolling_wr_up
    )

    return ubl_factor


def test_ubl_factor():
    """测试UBL因子计算"""
    print("Generating sample data...")
    data = generate_sample_data(n_days=252, n_assets=5)

    print(f"Data shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    print(
        f"Date range: {data.index.get_level_values('date').min()} to {data.index.get_level_values('date').max()}"
    )

    # 测试单个股票的因子计算
    asset = data.index.get_level_values("asset").unique()[0]
    asset_data = data.xs(asset, level="asset")

    print(f"\nTesting factor calculation for {asset}...")
    print(f"Asset data shape: {asset_data.shape}")

    # 计算各个组成部分
    upper_shadow = calculate_upper_shadow(asset_data)
    lower_shadow = calculate_lower_shadow(asset_data)
    wr_up = calculate_williams_r_up(asset_data)
    wr_down = calculate_williams_r_down(asset_data)

    print(
        f"Upper shadow stats: mean={upper_shadow.mean():.4f}, std={upper_shadow.std():.4f}"
    )
    print(
        f"Lower shadow stats: mean={lower_shadow.mean():.4f}, std={lower_shadow.std():.4f}"
    )
    print(f"WR up stats: mean={wr_up.mean():.4f}, std={wr_up.std():.4f}")
    print(f"WR down stats: mean={wr_down.mean():.4f}, std={wr_down.std():.4f}")

    # 计算UBL因子
    ubl_factor = calculate_ubl_factor(asset_data, lookback_period=20)

    print(f"\nUBL factor stats:")
    print(f"Mean: {ubl_factor.mean():.4f}")
    print(f"Std: {ubl_factor.std():.4f}")
    print(f"Min: {ubl_factor.min():.4f}")
    print(f"Max: {ubl_factor.max():.4f}")
    print(f"Non-null values: {ubl_factor.count()}/{len(ubl_factor)}")

    # 绘制因子时间序列
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(asset_data.index, upper_shadow, label="Upper Shadow", alpha=0.7)
    plt.plot(asset_data.index, lower_shadow, label="Lower Shadow", alpha=0.7)
    plt.title("Shadow Ratios")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(asset_data.index, wr_up, label="WR Up", alpha=0.7)
    plt.plot(asset_data.index, wr_down, label="WR Down", alpha=0.7)
    plt.title("Williams R Components")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(asset_data.index, ubl_factor, label="UBL Factor", color="red")
    plt.title("UBL Factor")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(asset_data.index, asset_data["close"], label="Close Price", color="blue")
    plt.title("Close Price")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("ubl_factor_test.png", dpi=150, bbox_inches="tight")
    plt.show()

    return data, ubl_factor


def prepare_alphalens_data(data):
    """准备alphalens格式的数据"""
    print("\nPreparing data for alphalens...")

    factor_data = []
    prices_data = []

    # 按资产分组计算因子
    for asset in data.index.get_level_values("asset").unique():
        asset_data = data.xs(asset, level="asset")

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
    factor_combined = pd.concat(factor_data, ignore_index=True)
    prices_combined = pd.concat(prices_data, ignore_index=True)

    # 转换为alphalens需要的格式
    factor_series = factor_combined.set_index(["date", "asset"])["factor"]
    prices_pivot = prices_combined.pivot(index="date", columns="asset", values="price")

    print(f"Factor data shape: {factor_series.shape}")
    print(f"Prices data shape: {prices_pivot.shape}")

    return factor_series, prices_pivot


def simple_factor_analysis(factor_data, prices):
    """简单的因子分析（不依赖alphalens）"""
    print("\nRunning simple factor analysis...")

    # 计算前向收益
    returns_1d = prices.pct_change().shift(-1)  # 1日前向收益
    returns_5d = prices.shift(-5) / prices - 1  # 5日前向收益

    # 将因子数据转换为宽表格式
    factor_pivot = factor_data.unstack("asset")

    # 对齐数据
    common_dates = factor_pivot.index.intersection(returns_1d.index)
    common_assets = factor_pivot.columns.intersection(returns_1d.columns)

    print(f"Common dates: {len(common_dates)}")
    print(f"Common assets: {len(common_assets)}")
    print(f"Factor columns: {factor_pivot.columns.tolist()}")
    print(f"Price columns: {returns_1d.columns.tolist()}")

    if len(common_assets) == 0:
        print("No common assets found, using all available assets")
        common_assets = returns_1d.columns

    factor_aligned = factor_pivot.loc[common_dates, common_assets]
    returns_1d_aligned = returns_1d.loc[common_dates, common_assets]
    returns_5d_aligned = returns_5d.loc[common_dates, common_assets]

    # 计算相关性
    correlations_1d = []
    correlations_5d = []

    for date in common_dates:
        try:
            factor_values = factor_aligned.loc[date].dropna()
            returns_1d_values = returns_1d_aligned.loc[date].dropna()
            returns_5d_values = returns_5d_aligned.loc[date].dropna()

            # 找到共同的资产
            common_assets_date = factor_values.index.intersection(
                returns_1d_values.index
            )

            if len(common_assets_date) > 2:
                factor_vals = factor_values.reindex(common_assets_date).values
                returns_1d_vals = returns_1d_values.reindex(common_assets_date).values
                returns_5d_vals = returns_5d_values.reindex(common_assets_date).values

                # 检查是否有有效值
                valid_mask = ~(np.isnan(factor_vals) | np.isnan(returns_1d_vals))
                if np.sum(valid_mask) > 2:
                    corr_1d = np.corrcoef(
                        factor_vals[valid_mask], returns_1d_vals[valid_mask]
                    )[0, 1]
                    if not np.isnan(corr_1d):
                        correlations_1d.append(corr_1d)

                valid_mask = ~(np.isnan(factor_vals) | np.isnan(returns_5d_vals))
                if np.sum(valid_mask) > 2:
                    corr_5d = np.corrcoef(
                        factor_vals[valid_mask], returns_5d_vals[valid_mask]
                    )[0, 1]
                    if not np.isnan(corr_5d):
                        correlations_5d.append(corr_5d)
        except Exception as e:
            continue

    print(f"1-day forward return correlation:")
    if correlations_1d:
        print(f"  Mean: {np.mean(correlations_1d):.4f}")
        print(f"  Std: {np.std(correlations_1d):.4f}")
        print(f"  Count: {len(correlations_1d)}")
    else:
        print("  No valid correlations calculated")

    print(f"5-day forward return correlation:")
    if correlations_5d:
        print(f"  Mean: {np.mean(correlations_5d):.4f}")
        print(f"  Std: {np.std(correlations_5d):.4f}")
        print(f"  Count: {len(correlations_5d)}")
    else:
        print("  No valid correlations calculated")

    return correlations_1d, correlations_5d


def main():
    """主函数"""
    print("=== UBL Factor Test ===")

    # 测试因子计算
    data, ubl_factor = test_ubl_factor()

    # 准备alphalens数据
    factor_series, prices_pivot = prepare_alphalens_data(data)

    # 简单因子分析
    corr_1d, corr_5d = simple_factor_analysis(factor_series, prices_pivot)

    print("\n=== Test Completed ===")
    print("Generated files:")
    print("- ubl_factor_test.png: Factor visualization")

    return factor_series, prices_pivot


if __name__ == "__main__":
    factor_data, prices = main()
