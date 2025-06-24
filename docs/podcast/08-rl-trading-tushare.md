
强化学习（RL）这个名字，第一次闯入大众视野，还要追溯到AlphaGo与李世石那场载入史册的人机大战。一战成名后，它似乎又回归了学术的象牙塔，直到最近，随着DeepSeek等模型的惊艳亮相，RL以其强大的推理能力，再次被推到了聚光灯下。

其实，强化学习在量化投资中早有实际的应用。尽管一些顶尖的投资公司的当家策略不会轻易透露出来，我们还是找到了一些案例，表明华尔街的顶级玩家们早已开始使用强化学习。

比如，2017年前后，全球顶级的投资银行摩根大通（J.P. Morgan）就推出了一个名为LOXM<sup>1</sup>的“觅影”交易执行平台。而驱动这个平台的『秘密武器』，正是我们今天的主角——强化学习（Reinforcement Learning, RL）。

LOXM的目标非常明确：在执行大额股票订单时，像一个顶级交易员一样，智能地将大单拆分成无数小单，在复杂的市场微观结构中穿梭，以最低的冲击成本和最快的速度完成交易。这已经不是简单地预测涨跌，而是在动态的市场博弈中，学习“如何交易”这门艺术。

### 究竟什么是强化学习？
那么，这个听起来如此高大上的强化学习，到底是什么？

根据《Reinforcement Learning for Quantitative Trading》这篇文章，我们可以构建一个统一的框架来理解它。

想象一下，你正在玩一个电子游戏，你的目标是获得尽可能高的分数。在这个游戏里：

- 你，就是代理（Agent）。在量化交易中，这个代理就是你的交易算法。
- 游戏世界，就是环境（Environment）。在交易中，这就是瞬息万变的金融市场。
- 你在游戏中看到的画面和状态（比如你的血量、位置、敌人的数量），就是状态（State）。在交易中，这可以是股价、成交量、技术指标、宏观数据等等。
- 你按下的每一个操作（前进、后退、开火），就是行动（Action） 。在交易中，这对应着买入、卖出或持有。
- 你每次行动后获得或失去的分数 ，就是奖励（Reward）。在交易中，这通常是你的投资组合的收益或损失。
强化学习的核心思想，就是让代理（交易算法）在这个环境（金融市场）中不断地“试错”（take actions），根据每次试错后得到的奖励（收益或亏损），来学习一套最优的策略（Policy），从而在长期内实现累计奖励的最大化（长期收益最大化）。它不是在学习“市场下一秒会怎样”，而是在学习**『面对当前的市场，我该怎么做才是最优的』**。

## 强化学习强在哪儿？

看到这里，你可能会问，我们已经有了监督学习（比如预测股价涨跌）和无监督学习（比如聚类发现市场风格），为什么还需要强化学习？它到底强在哪？

强化学习与与监督/无监督学习的根本区别在于学习范式。监督学习像是在背一本标准答案书。你给它一张历史K线图（输入特征），告诉它第二天是涨还是跌（标签），它学习的是一种静态的"看图识字"能力。无监督学习则是在没有答案的情况下，自己在一堆数据里找规律，比如把相似的股票自动归为一类。它们都在试图回答"是什么"的问题。

而强化学习，则是在学习一套决策流程。它没有"标准答案"可背。市场不会告诉你"在此时此刻买入就是唯一正确的答案"。RL面对的是一系列的决策，每个决策都会影响到未来的状态和可能的收益。它要回答的是"该做什么"的问题。这是一个动态的、有因果链条的、面向未来的学习过程。

有人会说，我可以用监督学习模型，然后不断地用新的数据去持续训练和预测（即在线学习，live learning），这和强化学习有什么区别？

表面上看，两者都在不断适应新数据，但内核完全不同。而强化学习的核心优势在于两个监督学习无法企及的维度：

!!! tip 探索与利用（Exploration vs. Exploitation）
    这是RL的灵魂。想象一下，你常去的一家餐厅味道不错（利用），但你偶尔也会想试试新馆子，万一有惊喜呢（探索）？RL代理在训练时，也会在"执行已知的最优策略"和"尝试未知的、可能有更高回报的策略"之间进行权衡。这种探索精神，使得RL有可能发现人类交易员或监督学习模型从未想过的、更优的交易模式。而监督学习只会告诉你，根据历史经验，去那家老餐厅是"正确答案"。
  
  
