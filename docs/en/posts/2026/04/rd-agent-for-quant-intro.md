---
title: "Microsoft RD-Agent: 4 Agents Automate Factor Mining"
date: 2026-04-30
slug: en/posts/tools/rd-agent-for-quant-intro
tags: [Factor Mining, LLM Agents, Quantitative Research, RD-Agent]
excerpt: "Microsoft’s RD-Agent(Q) automates factor mining via four LLM agents. Accepted at NeurIPS 2025, it integrates with QLib for robust, backtest-validated quantitative research."
lang: en
translation_of: posts/tools/rd-agent-for-quant-intro
auto_translated: true
source_sha: d003f56fd600b5c938c84ec5bec65aa1635bd00a
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/wolfgang-weiser-fIoBQ9i7Vjo-unsplash.jpg"
---

## 1. The Dilemma of Quantitative Research

Anyone who has worked in quantitative investing knows that factor mining and strategy development is a long, solitary journey. Facing massive datasets daily, you repeatedly run backtests, tune parameters, and write code. The birth of a "good" factor often requires weeks or even months of trial and error. The pain intensifies when market regimes shift; a carefully crafted strategy may become obsolete overnight, forcing you to start from scratch.

Meanwhile, Large Language Models (LLMs) have advanced rapidly over the past two years. However, using ChatGPT as a "quantitative analyst" is not yet practical. Ask it to generate trading signals, and it might "confidently hallucinate"; ask it to read research reports, and the factors it proposes often lack backtest validation. LLM "hallucination" is fatal when real money is at stake.

Is there a way to leverage LLM creativity while constraining it with rigorous backtesting and code execution?

Microsoft Research Asia’s answer is **RD-Agent** (Research & Development Agent), an automated multi-agent framework designed for industrial-grade R&D workflows. Its specialized version for quantitative finance, **RD-Agent(Q)** (R&D-Agent-Quant), was accepted at NeurIPS 2025 and is currently one of the most popular quantitative AI Agent projects on GitHub (12,000+ Stars).

## 2. What Is RD-Agent?

Essentially, RD-Agent is an automated R&D framework that uses **AI to drive data-driven AI**. It does not pursue "end-to-end black-box trading." Instead, it focuses on the most labor-intensive aspects of quantitative research—**factor mining, model optimization, and code implementation**—and automates these processes through multi-agent collaboration.

The project is fully open-source (MIT license), developed in Python, and deeply integrated with Microsoft’s proprietary AI quantitative platform, **QLib**. You can find the complete code on GitHub (microsoft/RD-Agent) or install it via PyPI:

```bash
pip install rdagent
```

## 3. Collaboration Among Four Agents

The core of RD-Agent(Q) is a "virtual research team" composed of four LLM agents. Each agent has a specific role, and they iterate continuously through closed-loop feedback:

| Agent | Role | Core Responsibilities |
| :--- | :--- | :--- |
| **Research Agent** | "Chief Analyst" | Automatically reads research reports, financial statements, and academic papers to extract investment hypotheses and propose new factors or model optimizations. |
| **Development Agent** | "Quant Engineer" | Translates research hypotheses into executable Python code, completing factor construction or model building. |
| **Dispatch Agent** | "Investment Director" | Uses Multi-Armed Bandit algorithms to dynamically decide whether to prioritize factor or model optimization. |
| **Implementation Agent** | "DevOps Engineer" | Handles engineering details such as bug fixing, time-series alignment, and data cleaning. |

This division of labor closely mirrors the operation of a real research team. The Research Agent "thinks," the Development Agent "does," the Dispatch Agent "prioritizes," and the Implementation Agent "handles edge cases." Crucially, they do not collaborate just once; they continuously iterate within an ongoing closed loop.

## 4. The Five-Step Automated R&D Loop

RD-Agent(Q) follows a strict five-step cycle:

**1. Specification (Requirement Definition)**
Define research goals and form testable hypotheses. For example, "extract sentiment factors from management discussion sections in financial reports" or "optimize the predictive power of the existing Alpha360 factor set."

**2. Synthesis (Solution Design)**
Design specific factor calculation formulas or model structures based on domain priors and data analysis. This step leverages the strong reasoning capabilities of LLMs, but all designs are anchored within an executable code framework.

**3. Implementation (Code Generation)**
Automatically write and execute code via the code-generation agent. RD-Agent incorporates a Co-STEER (Co-evolutionary Self-referential Execution and Refinement) mechanism to ensure generated code is not only syntactically correct but also passes unit tests.

**4. Validation (Backtest Verification)**
Backtest strategies on real market data to verify effectiveness. This step acts as the system’s "firewall"—no matter how eloquently an LLM speaks, the final result must be validated by hard metrics such as Information Coefficient (IC), returns, and Sharpe ratio.

**5. Analysis (Feedback)**
Comprehensively evaluate experimental results and feed them back into the next cycle. The system autonomously decides the next optimization direction: Should we dig deeper into the current factor family or switch to optimizing the model structure? Should we add data features or adjust the parameter space?

