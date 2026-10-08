---
title: "PEPE’s Warning: How High Can the Market Go?"
date: 2025-08-26
slug: en/posts/factor-strategy/is-the-Ashare-market-overvalued
tags: []
excerpt: "SSE Index PE hits 98.8th percentile, a 7-year high. We analyze if earnings growth can bring valuation back to safe levels or if the market is in uncharted territory. ===TAGs=== Valuation, PE Ratio, China A-Shares, Market Analysis ===BODY=== The market has surged with festive energy, but for the developers at East Money, it might mean overtime. The rally has been so strong that their programs overflowed:  <!-- more --->  <div style='width:66%;text-align:center;margin: 0 auto 1rem'> <img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250825205342.png'> <span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span> </div>  What is going on?  ## Reviewing the Past  In September 2024, we published [“A Heart-Stopping Scene Before the Holiday! Who Can Tell Me if China A-Shares Are Undervalued?”](https://blog.quantide.cn/blog/posts/factor-strategy/Is-the-A-share-market-undervalued). In that article, we used `akshare` to retrieve the Shanghai Composite Index’s price-to-earnings (PE) ratio and analyzed the valuation of the China A-share market through quantile and trend analysis.  Our conclusion at the time was:  > From a purely quantile statistical perspective, China A-shares appear undervalued. However, considering the PE ratio’s general upward trend and the divergence between PE and index performance over the past year, it remains questionable to label the market as undervalued. More dimensions should be included in the assessment.  It is now August 2025, nearly a year later. Judging by trading volume, the market seems to have entered a frenzied phase. Can the techniques we used last year still predict future trends?  Let the data speak.  ## Fetching Index PE via Tushare  Tushare gave us a break last week, but fortunately, it has since resumed operations. To obtain index PE data, we need to use the `index_dailybasic` function.  <!--PAID CONTENT START-->  ```python import pandas as pd import matplotlib.pyplot as plt import matplotlib.dates as mdates from datetime import datetime  pro = pro_api() ``` <!--PAID CONTENT END-->  ```python def get_index_pe_close(ts_code='000001.SH', start_date='20100101', end_date='20250825'):     # Fetch index PE data     df_pe = pro.index_dailybasic(ts_code=ts_code,                                  start_date=start_date,                                  end_date=end_date,                                  fields='trade_date,pe_ttm')     df_pe.rename(columns={'trade_date': 'date', 'pe_ttm': 'pe'}, inplace=True)     df_pe['date'] = pd.to_datetime(df_pe['date'])     df_pe.set_index('date', inplace=True)          # Fetch index closing price data     df_price = pro.index_daily(ts_code=ts_code,                               start_date=start_date,                               end_date=end_date,                               fields='trade_date,close')     df_price.rename(columns={'trade_date': 'date'}, inplace=True)     df_price['date'] = pd.to_datetime(df_price['date'])     df_price.set_index('date', inplace=True)          # Merge data     df = df_pe.merge(df_price, left_index=True, right_index=True, how='inner')          # Sort     df.sort_index(inplace=True)          # Remove records with empty PE     df = df.dropna(subset=['pe'])          return df ```  After obtaining the PE data, let’s first look at the intuitive trend:  ```python # Plot PE trend fig, ax = plt.subplots(figsize=(12,6))  color = \"tab:red\" ax.plot(df.index, df[\"pe\"], label=\"PE\", color=color) ax.set_xlabel(\"Year\") ax.set_ylabel(\"PE\", color=color) ax.xaxis.set_major_locator(mdates.YearLocator()) ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  df = get_index_pe_close(start_date=\"20100101\")  # Add quantile lines for i in range(1, 4):     quantile = df[\"pe\"].quantile(i/4)     ax.axhline(quantile, color='gray', linestyle='--', label=f\"{i/4:02.0%}\")  plt.title(\"SSE Index PE Ratio (via Tushare)\") plt.legend(loc=\"upper left\") plt.grid(True) plt.show() ```  <!-- BEGIN IPYNB STRIPOUT --> <div style='width:66%;text-align:center;margin: 0 auto 1rem'> <img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250825204156.png'> <span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span> </div> <!-- END IPYNB STRIPOUT -->  The data indicates that if we ignore the manic history of 2015 (driven by off-exchange margin leverage), the current PE level is quite high.  Just how high?  ```python def show_pe_quantile(df):     # Calculate current PE quantile     current_pe = df['pe'].iloc[-1]     rank = df['pe'].rank().iloc[-1]     percentile = rank / len(df)     print(f\"Current PE Quantile: {percentile:.2%}\")  show_pe_quantile(df)  df = df[df.index > '2016-01-01'] show_pe_quantile(df) ```  If calculated from 2013 (as Tushare does not seem to have earlier data), the current PE quantile is **95.18%**. If calculated from January 2016, the current PE quantile has reached **98.81%**, nearing perfection. For an index, this is indeed quite high.  How many days has the current PE value been the maximum? This can be easily calculated using pandas:  ```python def find_days_since_max_pe(df):     \"\"\"Calculate how many days ago the current PE was the maximum value\"\"\"     if df.empty or len(df) < 2:         return None          # Get current PE value     current_pe = df['pe'].iloc[-1]          # Find the position of the maximum PE value in historical data     max_pe_idx = df['pe'].idxmax()          # Calculate days since the maximum PE date     current_date = df.index[-1]     days_since_max = (current_date - max_pe_idx).days          return days_since_max, max_pe_idx  find_days_since_max_pe(df) ```  The answer is that the current PE value is the maximum since January 24, 2018, marking a new 7-year high.  Assuming the index stabilizes, the only way to bring the PE back to a safe zone is through corporate earnings growth. If the index stays at this level, how much must corporate profits increase to return the PE to a safe zone?  We calculate this using the following method:  ```python def required_earnings_growth(df, target_percentile=0.75, target_index=None):     \"\"\"Calculate the percentage of earnings growth required to reduce PE quantile to target\"\"\"     if df.empty:         return None          # Get current PE and current index level     current_pe = df['pe'].iloc[-1]     current_index = df['close'].iloc[-1]          # If a target index level is specified, calculate the target PE at that level;      # otherwise, use the PE corresponding to the target quantile in the dataframe     if target_index is not None:         # Based on PE = Price / Earnings, calculate PE at the target index level         # Assuming earnings remain unchanged, target PE = target_index / (current_index / current_pe)         # i.e., target_pe = target_index * current_pe / current_index         current_pe = target_index * current_pe / current_index       # Calculate target PE (PE corresponding to target quantile)     target_pe = df['pe'].quantile(target_percentile)          # If current PE is already below target PE, no earnings growth is needed     if current_pe <= target_pe:         return 0.0          # Calculate required earnings growth percentage     # PE = Price / Earnings => Earnings = Price / PE     # To reduce PE from current_pe to target_pe:     # (Price / target_pe) / (Price / current_pe) - 1 = current_pe / target_pe - 1     required_growth = (current_pe / target_pe) - 1          return required_growth  required_earnings_growth(df) ```  The calculation shows that on the current index, to bring the PE back below the 75th percentile, corporate profits need to increase by 10.2%. To bring the PE back below the 84.13th percentile (one standard deviation), corporate earnings need to grow by 5.5%. Based on the annual profit growth rate of enterprises, we can roughly estimate how many years this would take. Of course, this assumes that the annual profit growth rate of enterprises is positive.  If we hope the index rises to 4,000 points and the PE returns to within one standard deviation, corporate profits must grow by more than 8.68%.  That is the situation. In short, we have entered the “no-man’s land,” where no historical data can be utilized.  The code for this article can be run and downloaded on the Kuangti Research Platform."
lang: en
translation_of: posts/factor-strategy/is-the-Ashare-market-overvalued
auto_translated: true
source_sha: 36abb22a414a83e9af413f568b188e0873ec1e1c
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/title.jpg"
---

