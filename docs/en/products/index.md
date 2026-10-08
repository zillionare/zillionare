---
title: "Zillionare: Open-Source Quant Framework for Large-Scale Data"
date: "2026-10-09"
slug: en/articles/products/index
tags: [Quant Framework, Open Source, Backtesting, Python]
excerpt: "Zillionare is a deployable open-source quantitative framework supporting massive data storage (3.5B+ records). It features unified backtest/live APIs, InfluxDB integration, and a modular architecture for robust quantitative investing."
lang: en
translation_of: articles/products/index
auto_translated: true
source_sha: ed32f7a85b26c925781db314b6e701454594618c
---

## Zillionare

Zillionare is a locally deployable, open-source quantitative framework. It is fully featured and capable of handling ultra-large-scale datasets (currently storing over 3.5 billion market data records in production).

### Features
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>
1. **Decoupled backtest architecture**: Strategy backtesting and live trading use **identical** APIs, requiring no code changes.
2. **Precise volume matching algorithm**: Optimized for minute-level data.
3. **High-performance local platform based on InfluxDB**: Designed to handle massive data volumes.
    * Continuous synchronization of market data via JQData SDK (1-minute delay).
    * Real-time market data with <5-second latency via AKShare.
4. **Containerized deployment**: Built and deployed using container technology for stability.
5. **Jupyter Lab-based research environment**.
6. **Comprehensive quantitative APIs**:
    * **Time operations**: Calculate frames between two trading time frames, or shift forward by *n* frames from a specific time frame.
    * **Security list operations**: Fuzzy search by name, extract lists by sector, etc., supporting `include`/`exclude` operations.
    * **Time-series feature operations**: Functions such as `cross` (golden cross), `find_runs` (finding continuous values), `low_range` (minimum value over *n* periods), etc.
    * **Visualization**: Interactive K-line charts and strategy reports.
    * **Strategy base class**: Implementing your own strategy is as simple as overriding one function.
7. **Trader Client**: Provides a unified trading API for backtesting, simulation, and live trading.
8. **Extensive, precise documentation**.
9. **Quality assurance & CI/CD**: Built using Python Project Wizard, adhering to community best practices.

### Architecture and Components

<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>
The Zillionare quantitative framework consists of the following main components (services):

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/11/zillionare-deployment.png)

* [Omega](https://github.com/zillionare/omega): The data server for Zillionare, localizing data from upstream sources in real-time.
* [Omicron](https://zillionare.github.io/omicron): The core module of Zillionare, providing data access APIs, strategy base classes, K-line charting, calendar and security list operations, and backtest return plotting.
* [Backtesting](https://zillionare.github.io/backtesting): The backtesting server for Zillionare, providing matching functionality during backtests.
* [Trader-Client](https://zillionare.github.io/trader-client/): The trading client for Zillionare. A single API providing interfaces for backtesting, simulation, and live trading.
* [gm-adaptor](https://github.com/zillionare/trader-gm-adaptor): The trading gateway for Zillionare, providing live trading interfaces (requires East Money quantitative trading permissions).

In addition to Zillionare, we provide other open-source libraries, including:

## Project Wizard

[Python Project Wizard](https://zillionare.github.io/cookiecutter-pypackage) is a tool for creating Python project templates. Through the Wizard, you can quickly scaffold a Python project framework with the following features:

* [Poetry]: Manages versions, dependencies, builds, and releases.
* [Mkdocs]: Writes Markdown-based documentation, with common extensions pre-configured.
* [Pytest]: Performs unit tests (unittest is still supported and directly usable).
* [Codecov]: Generates coverage reports, endorsed by [Codecov], essential for open-source projects.
* [Tox]: Performs matrix-based code testing (including style and syntax checks).
* Code formatting using [Black] and [Isort].
* Syntax checking for code and docstrings using [Flake8] and [Flake8-docstrings].
* [Pre-commit hooks]: Enforces style and syntax checks, as well as formatting, before code commits.
* [Mkdocstrings]: Automatically generates API documentation.
* Generates command-line interfaces based on [Python Fire].
* Pre-configured GitHub Continuous Integration, including:
    - Integration testing.
    - Automatic publishing of dev builds to TestPyPI for testing upon successful integration tests.
    - Automatic publishing of documentation and wheels from the release branch upon detecting new tags (starting with 'v').
    - Automatic extraction of change logs to release notes.
    - Automatic publishing of GitHub releases.
* Documentation hosted via GitHub Pages.

Installation:
```
pip install ppw
```
  
## Configuration Management

[Cfg4Py](https://pypi.org/project/cfg4py/) is a Python library for parsing and managing configuration files. It provides the following features:

1. **Object-based configuration**: Parses YAML configuration files into Python objects, enabling attribute access syntax instead of cumbersome and error-prone dictionary access. This also enables IDE code hints and auto-completion, eliminating the need to memorize numerous configuration items.
2. **Environment-adaptive installation**: Supports generating independent configuration files for production, development, and test environments.
3. **Hierarchical configuration**: Allows using a central configuration source (e.g., Redis cache) while overriding specific options with local files. This is very useful for debugging and maintenance.
4. **Configuration templates**: Unsure how to write database connection strings? Cfg4Py helps. It provides configuration templates for common frameworks, allowing you to generate specific configuration items via `cfg4py scaffold`.
5. **Hot reloading**: Automatically updates configurations upon file modification without restarting the service.
6. **Macro functionality**: Automatically replaces macros in configuration items using environment variables.

Installation:
```
pip install cfg4py
```

## Development Environment Setup

[Python Development Environment Docker Image](https://hub.docker.com/r/zillionare/python-dev-machine)

It is recommended to build your development environment within a container. This offers the following benefits:

1. **Consistent development environment**: Ensures consistent setups, improving development efficiency.
2. **Clean test environments**: Facilitates testing by allowing the creation of new, clean containers for each test run.
3. **Prevention of accidental data loss**: Accidental file deletion in a container only affects the container itself, avoiding the need to reinstall the operating system.

This image includes the following features:

1. SSH server.
2. Git, Python3, wget, vim, Miniconda.
3. Redis and PostgreSQL installed.

Installation:
```
    docker pull zillionare/python-dev-machine
```

## Inter-Process Messaging

[Pyemit](https://github.com/zillionare/pyemit) provides an easy-to-use inter-process messaging mechanism and simple RPC services based on Redis.