The greatest value of this closed loop is that **it constrains LLM creativity with code execution and backtest results, avoiding "hallucination."** In other words, RD-Agent does not directly give you trading signals; it provides verified, interpretable, and reproducible factors and models.

## 5. Unique Value for Quants

For quantitative practitioners, RD-Agent(Q) offers unique value at several levels:

**Cost Reduction and Efficiency.** According to the paper’s experimental data, RD-Agent(Q) achieves approximately a 2x increase in Annualized Return Rate (ARR) with a single-run cost of less than $10, while reducing the number of factors by about 70%. This means you can achieve better results with fewer factors while significantly reducing data processing and computational resource consumption.

**Automation of Tedious Tasks.** Repetitive labor in factor mining—reading reports, writing code, running backtests, and tuning parameters—can be handed over to agents. Quantitative researchers can devote more time to strategy logic design, risk management, and live trading deployment.

**Avoiding the "Overfitting Trap."** Traditional automated factor mining methods (such as genetic algorithms) often generate numerous redundant factors, leading to overfitting. RD-Agent(Q)’s "joint factor-model optimization" strategy achieves a better balance between predictive accuracy and strategy robustness by alternating between factor and model optimization.

**Explainability and Compliance.** Unlike end-to-end deep learning black-box models, every factor generated by RD-Agent has a clear mathematical expression and backtest report, which is crucial for risk control audits and compliance disclosure.

## 6. Three Key Application Scenarios

RD-Agent(Q) currently supports the following three quantitative research scenarios:

**Scenario 1: Automatic Factor Mining and Iteration**

```bash
rdagent fin_factor
```

The system automatically proposes new factor hypotheses on historical data, combines them with backtest validation, and uses reinforcement learning to screen for high-yield factors, iterating continuously.

**Scenario 2: Automatic Factor Extraction from Reports/Financial Statements**

```bash
rdagent fin_factor_report --report-folder=<your_report_directory>
```

Automatically parses unstructured text (such as financial research reports and company financial statements), extracts key information, and converts it into computable structured factors. This is particularly valuable for event-driven strategies.

**Scenario 3: Joint Evolution of Factors and Models**

```bash
rdagent fin_quant
```

This is RD-Agent(Q)’s flagship feature. The Dispatch Agent dynamically decides whether to prioritize factor or model optimization, achieving "factor-model" co-evolution. Experiments show that this joint optimization strategy outperforms optimizing factors or models separately.

## 7. Deep Synergy with QLib

RD-Agent(Q) does not build all infrastructure from scratch; it stands on the shoulders of giants—Microsoft’s other star open-source project, **QLib**.

QLib provides complete quantitative research infrastructure: high-performance data storage (Parquet partitioning + binary caching), Alpha158/360 factor libraries, model training frameworks, strategy backtesting engines, and portfolio optimization modules. Its data reading speed far exceeds traditional database solutions, providing performance guarantees for rapid agent iteration.

RD-Agent acts as the "automated brain," responsible for the upper-layer intelligence of strategy R&D. Together, they form a complete automated pipeline from data to strategy.

## 8. Quick Start and Pitfalls to Avoid

