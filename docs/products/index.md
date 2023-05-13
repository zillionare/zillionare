!!! info "大富翁量化框架"
    大富翁是一款量化交易软件。它提供行情数据同步、量化因子、回测框架（驱动、撮合和图表）、交易客户端、模拟服务器及实盘接口。

一些朋友关注了本项目，也接到一些咨询。关于本项目状态进行一些说明。本项目1.0版于2022年初发布，当前仍然可用，但只提供了以下功能：

1. Omega服务器，进行行情数据同步和保存。行情数据保存在redis中（受限于物理内存容量，建议只存到30分钟），财务数据保存在postgres中
2. Omicron数据SDK。SDK提供了对行情数据的存取，以及证券列表的运算、日期时间的计算等。
3. 基于docker compose的部署

## 2.0的状态
2.0已经开发完毕，在公司内部使用已超过9个月，代码也开源了，但对外发布之前，还有不少工作要做，主要是：

1. 文档补全
2. 安装部署补全
3. 部分维护工作（特别是由于第三方造成的数据维护）还需要进一步自动化和智能化。

预计这个开源发布还要等较长时间，目前我们只为商业合作伙伴提供咨询、培训和部署服务（基于全部或者部分组件）。

## 2.0的功能
1. Omega服务器，盘中提供1分钟行情及实时行情（延时低至5秒）。数据存储使用了InfluxDB（时间序列数据库）和minio。在公司内部，我们已保存了超过30亿条行情数据（按关系型数据库的记录概念算），即从2005年以来的每一分钟数据。
2. Omicron数据SDK。接口基本同1.0版，主要是实现上，由对接redis改为从InfluxDB中取数据
3. backtesting server。提供回测时的交易撮合（使用分钟线，更准确）、账户管理和回测指标计算。
4. trader server。提供一个标准化的交易服务器，并且使用与backtesting server一样的API。 trader server通过各种adaptor来对接券商实盘API。
5. trader client。对接trader server和backtesting server的交易客户端。
6. Alpha research platform。投研平台界面及通用算法因子等。
7. Pluto（暂未开源），内部使用的策略和算法。基于这些算法，我们的一个内部实盘在2021年取得年代156%的最高收益。
## 1.0
关于1.0，请见[1.0](1.0.md)

### [Omega](https://github.com/zillionare/omega)
Omega是大富翁的数据服务器，将上游数据源提供的数据实时本地化。

### [Omicron](https://zillionare.github.io/omicron)
Omicron是大富翁的核心模块，提供了数据访问API，策略基类，K线图绘制、日历和证券列表运算、回测收益图绘制等功能。
### [Backtesting](https://zillionare.github.io/backtesting)
Backtesting是大富翁的回测服务器，提供了回测时的撮合功能。
### [Trader-Client](https://zillionare.github.io/trader-client/)
大富翁交易客户端。一套API，提供回测、模拟和实盘接口。
### [Trader-server](https://github.com/zillionare/trader-server)
大富翁交易网关，提供模拟盘和实盘接口。

## 公共模块库
### [Cfg4Py](https://pypi.org/project/cfg4py/)

Cfg4Py是一个Python库，用于解析和管理您的配置文件。它提供以下功能：

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

### [Pyemit](https://github.com/zillionare/pyemit)
提供了基于redis的简单易用的进程间消息通讯机制和简易RPC服务。

## 开发环境构建
### [Python开发环境Docker镜像](https://hub.docker.com/r/zillionare/python-dev-machine)

您的开发环境最好构建在容器之中。这样做有以下好处：

1. 始终使用一致的开发环境，可以提高开发效率。
2. 测试时往往需要干净的环境，通过使用镜像，我们可以随时构建一个新的、干净的容器来执行测试。
3. 防止开发中误删除文件。如果是在容器中发生误删除文件的操作，最多也就损坏了容器本身，不至于要重装系统。

这个镜像包括以下功能：

1. ssh服务器
2. git, python3, wget, vim, miniconda
3. 安装了redis和postgres

## 安装
```
    docker pull zillionare/python-dev-machine
```

### [Python Project Wizard](https://zillionare.github.io/cookiecutter-pypackage)

配套《Python能做大项目》开发的Python Project Wizard。通过Wizard，可以快速创建一个Python项目的框架，并具有以下功能：

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

安装:
```
ppw
```

