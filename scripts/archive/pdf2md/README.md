# PDF → Markdown 高保真转换（已归档）

> **状态：已归档（2026-10）。** 论文翻译主路径已切换为 pdf2zh
> （原位翻译、公式/版式/图表保留，见根 `pyproject.toml` 与
> `scripts/qa_pdf2zh.py`）。本目录是自研"页级视觉转写"路线的完整快照，
> 保留价值：
> - **可复用的技术**：双栏切分（栏界+质量门槛）、跨页重复行检测
>   （页眉/页码自动涂白）、图表涂白 + token 注入（截图替代转写）、
>   区域重叠/跨块重复检测——未来若做高保真 Markdown 提取可直接取用；
> - **锁定的判据**：`test_verify_rules.py` / `test_layout_rules.py`
>   用双向验证把误报/漏报阈值钉死，防止回归。
>
> 运行条件：Python ≥3.9 + PyMuPDF，配置见 `pdf2md.env.example`；
> 依赖与本文档其余说明仍然有效。

## 目录与依赖

```
scripts/pdf2md/
  pdf2md.py              主程序：版面解析 → 渲染 → VLM 转写 → 校验 → 复核
  tables_figures.py      表格/图的几何抽取（pdf2md.py 依赖，必须同目录）
  pyproject.toml         依赖声明（仅 pymupdf），可独立建环境
  requirements.txt       同上，pip 传统格式
  pdf2md.env.example     配置模板，复制为 pdf2md.env 后填入
  test_verify_rules.py   校验判据的双向验证（假阳性/漏报）
  test_layout_rules.py   版面/重复检测的回归测试（合成数据，无需 PDF）
  README.md              本文件
```

本目录自带依赖声明，**拷走即可重建环境**，不依赖上层仓库：

```bash
cd scripts/pdf2md
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt      # 或 pip install pymupdf>=1.24
cp pdf2md.env.example pdf2md.env    # 填入端点配置
python pdf2md.py <paper.pdf> -o out/
```

`pyproject.toml` **刻意不声明 `[build-system]`**——本目录是脚本而非可安装包，
声明它会强制 pip 先联网装 setuptools/wheel 才能装本包，在离线或受限网络下
反而装不成。依赖信息放在 `[project].dependencies` 里供工具读取。

**只有 PyMuPDF 一个第三方依赖。** LLM 调用走标准库 `urllib`，
不引入 `requests` / `openai`，Python ≥ 3.9（3.13 实测无警告）。

### 配置

配置只从**本目录**读 `pdf2md.env` 或 `.env`（不向上查找仓库根——
那会让配置来源随工作目录变化，不可预测）。要用别处就 `--env <path>`
或设 `PDF2MD_ENV`。

需要的键：

```
LLM_LOCAL_URL  LLM_LOCAL_API_KEY  LLM_LOCAL
LLM_SMART_URL  LLM_SMART_API_KEY  LLM_SMART
SMART_FALLBACKS=model-a,model-b      # 可选，复核模型限流时的轮换顺序
```

两个端点都须是 OpenAI 兼容的 `/v1/chat/completions`，且模型支持
`image_url` 类型 content（视觉输入）——**公式识别完全依赖看渲染图**，
不支持视觉就整条链路失效。

## 两条链路

| | `tables_figures.py` | `pdf2md.py` |
|---|---|---|
| 方法 | 解析 PDF 字符流 + 几何聚类 | 渲染区域 → 视觉模型转写 |
| 覆盖 | 表格、图、外链 | 正文段落、display 公式、行内公式 |
| 数学字体 | 不涉及 | **不需要字形映射** |

早期版本把公式也交给几何装配（`is_formula_char` 认 CMMI/CMSY/CMEX，
`BIG_OPS` 查 CMEX 大运算符）。实测 5 篇论文里有 4 篇识别出 **0 个公式**——
四类数学字体的编码约定完全不同，逐字族建表不可持续。现版本不再做字形映射。

## 用法

```bash
# 从仓库任意位置均可运行（.env 会自动向上查找）
python scripts/pdf2md/pdf2md.py <pdf> -o <outdir>
```

常用参数：

- `--max-pages N` 只转前 N 页（正文自动截止到 References 之前）
- `--dpi 260` 渲染分辨率，默认 260；公式复杂时可提到 320
- `--no-review` 关闭 smart 复核，只用 local 模型（快，但静默错误风险高）
- `--local-model` / `--smart-model` 指定模型
- `--env <path>` 指定配置文件；也可用环境变量 `PDF2MD_ENV`
- `--review-only` 不跑转换，仅从已有 `meta.json` 重新生成复核清单

