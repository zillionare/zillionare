---
name: quant-blog-writing
description: 'Write polished quant trading blog posts with strong taste, clear argument, verifiable evidence, and richer narrative texture. Use for 量化交易博文、因子研究、回测复盘、数据源排错、市场微观结构、策略原理、风险控制、职业观察、量化人物故事等选题。 Produces a concrete angle, article outline, evidence plan, and finished draft that is intellectually honest instead of slogan-driven, while using人物经历、quotes、贡献和行业背景让文章更有读头。'
argument-hint: 'Topic, target reader, and preferred format, for example: 写一篇面向有 Python 基础读者的文章，解释为什么小市值因子在 A 股容易失效'
user-invocable: true
---

# Quant Blog Writing

## Purpose

Create quant-trading-related blog posts that feel informed, restrained, and worth reading.

The skill is for articles that should have judgment and texture, not generic content marketing. It should help produce writing that starts from a real question, respects data and implementation detail, and ends with a conclusion that is narrower and truer than the original ambition.

It should also know how to use human material well: a well-chosen quote, a quant researcher’s hard-won lesson, a fund manager’s mistake, or an ordinary practitioner’s learning arc can make a technical point more memorable without diluting rigor.

Load [repo-style notes](./references/repo-style.md) when you need local conventions.

## When to Use

- The user wants to write a 量化交易、因子、回测、数据接口、策略实现、市场结构、风控、研究职业相关的博文
- The topic is technical but the article should still read like a story, not a notebook dump
- The draft needs a better angle, structure, or voice
- The user wants to weave in quant人物故事, career arcs, or hard-earned lessons to keep readers motivated
- The article would benefit from quotes, historical context, or a notable practitioner’s point of view
- The article must avoid empty判断, exaggerated收益承诺, and shallow “AI generated” phrasing

## Output Contract

Unless the user asks otherwise, produce these artifacts in order:

1. A one-sentence core thesis
2. A reader definition and why the topic matters now
3. A 4-8 section outline
4. An evidence plan: which facts, charts, code, or examples are needed
5. A recommendation for the most suitable local column or category
6. Only after user confirmation, the full draft itself
7. A final quality check with weak spots called out explicitly

Default behavior is outline-first, not full-draft-first.

## Writing Standard

The article should satisfy all of these:

- Starts from a concrete tension, puzzle, anomaly, tradeoff, or misconception
- The first screen should point at the article's real bottleneck, not a generic industry lament
- If the article revolves around specific tools, data sources, or workflows, name the key examples early instead of saving them for later
- Makes at least one falsifiable claim, not only attitude or vibes
- Uses hard logic, structural constraints, data, quantifiable metrics, or market mechanics as evidence rather than loose descriptive prose
- Prefer information density over explanatory padding; cut any paragraph whose main job is to tell the reader why the author chose this angle, structure, or tone
- When a claim can be grounded with numbers, dates, counts, stars, version info, or market scale, do so
- When a workflow claim depends on an external site, product, or standard, state the source in prose and make it easy to verify
- When the topic is practical, include the minimum concrete operating path: what to click, what to search, what to download, where to place it, how to verify it worked
- If screenshots, command output, tables, or concrete UI states would materially reduce ambiguity, plan for them instead of compensating with extra prose
- When recommending tools, skills, vendors, or workflows, prefer the best default choice for the reader rather than an exhaustive catalog
- Benchmark your recommendations using factual leverage (e.g., install scale, backing institutions, core metrics) so that conclusions are structurally unassailable, not just "this tool is neat"
- Add a second option only when the first choice has a clear, material gap and the alternative genuinely fills it
- When explaining setup or installation, distinguish clearly between discovery source, download format, and host-specific install location
- Verify workflow claims against current product docs when the article depends on operational details such as settings, folder paths, or activation behavior
- Uses human texture when helpful:人物经历、行业轶事、研究者分歧、名言、争论、失败教训
- Has visible 起承转合: open on the concrete problem, expand into concept or background, turn into mechanism or example, then close on the practical takeaway
- Distinguishes observation, inference, and speculation
- Keeps the conclusion proportional to the evidence
- Avoids title-clickbait, sermon tone, and empty abstractions like “empower”, “subvert”, “redefine”
- Reads like a practitioner talking to serious readers, not a growth marketer farming attention

## Frontmatter-Aware Metadata Rules

