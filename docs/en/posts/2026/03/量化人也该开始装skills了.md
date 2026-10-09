---
title: "Skills Marketplace: Installing AI Tools for Quant Workflows"
date: 2026-03-26
slug: en/posts/uncategory/量化人也该开始装skills了
tags: [Quantitative Investing, AI Skills, A-Shares, Automated Trading]
excerpt: "Skills Marketplace lets quants integrate A-share context from Tushare and XtQuant into AI workflows, offering more value than simple prompts."
lang: en
translation_of: posts/uncategory/量化人也该开始装skills了
auto_translated: true
source_sha: 7a517946a464d8fc9f4bd99f4e742952fbd56f48
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skillsmp.png"
---

In the AI era, developing strategies as an individual quant seems simpler: you can ask AI to hand-code a momentum strategy or explain multi-factor neutralization.

However, the core dilemma for individual quants often lies in the "last mile" of data acquisition. Data sources that are affordable often come with arbitrary API naming, outdated or incomplete documentation. This non-standardized infrastructure makes coding precarious for humans, and even top-tier large language models like Claude struggle without the correct context.

Skills are the solution, packaging this context into reusable capabilities.

I recently reviewed [skillsmp.com/zh](https://skillsmp.com/zh) and found it has evolved beyond a "programmer toy market." It now hosts a growing collection of skills directly relevant to finance, investing, and especially A-share quantitative workflows.

## What Is a Skill?

Initially, AI usage relied on writing prompts. Those who could describe problems effectively gained an early advantage. Crafting good prompts is difficult, which led to the emergence of high-paying prompt engineer roles.

!!! tip
    By 2026, the first wave of high-salary prompt engineers has been laid off, transitioning into "technicians."

This shift exposed several issues:

- Good prompts are hard to reuse.
- Quality fluctuates when switching users or conversations.
- Tasks requiring background knowledge demand re-providing context every time.
- Relying solely on prompts makes it difficult to carry scripts, templates, and long documents.

This led to the second generation: prompt libraries, prompt files, and slash commands. These consolidate common tasks into templates, solving the "repetitive input" problem and enabling teams to share workflows.

However, the problem isn't fully solved. Even the best prompt essentially focuses on "doing this one task." It excels at defining tasks but struggles to encapsulate long-term knowledge and standards.

This is where skills become necessary. The core value of a skill is not adding a command, but packaging knowledge, best practices, workflows, and resource files into incrementally loadable capability units. Models initially see only the name and description, loading full content only when relevant. This saves tokens compared to stuffing all instructions into the system prompt and is easier to maintain.

Anthropic released introductions and usage documentation for agent skills in October 2025; subsequently, OpenAI adopted the same format in Codex CLI and ChatGPT. Now, major development tools like Trae and VS Code, as well as Openclaw, support this format. Skills have evolved from Anthropic's pioneering exploration into a cross-tool workflow encapsulation format.

## Why Should Quants Care About This Marketplace?

SkillsMP is currently the largest marketplace. As of March this year, it has listed over 630,000 skills, many receiving over a million stars. Initially maintained by Manus (now part of Meta), it is now community-maintained and highly active.

!!! tip
    How popular are skills? When visiting SkillsMP, you have a high chance of encountering a "biological verification" test. Ordinary websites don't offer this "privilege."

![Geek-style SkillsMP website](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skillsmp.png)

SkillsMP categorizes various skills. For quants, the Finance & Investment category, containing 20,270 skills, is worth exploring. Subcategories under Data & AI, such as machine learning and data analysis, are also valuable.

Next, we will recommend key skills for quants. First, let's introduce how to find, install, and use skills.

On SkillsMP, you can search directly rather than browsing by category. For example, if you want AI to use AkShare's data API more accurately, search for "akshare" and review the highest-rated skills.

![High-rated skill cards found by searching akshare on SkillsMP](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/find-akshare.png)

Clicking the card reveals the assets of the AkShare skill.

!!! attention
    SkillsMP is not an Apple App Store. It has almost no review process for published skills. Since skills can carry various scripts (e.g., Python scripts), they may be **automatically called and executed** on your local machine. Therefore, security auditing of skill content is crucial. By the way, LiteLLM recently disclosed a severe security vulnerability that could steal all secrets from your machine. You can self-check using: `pip show litellm`

Once you find a desired skill, install it based on how you use the AI large model.

If you are using Openclaw, Claude Code, GPT Codex, etc., you can install it via the command line (refer to the installation command on the right side of the skill details page; the following is illustrative):

```bash
npx skills add openclaw/skills
```

If you are using IDE tools like Trae or VS Code, download the corresponding zip package and copy it to the directory specified by the IDE. For example, if using VS Code, unzip the skill's zip package (ensure the root directory contains the `SKILL.md` file) and copy it to the `.github/skills` directory.

The following image shows how to download the skill's zip package.

![Installation entry for downloading skills on SkillsMP](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/skills-how-to-install.png)

After installing the skill, you can use it via slash commands (or verify the installation). Using the Tushare skill as an example, we demonstrate how to verify successful installation in VS Code.

![Verifying Tushare skill installation via slash command in VS Code](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/tushare-skill-verify.png)

The screenshot is from VS Code's AI chat window. Through the slash command and its prompts, we verified the successful installation. Thereafter, these skills will trigger automatically as you write code.

## Essential Skills for Quants

**All software documentation is poor, but some is worse.**

Installing skills saves us from reading these "heavenly scripts" and helps AI understand how to use these APIs.

The first essential skill to install is likely the XtQuant skill—if you are planning to use QMT/XtQuant for live trading or market data acquisition.

Searching for "xtquant" yields several skills. We recommend clicking the `xtquant.md` from `openclaw/skills`, which currently has 3.3k stars.

After downloading its zip package, we find it contains all XtQuant documentation (over 100KB) and a `demo.py`.

We previously mentioned that AkShare's skill is also available on this marketplace. However, East Money's restrictions on web scraping are now severe, making it difficult to acquire data at scale via AkShare.

One alternative is Tushare. There are multiple Tushare skills on SkillsMP, but none are officially released. Therefore, **do not install them from here**. Instructions for installing Tushare skills are available on Tushare's official website.

For example, if you are using Openclaw, install it as follows:

```bash
clawhub install tushare-data
```

When using tools like VS Code, you can download it from [https://tushare.pro/files/pro/tushare-data.zip](https://tushare.pro/files/pro/tushare-data.zip).

BaoStock is a free market data source. You can also find skills on how to use it on SkillsMP.

## Skills for Discretionary Investors

SkillsMP also hosts skills suitable for discretionary investors. For example, `market-research.md` is used for market research, competitive analysis, investor due diligence, and industry intelligence, complete with source attribution and decision-oriented summaries.

There is also an East Money skill, `eastmoney-trading.md`. The East Money Securities Trading Skill supports automatic login, position inquiry, position analysis, conditional stock selection, buying, selling, order cancellation, order inquiry, and fund inquiry, providing complete trading functions. It uses CDP to connect to the browser and supports automatic CAPTCHA recognition. However, the author notes this is a high-risk operation and should be used with caution. For API-level live trading, it is still recommended to obtain a quantitative trading interface from your broker.

If you believe real-time tracking of financial news is important, you can install the `finance-news-source` skill.

![Real-time capture of financial news by the finance-news-source skill](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260326151611.png)

However, if you want to obtain these news in real-time, it may not work well in Trae/VS Code. It is better to install Claude Code or Openclaw. They are the best technicians.