退出码：`0` 成功 / `2` 环境配置缺失 / `3` 依赖模块缺失。
两者都在开跑前检查，不会白转一遍。

### 存疑提示与人工复核

**程序不会把存疑块静默塞进正文。** 转换结束会产出 `review.md`：

```
<outdir>/review.md              复核清单（只在有存疑块时生成）
<outdir>/review_shots/*.png     每个存疑块的原图裁切
```

清单按严重程度排序，每项给出**原图裁切 + 模型实际输出 + 自动检出的疑点**，
所以核对时不必打开原 PDF，对着图看 LaTeX 即可。

分级依据「错了会不会误导读者」：

| 级别 | 疑点 | 含义 |
|---|---|---|
| **critical** | `HALLUCINATED_SYMBOL` | 公式含原文没有的字母——可能是幻觉符号 |
| | `MISSING_DISPLAY` / `MISSING_MATH` | 公式没被转写出来 |
| | `PROSE_HALLUCINATION` | 模型写了原文没有的词 |
| | `PROSE_LOSS` | 原文词保留不足一半——内容大量漏写 |
| | `REASONING_LEAK` | 模型输出的是推理过程而非转写 |
| | `ERROR` | 转写调用失败 |
| | `OVERLAPPING_REGION` | 两个转写区域的框重叠——内容可能重复 |
| | `DUPLICATE_CONTENT` | 同一段文字出现在多个块里（且原文只出现一次） |
| warn | `PROSE_MISMATCH` | 原文词召回率偏低，可能漏写 |
| | `REPEATED_IN_SOURCE` | 同一段文字多处出现，但**原文本身即如此**，无需处理 |
| | `REPETITION` | 模型复读，内容冗余但多半可用 |
| | `TRUNCATED_OUTPUT` / `REVIEW_FAILED` | 截断或复核未完成 |

**公式错不可接受，所以凡涉及公式的疑点一律 critical。**
实测存疑块约占 5%，其中 critical 约占 1/5——人工核对的工作量就是这个量级。

后两项（`OVERLAPPING_REGION` / `DUPLICATE_CONTENT`）是**版面级检测**，
不依赖模型的自省能力，专抓「同一片内容被转写两次」这类结构性缺陷。
触发时 `review.md` 顶部有「文档级异常」小节，列出重复片段原文，
两处对照即可删除多余的一份。`meta.json` 的 `doc_issues` 字段是机器可读版本。

改过分级或报告格式后，可只重出报告不重跑模型：

```bash
python scripts/pdf2md/pdf2md.py <pdf> -o <outdir> --review-only
```

也可以查 `meta.json` 的 `review_counts` 字段拿机器可读的计数。

> `--review-only` 复用 `meta.json` 里**已存的**判定结果，不会用新判据重算。
> 若改了校验逻辑，要验证效果需清缓存重跑（或至少重跑受影响的块）。

### 校验判据的回归测试

校验阈值不是拍的，改动必须有测试兜着，否则会悄悄退化：

```bash
python scripts/pdf2md/test_verify_rules.py     # 校验判据（假阳性/漏报）
python scripts/pdf2md/test_layout_rules.py     # 版面/重复检测
```

`test_verify_rules.py` 对 `MISSING_MATH`（漏公式）判据做**双向**验证：

- **假阳性**：纯散文被判成含公式 → 每次误报都占掉一次人工核对
- **漏报**：真公式被判成不含公式 → **公式错了都不知道**，更严重

当前 9 假阳性样本 + 8 灵敏度样本全过。

`test_layout_rules.py`（纯合成数据，不依赖仓库 PDF）覆盖两个曾产生
实际缺陷的判据：栏探测（单栏页不得被行尾碎片误判为双栏）、
区域重叠与跨块重复检测（必须检出、且不误报）。

改判据时务必同时更新测试，并注意别把两份正则写成两份拷贝
（之前就踩过：实现改了、测试里的拷贝没改，测试假通过）。

### 批量处理

```bash
for pdf in originals/*.pdf; do
  name=$(basename "$pdf" .pdf)
  python scripts/pdf2md/pdf2md.py "$pdf" -o "extracted/$name" --dpi 260 \
    > "extracted/$name.log" 2>&1 &
done
wait
```

单篇 8–30 页耗时 10–35 分钟（取决于 smart 复核次数）。
**并发别超过 2–3 篇**——本地模型端点是单进程串行的，并发 5 篇会互相排队。
结果按块缓存到 `<out>/.vlm_cache/`，中断后重跑只补未完成的块。

