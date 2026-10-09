---
title: "Quantstats Reloaded: Fixing Python 3.12 Compatibility"
date: 2025-06-16
slug: en/posts/tools/quantstats-reloaded
tags: [Quantstats, Python, Backtesting, Maintenance]
excerpt: "Quantstats is a popular Python library for trading strategy performance analysis, but it has become nearly unusable on recent Python versions due to lack of maintenance. We introduce quantstats-reloaded to resolve critical compatibility issues."
lang: en
translation_of: posts/tools/quantstats-reloaded
auto_translated: true
source_sha: 81cf99f97b1ea6334572fe531aad2d7a6ea93bbd
cover: "tags: [python, quantstats]"
---

Quantstats is a Python library for trading strategy performance analysis, highly favored by the quantitative community, with over 5.8k stars on GitHub. Unfortunately, due to long-term lack of maintenance by the original author, newly installed Quantstats packages, especially on Python 3.12 and higher, are nearly unusable.

We have brought an update.

---

<div style='width:500px;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/Ran-Aroussi.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

Quantstats is an open-source project by Ran Aroussi, a software developer, financial innovator, and independent entrepreneur. He has created several popular Python libraries, including the widely known YFinance (17.9k stars) and Quantstats. He also founded Tradologics, a cloud-based platform for algorithmic trading. Currently, he is also a podcaster, hosting the show 'Old School, New Tech'.

Like us at Kuangti, he is dedicated to 'creating tools to help people work smarter,' sharing 'actionable tips, real-world strategies, and insider stories on coding, indie development, finance, and entrepreneurship.'

It is likely that due to his involvement in too many activities, he had to neglect the maintenance responsibilities for this well-known project. The last update was 8 months ago. Since then, the community has submitted numerous issue reports. For example, when using Python 3.12 (new installations on other versions may also encounter this), you might face the following error:

![issue 416](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/quantstats-issue-416.jpg)

This is an issue that occurs specifically in Jupyter Notebooks, primarily due to an upgrade in `nbformat`. After fixing this issue, you might still encounter the following error:

![issue 420](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/06/quantstats-issue-420.jpg)

For months, despite the community continuously submitting fixes, the author has not had time to release a new version. This is likely because the original Quantstats lacks unit tests and CI (Continuous Integration), requiring manual testing for every release, which is extremely tedious and difficult for the author to manage.

In Kuangti’s quantitative courses, we also recommend Quantstats to students. To ensure a good experience for our students, we decided to take over the maintenance of Quantstats and released a new package called `quantstats-reloaded` (the original package can only be published by Ran Aroussi).

If you are also affected by Quantstats issues, please use `quantstats-reloaded`. This version not only fixes bugs such as #416 and #420 but also undergoes the following refactoring:

!!! Abstract
    1. Removed the dependency on `yfinance`,改用 synthetic data for testing, significantly improving test reproducibility.
    2. Switched to `poetry` for dependency management, providing stricter, semantically versioned dependencies in the future.
    3. Added unit tests, increasing coverage from 0% to 21%.
    4. Dropped support for outdated Python versions (e.g., 3.6–3.9).
    5. Added multi-platform, multi-version testing frameworks and CI.

Considering the urgency of bugs like #416, we released this version early. Subsequent releases will be published after improving unit test coverage and passing multi-platform (mac, windows, linux) and CI (GitHub Actions) tests.

Now, please try:

```bash
pip install quantstats-reloaded
```
