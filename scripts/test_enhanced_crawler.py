#!/usr/bin/env python3
"""
增强版新闻爬虫测试脚本
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.enhanced_news_crawler import EnhancedNewsCrawler, NewsArticle

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_dependencies():
    """测试依赖库"""
    print("=== 测试依赖库 ===")
    dependencies = [
        ('requests', 'HTTP请求库'),
        ('feedparser', 'RSS解析库'),
        ('bs4', 'HTML解析库'),
        ('markdownify', 'HTML转Markdown库'),
        ('yaml', 'YAML配置文件库'),
        ('openai', 'OpenAI API库'),
        ('slugify', '文件名安全处理库')
    ]
    
    all_ok = True
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"✓ {desc} ({dep})")
        except ImportError:
            print(f"✗ {desc} ({dep}) - 未安装")
            all_ok = False
    
    # 测试OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✓ OpenAI API Key已配置")
    else:
        print(f"✗ OpenAI API Key未配置")
        all_ok = False
    
    return all_ok

def test_article_filename():
    """测试文章文件名生成"""
    print("\n=== 测试文件名生成 ===")
    
    test_cases = [
        ("正常英文标题", "Normal English Title"),
        ("中文标题测试", "中文标题测试"),
        ("特殊字符!@#$%^&*()", "Special Characters!@#$%^&*()"),
        ("很长的标题" * 20, "Very Long Title" * 20),
        ("", ""),  # 空标题
    ]
    
    crawl_date = "2025-06-22"
    
    for desc, title in test_cases:
        article = NewsArticle(
            title=title,
            url="https://example.com/test",
            source="测试源"
        )
        
        filename = article.get_safe_filename(crawl_date)
        print(f"✓ {desc}: {filename}")
    
    return True

def test_openai_connection():
    """测试OpenAI连接"""
    print("\n=== 测试OpenAI连接 ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("✗ 跳过OpenAI测试 - 未配置API Key")
        return False
    
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # 简单的测试请求
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, this is a test. Please respond with 'Test successful'."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✓ OpenAI API连接成功: {result}")
        return True
        
    except Exception as e:
        print(f"✗ OpenAI API连接失败: {e}")
        return False

def test_crawler_initialization():
    """测试爬虫初始化"""
    print("\n=== 测试爬虫初始化 ===")
    
    try:
        # 临时设置API Key（如果没有的话）
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "test-key"
        
        crawler = EnhancedNewsCrawler("rss.yaml")
        print(f"✓ 爬虫初始化成功")
        print(f"  - 配置源数量: {len(crawler.config.get('sources', []))}")
        print(f"  - 临时目录: {crawler.temp_dir}")
        
        return True
        
    except Exception as e:
        print(f"✗ 爬虫初始化失败: {e}")
        return False

def test_rss_parsing():
    """测试RSS解析（使用真实源）"""
    print("\n=== 测试RSS解析 ===")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("✗ 跳过RSS测试 - 需要OpenAI API Key")
        return False
    
    try:
        crawler = EnhancedNewsCrawler("rss.yaml")
        
        # 只测试第一个源
        sources = crawler.config.get('sources', [])
        if not sources:
            print("✗ 没有配置RSS源")
            return False
        
        test_source = sources[0]
        print(f"测试RSS源: {test_source['name']}")
        
        articles = crawler._fetch_single_source(test_source)
        print(f"✓ 成功获取 {len(articles)} 篇文章")
        
        if articles:
            sample_article = articles[0]
            print(f"  - 示例文章: {sample_article.title}")
            print(f"  - 链接: {sample_article.url}")
        
        return True
        
    except Exception as e:
        print(f"✗ RSS解析失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("增强版新闻爬虫测试")
    print("=" * 50)
    
    tests = [
        ("依赖库检查", test_dependencies),
        ("文件名生成", test_article_filename),
        ("OpenAI连接", test_openai_connection),
        ("爬虫初始化", test_crawler_initialization),
        ("RSS解析", test_rss_parsing),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} - 异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结:")
    
    passed = 0
    for test_name, result in results:
        status = "通过" if result else "失败"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！增强版爬虫可以正常使用。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