## 稳定性

已在 5 篇不同排版、不同数学字体的论文上验证（合计 481 块，95% 通过）。
**这不是"零失败"，用之前要知道三件事**：

1. **校验不通过的块内容通常是对的**，只是判为"不可信"。`MISSING_MATH`
   多为误报（段落有数字和关系符但实际无公式）；`PROSE_MISMATCH` 多因双栏
   切分后段落天然不完整。真正需要人工看的只有 `HALLUCINATED_SYMBOL`。
2. **概率性输出**。同样输入不保证逐字一致（temperature 0 也只是近似确定）。
   缓存保证重跑一致，但换环境重跑可能有细微差异。
3. **未经更大样本检验**。5 篇是动量因子这一类（双栏学术论文），
   遇到扫描件、书籍排版、含大量代码/伪代码的论文会有未覆盖的情况。

## 流水线

```
PDF ─┬─ 版面几何（字体无关）
     │   ├─ 脚注/页眉分隔线 → 正文带
     │   ├─ 行合并 → 段落（按栏左边距判段首缩进，支持双栏）
     │   ├─ 独占窄带 + 式号锚点 → display 公式块
     │   └─ 成片等距数值行 → 表格行（从公式候选中排除）
     │
     ├─ 逐块渲染（dpi 260，长段落纵向切半）
     │   └─ local VLM 转写 → Markdown（含 $...$ / $$...$$）
     │
     ├─ 校验（只用 PDF 字符，与字体无关）
     │   ├─ 散文精确率 < 0.80 → 编造
     │   ├─ 散文召回率 < 0.72 → 漏写
     │   ├─ 公式字母多重集 ⊄ 原文 → 幻觉符号
     │   ├─ ≥12 词片段重复 → 模型复读
     │   ├─ 思考泄漏检测
     │   └─ 原文有数学结构但无公式输出
     │
     ├─ 任一校验失败 → smart 模型带疑点复核（模型池自动轮换）
     │   └─ 复核结果与 local 结果按校验分择优
     │
     └─ 拼装：跨页续接合并 + 表格/图/链接汇总
```

## 设计要点

**为什么用渲染图而不是 PDF 字符流。**
数学字体各家不同：CM 系（CMMI/CMSY/CMEX）、Adobe 字体集（AdvGulliverMath-I、
AdvMacMthSyN）、MathTime（MTSY/RMTMI）、以及 Crashes 那篇的���定义单字母字族
（FB/FC/FE/FF/Ft/Fv/Fw/Fy）。逐字族建映射表不可持续，而字形在渲染图里是确定的。
实测：Crashes 的 display 公式 `\tilde r^e_{i,t} = \beta_0\tilde r^e_{m,t} + \cdots`
在 PDF 字符层几乎不出现（`has_math` 返回 False），但图上清清楚楚。

**display 公式不是独立 block。**
PyMuPDF 会把 eq4 切成 6 个 block，其中 4 个是求和限位碎片
（`T−1`、`P`）。依赖 block 完整性的方案必然失败，必须按几何聚合。
可靠的判据是「独占」：display 公式整行独占排版，行内公式总与正文并排。
宽度不是必要条件——接近栏宽的 display 公式很常见。

**校验器的灵敏度是标定出来的，不是拍脑袋。**
注入式对照：取真实输出，人为植入 4 类已知错误（幻觉符号 / 漏写散文 /
丢公式 / 虚增公式），要求全部被判FAIL。首轮 12/12 全漏，暴露三个 bug：
`overlap` 只算了精确率没算召回率（砍文本后恒为 1.0）；`+1` 容差放过真幻觉；
`LOST_MATH` 只处理 `$$` 而实际输出多用行内 `$`。修复后 12/12 全部捕获。

**静默错误是最危险的。**
VLM 会自信地编出 `\overline{RV}`（真式是 `(RV_{i,t}-1)(RV_{i,t}-\frac{\cdots}{...})^2`）。
这种错误比明显的乱码危险——下游翻译会照着错公式写，且看不出来。
字符多重集校验能兜住这类：原文没有的字母必然是编的。

## 剩余失败的主因

- `MISSING_MATH`（9）：段落里有数字和关系符但实际无公式，判据偏保守 → 触发一次
  无谓的 smart 复核，不产生错误内容，只是慢。
- `REPETITION`（8）：local 模型在长段落上偶发自我复读。已加超长段落切分
  （>185pt 按行间隙递归二分）与复读检测纳入校验，剩余的是切分后仍超长的块。
