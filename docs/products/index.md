<h1>大富翁开源产品系列</h1>

## 大富翁 (Zillionare )

大富翁是可以本地部署的开源量化框架，功能齐全，能容纳超大规模数据（目前在生产环境已存储超35亿条行情数据）。

### 功能和特性
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>
1. 分体式回测系统设计，策略回测与实盘交易使用**完全一致**的API，无须更改
2.  更精准的成交量匹配算法（需要分钟级数据）
3.  基于InfluxDB的高性能本地量化平台，能容纳海量数据
    * 通过聚宽jqdatasdk持续同步行情数据（延时1分钟）
    * 基于akshare获得延时小于5秒的实时行情数据
* 基于容器技术构建和部署，运行稳定
* 基于Jupyter Lab的研究环境
* 提供大量量化必用API：
    * 时间运算库，比如两个交易时间帧(frame)之间有多少个帧？从某个时间帧起，向前移动n个帧，得到的时间是？
    * 证券列表运算库。比如按名字模糊查找，按板块提取列表等，支持include/exclude运算。
    * 时间序列特征运算库。比如cross（金叉），find_runs（寻找连续值）、low_range（n周期以来最小值）等
    * 绘图。提供交互式k线图、策略报告。
    * 策略基类。基于该基类，实现自己的策略最简单只需要实现一个函数
* Trader client提供回测与实盘一致的交易API
* 大量详实、精准的文档
* 项目基于Python Project Wizard搭建质量保证及CI/CD体系，符合社区最佳实践。

### 架构和组件

<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>
大富翁量化框架由以下主要组件（服务）构成：

![75%](https://images.jieyu.ai/images/2023/11/zillionare-deployment.png)

* [Omega](https://github.com/zillionare/omega)是大富翁的数据服务器，将上游数据源提供的数据实时本地化。

* [Omicron](https://zillionare.github.io/omicron)是大富翁的核心模块，提供了数据访问API，策略基类，K线图绘制、日历和证券列表运算、回测收益图绘制等功能。
* [Backtesting](https://zillionare.github.io/backtesting) Backtesting是大富翁的回测服务器，提供了回测时的撮合功能。
* [Trader-Client](https://zillionare.github.io/trader-client/) 大富翁交易客户端。一套API，提供回测、模拟和实盘接口。
* [gm-adaptor](https://github.com/zillionare/trader-gm-adaptor) 大富翁交易网关，提供实盘交易接口（需要开通东财量化权限）。


除大富翁之外，我们还提供了其它开源库，比较重要的有：

## 项目生成向导

[Python Project Wizard](https://zillionare.github.io/cookiecutter-pypackage)是一个Python项目模板创建工具。通过Wizard，可以快速创建一个Python项目的框架，并具有以下功能：

* [Poetry]  通过Poetry来管理版本、依赖、构建和发布
* [Mkdocs] 撰写基于Markdown的文档，常见扩展也已经配置
* [Pytest] 使用Pytest进行单元测试（unittest仍然支持，并且直接可用）
* [Codecov] 生成coverage report，并且由[Codecov]背书，开源项目必备
* [Tox] 对代码进行矩阵化测试（包含风格检查和语法检查）
* 使用[Black] 和 [Isort]格式化代码
* 使用[Flake8] 和 [Flake8-docstrings]对代码和docstrings进行语法检查
* [Pre-commit hooks] 代码提交前强制进行风格和语法检查，以及格式化
* [Mkdocstrings] 自动生成API文档
* 生成基于[Python Fire]的命令行接口
* 已配置好Github持续集成，包括以下功能：
    - 集成测试
    - 集成测试通过后，自动发布dev build到testpypi，供测试
    - 检测到新的tag（以字母v开头）后，从release分支上自动发布文档和wheels包
    - 自动提取change log到release Notes
    - 自动发布github release
* 使用git pages来托管文档

安装：
```
pip install ppw
```
  
## 配置管理

[Cfg4Py](https://pypi.org/project/cfg4py/)是一个Python库，用于解析和管理您的配置文件。它提供以下功能：

1. 将yaml格式的配置文件解析成为一个Python对象，从而您可以使用属性访问语法，而不是繁琐易错的字典访问语法来使用配置项。并且由于这一特性，使得IDE代码提示和自动完成成为可能。这样，您不再需要记忆众多配置项了。
2. 自适应安装环境支持。支持您为生产环境、开发环境和测试环境生成独立的配置文件。
3. 层次式配置。您可以使用一个中央配置源（比如redis缓存），然后用本地文件来覆盖某些选项。这在查错和维护时非常有用。
4. 配置模板。要连接数据库，不知道连接串应该如何写？Cfg4Py可以帮您。Cfg4Py为常用的框架提供了配置模板，您可以通过`cfg4py scaffold`来选择生成哪些配置项。
5. 热更新。配置文件修改后，无需重启服务，自动更新。
6. 宏功能。自动使用环境变量来替换配置项中的宏。

安装:
```
pip install cfg4py
```

## 开发环境构建

[Python开发环境Docker镜像](https://hub.docker.com/r/zillionare/python-dev-machine)

您的开发环境最好构建在容器之中。这样做有以下好处：

1. 始终使用一致的开发环境，可以提高开发效率。
2. 测试时往往需要干净的环境，通过使用镜像，我们可以随时构建一个新的、干净的容器来执行测试。
3. 防止开发中误删除文件。如果是在容器中发生误删除文件的操作，最多也就损坏了容器本身，不至于要重装系统。

这个镜像包括以下功能：

1. ssh服务器
2. git, python3, wget, vim, miniconda
3. 安装了redis和postgres

安装
```
    docker pull zillionare/python-dev-machine
```

## 进程间消息

[Pyemit](https://github.com/zillionare/pyemit) 提供了基于redis的简单易用的进程间消息通讯机制和简易RPC服务。

