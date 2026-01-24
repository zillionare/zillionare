---
title: 白银大涨引发的量化套利策略
date: 2026-01-24
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/01/cover.jpg
excerpt: 全球避险情绪与工业需求双重驱动下，白银价格一路狂飙。这种单边行情不仅让持有实物或期货的投资者获利丰厚，更在场内催生了一个低风险的“捡钱”机会——LOF 基金场内外溢价套利。
img_copyright: samgoodgame@unsplash
category: factor-strategy
tags: [量化交易, 套利, LOF, 白银, Python]
addons:
  - slidev_themes/addons/slidev-addon-quantide-layout
  - slidev_themes/addons/slidev-addon-mouse-trail-pen
  - slidev_themes/addons/slidev-addon-array
  - slidev_themes/addons/slidev-addon-interactive-table
  - slidev_themes/addons/slidev-addon-card
aspectRatio: 3/4
layout: cover-random-img-portrait
---

最近白银的表现可谓惊艳，全球避险情绪与工业需求双重驱动下，白银价格一路狂飙。这种单边行情不仅让持有实物或期货的投资者获利丰厚，更在场内催生了一个低风险的“捡钱”机会——**LOF 基金场内外溢价套利**。

当场内投资者情绪高涨，疯狂买入白银相关基金时，场内价格往往会远高于基金份额的实际净值，形成高溢价。今天我们就来详细拆解 LOF 套利的原理、操作流程，以及如何通过量化手段监控全市场的套利机会。


## 什么是 LOF 套利？

**LOF (Listed Open-Ended Fund)**，即“上市开放式基金”。它最大的特点是：**既可以在场外（银行、券商 APP）申购赎回，也可以在场内（像股票一样）买卖。**

由于场内买卖受情绪驱动，而场外申购赎回基于基金净值，两者的“价格”并不总是相等的：



1.  **溢价（Premium）**：场内价格 > 场外净值。我们可以“场外申购，场内卖出”。
2.  **折价（Discount）**：场内价格 < 场外净值。我们可以“场内买入，场外赎回”。

### 白银 LOF 的典型案例
假设某白银 LOF 基金：
- **场外净值**：1.000 元
- **场内价格**：1.080 元（溢价 8%）
- **套利逻辑**：你在场外花 10000 元申购份额，待份额转到场内后，按 1.080 元卖出，扣除手续费后，净赚约 7% 的差价。


## 溢价套利的实操流程（T+2 模式）

套利的核心是**时间差**。目前 A 股 LOF 套利主流是 T+2 流程：

- **T 日**：在场内（或场外转场内）通过“申购”菜单申购基金份额。此时的价格是 T 日闭市后的基金净值。
- **T+1 日**：确认份额。
- **T+2 日**：份额到达场内持仓，当天即可按场内价格卖出。

这里的关键是： **场外转场内是如何完成的**？



转换有手动和自动两种方式，这里推荐一个**自动转换**的方式，即**通过证券账户购买**。

这种方式是，直接在**证券账户（券商 APP）**里操作：在交易软件中找到“场内基金”->“基金申购”菜单，点击『申购』买入 LOF 基金。此时你买到的场外基金。在买入时，你只能确认买入金额，但并不清楚买入的份额和价格。买入的份额和价格将在买入后的下一个交易日时得到确认。

在这种情况（通过证券账户买入）下，份额是**自动**到达场内持仓的。你不需要做任何额外操作。然后在 T+2 日早上，你打开账户就会发现持仓里多了这笔基金，直接点击“卖出”即可。

!!! tip
    在证券账户中操作时，这里千万不要误操作为场内买入！区分场内买入与场外买入的关键在于，你点击的按钮是『交易』还是『申购』。只要按钮名称是『申购』，你购买的就一定是场外基金。



## 这种『羊毛』真的没有风险吗

LOF 套利看起来很安全，但天下没有免费的午餐，LOF 套利尽管比较稳，但也是有风险（缺点）的：

1.  时间差敞口（T+2）：这是最大的风险。你 T 日场外申购，T+2 日才能在场内卖。如果这两天标的跌了 6%，即便有 5% 的溢价，你最后还是亏 1%。
2.  限额：很多基金公司为了保护原持有人，会限制申购金额（比如白银 LOF 近期单日限额 100 元）。可以认为，越是稳的机会，获得额度往往就越小。
3.  流动性枯竭：有些迷你基金场内每天成交额只有几十万。所以，即使有高溢价，但场内不容易卖出，或者必须降价才能卖出，这样，你的套利机会就变小了。


## 量化推广：如何监控全市场的套利机会？

最近的白银 LOF 套利确实很稳，很多人也在讨论和参与，但美中不足就是，基金申购限额，每天只能买入100元。我们不禁思考，是否还有其它 LOF 也存在类似的机会呢?

这就是量化交易的用武之地了。通过 Python 量化脚本，我们可以全自动地监控和发现所有 LOF 套利机会。



核心要点是：

1.  **通过 Akshare， 免费获取所有 LOF 基金代码**
2.  **通过 Akshare， 获取所有 LOF 基金净值和场内实时交易价格**
3.  **在收盘前，计算出 LOF 的溢价率，对高于5%的基金，发出邮件通知**

我们把核心代码展示如下：