The market has surged with festive energy, but for the developers at East Money, it might mean overtime. The rally has been so strong that their programs overflowed:

<!-- more --->

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250825205342.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

What is going on?

## Reviewing the Past

In September 2024, we published [“A Heart-Stopping Scene Before the Holiday! Who Can Tell Me if China A-Shares Are Undervalued?”](https://blog.quantide.cn/blog/posts/factor-strategy/Is-the-A-share-market-undervalued). In that article, we used `akshare` to retrieve the Shanghai Composite Index’s price-to-earnings (PE) ratio and analyzed the valuation of the China A-share market through quantile and trend analysis.

Our conclusion at the time was:

> From a purely quantile statistical perspective, China A-shares appear undervalued. However, considering the PE ratio’s general upward trend and the divergence between PE and index performance over the past year, it remains questionable to label the market as undervalued. More dimensions should be included in the assessment.

It is now August 2025, nearly a year later. Judging by trading volume, the market seems to have entered a frenzied phase. Can the techniques we used last year still predict future trends?

Let the data speak.

## Fetching Index PE via Tushare

Tushare gave us a break last week, but fortunately, it has since resumed operations. To obtain index PE data, we need to use the `index_dailybasic` function.

<!--PAID CONTENT START-->

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

pro = pro_api()
```
<!--PAID CONTENT END-->

```python
def get_index_pe_close(ts_code='000001.SH', start_date='20100101', end_date='20250825'):
    # Fetch index PE data
    df_pe = pro.index_dailybasic(ts_code=ts_code, 
                                start_date=start_date, 
                                end_date=end_date, 
                                fields='trade_date,pe_ttm')
    df_pe.rename(columns={'trade_date': 'date', 'pe_ttm': 'pe'}, inplace=True)
    df_pe['date'] = pd.to_datetime(df_pe['date'])
    df_pe.set_index('date', inplace=True)
    
    # Fetch index closing price data
    df_price = pro.index_daily(ts_code=ts_code,
                              start_date=start_date,
                              end_date=end_date,
                              fields='trade_date,close')
    df_price.rename(columns={'trade_date': 'date'}, inplace=True)
    df_price['date'] = pd.to_datetime(df_price['date'])
    df_price.set_index('date', inplace=True)
    
    # Merge data
    df = df_pe.merge(df_price, left_index=True, right_index=True, how='inner')
    
    # Sort
    df.sort_index(inplace=True)
    
    # Remove records with empty PE
    df = df.dropna(subset=['pe'])
    
    return df
```

After obtaining the PE data, let’s first look at the intuitive trend:

```python
# Plot PE trend
fig, ax = plt.subplots(figsize=(12,6))

color = "tab:red"
ax.plot(df.index, df["pe"], label="PE", color=color)
ax.set_xlabel("Year")
ax.set_ylabel("PE", color=color)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

df = get_index_pe_close(start_date="20100101")

# Add quantile lines
for i in range(1, 4):
    quantile = df["pe"].quantile(i/4)
    ax.axhline(quantile, color='gray', linestyle='--', label=f"{i/4:02.0%}")

plt.title("SSE Index PE Ratio (via Tushare)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
```

<!-- BEGIN IPYNB STRIPOUT -->
<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2025/08/20250825204156.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>
<!-- END IPYNB STRIPOUT -->

The data indicates that if we ignore the manic history of 2015 (driven by off-exchange margin leverage), the current PE level is quite high.

Just how high?

```python
def show_pe_quantile(df):
    # Calculate current PE quantile
    current_pe = df['pe'].iloc[-1]
    rank = df['pe'].rank().iloc[-1]
    percentile = rank / len(df)
    print(f"Current PE Quantile: {percentile:.2%}")

show_pe_quantile(df)

df = df[df.index > '2016-01-01']
show_pe_quantile(df)
```

If calculated from 2013 (as Tushare does not seem to have earlier data), the current PE quantile is **95.18%**. If calculated from January 2016, the current PE quantile has reached **98.81%**, nearing perfection. For an index, this is indeed quite high.

How many days has the current PE value been the maximum? This can be easily calculated using pandas:

```python
def find_days_since_max_pe(df):
    """Calculate how many days ago the current PE was the maximum value"""
    if df.empty or len(df) < 2:
        return None
    
    # Get current PE value
    current_pe = df['pe'].iloc[-1]
    
    # Find the position of the maximum PE value in historical data
    max_pe_idx = df['pe'].idxmax()
    
    # Calculate days since the maximum PE date
    current_date = df.index[-1]
    days_since_max = (current_date - max_pe_idx).days
    
    return days_since_max, max_pe_idx

find_days_since_max_pe(df)
```

The answer is that the current PE value is the maximum since January 24, 2018, marking a new 7-year high.

Assuming the index stabilizes, the only way to bring the PE back to a safe zone is through corporate earnings growth. If the index stays at this level, how much must corporate profits increase to return the PE to a safe zone?

We calculate this using the following method:

```python
def required_earnings_growth(df, target_percentile=0.75, target_index=None):
    """Calculate the percentage of earnings growth required to reduce PE quantile to target"""
    if df.empty:
        return None
    
    # Get current PE and current index level
    current_pe = df['pe'].iloc[-1]
    current_index = df['close'].iloc[-1]
    
    # If a target index level is specified, calculate the target PE at that level; 
    # otherwise, use the PE corresponding to the target quantile in the dataframe
    if target_index is not None:
        # Based on PE = Price / Earnings, calculate PE at the target index level
        # Assuming earnings remain unchanged, target PE = target_index / (current_index / current_pe)
        # i.e., target_pe = target_index * current_pe / current_index
        current_pe = target_index * current_pe / current_index


    # Calculate target PE (PE corresponding to target quantile)
    target_pe = df['pe'].quantile(target_percentile)
    
    # If current PE is already below target PE, no earnings growth is needed
    if current_pe <= target_pe:
        return 0.0
    
    # Calculate required earnings growth percentage
    # PE = Price / Earnings => Earnings = Price / PE
    # To reduce PE from current_pe to target_pe:
    # (Price / target_pe) / (Price / current_pe) - 1 = current_pe / target_pe - 1
    required_growth = (current_pe / target_pe) - 1
    
    return required_growth

required_earnings_growth(df)
```

The calculation shows that on the current index, to bring the PE back below the 75th percentile, corporate profits need to increase by 10.2%. To bring the PE back below the 84.13th percentile (one standard deviation), corporate earnings need to grow by 5.5%. Based on the annual profit growth rate of enterprises, we can roughly estimate how many years this would take. Of course, this assumes that the annual profit growth rate of enterprises is positive.

If we hope the index rises to 4,000 points and the PE returns to within one standard deviation, corporate profits must grow by more than 8.68%.

That is the situation. In short, we have entered the “no-man’s land,” where no historical data can be utilized.

The code for this article can be run and downloaded on the Kuangti Research Platform.
