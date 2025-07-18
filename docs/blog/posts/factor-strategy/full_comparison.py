#!/usr/bin/env python3
"""
完整数据集的深入对比分析
"""

import pandas as pd
import numpy as np

def calculate_llt(prices, alpha=0.05):
    if hasattr(prices, 'values'):
        prices = prices.values
    
    n = len(prices)
    llt = np.zeros(n)
    if n >= 1:
        llt[0] = prices[0]
    if n >= 2:
        llt[1] = prices[1]
    
    a1 = alpha - (alpha**2) / 4
    a2 = (alpha**2) / 2
    a3 = alpha - 3 * (alpha**2) / 4
    a4 = 2 * (1 - alpha)
    a5 = - (1 - alpha)**2
    
    for t in range(2, n):
        llt[t] = a1 * prices[t] + a2 * prices[t-1] - a3 * prices[t-2] + a4 * llt[t-1] + a5 * llt[t-2]
    
    return llt

def llt_slope_signal(df, d: int=30, slope_window=5):
    df = df.copy()
    alpha = 2 / (d + 1)
    df["llt"] = calculate_llt(df["close"], alpha)
    df['slope'] = (df["llt"].rolling(slope_window)
                    .apply(lambda x: np.polyfit(np.arange(slope_window), x, 1)[0]))
    
    signals = pd.Series(0, index=df.index)
    signals[df['slope'] > 0] = 1
    signals[df['slope'] < 0] = -1
    
    return signals

def original_backtest(df, calc_signal, args, price: str = "close", long_weight: float = 0.5, short_weight: float = 0.5):
    """原始回测函数 - 修正版本"""
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)  # 信号延迟一天执行
    df["benchmark"] = df[price].pct_change()
    
    df['long_return'] = np.where(df['signal_shifted'] == 1, df['benchmark'], 0)
    df['short_return'] = np.where(df['signal_shifted'] == -1, -df['benchmark'], 0)
    df["long_short_return"] = df['long_return'] * long_weight + df['short_return'] * short_weight
    
    return df

def simulate_realistic_backtest(df, calc_signal, args, commission_rate=0.001, price: str = "close"):
    """更现实的回测模拟"""
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)
    df["benchmark"] = df[price].pct_change()
    
    # 模拟实际交易
    cash = 100000
    position = 0
    portfolio_values = []
    trade_costs = []
    
    for i, row in df.iterrows():
        signal = row['signal_shifted']
        price_change = row['benchmark']
        current_price = row[price]
        
        if pd.isna(signal) or pd.isna(price_change):
            portfolio_values.append(cash + position * current_price)
            trade_costs.append(0)
            continue
        
        # 计算目标仓位
        if signal == 1:
            target_position_value = cash * 0.95  # 95%做多
            target_shares = target_position_value / current_price
        elif signal == -1:
            target_position_value = -cash * 0.95  # 95%做空
            target_shares = target_position_value / current_price
        else:
            target_shares = 0
        
        # 计算交易量和成本
        trade_shares = target_shares - position
        trade_value = abs(trade_shares * current_price)
        commission = trade_value * commission_rate
        
        # 执行交易
        if trade_shares != 0:
            cash -= trade_shares * current_price + commission
            position = target_shares
            trade_costs.append(commission)
        else:
            trade_costs.append(0)
        
        # 更新持仓价值（考虑价格变化）
        if position != 0:
            position_value = position * current_price
        else:
            position_value = 0
            
        portfolio_values.append(cash + position_value)
    
    df['portfolio_value'] = portfolio_values
    df['trade_cost'] = trade_costs
    df['portfolio_return'] = df['portfolio_value'].pct_change()
    
    return df

