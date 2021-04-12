# 大富翁

大富翁是一款量化交易软件。它提供行情数据同步、量化因子计算和基于机器学习（深度学习）的交易策略。

您可以通过pip来安装大富翁，也可以通过下面的安装文件来安装基于Docker的发行版。

=== "Linux"
    以可执行文件的方式提供，适用于Linux。
    
    您需要事先在机器上安装Docker-engine和Docker compose。请参见[安装指南](../installation.md#安装到Linux操作系统)。
    
    [点击这里下载](/download/zillionare_1.0.0.a6.sh?latest)

=== "Other OS"
    以压缩包方式提供，适用于其它操作系统。
    
    您需要事先在机器上安装Docker-engine和Docker compose。请参见[安装指南](../installation.md#安装到其它操作系统)。
    
    [点击这里下载](/downlooad/zillionare_1.0.0.a6.tar.gz?latest)

=== "Pip"
    您也可以通过Pip来分别安装各项服务。

    ```bash
    pip install zillionare-omega
    ```
    请参见 ==[TODO](404.md)==

# [Cfg4Py](https://pypi.org/project/cfg4py/)

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

# [Python Project Wizard](https://zillionare.github.io/cookiecutter-pypackage)

配套《Python最佳工程实践》开发的Python Project Wizard。通过Wizard，可以快速创建一个Python项目的框架，并具有以下功能：

1. 使用Poetry来管理项目版本和依赖，构建和发布到PyPI。
2. 使用Mkdocs和Markdown来写作文档。文档支持表格、图像、admonition等功能，并提供实时预览。
3. cascading quality control:
    - pre-commit hooks强制每次代码提交时进行语法和风格检查。
    - 本地执行通过tox命令，对支持的Python版本矩阵执行单元测试和Lint。
    - 集成Github Actions CI，在代码Push到Github后，自动运行CI
4. 自动发布版本到PyPI。当推送代码到release branch，并且带有tag时，CI会在测试通过后自动发布。
5. 使用Gitpages来托管文档。当文档推送到master, main或者release branch之后，自动构建并发布到git pages。
6. 使用flak8作为代码检查工具，black作为格式化工具。
7. 通过Codecov来托管测试覆盖报告，为您的开源程序提供信任徽章。
8. 提供基于google fire的命令行接口（可选）。

[安装说明](https://zillionare.github.io/cookiecutter-pypackage/tutorial/)


# [Python开发环境Docker镜像](https://hub.docker.com/r/zillionare/python-dev-machine)

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

[大富翁]: https://github.com/zillionare
[Cookiecutter]: https://cookiecutter.readthedocs.io/en/1.7.2/
