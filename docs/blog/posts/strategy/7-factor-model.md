---
title: 7因子模型
slug: what-is-7-factor-model
date: 2024-03-26
categories:
    - strategy
motto: Hope is wishing something would happen. Faith is believing something will happen. Courage is making something happen.
lunar:
lineNumbers: true
img: https://images.jieyu.ai/images/2024/03/duke.jpg
tags: 
    - 因子
---

七因子模型一般是指David Hsieh和William Fung于2004年在一篇题为《Hedge Fund Benchmarks: A Risk Based Approach》中提出的7 factor model。

David Hsieh出生于香港，是Duke大学教授，在对冲基金和另类beta上有广泛研究。William Fung是伦敦商学院对冲基金教育研究中心访问学者，教授。

---

在[这篇论文](/assets/ebooks/Hedge-Fund-Benchmarks-A-Risk-Based-Approach.pdf)中，7因子模型指的是以下7个：

1. Bond Trend-Following Factor 债券趋势跟随因子
2. Currency Trend-Following Factor 货币趋势跟随因子
3. Commodity Trend-Following Factor 商品趋势跟踪因子
4. Equity Market Factor 股票市场因子
5. The Equity Size Spread Factor 股票规模利差因子
6. The Bond Market Factor 债券市场因子
7. The Bond Size Spread Factor 债券规模利差因子

这几个因子中，股票市场因子、规模利差因子本质上就是市场因子和规模因子。其中前三个因子来自Fung和Hsieh另一篇论文：《The Risk in Hedge Fund Strategies: Theory and Evidence from Trend Followers》。
几年后， Fung和Hsieh又增加了第8个因子，即MSCI新兴市场指数。

清华大学国家金融研究院在2017年3月的一个简报中，参考了Fung和Hsieh的7因子模型，提出了一个[中国私募基金8因子模型](/assets/ebooks/中国私募基金风险因子分析.pdf)，分别是：

1. 股票市场风险因子（MKT）
2. 规模因子（SMB）
3. 价值因子（HML)
4. 动量因子（MOM）
5. 债券因子（BOND10)
6. 信用风险因子（CBMB10)
7. 债券市场综合因子（BOND_RET）
8. 商品市场风险因子

---

不难看出，这个8因子模型是在经典的FF三因子（规模、市场、价值）基础上，增加了动量因子（Titman和Jegadesssh），再结合Fung和Hsieh的七因子中的一些因子构成的。

在这个模型中，股票市场风险因子定义为：

![](https://images.jieyu.ai/images/2024/03/mkt-factor.png)

$RET_HS300_t$为第$t$月的沪深300指数的月收益率， $RF_t$为第$t$月1年期定期存款利率的月利率。这点比较意外，一般来说，国债的风险比存款还要低（大额存款有50万的止付额），但收益要高一些，一般多会使用国债利率作为无风险收益率。

它的规模因子构建方法是，以一年为期进行一次换手。在每年6月底构建一次投资组合，将A股按流通市值将样本股票等分为小盘组和大盘组，再根据T-1期年报中的账面市值比和A股流通市值（ME）计算出账面市值比后，将股票按30%, 40%, 30%的比例划分为成长组、平衡组和价值组。最后，将两种分组方式所得的结果，按笛卡尔积的方式组成为六组，再计算各组的月收益率。

它的价值因子、动量因子构建方法与规模因子类似。

债券因子公式为：

![](https://images.jieyu.ai/images/2024/03/bond10.jpg)

---

信用风险因子为：

![](https://images.jieyu.ai/images/2024/03/cbmb10.jpg)

债券市场综合因子公式为：

![](https://images.jieyu.ai/images/2024/03/bond_ret.jpg)

数据使用的是中债综合全价指数。

这篇文章是为回答[读者问题](https://www.zhihu.com/question/649940963)写的，文中提到的论文都有PDF版本。

