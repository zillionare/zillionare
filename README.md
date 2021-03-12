![](http://images.jieyu.ai/images/hot/zillionbanner.jpg)

<h1 align="center">大富翁AI量化社区欢迎您!</h1>

<p align="right">
<a href="https://zillionare.readthedocs.io/zh_CN/latest/?badge=latest"><img src="https://readthedocs.org/projects/zillionare/badge/?version=latest"></img></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>


Zillionare（大富翁）是一个分布式高速量化交易框架。它基于Python 3.8以上版本构建，使用了异步IO和微服务技术，其目标是：

- 分布式高速量化计算平台，算力可根据需要无缝扩展
- 行情数据本地化存储，低延时同步，轻松支持实时触发分钟级别以上交易信号
- 支持私有化部署，保护您的策略
- 虚拟化部署，更易维护
- 诸多量化因子
- 基于机器学习的交易策略
- 基于深度学习的交易策略
- 高速回测框架

!!! Note

    大富翁有基础版和专业版两个版本。基础版完全开源、终生免费。专业版提供丰富的交易策略和定制功能。各个版本的功能发布进度请参考[[FIXME]]。


# 大富翁的技术优势
    [[TODO: add introduce here]]
大富翁由一系列子项目组成：

## Omicron

[Omicron](https://github.com/zillionare/omicron>) 提供了数据的本地存储读写和其它基础功能，比如交易日历和时间，Triggers，类型定义等。它是zillionare各子项目依赖的数据访问sdk。在您安装了Omega服务器之后，就通过Omicron这个sdk来使用行情数据。

[使用文档](https://zillionare-omicron.readthedocs.io/zh_CN/latest/>) [项目地址](https://github.com/zillionare/omicron)

## Omega

[Omega](https://github.com/zillionare/omega>) 是基于Sanic构建的微服务，它通过行情适配器来收发数据，通过Omicron来将这些数据存储到本地。Omega也是行情同步任务的管理者。

通过前置Nginx，就可以分布式方式提供行情数据服务。

[使用文档](https://zillionare-omega.readthedocs.io/zh_CN/latest) [项目地址](https://github.com/zillionare/omega)

## Alpha 

策略服务器。运行定义的各种策略，并发出交易信号。

## Epsilon 

Web控制台

## Gamma

交易网关。接收Alpha发出的交易信号，执行交易。这部分也可以集成在Alpha中。

## jqadaptor

JoinQuant行情数据适配器。

# 项目状态

截止2020年11月，大富翁已通过Omega提供高速分布式行情服务。部署Omega之后，即可通过Omicron（行情数据访问SDK）来请求行情数据和市值数据。


| 项目名称  | 最新版本 | 状态  | 说明                 |
|-----------|----------|-------|--------------------|
| Omega     | 0.6      | alpha | 高速分布式行情服务器 |
| Omicron   | 0.6      | alpha | 行情数据SDK          |
| jqadaptor | 0.2.x    | alpha | Joinquant行情适配器  |


## 更多

进一步了解大富翁，请跳转到 [文档](https://zillionare.readthedocs.io/en/latest/) 进一步阅读，谢谢！

## 加入社区

 * QQ群: 142961883
 * 头条号: 解语科技
 * 知乎圈子： Python与量化交易

<p align="center">
<img src="http://images.jieyu.ai/images/hot/qq.png" height="72px">
<img src="http://images.jieyu.ai/images/hot/logo-128-transparent.png" height="72px">
<img src="http://images.jieyu.ai/images/hot/quant-logo.jpg" height="72px">
</p>


