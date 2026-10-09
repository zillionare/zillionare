---
title: "31k-Star Open Source: Turning Market Noise into Systematic Decisions"
date: 2026-04-23
slug: en/posts/algo/tcn/ai股票分析
tags: [Open Source, Quantitative Analysis, Automated Investing, Systematic Trading]
excerpt: "This 31k-star GitHub project automates stock analysis by transforming fragmented data into structured decision dashboards, prioritizing robust workflows and fail-safe mechanisms over simple AI predictions."
lang: en
translation_of: posts/algo/tcn/ai股票分析
auto_translated: true
source_sha: 789825118f671d2294c7aa3b3a57e27604fce4d0
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260423182355505.png"
---

# A Robust Stock Intelligence System

I recently reviewed an open-source project called `daily_stock_analysis`, which has garnered `31k stars` on GitHub.
At first glance, the name might suggest it is just another "AI-powered stock analysis" tool. However, after reading the README thoroughly, I believe its true value lies not in the term "AI," but in its attempt to solve a more fundamental problem:

**The scarcest resource in investing is never information itself, but the ability to consistently process information into judgments.**

The market is saturated with information. In China A-shares, Hong Kong stocks, and US markets, quotes, announcements, capital flows, news, sentiment, technicals, and fundamentals update explosively every day. The disadvantage for ordinary investors is often not a lack of information, but information that is too fragmented and reactions that are too fast, leading to judgments driven by emotion rather than logic.

Therefore, this project’s goal is not to "trade for you," but to consolidate scattered, repetitive, and emotion-prone analysis actions into a process that can run automatically, push notifications, review history, and continuously improve.

## What It Actually Does

In simple terms, this project automatically analyzes your watchlist stocks daily and compiles the results into a "decision dashboard" for you.
The key word here is not "daily report," but "dashboard."

It does not simply give you a "bullish" or "bearish" statement. Instead, it integrates the following elements:

- A one-sentence core conclusion
- Entry price, stop-loss price, and target price
- Risk warnings
- Operational checklists
- Multi-dimensional information including technicals, capital flows, sentiment, and announcements

This distinction is crucial. Many so-called AI stock tools simply feed data into a model and output text that *looks* like analysis. This project takes a step further by attempting to transform "information" into a "decision entry point." The difference is significant: the former is merely descriptive, while the latter approaches decision support.

## It Covers More Than Just Individual Stock Analysis

Based on the README, this project has evolved from a single-point script into a comprehensive workflow:

- Supports China A-shares, Hong Kong stocks, US stocks, and some US indices
- Capable of individual stock analysis and broader market review
- Includes built-in market strategy systems: a "three-stage review strategy" for China A-shares and a Regime Strategy for US stocks
- Supports historical report details, full Markdown reports, and plain-text copying
- Supports AI backtesting verification, allowing comparison between historical analysis and next-day actual performance
- Supports strategy-based stock queries, enabling chat-style inquiries based on specific strategy frameworks
- Provides a complete Web workspace for holdings, history, settings, and notification sending

This indicates that the project is no longer just a "data scraping + LLM calling" demo, but is evolving into a sustainable investment research workspace.

## The Real Challenge: Can the System Run Long-Term?

I believe the most profound aspect of this project is not the number of technical terms the model outputs, but its serious handling of issues that are easily overlooked yet fatal in financial scenarios.

Take data sources, for example.

The project integrates not a single market data source, but a combination:

- Market Data: `AkShare`, `Tushare`, `Pytdx`, `Baostock`, `YFinance`, `Longbridge`
- News Search: `Anspire`, `Tavily`, `SerpAPI`, `Bocha`, `Brave`, `MiniMax`
- Social Sentiment: `Stock Sentiment API`, covering Reddit, X, and Polymarket (US stocks only)
- AI Models: `AIHubMix`, `Gemini`, `OpenAI`-compatible interfaces, `DeepSeek`, `Tongyi Qianwen`, `Claude`, `Ollama`

These names might look like "feature stacking," but the critical factor is not the quantity of integrations, but the underlying logic: **Financial systems fear single points of failure the most.**

