---
title: 龙虾流量太贵？ 我一招搞定每天7500万词元
date: 2026-04-11
img: https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/coppertist-wu-42w64JPhABA-unsplash.jpg
excerpt: OpenClaw 是未来的操作系统。它非常强大，是你的第二大脑和智能装甲。但是，你可能正在未流量费用太贵而苦恼，却浑然不知，有人一天获得过7500万的免费 QWen 3.6的token.
category: tools
tags: [tools, openclaw, resources]
---

既然要运营和操作小龙虾（oplenclaw），Token 就是实打实的消耗品。我们最近深度测试了两个非常稳的大厂免费渠道，能直接调用顶级模型（比如 GLM-5），而且几乎没有额度限制，非常适合拿来跑小龙虾。

## 01 来自 OpenRouter的每日7000万

OpenRouter 最大的优势是聚合了几乎市面上所有的主流模型，且提供大量免费配额。我养龙虾的第二天，就完全领会了 OpenRouter 的玩法。当时 QWen 3.6正在免费使用期，我一天最高用到7500万的 Token，用完了整整一千次请求。

![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260411191423.png)


现在，QWen 3.6虽然不再免费提供了，但是仍然有一些非常不错的大模型仍在免费，非常值得一冲。

!!! tip
    OpenRouter 的免费模式始于去年3季度。大模型以免费方式提供访问一般有两个目的，一是商业宣传；另一个是新的模式在正式发布之前，需要大量真实的用例帮助他们微调。所以，请理直气壮地『免费』使用它们，帮助它们！

下面，我就像素级还原用上 OpenRouter 千万级免费 Token 的步骤。

#### 访问官网

输入网址 `https://openrouter.ai`。

![step1：进入OpenRouter界面](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/390bb2f6807b7acd82e9fb4d36af7314.jpg)

#### 登录账户

使用邮箱注册并确认（verify）登录。

![step2:成功注册登陆](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/e3e1cd2d2d821b2943a2f13b37739983.jpg)

#### 创建 API Key 与限额设置

在后台点击生成 API Key。现在，就可以用这个 key 来配置OpenClaw 的模型了。不过，你现在还有每日50次的限额。

根据官方文档，如果你购买10个 credits，每日上限就立刻调整到1000次 -- 这是实现养虾自由的关键！

购买 credits 之后，我们一定要防止误用了付费模型。所以，要像下面这样，设置『防火墙』：

![step3.3&step3.5&step3.9:API Key生成与限额设置](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/0024f396bf94684c69653c1dd9290e46.png)

在你购买 credits 之后，就可以编辑你的 API key,为它设置一个月度消耗最大值。这里设置为0.1就好了。

防火墙设好之后，接下来就是你做公益善事的时候了 -- 选择免费模型，帮他们测试吧！

#### 模型选择与计费逻辑
- **计费逻辑**：大模型通常是按 Token计费，Input（提示词）和 Output（生成内容）往往有不同的收费标准。
- **免费模型筛选**：选择免费模型时，关注 `Input: 0, Output: 0` 的模型。

按下图提示，找到 Prompt Pricing, 把价格区间设置为0，过滤大部分付费模型，然后注意选择 input/output 都是0的模型：

![step4.1:模型选择列表](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/d68e4742e47aed44da32ae583248b8d8.jpg)
![step4.5&step4.9:选择免费的模型](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/6d1e194aff579914d57d40ce7d55af6e.png)

#### 测试

![step5:点击chat可使用大模型](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/53998e9666b1e3d008a7f074201269fc.jpg)

在现阶段有这样一些模型（仅限免费）可以推荐：

- **养虾模型推荐**：
    - **Gemma 4 26B A4B**：速度极快，效果好，首选。
    - **NVIDIA: Nemotron 3 Super**：英伟达出品，免费且好用。
    - **OpenAI: gpt-oss-120b**：性能强，适合复杂的养虾指令。

## 02 顶级智力，不限额度，还得是老黄

当下开源模型中的顶流当属 GLM-5。如果能用上这个模型来养虾，还不用担心账单，生产力真是直线拉满。

英伟达说，我来！

这就是英伟达通过 AI Playground 服务。它提供了顶级智力模型比如 GLM-5, Kimi 2.5，无须绑信用卡，即可永久免费使用。在大大的诚意之外，我们也看到了黄仁勋的野望： 如果 OpenClaw 不做起来，几年之年，N 家的芯片卖给谁？

所以，相信这个『永久』的承诺，应该还有好几年的保鲜期。话不多说，我们接下来就看看如何接着老黄送出的大礼。

#### 访问官网

输入网址：`https://build.nvidia.com`。注意登录时，可能根据你的地域和语言设置发生重定向到别的 URL。我们没有详细测试，但这个免费服务应该只能在这个网址上申请。


![](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/04/20260411194605.png)

使用这里的大模型很简单，主要就是申请 Api Key，然后找到模型卡。我们先看注册。

#### 注册与验证

任何邮箱都可以注册。但要申请 Api Key，还得进行一次验证。这个验证需要通过短信验证。我们测试中，这一步对手机号没有限制。

