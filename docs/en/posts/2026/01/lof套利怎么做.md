---
title: "LOF Arbitrage: Pricing, Engineering, and Code"
date: 2026-01-24
slug: en/posts/factor-strategy/lof套利怎么做
tags: [Loft Arbitrage, Quantitative Trading, Python, Akshare]
excerpt: "This guide details LOF fund arbitrage mechanics, the T+2 execution workflow, and risk factors like liquidity and limits. It includes a Python script using Akshare to monitor cross-market premiums and automate alerts."
lang: en
translation_of: posts/factor-strategy/lof套利怎么做
auto_translated: true
source_sha: 2f7346da1edb5765f99dc69db32ba643bacc8165
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/cover.jpg"
---

Silver’s recent performance has been stunning. Driven by dual forces of global risk aversion and industrial demand, silver prices have skyrocketed. This one-way trend not only generated substantial profits for holders of physical silver or futures but also created a low-risk “money-grabbing” opportunity in the secondary market: **LOF (Listed Open-Ended Fund) cross-market premium arbitrage**.

When retail investor sentiment in the secondary market runs high and they frantically buy silver-related funds, the secondary market price often far exceeds the fund’s actual net asset value (NAV), creating a high premium. Today, we will dissect the principles and operational workflows of LOF arbitrage, and demonstrate how to use quantitative methods to monitor arbitrage opportunities across the entire market.

## What Is LOF Arbitrage?

**LOF (Listed Open-Ended Fund)**, or “Listed Open-Ended Fund,” has a unique feature: **it can be subscribed to and redeemed in the over-the-counter (OTC) market (via banks or broker apps) and traded in the secondary market (like stocks).**

Because secondary market trading is driven by sentiment while OTC subscriptions/redemptions are based on fund NAV, their “prices” are not always equal:

1.  **Premium**: Secondary market price > OTC NAV. Strategy: “Subscribe OTC, sell in secondary market.”
2.  **Discount**: Secondary market price < OTC NAV. Strategy: “Buy in secondary market, redeem OTC.”

### A Typical Silver LOF Case Study
Assume a specific Silver LOF fund:
- **OTC NAV**: 1.000 CNY
- **Secondary Market Price**: 1.080 CNY (8% premium)
- **Arbitrage Logic**: You subscribe for 10,000 CNY worth of shares in the OTC market. After the shares are transferred to the secondary market, you sell them at 1.080 CNY. After deducting fees, you net approximately a 7% spread.

## Practical Workflow for Premium Arbitrage (T+2 Model)

The core of arbitrage lies in the **time lag**. The mainstream A-share LOF arbitrage process currently follows a T+2 timeline:

- **T Day**: Subscribe to fund shares via the “Subscription” menu in the secondary market (or via OTC-to-secondary transfer). The price used is the fund’s NAV after market close on T Day.
- **T+1 Day**: Share confirmation.
- **T+2 Day**: Shares arrive in your secondary market holdings. You can sell them at the secondary market price on this day.

The key question here is: **How is the OTC-to-secondary transfer completed?**

There are manual and automatic methods. We recommend an **automatic transfer** method: **purchasing through a securities account**.

This involves operating directly in your **securities account (broker app)**: In the trading software, navigate to “Secondary Market Funds” -> “Fund Subscription” menu, and click ‘Subscribe’ to buy the LOF. At this point, you are buying an OTC fund. You confirm the purchase amount, but the exact number of shares and price are not immediately known. These will be confirmed on the next trading day after purchase.

In this scenario (buying via a securities account), the shares are **automatically** transferred to your secondary market holdings. No additional manual steps are required. On the morning of T+2, you will see the new fund position in your account and can simply click “Sell.”

!!! tip
    When operating in a securities account, do not accidentally execute a secondary market *purchase*. The key distinction between a secondary market purchase and an OTC subscription is the button you click: ‘Trade’ vs. ‘Subscribe’. As long as the button says ‘Subscribe’, you are buying an OTC fund.

## Is There Really No Risk in This ‘Arbitrage’?

LOF arbitrage looks safe, but there is no free lunch. Although relatively stable, LOF arbitrage carries risks (drawbacks):

1.  **Time-Lag Exposure (T+2)**: This is the biggest risk. You subscribe OTC on T Day and can only sell in the secondary market on T+2. If the underlying asset drops 6% over those two days, even with a 5% premium, you will ultimately lose 1%.
2.  **Subscription Limits**: Many fund companies limit subscription amounts (e.g., the Silver LOF recently had a daily limit of 100 CNY) to protect existing holders. Generally, the safer the opportunity, the smaller the allocation you receive.
3.  **Liquidity Crunch**: Some small-cap funds have daily secondary market turnover of only hundreds of thousands of yuan. Thus, even with high premiums, it may be difficult to sell in the secondary market, or you may have to lower the price to sell, reducing your arbitrage margin.

