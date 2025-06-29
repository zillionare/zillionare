#!/usr/bin/env python3
"""
改进版UBL因子实现
基于东吴证券研报《上下影线，蜡烛好还是威廉好？》
修复和改进原有实现中的问题
"""

import datetime
import os
import sys
import warnings
from typing import Optional, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

# 添加startup.py路径
sys.path.insert(0, os.path.expanduser('~/workspace/cheese_course/docs/factor-analysis/assets'))


def calculate_upper_shadow_ratio(bars: pd.DataFrame) -> pd.Series:
    """
    计算上影线比率
    
    改进点：
    1. 添加类型注解
    2. 更严格的除零处理
    3. 处理异常K线（如一字板）
    """
    high = bars['high']
    low = bars['low']
    open_price = bars['open']
    close = bars['close']
    
    # 计算实体顶部
    body_top = np.maximum(open_price, close)
    
    # 计算上影线长度
    upper_shadow = high - body_top
    
    # 计算K线总长度，处理一字板情况
    total_range = high - low
    
    # 对于一字板（high == low），上影线比率为0
    mask = total_range > 1e-8  # 更严格的阈值
    upper_shadow_ratio = pd.Series(0.0, index=bars.index)
    upper_shadow_ratio[mask] = upper_shadow[mask] / total_range[mask]
    
    # 确保比率在[0, 1]范围内
    upper_shadow_ratio = np.clip(upper_shadow_ratio, 0, 1)
    
    return upper_shadow_ratio


def calculate_lower_shadow_ratio(bars: pd.DataFrame) -> pd.Series:
    """
    计算下影线比率
    
    改进点：
    1. 添加类型注解
    2. 更严格的除零处理
    3. 处理异常K线
    """
    high = bars['high']
    low = bars['low']
    open_price = bars['open']
    close = bars['close']
    
    # 计算实体底部
    body_bottom = np.minimum(open_price, close)
    
    # 计算下影线长度
    lower_shadow = body_bottom - low
    
    # 计算K线总长度
    total_range = high - low
    
    # 对于一字板，下影线比率为0
    mask = total_range > 1e-8
    lower_shadow_ratio = pd.Series(0.0, index=bars.index)
    lower_shadow_ratio[mask] = lower_shadow[mask] / total_range[mask]
    
    # 确保比率在[0, 1]范围内
    lower_shadow_ratio = np.clip(lower_shadow_ratio, 0, 1)
    
    return lower_shadow_ratio