1. **邮箱注册**：仅需邮箱即可。
2. **账号验证 (Verify)**：注册后必须点击上方的 Verify 进行验证，否则拿不到 API Key。
3. **手机号 Bug 处理**：验证时需要手机号。这里有一个小 bug, 你需要**手动把区号修改为 `+86`** 。填完后点击发送验证码即可。

![step2.1：注册后点击验证](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/d393125c0d45e74414e2697cb68a79c7.png)
![step2.5：手机号验证与区号修改界面](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/cd67c5026643192388341c05814ad153.png)

#### 生成 API Key

完成验证后，回到页面，点击右上角的**头像**，就会弹出一个“生成 API Key”的按钮。点击并保存好你的 Key，有了它就可以连接业务了。

![step3：英伟达API Key生成位置](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/c4c0692308788a98412a25ff9c6e4313.jpg)

#### 模型选择与限制

以下就是查模型 ID。这一步对熟悉大模型玩法的人来说可以不用看了。比如提到 GLM5大模型，老手可能知道，它几乎在所有平台上，id 都是 z-ai/glm5，所以，查模型 ID 这一步就可以省去了。

1. **选择模型**：在页面中找到 `models: glm-5`，这是我们目前推荐使用的顶级模型。
2. **访问限制**：目前英伟达不限额度，但会限制访问速度（RPM）：**每分钟不要超过 50 次**。这个调用次数基本上对所有人来讲都不会超过。

![step4:找到免费模型](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/8905936e111f8f604f92ffce17639bb9.jpg)

同样，你也可以对模型进行一下测试。可以如图在下面的 chat 窗口聊几句。

![完成](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/eca539049d98716e1887897b3ba31e2e.jpg)


## 03 如何配置 OpenClaw?

配置大模型时，核心信息主要是三个：

1. 访问地址（即URL）
2. Api Key，用来确定你是否有权限使用服务
3. 模型ID。一个服务商往往提供多个大模型以供使用，所以，需要模型 id来区分它们。

对于 OpenRouter 来说，它一直是知名的在线大模型服务端，所以，它的服务地址是 OpenClaw 预知的，我们在设置时，就不需要提供 URL。

而 build.nvidia.com 这个服务则比较新，并且它也不是专业的大模型服务商，所以， Openclaw 并不会收录它的地址，我们在设置小龙虾时，就需要给出服务地址。

这里的关键信息是： `https://integrate.api.nvidia.com/v1`

接下来，我们就看看在小龙虾中的配置，这里以英伟达为例。配置 OpenRouter 大同小异，不过会少一步填写服务地址而已。

以下是配置步骤：

1. **获取信息**：准备好 api key 和模型 id
2. **打开 OpenClaw 配置页面**： `openclaw config --section models`
3. **按图示操作**

![小龙虾配置界面截图 1](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/57691e8f86375e1b329a46dc510a4b3b.png)

如果是使用 OpenRouter 的服务，这里就要选择 OpenRouter。图中最后一项。接下来是填写 Base URL（如果是 OpenRouter，则无此步聚）、填写 Api Key和 Model ID，如下图所示：

![小龙虾配置界面截图 2](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/03/0fef218f3a20348f6bc9fac514ea7489.png)


你可以直接参考下面的 Python 验证代码来对应填入 URL、API-Key 和 Model 模型：

```python
# 小龙虾接入参数参考（对应代码中的关键行）
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1", # <--- 填入小龙虾的 URL/Base URL
    api_key="YOUR_NVAPI_KEY"                       # <--- 填入小龙虾的 API-Key
)

model="z-ai/glm5"                                  # <--- 填入小龙虾的 Model/模型名称
```

- **URL (Base URL)**：填入 `https://integrate.api.nvidia.com/v1`
- **API-Key**：填入你刚刚保存的英伟达 Key。
- **Model (模型名称)**：填入 `z-ai/glm5`（如果你想尝试英伟达其他模型，如 Nemotron，也可以在这里更换对应的名称）。

## 04 参数验证

如果配置不成功，你还可以运行下面完整的 Python 程序来最终确认相关信息是否正确：

```python
import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="YOUR_NVAPI_KEY" # 替换成你生成的 Key
)

# 调用 GLM-5 模型
response = client.chat.completions.create(
    model="z-ai/glm5",
    messages=[
        {"role": "system", "content": "你是世界顶流人工智能！"},
        {"role": "user", "content": "你好，GLM-5模型！"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

## 后记

在一天烧掉了7500万 token 之后，我深深地被 OpenClaw的无限可能所折服。

每个人都应该养几支小龙虾。智能代码拓展了我们的大脑，拓宽了我们的工作空间，也提升了我们的工作效率。所有这一切，都是为了构建更强大的自己。

但是，尽管你知道这件事的极端重要性，但却受困于养龙虾贵，养龙虾不安全，和养龙虾太难。

一开始我也遇到了同样的困难，但借助于社区，我不仅找到了非常好的方案，还把这个方案做成了产品，在这个过程中，也有了很多经验和踩坑的经历要跟大家分享。

今天的分享只是其中的一小部分。关注我们，一起来养虾吧。而且，今天分享的信息肯定是有时效性的，下一波免费的资源，很可能还是我先找到。

保持联系！