API rate limits, missing fields, search failures, and model instability may be minor issues in general tools; in financial analysis, they propagate and ultimately lead to erroneous conclusions. Therefore, the repeated emphasis in the README on fallbacks, degradation, caching, and field contracts is not engineering pedantry, but a component of credibility.

## Data Routing Is Not Arbitrary

This system employs explicit priority for data routing.

For US and Hong Kong stocks, if `LONGBRIDGE_APP_KEY`, `LONGBRIDGE_APP_SECRET`, and `LONGBRIDGE_ACCESS_TOKEN` are configured, daily K-line and real-time quotes prioritize `Longbridge`. If this fails or fields are incomplete, `YFinance` or `AkShare` serve as backups. For US broad indices like `SPX`, `YFinance` is always prioritized because Longbridge does not provide index data.

The routing for China A-shares remains:

`Efinance -> AkShare -> Tushare -> Pytdx -> Baostock`

Additionally, `Tushare` now supports Hong Kong stock queries. As long as `TUSHARE_TOKEN` is configured and the account has Hong Kong stock daily data permissions, entering Hong Kong stock codes on the homepage will analyze them normally.

This approach indicates that the code is not written "just to run once," but to address real-world issues encountered in live deployment: different markets, permissions, and interfaces have varying capability boundaries.

## This Project Does Something Harder: Externalizing Intuition into Process

What is truly worth pondering is not whether it can write analysis, but its attempt to externalize the judgment process—which traditionally relies on personal experience and state—into a more reviewable structure.

For instance, it embeds trading discipline:

- Deviation rates exceeding thresholds default to "Strictly No Chasing Highs" warnings
- Trend trading requires `MA5 > MA10 > MA20`
- Entry, stop-loss, and target prices are explicitly defined
- Checklists are marked as "Met," "Note," or "Not Met"
- News时效 defaults to the last 3 days, preventing the use of outdated information to support new judgments

These may look like rules, but they are more akin to combating human volatility. The core issue for ordinary investors is often not a lack of knowledge, but instability in application. One day you know not to chase highs, but tomorrow, excited by intraday movements, you still do; you know to check announcements and capital flows first, but ultimately get dragged by price limits.

Therefore, the true value of such tools is not to prevent you from making mistakes, but to prevent you from making mistakes due to低级混乱 (low-level chaos).

## The GitHub Actions Section Demonstrates Strongest "Product Sense"

My favorite part of the README is not the model, but the deployment.

The recommended solution is `GitHub Actions`, with a very direct goal:

**Deploy in 5 minutes, zero cost, no server required.**

The process is simple:

1. Fork the repository  
2. Configure Secrets in `Settings -> Secrets and variables -> Actions`  
3. Enable Actions  
4. Manually run a workflow test

By default, it executes automatically at `18:00` Beijing Time on each working day, with manual triggering also supported. Non-trading days are skipped by default, but you can bypass the trading day check in two ways:

- Global disable: `TRADING_DAY_CHECK_ENABLED=false`
- Single run force: Check `force_run` when manually triggering Actions

Why is this important? Because it lowers the barrier significantly. Many people do not want to use automation tools, but give up upon hearing "deployment," "servers," "scheduled tasks," or "environment variables." This project clearly understands that **enabling ordinary users to run it is itself a product capability.**

Of course, the README does not offer only GitHub Actions. It also provides a second method: local execution or Docker deployment.

The basic local execution flow involves four steps:

```bash
# Clone the project
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env && vim .env

# Run analysis
python main.py
```

If you do not use the Web interface, the README provides a more direct model channel configuration, suggesting direct configuration in `.env`:

```env
LLM_CHANNELS=primary
LLM_PRIMARY_PROTOCOL=openai
LLM_PRIMARY_BASE_URL=https://api.deepseek.com/v1
LLM_PRIMARY_API_KEY=sk-xxxxxxxx
LLM_PRIMARY_MODELS=deepseek-chat
LITELLM_MODEL=openai/deepseek-chat
```