def calculate_williams_r_components(bars: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    计算威廉指标的上下两个组成部分
    
    改进点：
    1. 同时计算两个组成部分，确保一致性
    2. 验证 WR_up + WR_down = 1
    3. 处理异常情况
    """
    high = bars['high']
    low = bars['low']
    close = bars['close']
    
    # 计算K线总长度
    total_range = high - low
    
    # 处理一字板情况
    mask = total_range > 1e-8
    
    wr_up = pd.Series(0.5, index=bars.index)  # 一字板时默认为0.5
    wr_down = pd.Series(0.5, index=bars.index)
    
    # 正常K线的计算
    wr_up[mask] = (high[mask] - close[mask]) / total_range[mask]
    wr_down[mask] = (close[mask] - low[mask]) / total_range[mask]
    
    # 确保比率在[0, 1]范围内
    wr_up = np.clip(wr_up, 0, 1)
    wr_down = np.clip(wr_down, 0, 1)
    
    # 验证一致性（WR_up + WR_down 应该等于1）
    sum_check = wr_up + wr_down
    if not np.allclose(sum_check[mask], 1.0, atol=1e-6):
        warnings.warn("Williams R components do not sum to 1, possible calculation error")
    
    return wr_up, wr_down


def calculate_ubl_factor_improved(bars: pd.DataFrame, 
                                lookback_period: int = 20,
                                min_periods: Optional[int] = None,
                                standardize: bool = True) -> pd.Series:
    """
    改进版UBL因子计算
    
    改进点：
    1. 添加min_periods参数控制最小计算周期
    2. 可选的标准化处理
    3. 更好的数据验证
    4. 处理边界情况
    
    Args:
        bars: 包含OHLC数据的DataFrame
        lookback_period: 滚动窗口大小
        min_periods: 最小有效期数，默认为lookback_period的一半
        standardize: 是否对因子进行标准化
    
    Returns:
        UBL因子值的Series
    """
    if min_periods is None:
        min_periods = max(1, lookback_period // 2)
    
    # 数据验证
    required_cols = ['high', 'low', 'open', 'close']
    if not all(col in bars.columns for col in required_cols):
        raise ValueError(f"Missing required columns: {required_cols}")
    
    if len(bars) < min_periods:
        raise ValueError(f"Insufficient data: need at least {min_periods} periods")
    
    # 计算各个组成部分
    upper_shadow_ratio = calculate_upper_shadow_ratio(bars)
    lower_shadow_ratio = calculate_lower_shadow_ratio(bars)
    wr_up, wr_down = calculate_williams_r_components(bars)
    
    # 验证影线比率的合理性
    shadow_sum = upper_shadow_ratio + lower_shadow_ratio
    if (shadow_sum > 1.01).any():  # 允许小的数值误差
        warnings.warn("Shadow ratios sum exceeds 1, possible calculation error")
    
    # 计算滚动均值
    rolling_upper_shadow = upper_shadow_ratio.rolling(
        window=lookback_period, min_periods=min_periods).mean()
    rolling_lower_shadow = lower_shadow_ratio.rolling(
        window=lookback_period, min_periods=min_periods).mean()
    rolling_wr_up = wr_up.rolling(
        window=lookback_period, min_periods=min_periods).mean()
    rolling_wr_down = wr_down.rolling(
        window=lookback_period, min_periods=min_periods).mean()
    
    # UBL因子组合
    # 正向因子：下影线（支撑强）+ WR_down（收盘价相对较高）
    positive_component = rolling_lower_shadow + rolling_wr_down
    
    # 负向因子：上影线（压力大）+ WR_up（收盘价相对较低）
    negative_component = rolling_upper_shadow + rolling_wr_up
    
    # 最终UBL因子
    ubl_factor = positive_component - negative_component
    
    # 可选的标准化处理
    if standardize:
        # 使用滚动标准化，避免前瞻偏差
        rolling_mean = ubl_factor.rolling(
            window=lookback_period * 2, min_periods=lookback_period).mean()
        rolling_std = ubl_factor.rolling(
            window=lookback_period * 2, min_periods=lookback_period).std()
        
        # 避免除零
        rolling_std = rolling_std.fillna(1.0)
        rolling_std[rolling_std < 1e-8] = 1.0
        
        ubl_factor = (ubl_factor - rolling_mean) / rolling_std
    
    return ubl_factor


def validate_ubl_calculation(bars: pd.DataFrame, ubl_factor: pd.Series) -> dict:
    """
    验证UBL因子计算的合理性
    
    Returns:
        包含验证结果的字典
    """
    validation_results = {}
    
    # 1. 检查数据完整性
    validation_results['data_completeness'] = {
        'total_periods': len(bars),
        'valid_ubl_values': ubl_factor.count(),
        'missing_ratio': (len(ubl_factor) - ubl_factor.count()) / len(ubl_factor)
    }
    
    # 2. 检查因子分布
    validation_results['factor_distribution'] = {
        'mean': ubl_factor.mean(),
        'std': ubl_factor.std(),
        'min': ubl_factor.min(),
        'max': ubl_factor.max(),
        'skewness': ubl_factor.skew(),
        'kurtosis': ubl_factor.kurtosis()
    }
    
    # 3. 检查极值
    q99 = ubl_factor.quantile(0.99)
    q01 = ubl_factor.quantile(0.01)
    outlier_ratio = ((ubl_factor > q99) | (ubl_factor < q01)).sum() / len(ubl_factor)
    
    validation_results['outlier_analysis'] = {
        'q01': q01,
        'q99': q99,
        'outlier_ratio': outlier_ratio
    }
    
    # 4. 检查时间序列特性
    validation_results['time_series_properties'] = {
        'autocorr_lag1': ubl_factor.autocorr(lag=1),
        'autocorr_lag5': ubl_factor.autocorr(lag=5),
        'autocorr_lag20': ubl_factor.autocorr(lag=20)
    }
    
    return validation_results


def compare_implementations(bars: pd.DataFrame, lookback_period: int = 20) -> pd.DataFrame:
    """
    比较原始实现和改进实现的差异
    """
    # 原始实现（简化版）
    def original_ubl(bars, lookback_period):
        high, low, open_price, close = bars['high'], bars['low'], bars['open'], bars['close']
        
        upper_shadow = (high - np.maximum(open_price, close)) / (high - low + 1e-7)
        lower_shadow = (np.minimum(open_price, close) - low) / (high - low + 1e-7)
        wr_up = (high - close) / (high - low + 1e-7)
        wr_down = (close - low) / (high - low + 1e-7)
        
        df = pd.DataFrame({
            'upper_shadow': upper_shadow,
            'lower_shadow': lower_shadow,
            'wr_up': wr_up,
            'wr_down': wr_down
        })
        
        rolling_upper = df['upper_shadow'].rolling(window=lookback_period).mean()
        rolling_lower = df['lower_shadow'].rolling(window=lookback_period).mean()
        rolling_wr_up = df['wr_up'].rolling(window=lookback_period).mean()
        rolling_wr_down = df['wr_down'].rolling(window=lookback_period).mean()
        
        return (rolling_lower + rolling_wr_down) - (rolling_upper + rolling_wr_up)
    
    # 计算两个版本
    original_factor = original_ubl(bars, lookback_period)
    improved_factor = calculate_ubl_factor_improved(bars, lookback_period, standardize=False)
    
    # 比较结果
    comparison = pd.DataFrame({
        'original': original_factor,
        'improved': improved_factor,
        'difference': improved_factor - original_factor,
        'abs_difference': np.abs(improved_factor - original_factor)
    })
    
    return comparison


def main():
    """演示改进版UBL因子的使用"""
    print("=== 改进版UBL因子演示 ===")
    
    # 这里需要实际的数据加载逻辑
    # 为演示目的，创建一些示例数据
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    # 生成模拟OHLC数据
    close_prices = 100 * np.exp(np.cumsum(np.random.normal(0, 0.02, 100)))
    open_prices = close_prices * (1 + np.random.normal(0, 0.005, 100))
    high_prices = np.maximum(open_prices, close_prices) * (1 + np.random.exponential(0.01, 100))
    low_prices = np.minimum(open_prices, close_prices) * (1 - np.random.exponential(0.01, 100))
    
    bars = pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices
    }).set_index('date')
    
    # 计算改进版UBL因子
    ubl_factor = calculate_ubl_factor_improved(bars, lookback_period=20, standardize=True)
    
    # 验证计算结果
    validation = validate_ubl_calculation(bars, ubl_factor)
    
    print("验证结果:")
    for category, results in validation.items():
        print(f"\n{category}:")
        for key, value in results.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
    
    # 比较实现差异
    comparison = compare_implementations(bars, lookback_period=20)
    print(f"\n实现差异统计:")
    print(f"平均绝对差异: {comparison['abs_difference'].mean():.6f}")
    print(f"最大绝对差异: {comparison['abs_difference'].max():.6f}")
    print(f"相关系数: {comparison['original'].corr(comparison['improved']):.6f}")


if __name__ == "__main__":
    main()
