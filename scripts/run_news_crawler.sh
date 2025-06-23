#!/bin/bash

# 新闻爬虫启动脚本
# 使用方法: ./run_news_crawler.sh [command] [options]

# 设置Poetry路径
export PATH="/home/augment-agent/.local/bin:$PATH"

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印帮助信息
show_help() {
    echo -e "${BLUE}新闻爬虫系统 - 使用说明${NC}"
    echo ""
    echo "使用方法: $0 [command] [options]"
    echo ""
    echo "可用命令:"
    echo "  test                    运行系统测试"
    echo "  crawl                   运行一次新闻抓取（原版）"
    echo "  enhanced-crawl          运行增强版新闻抓取（需要OpenAI API）"
    echo "  test-enhanced           测试增强版爬虫"
    echo "  debug                   调试增强版爬虫问题"
    echo "  schedule                启动定时调度器"
    echo "  stats                   显示统计信息"
    echo "  search <keyword>        搜索文章"
    echo "  recent [days]           显示最近文章（默认7天）"
    echo "  clean [days]            清理旧文件（默认30天）"
    echo "  restore                 恢复被删除的文件"
    echo "  help                    显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 test                 # 运行系统测试"
    echo "  $0 crawl                # 抓取新闻（原版）"
    echo "  $0 enhanced-crawl       # 增强版抓取（需要OpenAI API）"
    echo "  $0 test-enhanced        # 测试增强版爬虫"
    echo "  $0 debug                # 调试增强版爬虫问题"
    echo "  $0 search 量化交易       # 搜索量化交易相关文章"
    echo "  $0 recent 3             # 显示最近3天的文章"
    echo "  $0 clean 15             # 清理15天前的文件"
}

# 检查Poetry是否安装
check_poetry() {
    if ! command -v poetry &> /dev/null; then
        echo -e "${RED}错误: Poetry未安装${NC}"
        echo "请先安装Poetry: curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi
}

# 检查依赖是否安装
check_dependencies() {
    if [ ! -f "poetry.lock" ]; then
        echo -e "${YELLOW}警告: 依赖未安装，正在安装...${NC}"
        poetry install --no-root
    fi
}

# 运行测试
run_test() {
    echo -e "${BLUE}运行系统测试...${NC}"
    poetry run python scripts/test_crawler.py
}

# 运行爬虫
run_crawl() {
    echo -e "${BLUE}开始抓取新闻（原版）...${NC}"
    poetry run python scripts/news_crawler.py "$@"
}

# 运行增强版爬虫
run_enhanced_crawl() {
    echo -e "${BLUE}开始增强版新闻抓取...${NC}"
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}错误: 需要设置 OPENAI_API_KEY 环境变量${NC}"
        echo "请设置: export OPENAI_API_KEY=your-api-key"
        exit 1
    fi
    poetry run python scripts/enhanced_news_crawler.py "$@"
}

# 测试增强版爬虫
test_enhanced() {
    echo -e "${BLUE}测试增强版爬虫...${NC}"
    poetry run python scripts/test_enhanced_crawler.py
}

# 调试增强版爬虫
debug_crawler() {
    echo -e "${BLUE}调试增强版爬虫...${NC}"
    poetry run python scripts/debug_crawler.py
}

# 启动调度器
run_schedule() {
    echo -e "${BLUE}启动定时调度器...${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止调度器${NC}"
    poetry run python scripts/schedule_crawler.py "$@"
}

# 显示统计信息
show_stats() {
    echo -e "${BLUE}显示统计信息...${NC}"
    poetry run python scripts/news_manager.py stats
}

# 搜索文章
search_articles() {
    if [ -z "$1" ]; then
        echo -e "${RED}错误: 请提供搜索关键词${NC}"
        echo "使用方法: $0 search <keyword>"
        exit 1
    fi
    echo -e "${BLUE}搜索文章: $1${NC}"
    poetry run python scripts/news_manager.py search "$1"
}

# 显示最近文章
show_recent() {
    local days=${1:-7}
    echo -e "${BLUE}显示最近 $days 天的文章...${NC}"
    poetry run python scripts/news_manager.py recent --days "$days"
}

# 清理旧文件
clean_files() {
    local days=${1:-30}
    echo -e "${BLUE}清理 $days 天前的文件...${NC}"
    poetry run python scripts/news_manager.py clean --days "$days"
}

# 恢复文件
restore_files() {
    echo -e "${BLUE}恢复被删除的文件...${NC}"
    poetry run python scripts/news_manager.py restore
}

# 主函数
main() {
    # 检查环境
    check_poetry
    check_dependencies
    
    # 解析命令
    case "${1:-help}" in
        "test")
            run_test
            ;;
        "crawl")
            shift
            run_crawl "$@"
            ;;
        "enhanced-crawl")
            shift
            run_enhanced_crawl "$@"
            ;;
        "test-enhanced")
            test_enhanced
            ;;
        "debug")
            debug_crawler
            ;;
        "schedule")
            shift
            run_schedule "$@"
            ;;
        "stats")
            show_stats
            ;;
        "search")
            shift
            search_articles "$@"
            ;;
        "recent")
            shift
            show_recent "$@"
            ;;
        "clean")
            shift
            clean_files "$@"
            ;;
        "restore")
            restore_files
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}错误: 未知命令 '$1'${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
