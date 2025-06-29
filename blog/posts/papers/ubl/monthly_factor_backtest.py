#!/usr/bin/env python3
"""
月度因子回测框架
实现月度调仓策略：每月初根据上月末因子分组买入，月底卖出
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def monthly_factor_backtest(factor_data: pd.Series, 
                           bars: pd.DataFrame,
                           quantiles: Optional[int] = 5,
                           bins: Optional[Union[int, list]] = None) -> tuple[pd.DataFrame, pd.Series]:
    """
    月度因子回测框架

    如果在月初、月尾某资产没有价格数据，则会跳过买入、卖出；如果因子在月末没有数据也会如此。这是既正确又错误的做法。但你可以在回测前，先对factor_data, bars进行预处理，通过前向填充来修正。
    
    Args:
        factor_data: 因子数据，双重索引(date, asset)的Series
        bars: 价格数据，双重索引(date, asset)，包含open, close列
        quantiles: 分组数量，与bins互斥
        bins: 自定义分组边界，与quantiles互斥
    
    Returns:
        tuple: (策略各组月收益率DataFrame, 基准月收益率Series)
               策略收益率索引为月份，列为分组
               基准收益率为等权买入所有股票的月收益率
    """
    
    # 参数检查
    if quantiles is not None and bins is not None:
        raise ValueError("quantiles和bins不能同时指定")
    if quantiles is None and bins is None:
        quantiles = 5
    
    # 重置索引以便操作
    factor_df = factor_data.to_frame(name='factor').reset_index()
    factor_col = 'factor'
    bars_df = bars.reset_index()
    
    # 检查数据是否为空
    if len(factor_df) == 0 or len(bars_df) == 0:
        return pd.DataFrame(), pd.Series()
    
    # 获取所有月份的第一个和最后一个交易日
    factor_df['year_month'] = factor_df['date'].dt.to_period('M')
    month_ends = factor_df.groupby('year_month')['date'].max().reset_index()
    month_starts = factor_df.groupby('year_month')['date'].min().reset_index()
    month_ends.columns = ['year_month', 'month_end_date']
    month_starts.columns = ['year_month', 'month_start_date']
    
    # 存储每月收益率
    monthly_returns = []
    benchmark_returns = []
    
    for i in range(len(month_ends) - 1):
        current_month = month_ends.iloc[i]
        next_month = month_ends.iloc[i + 1]
        next_month_start = month_starts.iloc[i + 1]
        
        # 当前月末的因子数据
        factor_date = current_month['month_end_date']
        factor_month_data = factor_df[factor_df['date'] == factor_date]
        
        if len(factor_month_data) == 0:
            continue
            
        # 下月初买入价格（开盘价）
        buy_date = next_month_start['month_start_date']
        buy_prices = bars_df[bars_df['date'] == buy_date][['asset', 'open']]
        buy_prices.columns = ['asset', 'price_buy']
        
        # 下月末卖出价格（收盘价）
        sell_date = next_month['month_end_date']
        sell_prices = bars_df[bars_df['date'] == sell_date][['asset', 'close']]
        sell_prices.columns = ['asset', 'price_sell']
        
        if len(buy_prices) == 0 or len(sell_prices) == 0:
            continue
            
        # 合并数据
        month_data = factor_month_data.merge(buy_prices, on='asset')
        month_data = month_data.merge(sell_prices, on='asset')
        
        # 删除价格数据缺失的股票
        month_data = month_data.dropna(subset=[factor_col, 'price_buy', 'price_sell'])
        
        if len(month_data) == 0:
            continue
            
        # 因子分组
        if quantiles is not None:
            month_data['group'] = pd.qcut(month_data[factor_col], 
                                        q=quantiles, 
                                        labels=False, 
                                        duplicates='drop') + 1
        else:
            month_data['group'] = pd.cut(month_data[factor_col], 
                                       bins=bins, 
                                       labels=False, 
                                       include_lowest=True) + 1
        
        # 计算个股收益率
        month_data['return'] = month_data['price_sell'] / month_data['price_buy'] - 1
        
        # 计算各组等权收益率
        group_returns = month_data.groupby('group')['return'].mean()
        
        # 计算基准收益率（等权买入所有股票）
        benchmark_return = month_data['return'].mean()
        
        # 添加月份信息
        group_returns.name = current_month['year_month']
        monthly_returns.append(group_returns)
        benchmark_returns.append(benchmark_return)
    
    # 合并所有月份的收益率
    if not monthly_returns:
        return pd.DataFrame(), pd.Series()
        
    # 策略收益率
    strategy_returns = pd.concat(monthly_returns, axis=1).T
    strategy_returns.index = pd.to_datetime(strategy_returns.index.astype(str))
    
    # 重命名列
    if quantiles is not None:
        strategy_returns.columns = [f'Q{i}' for i in strategy_returns.columns]
    else:
        strategy_returns.columns = [f'Bin{i}' for i in strategy_returns.columns]
    
    # 基准收益率
    benchmark_series = pd.Series(benchmark_returns, 
                                index=strategy_returns.index, 
                                name='Benchmark')
    
    return strategy_returns, benchmark_series


def calculate_group_statistics(monthly_returns: pd.DataFrame) -> pd.DataFrame:
    """
    计算各组统计指标
    
    Args:
        monthly_returns: 月度收益率DataFrame
    
    Returns:
        统计指标DataFrame
    """
    stats = pd.DataFrame(index=monthly_returns.columns)
    
    # 年化收益率
    stats['年化收益率'] = monthly_returns.mean() * 12
    
    # 年化波动率
    stats['年化波动率'] = monthly_returns.std() * np.sqrt(12)
    
    # 夏普比率（假设无风险利率为0）
    stats['夏普比率'] = stats['年化收益率'] / stats['年化波动率']
    
    # 最大回撤
    cumulative_returns = (1 + monthly_returns).cumprod()
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    stats['最大回撤'] = drawdown.min()
    
    # 胜率
    stats['胜率'] = (monthly_returns > 0).mean()
    
    # 月度收益率统计
    stats['月均收益率'] = monthly_returns.mean()
    stats['月收益率标准差'] = monthly_returns.std()
    
    return stats


def plot_cumulative_returns(monthly_returns: pd.DataFrame, title: str = "各组累计收益率"):
    """
    绘制各组累计收益率曲线
    
    Args:
        monthly_returns: 月度收益率DataFrame
        title: 图表标题
    """    
    cumulative_returns = (1 + monthly_returns).cumprod()
    
    plt.figure(figsize=(12, 8))
    for col in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[col], label=col, linewidth=2)
    
    plt.title(title, fontsize=14)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('累计收益率', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def analyze_long_short_spread(monthly_returns: pd.DataFrame) -> pd.Series:
    """
    分析多空价差（最高分组 - 最低分组）
    
    Args:
        monthly_returns: 月度收益率DataFrame
    
    Returns:
        多空价差的月度收益率Series
    """
    if len(monthly_returns.columns) < 2:
        raise ValueError("至少需要2个分组才能计算多空价差")
    
    highest_group = monthly_returns.iloc[:, -1]  # 最后一列（最高分组）
    lowest_group = monthly_returns.iloc[:, 0]    # 第一列（最低分组）
    
    spread_returns = highest_group - lowest_group
    spread_returns.name = 'Long_Short_Spread'
    
    return spread_returns


if __name__ == "__main__":
    # 示例用法
    print("月度因子回测框架")
    print("主要功能：")
    print("1. monthly_factor_backtest(): 执行月度调仓回测")
    print("2. calculate_group_statistics(): 计算各组统计指标")
    print("3. plot_cumulative_returns(): 绘制累计收益率曲线")
    print("4. analyze_long_short_spread(): 分析多空价差")
    
    # 数据格式说明
    print("\n数据格式要求：")
    print("factor_data: 双重索引(date, asset)的DataFrame，包含因子值")
    print("bars: 双重索引(date, asset)的DataFrame，包含ohlc和price列")
    print("price列为次日开盘价，用于T+1买入计算")
