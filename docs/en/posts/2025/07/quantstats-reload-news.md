---
title: "Fixing Quantstats: Backtest Bugs, Overfitting, and Recovery"
date: 2025-07-23
slug: en/posts/tools/quantstats-reload-news
tags: [Quantstats, Backtesting, Overfitting, Python]
excerpt: "We revived Quantstats after an 8-month hiatus, fixing critical Python 3.12 bugs and correcting lookahead bias in vectorized backtests. We then validate the strategy using backtrader, optimizing parameters while rigorously testing for overfitting."
lang: en
translation_of: posts/tools/quantstats-reload-news
auto_translated: true
source_sha: 6e7ec3cee4fc6e42eccbdb43d22214e738f74cb5
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/kamil-pietrzak-AlA8S9tALAs-unsplash.jpg"
---

Quantstats is a widely recognized library for quantitative strategy evaluation and visualization. However, for about eight months starting late 2024, it received no active maintenance, leading to severe bugs such as complete failure to run on Python 3.12 and above.

The good news is that in the past week, the original author, Ran Aroussi, has resumed maintenance of the library, releasing five consecutive versions (from 0.0.64 to 0.0.68).

---

We have consistently recommended this library in our courses for strategy evaluation and visualization to avoid reinventing the wheel. This recommendation also imposes an obligation on us to maintain it. Consequently, in early July, we released `quantstats-reloaded`.

To prevent future disconnection, we will continue to maintain `quantstats-reloaded` for a period to ensure our students always have access to a functional `quantstats`. Additionally, we will implement significant improvements, starting with enhanced unit testing.

The original library lacked systematic unit testing and CI, which may have been the primary reason the original author could not fix bugs in a timely manner.

This also raised concerns for us as users. Therefore, after restarting maintenance, we first used AI to add complete unit tests and CI workflows. Then, we manually completed unit tests for the most critical `stats` module. The test results are fully consistent with the original library (though not necessarily correct!), achieving a 91% unit test coverage rate.

Below is our comparative testing method.
```
{code-block} python
df = df.copy()
df['slope'] = (df[factor_col].rolling(slope_window)
                .apply(lambda x: np.polyfit(np.arange(slope_window), x, 1)[0]))

df['signal'] = 0
df.loc[df['slope'] > 0, 'signal'] = 1
df.loc[df['slope'] < 0, 'signal'] = -1

# 计算每日收益率
df['benchmark'] = df['close'].pct_change()

# 计算多空组合收益
df['long_return'] = np.where(df['signal'] == 1, df['benchmark'], 0)
df['short_return'] = np.where(df['signal'] == -1, -df['benchmark'], 0)

# 组合收益 = 多头收益 * 多头权重 + 空头收益 * 空头权重
df['strategy'] = df['long_return'] * long_weight + df['short_return'] * short_weight

return df
```

If we treat the signal as a factor, then in this code, the factor and future returns are aligned in time, rather than lagged. That is, the code attributes the return on day $T_0$ to the factor on day $T_0$. However, the exact meaning of the return on day $T_0$ is that you must buy on day $T_{-1}$ and sell on day $T_0$ to calculate it. This is obviously incorrect.

If the stock price rises today, the tangent of the moving average may point upward, resulting in `signal = 1`; if the stock price falls today, the tangent may point downward, resulting in `signal = -1`. Both cases are unreasonably counted in the portfolio return.

!!! tip
    According to the research report, the position building is done as follows:

    ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/20250717143703.png)


Although this statement does not contain implementation details, it essentially includes future data, but with less side effects: it only requires calculating the trend line tangent slope and signal after market close based on the closing price, and then buying at the closing price.

Although this also has a slight hint of future data, it is allowed in practice because theoretically, you can calculate the signal and buy during the closing auction: the price used to calculate the signal would be very close to the final closing price, likely differing by only one slippage. Some backtesting tools allow this. For example, `backtrader` allows buying at the day's closing price if you declare `COC` (Cheat on Close) is allowed.

## Correcting the Algorithm

Now, let's correct the errors in the above code. First, can we also avoid the small flaw of "Cheat on Close" mentioned in the research report?

```python
def backtest(df, calc_signal, args, 
             price: str = "open", 
             long_weight: float = 0.5, 
             short_weight: float = 0.5):
    df = df.copy()
    df["signal"] = calc_signal(df, *args)
    df["signal"] = df["signal"].fillna(0)
    df["signal_shifted"] = df["signal"].shift(1)
    df["benchmark"] = df[price].pct_change()
    
    df['long_return'] = np.where(df['signal_shifted'] == 1, df['benchmark'], 0)
    df['short_return'] = np.where(df['signal_shifted'] == -1, -df['benchmark'], 0)
    df["long_short_return"] = df['long_return'] * long_weight + df['short_return'] * short_weight
    
    return df
```

