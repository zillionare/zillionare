---
title: "Global Windows Outage: Lessons for Building Robust Quant Systems"
date: 2024-07-20
slug: en/posts/uncategory/crowed-strike-postmoterm
tags: [Quantitative Trading, Risk Management, System Reliability]
excerpt: "The CrowdStrike faulty update caused a global Windows outage hitting airlines, banks and exchanges. Here's what quants must learn to keep live trading systems stable and resilient."
lang: en
translation_of: posts/uncategory/crowed-strike-postmoterm
auto_translated: true
source_sha: 127aff6c375590f657d9bd10991cee88209aa9d3
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/bsod.jpg"
---

Yesterday afternoon, Microsoft gave everyone an unexpected day off. Windows crashed yet again — but this time it wasn't just a few machines, it was a massive global outage. For a moment, we were all flying the "Blue Banner."

The root cause has now been found, and most machines have been fixed. During a routine update, a security company called CrowdStrike pushed a faulty configuration file to Windows.

That mistake was itself triggered by another, rarer failure. CrowdStrike relies on Microsoft's Azure cloud in US Central, and that data center happened to go down.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/crowd-strike.jpg)

That glitch caused CrowdStrike to pull in corrupted configuration data. Once pushed to endpoints, agents running on that bad config loaded an extra driver called csagent.sys on Windows terminals. That driver contained a bug that sent systems into a blue-screen boot loop.

The outage severely disrupted airlines, banks, and exchanges. It is still unclear whether huge compensation claims will follow, but Microsoft's stock has already taken a serious hit.

It is still unclear how many trading firms and individuals in China were affected, but it is a wake-up call for us quants: Is the trading system you built truly safe and reliable? How should we build our own quantitative trading systems so they keep running stably even when something like this happens?

Here are a few suggestions.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/CI-CD-process.png)

First, achieve high unit-test coverage with a solid CI/CD pipeline. Always remember that any software or hardware system has bugs. When you build a quantitative trading system, high-coverage unit testing plus CI/CD is a must.

Unit tests don't just help us verify each module during development. More importantly, they establish a baseline that lets us confirm the system still meets its requirements as the environment keeps changing.

As the CrowdStrike case shows, even if your trading system itself was not upgraded — just like Windows in this incident — third-party components it depends on, such as data feeds, Pandas or NumPy, may still be upgraded. Before accepting any upgrade, our trading system must be proven to still pass all of our test cases.

Software like CrowdStrike is actually tested quite rigorously in normal times, so why did such a failure still happen? There was certainly an element of bad luck — the Azure failure this time — but most likely CrowdStrike's testing did not fully cover CI/CD. Only with continuous delivery can you ensure that even deployment itself is covered by tests, minimizing errors.

Traditionally, quant teams are led by finance professionals who may lack software-engineering experience and are unfamiliar with testing and CI/CD. That is exactly why, after finishing my book *Efficient Python Programming in Practice*, I specifically invited two leading figures from the finance world to endorse it. Having worked in quant finance for many years, I know this field desperately needs systematic software-engineering methods to ensure software quality.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/girl-reading.png)

Second, turn off all auto-updates. In production, any automatic update is extremely dangerous and must be disabled. Only updates that have passed rigorous testing should be applied.

Third, always use staged rollout when updating systems.

On deployment, CrowdStrike made a major mistake this time by not implementing staged rollout. In fact, security software runs with very high privileges, so once something goes wrong, it often causes very severe failures. That makes staged rollout especially critical.

If CrowdStrike had implemented staged rollout — for example, deploying to just 1% of machines at first and monitoring the results after the upgrade, as data collection is part of canary releases, then gradually expanding the rollout only when no errors were reported — this massive incident could have been avoided entirely.

Staged rollout applies to quant systems too. On August 1, 2012, Knight Capital deployed new trading software on Nasdaq, but due to insufficient testing, the software triggered a cascade of erroneous orders upon activation, losing about $440 million in 45 minutes. It ultimately led to the firm being acquired by Jefferies Group.

<div style='width:75%;text-align:center;margin-bottom:1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/knight-capital-case.jpg' style="box-shadow:0 2px 5px rgba(0,0,0,0.3)">
<span style='font-style:italic;font-size:0.8rem'>Knight Capital Case Report</span>
</div>

In hindsight, properly implemented staged rollout could have completely avoided such a mistake.

>For the nitpickers: this is a complicated story. In short, it's not that staged rollout wasn't implemented, but that it wasn't implemented correctly.

Futures traders often say you make money 90% of the time — it's the less than 1% of extreme tail events that wipe you out.

Fourth, build a controllable system.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/i-robot.jpg)

If your signal system is built on AI models, then your risk-control model must not be built on a black box. Always set circuit breakers and stop out unconditionally when triggered — yes, this may cause other quants to stop out alongside you, but on the flip side, if you run too late, you will be the one getting buried.

Fifth, no matter how advanced the system, never leave it unattended. Even with a fully automated quant system, don't lay off all your manual traders. If you visit the power plant at the Three Gorges Dam, you'll see that power generation is highly automated, yet the operators in front of the monitors still work in strict shifts.