!!! tip 学习动态因果关系
    强化学习关注的是一个行动序列（比如，先买入A，再卖出B）与最终结果之间的因果联系。它能理解，有时候一个短期的亏损（比如为了建仓拉低成本而主动承受浮亏）是为了一个更大的长期目标。而监督学习一次只看一个"时间切片"，它很难理解这种跨时间的、具有延迟效应的因果逻辑。

由于强化学习的这两个特点，所以，比起监督学习，它能更好地对抗金融噪声 -- 众所周知，深度学习在金融投资领域折戟沉沙，主要就是因为金融数据噪声太大的原因。

金融数据以低信噪比著称，充满了随机波动和"假信号"。强化学习之所以在这样的环境中更具优势，主要源于其独特的设计：

- 关注长期回报，容忍短期阵痛：监督学习模型追求的是在每个时间点上预测的准确率。如果市场噪音让它做出了一个错误的预测，它就会被"惩罚"。而RL的目标是最大化整个交易过程的累计回报。这意味着，它可以有意识地执行一个短期看起来会亏钱的动作（比如，在一个看似要下跌的时刻买入），如果这个动作是其长期制胜策略的一部分（比如，它判断这是一个主力洗盘的假摔）。这种"延迟满足"的特性，让它对短期市场噪音有更强的免疫力。

- 动态适应，而非刻舟求剑：市场风格是会切换的，昨天有效的因子，今天可能就失效了。监督学习模型一旦训练好，其模式就相对固定，像一个刻舟求剑的傻瓜。而RL代理的策略本身就是状态的函数，它被设计为根据环境的变化而动态调整自己的行为。当市场从牛市转向熊市，RL代理能够通过与环境的持续交互，感知到这种变化，并相应地调整其交易策略，从激进做多转为保守甚至做空。这种与生俱来的适应性，是其对抗非平稳市场的关键。


## 从"追涨杀跌"的AlphaStock说起

顶级机构的量化策略都是秘而不宣的，即使是摩根大通的LOXM这种公开出圈的模型，其构建与运行机制对普通人来讲，也仍然是无法接触的。那么，作为量化交易者，我们要如何构建自己的强化学习交易模型呢？

2019年，来自清华大学和微软亚洲研究院的团队开发了一个名为 AlphaStock<sup>1</sup> 的模型。这个模型巧妙地将强化学习与注意力机制（Attention Mechanism，没错，就是Transformer模型的核心）相结合，专门用来优化一个古老而有效的策略——追涨杀跌（即动量交易）。

传统的动量策略很简单：买入过去表现好的股票，卖出过去表现差的。但问题是，动量什么时候会持续？什么时候会反转？AlphaStock的聪明之处在于，它不依赖于固定的规则，而是让RL代理去学习。代理观察市场上数百只股票的价格和成交量数据（状态），然后决定在哪些股票上分配多少资金（行动）。如果这个决策在未来一段时间带来了正收益，它就获得正奖励，反之亦然。通过海量历史数据的回测训练，AlphaStock最终就能会了如何动态地识别和利用市场中的动量效应，甚至能在一定程度上规避动量反转的风险。这就像一个武林高手，通过无数次实战，最终练就了对战局的敏锐直觉。

## Get Hands Dirty!动手练一下！

理论听起来很美，但如何付诸实践？我们自己能否做出来一个有用的强化学习模型？接下来，我就演示如何做出一个

对于那些可以『无限』（即不受限）访问yfinance及alpaca_trade_api的同学，我强烈推荐从 FinRL 这个开源库开始。它被誉为"金融领域的OpenAI Gym"，极大地降低了入门门槛。

### 安装 FinRL

首先，确保你有一个Python环境（推荐使用Anaconda或venv创建虚拟环境），然后通过pip安装FinRL及其依赖。

```bash
pip install finrl
```

