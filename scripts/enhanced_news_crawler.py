#!/usr/bin/env python3
"""
增强版新闻爬虫 - 专为GitHub Actions设计
功能：
1. 强制使用OpenAI API进行内容分析
2. 翻译量化交易相关文章
3. 保存到quant_news分支的指定目录结构
4. 安全的文件名处理
"""

import os
import sys
import time
import logging
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yaml
import requests
import feedparser
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import openai
from dateutil import parser as date_parser
from slugify import slugify

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NewsArticle:
    """新闻文章数据类"""
    def __init__(self, title: str, url: str, content: str = "", 
                 published: Optional[datetime] = None, source: str = ""):
        self.title = title
        self.url = url
        self.content = content
        self.published = published or datetime.now()
        self.source = source
        self.markdown_content = ""
        self.is_quant_related = False
        self.translated_content = ""
        self.analysis_reason = ""
        
    def get_safe_filename(self, crawl_date: str) -> str:
        """生成安全的文件名"""
        # 使用slugify处理标题
        safe_title = slugify(self.title, max_length=100)
        if not safe_title:
            # 如果标题无法转换，使用URL的hash
            url_hash = hashlib.md5(self.url.encode()).hexdigest()[:8]
            safe_title = f"article_{url_hash}"
        
        return f"news/{crawl_date}/{safe_title}.md"