The advantage of this approach is simplicity and directness, without needing to maintain an additional configuration file. After saving, if you switch back to the Web interface later, you can continue editing the same fields in the Web settings page; the two are interconnected.

The README also includes an important note: if you simultaneously enable advanced model routing YAML, i.e., `LITELLM_CONFIG`, then the YAML file is primarily responsible for defining available models and routing rules (`model_list`); however, the actual running main model, fallback models, Vision settings, and Temperature are determined by these fields:

- `LITELLM_MODEL`
- `LITELLM_FALLBACK_MODELS`
- `VISION_MODEL`
- `LLM_TEMPERATURE`

In other words, the channel editor saves "channel entries" and does not override the selection of these runtime fields. This distinction is important because many users get confused about which configuration is actually生效 (effective) when mixing page configurations, `.env`, and YAML.

Furthermore, if you plan to use Docker, the README specifically warns against two common pitfalls.

First, Docker deployment and scheduled task configurations require consulting the full guide, while desktop client packaging requires referring to the desktop packaging instructions.

Second, do not misread the Docker version number. You should recognize the image tag you actually pull or run, such as `v3.12.0`. This is because Docker releases in the repository are triggered by `.github/workflows/docker-publish.yml` based on `v*.*.*` Git tags, while `0.0.0` in `apps/dsa-web/package.json` is merely a placeholder and does not represent the real Docker release version. This attention to detail is useful, as many users make the first mistake in troubleshooting by misidentifying the version.

## Many Configurations, But Not Chaotic

This project has many configuration items, but they are largely layered.

The core layers include:

**Model Layer**
- `AIHUBMIX_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `OPENAI_VISION_MODEL`
- `OLLAMA_API_BASE`

Models are uniformly called via `LiteLLM`. For multi-model usage, it is recommended to use:

`LLM_CHANNELS + LLM_<NAME>_PROTOCOL/BASE_URL/API_KEY/MODELS/ENABLED`

If you need to explicitly specify the main or fallback models, configure additionally:

- `LITELLM_MODEL`
- `LITELLM_FALLBACK_MODELS`

The README also highlights several pitfalls here:

- AI priority defaults to `Gemini > Anthropic > OpenAI (including AIHubMix) > Ollama`
- `AIHUBMIX_KEY` does not require configuring `OPENAI_BASE_URL`
- Image recognition must use models supporting Vision
- `DeepSeek` thinking models are automatically identified by model name
- `Ollama` local models must use `OLLAMA_API_BASE`; misusing `OPENAI_BASE_URL` will result in a 404 error.

**Search and Sentiment Layer**
- `TAVILY_API_KEYS`
- `ANSPIRE_API_KEYS`
- `MINIMAX_API_KEYS`
- `SERPAPI_API_KEYS`
- `BOCHA_API_KEYS`
- `BRAVE_API_KEYS`
- `SEARXNG_BASE_URLS`
- `SEARXNG_PUBLIC_INSTANCES_ENABLED`
- `SOCIAL_SENTIMENT_API_KEY`
- `SOCIAL_SENTIMENT_API_URL`

**Market Data and Enhancement Layer**
- `STOCK_LIST`
- `TUSHARE_TOKEN`
- `TICKFLOW_API_KEY`
- Full set of `LONGBRIDGE_*` configurations

**Runtime and Strategy Layer**
- `WECHAT_MSG_TYPE`
- `NEWS_STRATEGY_PROFILE`
- `NEWS_MAX_AGE_DAYS`
- `BIAS_THRESHOLD`
- `TRADING_DAY_CHECK_ENABLED`
- `PREFETCH_REALTIME_QUOTES`

**Agent Layer**
- `AGENT_MODE`
- `AGENT_LITELLM_MODEL`
- `AGENT_SKILLS`
- `AGENT_MAX_STEPS`
- `AGENT_SKILL_DIR`

**Fundamental Layer**
- `ENABLE_FUNDAMENTAL_PIPELINE`
- `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS`
- `FUNDAMENTAL_FETCH_TIMEOUT_SECONDS`
- `FUNDAMENTAL_RETRY_MAX`
- `FUNDAMENTAL_CACHE_TTL_SECONDS`
- `FUNDAMENTAL_CACHE_MAX_ENTRIES`

The abundance of configurations does not indicate chaos. It shows that the project has moved from "can it run" to "how to run stably, and how to adjust for different users and scenarios."

## It Even Anticipates How Failures Occur

There is a section in the README that many might skip, but I consider critical: the timeout semantics for fundamental aggregation.

It explicitly states:

- Currently adopts `best-effort` soft timeout, i.e., `fail-open`
- Timeouts immediately degrade, continuing the main process
- Does not guarantee strict hard interruption of third-party threads
- If business requires hard SLA in the future, it can be upgraded to a "subprocess isolation + kill" solution

This passage may seem like engineering documentation, but it is actually profound. It conveys one message: the author knows the system cannot be perfect forever, but his goal is not to pretend failures won't happen, but to ensure failures occur in a controllable and predictable manner.

This is more mature than claiming "always problem-free."

Field contracts are similarly defined. The README explicitly fixes key structural conventions, such as:

- `fundamental_context.boards.data = sector_rankings`
- `fundamental_context.earnings.data.financial_report = Financial Report Summary`
- `fundamental_context.earnings.data.dividend = Dividend Indicators`
- `get_stock_info.belong_boards = Individual Stock Sector Affiliation`
- `get_stock_info.boards` retained as a compatibility alias

This indicates the project is not just accumulating features, but seriously managing semantics.

## Web Interface and Agent Indicate It Is More Than a "Backend Script"

The project includes a complete Web workspace, and this round of interface upgrades is clearly moving towards a "product" rather than a "tool page":

- Full redraw of light and dark themes
- Persistent theme switching
- Unified visual system for homepage, stock queries, backtesting, holdings, and settings
- Enhanced experience for small screens and touch interfaces
- `ADMIN_AUTH_ENABLED=true` enables password protection

It also features smart import capabilities:

- Import stock pools via screenshots, with Vision AI automatically identifying codes and names
- Support for CSV/Excel
- Support for direct pasting
- Confidence-level layered confirmation, deduplication, select all, and clear functions

Homepage search completion is not simple matching but supports:

- Stock codes
- Chinese names
- Pinyin abbreviations
- Aliases

For example:

- `gzmt -> Kweichow Moutai`
- `tencent -> Tencent Holdings`
- `aapl -> Apple Inc.`

It also implements degradation logic: if indexing fails, it falls back to normal input mode, preventing the entire analysis chain from being blocked.

The Agent stock query section resembles a "second product line."
You can engage in multi-turn dialogues based on strategies in `/chat`, supporting `11` built-in strategies such as moving average golden crosses, Chan Theory, Elliott Wave Theory, and bullish trends. It also supports:

- Streaming display of thought paths
- Exporting `.md` files
- Bot command invocation
- Custom YAML strategies
- `SKILL.md` bundles
- Multi-Agent architecture: `Technical -> Intel -> Risk -> Specialist -> Decision`

It even considers compatible fields, such as `capital_flow_signal` being an enhanced field that does not return results or affect subsequent stages.

All these details indicate that this is no longer a project that "writes a daily report and ends," but is building an extensible analysis framework.

## Final Conclusion

I believe the most noteworthy aspect of this project is not "whether AI can help you pick good stocks," but the realistic direction it demonstrates:

**In investing, truly valuable systems do not cancel your judgment for you; instead, they make the analysis process, which traditionally relies on personal intuition, more stable, reviewable, and repeatable.**

It certainly cannot bear market risks for you, nor can it guarantee profits.
However, it is indeed doing something that few seriously attempt: gradually shifting analysis from an ad-hoc reaction to a systematic capability.

This is not flashy, legendary, or suitable for myth-making.
But if you seriously conduct research, build tools, and view the market, I believe it is closer to what is truly useful in the real world over the long term than many "AI stock-picking stories."

Project Address:  
[https://github.com/ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)
