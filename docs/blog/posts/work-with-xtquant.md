---
date: 2023-12-22
title: QMT/XtQuant 之开发环境篇
slug: how-to-setup-xtquatn-development-env
lunar: 冬至
motto: 宜吃汤圆 必成双成对
tags:
    - quantlib
---

!!! tip 笔记要点
    1. XtQuant 获取及安装
    2. XtQuant 工作原理 （图2）
    3. 版本和文档一致性问题 （图3）
    4. 使用 VsCode 远程开发

<!--more-->

## 获取及安装

XtQuant 是可以脱离 QMT 运行的行情和交易接口库，即右图中对应的“原生 Python”概念。它没有 wheels 格式的安装包，要安装它，我们要到迅投的官网上 [下载](http://dict.thinktrader.net/nativeApi/download_xtquant.html) 源代码包。XtQuant 使用了打包日期来标识版本。

![R50](https://images.jieyu.ai/images/2023/12/think-trader-wiki.png)

下载下来的是一个 zip 包，里面有一些 python 文章和 windows dll 文件。它能支持从 3.8 到 3.11 的各种版本，这一点相对于其它产品，是有一定优势的地方。XtQuant 文档中暗示它可以安装在 Linux 上，但没有足够的文档和用例，所以建议暂时不要尝试这种方式。

---

我们的建议是，就与 QMT 安装在同一台 Windows 机器上，但要先创建虚拟环境。

创建虚拟环境的方式是通过 Conda（假定虚拟环境名为 myquant)

```bash
conda create -n myquant python=3.10
```

创建好虚拟环境之后，运行以下命令，找到 site-packages 目录：

```bash
conda run -n myquant python -m site
```

如果你要进一步学习 Conda 命令，可以阅读 [《Python 能做大项目》](http://www.jieyu.ai/articles/python/best-practice-python/chap01/) 这本书。上面的命令将输出：

```bash
D:\\conda\\envs\\myquant\\lib\\site-packages
```

现在，把解压缩后的包拷贝到 site-packages 目录下，安装就完成了。注意目录名为 xtquant，该目录下应该有一个名为__init__.py 的文件。如果不是这样，那么你解压缩时做错了。

## XtQuant 的工作原理

仅仅从迅投官网下载 XtQuant 并安装，是无法让 XtQuant 正常工作的。

XtQuant 实际上是一个代理，它需要与 QMT 客户端合作，才能完成数据下载与交易。在调用 XtQuant 的 API 时，XtQuant 会创建与 Qmt 的 socket 通讯，把用户请求转发给 Qmt 来完成。Qmt 软件在网上无法下载，你必须找一个券商开设账户，然后才能从客服处拿到软件。

安装 Qmt 后，必须保证 Qmt 或者 Qmt-mini 始终在线。否则，XtQuant 也无法正常工作。

## 版本和文档一致性问题

迅投是软件开发商，最终为我们提供服务的，是采购了 QMT 及 XtQuant 
---

的券商。可能因为这种原因，导致我们从迅投官网上下载的 XtQuant 版本，券商服务端还没升级，因此，文档里提到的新功能和 bug 修复，暂时仍然不可用。

比如，在 20231209 这个版本中，增加了 get_etf_info 及获取历史涨跌停数据。但截止 12 月 20 日，有的券商的客户还不能使用这些新的接口。如果你调用这些 API，会抛出"function not realize"的错误。

## 使用 VsCode 远程开发

如果你使用的是 Windows 做开发机，可以不看这一部分。如果你使用的

![R33](https://images.jieyu.ai/images/2023/12/remote-explorer-on-sidebar.png)

是 Linux 或者 Mac 作为开发机，是可以不远程登录到安装 QMT 的 windows
机器，而直接在本地机器上进行开发的。

基本步骤是：

1. 在 windows 上安装 openssh server。也有可能您的机器上已经安装过了
2. 在 vscode 中，点击 Remote Explorer
3. 如标号 2 所示，点击添加远程 windows 机器。
4. 此后的每次连接都需要输入密码。您也可以设置通过密钥认证方式，实现免密登录，可以参考 [微软官方文档](https://code.visualstudio.com/docs/remote/ssh#_getting-started)