```python 
# 这里是获取所有 LOF 的实时行情，如最新价、折价率等
df_spot = ak.fund_lof_spot_em()

# 2. 获取所有开放式基金的当日/昨日净值 (作为计算溢价率的基准)
df_nav = ak.fund_open_fund_daily_em()

# 黑科技：akshare 会返回多日的净值，每一日的净值对应列名为'YYYY-MM-DD-单位净值'
# 所以我们要按 pattern 获取列名并排序，这样才能得到最新的净值
nav_cols = [c for c in df_nav.columns if "单位净值" in c and "-" in c]
if nav_cols:
    # 排序取最新的日期
    latest_nav_col = sorted(nav_cols, reverse=True)[0]
    nav_map = dict(zip(df_nav["基金代码"], df_nav[latest_nav_col]))
    # 获取申购和赎回状态映射
    status_map = dict(zip(df_nav["基金代码"], df_nav["申购状态"]))
    redemption_map = dict(zip(df_nav["基金代码"], df_nav["赎回状态"]))
    logger.info(f"Using NAV column: {latest_nav_col}")
```



除此之外，我们还需要过滤掉暂停申赎的基金，以及定时启动（在14：50左右），扫描市场并发出邮件通知。

如果你不想自己写程序，我们也把完整的脚本准备好啦！每天14：50，它就会自动扫描市场，如果发现套利机会，就会发邮件通知你。

!!! warning
    投资有风险，入市须谨慎。本文所述的策略仅供学习量化交易技术，不构成对任何品种的推荐！
    
    我们不对任何品种未来运行趋势表示意见。



<!-- BEGIN IPYNB STRIPOUT -->
完整的代码可以加入匡醍会员获取。
<!-- END IPYNB STRIPOUT -->

<!--PAID CONTENT START-->
```python
#!/usr/bin/env python3
"""
如果要发邮件通知，请设置以下变量：
SMTP_SERVER
SMTP_PORT
SMTP_USER
SMTP_PASS

脚本运行方式：
1. 一次性运行： python lof_arbitrage.py --run-once
2. 定时运行：  nohup python lof_arbitrage.py &

在第二种方式下，脚本将在 RUN_AT 指定的时间运行。默认为14：50分。这样会留下10分钟左右的操作时间。
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
    """发送邮件通知"""
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
    """简单的重试装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Error: {e}, 重试中 (剩余次数: {_tries-1})...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return f(*args, **kwargs)
        return wrapper
    return decorator

@retry(Exception, tries=3, delay=30)
def get_lof_data_akshare():
    """使用 akshare 获取 LOF 数据"""
    try:
        import akshare as ak
        logger.info("Fetching LOF data via akshare...")
        
        # 1. 获取 LOF 实时行情 (包含代码、名称、最新价、折价率)
        df_spot = ak.fund_lof_spot_em()
        logger.info(f"Fetched {len(df_spot)} LOF spot data.")
        
        # 2. 获取所有开放式基金的当日/昨日净值 (作为计算溢价率的基准)
        try:
            df_nav = ak.fund_open_fund_daily_em()
            # 找到最新的单位净值列，格式通常为 'YYYY-MM-DD-单位净值'
            nav_cols = [c for c in df_nav.columns if "单位净值" in c and "-" in c]
            if nav_cols:
                # 排序取最新的日期
                latest_nav_col = sorted(nav_cols, reverse=True)[0]
                nav_map = dict(zip(df_nav["基金代码"], df_nav[latest_nav_col]))
                # 获取申购和赎回状态映射
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
                
                # 优先使用实时折价率字段
                discount_rate_raw = row.get("折价率", None)
                
                # 获取状态
                sub_status = status_map.get(code, "")
                red_status = redemption_map.get(code, "")
                
                # 尝试获取净值
                nav = nav_map.get(code)
                if nav is not None:
                    nav = float(nav)
                
                rate = None
                if discount_rate_raw is not None and not pd.isna(discount_rate_raw):
                    rate = float(discount_rate_raw) / 100.0
                elif nav and nav > 0:
                    rate = (price - nav) / nav
                
                # 核心过滤逻辑：
                # 1. 达到阈值
                if rate is not None and abs(rate) >= THRESHOLD:
                    # 2. 定向过滤状态
                    if rate > 0: # 溢价套利，需要能申购
                        if sub_status not in ["开放申购", "限制大额申购"]:
                            continue
                    else: # 折价套利，需要能赎回
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
    """执行 LOF 溢折价检查"""
    logger.info("Starting LOF arbitrage check...")
    
    # 使用 akshare 获取数据
    results = get_lof_data_akshare()
    
    if results:
        # 格式化通知内容
        content = "发现以下 LOF 基金溢折价率超过 5%：\n\n"
        content += f"{'代码':<10} {'名称':<20} {'最新价':<10} {'单位净值':<10} {'溢折价率':<10}\n"
        content += "-" * 70 + "\n"
        
        for item in results:
            rate_pct = f"{item['rate']*100:.2f}%"
            nav_str = f"{item['nav']:.4f}" if item['nav'] else "未知"
            content += f"{item['code']:<10} {item['name']:<20} {item['price']:<10.3f} {nav_str:<10} {rate_pct:<10}\n"
        
        subject = f"LOF 溢折价预警 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(content)
        if SMTP_SERVER != "":
            send_email(subject, content)
    else:
        logger.info("No LOF arbitrage opportunities found or data fetch failed.")

def main():
    """程序入口"""
    import argparse
    parser = argparse.ArgumentParser(description="LOF Arbitrage Monitor")
    parser.add_argument("--run-once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    if args.run_once:
        check_lof_arbitrage()
        return

    logger.info("Starting LOF Monitor Scheduler...")
    # 每天 14:50运行，通过 RUN_AT 变量指定
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
脚本有两种运行方式，一是一次性的，可用以调试，命令是：

```python
python lof_arbitrage.py --run-once
```

这会立即运行并输出结果 。

另一种方式是后台运行，定时启动：

```python
python lof_arbitrage.py
```

在这种方式下，请修改脚本开头处的 SMTP_SERVER 等变量，以便收到邮件通知。另外，运行时间也可以通过修改 RUN_AT 变量来指定。默认是14:50。
<!-- END IPYNB STRIPOUT -->




