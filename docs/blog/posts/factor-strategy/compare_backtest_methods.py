#!/usr/bin/env python3
"""
对比分析test_v2中的backtest函数和backtrader版本的差异
"""

import backtrader as bt
import pandas as pd
import numpy as np
import datetime

# LLT计算函数
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

# test_v2中的原始backtest函数
def original_backtest(df, calc_signal, args, price: str = "open", long_weight: float = 0.5, short_weight: float = 0.5, long_short=True):
    """原始回测函数"""
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)
    df["benchmark"] = df[price].pct_change()
    
    df['long_return'] = np.where(df['signal_shifted'] == 1, df['benchmark'], 0)
    df['short_return'] = np.where(df['signal_shifted'] == -1, -df['benchmark'], 0)
    df["long_short_return"] = df['long_return'] * long_weight + df['short_return'] * short_weight
    
    return df

# 详细分析版本的backtest函数
def detailed_backtest(df, calc_signal, args, price: str = "open", long_weight: float = 0.5, short_weight: float = 0.5):
    """详细分析版本的回测函数"""
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)
    df["benchmark"] = df[price].pct_change()
    
    # 详细记录每一步
    df['long_return'] = np.where(df['signal_shifted'] == 1, df['benchmark'], 0)
    df['short_return'] = np.where(df['signal_shifted'] == -1, -df['benchmark'], 0)
    df["long_short_return"] = df['long_return'] * long_weight + df['short_return'] * short_weight
    
    # 计算累积收益
    df['cumulative_return'] = (1 + df['long_short_return']).cumprod()
    df['benchmark_cumulative'] = (1 + df['benchmark']).cumprod()
    
    # 添加调试信息
    df['position'] = df['signal_shifted']
    df['price_change'] = df['benchmark']
    
    return df

class LongShortStrategy(bt.Strategy):
    params = (
        ('d', 5),
        ('slope_window', 5),
    )
    
    def __init__(self):
        # 预计算信号
        self.signals = llt_slope_signal(
            self.data._dataname,
            d=self.p.d,
            slope_window=self.p.slope_window
        )
        if hasattr(self.signals.index, 'tz_localize'):
            self.signals = self.signals.tz_localize(None)
        
        # 记录交易详情
        self.trade_log = []
        self.daily_log = []
        
    def next(self):
        current_date = pd.Timestamp(self.data.datetime.date())
        
        try:
            current_signal = self.signals.loc[current_date]
        except KeyError:
            current_signal = 0
        
        current_position = self.getposition(self.data)
        cash = self.broker.getcash()
        total_value = self.broker.getvalue()
        
        # 记录每日状态
        self.daily_log.append({
            'date': current_date,
            'signal': current_signal,
            'position': current_position.size,
            'price': self.data.close[0],
            'cash': cash,
            'total_value': total_value
        })
        
        # 交易逻辑
        if current_signal == 1:
            order = self.order_target_percent(target=0.95)
        elif current_signal == -1:
            order = self.order_target_percent(target=-0.95)
        else:
            if current_position.size != 0:
                order = self.order_target_percent(target=0.0)

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trade_log.append({
                'close_date': trade.close_datetime(),
                'open_price': trade.price,
                'size': trade.size,
                'pnl': trade.pnl,
                'commission': trade.commission
            })

def run_backtrader_test(data, d=5, slope_window=5, initial_cash=100_000):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(LongShortStrategy, d=d, slope_window=slope_window)
    
    bt_data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(bt_data)
    
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)
    
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    
    strat = results[0]
    returns = strat.analyzers.returns.get_analysis()
    
    return {
        'initial_cash': initial_cash,
        'final_value': final_value,
        'total_return': (final_value - initial_cash) / initial_cash,
        'annual_return': returns.get('rnorm100', 0) / 100,
        'trade_log': strat.trade_log,
        'daily_log': strat.daily_log
    }

