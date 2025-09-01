#!/usr/bin/env python3
"""
调试版新闻爬虫 - 用于诊断问题
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.enhanced_news_crawler import EnhancedNewsCrawler

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("debug_crawler.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def debug_rss_sources():
    """调试RSS源"""
    print("=== 调试RSS源 ===")

    try:
        # 临时设置API key进行测试
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "test-key-for-rss-testing"

        crawler = EnhancedNewsCrawler("rss.yaml")
        sources = crawler.config.get("sources", [])

        print(f"配置的RSS源数量: {len(sources)}")

        for i, source in enumerate(sources, 1):
            print(f"\n{i}. {source['name']}")
            print(f"   URL: {source['url']}")
            print(f"   分类: {source.get('category', 'N/A')}")

            try:
                articles = crawler._fetch_single_source(source)
                print(f"   获取文章数: {len(articles)}")

                if articles:
                    sample = articles[0]
                    print(f"   示例标题: {sample.title}")
                    print(f"   示例链接: {sample.url}")
                else:
                    print("   ⚠️ 未获取到文章")

            except Exception as e:
                print(f"   ❌ 错误: {e}")

        return True

    except Exception as e:
        print(f"❌ RSS源调试失败: {e}")
        return False


def debug_openai_connection():
    """调试OpenAI连接"""
    print("\n=== 调试OpenAI连接 ===")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY 环境变量未设置")
        return False

    print(f"✓ API Key已设置 (长度: {len(api_key)})")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        # 测试简单请求
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "请回答'测试成功'"}],
            max_tokens=10,
        )

        result = response.choices[0].message.content.strip()
        print(f"✓ OpenAI API连接成功: {result}")
        return True

    except Exception as e:
        print(f"❌ OpenAI API连接失败: {e}")
        return False


def debug_single_article():
    """调试单篇文章处理"""
    print("\n=== 调试单篇文章处理 ===")

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 需要OPENAI_API_KEY进行测试")
        return False

    try:
        crawler = EnhancedNewsCrawler("rss.yaml")

        # 获取第一篇文章
        articles = crawler.fetch_rss_feeds()
        if not articles:
            print("❌ 未获取到任何文章")
            return False

        article = articles[0]
        print(f"测试文章: {article.title}")
        print(f"来源: {article.source}")
        print(f"链接: {article.url}")

        # 获取内容
        print("\n1. 获取文章内容...")
        if crawler.fetch_article_content(article):
            print(f"✓ 内容获取成功 (长度: {len(article.content)})")
            print(f"内容预览: {article.content[:200]}...")
        else:
            print("❌ 内容获取失败")
            return False

        # OpenAI分析
        print("\n2. OpenAI分析...")
        if crawler.analyze_with_openai(article):
            print(f"✓ 分析完成")
            print(f"是否量化相关: {article.is_quant_related}")
            print(f"分析理由: {article.analysis_reason}")
        else:
            print("❌ 分析失败")
            return False

        # 如果相关，尝试翻译
        if article.is_quant_related:
            print("\n3. 翻译文章...")
            if crawler.translate_article(article):
                print(f"✓ 翻译成功")
                print(f"翻译后标题: {article.title}")
                print(f"翻译内容预览: {article.translated_content[:200]}...")

                # 保存文章
                print("\n4. 保存文章...")
                crawl_date = "2025-06-23"  # 测试日期
                if crawler.save_article(article, crawl_date):
                    print("✓ 文章保存成功")

                    # 检查文件
                    filename = article.get_safe_filename(crawl_date)
                    filepath = crawler.temp_dir / filename
                    if filepath.exists():
                        print(f"✓ 文件已创建: {filepath}")
                        print(f"文件大小: {filepath.stat().st_size} bytes")
                    else:
                        print("❌ 文件未找到")
                else:
                    print("❌ 文章保存失败")
            else:
                print("❌ 翻译失败")
        else:
            print("文章不相关，跳过翻译")

        return True

    except Exception as e:
        print(f"❌ 单篇文章处理失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def debug_temp_directory():
    """调试临时目录"""
    print("\n=== 调试临时目录 ===")

    temp_dir = Path("temp_news")
    print(f"临时目录: {temp_dir.absolute()}")
    print(f"目录存在: {temp_dir.exists()}")

    if temp_dir.exists():
        files = list(temp_dir.rglob("*"))
        print(f"目录中文件数: {len(files)}")

        for file in files[:5]:  # 只显示前5个
            if file.is_file():
                print(f"  - {file.relative_to(temp_dir)} ({file.stat().st_size} bytes)")

    return True


def main():
    """运行调试"""
    print("新闻爬虫调试工具")
    print("=" * 50)

    tests = [
        ("RSS源调试", debug_rss_sources),
        ("OpenAI连接", debug_openai_connection),
        ("单篇文章处理", debug_single_article),
        ("临时目录检查", debug_temp_directory),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - 异常: {e}")
            results.append((test_name, False))

    # 总结
    print("\n" + "=" * 50)
    print("调试结果总结:")

    for test_name, result in results:
        status = "成功" if result else "失败"
        symbol = "✓" if result else "❌"
        print(f"{symbol} {test_name}: {status}")

    print(f"\n详细日志已保存到: debug_crawler.log")


if __name__ == "__main__":
    main()
