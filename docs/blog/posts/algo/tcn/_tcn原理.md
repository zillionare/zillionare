---
title: 时间卷积网络：为什么它成了我的默认选择
date: 2024-09-15
category: algo
slug: temporal-convolutional-network
motto: 简单的东西往往最有效
tags: [algo, TCN, deep-learning]
---

我曾经是 LSTM 的忠实信徒。

从2017年开始，几乎所有的时间序列预测项目，我的第一反应都是堆叠几层 LSTM。门控机制、遗忘门、细胞状态 —— 这些概念听起来就很"智能"，不是吗？

但问题也随之而来。训练慢是一方面，更头疼的是调参。学习率、隐藏层维度、层数、dropout 比例... 稍微改动一下，结果就可能天差地别。我曾有一个项目，同样的数据，只是随机种子不同，结果一个能赚钱，一个亏掉20%。

直到2018年，我在一篇论文里看到 TCN（Temporal Convolutional Network）的介绍。当时我的第一反应是：卷积？那不是用来做图像的吗？

但试了之后，我就再也没回去用过 LSTM。

## 从 LSTM 的困境说起

LSTM 的核心问题是：**它必须一步一步地计算**。

要预测第100天的价格，你必须先算出第99天的隐藏状态；要算第99天，必须先算第98天... 这种串行结构意味着，无论你的GPU多强大，它也只能一个时间步一个时间步地跑。

更要命的是梯度消失。虽然 LSTM 用门控机制缓解了这个问题，但当序列长度超过一定程度（我的经验是60天左右），前面的信息基本上就传不到后面了。你输入了120天的数据，实际上模型能"记住"的，可能只有最近两个月。

我曾经尝试过各种技巧：双向 LSTM、Attention 机制、分层结构... 效果都有，但代价是模型越来越复杂，训练时间越来越长，而且过拟合的风险也随之增加。

TCN 的出现，某种程度上是一种"返璞归真"。

## 因果卷积：一个简单但关键的设计

TCN 的第一个核心设计是**因果卷积**（Causal Convolution）。

这个名字听起来很学术，但概念极其简单：预测第 t 天的价格时，只能用第 t 天及之前的数据，不能用未来的数据。

你可能会说：这不是理所当然的吗？

但标准的卷积操作并不满足这个约束。想象一下，一个卷积核在序列上滑动时，它通常是中心对齐的 —— 这意味着计算当前位置的输出时，会同时用到前面和后面的数据。对于图像来说这没问题，但对于时间序列预测来说，这就是"作弊"了。

TCN 的解决方案很简单：**只在左侧做 padding**。

```python
import torch.nn as nn

# 标准卷积：两边都 padding，会用到未来数据
standard_conv = nn.Conv1d(in_ch, out_ch, kernel_size=3, padding=1)

# 因果卷积：只在左侧 padding
causal_padding = kernel_size - 1
causal_conv = nn.Conv1d(in_ch, out_ch, kernel_size=3, padding=causal_padding)
# 然后切掉右侧多余的输出
output = output[:, :, :-causal_padding]
```

这个设计如此简单，以至于我第一次看到时甚至有些失望 —— 就这就解决了？但事实证明，简单的东西往往最有效。

## 膨胀卷积：看到更远的过去

解决了因果性问题，下一个挑战是**感受野**。

在卷积网络中，感受野指的是一个输出单元能"看到"的输入范围。对于时间序列预测来说，感受野越大，模型能利用的历史信息就越多。

但普通的卷积层堆叠，感受野增长是线性的：
- 1层，kernel=3 → 感受野 = 3
- 2层，kernel=3 → 感受野 = 5  
- 3层，kernel=3 → 感受野 = 7

如果要覆盖一年的交易日（约250天），你需要堆叠100多层。这不仅计算量大，还会导致梯度消失问题卷土重来。

TCN 的第二个核心设计是**膨胀卷积**（Dilated Convolution）。

膨胀卷积的思想是：**跳着采样**。膨胀率（dilation）为 d 的卷积，在采样时会间隔 d-1 个位置。

```python
# 膨胀率为 2 的卷积：采样位置是 x[t], x[t-2], x[t-4]
dilated_conv = nn.Conv1d(in_ch, out_ch, kernel_size=3, 
                         padding=2, dilation=2)
```

关键是，TCN 采用**指数增长的膨胀率**：第1层 d=1，第2层 d=2，第3层 d=4，第4层 d=8...

这样，感受野的增长变成了指数级：
- 第1层 (d=1) → 感受野 = 3
- 第2层 (d=2) → 感受野 = 7
- 第3层 (d=4) → 感受野 = 15
- 第4层 (d=8) → 感受野 = 31
- 第5层 (d=16) → 感受野 = 63
- 第6层 (d=32) → 感受野 = 127

只需要6层，就能覆盖约半年的交易日。这是 LSTM 很难做到的。

## 残差连接：让深度成为可能

有了因果卷积和膨胀卷积，TCN 已经能工作了。但如果要堆叠更多层，还是会遇到梯度消失的问题。

TCN 的第三个设计是**残差连接**（Residual Connection），这也是从 ResNet 借鉴来的思想。

核心想法是：与其让网络学习从输入 x 到输出 y 的直接映射，不如让它学习 y - x 的"残差"。