When generating frontmatter-facing values such as title, excerpt, subtitle-like labels, or tag values:

- do not use `:` or `：`
- if a phrase naturally wants a colon, rewrite the phrase instead
- keep `excerpt` within 120 characters total, counting Chinese and English characters together and including punctuation
- prefer short, stable wording over decorative phrasing that risks YAML conflicts

## Narrative Enrichment

Use narrative enrichment deliberately, not decoratively.

Two preferred devices:

### 1. Character arc

Bring in a person when the article needs emotional traction, persistence, or a lived example of how serious work is done.

Good uses:

- a famous quant whose work shaped the field
- an underappreciated practitioner whose discipline or failure reveals something important
- an ordinary researcher, trader, or developer whose learning path mirrors the reader’s own situation

What to extract from the person:

- what problem they were trying to solve
- what constraint or setback they faced
- what habit, method, or intellectual posture made the difference
- what the reader should learn from that example

The point is not hero worship. The point is to turn abstraction into a lived problem.

### 2. Idea anchor

When introducing a concept, viewpoint, or term, anchor it to a memorable external reference when doing so sharpens understanding.

Possible anchors:

- a quote
- a disagreement between respected practitioners
- a short note on who popularized the idea
- a concise mention of a person’s actual contribution to the field
- a historical episode that changed how the concept is used

An anchor should clarify or deepen the point. If it only decorates the paragraph, remove it.

## Procedure

### 1. Define the angle

Convert the raw topic into a sharp question.

Good starting forms:

- “Why does this result look wrong?”
- “What assumption breaks first in live trading?”
- “What does this factor actually buy you, and what does it cost?”
- “Why do two authoritative data sources disagree?”
- “What do most tutorials omit because it is inconvenient?”

If the topic is broad, narrow it by choosing one:

- one market
- one data source
- one failure mode
- one strategy family
- one reader level

### 2. Identify the reader

Pick one primary reader and write for that person only:

- curious beginner with Python basics: ok to explain concepts in accessible terms
- practicing retail quant: focus on local setup, cost, and friction
- junior researcher: focus on robustness, data traps, and edge cases
- experienced practitioner / graduate-level reader: drastically tighten the vocabulary. Rely on structural constraints, hard logic, factual benchmarks (numbers/industry scale), and precise academic/engineering terminology (e.g., Curation, Entropy, Zero-shot, Extrapolation, Engineering fragility). Drop all loose, folksy, or overly colloquial "chatty" analogies (大白话). 

Adjust depth accordingly. Do not mix beginner hand-holding with expert shorthand in the same section.

### 3. Build the argument before writing prose

Draft these internal notes first:

- What is the claim?
- Why might an informed reader disagree?
- What evidence would change that reader’s mind?
- What part remains uncertain even after the analysis?
- Which human story or external viewpoint would make this argument more vivid without turning it sentimental?
- Which concrete tools, datasets, APIs, or workflow objects are doing the real work in this article, and can the opening name them immediately?
- Which recommendation is the strongest default for this reader, and is there any real need to mention a second-best or complementary option?

If you cannot answer these, do not write the full article yet. Strengthen the angle first.

### 3.5. Design the first screen

Before writing the opening paragraphs, decide what the reader should encounter on the first screen.

- Start from the actual pain point or operational constraint, not from a broad thesis about the whole industry
- If the article mainly discusses a few representative tools or data sources, bring them into the opening instead of holding them back for the middle
- Make the first paragraph do at least two jobs: identify the concrete problem and hint at why the rest of the article is worth reading
- Avoid throat-clearing that could fit any topic; the opening should feel impossible to detach from this specific article

### 4. Choose the article shape

Use one of these structures.

#### A. Mystery to explanation

Best for data anomalies, backtest surprises, pricing inconsistencies, and implementation bugs.

Flow:

1. Present the odd result
2. Show why the obvious explanation is insufficient
3. Test competing explanations
4. Reveal the actual mechanism
5. End with the practical implication

#### B. Claim to decomposition

Best for factor research, strategy myths, capacity, and risk discussions.

Flow:

1. State the popular claim
2. Break it into components
3. Evaluate each component separately
4. Reassemble with a narrower conclusion

#### C. Narrative essay with technical spine

Best for人物、职业路径、研究方法、行业观察.

Flow:

1. Open with a scene, quote, or specific episode
2. Introduce the core tension
3. Use one or two concrete technical details to anchor credibility
4. Expand into the broader lesson
5. Finish with a restrained, memorable close

#### D. Technical article with human anchor

Best for concepts that are correct but dry, such as execution assumptions, factor construction, model risk, or research workflow.

Flow:

1. Open with the technical tension
2. Introduce the concept cleanly
3. Bring in a practitioner, quote, or episode that sharpens the stakes
4. Return to the mechanism, evidence, or code
5. End with both the practical takeaway and the human lesson about craft

### 5. Gather evidence

Match the topic to the minimum evidence required.

- Data-source article: table, field definition, comparison example, edge case
- Factor article: universe definition, rebalance rule, costs or crowding caveat, failure regime
- Strategy article: trigger condition, execution assumption, slippage/latency constraint, risk control
- Career/opinion article: one concrete anecdote, one technical example, one non-obvious insight
- Motivational or人物 article: one concrete setback, one turning-point decision, one durable habit or method, one takeaway that respects reality rather than selling optimism
- Tooling / workflow article: concrete platform facts, at least one sourceable metric or count, one verification path, one install or usage example, and screenshots or visual placeholders when UI steps matter

If the article compares tools, skills, or data sources:

- do not enumerate everything you found just because it exists
- choose the best default recommendation first and justify why it wins for this reader
- mention a second or complementary option only if it clearly covers a concrete shortcoming in the first choice
- avoid repeating documentation-level feature lists unless the article's point depends on that detail
- keep the focus on what the reader would not get from reading the official docs alone

If the article is revising or tightening an existing draft:

- remove throat-clearing and self-justifying transitions first
- compress any paragraph that restates the same claim without adding new evidence
- prefer one sentence with a number or source over three sentences of abstract framing
- keep only the conceptual background needed for the reader to execute the next step or understand the recommendation

If the article includes installation or usage instructions for portable skills across multiple hosts:

- separate marketplace discovery from actual installation
- state which steps belong to Skills Marketplace and which belong to VS Code, Claude Code, Codex CLI, or another host
- do not infer install paths from a repository convention unless the host documentation confirms it

If a claim depends on code, include only the code needed to make the point. Prefer short, inspectable snippets over long notebooks.

If you cite a quote, contribution, or historical anecdote, verify the wording and attribution before presenting it as fact.

### 6. Write section by section

For each section:

- lead with the point of the section
- give evidence or mechanism
- optionally add a person, quote, or field contribution if it deepens the section’s meaning
- close with what the reader should update their belief to
- do not give a familiar tool, API, or library its own section unless that section advances the article's core argument rather than restating its documentation
- do not spend sentences narrating the author's writing process, justification, or rhetorical intent unless that meta-level itself is the subject

Prefer dense, clean paragraphs. Use lists only when comparison or procedure matters.

### 7. Control the tone

Target tone:

- calm and structurally rigorous
- exact in terms of metrics, system constraints, and logic
- intellectually dense when targeting advanced readers (prefer cold, professional academic/engineering vernacular)
- mildly witty when earned
- skeptical of easy conclusions and "silver bullets"
- generous to the reader’s intelligence (explain the mechanism, skip the hand-holding)
- quietly encouraging about the long game of learning

Avoid:

- overly conversational/colloquial "chatty" transitions (泛泛之谈 / 大白话)
- exaggerated certainty or generic AI praising (e.g., "AI empowers everything")
- fake intimacy ("你是不是也遇到过...")
- inflated moral language
- pretending a toy backtest proves a durable edge
- cheap inspiration that ignores how hard the work actually is

### 8. Finish with an honest ending

End on one of these notes:

- what changes in practice because of this finding
- which assumption the reader should re-check in their own work
- what remains unresolved
- why the problem is more subtle than it first looked

Do not end with “希望对你有帮助” style filler unless the user explicitly wants that tone.

## Decision Rules

Use these branches while drafting.