但是，我们的读者可能多数无法使用yfinance及alpaca_trade_api库。这样，你可能就不得不使用Gymnasium库，自己做多一点工作。

!!! tip
    Gymnasium 是 OpenAI Gym 的继任者，是用于开发和比较强化学习算法的开源工具包。它提供了标准化的环境接口，让研究者和开发者能够更方便地测试算法性能。

### 安装 Gymnasium和SB3！

如果不用FinRL，我们就要安装两个名字奇奇怪怪的强化学习库。

!!! tip
    “Gymnasium” 一词源于古希腊语 “γυμνάσιον”（gymnasion），字面意思是 “裸体锻炼的地方”。现代英语中，常指健身房。但在德语中，也指初级中学。

SB3即是Stable-Baselines3，是强化学习领域的主流库之一，凭借其高效性、易用性和丰富的算法支持，成为学术研究和工业应用的首选工具。

这两个库中，Gym是接口，而SB3提供了各种算法。在我们的示例中，将使用它提供的PPO算法。下面是安装这两个库的指南。

```bash
pip install gymnasium
pip install stable_baselines3
```

接下来，需要获取数据，进行一些特征工程。为避免文章太长，我们省略这些没有营养的东西。对代码感兴趣的读者，可以订阅我们研究平台进行查看（和运行）。

<!--PAID CONTENT START-->

```python
# 导入基础库（避免复杂依赖）
import pandas as pd
import numpy as np
import talib

from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

A_STOCK_LIST = [
    '000001.SZ',  # 平安银行
    '000002.SZ',  # 万科A
    '000858.SZ',  # 五粮液
    '002415.SZ',  # 海康威视
    '600000.SH',  # 浦发银行
    '600036.SH',  # 招商银行
    '600519.SH',  # 贵州茅台
    '600887.SH',  # 伊利股份
    '002594.SZ'   # 比亚迪
]

TRAIN_START_DATE = "20190101"
TRAIN_END_DATE = "20200701"
TRADE_START_DATE = "20200701"
TRADE_END_DATE = "20211031"

def get_stock_data_tushare(stock_list, start_date, end_date):
    all_data = []
    
    for stock in stock_list:
        try:
            # 获取日线数据
            df_stock = pro.daily(ts_code=stock, 
                                start_date=start_date, 
                                end_date=end_date)
            
            if not df_stock.empty:
                # 重命名列以符合FinRL格式
                df_stock = df_stock.rename(columns={
                    'ts_code': 'tic',
                    'trade_date': 'date',
                    'vol': 'volume'
                })
                
                # 转换日期格式
                df_stock['date'] = pd.to_datetime(df_stock['date'])
                
                # 按日期排序（tushare返回的数据是倒序的）
                df_stock = df_stock.sort_values('date').reset_index(drop=True)
                
                # 选择需要的列
                df_stock = df_stock[['date', 'tic', 'open', 'high', 'low', 'close', 'volume']]
                
                all_data.append(df_stock)
                print(f"成功获取 {stock} 的数据，共 {len(df_stock)} 条记录")
            else:
                print(f"警告：{stock} 没有数据")
                
        except Exception as e:
            print(f"获取 {stock} 数据时出错: {e}")
    
    if all_data:
        # 合并所有股票数据
        df_combined = pd.concat(all_data, ignore_index=True)
        return df_combined
    else:
        return pd.DataFrame()

class FeatureEngineer:
    """
    使用TA-Lib计算技术指标
    """
    
    def __init__(self, use_technical_indicator=True, tech_indicator_list=None):
        self.use_technical_indicator = use_technical_indicator
        self.tech_indicator_list = tech_indicator_list or [
            'macd', 'rsi', 'sma', 'bbands'
        ]

    def preprocess_data(self, df):
        """
        改进版本的数据预处理函数
        """
        print("🔧 开始计算技术指标...")

        if not self.use_technical_indicator:
            return df.copy()

        processed_stocks = []

        for tic in df['tic'].unique():
            stock_data = df[df['tic'] == tic].copy().sort_values('date')

            close = stock_data['close'].values.astype(float)

            if 'macd' in self.tech_indicator_list:
                macd, macd_signal, macd_hist = talib.MACD(close)
                stock_data['macd'] = macd
                stock_data['macd_signal'] = macd_signal
                stock_data['macd_hist'] = macd_hist

            if 'rsi' in self.tech_indicator_list:
                stock_data['rsi_14'] = talib.RSI(close, timeperiod=14)

            if 'sma' in self.tech_indicator_list:
                stock_data['close_20_sma'] = talib.SMA(close, timeperiod=20)

            if 'bbands' in self.tech_indicator_list:
                bb_upper, bb_middle, bb_lower = talib.BBANDS(close, timeperiod=20)
                stock_data['boll_ub'] = bb_upper
                stock_data['boll_lb'] = bb_lower
                stock_data['boll_middle'] = bb_middle

            # 添加基础指标
            stock_data['returns'] = stock_data['close'].pct_change()
            stock_data['log_volume'] = np.log(stock_data['volume'] + 1)

            processed_stocks.append(stock_data)

        # 一次性合并所有数据
        df_processed = pd.concat(processed_stocks, ignore_index=True)

        # 删除包含NaN的行
        before_count = len(df_processed)
        df_processed = df_processed.dropna().reset_index(drop=True)
        after_count = len(df_processed)

        print(f"✅ 技术指标计算完成: {before_count} -> {after_count} 条记录")

        # 显示新增的列
        new_columns = [col for col in df_processed.columns if col not in df.columns]
        print(f"新增指标: {new_columns}")

        return df_processed

def data_split(df, start, end):
    """
    数据分割函数
    """
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df[mask].copy().reset_index(drop=True)

# 创建特征工程器
fe = FeatureEngineer(
    use_technical_indicator=True,
    tech_indicator_list=['macd', 'rsi', 'sma', 'bbands']
)

# 获取数据
print("开始获取股票数据...")
raw_data = get_stock_data_tushare(A_STOCK_LIST, TRAIN_START_DATE, TRADE_END_DATE)
print(f"数据获取完成，总共 {len(raw_data)} 条记录")
print("数据预览:")
print(raw_data.head())

# 处理数据
processed_data = fe.preprocess_data(raw_data)

# 分割数据
train_data = data_split(processed_data, "2020-01-01", "2020-06-30")
test_data = data_split(processed_data, "2020-07-01", "2020-12-31")

print(f"\n📈 训练数据: {train_data.shape}")
print(f"📊 测试数据: {test_data.shape}")

# 显示处理后的数据样例
print("\n处理后的数据预览:")
print(train_data.head())
```
<!--PAID CONTENT END-->


