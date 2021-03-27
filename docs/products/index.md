
# 大富翁(zillionare)

大富翁是一款量化交易软件。它提供行情数据同步、量化因子计算和基于机器学习（深度学习）的交易策略。

您可以通过pip来安装大富翁，也可以通过下面的安装文件来安装基于Docker的发行版。

=== "Linux"
    以可执行文件的方式提供，适用于Linux。
    
    您需要事先在机器上安装Docker-engine和Docker compose。请参见[安装指南](../installation.md#安装到Linux操作系统)。
    
    [点击这里下载](/download/zillionare.sh?latest)

=== "Other OS"
    以压缩包方式提供，适用于其它操作系统。
    
    您需要事先在机器上安装Docker-engine和Docker compose。请参见[安装指南](../installation.md#安装到其它操作系统)。
    
    [点击这里下载](/downlooad/zillionare.tar.gz?latest)

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