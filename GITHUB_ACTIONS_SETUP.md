# GitHub Actions 自动化设置指南

由于API token权限限制，需要手动创建GitHub Actions工作流文件。

## 📁 创建工作流文件

在GitHub仓库中创建以下文件：

**文件路径**: `.github/workflows/news-crawler.yml`

**文件内容**:

```yaml
name: Daily News Crawler

on:
  schedule:
    # 每天 UTC+8 上午 8:00 运行 (UTC 00:00)
    - cron: '0 0 * * *'
  workflow_dispatch: # 允许手动触发

jobs:
  crawl-news:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}
    
    - name: Install dependencies
      run: poetry install --no-root
    
    - name: Create quant_news branch if not exists
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        
        # 检查 quant_news 分支是否存在
        if git show-ref --verify --quiet refs/remotes/origin/quant_news; then
          echo "quant_news branch exists, checking out"
          git checkout quant_news
          git pull origin quant_news
        else
          echo "Creating new quant_news branch"
          git checkout --orphan quant_news
          git rm -rf .
          echo "# Quantitative Trading News" > README.md
          echo "" >> README.md
          echo "This branch contains translated quantitative trading news articles." >> README.md
          echo "" >> README.md
          echo "## Structure" >> README.md
          echo "" >> README.md
          echo "- \`news/YYYY-MM-DD/article-title.md\` - Daily news articles" >> README.md
          git add README.md
          git commit -m "Initial commit for quant_news branch"
          git push origin quant_news
        fi
        
        # 切换回 master 分支进行爬取
        git checkout master
    
    - name: Run news crawler
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        poetry run python scripts/enhanced_news_crawler.py
    
    - name: Commit and push news articles
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        
        # 检查是否有新文章
        if [ -d "temp_news" ] && [ "$(ls -A temp_news)" ]; then
          # 切换到 quant_news 分支
          git checkout quant_news
          
          # 复制新文章
          cp -r temp_news/* . 2>/dev/null || true
          
          # 添加并提交
          git add .
          if git diff --staged --quiet; then
            echo "No new articles to commit"
          else
            git commit -m "Add news articles for $(date -u +%Y-%m-%d)"
            git push origin quant_news
            echo "Successfully pushed new articles"
          fi
        else
          echo "No new articles found"
        fi
```

## 🔑 设置 GitHub Secrets

1. 进入仓库的 **Settings** → **Secrets and variables** → **Actions**

2. 点击 **New repository secret**

3. 添加以下Secret：
   - **Name**: `OPENAI_API_KEY`
   - **Value**: 您的OpenAI API密钥

## 🚀 启用和测试

### 手动触发测试

1. 进入仓库的 **Actions** 页面
2. 选择 **Daily News Crawler** 工作流
3. 点击 **Run workflow** 按钮
4. 选择 **master** 分支并点击 **Run workflow**

### 自动运行

工作流将在每天UTC+8时间上午8:00自动运行。

## 📊 监控运行状态

### 查看运行日志

1. 进入 **Actions** 页面
2. 点击具体的运行记录
3. 查看各个步骤的详细日志

### 检查结果

1. 运行成功后，检查是否创建了 `quant_news` 分支
2. 在 `quant_news` 分支中查看 `news/YYYY-MM-DD/` 目录
3. 检查翻译后的文章内容

## 🔧 故障排除

### 常见问题

1. **OpenAI API错误**
   - 检查Secret中的API Key是否正确
   - 确认OpenAI账户有足够余额

2. **权限错误**
   - 确认GitHub token有足够权限
   - 检查仓库设置中的Actions权限

3. **分支创建失败**
   - 检查是否有推送权限
   - 确认仓库不是fork（fork仓库的Actions有限制）

### 调试步骤

1. 查看Actions运行日志
2. 检查每个步骤的输出
3. 确认环境变量设置正确
4. 验证依赖安装成功

## 📈 预期结果

成功运行后，您将看到：

1. **quant_news分支**：包含所有量化交易相关文章
2. **目录结构**：`news/2025-06-23/article-title.md`
3. **翻译内容**：英文文章自动翻译为中文
4. **元数据**：每篇文章包含来源、链接、时间等信息
5. **统计日志**：处理统计和分析结果

## 🎯 下一步

1. 创建上述工作流文件
2. 设置OpenAI API Key Secret
3. 手动触发测试运行
4. 检查结果并调整配置
5. 等待自动定时运行

---

*注意：首次运行可能需要较长时间，因为需要安装依赖和处理多篇文章。后续运行会更快。*