### 定义环境

通常来说，我们要定义环境和Agent，但是，在使用SB3之后，我们可以直接使用PPO模型，从而无须定义Agent，因为PPO本身就是Agent，所以，Agent的定义和模型训练是一体的。

所以，我们先用gym来定义环境：

```python
import gymnasium as gym
from gymnasium import spaces

class StockTradingEnv(gym.Env):
    """
    基于Gymnasium的股票交易环境
    
    动作空间: 连续动作，每只股票的买卖比例 [-1, 1]
    状态空间: [现金比例, 持仓比例..., 技术指标...]
    """
    
    def __init__(self, data, initial_amount=100000, transaction_cost=0.001):
        super().__init__()
        
        self.data = data.copy()
        self.initial_amount = initial_amount
        self.transaction_cost = transaction_cost
        
        # 获取股票列表和日期
        self.stock_list = sorted(self.data['tic'].unique())
        self.dates = sorted(self.data['date'].unique())
        self.stock_dim = len(self.stock_list)
        
        # 技术指标列表
        self.tech_indicators = ['macd', 'rsi_14', 'close_20_sma', 'boll_ub', 'boll_lb']
        
        # 定义动作和观察空间
        # 动作: 每只股票的买卖比例 [-1, 1]
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(self.stock_dim,), dtype=np.float32
        )
        
        # 观察空间: [现金比例] + [持仓比例...] + [技术指标...]
        obs_dim = 1 + self.stock_dim + len(self.tech_indicators) * self.stock_dim
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )
        
        print(f"🏗️  环境初始化完成:")
        print(f"   股票数量: {self.stock_dim}")
        print(f"   交易日数: {len(self.dates)}")
        print(f"   动作维度: {self.action_space.shape}")
        print(f"   状态维度: {self.observation_space.shape}")
        
        self.reset()
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.day = 0
        self.cash = self.initial_amount
        self.holdings = np.zeros(self.stock_dim)
        self.portfolio_value = self.initial_amount
        self.portfolio_history = [self.initial_amount]
        
        observation = self._get_observation()
        info = {}
        
        return observation, info
    
    def step(self, actions):
        # 检查是否结束
        if self.day >= len(self.dates) - 1:
            return self._get_observation(), 0, True, True, {}
        
        # 获取当前价格
        current_date = self.dates[self.day]
        current_data = self.data[self.data['date'] == current_date]
        prices = np.array([current_data[current_data['tic'] == stock]['close'].iloc[0] 
                          for stock in self.stock_list])
        
        # 执行交易
        self._execute_trades(actions, prices)
        
        # 移动到下一天
        self.day += 1
        
        # 计算新的投资组合价值
        if self.day < len(self.dates):
            next_date = self.dates[self.day]
            next_data = self.data[self.data['date'] == next_date]
            next_prices = np.array([next_data[next_data['tic'] == stock]['close'].iloc[0] 
                                   for stock in self.stock_list])
            new_portfolio_value = self.cash + np.sum(self.holdings * next_prices)
        else:
            new_portfolio_value = self.cash + np.sum(self.holdings * prices)
        
        # 计算奖励
        reward = (new_portfolio_value - self.portfolio_value) / self.portfolio_value
        self.portfolio_value = new_portfolio_value
        self.portfolio_history.append(self.portfolio_value)
        
        # 检查是否结束
        terminated = self.day >= len(self.dates) - 1
        truncated = False
        
        info = {
            'portfolio_value': self.portfolio_value,
            'cash': self.cash,
            'holdings': self.holdings.copy()
        }
        
        return self._get_observation(), reward, terminated, truncated, info
    
    def _execute_trades(self, actions, prices):
        """
        执行交易动作
        """
        # 计算目标持仓价值
        total_value = self.cash + np.sum(self.holdings * prices)
        
        for i, action in enumerate(actions):
            if abs(action) < 0.01:  # 忽略很小的动作
                continue
                
            current_value = self.holdings[i] * prices[i]
            target_value = total_value * max(0, action)  # 只允许正持仓
            trade_value = target_value - current_value
            
            if trade_value > 0:  # 买入
                cost = trade_value * (1 + self.transaction_cost)
                if cost <= self.cash:
                    shares_to_buy = trade_value / prices[i]
                    self.holdings[i] += shares_to_buy
                    self.cash -= cost
            elif trade_value < 0:  # 卖出
                shares_to_sell = abs(trade_value) / prices[i]
                if shares_to_sell <= self.holdings[i]:
                    self.holdings[i] -= shares_to_sell
                    self.cash += abs(trade_value) * (1 - self.transaction_cost)
    
    def _get_observation(self):
        """
        获取当前状态观察
        """
        if self.day >= len(self.dates):
            # 返回最后一天的观察
            self.day = len(self.dates) - 1
        
        current_date = self.dates[self.day]
        current_data = self.data[self.data['date'] == current_date]
        
        # 现金比例
        cash_ratio = self.cash / self.portfolio_value if self.portfolio_value > 0 else 0
        
        # 持仓比例
        prices = np.array([current_data[current_data['tic'] == stock]['close'].iloc[0] 
                          for stock in self.stock_list])
        holdings_value = self.holdings * prices
        holdings_ratio = holdings_value / self.portfolio_value if self.portfolio_value > 0 else np.zeros_like(holdings_value)
        
        # 技术指标
        tech_values = []
        for stock in self.stock_list:
            stock_data = current_data[current_data['tic'] == stock]
            for indicator in self.tech_indicators:
                if indicator in stock_data.columns:
                    value = stock_data[indicator].iloc[0]
                    # 标准化技术指标
                    if indicator == 'rsi_14':
                        value = (value - 50) / 50  # RSI标准化到[-1, 1]
                    elif 'macd' in indicator:
                        value = np.tanh(value / 100)  # MACD使用tanh标准化
                    else:
                        value = np.tanh(value / stock_data['close'].iloc[0])  # 相对价格标准化
                    tech_values.append(value if not np.isnan(value) else 0)
                else:
                    tech_values.append(0)
        
        # 组合观察向量
        observation = np.concatenate([
            [cash_ratio],
            holdings_ratio,
            tech_values
        ])
        
        return observation.astype(np.float32)

# 创建环境
print("🏗️  创建交易环境...")
train_env = StockTradingEnv(train_data, initial_amount=100000)
test_env = StockTradingEnv(test_data, initial_amount=100000)

print("\n✅ 环境创建完成！")
```

