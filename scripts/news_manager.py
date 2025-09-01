#!/usr/bin/env python3
"""
新闻文件管理工具
提供清理、统计、搜索等功能
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NewsManager:
    """新闻文件管理器"""

    def __init__(self, cache_dir: str = ".cache/news"):
        self.cache_dir = Path(cache_dir)
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            "total_files": 0,
            "quant_related": 0,
            "non_quant": 0,
            "deleted_files": 0,
            "file_sizes": [],
        }

        for filepath in self.cache_dir.glob("*.md"):
            stats["total_files"] += 1

            if filepath.name.startswith("del_"):
                stats["deleted_files"] += 1
            else:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    if "**是否量化相关**: 是" in content:
                        stats["quant_related"] += 1
                    else:
                        stats["non_quant"] += 1

                    stats["file_sizes"].append(filepath.stat().st_size)

                except Exception as e:
                    logger.error(f"Error reading {filepath}: {e}")

        return stats

    def print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()

        print("\n=== 新闻文件统计 ===")
        print(f"总文件数: {stats['total_files']}")
        print(f"量化相关: {stats['quant_related']}")
        print(f"非量化相关: {stats['non_quant']}")
        print(f"已删除文件: {stats['deleted_files']}")

        if stats["file_sizes"]:
            avg_size = sum(stats["file_sizes"]) / len(stats["file_sizes"])
            total_size = sum(stats["file_sizes"])
            print(f"平均文件大小: {avg_size:.1f} bytes")
            print(f"总大小: {total_size / 1024:.1f} KB")

    def clean_old_files(self, days: int = 30):
        """清理旧文件"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0

        for filepath in self.cache_dir.glob("*.md"):
            try:
                # 从文件名中提取日期
                filename = filepath.name
                if len(filename) >= 8 and filename[:8].isdigit():
                    file_date_str = filename[:8]
                    file_date = datetime.strptime(file_date_str, "%Y%m%d")

                    if file_date < cutoff_date:
                        filepath.unlink()
                        cleaned_count += 1
                        logger.info(f"Deleted old file: {filename}")

            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")

        print(f"清理了 {cleaned_count} 个超过 {days} 天的文件")

    def search_articles(self, keyword: str) -> List[Path]:
        """搜索包含关键词的文章"""
        matching_files = []

        for filepath in self.cache_dir.glob("*.md"):
            if filepath.name.startswith("del_"):
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                if keyword.lower() in content.lower():
                    matching_files.append(filepath)

            except Exception as e:
                logger.error(f"Error searching {filepath}: {e}")

        return matching_files

    def list_recent_articles(self, days: int = 7):
        """列出最近的文章"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_files = []

        for filepath in self.cache_dir.glob("*.md"):
            if filepath.name.startswith("del_"):
                continue

            try:
                # 从文件名中提取日期
                filename = filepath.name
                if len(filename) >= 8 and filename[:8].isdigit():
                    file_date_str = filename[:8]
                    file_date = datetime.strptime(file_date_str, "%Y%m%d")

                    if file_date >= cutoff_date:
                        recent_files.append((filepath, file_date))

            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")

        # 按日期排序
        recent_files.sort(key=lambda x: x[1], reverse=True)

        print(f"\n=== 最近 {days} 天的文章 ===")
        for filepath, file_date in recent_files:
            # 读取标题
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    title = (
                        first_line.replace("# ", "")
                        if first_line.startswith("# ")
                        else filepath.name
                    )

                print(f"{file_date.strftime('%Y-%m-%d')}: {title}")

            except Exception as e:
                print(f"{file_date.strftime('%Y-%m-%d')}: {filepath.name}")

    def restore_deleted_files(self):
        """恢复被删除的文件（移除del_前缀）"""
        restored_count = 0

        for filepath in self.cache_dir.glob("del_*.md"):
            try:
                new_name = filepath.name[4:]  # 移除"del_"前缀
                new_path = filepath.parent / new_name

                if not new_path.exists():
                    filepath.rename(new_path)
                    restored_count += 1
                    logger.info(f"Restored file: {filepath.name} -> {new_name}")
                else:
                    logger.warning(f"Cannot restore {filepath.name}: target exists")

            except Exception as e:
                logger.error(f"Error restoring {filepath}: {e}")

        print(f"恢复了 {restored_count} 个文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="News File Manager")
    parser.add_argument(
        "--cache-dir", default=".cache/news", help="Cache directory path"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 统计命令
    subparsers.add_parser("stats", help="Show statistics")

    # 清理命令
    clean_parser = subparsers.add_parser("clean", help="Clean old files")
    clean_parser.add_argument(
        "--days", type=int, default=30, help="Days to keep (default: 30)"
    )

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="Search articles")
    search_parser.add_argument("keyword", help="Keyword to search")

    # 列出最近文章
    recent_parser = subparsers.add_parser("recent", help="List recent articles")
    recent_parser.add_argument(
        "--days", type=int, default=7, help="Days to look back (default: 7)"
    )

    # 恢复文件
    subparsers.add_parser("restore", help="Restore deleted files")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = NewsManager(args.cache_dir)

    if args.command == "stats":
        manager.print_stats()
    elif args.command == "clean":
        manager.clean_old_files(args.days)
    elif args.command == "search":
        results = manager.search_articles(args.keyword)
        print(f"\n找到 {len(results)} 篇包含 '{args.keyword}' 的文章:")
        for filepath in results:
            print(f"- {filepath.name}")
    elif args.command == "recent":
        manager.list_recent_articles(args.days)
    elif args.command == "restore":
        manager.restore_deleted_files()


if __name__ == "__main__":
    main()
