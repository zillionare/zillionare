---
title: "Zillionare: Open-Source Quant Framework for Large-Scale Data"
date: 2021-03-20
slug: en/articles/products/index
tags: [Quant Framework, Open Source, Backtesting, Live Trading]
excerpt: "Zillionare is a deployable open-source quantitative framework supporting massive data storage. It features consistent backtest and live trading APIs, high-performance local data servers, and comprehensive developer tools."
lang: en
translation_of: articles/products/index
auto_translated: true
source_sha: 7541ffb3f282acbfe76798df8d348cafb443eedf
---

## Zillionare

Zillionare is a locally deployable, open-source quantitative framework with full functionality, capable of handling ultra-large-scale data (currently storing over 3.5 billion market data records in production).

### Features and Capabilities
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

1. Decoupled backtesting system design: Strategy backtesting and live trading use the **identical** API, requiring no code changes.
2. More precise volume-matching algorithm (requires minute-level data).
3. High-performance local quantitative platform based on InfluxDB, capable of handling massive data:
    * Continuous synchronization of market data via JueQuan’s `jqdatasdk` (1-minute delay).
    * Real-time market data with less than 5-second delay via AKShare.
* Container-based construction and deployment for stable operation.
* Jupyter Lab-based research environment.
* Extensive essential quantitative APIs:
    * Time-series operations: e.g., calculating the number of frames between two trading time frames, or determining the time after moving forward by $n$ frames from a specific frame.
    * Security list operations: e.g., fuzzy search by name, extracting lists by sector, supporting `include`/`exclude` operations.
    * Time-series feature operations: e.g., `cross` (golden cross), `find_runs` (finding continuous values), `low_range` (minimum value over $n$ periods), etc.
    * Plotting: Interactive candlestick charts and strategy reports.
    * Strategy base class: Implementing your own strategy is as simple as implementing one function based on this base class.
* Trader client provides a consistent trading API for backtesting and live trading.
* Extensive, detailed, and precise documentation.
* The project is built using Python Project Wizard, incorporating quality assurance and CI/CD systems that align with community best practices.

### Architecture and Components

<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

The Zillionare quantitative framework consists of the following main components (services):

![75%](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/11/zillionare-deployment.png)

* [Omega](https://github.com/zillionare/omega) is Zillionare’s data server, localizing data from upstream sources in real-time.
* [Omicron](https://zillionare.github.io/omicron) is Zillionare’s core module, providing data access APIs, strategy base classes, candlestick charting, calendar and security list operations, and backtest return plotting.
* [Backtesting](https://zillionare.github.io/backtesting) is Zillionare’s backtesting server, providing matching functionality during backtests.
* [Trader-Client](https://zillionare.github.io/trader-client/) is Zillionare’s trading client. A single API provides interfaces for backtesting, simulation, and live trading.
* [gm-adaptor](https://github.com/zillionare/trader-gm-adaptor) is Zillionare’s trading gateway, providing live trading interfaces (requires East Money quantitative permissions).

In addition to Zillionare, we offer other open-source libraries, including:

## Project Generation Wizard

[Python Project Wizard](https://zillionare.github.io/cookiecutter-pypackage) is a tool for creating Python project templates. With the Wizard, you can quickly scaffold a Python project framework with the following features:

* [Poetry] Manages versions, dependencies, builds, and releases.
* [Mkdocs] Writes Markdown-based documentation, with common extensions pre-configured.
* [Pytest] Performs unit testing (unittest is still supported and directly usable).
* [Codecov] Generates coverage reports, endorsed by [Codecov], essential for open-source projects.
* [Tox] Performs matrix testing of code (including style and syntax checks).
* Code formatting using [Black] and [Isort].
* Syntax checking for code and docstrings using [Flake8] and [Flake8-docstrings].
* [Pre-commit hooks] Enforce style and syntax checks, as well as formatting, before code commits.
* [Mkdocstrings] Automatically generates API documentation.
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

[Cfg4Py](https://pypi.org/project/cfg4py/) is a Python library for parsing and managing your configuration files. It provides the following features:

1. Parses YAML configuration files into Python objects, allowing you to access configuration items using attribute access syntax instead of cumbersome and error-prone dictionary access. This feature also enables IDE code hints and auto-completion, eliminating the need to memorize numerous configuration items.
2. Adaptive environment support. Supports generating independent configuration files for production, development, and testing environments.
3. Hierarchical configuration. You can use a central configuration source (e.g., Redis cache) and override certain options with local files, which is very useful for debugging and maintenance.
4. Configuration templates. Unsure how to write database connection strings? Cfg4Py can help. Cfg4Py provides configuration templates for common frameworks; you can use `cfg4py scaffold` to select which configuration items to generate.
5. Hot reloading. Automatically updates upon configuration file modifications without restarting the service.
6. Macro functionality. Automatically replaces macros in configuration items using environment variables.

Installation:
```
pip install cfg4py
```

## Development Environment Setup

[Python Development Environment Docker Image](https://hub.docker.com/r/zillionare/python-dev-machine)

It is recommended to build your development environment within a container. This offers the following benefits:

1. Consistent development environments improve development efficiency.
2. Testing often requires clean environments. Using images allows us to build new, clean containers for testing at any time.
3. Prevents accidental file deletion during development. If files are deleted in a container, it only affects the container itself, avoiding the need to reinstall the operating system.

This image includes the following features:

1. SSH server.
2. git, python3, wget, vim, miniconda.
3. Pre-installed redis and postgres.

Installation:
```
    docker pull zillionare/python-dev-machine
```

## Inter-Process Messaging

[Pyemit](https://github.com/zillionare/pyemit) provides a simple and easy-to-use inter-process messaging mechanism and lightweight RPC service based on Redis.
