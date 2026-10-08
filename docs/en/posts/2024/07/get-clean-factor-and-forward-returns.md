---
title: "Mastering Alphalens: 12 Parameters for Factor Analysis"
date: 2024-07-26
slug: en/posts/tools/get-clean-factor-and-forward-returns
tags: [Alphalens, Factor Analysis, Backtesting, Python]
excerpt: "The get_clean_factor_and_forward_returns function automates return calculation, layering, missing value handling, and standardization. This article demystifies its 12 parameters to help quants avoid common pitfalls in factor testing."
lang: en
translation_of: posts/tools/get-clean-factor-and-forward-returns
auto_translated: true
source_sha: f69030cd5322ef55f7971d6732adb0d97d40bf6f
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/girl-on-sofa.jpg"
---

In Alphalens, the `get_clean_factor_and_forward_returns` function automates return calculation, layering, missing value handling, and standardization, significantly simplifying the workflow of factor analysis.

However, this function has 12 parameters and 48 possible parameter combinations. Its complexity index far exceeds the "high-risk zone" threshold of 50 proposed by Dr. McCabe. Combined with a lack of deep understanding of factor analysis principles, beginners often make mistakes at this stage without realizing it.

These twelve parameters can be categorized into five groups. The `factor` and `price` parameters serve as data inputs, which have been covered previously, so they are not displayed here.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/get-clean-factor-and-forward-returns-group-params.jpg)

By controlling these parameters, Alphalens can assist us in completing return calculation, layering, missing value handling, and standardization.

The position of these functions within the overall factor analysis framework is shown below:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/gcfafr-in-factor-analysis.png)
<cap>Position and role of the function within the framework. Forward return calculation is not depicted.</cap>

<!-- draw group plot
<div class="text-2xl">

<v-drag pos="40,550,98,98">

<Ellipse/>
</v-drag>


<v-drag pos="180,400,120,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4 > Grouping</Box>
</v-drag>

<v-drag pos="180,510,120,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > Missing Values</Box>
</v-drag>

<v-drag pos="180,620,120,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > Return Calculation</Box>
</v-drag>

<v-drag pos="180,730,120,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > Layering</Box>
</v-drag>

<v-drag pos="620,280,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4 > zeroaware</Box>
</v-drag>

<v-drag pos="620,370,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4  > quantiles</Box>
</v-drag>

<v-drag pos="620,460,220,80">

<Box :hue1=0.4 :hue2=0.4 :hue3=0.4  > bins</Box>
</v-drag>

<v-drag pos="620,660,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > groupby</Box>
</v-drag>

<v-drag pos="620,750,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > groupby_labels</Box>
</v-drag>

<v-drag pos="620,840,220,80">

<Box :hue1=0.8 :hue2=0.8 :hue3=0.8 > binning_by_group</Box>
</v-drag>


<v-drag pos="350,370,230,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > max_loss</Box>
</v-drag>

<v-drag pos="350,480,230,80">

<Box :hue1=0.6 :hue2=0.6 :hue3=0.6 > filter_zscore</Box>
</v-drag>


<v-drag pos="350,640,230,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > periods</Box>
</v-drag>

<v-drag pos="350,750,230,80">

<Box :hue1=0.1 :hue2=0.1 :hue3=0.1 > cumulative_returns</Box>
</v-drag>
</div>

-->

The layering behavior is controlled by the `quantiles`, `bins`, and `zeroaware` parameters. `quantiles` and `bins` are mutually exclusive. When specifying `bins`, you must explicitly set `quantiles` to `None` for `bins` to take effect.

This article focuses on explaining these two parameters. Please see the video.

<iframe src="https://www.bilibili.com/video/BV1zJe9ebETH/?spm_id_from=333.999.0.0" class="w-800px h-400px"/>

<!--
`zeroaware` is used in scenarios where factors are centered around zero and generate long/short signals. In such cases, we should generally set `zeroaware` to `True` to prevent Alphalens from grouping factors that should belong to different signals into the same category.

During layering, we can also use grouping parameters to control whether layering is performed within groups or across the entire Universe.

Return calculation is primarily controlled by the `periods` and `cumulative_returns` parameters.

Handling missing values is the most intuitive part of these parameters. `max_loss` determines the maximum ratio of missing values that can be discarded while still allowing factor analysis to proceed. Its default value is 35%. `filter_zscore` specifies how many standard deviations away from the mean a factor value must be to be considered an outlier and discarded. Its default value is 20. This value may seem large, but this is because discrepancies between some financial data can often be significant. -->
