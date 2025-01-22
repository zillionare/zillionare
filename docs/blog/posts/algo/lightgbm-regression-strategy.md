---
title: 地表最强挑战！资产价格预测，我们如何做到0.5%以下误差
---

<!--这里有两块金条，你能说哪一块是高尚的，哪一块是卑劣的？但实际上，散户的钱没有定价的权力，但有更强的购买力，他们可以以自己想要的价格买到股票；主力的钱有定价的权力，但购买力较弱，他们很难以自己想要的价格买到股票-->

资产价格预测一直是个难题。诺贝尔奖都拿了好几期了，可能现在大家才发觉，这个命题本身可能就不成立。

不过，在一些限定的条件下，短期的价格预测并且从中获得套利则仍然是完全可能的。今天我们就来证明这一点。

我们会讨论三个有效的版本。其中v1版源代码可通过星球获得；v2版源码对《QuanTide: 因子分析与机器学习策略》学员开发。最强的v3版本虽然不对外开放，但是，一旦掌握了基本原理，以及和我们类似的研究方法，迟早也会有人自己能开发出来。

!!! tip
    这里有两块金条，你能说哪一块是高尚的，哪一块是卑劣的？这是某谍战剧中我很喜欢的的一句台词。但在股市中，散户的钱和主力的钱，尽管同样是钱，却有着不同的特性：散户的钱没有定价的能力，但能以自己想要的价格买入股票；主力的钱有定价的能力，但却无法以自己想要的价格买入股票（指短线操作）。这是小体量资金可以套利的空间：发现主力的定价和意图，在不影响主力定价的前提下，实现自己的利润。

因为是定价任务，所以，我们要使用回归模型。这一次，我们将使用lightgbm来完成。

## v0: vanllina版本

首先，我们来看一个网络上随处可见的例子（请对各种论文袪魅！这几乎就是各种论文会讲的例子）。不过，我们在数据集划分上略微做了一点增强，以便无论我们得到什么样的结果，它至少不是荒谬的、或者是包含了未来数据的。

```python
np.random.seed(78)
start = datetime.date(2023, 1, 1)
end = datetime.date(2023, 12, 29)
universe = 2000
barss = load_bars(start, end, universe=universe)
```

首先，我们随机选择2000只股票一年的行情数据。接下来，我们将使用每支股票过去10天的价格作为特征，来预测下一天的价格。我们通过下面的代码来实现特征提取：

```python
from numpy.lib.stride_tricks import as_strided

def rolling_time_series(ts: NDArray, win: int):
    stride = ts.strides
    shape = (len(ts) - win + 1, win)
    strides = stride + stride
    return as_strided(ts, shape, strides)
    
def rolling_close(group, win, columns):
    index = group.index
    if len(group) < win:
        features = np.full((len(group), win), np.nan)
        df = pd.DataFrame(features, columns=columns, index=index)
        return df
        
    rolled = rolling_time_series(group["close"].values, win)
    padded = np.pad(
        rolled, ((win-1, 0), (0,0)), mode="constant", constant_values=np.nan)
    df = pd.DataFrame(padded, columns=columns, index=index)
    return df

win = 10
feature_cols = [f"c{win-i}" for i in range(win)]

features = barss.groupby(level="asset").apply(rolling_close, win, columns = feature_cols)
features = features.droplevel(0)
features.tail()
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/lightgbm-rolling-close-features.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

<!-- v1
我们生成的数据格式是以date/asset为索引的DataFrame，过去10天的价格作为特征。不过，我们还会把asset本身也作为一种特征来使用，毕竟，每一支股票都可能有自已独特的走势，我们希望模型也能关注到这些特点。


训练目标(target)自然是次日收盘价。在训练中，框架一般要求分别提供特征X和target y，但它们必须是对齐的。到目前为止，我们得到的数据集都是以date/asset进行索引的。既然索引相同，我们就可以简单地利用赋值来进行对齐。

```python
data=features
data["target"] = barss["close"].unstack().shift(-1).stack()
data = data.reset_index(level=1).dropna(subset=["target"])
data.tail()
```




<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/lightgbm-rolling-close-target.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>


输出结果的索引是日期，但与特征集比，多出了asset和target列。

-->

接下来，我们就生成划分数据集，最终生成可以用来训练的lightgbm的dataset格式。

```python
import lightgbm as lgb
def train_test_split(data, feature_cols, cuts = (0.7,0.2)):
    train, valid, test = [], [], []
    def cut_time_series(group, cuts):
        itrain = int(len(group) * cuts[0])
        ival = itrain + int(len(group) * cuts[1])

        return (group.iloc[:itrain], group.iloc[itrain: ival], group.iloc[ival:])

    for item in data.groupby("asset").apply(cut_time_series, cuts=cuts).values:
        train.append(item[0])
        valid.append(item[1])
        test.append(item[2])

    df_train = pd.concat(train)
    df_valid = pd.concat(valid)
    df_test = pd.concat(test)

    return (df_train[feature_cols], df_valid[feature_cols], df_test[feature_cols], 
            df_train["target"], df_valid["target"], df_test["target"])