**Official Support is Linux-Only.** This is the biggest barrier to RD-Agent in practical use. The core reason is that the quantitative backtesting phase relies heavily on Docker container execution (the code hardcodes `unix://var/run/docker.sock` for Docker API calls). Docker path mapping and file system permissions on macOS and Windows differ from Linux, leading to runtime errors (see issue #1064 for Windows issues). GitHub issues regarding macOS support remain open (#1227).

**Clarification: CUDA/GPU Is Not Mandatory.** Although the Dockerfile is based on the PyTorch CUDA runtime image, the code includes automatic GPU detection and fallback mechanisms. If `nvidia-smi` fails inside the container or the host lacks a GPU, it automatically switches to CPU mode. Community feedback confirms successful operation of scenarios like `fin_model` on pure CPU environments (issue #445). Therefore, what hinders macOS operation is not CUDA, but Docker’s cross-platform compatibility issues.

**Viable Solutions for Mac or Windows Users:**

- **macOS:** Install OrbStack (a stable container solution for macOS that does not require root), then run it within. However, Docker path mapping issues may still arise, requiring troubleshooting skills.
- **Windows:** Enable WSL2 and install/run RD-Agent within the Linux subsystem. This is currently the most stable non-Linux solution.
- **Cloud Servers:** Deploy directly on Linux cloud hosts (e.g., Alibaba Cloud, Tencent Cloud), which is the recommended approach.

The first run will automatically pull and build QLib’s Docker image (based on PyTorch CUDA runtime). Without image acceleration, this may take 10–20 minutes, so please be patient.

### Installation Steps

```bash
# 1. Environment Preparation (Python 3.10 or 3.11)
conda create -n rdagent python=3.10
conda activate rdagent
pip install rdagent

# 2. Configure LLM Backend
# RD-Agent supports various LLM providers via LiteLLM. Example for OpenAI:
cat << EOF > .env
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=<your_API_Key>
EOF

# It also supports Azure OpenAI, DeepSeek, SiliconFlow, and other backends.
# Note: The system requires ChatCompletion, json_mode, and embedding query capabilities to be available simultaneously.

# 3. Health Check
rdagent health_check
```

**About LiteLLM:** RD-Agent calls large models via LiteLLM by default. However, LiteLLM is installed automatically as a dependency (`pip install rdagent`), so **you do not need to learn or configure LiteLLM separately**. LiteLLM’s role is to adapt different vendors’ API formats internally; externally, you only need to provide the model name and API key.

If you have a single OpenAI-compatible API, the configuration above is sufficient. If your chat model and embedding model use different API endpoints, you can configure them separately:

```bash
cat << EOF > .env
CHAT_MODEL=gpt-4o
CHAT_OPENAI_API_KEY=sk-xxx
CHAT_OPENAI_BASE_URL=https://chat-api.example.com/v1

EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_OPENAI_API_KEY=sk-yyy
EMBEDDING_OPENAI_BASE_URL=https://embedding-api.example.com/v1
EOF
```

If your model includes chain-of-thought reasoning (such as DeepSeek-R1’s `` tags), remember to add `REASONING_THINK_RM=True`.

### Data Sources Are Always a Challenge

**This is the most common pitfall.** RD-Agent’s quantitative backtesting relies on QLib data, but QLib’s **official dataset has been temporarily disabled due to data security policies**. The project documentation does not highlight this sufficiently (community issue #1335 also reflects this problem).

Currently, you must use **community-maintained data sources**:

```bash
# Download community-version A-share daily data (maintained by chenditc)
wget https://github.com/chenditc/investment_data/releases/latest/download/qlib_bin.tar.gz
tar -xzf qlib_bin.tar.gz -C ~/.qlib/qlib_data/
```

The raw data originates from Yahoo Finance and is not perfect; it is intended only for experimentation and research. If you have higher-quality data sources (such as Wind, JoinQuant, or Tushare Pro), you can import them into QLib’s data format. For institutional users, replacing the default data source with internally cleaned data is a more reasonable approach.

Therefore, for those without programming and quantitative foundations, this is not a "plug-and-play" project.

### Running Quantitative Scenarios

Once data is ready, you can start the Agent:

```bash
# Automatic factor iteration
rdagent fin_factor

# Joint factor-model evolution
rdagent fin_quant

# Factor extraction from reports
rdagent fin_factor_report --report-folder=./reports
```

During operation, the system automatically generates visual reports, including factor effectiveness heatmaps and backtest return curves, facilitating manual review. Additionally, the project provides a Web UI (`rdagent server_ui`) to monitor the Agent’s operational status and iteration trajectory in real time.

### Other Important Notes

**Data Leakage and Overfitting Risks.** Community users have raised questions (issue #1387): Does the system using backtest results as feedback for the next iteration lead to implicit overfitting on the test set? This is a warning-worthy issue. It is recommended to independently validate factors produced by RD-Agent on out-of-sample periods before considering live trading.

**Docker Image Build Time.** The first run automatically pulls and builds QLib’s Docker image (based on `pytorch/pytorch:2.2.1-cuda12.1`). This process depends on network conditions and may be lengthy or even infeasible. Be sure to configure mirror sites in advance.

## 10. Conclusion

For quants, RD-Agent is not meant to replace your role but to serve as your "super assistant." It handles tedious, repetitive, and mechanical tasks.

RD-Agent represents a clear direction: **not letting AI directly make trading decisions, but letting AI accelerate your R&D iteration, enabling every quantitative researcher to have their own "automated factor factory."** You will then focus on what truly requires human wisdom—understanding the market, judging risks, and relying on strategy intuition.

But first, you must understand **what a factor is, what quantitative trading is, and what machine learning is**.

KuangTi Quant’s "Quantitative 24 Lessons" and "Factor Analysis and Machine Learning Strategies" will guide you from beginner to expert, helping you build a complete quantitative trading knowledge system and cultivate your taste and intuition. Over the past three years, we have not only trained new employees for over 10 private equity firms but also witnessed some new employees become the backbone of their teams, taking on interviewing and mentoring roles.

In every aspect, our quantitative courses are undoubtedly an express lane into the quantitative field.

If you are looking for a way to improve factor mining efficiency and reduce strategy R&D costs, RD-Agent is worth studying this May Day holiday. To coincide with the holiday, we are offering a discount—the only one in the past six months—a 10% discount for new students, valid for four days (until May 4)!

---

**References:**
- GitHub: https://github.com/microsoft/RD-Agent
- Paper: https://arxiv.org/abs/2505.15155
- Documentation: https://rdagent.readthedocs.io/
- Technical Report: https://aka.ms/RD-Agent-Tech-Report
- QLib: https://github.com/microsoft/qlib