- `PROSE_MISMATCH`（4）/ `NO_PROSE`（3）/ `HALLUCINATED_SYMBOL`（4）：
  双栏切分后的召回率偏差、表格/公式走错通道、以及真正的公式幻觉。

**这些块的内容本身多��正确**（校验判为"不可信"而非"确定错误"），
真正需要人工复核的是 `HALLUCINATED_SYMBOL` 那 4 个。

## 已知限制

- **Crashes 的 display 公式定位为 0。** 该篇 NBER 版式的公式与表格紧邻，
  表格检测把它们一起排除了。公式仍以行内形式出现在正文段落里（VLM 转写正确），
  但没有独立的 `$$` 块。
- **ValMomEverywhere 的图表未抽取**（legacy 链路对 MathTime 版式不匹配）。
  该篇表格/图片仍在 PDF 原文里，需要补一条抽取路径。
- **只处理英文正文。** 正文截止于 References 标题页，参考文献不转写。
- **概率性输出。** 同样输入不保证逐字一致（temperature 0 也只是近似确定）。
  缓存按 `(pdf, 页, 块类型, 坐标, 提示词)` 哈希落盘，保证重跑一致。

## 复现方式

```bash
python scripts/pdf2md/pdf2md.py \
  docs/assets/2026/30-quant-papers-module2/originals/<paper>.pdf \
  -o /tmp/out/<name> --dpi 260
# 输出：/tmp/out/<name>/paper.md, meta.json, assets/*.png, .vlm_cache/
```

## 缓存

每次转写的结果按 `(pdf, 页, 块类型, 坐标, 提示词)` 哈希落盘到
`<outdir>/.vlm_cache/*.json`。重复运行只重算未命中的块；
改提示词会自动让旧缓存失效（哈希含提示词全文）。

## 实测结果

local = qwen-3.6-crack（MLX），复核池 = deepseek-v4.1-flash / mimo-v2.6-flash /
space-bunny / kimi-k3，dpi 260。「块」= 一次VLM 调用的粒度（段落或 display 公式）。

| 论文 | 数学字体 | 正文字数 | 块数 | 校验通过 | 复核次数 |
|---|---|---|---|---|---|
| Momentum-Has-Its-Moments | CMR/CMMI/CMSY/CMEX | 27KB | 69 | 69 (**100%**) | 0 |
| Momentum_turning_points | Gulliver/MTSY/RMTMI | 99KB | 167 | 154 (92%) | 26 |
| Momentum-Crashes | 自定义 FB/FC/FE/FF/Ft/Fv/Fw/Fy | 40KB | 68 | 66 (97%) | 4 |
| ValMomEverywhere | MTSY/NewCenturySchlbk | 40KB | 60 | 58 (97%) | 4 |
| TimeSeriesMomentum | AdvGulliver/AdvMacMthSyN | 68KB | 117 | 108 (92%) | 19 |
| **合计** | | | **481** | **455 (95%)** | 53 |

四类数学字体的论文全部跑通——包括 Crashes 那篇连字形映射都无法建立的自定义字族。
对照组：字形映射方案在这 5 篇里有 4 篇识别出 0 个公式。

最难的两个公式（嵌套分数 + 求和限位，几何方案长期做不对）：

```latex
R^2_{i,OOS} = 1 - \frac{\sum_{t=S}^{T-1}
    (\widehat{\alpha}_t + \widehat{\rho}_t RV_{i,t} - RV_{i,t+1})^2}
    {\sum_{t=S}^{T-1}\cdots}

\text{Sharpe } [r_{\text{SLOW,t}}] =
  \frac{\sqrt{24/\pi}\,(1-\theta)\varphi}
       {\sqrt{(1-\theta)[12(1-\varphi)^2\cdots]}}
```

图表保留情况：

| 论文 | 表 | 图 | 图文件 | 外链 | md |
|---|---|---|---|---|---|
| Momentum-Has-Its-Moments | 6 | 6 | 6 | 0 | 29KB |
| Momentum_turning_points | 9 | 9 | 9 | 86 | 94KB |
| Momentum-Crashes | 7 | 0 | 0 | 0 | 40KB |
| ValMomEverywhere | 0 | 0 | 0 | 59 | 40KB |
| TimeSeriesMomentum | 5 | 5 | 5 | 1 | 68KB |

Crashes 是 NBER 工作论文版式（无图表、无超链接），ValMom 的图表走 legacy
抽取链路未命中（MathTime 版式），两者待补。