```python
class TCNBlock(nn.Module):
    def __init__(self, in_ch, out_ch, kernel_size, dilation):
        super().__init__()
        self.conv1 = nn.Conv1d(in_ch, out_ch, kernel_size, 
                               padding=(kernel_size-1)*dilation, 
                               dilation=dilation)
        self.conv2 = nn.Conv1d(out_ch, out_ch, kernel_size,
                               padding=(kernel_size-1)*dilation,
                               dilation=dilation)
        # 如果输入输出维度不同，用 1x1 卷积调整
        self.downsample = nn.Conv1d(in_ch, out_ch, 1) if in_ch != out_ch else None
        
    def forward(self, x):
        residual = x if self.downsample is None else self.downsample(x)
        out = torch.relu(self.conv1(x))
        out = self.conv2(out)
        # 关键：残差连接
        return torch.relu(out + residual)
```

残差连接的神奇之处在于，它给梯度提供了一条"高速公路"。即使中间层的梯度很小，梯度也能通过残差路径直接传回输入层。这使得我们可以放心地堆叠十几层甚至更多，而不用担心梯度消失。

## 一个完整的 TCN 预测模型

把以上三个组件组合起来，就是一个完整的 TCN：

```python
class TCN(nn.Module):
    def __init__(self, input_size, num_channels, kernel_size=3, dropout=0.2):
        super().__init__()
        layers = []
        for i in range(len(num_channels)):
            dilation = 2 ** i
            in_ch = input_size if i == 0 else num_channels[i-1]
            out_ch = num_channels[i]
            layers.append(TCNBlock(in_ch, out_ch, kernel_size, dilation))
            layers.append(nn.Dropout(dropout))
        self.network = nn.Sequential(*layers)
        self.fc = nn.Linear(num_channels[-1], 1)
        
    def forward(self, x):
        # x: [batch, seq_len, features]
        out = self.network(x.transpose(1, 2))  # Conv1d 需要 [batch, ch, seq]
        out = out[:, :, -1]  # 取最后一个时间步
        return self.fc(out.transpose(1, 2))
```

使用时的配置示例：

```python
# 短线模型：关注最近1个月
tcn_short = TCN(input_size=5, num_channels=[32, 32, 32, 32])
# 感受野约 30 天

# 中线模型：关注最近2-3个月  
tcn_medium = TCN(input_size=5, num_channels=[64, 64, 64, 64, 64])
# 感受野约 60 天

# 长线模型：关注最近半年
tcn_long = TCN(input_size=5, num_channels=[64, 64, 64, 64, 64, 64])
# 感受野约 120 天
```

## 为什么我选择 TCN 作为默认方案

在实际项目中，TCN 给我带来了几个明显的好处：

**1. 训练速度快**

由于卷积操作可以并行计算，TCN 的训练速度通常是 LSTM 的3-5倍。在同样的数据集上，LSTM 可能需要训练2小时，TCN 只要30分钟。

**2. 超参数少**

TCN 的主要超参数只有：层数、每层的通道数、kernel 大小、dropout 比例。相比之下，LSTM 还需要考虑：是否双向、是否用 Attention、细胞状态的初始化方式... 调参空间大得多。

**3. 感受野可控**

通过调整层数和膨胀率，我可以精确控制模型能"看到"多远的过去。这在多因子策略中特别有用 —— 不同因子可能需要不同的时间尺度。

**4. 稳定性好**

同样的配置，多次运行的结果波动很小。这在我做回测时特别重要，因为我不想因为随机性而误判一个策略的有效性。

当然，TCN 也不是万能的。

## TCN 的局限

**1. 对局部模式的捕捉**

在某些任务中，LSTM 对局部模式的捕捉能力确实更强。特别是当序列中有复杂的、非线性的短期依赖时，LSTM 的门控机制可能更有优势。

**2. 变长序列处理**

TCN 要求输入序列长度固定（或者至少在每个 batch 内固定）。对于变长序列，需要额外的处理。而 LSTM 天然支持变长序列，通过 packed sequence 可以高效处理。

**3. 某些特定领域的 SOTA**

在语音识别、机器翻译等任务上，Transformer 已经全面超越了 TCN 和 LSTM。但在金融时间序列预测这个特定领域，TCN 仍然是我的首选。

## 一个未完成的实验

去年我尝试过一个想法：把 TCN 和 FFT 结合起来。

思路是这样的：先用 FFT 把价格序列分解成不同频率的成分，然后用多个 TCN 分别预测每个频率成分，最后把预测结果合成回去。

理论上，这可以让模型分别学习长期趋势（低频）和短期波动（高频）。

初步实验显示，在趋势明显的市场中，这种方法确实比单一 TCN 效果更好。但在震荡市中，不同频率的预测结果会互相干扰，反而降低了整体表现。

我还没有找到一个稳定的权重分配方案。如果你对这个方向感兴趣，欢迎交流。

## 总结

TCN 不是最时髦的模型，但它简单、高效、稳定。在工程实践中，这些品质往往比"最先进"更重要。

如果你还在用 LSTM 做时间序列预测，不妨给 TCN 一个机会。也许它不会让你失望。

本文的完整代码和更多策略实现，已上传到我们的课程环境。加入投研圈子即可获取。

<!-- 有时候我在想，深度学习领域是不是太追求复杂度了。ResNet、DenseNet、Transformer、Mamba... 每一代都在增加更多的机制、更多的参数。但 TCN 提醒我，有时候减法比加法更有效 -->