## Quantitative Scaling: Monitoring Arbitrage Opportunities Across the Market

The recent Silver LOF arbitrage has been very stable, and many are discussing and participating. However, the drawback is the subscription limit of 100 CNY per day. This raises the question: Are there other LOFs with similar opportunities?

This is where quantitative trading comes in. Using Python quantitative scripts, we can automatically monitor and discover all LOF arbitrage opportunities.

The core steps are:

1.  **Use Akshare to free-of-charge fetch all LOF fund codes.**
2.  **Use Akshare to fetch the NAV and real-time secondary market trading prices for all LOFs.**
3.  **Calculate the LOF premium rate before market close and send email alerts for funds with premiums above 5%.**

We present the core code below:

````md
```python 
# Fetch real-time quotes for all LOFs, such as latest price and discount rate
df_spot = ak.fund_lof_spot_em()

# 2. Fetch daily/yesterday NAV for all open-end funds (used as the benchmark for premium calculation)
df_nav = ak.fund_open_fund_daily_em()

# Black magic: akshare returns NAV for multiple days, with column names formatted as 'YYYY-MM-DD-NAV'
# Therefore, we must extract column names by pattern and sort them to obtain the latest NAV
nav_cols = [c for c in df_nav.columns if "单位净值" in c and "-" in c]
if nav_cols:
    # Sort to get the latest date
    latest_nav_col = sorted(nav_cols, reverse=True)[0]
    nav_map = dict(zip(df_nav["基金代码"], df_nav[latest_nav_col]))
    # Fetch subscription and redemption status mappings
    status_map = dict(zip(df_nav["基金代码"], df_nav["申购状态"]))
    redemption_map = dict(zip(df_nav["基金代码"], df_nav["赎回状态"]))
    logger.info(f"Using NAV column: {latest_nav_col}")
```
````

Additionally, we need to filter out funds with suspended subscriptions/redemptions and schedule the script to run (around 14:50) to scan the market and send email alerts.

If you don’t want to write the program yourself, we have prepared the complete script! It automatically scans the market at 14:50 daily and emails you if arbitrage opportunities are found.

!!! warning
    Investment involves risk; enter the market with caution. The strategy described in this article is for learning quantitative trading techniques only and does not constitute a recommendation for any specific asset.
    
    We do not express opinions on the future trends of any assets.

<!-- BEGIN IPYNB STRIPOUT -->
The complete code is available to Kuangti members.
<!-- END IPYNB STRIPOUT -->

<!--PAID CONTENT START-->
The following code should be copied and run locally. Please install the `schedule` library before running:

```bash
pip install schedule
```