- If the topic is highly technical, privilege correctness over lyricism
- If the topic is conceptual, add one concrete market or implementation example to avoid floating abstractions
- If the opening sounds like it could introduce ten different articles, rewrite it until it names this article’s actual constraint, dataset, toolchain, or conflict
- If later sections are carried by a few concrete examples, pull those examples earlier so the reader sees the article’s true subject on the first screen
- If a recommendation section starts turning into a directory listing, cut it down to the best default choice and one justified backup at most
- If a section mostly repeats what the official docs already say, compress it and move the emphasis back to selection, workflow, installation, or practical use
- If a paragraph explains why the article is written a certain way rather than delivering facts, judgment, or procedure, cut it
- If the piece would be stronger with one screenshot, count, link, or command than with another paragraph of framing, choose the artifact
- If the article feels dry, add one human anchor: a quote, an anecdote, a disagreement, or a biographical detail tied to the exact point being made
- If the article turns preachy, replace motivation with specificity: habit, process, mistake, or constraint
- If using a famous name, explain the exact relevance instead of name-dropping
- If the article risks sounding absolute, add scope conditions and failure cases
- If the draft becomes tutorial-like, reinsert tension by asking what is surprising, costly, or controversial here
- If the article has strong opinions, make the strongest opposing case before concluding

## Character And Quote Guidelines

When bringing in人物、quotes, or contributions:

- prefer relevance over fame
- prefer one sharp reference over a parade of names
- explain why this person belongs in this paragraph
- connect the quote or story back to market structure, research practice, execution, or intellectual discipline
- use ordinary practitioners too when their arc is closer to the reader’s real constraints

Do not:

- use fabricated quotes
- use vague admiration in place of analysis
- reduce a person’s work to a motivational poster
- turn the article into biography when the article’s real subject is technical

## Quant-Specific Checks

Before finishing, verify that the draft does not:

- confuse signal quality with executable PnL
- ignore transaction cost, delay, borrow, liquidity, or regime dependence when they matter
- treat vendor fields as self-evident without checking definitions
- smuggle in survivorship, look-ahead, or selection bias
- generalize from one market structure to all markets
- use a quote, anecdote, or historical reference whose attribution is shaky

## Final Review Checklist

Run this check explicitly:

1. Is the title precise and intriguing without overpromising?
2. Does the first screen contain a real problem, not background throat-clearing?
3. Does the opening name the concrete tools, datasets, APIs, or workflow objects that the article is actually built around when they are central to the piece?
4. Can each major claim be tied to evidence or mechanism?
5. Is the article’s 起承转合 visible, with each section clearly handing off to the next rather than piling up observations?
6. Is any paragraph saying the same thing twice?
7. Does the article recommend the best default option instead of burying the reader in an undifferentiated list?
8. Are any sections just paraphrasing docs when they should instead emphasize judgment, workflow, installation, or use?
9. Where is the draft most likely wrong or incomplete?
10. Would a serious quant reader learn at least one non-obvious thing?
11. If the article uses人物或quotes, do they genuinely sharpen the point rather than decorate it?
12. Do generated frontmatter values avoid `:` and `：`, and does the `excerpt` stay within 120 characters including punctuation?
13. Does the draft contain enough hard information to be useful on its own: numbers, source cues, concrete steps, commands, or visual evidence?
14. Is any paragraph mostly explaining the author's framing rather than advancing the reader's understanding or execution path?

If the answer to 9, 10, 11, 12, 13, or 14 is weak, revise before presenting the article as finished.

## Local Publishing Convention

If the user wants the article written into the repository, draft it under `docs/_drafts/` first unless they explicitly request direct publication elsewhere.

Choose the eventual destination by topic:

- technical investigations usually map to `docs/blog/posts/algo/`
- research commentary may map to `docs/blog/posts/papers/`
- broader essays may map to `docs/blog/posts/others/` or another user-specified section

## Default Deliverable Format

When the user asks to “write” but gives little structure, respond in this order:

1. Proposed angle
2. Thesis
3. Outline
4. Evidence and material checklist
5. Suggested draft filename and destination under `docs/_drafts/`

Only write the full article immediately if the user explicitly asks for the full draft in the same turn.

## Examples of Good Prompts

- 写一篇有判断力的量化博文，解释为什么很多日频因子一实盘就失灵
- 写一篇从数据接口差异切入的文章，读者是会 Python 的个人投资者
- 围绕“回测时间越长越好吗”写一篇不是鸡汤的文章
- 把一个策略踩坑经历改写成适合博客发布的文章，保留代码细节
- 写一篇技术文章，解释一个量化概念时顺带穿插两位研究者的观点和贡献
- 写一篇关于普通量化从业者如何持续学习的文章，不煽情，但要让读者更愿意长期投入
