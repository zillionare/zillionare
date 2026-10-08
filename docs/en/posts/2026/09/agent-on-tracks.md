---
title: "Can Vibe Coding Build Large Quant Projects? A Developer’s Test"
date: 2026-09-07
slug: en/posts/tools/agent-on-tracks
tags: [AI Coding, Quant Frameworks, Vibe Coding, Software Engineering]
excerpt: "This article evaluates whether AI-driven \"vibe coding\" can handle complex quantitative trading frameworks. It explores the gap between rapid prototyping and production-ready code, highlighting the need for formal verification in large-scale systems."
lang: en
translation_of: posts/tools/agent-on-tracks
auto_translated: true
source_sha: 7d4a9e53c6b049cb692a41cce5419b0d1521e81e
---

Vibe coding has indeed turned software development dreams into reality for many, including us veterans of traditional "hand-crafted" programming. We had many ideas in the past but hesitated to attempt them due to insufficient manpower or knowledge reserves. Now, we can’t help but feel eager to try.

Our team previously developed **zillionaire 2.0**, a platform designed for private equity teams. It uses a containerized microservices architecture, with market data stored in InfluxDB and cached via Redis, and connects to East Money’s trading interface. However, we lacked a quantitative trading framework tailored for individuals—one that handles local data storage, utilizes more affordable trading interfaces, and primarily operates on a single machine.

This year marks a breakthrough year for AI coding. Starting in late April, we began attempting to develop a personal version of a quantitative trading framework—**Millionaire**—using AI-assisted coding.

**Once you dive into Vibe Coding, the weekend becomes a distant memory.**

## /01 What Can AI Do Today?
**Better Algorithm Implementation**

Any quantitative trading framework requires strategy evaluation. Some frameworks use fixed-horizon forward returns as input metrics—for example, evaluating a strategy’s effectiveness based on returns 1, 3, or 5 days after a buy order (T0). This approach requires fixed trading cycles, which may cause you to miss optimal trading opportunities. Even if we consider market timing unreliable, we still encounter situations where fixed-cycle methods become clumsy, particularly when overlaying risk management strategies, as the sell time cannot be fixed.

For instance, we might backtest a strategy using T+3 returns, but in live trading, we might hit our stop-loss the next day. How do we backtest risk management strategies overlaid with the base strategy?

After discussing with AI for some time, I realized that this risk management strategy is actually the **Triple-Barrier Method** proposed by Marcos López de Prado. Since AI identified this, it can now implement it effectively!

Another example is the use of **placebo groups** in Form 4 research. Form 4 is a form required by the U.S. Securities and Exchange Commission (SEC) to prevent company directors, supervisors, and executives from profiting from insider trading. They must file and submit this form within two working days after completing a trade. It is an electronic form that, once submitted, is publicly released via the EDGAR system and visible to all investors.

> As a supporting regulation, the law requires that any profits generated from selling shares within six months of buying them must be turned over to the company. Combined, these two systems essentially eliminate the arbitrage space for insider trading.

After backtesting the Form 4 factor, I suddenly recalled that this strategy lacks reproducibility—how can we prove that the asset’s volatility return after the event is indeed due to the event itself, rather than other factors? There seemed to be no market factor to deduct. After some exploration, we finally found the **placebo statistical method**. Clearly, AI is already familiar with this method, making implementation effortless.

Thus, AI can now help us write efficient algorithms we previously didn’t know existed—especially once you identify the correct "terminology."

These algorithms have clear, solid definitions with no ambiguity, a area where AI excels.

## /02 What Is AI Still Struggling With?
Initially, **Millionaire** progressed smoothly through vibe coding. Gradually, however, problems multiplied. Features I remembered proposing or even implementing turned out to be missing in testing; some were only 80% or 20% complete.

Slowly, I lost my memory. **I no longer know what features the system should have, what it already has, or which displayed features are actually dead code I had previously rejected but remains in the codebase.** This dead code constantly tempts AI to continue down the wrong path.

**It gives you hope, then disappointment, until despair.** This is also where AI currently shines. In the **oh-my-opencode** framework, there is a master Agent named **Sisyphus**. Like the mythological figure who rolls a boulder up a hill only for it to roll back down just before reaching the top, forcing him to start over every day, this name is aptly chosen for the master Agent.

This is the fate of Vibe Coding.

Even if you use tools like **speckit**, **ralph**, or **super power**, once the project exceeds tens of thousands of lines of code without human intervention, what you get is another 90%-complete **Millionaire**: many features are implemented, and AI even adds extras—like giving you an extra finger when you asked for a hand. In other places, it looks like a perfect hand, but it can’t make a fist.

And if you try to remove the extra sixth finger, you might get five fingers, but they might grow on your foot.

## /03 The Final Proof

The answer lies in the formal proof of programming problems.

In recent days, mathematicians **Astra** and **Fable** achieved major breakthroughs. Astra advanced the Twin Prime Conjecture to 186, a record that had been stagnant for over a decade. If Astra had been born 12 years earlier, Yitang Zhang might have had to wash dishes for life. Fable, on the other hand, formally verified Fermat’s Last Theorem.

The core technological foundation of these breakthroughs is **Lean’s formal verification**. It is the key that allows AI to autonomously explore numbers and ensure conclusions can be verified.

Currently, in AI coding, we still lack such a framework that allows a user story, with user assistance, to be decomposed into specifications (specs), followed by defining acceptance criteria. Then, AI implements it, and tests verify that all specs are met.

Programming is an engineering problem; it cannot and need not fully satisfy formal verification like Lean (although individual algorithms can). It doesn’t matter if the machine "gives birth" to a duck; as long as it quacks like a duck and walks like a duck, it is a duck.

This is the goal of my **Agent on Tracks** project. It is currently undergoing iterative development via bootstrapping, just a few steps away from completing CI and release. From then on, you should be able to write a software product with hundreds of thousands of lines of code by simply providing user stories.

**Millionaire** will be the second product released under this framework.
