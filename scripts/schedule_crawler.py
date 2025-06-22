#!/usr/bin/env python3
"""
定时新闻抓取脚本
使用schedule库实现定时任务
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.news_crawler import NewsCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsScheduler:
    """新闻抓取调度器"""
    
    def __init__(self, config_path: str = "rss.yaml"):
        self.config_path = config_path
        self.crawler = None
        
    def run_crawler(self):
        """运行爬虫任务"""
        try:
            logger.info(f"Starting scheduled news crawling at {datetime.now()}")
            
            # 创建新的爬虫实例
            self.crawler = NewsCrawler(self.config_path)
            self.crawler.run()
            
            logger.info(f"Completed scheduled news crawling at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"Error in scheduled crawling: {e}")
    
    def start_scheduler(self):
        """启动调度器"""
        logger.info("Starting news crawler scheduler...")
        
        # 每天早上8点运行
        schedule.every().day.at("08:00").do(self.run_crawler)
        
        # 每天下午2点运行
        schedule.every().day.at("14:00").do(self.run_crawler)
        
        # 每天晚上8点运行
        schedule.every().day.at("20:00").do(self.run_crawler)
        
        logger.info("Scheduler configured:")
        logger.info("- Daily at 08:00")
        logger.info("- Daily at 14:00") 
        logger.info("- Daily at 20:00")
        
        # 立即运行一次
        logger.info("Running initial crawl...")
        self.run_crawler()
        
        # 开始调度循环
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # 出错后等待5分钟再继续


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="News Crawler Scheduler")
    parser.add_argument("--config", default="rss.yaml", help="Config file path")
    parser.add_argument("--run-once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    
    scheduler = NewsScheduler(args.config)
    
    if args.run_once:
        # 只运行一次
        scheduler.run_crawler()
    else:
        # 启动定时调度
        scheduler.start_scheduler()


if __name__ == "__main__":
    main()