def analyze_differences(data, d=5):
    print("=== 对比分析：原始backtest vs backtrader ===\n")
    
    # 1. 运行原始backtest
    print("1. 运行原始backtest函数...")
    original_result = original_backtest(data, llt_slope_signal, (d,))
    original_total_return = original_result['long_short_return'].sum()
    original_cumulative = (1 + original_result['long_short_return']).cumprod().iloc[-1] - 1
    
    print(f"   总收益率（简单求和）: {original_total_return:.4f}")
    print(f"   累积收益率: {original_cumulative:.4f}")
    
    # 2. 运行详细backtest
    print("\n2. 运行详细分析版本...")
    detailed_result = detailed_backtest(data, llt_slope_signal, (d,))
    
    # 3. 运行backtrader
    print("\n3. 运行backtrader版本...")
    bt_result = run_backtrader_test(data, d=d)
    
    print(f"   初始资金: {bt_result['initial_cash']:,.2f}")
    print(f"   最终资金: {bt_result['final_value']:,.2f}")
    print(f"   总收益率: {bt_result['total_return']:.4f}")
    print(f"   年化收益率: {bt_result['annual_return']:.4f}")
    
    # 4. 分析关键差异
    print("\n=== 关键差异分析 ===")
    
    # 信号对比
    signals = detailed_result['signal'].dropna()
    signal_changes = (signals != signals.shift(1)).sum()
    print(f"信号变化次数: {signal_changes}")
    
    # 收益计算方式对比
    print(f"\n收益计算差异:")
    print(f"原始方法累积收益: {original_cumulative:.4f} ({original_cumulative*100:.2f}%)")
    print(f"Backtrader收益: {bt_result['total_return']:.4f} ({bt_result['total_return']*100:.2f}%)")
    print(f"差异: {abs(original_cumulative - bt_result['total_return']):.4f}")
    
    # 分析前10个交易日的详细情况
    print(f"\n前10个交易日详细对比:")
    print("日期\t\t信号\t价格变化\t原始收益\tBacktrader状态")
    print("-" * 80)
    
    for i in range(min(10, len(detailed_result))):
        row = detailed_result.iloc[i]
        date = row.name if hasattr(row.name, 'date') else str(row.name)[:10]
        signal = row['signal_shifted']
        price_change = row['benchmark']
        strategy_return = row['long_short_return']
        
        bt_day = None
        if i < len(bt_result['daily_log']):
            bt_day = bt_result['daily_log'][i]
        
        bt_value = f"{bt_day['total_value']:.2f}" if bt_day else 'N/A'
        signal_str = f"{signal:.0f}" if not pd.isna(signal) else 'NaN'
        print(f"{date}\t{signal_str}\t{price_change:.4f}\t\t{strategy_return:.4f}\t\t{bt_value}")
    
    # 5. 深入分析关键差异
    print(f"\n=== 深入分析关键差异 ===")

    # 分析交易成本影响
    total_trades = len(bt_result['trade_log'])
    total_commission = sum([trade['commission'] for trade in bt_result['trade_log']])
    print(f"总交易次数: {total_trades}")
    print(f"总手续费: {total_commission:.2f}")
    print(f"手续费占初始资金比例: {total_commission/100000:.4f}")

    # 分析仓位差异
    print(f"\n原始方法假设:")
    print("- 每次信号变化时立即全仓买入/卖出")
    print("- 无交易成本")
    print("- 使用当日收盘价计算收益")
    print("- 信号当天就能获得收益")

    print(f"\nBacktrader实际情况:")
    print("- 需要考虑现金限制和仓位管理")
    print("- 有交易手续费")
    print("- 可能存在滑点和执行延迟")
    print("- 信号发出后次日才能交易")

    # 计算理论vs实际的差异来源
    print(f"\n差异来源分析:")
    no_commission_return = bt_result['total_return'] + total_commission/100000
    print(f"如果没有手续费的Backtrader收益: {no_commission_return:.4f}")
    print(f"与原始方法的剩余差异: {abs(original_cumulative - no_commission_return):.4f}")

    return {
        'original': original_result,
        'detailed': detailed_result,
        'backtrader': bt_result
    }

if __name__ == "__main__":
    # 读取数据
    data = pd.read_csv('sh.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    
    # 使用较小的数据集进行测试
    test_data = data.head(100)  # 只用前100天进行详细分析
    
    results = analyze_differences(test_data, d=5)