data=features
data["ret"] = barss["close"].unstack().pct_change().stack()
data["target"] = barss["close"].unstack().shift(-1).stack()
data = data.dropna(subset=["target", "ret"])
data.reset_index(inplace=True)

(X_train, X_val, X_test, 
y_train, y_val, y_test) = train_test_split(data, feature_cols)

train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_val, label=y_val)
```

在特征中，包含了一些nan值，我们并没有进行任何处理；但对target中的nan进行了处理。lightgbm要求target必须为浮点、整数或者bool，不接受包括nan在类的其它任何类型。但对特征数据并没有要求，它在训练时，可以处理好这些输入。

<!--

当我们把股票代码作为特征时，需要把它当成类别特征（从交易含义及数据格式要求上看都是如此）。lighgtgbm可以直接处理类别特征，无需转换成为独热码。但在此之前，我们也必须将它转换为整数编码。这个任务是由sklearn中的LabelEncode完成的。

-->

我们把数据划分为三份，训练集、验证集和测试集。训练集和验证集用于训练和调参，测试集用于最终的模型性能评测。这部分做法在后面的改进版本中，也将会保持如此。

注意在划分数据集时，我们充分考虑了时间序列的特点，并没有使用现成的库，比如sklearn中的train_test_split来实现，而是自己实现了一个能保持时间顺序的切分方法。在这个实现中，大致上是用前8个月的数据训练，前2个月的数据验证和调优，用最后一个多月的数据来对模型的性能进行最终评定。

这种划分也保证了模型的泛化能力，即，训练出来的模型，至少能保持三个月以上的有效性。

现在，我们开始训练模型。

```python
from sklearn.metrics import mean_absolute_percentage_error
params = {
    'objective': 'regression',
    'metric': 'mape',
    'num_leaves': 31,
    'learning_rate': 0.05
}

esr = 50
evals_result = {}

num_rounds = 500
model = lgb.train(
    params,
    train_data,
    num_boost_round=num_rounds,
    valid_sets=[valid_data],
    callbacks = [lgb.early_stopping(esr), lgb.record_evaluation(evals_result)]
)

y_pred = model.predict(X_test.values)
mean_absolute_percentage_error(y_test, y_pred)
```

在训练中，我们使用了early stopping来控制训练结束。在训练结束之后，我们立即使用测试集进行预测，并计算了mape。

我们使用了mean absolute percentage error（即mape）作为评估指标，这个指标非常直观。我们通过变更随机数，先后运行了10次，这10次的平均误差约为1.7%（标准差为0.1%），表明我们的方法是稳定的。

这个结果看起来不错。我们甚至可以假设，既然模型预测的误差只有1.7%，那么，在一个做多的策略中，如果我们选择预测价格高于现价1.7%的股票买入，不就可以实现盈利了吗？

不过，直觉告诉我们，印钞机不应该这么容易制造。下面，我们深入分析到底发生了什么。

## v0版真的有效吗？

实际上，尽管v0版看上去误差并不大，但其实是被众多低波动的数据点平均的结果。每日波动在正负1.7%以内的数据点超过了76%，它们足以把少数的高波动数据点抵消。比如，在平安银行这样的个股上，mape就只有1%不到，但同时，它的波动也不到0.9%。这种情况下，只要模型拿当前的收盘价去预测次日收盘价，准确率就很高，但没有任何意义。

我们可以把模型的决策树绘制出来，就能清晰地看到这一点：

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/blog-17-v0-tree.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>第0号树</span>
</div>

在梯度提升树中，第0号树最先被构建出来，它负责捕捉数据中最主要的走势或者模式。其它的树只是负责消化第0号树所不能解释的残差或者少数情况，不能影响大的走势、或者多数场景。

我们把第2棵树绘制出来，两相比较，就能验证上述结论。


<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/blog-17-v0-treeplot-1.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>第1号树</span>
</div>


第2棵树的叶子结点值远小于第一棵树。而且，在这两棵树中，特征c1都是分裂的最常用依据。因此，在这个模型中，昨收主导了预测。因此，它没有任何意义。

为什么会这样呢？实际上，它是决策树的原理决定的。决策树能够拟合出复杂的非线性函数，但它不能发现相邻节点之间的规律（即时间序列的规律）。我们可以通过以下试验来验证这个结论。

```python
import lightgbm as lgb

def generate_data():
    np.random.seed(42)
    c = np.linspace(0, 1, 100)
    p = np.random.rand(100)
    target = c * (1 + p)
    df = pd.DataFrame({'c': c, 'p': p, 'target': target})
    return df

def train_lightgbm_model(df):
    X = df[['c', 'p']]
    y = df['target']
    train_data = lgb.Dataset(X, label=y)
    params = {
       'objective':'regression',
       'metric': 'rmse',
       'num_leaves': 31,
       'learning_rate': 0.05,
       'feature_fraction': 0.9,
       'verbosity': -1
    }
    model = lgb.train(params, train_data, num_boost_round=2)
    return model

