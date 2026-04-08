---
title: 安全养虾，免费养虾
---


OpenClaw 的风终究还是吹到了我的书桌。经过短暂的研究，我的判断是，OpenClaw的风不会这么快就就停下来。实际上，正如黄仁勋所说，OpenClaw 可能是我们这个时代最重要的软件，它将成为 AI 时代的操作系统，所以，值得每一个人 all in openclaw。

不过，反对的声音也确实有它的道理，养龙虾确实太贵了，而且看上去很不安全。

经过几天的实践，我成功地解决了这个问题，实现了几乎零成本地和安全养虾。

## 小龙虾怎么就不安全了

小龙虾的不安全有两层意思。第一层是小龙虾可能被人操纵，从而盗取你的重要资料和秘密信息。第二层则是，小龙虾自己会用工具，但也可能因为误操作，导致你的硬盘文件被删，安装错了软件导致蓝屏等等。

这两天关于小龙虾安全的各种段子满天飞。其中有一个是这样的，说，如果有人要你

尽管小龙虾团队正在没日没夜地赶发版本，尝试各种安全加固。

无论是把龙虾安装在主力工作机还是备用工作机上，其实都不安全。这有两层意思，一是担心它过于强大，破坏我们的系统，导致机器无法正常工作；二是担心它突破安全限制，盗取我们的资产、秘密。

要解决这两个问题，其实最好是把它安装在虚拟机中。这样如果导致系统损坏，也可以通过虚拟机状态回滚来修复。另外，小龙虾也无法突破虚拟机的安全机制，所以不担心它盗取我们的账号等秘密资产。当然这一点并不绝对，如果你不共享任何账号、秘密（比如大模型的订阅 key），它也无法完成任何工作。

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



## 配置QQ 机器人

我个人更推荐同时配置 QQ 机器人。因为微信机器人不能在电脑上使用。如果龙虾养成了，当然我们可能更多地通过语音来指挥它，但在早期，或者在处理一些专业性很强的事务时，在电脑上使用还是更方便一些。

配置 QQ 机器人很简单，尽管扯到了什么开放平台、开发者之类的，但实际上很简单，你访问 q.qq.com，按提示创建一个 openclaw 机器人，拿到 appId 和 appSecret，然后回到 openclaw配置就好。

## 额外的安全性

openclaw 对外只有一个接口，就是默认监听在本地18789的 websocket 端口。从网络的角度来看是很安全的，但是，也存在我们安装了 skill 之后，skill 就自己打通一条新的信道，从而在你没有察觉的情况下，有别的人通过qq、微信来使用你的 openclaw 的情况。

因此，从4月1日的版本开始，加上了 pairing 这个功能。当你初次要求 openclaw 调用工具时，就可能遇到这个问题，说是需要先配对。

此时，你要回到 openclaw 的控制台，通过命令：

```bash
openclaw devices list
```

来查看：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260403130851.png)

然后你调用 `openclaw devices approve`命令，带上这个待批准的 Request ID就好了。只有过了这一步，你才能真正把龙虾用起来 -- 因为从现在起，龙虾才能用工具了。

接下来，你还会遇到调用工具时，逐次要求审批的情况：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260403132402.png)

这种情况下，你需要修改 openclaw.json（在~/.openclaw/目录下）

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260403132210.png)

## 财务安全

默认 openrouter 的配置，会配置 openrouter/auto作为缺省，而且不知道为什么在 openclaw onboard 时，它是一闪而过，让你注意不到。然后即使你配置了 openrouter/free，也仍然使用 openrouter/auto -- 这会导致计费。

我安装 openclaw，仅仅是一些排错，再加上发语音能力，还没有走通，就换了450万 qwen 3.6的 token 了。所以走付费的话，这个费用肯定是打不住的。

但是现在其实有很多好用的免费模型。比如 qwen 3.6 plus 现在处在 preview 阶段，在 openrouter 上就是免费的。另外像小米，之前 GLM 5在 preview 时也是这样。很可能后面新出的大模型，都会在 preview 阶段给一些免费试用时间，所以用好这个，基本不用担心 token 费用了。

但是在配置 openclaw 时，不能走它的 openclaw config的菜单命令，要直接配置：

```bash
openclaw models set openrouter/qwen/qwen3.6-plus:free
```

这样就直接设置了默认的模型了。

另外，openrouter 免费模型有两层，一个是如果你没有任何充值，那么每天可以调用50次 API，这个会很快用完；但如果你充值10$以上，并且保持账户余额超过10$，则每天可以调用1000次，基本上够用了。

这里有一个技巧，你在充值完成之后，要把 api key 的消费限额设置为一个很小的值，比如每月0.1$，这样就可以管很久了。

这个配置在 API tab里：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260403134239.png)

一天究竟要用多少 token? 我试用第一天，不到10个小时，用了3千多万 token：

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/20260403203222.png)

所以，一个 Agent，简单干活的话，要准备一个亿的 token。按流量买 token 肯定是很贵的。如果有便宜的按月付费的，就趁早拿下吧。另外，现在有一些大模型可以本地部署，也可以运行了。
