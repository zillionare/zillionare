import backtrader as bt
import numpy as np
import pandas as pd


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
def llt_slope_signal(df, d: int=39, slope_window=5, thresh=(0, 0)):
    df = df.copy()
    alpha = 2 / (d + 1)
    df["llt"] = calculate_llt(df["close"], alpha)
    df['slope'] = (df["llt"].rolling(slope_window)
                    .apply(lambda x: np.polyfit(np.arange(slope_window), x, 1)[0]))
    
    signals = pd.Series(0, index=df.index)
    signals[df['slope'] > thresh[1]] = 1
    signals[df['slope'] < thresh[0]] = -1
    signals.ffill(inplace = True)
    
    return signals

def llt_slope_quantiles(df, d: int=39, slope_window=5):
    df = df.copy()
    alpha = 2 / (d + 1)
    df["llt"] = calculate_llt(df["close"], alpha)
    df['slope'] = (df["llt"].rolling(slope_window)
                    .apply(lambda x: np.polyfit(np.arange(slope_window), x, 1)[0]))
    
    return df['slope'].quantile(0.25), df['slope'].quantile(0.75)

class LLTStrategy(bt.Strategy):
    params = (
        ('d', 39),                # LLT参数d
        ('slope_window', 5),      # 斜率窗口
        ('position_ratio', 1),
        ('thresh', (-0.05, 0.05))
    )
    
    def __init__(self):
        self.order_dict = {}
        self.signals = llt_slope_signal(
            self.data._dataname,
            d=self.p.d,
            slope_window=self.p.slope_window,
            thresh=self.p.thresh
        )
        # 确保信号索引是datetime类型
        if hasattr(self.signals.index, 'tz_localize'):
            self.signals = self.signals.tz_localize(None)
        
        # 初始化持仓跟踪
        self._last_direction = 0
        
        print(f"策略初始化完成，信号数量: {len(self.signals)}")
        print(f"信号前20个值: {self.signals.head(20)}")
    
    def next(self):
        # 获取当前日期和信号
        current_date = pd.Timestamp(self.data.datetime.date())
        
        # 获取当前信号（处理日期不匹配）
        try:
            current_signal = self.signals.loc[current_date]
        except KeyError:
            current_signal = 0
        
        current_position = self.getposition(self.data)
        
        if current_signal != 0:
            print(f"日期: {current_date.date()}, 信号: {current_signal}, 当前持仓: {current_position.size}")
        
        # 执行交易逻辑 - 使用百分比目标（修复版本）
        if current_signal == 1 and self._last_direction <= 0:
            order = self.order_target_percent(target=0.95)
            if order:
                print(f"做多信号: {current_date.date()}")
        elif current_signal == -1 and self._last_direction >= 0:
            order = self.order_target_percent(target=-0.95)
            if order:
                print(f"做空信号: {current_date.date()}")
        elif current_signal == 0 and current_position.size != 0:
            order = self.order_target_percent(target=0.0)
            if order:
                print(f"平仓信号: {current_date.date()}")
        else:
            pass