## 定义Agent及训练

```python
from stable_baselines3 import PPO

model = PPO(
    "MlpPolicy",
    train_env,
    verbose=1,
    learning_rate=0.0003,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5,
    seed=42
)

print("🚀 开始训练...")
model.learn(total_timesteps=10000, progress_bar=True)
print("✅ 训练完成！")

# 保存模型
# model.save("ppo_trading_model")
```

### 回测与结果

现在，我们开始回测，并将回测结果可视化。

```python
print("📊 开始回测...")
obs, _ = test_env.reset()
done = False
total_reward = 0
step_count = 0
portfolio_values = []

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = test_env.step(action)
    done = terminated or truncated
    total_reward += reward
    step_count += 1
    portfolio_values.append(info['portfolio_value'])
    
    if step_count % 20 == 0:
        print(f"步骤 {step_count}: 投资组合价值 = ¥{info['portfolio_value']:,.2f}")

print(f"\n📈 回测完成!")
print(f"总步数: {step_count}")
print(f"总奖励: {total_reward:.4f}")
print(f"最终投资组合价值: ¥{portfolio_values[-1]:,.2f}")
print(f"总收益率: {(portfolio_values[-1] / 100000 - 1) * 100:.2f}%")

# 绘制投资组合价值变化
plt.figure(figsize=(12, 8))

# 子图1: 投资组合价值
plt.subplot(2, 1, 1)
plt.plot(portfolio_values, label='强化学习策略', linewidth=2)
plt.axhline(y=100000, color='r', linestyle='--', label='初始资金')
plt.title('投资组合价值变化', fontsize=14, fontweight='bold')
plt.ylabel('投资组合价值 (¥)')
plt.legend()
plt.grid(True, alpha=0.3)

# 子图2: 收益率
plt.subplot(2, 1, 2)
returns = [(v / 100000 - 1) * 100 for v in portfolio_values]
plt.plot(returns, label='累积收益率', color='green', linewidth=2)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)
plt.title('累积收益率变化', fontsize=14, fontweight='bold')
plt.xlabel('交易日')
plt.ylabel('收益率 (%)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 计算关键指标
final_return = (portfolio_values[-1] / 100000 - 1) * 100
daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]
volatility = np.std(daily_returns) * np.sqrt(252) * 100  # 年化波动率
sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252) if np.std(daily_returns) > 0 else 0

print("\n📊 关键绩效指标:")
print(f"总收益率: {final_return:.2f}%")
print(f"年化波动率: {volatility:.2f}%")
print(f"夏普比率: {sharpe_ratio:.3f}")
print(f"最大回撤: {((np.minimum.accumulate(portfolio_values) - portfolio_values) / np.minimum.accumulate(portfolio_values)).max() * 100:.2f}%")
```




总而言之，强化学习为量化交易打开了一扇通往更高维度智能的大门。它不再是让机器模仿人类，而是让机器在模拟的市场中自我进化、自我博弈，最终习得超越人类直觉的交易智慧。这条路充满挑战，但也同样充满机遇。那么，你准备好，让你的第一个交易Agent，开始它的"进化之旅"了吗？

---
1. LOXM: https://www.businessinsider.com/jpmorgan-takes-ai-use-to-the-next-level-2017-8
2. 量化交易中的强化学习：https://dl.acm.org/doi/10.1145/3582560
3. Alphastock，一个追涨杀跌模型: https://arxiv.org/abs/1908.02646
