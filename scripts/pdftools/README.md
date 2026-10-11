# quant-papers 工具链

30 篇论文课程项目的生产工具。翻译链路已一锤定音：**pdf2zh（保版式，
公式/图表原位，只出 mono 中文版）**。自研重排链路已废弃并归档到
仓库 `scripts/archive/pdf2md/`（git 已提交）。

## 翻译链路（唯一入口：`run_pdf2zh.py`）

### 一次性安装

```bash
# 1) 用 uv 装 pdf2zh（隔离环境，不污染 conda；可执行在 ~/.local/bin/pdf2zh）
uv tool install --python 3.12 pdf2zh \
    --index-url https://mirrors.aliyun.com/pypi/simple/

# 2) 修 pdf2zh 1.9.11 的依赖 bug：新版 tencentcloud-sdk-python-tmt（3.1.x）
#    删除了 TextTranslateRequest，导致启动即 ImportError
uv pip install --python ~/.local/share/uv/tools/pdf2zh/bin/python \
    'tencentcloud-sdk-python-tmt<3.1' \
    --index-url https://mirrors.aliyun.com/pypi/simple/
```

### 批量翻译

```bash
python3 scripts/pdftools/run_pdf2zh.py                # 默认：originals 中尚无译文的论文
python3 scripts/pdftools/run_pdf2zh.py --dry-run      # 只打印命令
python3 scripts/pdftools/run_pdf2zh.py TimeSeriesMomentum --ignore-cache   # 强制重译
```

特性：从仓库 `.env` 读取 `LLM_SMART_*`（容错等号空格），映射为
`OPENAILIKED_*`；自动加载术语表 `docs/assets/2026/pdf2zh-prompt.txt`；
产物 `translations/<名>/zh.pdf`（mono 重命名），dual 版直接删除；
逐篇日志 `/tmp/pdf2zh_<名>.log`。

### 质量核查

```bash
python3 scripts/pdftools/qa_pdf2zh.py <translations 目录>   # 主质检
```

四项：归属（页数 vs 原文，抓装错论文）、真实性（中文占比，NFC 归一化）、
完整性（空白页）、公式保全（数学符号量级）。
`scripts/pdftools/verify_translation.py <原文> <译文>` 为备用核查（逐页矢量绘图对比、
图表占位符对比），其"未翻译长英文行"检查对逐字文本层有盲区，仅参考。

### 已踩过的坑

| 问题 | 现象 | 解决 |
|---|---|---|
| 腾讯云 SDK | `ImportError: TextTranslateRequest` | 见上文安装第 2 步（钉 `<3.1`） |
| 版面模型下载 | 首次运行卡住/失败 | `HF_ENDPOINT=https://hf-mirror.com`（run_pdf2zh.py 已内置） |
| `.env` 格式 | 等号带空格 bash `source` 报错 | `run_pdf2zh.py` / `dotenv_run.py` 用容错解析 |
| 输出目录 | 不存在时报 FileNotFoundError | 脚本已先 `mkdir -p` |
| 耗时 | 23–57 页约 20–35 分钟（muse-spark 本地网关） | 后台运行；有缓存，重跑很快 |

### 已知短板（可用 `--prompt` 继续改善）

- ValMom 类旧排版：整页旋转的表格**保留英文不翻译**（字符位置与原文一致，
  视觉无损）——符合"表格不要求翻译"的定位
- 章节标题偶有不译；部分脚注漏译

## 保留工具

| 脚本 | 用途 | 状态 |
|---|---|---|
| `run_pdf2zh.py` | 批量翻译（当前维护入口） | 在用 |
| `dotenv_run.py` | 解析仓库 `.env` 并以其执行子命令 | 在用 |
| `extract_pdf.py` | 从 PDF 裁剪图表截图（导读配图候选） | 备用 |
| `contact_sheet.py` | 图表截图联络图（人工目检） | 备用 |
| `merge_figures.py` | 工作论文版图文合流（[Insert Fig.X] → 文末图表截图，生成 zh-flow，可选） | 备用 |
| `verify_translation.py` | 备用译文核查 | 备用 |

## 交付物（每篇论文）

```
docs/assets/2026/30-quant-papers-module2/
  originals/<名>.pdf            英文原文
  translations/<名>/zh.pdf      中文译文（仅 mono；按决策不做对照版）
  code/<名>.ipynb               复现代码
docs/posts/2026/10/momentum-series/*.md   导读文章（模块二 7 篇）
```

## 已删除记录

- **2026-10-11**（本目录）：`pdf_to_markdown.py`、`translate_markdown.py`、
  `md_to_pdf.py`、`pdf2md_vlm.py`、`README_pdf2md_vlm.md`、
  `batch_translate.sh`（指向已删除的 /tmp venv 与旧目录结构）。
  自研链路最新副本在仓库 `scripts/archive/pdf2md/`，git 已提交。
- **2026-10-08**：`translate_paper.py`、`llm_client.py`、`extracted/`（14MB）。