df = generate_data()

model = train_lightgbm_model(df)

c = np.linspace(0, 100, 10)
p = np.linspace(1, 1, 10)
test_data = pd.DataFrame({
    "c": c,
    "p": p
})

y_pred = model.predict(test_data)

print(y_pred)
```

代码输出的预测值为[0.681, 0.7914, ...]。冒号部分的数值都是0.7914。

我们希望lightgbm能发现数据的简单规律：一条 $y=c + c \times p$的直线。我们在[0,1]的区间对它进行训练，为了简单起见，我们只训练了两轮（你可以按这里讲的原理，训练多轮，但不改变基本结论），因此，lightgbm将构建两棵树。

这是它构造的零号树:

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/blog-17-sample-tree.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>模拟数据: 零号树</span>
</div>

这是它构建的1号树：

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/blog-17-sample-tree-1.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

如果我们把数值c=11, p=1代入两棵决策树，我们会发现，最终会分别落到0.765和0.027的叶子结点上。这两个值加起来，就等于预测值0.7914(小数部分受4舍5入影响)。

这就是梯度提升决策树在回归任务时的算法。因此，**如果我们使用收盘价作为特征，那么，它几乎不能从中学习到任何有用的东西**。并且，v0模型还会把不同的股票的收盘价混在一起，也就是，只要价格都是10元，工商银行和一个小盘股在10元上的表现没有任何区别。

所以，要增强lightgbm的预测能力，我们必须改进特征，把提取出来的规律喂给它。lightgbm能帮助我们的在于，它能知道每个规律的统计分布，知道如何平衡多个特征的影响。

## 有效评估指标

在v0版中，我们还看到一个问题，就是传统的评估指标对量化交易并没有什么效果。**因为模型只是拿昨天的收盘价糊弄了一下，数据就并没有很差**。即使我们训练出一个模型，它的mape指标（这已经是很多论文推荐的适合量化的指标了）降到0.5%，又能如何？我们心里一样没底。

所以，我们需要根据交易的需要，自己发明『有效的』评估指标。

```python
from matplotlib.dates import WeekdayLocator

def eval_model(model, X_test, data, long_threshold = 0.02, traces:int = 0):
    df = data.rename(columns={"c1": "prev", "target": "actual"})
    df = df.loc[X_test.index]
    
    df["pred"] = model.predict(X_test.values)
    
    error = mean_absolute_percentage_error(df["actual"], df["pred"])

    print(f"mape is {error:.3f}")
                                       
    df["pred_ret"] = df["pred"]/df["prev"] - 1

    long_df = df.query(f"pred_ret > {long_threshold}")

    print(f'actual p&l {long_df["ret"].mean():.2%}')

    if traces > 0:
        row = int(np.sqrt(traces))
        col = int(traces / row)

        if row * col < traces:
            row += 1

        symbols = long_df["asset"].unique()[:traces]
        _, axes = plt.subplots(row, col, figsize=(row * 4, col * 2))
        axes = axes.flatten()
        
        for i, symbol in enumerate(symbols):
            close = df.query(f"asset == '{symbol}'")[["prev", "date"]].set_index("date")
            x = list(close.index.strftime("%m/%d"))
            axes[i].plot(x, close, label="close")

            pred_close = df.query(f"asset == '{symbol}'")["pred"]
            axes[i].plot(x[1:], pred_close[:-1], label="pred")

            locator = WeekdayLocator()
            axes[i].xaxis.set_major_locator(locator)
            
            # mark signals
            signal_dates = df.query(f"pred_ret > {long_threshold}")["date"]
            x = [i.strftime("%m/%d") for i in signal_dates]
            y = close.loc[signal_dates]
            axes[i].scatter(x, y, marker='^', color='red')
            axes[i].set_title(symbol)
            axes[i].legend()

        plt.tight_layout()

eval_model(model, X_test, data, traces = 6)
```

这个函数的主要功能有这样几点：
1. 计算出mape指标
2. 计算在预测收益大于指标阈值时，以t0收盘价买入，t1收盘价卖出，得到的p&l均值。这才是我们要追求的目标。
3. 对预测收益大于指标阈值的样本，随机挑选几支进行可视化。

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://images.jieyu.ai/images/2025/01/blog-17-eval-model-output.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>eval model的可视化</span>
</div>
这个评估指标合理多了。毕竟，在实际交易中，我们只会关注那些预测上涨较多的样本。如果这部分样本预测结果正确，那么模型就是有效的。

现在，根据新的评估函数，之前的模型在2023年11月到12月期间，mape值为0.017，但如果你挑预测上涨2%的个股买入，平均每次能亏0.73%。

lightgbm是个好算法，但它不是银弹，更没有点石成金的魔法。

## v1: 增强特征工程