def comprehensive_analysis():
    print("=== 完整数据集深入对比分析 ===\n")
    
    # 读取数据
    data = pd.read_csv('sh.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    
    print(f"数据范围: {data.index[0]} 到 {data.index[-1]}")
    print(f"数据行数: {len(data)}")
    
    # 1. 原始方法
    print("\n1. 原始backtest方法:")
    original_result = original_backtest(data, llt_slope_signal, (5,))
    original_cumulative = (1 + original_result['long_short_return']).cumprod().iloc[-1] - 1
    original_annual = (1 + original_cumulative) ** (252 / len(data)) - 1
    
    print(f"   累积收益率: {original_cumulative:.4f} ({original_cumulative*100:.2f}%)")
    print(f"   年化收益率: {original_annual:.4f} ({original_annual*100:.2f}%)")
    
    # 2. 现实模拟方法
    print("\n2. 现实模拟方法（含手续费）:")
    realistic_result = simulate_realistic_backtest(data, llt_slope_signal, (5,))
    realistic_final_value = realistic_result['portfolio_value'].iloc[-1]
    realistic_return = (realistic_final_value - 100000) / 100000
    realistic_annual = (1 + realistic_return) ** (252 / len(data)) - 1
    total_commission = realistic_result['trade_cost'].sum()
    
    print(f"   最终资金: {realistic_final_value:,.2f}")
    print(f"   累积收益率: {realistic_return:.4f} ({realistic_return*100:.2f}%)")
    print(f"   年化收益率: {realistic_annual:.4f} ({realistic_annual*100:.2f}%)")
    print(f"   总手续费: {total_commission:,.2f}")
    
    # 3. 分析差异来源
    print(f"\n3. 差异分析:")
    print(f"   收益率差异: {abs(original_cumulative - realistic_return):.4f}")
    print(f"   手续费影响: {total_commission/100000:.4f}")
    
    # 4. 信号分析
    signals = original_result['signal'].dropna()
    signal_changes = (signals != signals.shift(1)).sum()
    long_signals = (signals == 1).sum()
    short_signals = (signals == -1).sum()
    neutral_signals = (signals == 0).sum()
    
    print(f"\n4. 信号统计:")
    print(f"   信号变化次数: {signal_changes}")
    print(f"   做多信号天数: {long_signals} ({long_signals/len(signals)*100:.1f}%)")
    print(f"   做空信号天数: {short_signals} ({short_signals/len(signals)*100:.1f}%)")
    print(f"   中性信号天数: {neutral_signals} ({neutral_signals/len(signals)*100:.1f}%)")
    
    # 5. 关键问题分析
    print(f"\n=== 关键问题分析 ===")
    print("原始方法的问题:")
    print("1. 假设无限资金，可以无成本地进行任意规模交易")
    print("2. 忽略了交易手续费和滑点")
    print("3. 假设信号当天就能获得收益（实际应该是次日）")
    print("4. 没有考虑仓位管理和风险控制")
    print("5. 多空切换时假设可以瞬间完成")
    
    print(f"\nBacktrader的现实考虑:")
    print("1. 有限的现金和仓位约束")
    print("2. 真实的交易成本")
    print("3. 信号延迟执行")
    print("4. 仓位管理和风险控制")
    print("5. 更复杂的订单执行逻辑")
    
    # 6. 修正建议
    print(f"\n=== 修正建议 ===")
    
    # 计算无手续费的现实模拟
    no_commission_result = simulate_realistic_backtest(data, llt_slope_signal, (5,), commission_rate=0)
    no_commission_return = (no_commission_result['portfolio_value'].iloc[-1] - 100000) / 100000
    
    print(f"无手续费的现实模拟收益: {no_commission_return:.4f} ({no_commission_return*100:.2f}%)")
    print(f"与原始方法的剩余差异: {abs(original_cumulative - no_commission_return):.4f}")
    
    if abs(original_cumulative - no_commission_return) < 0.01:
        print("✓ 主要差异来源于交易成本")
    else:
        print("✗ 还有其他重要差异来源需要进一步调查")
    
    return {
        'original_return': original_cumulative,
        'realistic_return': realistic_return,
        'no_commission_return': no_commission_return,
        'total_commission': total_commission,
        'signal_changes': signal_changes
    }

if __name__ == "__main__":
    results = comprehensive_analysis()