```python
#!/usr/bin/env python3
"""
To enable email notifications, set the following variables:
SMTP_SERVER
SMTP_PORT
SMTP_USER
SMTP_PASS

Script Execution Methods:
1. One-time run: python lof_arbitrage.py --run-once
2. Scheduled run: nohup python lof_arbitrage.py &

In the second method, the script runs at the time specified by RUN_AT. The default is 14:50, leaving about 10 minutes for execution.
"""
import logging
import os
import smtplib
import sys
import time
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from functools import wraps
from pathlib import Path

import pandas as pd
import schedule

# Configuration - Prefer environment variables
SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER", "") 
SMTP_PASS = os.environ.get("SMTP_PASS", "")  # e.g., "your_auth_token"
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", SMTP_USER)
THRESHOLD = 0.05  # 5%
RUN_AT = "14:50"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("lof_arbitrage.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

def send_email(subject, content):
    """Send email notification"""
    if not SMTP_USER or not SMTP_PASS:
        logger.warning("SMTP_USER or SMTP_PASS not set, skipping email notification.")
        logger.info(f"Notification Content:\n{content}")
        return

    try:
        message = MIMEText(content, "plain", "utf-8")
        message["From"] = SMTP_USER
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = Header(subject, "utf-8")

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [RECEIVER_EMAIL], message.as_string())
        logger.info("Email notification sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def retry(exceptions, tries=3, delay=2, backoff=2):
    """Simple retry decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Error: {e}, Retrying (remaining attempts: {_tries-1})...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return f(*args, **kwargs)
        return wrapper
    return decorator

@retry(Exception, tries=3, delay=30)
def get_lof_data_akshare():
    """Fetch LOF data using akshare"""
    try:
        import akshare as ak
        logger.info("Fetching LOF data via akshare...")
        
        # 1. Fetch LOF real-time quotes (including code, name, latest price, discount rate)
        df_spot = ak.fund_lof_spot_em()
        logger.info(f"Fetched {len(df_spot)} LOF spot data.")
        
        # 2. Fetch daily/yesterday NAV for all open-end funds (used as the benchmark for premium calculation)
        try:
            df_nav = ak.fund_open_fund_daily_em()
            # Find the latest NAV column, typically formatted as 'YYYY-MM-DD-NAV'
            nav_cols = [c for c in df_nav.columns if "单位净值" in c and "-" in c]
            if nav_cols:
                # Sort to get the latest date
                latest_nav_col = sorted(nav_cols, reverse=True)[0]
                nav_map = dict(zip(df_nav["基金代码"], df_nav[latest_nav_col]))
                # Fetch subscription and redemption status mappings
                status_map = dict(zip(df_nav["基金代码"], df_nav["申购状态"]))
                redemption_map = dict(zip(df_nav["基金代码"], df_nav["赎回状态"]))
                logger.info(f"Using NAV column: {latest_nav_col}")
        except Exception as nav_e:
            logger.warning(f"Failed to fetch NAV list from fund_open_fund_daily_em: {nav_e}")
            nav_map = {}
            status_map = {}
            redemption_map = {}
        
        results = []
        for _, row in df_spot.iterrows():
            try:
                code = row["代码"]
                name = row["名称"]
                price = float(row["最新价"])
                
                # Prioritize using the real-time discount rate field
                discount_rate_raw = row.get("折价率", None)
                
                # Fetch status
                sub_status = status_map.get(code, "")
                red_status = redemption_map.get(code, "")
                
                # Attempt to fetch NAV
                nav = nav_map.get(code)
                if nav is not None:
                    nav = float(nav)
                
                rate = None
                if discount_rate_raw is not None and not pd.isna(discount_rate_raw):
                    rate = float(discount_rate_raw) / 100.0
                elif nav and nav > 0:
                    rate = (price - nav) / nav
                
                # Core filtering logic:
                # 1. Meet threshold
                if rate is not None and abs(rate) >= THRESHOLD:
                    # 2. Directional filtering based on status
                    if rate > 0: # Premium arbitrage requires ability to subscribe
                        if sub_status not in ["开放申购", "限制大额申购"]:
                            continue
                    else: # Discount arbitrage requires ability to redeem
                        if red_status not in ["开放赎回"]:
                            continue
                            
                    results.append({
                        "code": code,
                        "name": name,
                        "price": price,
                        "rate": rate,
                        "nav": nav
                    })
            except (ValueError, TypeError):
                continue
                
        return results
    except ImportError:
        logger.warning("akshare not installed.")
        return None
    except Exception as e:
        logger.error(f"akshare fetch error: {e}")
        return None

def check_lof_arbitrage():
    """Execute LOF premium/discount check"""
    logger.info("Starting LOF arbitrage check...")
    
    # Fetch data using akshare
    results = get_lof_data_akshare()
    
    if results:
        # Format notification content
        content = "The following LOF funds have premium/discount rates exceeding 5%:\n\n"
        content += f"{'Code':<10} {'Name':<20} {'Price':<10} {'NAV':<10} {'Rate':<10}\n"
        content += "-" * 70 + "\n"
        
        for item in results:
            rate_pct = f"{item['rate']*100:.2f}%"
            nav_str = f"{item['nav']:.4f}" if item['nav'] else "Unknown"
            content += f"{item['code']:<10} {item['name']:<20} {item['price']:<10.3f} {nav_str:<10} {rate_pct:<10}\n"
        
        subject = f"LOF Premium/Discount Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(content)
        if SMTP_SERVER != "":
            send_email(subject, content)
    else:
        logger.info("No LOF arbitrage opportunities found or data fetch failed.")

def main():
    """Program entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="LOF Arbitrage Monitor")
    parser.add_argument("--run-once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    if args.run_once:
        check_lof_arbitrage()
        return

    logger.info("Starting LOF Monitor Scheduler...")
    # Run daily at 14:50, specified by RUN_AT variable
    schedule.every().day.at(RUN_AT).do(check_lof_arbitrage)
    
    logger.info("Monitor configured for 14:45 daily.")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user.")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
```
<!--PAID CONTENT END-->

<!-- BEGIN IPYNB STRIPOUT -->
The script has two execution modes: one-time runs for debugging, and scheduled background runs.

For one-time execution, use the command:

```python
python lof_arbitrage.py --run-once
```

This will run immediately and output the results.

For background scheduled execution:

```python
python lof_arbitrage.py
```

In this mode, please modify the `SMTP_SERVER` and other variables at the beginning of the script to receive email notifications. The execution time can also be specified by modifying the `RUN_AT` variable. The default is 14:50.
<!-- END IPYNB STRIPOUT -->
