#!/usr/bin/env python3
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
        # send_email(subject, content)
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
    # 每天 14:45 运行
    schedule.every().day.at("14:45").do(check_lof_arbitrage)
    
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