class EnhancedNewsCrawler:
    """增强版新闻爬虫"""
    
    def __init__(self, config_path: str = "rss.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.session = requests.Session()
        self._setup_session()
        
        # 检查OpenAI API密钥
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.error("OPENAI_API_KEY is required for enhanced crawler")
            sys.exit(1)
        
        # 创建临时目录
        self.temp_dir = Path("temp_news")
        self.temp_dir.mkdir(exist_ok=True)
        
        # 统计信息
        self.stats = {
            'total_articles': 0,
            'quant_related': 0,
            'non_quant': 0,
            'translation_success': 0,
            'translation_failed': 0
        }
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def _setup_session(self):
        """设置请求会话"""
        headers = self.config.get('crawler_config', {}).get('headers', {})
        self.session.headers.update(headers)
        
        timeout = self.config.get('crawler_config', {}).get('timeout', 30)
        self.session.timeout = timeout
    
    def fetch_rss_feeds(self) -> List[NewsArticle]:
        """获取RSS源中的文章列表"""
        articles = []
        sources = self.config.get('sources', [])
        
        for source in sources:
            try:
                logger.info(f"Fetching from {source['name']}")
                articles.extend(self._fetch_single_source(source))
                
                delay = self.config.get('crawler_config', {}).get('delay_between_requests', 1)
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {e}")
                continue
        
        return articles
    
    def _fetch_single_source(self, source: Dict) -> List[NewsArticle]:
        """从单个RSS源获取文章"""
        articles = []
        max_articles = self.config.get('crawler_config', {}).get('max_articles_per_source', 20)
        
        try:
            feed = feedparser.parse(source['url'])
            
            if feed.entries:
                for entry in feed.entries[:max_articles]:
                    article = NewsArticle(
                        title=entry.get('title', ''),
                        url=entry.get('link', ''),
                        source=source['name']
                    )
                    
                    if hasattr(entry, 'published'):
                        try:
                            article.published = date_parser.parse(entry.published)
                        except:
                            pass
                    
                    articles.append(article)
            else:
                logger.warning(f"No entries found in RSS feed: {source['name']}")
                
        except Exception as e:
            logger.error(f"Error parsing source {source['name']}: {e}")
        
        return articles
    
    def fetch_article_content(self, article: NewsArticle) -> bool:
        """获取文章正文内容"""
        try:
            logger.info(f"Fetching content for: {article.title}")
            response = self.session.get(article.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # 尝试找到主要内容区域
            content_selectors = [
                'article', '.article-content', '.content', '.post-content',
                '.entry-content', '.article-body', '#content', '.main-content'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    break
            
            if not content_element:
                content_element = soup.find('body')
            
            if content_element:
                article.markdown_content = md(str(content_element))
                article.content = content_element.get_text().strip()
                return True
            
        except Exception as e:
            logger.error(f"Error fetching content for {article.url}: {e}")
        
        return False

    def analyze_with_openai(self, article: NewsArticle) -> bool:
        """使用OpenAI分析文章是否与量化交易相关"""
        try:
            prompt = f"""
请分析以下文章是否与量化交易、算法交易、程序化交易相关。

文章标题：{article.title}
文章来源：{article.source}
文章内容：{article.content[:3000]}

请严格按照以下格式回答：
判断：是/否
理由：[简要说明判断理由，不超过100字]

量化交易相关的主题包括但不限于：
- 算法交易策略和技术
- 程序化交易系统
- 高频交易技术
- 因子投资和多因子模型
- 风险管理模型和技术
- 回测分析和策略验证
- 机器学习在金融中的应用
- 量化投资工具和平台
- 技术分析指标和模型
- 金融数据分析和挖掘
- 交易系统开发
- 金融工程和衍生品定价

请注意：
- 仅仅提到股票、基金、投资等一般性金融话题不算量化交易相关
- 必须涉及具体的量化、算法、程序化、技术分析等内容才算相关
- 公司财报、市场新闻、政策解读等不算量化交易相关
"""

            response = openai.ChatCompletion.create(
                model=self.config.get('ai_config', {}).get('openai', {}).get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "你是一个专业的量化交易分析师，能够准确识别与量化交易相关的内容。请严格按照要求的格式回答。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"AI analysis for '{article.title}': {result}")

            # 解析结果
            lines = result.split('\n')
            judgment_line = ""
            reason_line = ""

            for line in lines:
                if line.startswith('判断：'):
                    judgment_line = line
                elif line.startswith('理由：'):
                    reason_line = line

            article.is_quant_related = "是" in judgment_line
            article.analysis_reason = reason_line.replace('理由：', '').strip()

            return True

        except Exception as e:
            logger.error(f"Error in OpenAI analysis: {e}")
            return False

    def translate_article(self, article: NewsArticle) -> bool:
        """翻译文章内容为中文"""
        try:
            # 如果原文已经是中文，可能不需要翻译
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', article.content))
            total_chars = len(article.content)

            if total_chars > 0 and chinese_chars / total_chars > 0.3:
                logger.info(f"Article '{article.title}' appears to be in Chinese, skipping translation")
                article.translated_content = article.markdown_content
                return True

            prompt = f"""
请将以下英文新闻文章翻译成中文，保持专业性和准确性，特别注意量化交易相关术语的准确翻译。

标题：{article.title}
内容：{article.markdown_content[:4000]}

请按照以下格式输出：
标题：[翻译后的标题]
内容：[翻译后的内容，保持Markdown格式]
"""

            response = openai.ChatCompletion.create(
                model=self.config.get('ai_config', {}).get('openai', {}).get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "你是一个专业的金融翻译专家，擅长翻译量化交易相关内容。请保持翻译的专业性和准确性。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            result = response.choices[0].message.content.strip()

            # 解析翻译结果
            lines = result.split('\n', 1)
            if len(lines) >= 2:
                translated_title = lines[0].replace('标题：', '').strip()
                translated_content = lines[1].replace('内容：', '').strip()

                # 更新文章标题和内容
                if translated_title:
                    article.title = translated_title
                article.translated_content = translated_content
            else:
                article.translated_content = result

            logger.info(f"Successfully translated article: {article.title}")
            return True

        except Exception as e:
            logger.error(f"Error translating article: {e}")
            return False

    def save_article(self, article: NewsArticle, crawl_date: str) -> bool:
        """保存文章到临时目录"""
        try:
            filename = article.get_safe_filename(crawl_date)
            filepath = self.temp_dir / filename

            # 确保目录存在
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # 准备Markdown内容
            markdown_content = f"""# {article.title}

**来源**: {article.source}
**原文链接**: {article.url}
**发布时间**: {article.published.strftime('%Y-%m-%d %H:%M:%S')}
**抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析理由**: {article.analysis_reason}

---

{article.translated_content}

---

*本文由AI自动翻译，如有错误请以原文为准。*
"""

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            logger.info(f"Saved article: {filename}")
            return True

        except Exception as e:
            logger.error(f"Error saving article {article.title}: {e}")
            return False

    def log_discarded_article(self, article: NewsArticle):
        """记录被丢弃的文章信息"""
        logger.info(f"DISCARDED - Title: {article.title}")
        logger.info(f"DISCARDED - URL: {article.url}")
        logger.info(f"DISCARDED - Reason: {article.analysis_reason}")

        self.stats['non_quant'] += 1

    def run(self):
        """运行主流程"""
        logger.info("Starting enhanced news crawler...")

        crawl_date = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"Crawl date: {crawl_date}")

        # 1. 获取文章列表
        articles = self.fetch_rss_feeds()
        logger.info(f"Found {len(articles)} articles")
        self.stats['total_articles'] = len(articles)

        if not articles:
            logger.warning("No articles found")
            return

        # 2. 处理每篇文章
        for i, article in enumerate(articles, 1):
            try:
                logger.info(f"Processing article {i}/{len(articles)}: {article.title}")

                # 获取内容
                if not self.fetch_article_content(article):
                    logger.warning(f"Failed to fetch content for: {article.title}")
                    continue

                # OpenAI分析
                if not self.analyze_with_openai(article):
                    logger.warning(f"Failed to analyze article: {article.title}")
                    continue

                # 检查是否量化相关
                if not article.is_quant_related:
                    self.log_discarded_article(article)
                    continue

                logger.info(f"Article is quant-related: {article.title}")
                self.stats['quant_related'] += 1

                # 翻译文章
                if self.translate_article(article):
                    self.stats['translation_success'] += 1

                    # 保存文章
                    if self.save_article(article, crawl_date):
                        logger.info(f"Successfully processed: {article.title}")
                    else:
                        logger.error(f"Failed to save: {article.title}")
                else:
                    self.stats['translation_failed'] += 1
                    logger.error(f"Failed to translate: {article.title}")

                # 延迟请求
                delay = self.config.get('crawler_config', {}).get('delay_between_requests', 2)
                time.sleep(delay)

            except Exception as e:
                logger.error(f"Error processing article '{article.title}': {e}")
                continue

        # 3. 输出统计信息
        self.print_stats()

        logger.info("Enhanced news crawler completed")

    def print_stats(self):
        """打印统计信息"""
        logger.info("=== Crawling Statistics ===")
        logger.info(f"Total articles processed: {self.stats['total_articles']}")
        logger.info(f"Quant-related articles: {self.stats['quant_related']}")
        logger.info(f"Non-quant articles: {self.stats['non_quant']}")
        logger.info(f"Translation successful: {self.stats['translation_success']}")
        logger.info(f"Translation failed: {self.stats['translation_failed']}")

        if self.stats['total_articles'] > 0:
            quant_rate = (self.stats['quant_related'] / self.stats['total_articles']) * 100
            logger.info(f"Quant-related rate: {quant_rate:.1f}%")


def main():
    """主函数"""
    try:
        crawler = EnhancedNewsCrawler("rss.yaml")
        crawler.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