Compared to the previous version, there are two important differences:

1. We shifted the signal one row backward (not forward). Thus, when calculating positions, if the signal was 1 the previous day, we multiply this 1 by the day's return.
2. We allow specifying the price data column for calculating returns, defaulting to `open`.

If you are familiar with `Alphalens`, you know that when calculating returns, it buys at the opening price of the second day after the signal is issued and sells at the opening price of the third day to calculate the return for `period = 1D`. Now, it seems we are doing exactly that!

The figure below shows the complete process of the initial trades (using synthetic data with fixed alternating gains/losses of 5% and -5%):

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/vector-backtest.jpeg)

On January 2, the strategy issued a long signal. Thus, we bought long at the opening on January 3 at a price of 104.73. With a daily gain of 5%, using the shifted signal of 1 as the position, the final long-short portfolio return is calculated as 2.5% (assuming 50% position for both long and short). The signal for January 3 was also 1, so we held the position; but since the price fell 5% that day, the portfolio return was -2.5%. The signal for the 4th was 0, so the strategy needed to sell at the opening on the 5th. On the 5th, since we held no position, the portfolio return was 0.

After using `open` as the price column for calculating returns, we still get a cumulative return graph almost identical to before. Is this result credible?

It looks correct and perfect. Except for one point: in a DataFrame-based vectorized backtesting framework, we cannot use a strategy that buys at the next day's opening price. Taking the buy signal on January 2 as an example, since the buy signal (1) on January 2 was shifted to January 3 and counted as a long position, this causes the gain from the January 3 opening price to the January 2 opening price to be counted as long return. However, at the opening of January 2, we had not yet executed the long buy.

Considering that if $T_0$ closes with a rise, it is more likely to issue a long signal, and the next day's opening price is also likely to be higher than the previous day's opening price, the strategy return calculated this way will have a significant "cheating" component on the first day, which is the main reason why backtest results look good when using the opening price to calculate returns.

