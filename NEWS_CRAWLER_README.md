# 新闻自动抓取系统

这是一个专门为量化交易内容设计的新闻自动抓取系统，能够从多个RSS源获取新闻，使用AI识别量化交易相关内容，并自动管理文件。

## 功能特性

1. **多源RSS抓取**: 支持多个新闻源的RSS订阅
2. **智能内容提取**: 自动提取网页正文并转换为Markdown格式
3. **AI内容分析**: 使用OpenAI API或关键词匹配识别量化交易相关内容
4. **自动文件管理**: 保存相关文章，标记删除无关文章
5. **定时任务**: 支持定时自动抓取
6. **文件管理工具**: 提供统计、搜索、清理等管理功能

## 安装依赖

```bash
# 安装Poetry（如果未安装）
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install --no-root
```

## 配置

### 1. RSS源配置

编辑 `rss.yaml` 文件，配置新闻源：

```yaml
sources:
  - name: "新浪财经"
    url: "https://finance.sina.com.cn/roll/index.d.html?cid=56588&page=1"
    category: "finance"
    encoding: "utf-8"
```

### 2. AI配置

设置环境变量：

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

如果没有OpenAI API key，系统会自动使用关键词匹配模式。

## 使用方法

### 1. 单次运行

```bash
# 运行新闻抓取
poetry run python scripts/news_crawler.py

# 干运行模式（不保存文件）
poetry run python scripts/news_crawler.py --dry-run
```

### 2. 定时运行

```bash
# 启动定时调度器（每天8点、14点、20点运行）
poetry run python scripts/schedule_crawler.py

# 只运行一次
poetry run python scripts/schedule_crawler.py --run-once
```

### 3. 文件管理

```bash
# 查看统计信息
poetry run python scripts/news_manager.py stats

# 搜索文章
poetry run python scripts/news_manager.py search "量化交易"

# 列出最近7天的文章
poetry run python scripts/news_manager.py recent --days 7

# 清理30天前的文件
poetry run python scripts/news_manager.py clean --days 30

# 恢复被删除的文件
poetry run python scripts/news_manager.py restore
```

## 文件结构

```
.
├── rss.yaml                    # RSS源配置文件
├── pyproject.toml             # Python项目配置
├── scripts/
│   ├── news_crawler.py        # 主要爬虫脚本
│   ├── schedule_crawler.py    # 定时任务脚本
│   └── news_manager.py        # 文件管理工具
└── .cache/news/               # 新闻文件存储目录
    ├── 20231201_article1.md   # 量化相关文章
    ├── 20231201_article2.md
    └── del_20231201_article3.md  # 被标记删除的文章
```

## 工作流程

1. **获取文章列表**: 从配置的RSS源获取最新文章链接
2. **抓取正文内容**: 访问每个文章链接，提取正文内容
3. **转换为Markdown**: 将HTML内容转换为Markdown格式
4. **AI内容分析**: 使用OpenAI API或关键词匹配判断是否与量化交易相关
5. **保存文章**: 将文章保存为Markdown文件，包含元数据
6. **文件管理**: 将非量化相关的文章重命名为`del_*`前缀

## 配置说明

### RSS源配置

- `name`: 新闻源名称
- `url`: RSS订阅地址或网页地址
- `category`: 分类标签
- `encoding`: 编码格式

### AI配置

- `openai.api_key`: OpenAI API密钥
- `openai.model`: 使用的模型（默认gpt-3.5-turbo）
- `quant_keywords`: 量化交易关键词列表

### 爬虫配置

- `headers`: HTTP请求头
- `timeout`: 请求超时时间
- `max_retries`: 最大重试次数
- `delay_between_requests`: 请求间延迟
- `max_articles_per_source`: 每个源最大文章数

## 日志

系统会生成以下日志文件：

- `news_crawler.log`: 爬虫运行日志
- `scheduler.log`: 定时任务日志

## 注意事项

1. **请求频率**: 系统内置了请求延迟，避免对目标网站造成压力
2. **内容版权**: 抓取的内容仅供个人学习研究使用
3. **API限制**: 使用OpenAI API时注意token使用量
4. **网站结构**: 不同网站的HTML结构可能需要调整解析逻辑

## 故障排除

### 常见问题

1. **无法获取文章内容**: 检查网站是否需要特殊的请求头或认证
2. **AI分析失败**: 检查OpenAI API key是否正确设置
3. **编码问题**: 调整RSS源配置中的encoding参数
4. **文件权限**: 确保对`.cache/news`目录有写权限

### 调试模式

使用`--dry-run`参数进行调试，不会实际保存文件：

```bash
poetry run python scripts/news_crawler.py --dry-run
```

## 扩展开发

系统采用模块化设计，可以轻松扩展：

1. **添加新的新闻源**: 在`rss.yaml`中添加配置
2. **自定义内容解析**: 修改`_parse_web_page`方法
3. **改进AI分析**: 调整提示词或使用其他AI服务
4. **添加新的文件格式**: 扩展`save_article`方法

## 许可证

本项目仅供学习和研究使用。
