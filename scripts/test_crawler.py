#!/usr/bin/env python3
"""
新闻爬虫测试脚本
用于测试系统各个组件是否正常工作
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.news_crawler import NewsCrawler, NewsArticle
from scripts.news_manager import NewsManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_config_loading():
    """测试配置文件加载"""
    print("=== 测试配置文件加载 ===")
    try:
        crawler = NewsCrawler("rss.yaml")
        config = crawler.config
        
        print(f"✓ 配置文件加载成功")
        print(f"  - RSS源数量: {len(config.get('sources', []))}")
        print(f"  - AI配置: {'存在' if config.get('ai_config') else '不存在'}")
        print(f"  - 爬虫配置: {'存在' if config.get('crawler_config') else '不存在'}")
        
        return True
    except Exception as e:
        print(f"✗ 配置文件加载失败: {e}")
        return False

def test_article_creation():
    """测试文章对象创建"""
    print("\n=== 测试文章对象创建 ===")
    try:
        article = NewsArticle(
            title="测试文章标题",
            url="https://example.com/test",
            content="这是一个测试文章内容，包含量化交易相关信息。",
            source="测试源"
        )
        
        filename = article.get_filename()
        print(f"✓ 文章对象创建成功")
        print(f"  - 标题: {article.title}")
        print(f"  - URL: {article.url}")
        print(f"  - 生成文件名: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ 文章对象创建失败: {e}")
        return False

def test_keyword_analysis():
    """测试关键词分析"""
    print("\n=== 测试关键词分析 ===")
    try:
        crawler = NewsCrawler("rss.yaml")
        
        # 测试量化相关文章
        quant_article = NewsArticle(
            title="量化交易策略研究",
            url="https://example.com/quant",
            content="本文介绍了一种基于机器学习的量化交易策略，通过因子分析和回测验证了策略的有效性。",
            source="测试源"
        )
        
        # 测试非量化相关文章
        non_quant_article = NewsArticle(
            title="今日天气预报",
            url="https://example.com/weather",
            content="今天天气晴朗，温度适宜，适合外出活动。",
            source="测试源"
        )
        
        # 分析文章
        crawler._analyze_with_keywords(quant_article)
        crawler._analyze_with_keywords(non_quant_article)
        
        print(f"✓ 关键词分析完成")
        print(f"  - 量化文章识别: {'正确' if quant_article.is_quant_related else '错误'}")
        print(f"  - 非量化文章识别: {'正确' if not non_quant_article.is_quant_related else '错误'}")
        
        return quant_article.is_quant_related and not non_quant_article.is_quant_related
        
    except Exception as e:
        print(f"✗ 关键词分析失败: {e}")
        return False

def test_file_operations():
    """测试文件操作"""
    print("\n=== 测试文件操作 ===")
    try:
        crawler = NewsCrawler("rss.yaml")
        
        # 创建测试文章
        test_article = NewsArticle(
            title="测试文章",
            url="https://example.com/test",
            content="这是一个测试文章",
            source="测试源"
        )
        test_article.markdown_content = "# 测试文章\n\n这是测试内容。"
        test_article.is_quant_related = True
        
        # 保存文章
        filepath = crawler.save_article(test_article)
        
        if filepath and Path(filepath).exists():
            print(f"✓ 文章保存成功: {Path(filepath).name}")
            
            # 清理测试文件
            Path(filepath).unlink()
            print(f"✓ 测试文件清理完成")
            return True
        else:
            print(f"✗ 文章保存失败")
            return False
            
    except Exception as e:
        print(f"✗ 文件操作失败: {e}")
        return False

def test_news_manager():
    """测试新闻管理器"""
    print("\n=== 测试新闻管理器 ===")
    try:
        manager = NewsManager()
        stats = manager.get_stats()
        
        print(f"✓ 新闻管理器创建成功")
        print(f"  - 缓存目录: {manager.cache_dir}")
        print(f"  - 当前文件数: {stats['total_files']}")
        
        return True
    except Exception as e:
        print(f"✗ 新闻管理器测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖库"""
    print("\n=== 测试依赖库 ===")
    dependencies = [
        ('requests', 'HTTP请求库'),
        ('feedparser', 'RSS解析库'),
        ('bs4', 'HTML解析库'),
        ('markdownify', 'HTML转Markdown库'),
        ('yaml', 'YAML配置文件库'),
        ('schedule', '定时任务库')
    ]
    
    all_ok = True
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"✓ {desc} ({dep})")
        except ImportError:
            print(f"✗ {desc} ({dep}) - 未安装")
            all_ok = False
    
    # 测试OpenAI（可选）
    try:
        import openai
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"✓ OpenAI库 - API Key已配置")
        else:
            print(f"⚠ OpenAI库 - API Key未配置（将使用关键词匹配）")
    except ImportError:
        print(f"✗ OpenAI库 - 未安装")
        all_ok = False
    
    return all_ok

def main():
    """运行所有测试"""
    print("新闻爬虫系统测试")
    print("=" * 50)
    
    tests = [
        ("依赖库检查", test_dependencies),
        ("配置文件加载", test_config_loading),
        ("文章对象创建", test_article_creation),
        ("关键词分析", test_keyword_analysis),
        ("文件操作", test_file_operations),
        ("新闻管理器", test_news_manager),
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
        print("🎉 所有测试通过！系统可以正常使用。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
