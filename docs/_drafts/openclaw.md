---
title: 安全养虾，免费养虾
---

养龙虾的关键担忧有两个，安全和费用。

无论是把龙虾安装在主力工作机还是备用工作机上，其实都不安全。这有两层意思，一是担心它过于强大，破坏我们的系统，导致机器无法正常工作；二是担心它突破安全限制，盗取我们的资产、秘密。

要解决这两个问题，其实最好是把它安装在虚拟机中。这样即使系统损坏，也可以一键恢复。另外，小龙虾也无法突破虚拟机的安全机制，所以不担心它盗取我们的账号等秘密资产。当然这一点并不绝对，如果你不共享任何账号、秘密（比如大模型的订阅 key），它也无法完成任何工作。

但是，安装在虚拟机中只后，我们可以从一个干净的环境开始，明确自己要分享哪些关键信息，从而做到风险可控。


关于费用问题，我尝试运行了一下之后，发现 token 消耗确实很快。刚开始的时间都是花在寻找免费或者非常低廉的大模型服务商上。不过，最后算是找到了现阶段最好的方案。

## 虚拟机养虾方案

!!! tip
    OpenClaw 刚开始安装可能会觉得有点麻烦。但无论如何，也不要找不可信的第三方服务，要坚持从官方下载安装。我就在 hub.docker.com 上发现了一个名为0penclaw 的账号，发布 openclaw 的 docker 镜像。可想而知，他们的目的是什么。

Openclaw 官方支持两种安装方式，一种是本地安装；另一种是通过 docker 容器来使用。不知何故，第二种方式下，即使有一些预编译的 docker 镜像存在，你仍然要clone 整个openclaw 的仓库，再通过 scripts/docker/setup.sh 来构建一个本地镜像。

最初我一直以为它只是简单地拉取一些远程镜像。直到构建花了我很多时间，才发现它是从源码进行的本地 docker 镜像构建。由于它使用的 ubuntu 源、bun 源和 npm 源全在国外，所以构建花的时间很长、容易出错。

!!! attention
    如果你希望通过容器来运行 openclaw，在构建之前，记得先用 AI 改一下 Dockerfile，把国内源加进去。但是，在我尝试过之后，总算明白了为何官方并不推荐通过 docker 容器来运行。

所以，这里我就不再推荐 docker 方式，而是改用虚拟机方式。当你进入虚拟机后，只要先将 nodejs 安装到正确的版本，然后再通过以下命令安装 openclaw，整个过程会非常丝滑。

如果你使用 windows，使用自己熟悉的虚拟机软件就好，比如 vmware, virtualbox 等。

如果你的工作机是 mac，推荐使用免费的 orbstack 来创建虚拟机。Orbstack 是一个非常优秀的容器/虚拟机软件。

![orbstack 管理的 linux 虚拟机](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331124419.png)

选中虚拟机，在右边的面板有一个 Terminal 选项，就可以直接进入它的控制台。

在创建虚拟机时，最好创建 linux 系列的虚拟机，而不要使用 windows 的。

当 linux 虚拟机创建好之后，进入控制台，就可以执行以下命令安装：

```bash
# 安装 nodejs，确保使用 24以上版本
# 更新 npm 源为国内

curl -fsSL https://openclaw.ai/install.sh | bash
```

然后会进入配置，这个过程在 openclaw 中被称为 onboard，之后你仍然可以通过 `openclaw onboard`来再次进行设置。在进行设置之前，我们还要先准备好一些关键信息。

最关键的信息就是大模型由谁提供，它的配置界面如下：

![模型配置](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331124927.png)

我最初是选择了 openrouter，因为它有一些免费模型可用。但是，不知为何，几轮对话之后，就提示我产生了账单。所以，我开始寻找更明确的免费方案。

## 申请百炼免费额度

阿里的百炼平台为新注册用户提供了一定额度的免费 TOKEN。你要先在[百炼免费额度](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-usage/free-quota)这里开通：

![开启免费额度](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331125442.png)

如果你不想付费使用的话，**必须**开启『免费额度用完即停』选项，否则会有账单。

然后是要申请 API key, 从左侧的 Api Key 菜单进入，在右侧就有创建按钮：

![创建 API key](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331125727.png)

把新创建的 API key复制出来，再回到OpenClaw 的模型配置界面，选择 `Qwen (Alibaba Cloud Model Studio)这一项，就进入下面的选择菜单：

![Auth mode](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331130018.png)

在这里我们要选 Standard API Key for China 这一项。前面的 Coding Plan 目前是按月付费制，大约是200多一个月。再回车，就进入输入 api key 的地方：

![输入 API key](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331130211.png)

输入回车，就进行模型选择：

![选择模型](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331130517.png)

为了使用上所有的免费额度，可以都选上。如果你最终要使用openclaw 来编程，可能还是再付费购买 Claude 4.6更好。

!!! tip
    你可以随时通过 `openclaw configure --section models`来重新配置模型。

## 配置微信机器人

首先，我们要在微信 > 设置 > 插件下，启用微信ClawBot：

![微信 ClawBot](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/1bff573db2c7c804b09171e485aeb628.jpg)

继续在虚拟机的终端中输入：

```bash
npx -y @tencent-weixin/openclaw-weixin-cli@latest install
```

安装过程中可能遇到 clawhub 报告 rate limit 错误，这是因为同时安装的人太多了。稍等一下重试即可。

安装完成之后，我们就可以再设置 Channel，通过以下命令：

```bash
openclaw configure --section channels
```

现在我们会看到：

![选择 channel](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260331131033.png)


现在， openclaw-weixin 这个信道就出现在列表中了。选择它，回车，会出现一个二维码，此时使用微信扫码就可以了。



