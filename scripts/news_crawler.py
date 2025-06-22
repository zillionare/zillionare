#!/usr/bin/env python3
"""
新闻自动抓取脚本
功能：
1. 从RSS源获取新闻列表
2. 抓取新闻正文并转换为Markdown
3. 使用AI识别量化交易相关内容
4. 保存相关文章，删除无关文章
"""

import os
import sys
import time
import logging
import hashlib
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
        
    def get_filename(self) -> str:
        """生成文件名"""
        # 使用URL的hash作为唯一标识
        url_hash = hashlib.md5(self.url.encode()).hexdigest()[:8]
        # 清理标题中的特殊字符
        clean_title = "".join(c for c in self.title if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_title = clean_title.replace(' ', '_')[:50]  # 限制长度
        date_str = self.published.strftime("%Y%m%d")
        return f"{date_str}_{clean_title}_{url_hash}.md"

class NewsCrawler:
    """新闻爬虫主类"""
    
    def __init__(self, config_path: str = "rss.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.session = requests.Session()
        self._setup_session()
        self.cache_dir = Path(".cache/news")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
    
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
        
        # 设置超时
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
                
                # 延迟请求
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
            # 尝试作为RSS源解析
            feed = feedparser.parse(source['url'])
            
            if feed.entries:
                # 标准RSS源
                for entry in feed.entries[:max_articles]:
                    article = NewsArticle(
                        title=entry.get('title', ''),
                        url=entry.get('link', ''),
                        source=source['name']
                    )
                    
                    # 解析发布时间
                    if hasattr(entry, 'published'):
                        try:
                            article.published = date_parser.parse(entry.published)
                        except:
                            pass
                    
                    articles.append(article)
            else:
                # 非标准RSS，尝试网页解析
                articles.extend(self._parse_web_page(source))
                
        except Exception as e:
            logger.error(f"Error parsing source {source['name']}: {e}")
        
        return articles
    
    def _parse_web_page(self, source: Dict) -> List[NewsArticle]:
        """解析网页获取文章链接"""
        articles = []
        try:
            response = self.session.get(source['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 根据不同网站的结构解析链接
            # 这里需要根据具体网站调整选择器
            links = soup.find_all('a', href=True)
            
            for link in links[:20]:  # 限制数量
                href = link.get('href')
                title = link.get_text().strip()
                
                if href and title and len(title) > 10:
                    # 处理相对链接
                    if href.startswith('/'):
                        href = f"{source['url'].split('/')[0]}//{source['url'].split('/')[2]}{href}"
                    elif not href.startswith('http'):
                        continue
                    
                    article = NewsArticle(
                        title=title,
                        url=href,
                        source=source['name']
                    )
                    articles.append(article)
                    
        except Exception as e:
            logger.error(f"Error parsing web page {source['url']}: {e}")
        
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
                # 如果没找到特定容器，使用body
                content_element = soup.find('body')

            if content_element:
                # 转换为Markdown
                article.markdown_content = md(str(content_element))
                article.content = content_element.get_text().strip()
                return True

        except Exception as e:
            logger.error(f"Error fetching content for {article.url}: {e}")

        return False

    def analyze_content_with_ai(self, article: NewsArticle) -> bool:
        """使用AI分析文章是否与量化交易相关"""
        if not openai.api_key:
            # 如果没有API key，使用关键词匹配
            return self._analyze_with_keywords(article)

        try:
            # 准备提示词
            prompt = f"""
请分析以下文章是否与量化交易、算法交易、程序化交易相关。

文章标题：{article.title}
文章内容：{article.content[:2000]}  # 限制长度

请回答"是"或"否"，并简要说明理由。

量化交易相关的主题包括但不限于：
- 算法交易策略
- 程序化交易
- 高频交易
- 因子投资
- 风险管理模型
- 回测分析
- 机器学习在金融中的应用
- 技术分析指标
- 量化投资工具
"""

            response = openai.ChatCompletion.create(
                model=self.config.get('ai_config', {}).get('openai', {}).get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "你是一个专业的量化交易分析师，能够准确识别与量化交易相关的内容。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get('ai_config', {}).get('openai', {}).get('max_tokens', 500),
                temperature=0.1
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"AI analysis for '{article.title}': {result}")

            # 判断结果
            article.is_quant_related = "是" in result or "yes" in result.lower()
            return True

        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            # 回退到关键词匹配
            return self._analyze_with_keywords(article)

    def _analyze_with_keywords(self, article: NewsArticle) -> bool:
        """使用关键词匹配分析文章"""
        keywords = self.config.get('ai_config', {}).get('quant_keywords', [])

        # 合并标题和内容进行匹配
        full_text = f"{article.title} {article.content}".lower()

        matched_keywords = []
        for keyword in keywords:
            if keyword.lower() in full_text:
                matched_keywords.append(keyword)

        # 如果匹配到关键词，认为相关
        article.is_quant_related = len(matched_keywords) > 0

        if matched_keywords:
            logger.info(f"Keyword match for '{article.title}': {matched_keywords}")

        return True

    def save_article(self, article: NewsArticle) -> str:
        """保存文章到文件"""
        filename = article.get_filename()
        filepath = self.cache_dir / filename

        # 准备Markdown内容
        markdown_content = f"""# {article.title}

**来源**: {article.source}
**链接**: {article.url}
**发布时间**: {article.published.strftime('%Y-%m-%d %H:%M:%S')}
**是否量化相关**: {'是' if article.is_quant_related else '否'}

---

{article.markdown_content}
"""

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Saved article: {filename}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving article {filename}: {e}")
            return ""

    def manage_files(self):
        """管理文件：删除非量化相关的文章，重命名为del_*"""
        for filepath in self.cache_dir.glob("*.md"):
            if filepath.name.startswith("del_"):
                continue

            try:
                # 读取文件检查是否量化相关
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if "**是否量化相关**: 否" in content:
                    # 重命名为del_*
                    new_name = f"del_{filepath.name}"
                    new_path = filepath.parent / new_name
                    filepath.rename(new_path)
                    logger.info(f"Renamed non-quant article: {filepath.name} -> {new_name}")

            except Exception as e:
                logger.error(f"Error managing file {filepath}: {e}")

    def run(self):
        """运行主流程"""
        logger.info("Starting news crawler...")

        # 1. 获取文章列表
        articles = self.fetch_rss_feeds()
        logger.info(f"Found {len(articles)} articles")

        if not articles:
            logger.warning("No articles found")
            return

        # 2. 获取文章内容并分析
        processed_count = 0
        for article in articles:
            try:
                # 获取内容
                if not self.fetch_article_content(article):
                    continue

                # AI分析
                self.analyze_content_with_ai(article)

                # 保存文章
                self.save_article(article)
                processed_count += 1

                # 延迟请求
                delay = self.config.get('crawler_config', {}).get('delay_between_requests', 1)
                time.sleep(delay)

            except Exception as e:
                logger.error(f"Error processing article '{article.title}': {e}")
                continue

        logger.info(f"Processed {processed_count} articles")

        # 3. 管理文件
        self.manage_files()

        logger.info("News crawler completed")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="News Crawler for Quantitative Trading")
    parser.add_argument("--config", default="rss.yaml", help="Config file path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

    args = parser.parse_args()

    try:
        crawler = NewsCrawler(args.config)
        if args.dry_run:
            logger.info("Dry run mode - no files will be saved")
        else:
            crawler.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
