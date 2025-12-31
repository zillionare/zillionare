
## Winter is Coming

A DataDrivenInvestor post backtested 20 years of currency strength data, identifying market phases and the effectiveness of simple moving average strategies in forex trading.

https://medium.com/@phitzi/winter-is-coming-to-forex-markets-i-backtested-20-years-of-currency-strength-data-3b3c2d38552b

## Engineering and Interviewing at HRT

We do now have a much wider variety of engineering jobs, which, generally speaking, is a good thing. But it can be a little difficult for someone interested in engineering at HRT to figure out what exactly is happening internally and where they may best fit. I’ve found myself repeatedly giving the same “spiel” during interviews, and I figured it’d make sense to just write it down so everyone has access to the same information. The remainder of this post should help you get a better mental model of the topology of engineering at HRT and then explain how to approach the interview. Please keep in mind that I cannot possibly address every specialty at HRT in a single blog post. So if you have a skill set that would work at HRT and it’s not explicitly mentioned here, please still apply, and our recruiting team will help you find the right fit.

https://www.hudsonrivertrading.com/hrtbeat/engineering-and-interviewing-at-hrt/


## 2026十大量化技术

1. Agentic AI
   Agentic AI 是2025-2026年金融界最快增长的技术趋势之一。与传统模型不同，这种“AI 助手”能够自主规划并执行多步工作流。在量化领域，它意味着 AI 不再只是生成策略代码，而是能自主监控市场变化、根据回测结果调整风险参数并执行交易订单。
2. 量子增强量化模型
   2025年摩根大通、高盛等巨头已开始应用量子计算进行风险分析。到2026年，量化人需要理解如何利用量子计算优化投资组合、加速衍生品定价及增强高频交易算法，量子技术正在从实验室走向实战化规模应用
3. 可解释的 AI
   随着监管压力和内部风控要求的提高，黑箱策略已不可持续。2026年，量化人必须掌握如 SHAP 值分析、注意力机制分析等 XAI 技术，以解释算法决策背后的逻辑，确保模型符合受托责任和合规标准。
4. 增强型强化学习 (Reinforcement Learning Agents)
强化学习代理能在模拟市场环境中持续学习。2026年的量化系统要求开发者能够构建并在实时数据流中持续训练强化学习代理，使其能动态响应市场制度的变化
5. Polars: 高性能数据处理的“绝对主力: 多线程并行、查询优化器（Lazy API）和零拷贝（Zero-copy）
6. Pandas 3.0：生态系统的“守门员”Pandas 3.0 彻底解决了长期困扰量化人的内存占用大、字符串处理慢的问题。在 2026 年，如果你不了解如何利用 Arrow 后端进行内存高效操作，你的代码将无法兼容主流的金融数据 API（如 Bloomberg、Refinitiv 的新版 SDK）。
7. Apache Arrow 
8. FastHTML：量化看板与工具的“极速交付”
FastHTML 是 2024 年末兴起、2025 年爆发的 Python 全栈框架，它正在取代 Streamlit 在专业量化团队中的地位。实时损益（P&L）监控看板、因子分析交互界面、策略参数动态调节终端。
9. LaunceDB/DuckDB 针对向量检索（RAG）和本地 OLAP 分析的极速数据库
10. sqlite3 > sqlite-utils > fastlite
11. Nanobind 比pybind11更轻量
12. ~~uv~~
13. redis timeseries 和 gears （自动将 tick 重采样为 1min 15min 30min 1h 4h 1d，超快，占内存很少（1G），日线可以完全放在其中
14. ~~pydantic: - 在 Agentic AI 时代，LLM 输出的是非结构化文本，通过 Function Calling 转化为结构化指令。 Pydantic 是 LLM 和 Python 代码之间的“翻译官”和“卫士”。~~
- 关联： FastHTML 严重依赖 Pydantic；Agent 框架（如 LangChain/Smolagents）的核心也是 Pydantic。它是 2026 年 Python 代码健壮性的基石。
