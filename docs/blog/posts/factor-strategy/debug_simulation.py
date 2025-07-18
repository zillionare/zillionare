#!/usr/bin/env python3
"""
调试现实模拟中的问题
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

def debug_simulation(df, calc_signal, args, commission_rate=0.001, price: str = "close"):
    """调试版本的现实模拟"""
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)
    df["benchmark"] = df[price].pct_change()
    
    # 模拟实际交易
    initial_cash = 100000
    cash = initial_cash
    position = 0  # 持有股数
    portfolio_values = []
    trade_costs = []
    positions = []
    cash_values = []
    
    print("开始调试模拟...")
    print("日期\t\t信号\t价格\t\t目标仓位\t交易量\t\t现金\t\t持仓价值\t总价值")
    print("-" * 100)
    
    for i, (date, row) in enumerate(df.iterrows()):
        signal = row['signal_shifted']
        price_change = row['benchmark']
        current_price = row[price]
        
        if pd.isna(signal) or pd.isna(price_change) or pd.isna(current_price):
            portfolio_value = cash + position * current_price if not pd.isna(current_price) else cash
            portfolio_values.append(portfolio_value)
            trade_costs.append(0)
            positions.append(position)
            cash_values.append(cash)
            continue
        
        # 计算当前持仓价值
        position_value = position * current_price
        total_value = cash + position_value
        
        # 计算目标仓位
        if signal == 1:
            # 95%做多
            target_value = total_value * 0.95
            target_shares = target_value / current_price
        elif signal == -1:
            # 95%做空
            target_value = -total_value * 0.95
            target_shares = target_value / current_price
        else:
            target_shares = 0
        
        # 计算交易量
        trade_shares = target_shares - position
        trade_value = abs(trade_shares * current_price)
        commission = trade_value * commission_rate if trade_shares != 0 else 0
        
        # 执行交易
        if trade_shares != 0:
            cash -= trade_shares * current_price + commission
            position = target_shares
        
        # 更新记录
        position_value = position * current_price
        total_value = cash + position_value
        
        portfolio_values.append(total_value)
        trade_costs.append(commission)
        positions.append(position)
        cash_values.append(cash)
        
        # 打印前20天的详细信息
        if i < 20:
            print(f"{str(date)[:10]}\t{signal:.0f}\t{current_price:.2f}\t\t{target_shares:.1f}\t\t{trade_shares:.1f}\t\t{cash:.2f}\t{position_value:.2f}\t\t{total_value:.2f}")
        
        # 检查异常情况
        if total_value < 0:
            print(f"警告：第{i}天总价值为负: {total_value:.2f}")
            break
        
        if abs(cash) > initial_cash * 10:  # 现金超过初始资金10倍
            print(f"警告：第{i}天现金异常: {cash:.2f}")
            break
    
    df['portfolio_value'] = portfolio_values
    df['trade_cost'] = trade_costs
    df['position'] = positions
    df['cash'] = cash_values
    
    return df

def main():
    # 读取数据
    data = pd.read_csv('sh.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    
    # 只用前50天进行调试
    test_data = data.head(50)
    
    print("=== 调试现实模拟问题 ===\n")
    print(f"测试数据: {len(test_data)}天")
    
    result = debug_simulation(test_data, llt_slope_signal, (5,), commission_rate=0.001)
    
    print(f"\n最终结果:")
    print(f"初始资金: 100,000.00")
    print(f"最终资金: {result['portfolio_value'].iloc[-1]:,.2f}")
    print(f"总手续费: {result['trade_cost'].sum():,.2f}")
    print(f"最终现金: {result['cash'].iloc[-1]:,.2f}")
    print(f"最终持仓价值: {result['position'].iloc[-1] * test_data['close'].iloc[-1]:,.2f}")

if __name__ == "__main__":
    main()