But we cannot buy at the opening price on the third day after the signal is issued (signals don't wait!), so we must use the "Cheat on Close" strategy, meaning the price column must be specified as "close".

When specifying the price column as `close`, if we denote the signal occurrence day as $T_0$ and the signal as , due to the shift, when calculating the portfolio return on day $T_1$, we will compute $1 \times \text{Return}_{T_1}$. The return on day $T_1$ is calculated from the closing price of day $T_1$ and the closing price of day $T_0$. Although this is a form of "Cheat on Close," it does not cause significant error.

The main reason we use DataFrames for backtesting is simplicity and speed. From an idea to live trading, numerous processes take months (on a daily frequency, including simulation), so there is no need to use heavier frameworks initially. If an idea doesn't work in simple tests, we should probably abandon it -- because statistically, most ideas are inherently invalid.

## backtrader: Slower, but More Reliable

For event-driven strategy backtesting, `backtrader`, although slower, yields more reliable results, as shown by:

1. `backtrader` defaults to buying at the opening price on the next bar after the signal is issued.
2. `backtrader` calculates transaction fees, position limits, and volume limits.
3. Since DataFrame-based vector backtesting is very simple, there is no standard library to implement it. Our manual implementation is prone to errors.

Let's use `backtrader` to verify the previous backtest results.

<!-- BEGIN IPYNB STRIPOUT -->
The code for calculating LLT and tangent slope was provided in the previous issue, so it is not repeated here.
<!-- END IPYNB STRIPOUT -->

<!--PAID CONTENT START-->
This is the code for calculating llt and tangent slope to generate signals. Compared to the previous article, we added the `thresh` parameter, which will be used in tuning.

```python
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
```
<!--PAID CONTENT END-->

!!! tip
    A brief note on the parameter `d` for `llt_slope_signal`. It comes from the EMA indicator formula. When `d` takes values such as 9, 19, 39, etc., the corresponding alphas are 0.2, 0.1, 0.05, etc.

This is the backtesting strategy class:

```python
import backtrader as bt
class LLTStrategy(bt.Strategy):
    params = (
        ('d', 39),
        ('slope_window', 5), 
        ('position_ratio', 1),
        ('thresh', (0, 0))
    )
    
    def __init__(self):
        self.order_dict = {}
        self.signals = llt_slope_signal(
            self.data._dataname,
            d=self.p.d,
            slope_window=self.p.slope_window,
            thresh=self.p.thresh
        )
        
        self._last_direction = 0
        
        print(f"策略初始化完成，信号数量: {len(self.signals)}")
        print(f"信号前20个值: {self.signals.head(20)}")
    
    def next(self):
        current_date = pd.Timestamp(self.data.datetime.date())
        
        current_signal = self.signals.loc[current_date]
        position = self.getposition(self.data).size
        
        if current_signal != 0:
            print(f"日期: {current_date}, 信号: {current_signal}, 当前持仓: {position}")
        
        if current_signal == 1 and self._last_direction <= 0:
            order = self.order_target_percent(target=0.95)
            if order:
                print(f"做多信号: {current_date.date()}")
        elif current_signal == -1 and self._last_direction >= 0:
            order = self.order_target_percent(target=-0.95)
            if order:
                print(f"做空信号: {current_date.date()}")
        elif current_signal == 0 and position != 0:
            order = self.order_target_percent(target=0.0)
            if order:
                print(f"平仓信号: {current_date.date()}")
        else:
            pass
```

<!-- BEGIN IPYNB STRIPOUT -->
We omit the backtest calling code to save space. If you need this code, you can purchase a Kuangti membership. If you don't quite understand what we are discussing, you should enroll in Kuangti's "Quant 24 Lessons" and "Factor Mining and Machine Learning Strategies."
<!-- END IPYNB STRIPOUT -->

<!--PAID CONTENT START-->
```python
def run_backtest(data, d=39, 
                 slope_window=5, 
                 thresh=(0,0),
                 initial_cash=1_000_0000, 
                 commission=1e-4):
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=commission)

    cerebro.addstrategy(LLTStrategy, d=d, slope_window=slope_window, thresh=thresh)
    
    bt_data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(bt_data)
    
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
    
    print(f"夏普比率: {sharpe.get('sharperatio', 0):.2f}")
    print(f"最大回撤: {drawdown.get('max', {}).get('drawdown', 0):.2f}%")
    print(f"年化收益率: {returns.get('rnorm', 0):.2%}")

    return returns.get('rnorm', 0), sharpe.get('sharperatio', 0), drawdown.get('max',{}).get('drawdown',0)


def get_price(symbol, start_date, end_date):
    pro = pro_api()

    price_df = pro.index_daily(
        ts_code=symbol,
        start_date=start_date.strftime("%Y%m%d"),
        end_date=end_date.strftime("%Y%m%d"),
    )

    price_df = (
        price_df.rename({"trade_date": "date", "ts_code": "asset"}, axis=1)
        .sort_values("date", ascending=True)
        .set_index("date")
    )

    price_df.index = pd.to_datetime(price_df.index)
    return price_df

start = datetime.date(2005, 9, 6)
end = datetime.date(2013, 6, 28)
prices= get_price("000001.SH", start, end)

run_backtest(prices, commission = 1e-3)
```
<!--PAID CONTENT END-->

The result we obtained is an annualized return of 11.8% and a Sharpe ratio of 0.4. It is slightly better than the benchmark. However, if we backtest the interval after 2013, we will find that we have actually just picked up a biting snake:

```python
start = datetime.date(2013, 1, 1)
end = datetime.date(2024, 12, 31)
prices= get_price("000001.SH", start, end)

run_backtest(prices, commission=1e-3)
```

The annualized return this time is -6.4%, with a max drawdown of 79%.

## backtrader Parameter Optimization

Should we be disappointed by this?

No! We should never expect a simple strategy, or even one with fewer than 100 lines of code, to become a money-printing machine. Complexity and profundity do not guarantee success, but in the capital market, simplicity or even crudeness is definitely not enough. Any profitable business must have barriers.

Therefore, our optimization journey has just begun. It is far from time to be disappointed!

First, a transaction fee of one-thousandth is too high. When backtesting on indices, we must remember that indices themselves have limited profit space; any leakage is unacceptable!

Now, most brokerages' trading fees, especially for quantitative trading, have dropped to as low as 0.00854%. So, there is no need to set such a high fee of one-thousandth.

!!! info
    When we adjusted the commission to one-thousandth (still higher than the market), the annualized return improved to -3.7%. That's much better. We will use this setting in subsequent tests. However, this is not strategy optimization. True optimization is about to begin!

After careful analysis, we found that signal flips are too frequent. When the tangent slope changes from -0.01 to 0.005, do we immediately switch from short to long? This is obviously unreasonable. We should filter out such false signals. The calculation of the tangent slope is also affected by alpha. In our previous backtests, we used 0.05. Is it optimal?

We decided to use the built-in parameter optimization scheme of `backtrader` to help us tune. However, tuning may lead to overfitting, so we will also share how to judge whether the tuning results are overfit.

First, let's define the optimization function.

```python
from IPython.display import clear_output
def optimize(data, d, thresh):
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(1_000_0000)
    # 万分之一的佣金。现在多数券商给到了万分之 0.854
    cerebro.broker.setcommission(commission=0.0001)
    
    bt_data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(bt_data)
    
    # 添加绩效分析
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    cerebro.optstrategy(LLTStrategy, d = d, thresh = thresh)
    strats = cerebro.run(maxcpus = 1, optreturn = True)

    clear_output()

    params_and_returns = []
    for s in strats:
        returns = s[0].analyzers.returns.get_analysis()
        d, thresh = s[0].params.d, s[0].params.thresh[0]
        
        rnorm, pnl = f"{returns['rnorm']:.2%}", f"{returns['rtot']:.2%}"
        params_and_returns.append((d, thresh, rnorm, pnl))

    return pd.DataFrame(params_and_returns, columns=["d", "thresh", "rnorm", "pnl"])

start = datetime.date(2008, 1, 1)
end = datetime.date(2012, 12, 31)
prices= get_price("000001.SH", start, end)

result = optimize(prices, 
                  (9, 19, 39, 49, 59), 
                  (
                    (-0.01, 0.01), 
                    (-0.02, 0.02), 
                    (-0.04, 0.04), 
                    (-0.08, 0.08), 
                    (-0.12, 0.12)
                  ))
result
```



The key to parameter optimization via `backtrader` is these two lines of code:

```
{code-block} python
    cerebro.optstrategy(LLTStrategy, d = d, thresh = thresh)
    strats = cerebro.run(maxcpus = 1, optreturn = True)
```

When running in a notebook, we must set `maxcpus = 1`. If `maxcpus > 1`, it will start multi-process optimization. This involves the persistence of code in the notebook (because the code needs to be transmitted to new processes), which will cause errors.

<!--PAID CONTENT START-->
In our "Quant 24 Lessons," we detail how to use `backtrader`, including strategy optimization.
<!--PAID CONTENT END-->

We let the parameter `d` take values between (9, 19, 39, 49, 59, 69), so the corresponding alphas would be (0.2, 0.1, 0.05, 0.03), while `thresh` takes values between (-0.01, 0.01) and (-0.12, 0.12) in a doubling manner.

<!--PAID CONTENT START-->
<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/20250718163528.png?1'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>Parameter Optimization</span>
</div>

For visual aesthetics, only some results are filtered here.
<!--PAID CONTENT END-->

From the parameter optimization results, `d = 59, thresh = -0.01` is the best combination, achieving an ultra-high annualized return of 26.6%. Overall, as the `d` value increases, returns improve; the impact of `thresh` is not significant. Additionally, there is a parameter affecting performance: how many bars are used to calculate the tangent slope? Here, only a fixed 5 were used.

The above parameter optimization was based on data from 2008 to 2012. How does it perform between 2005 and 2013? The conclusion is: the annualized return reached 25.6%.

If we use these parameters for investment from 2013 to 2014, we will get an annualized return of 13.9% and a Sharpe ratio of 0.97. This performance is quite good.

## Correctly Viewing Overfitting

When using `backtrader` for parameter optimization, we must be aware that overfitting is easier to occur.

In the previous section, we already applied the optimal parameters obtained based on [2008, 2012] to the past [2005, 2012] and future [2013, 2014] intervals to compare the results. This is a method to check for overfitting. If the parameters are not overfit, they should be able to tell a good story on data they have not seen.

Here is another idea regarding the `thresh` parameter. It is undoubtedly more reasonable to decide the signal based on `thresh` than simply based on 0. But will the optimized `thresh` parameter lead to overfitting? At this point, we can observe the distribution of the tangent slope:

```python
def llt_slope(df, d: int=59, slope_window=5):
    df = df.copy()
    alpha = 2 / (d + 1)
    df["llt"] = calculate_llt(df["close"], alpha)
    df['slope'] = (df["llt"].rolling(slope_window)
                    .apply(lambda x: np.polyfit(np.arange(slope_window), x, 1)[0]))
    
    return df['slope']

start = datetime.date(2005, 1, 1)
end = datetime.date(2013, 12, 31)
prices= get_price("000001.SH", start, end)

slopes = llt_slope(prices, d = 39)
slopes.plot(kind='hist')
s1 = (slopes < -0.02).sum()/len(slopes)
s2 = (slopes < 0.02).sum()/len(slopes)

s2 - s1
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/07/20250718165206.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>Tangent Slope Distribution</span>
</div>
<!-- END IPYNB STRIPOUT -->

It can be seen that by setting `thresh` to [-0.02, 0.02], we only excluded about 0.3% of the data. This shows that we did not use hacking methods to exclude most scenarios, leaving only a small amount of data that makes the final return look good. Therefore, at least for the `thresh` parameter, it is very likely that overfitting has not occurred here.

If we use the parameters `d = 59, thresh = [-0.01, 0.01]` optimized from the 2008-2012 data unchanged from 2013 to 2024, the annualized return will decay to 2.79%. This shows that market styles are constantly changing. This strategy is essentially just a $\beta$ factor.

However, we can update the parameters every few years and then use this strategy for a short period thereafter.

The following code demonstrates how to search for optimized parameters based on the past five years of data and then use them for investment in the following two years:

```python
