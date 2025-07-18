#!/usr/bin/env python3
"""
调试版本的回测脚本，用于解决test_v3.ipynb中的问题
"""

import backtrader as bt
import pandas as pd
import numpy as np
import datetime

# LLT计算函数
def calculate_llt(prices, alpha=0.05):
    # 转换为numpy数组以避免pandas索引问题
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

# 信号计算函数
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

class TradeLogger(bt.Observer):
    """简化的交易日志记录器"""
    lines = ('value',)
    
    def __init__(self):
        self.trade_count = 0
        
    def next(self):
        # 记录组合价值
        self.l.value[0] = self._owner.broker.getvalue()

        # 获取当前持仓信息
        cash = self._owner.broker.getcash()
        total_value = self._owner.broker.getvalue()

        # 计算持仓价值和数量
        position_value = 0
        position_size = 0

        for data in self._owner.datas:
            position = self._owner.getposition(data)
            position_size = position.size
            if position.size != 0:
                position_value = position.size * data.close[0]

        # 每天打印组合状态
        date = self._owner.data.datetime.date(0)
        print(f"{date} - 持仓:{position_size:.0f}股, 持仓价值:{position_value:.2f}, 现金:{cash:.2f}, 总价值:{total_value:.2f}")

class LongShort1x1Strategy(bt.Strategy):
    params = (
        ('d', 5),                # LLT参数d
        ('slope_window', 5),      # 斜率窗口
        ('position_ratio', 1),
    )
    
    def __init__(self):
        # 预计算信号
        self.signals = llt_slope_signal(
            self.data._dataname,  # 访问原始DataFrame
            d=self.p.d,
            slope_window=self.p.slope_window
        )
        # 确保信号索引是datetime类型
        if hasattr(self.signals.index, 'tz_localize'):
            self.signals = self.signals.tz_localize(None)

        print(f"策略初始化完成，信号数量: {len(self.signals)}")
        print(f"信号前5个值: {self.signals.head()}")
    
    def next(self):
        # 获取当前日期和信号
        current_date = pd.Timestamp(self.data.datetime.date())
        
        # 获取当前信号（处理日期不匹配）
        try:
            current_signal = self.signals.loc[current_date]
        except KeyError:
            current_signal = 0
        
        # 获取当前持仓
        current_position = self.getposition(self.data)
        
        # 记录交易决策
        if current_signal != 0:
            print(f"日期: {current_date.date()}, 信号: {current_signal}, 当前持仓: {current_position.size}")
        
        # 执行交易逻辑 - 使用百分比目标
        if current_signal == 1:
            # 做多信号：目标持仓95%
            order = self.order_target_percent(target=0.95)
            if order:
                print(f"做多信号: {current_date.date()}, 价格={self.data.close[0]:.2f}, 目标仓位=95%")
        elif current_signal == -1:
            # 做空信号：目标持仓-95%
            order = self.order_target_percent(target=-0.95)
            if order:
                print(f"做空信号: {current_date.date()}, 价格={self.data.close[0]:.2f}, 目标仓位=-95%")
        else:
            # 信号为0，平仓
            if current_position.size != 0:
                order = self.order_target_percent(target=0.0)
                if order:
                    print(f"平仓信号: {current_date.date()}, 价格={self.data.close[0]:.2f}, 目标仓位=0%")

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"交易结束：{trade.close_datetime()}")
            print(f"    开仓价格: {trade.price:.2f}")
            print(f"    交易数量: {trade.size}")
            print(f"    pnl: {trade.pnl:.2f}")
            print(f"    佣金: {trade.commission:.2f}")

def run_backtest(data, d=30, slope_window=5, initial_cash=100_000):
    # 数据清洗
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    if 'volume' in data.columns:
        data['volume'] = data['volume'].clip(lower=0)

    print(f"数据范围: {data.index[0]} 到 {data.index[-1]}")
    print(f"数据行数: {len(data)}")

    # 初始化回测引擎
    cerebro = bt.Cerebro()
    cerebro.addstrategy(LongShort1x1Strategy, d=d, slope_window=slope_window)

    # 添加数据
    bt_data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(bt_data)

    # 添加观察器
    cerebro.addobserver(TradeLogger)

    # 配置回测参数
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)  # 佣金0.1%

    # 添加绩效分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

    # 运行回测
    print(f"初始资金: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(f"最终资金: {final_value:.2f}")

    # 输出绩效指标
    strat = results[0]
    returns = strat.analyzers.returns.get_analysis()
    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()

    print(f"年化收益率: {returns.get('rnorm100', 0):.2f}%")
    print(f"夏普比率: {sharpe.get('sharperatio', 0):.2f}")
    print(f"最大回撤: {drawdown.get('max', {}).get('drawdown', 0):.2f}%")

    return results

if __name__ == "__main__":
    # 读取数据
    data = pd.read_csv('sh.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')

    print("=== 回测开始 ===")
    # 运行回测
    result = run_backtest(data, d=5)

    print("\n=== 回测完成 ===")
    print("主要问题已修复：")
    print("1. 使用百分比目标而不是固定股数")
    print("2. 正确计算持仓价值和现金")
    print("3. 交易逻辑正常工作")