复杂公式转写正确的例子（Gulliver 字族，几何方案完全做不到）：

```
$$ \text{Sharpe } [r_{\text{SLOW,t}}] = \frac{\sqrt{24/\pi}(1-\theta)\varphi}
                                        {\sqrt{(1-\theta)[12\pi]^{-1} + \cdots}} $$
$$ \mathbf{E}[r_{\mathrm{FAST},t} \mid \mu_{t-1}, \mu_{t-2}]
   = \varphi \mu_{t-1} \cdot \left[ 2\Phi\!\left( \frac{\mu_{t-1}}{1-\varphi} \right) - 1 \right] $$
```

## 版面陷阱清单（都已处理，记录以免重蹈）

1. **display 公式不是独立 block。** PyMuPDF 把 eq4 切成 6 个 block，其中 4 个是求和限位碎片。任何依赖 block 完整性的方案都会失败。
2. **双栏必须先分栏再聚行。** `to_rows` 会把左右栏同一 y 的行并成一行；先合并再分栏会得到 3000+ 字符的"段落"。TimeSeriesMomentum p2 原本 3255 字符/页，修后降到 800。
3. **段首缩进要与栏左边距比，不是与上一行比。** 后者会被行内公式碎片的 x 偏移误触发，把段落从中间切断。
4. **图内框线会被误认成脚注分隔线。** TimeSeriesMomentum p7 的 Figure 1 有两条 206pt（页宽 544，38%）的线位于页面中部，只看宽度会把 y>466 的正文整片丢掉。脚注线要求 >=45% 页宽**且**位于页底 12%。
5. **图注与正文字号交错。** turning_points p14 的 8.0pt 正文与 6.4pt 图注在 y=662/667/673/676 交替——只看"连续小字号"仍会误判。要用行间距的连续性 + 排除区行数上限。
6. **Crashes 的公式不出现在文本层。** `\tilde r^e_{i,t} = \beta_0\tilde r^e_{m,t} + \cdots` 在字符流里几乎不可见（`has_math` 返回 False），只有渲染图能读出来。任何基于文本层的公式检测在该篇上失效。
7. **接近栏宽的 display 公式很常见。** eq1 的 `rWML,t = 1.752 - 0.378 rRMRF,t ...` 占 353pt/栏宽 417pt。宽度阈值会把它们漏掉——判据应是"独占一行"而非"窄"。
8. **单个行尾碎片能让单栏页被误判成双栏。** 栏探测原来看「不同 x 起始点的众数峰」，
   而 PDF 会把行内公式的行拆出**行尾碎片**（mhim p4 的 `An autoregression of monthly`
   以 x0=348 独立成 line，len=26）。它形成一个远离主栏的 x0 峰，页被判为双栏，
   碎片被当成"右栏"单独聚段转写 → 产出与正文重复的垃圾块。
   修法：第二栏要有**质量门槛**（实测真第二栏最少 5 行，碎片堆最多 2 行，取 `max(5, 15%)`）。
   安全网：`_annotate_overlaps` 检测转写区域框重叠，`_find_duplicate_blocks` 检测跨块重复文本，
   两者都会把问题块送进 `review.md`。
9. **切分子块的边界不能被两边的裁剪图同时看到。** `_split_long_para` 切长段落时，
   子块边界若重叠（旧实现重叠 4pt），加上渲染两侧各 5pt padding，两张裁剪图
   的重叠区达 14pt——**超过一行文字的高度**，边界行被转写两次
   （实测 mhim p1 致谢脚注因此重复了 25 词）。修法：两个子块 box 之间留 6pt
   空隙（`cut-3` / `cut+3`），渲染后重叠仅 4pt，不足一个字高。
10. **未完的脚注块不能参与跨页合并。** 页底脚注常被模型截断在标记处（如 `<sup>4</sup`），
    若按「未完句 + 下段小写开头」规则合并，会把它与下一页正文缝在一起
    （实测 `<sup>4</sup three months. Even the large returns...`）。
    修法：`_join_page_breaks` 对以 `<sup>`/`^N`/`N 大写` 开头的块拒绝合并。

## 剩余失败的主因

`PROSE_MISMATCH` 为主：双栏切分后栏底/栏顶段落天然被切断（首词是残词、尾词在另一栏），
召回率偏低。已对首词为小写残词的块放宽阈值到 0.55，且对 <12 词的短块（标题/标签）
跳过散文比对。这些块内容本身正确，只是校验判为不可信。