---
title: 09 持续集成
---

当一组开发者共同开发一个项目时，各种冲突似乎不可避免。我们在第 8 章介绍了分支和 gitflow 工作流模型，从而解决了代码冲突的问题。但是，代码合并只能达到表面上的和谐。不同的人开发的代码能否协同工作，最终还得通过测试来检验。

在已经介绍过的开发流程中，开发者在签入代码并推送到远程服务器之前，应该通过 tox 执行的单元测试和代码检查。但是，如果开发者有意忽略这些步骤，不良代码仍然能溜进仓库。此外，尽管我们虚拟化了测试环境，但仍然有可能在一名开发者机器上通过的测试，不能在另一个环境里运行。比如，可能引入了新的配置项，这些配置项存在于本地环境，但其它人并不知道；或者更改了本地数据库，但相应的变更脚本并没有集成进来，等等。如果只要有新的代码签入，就能在一台公共机器上自动执行所有测试以确保代码正确性，显然可以更早地发现问题，降低后期维护成本。这就是持续集成的意义所在。

持续集成是一种 DevOps 软件开发实践。采用持续集成时，开发人员会定期将代码变更合并到一个中央存储库中，之后系统会自动运行构建和测试操作。持续集成通常是指软件发布流程的构建或集成阶段，需要用到自动化组件（例如 CI 或构建服务）和文化组件（指组织的流程和规范等，例如学习频繁地集成）。持续集成的主要目标是更快发现并解决缺陷，提高软件质量，并减少验证和发布新软件更新所需的时间。

!!! Info
    持续集成强调的文化是：Fail fast, fail often。但实际上，一旦构建起良好的 CI/CD 流水线和文化，最终我们得到的将是 Move fast and don't break things。

## 1. 盘点 CI 软件和在线服务
我们先来认识一下持续集成领域的头部玩家。Jekins 是持续集成领域的老大哥，Jenkins 自诞生之日起，至今已发展了近 20 年，社区、生态最为完善。Gitlab 最初是基于 Git 的代码托管平台，自版本 8.0 起，开始提供持续集成功能。其优点是与代码仓库无缝集成，原生地支持代码仓库各类事件触发流水线。不足之处是，无论 Jekins 还是 Gitlab，都需要自己搭建服务器，这对于开源项目和个人开发者来说，成本太高了。

构建 CI 服务器的成本是昂贵的。在虚拟机没有广泛应用之前，这个成本就更为昂贵。你需要为你的应用将要部署到的每一种操作系统至少准备一台机器。如果你的应用需要部署到从 windows 到 Linux 到 Macos 上的各个版本，你可能就需要准备至少十台以上的机器硬件。虚拟化的出现大大降低了 CI 的成本，随后是容器化的出现，进一步降低了 CI 的成本。但是，即便是这样，对开源项目，自行搭建和维护 CI 服务器的成本仍然是昂贵的。比如，如果你的应用需要部署到 MacOs 上，你必须至少有一到多台苹果的服务器，因为其它机器上都无法虚拟化出来 macos 的容器。

这就是为什么我们推荐使用在线 CI 服务的原因。好消息是，对开源项目，有相当多的在线 CI 服务是免费的。这里我们仅仅介绍 Travis CI 和 Github Actions。

Travis CI 是一个基于云的持续集成服务，它可以帮助开发者在 Github 上构建和测试代码，从而减少发布软件的时间。Travis CI 为开源项目提供了一定量的服务时间，对于私有项目，则需要付费--起价是每月 69 美元。这个定价本身也说明了持续集成的价值，以及要实现持续集成，所需要消耗的资源。

Github Actions 是 Github 在 2020 年前后推出的持续集成服务，它的优点同 gitlab CI 一样，也在于与代码托管服务无缝集成。在价格方面，Github Actions 对开源项目也是免费使用的，与 Travis CI 相比，给出的免费 quota 更多，足堪使用。因此，我们本章就略过 Travis CI，直接介绍 Github Actions。
# 2. GITHUB ACTIONS
Github Actions 是一个持续集成与交付的平台，它使得我们可以将构建、测试和部署像流水线一样自动化。您可以创建工作流程来构建和测试存储库的每个拉取请求，或将合并的拉取请求部署到生产环境。

GitHub 通过云服务来提供 Linux、Windows 和 macOS 这些基础设施，但也允许我们在自己的私有云上进行本地化部署。

## 2. Github Actions 的架构和概念

Github Actions 由工作流 (workflow)、事件 (Event)、作业 (job)、操作 (Action) 和执行者 (runner) 等组件构成。

工作流由一个 yaml 文件来定义，它位于项目根目录下的.github/workflows。我们也可以简单地将该文件当成脚本来理解。该文件定义了哪些事件可以触发工作流，工作流中应该包含哪些作业，以及作业应该在什么样的执行者（容器）中运行。一个存储库中可以有多个工作流，分别执行不同的任务集。

事件是能引发工作流运行的特定事件，比如当有人创建拉取请求、或者将提交 (commit) 推送到存储库时，这就是一个能触发工作流的事件。

作业 (job) 是工作流中在同一运行器上执行的一组步骤（steps)。 每个步骤 (step) 要么是一个将要执行的 shell 脚本，要么是一个将要运行的操作 (Action）。 步骤按顺序执行，并且相互依赖。 由于每个步骤都在同一运行器上执行，因此您可以将数据从一个步骤共享到另一个步骤。 例如，可以有一个生成应用程序的步骤，后跟一个测试已生成应用程序的步骤。

一个工作流中可以有多个作业。作业之间默认没有依赖关系，并且彼此并行运行。 但我们也可以配置一个作业依赖于另一个作业，此时，它将等待从属作业完成，然后才能运行。 例如，对于没有依赖关系的不同体系结构，您可能有多个测试作业，以及一个依赖于这些作业的打包作业。 测试作业将并行运行，当它们全部成功完成后，打包作业将运行。

操作 (Action) 是用于 GitHub Actions 平台的自定义应用程序，它执行复杂但经常重复的任务。 使用操作可帮助减少在工作流程文件中编写的重复代码量。 操作可以从 GitHub 拉取 git 存储库，为您的构建环境设置正确的工具链，或设置对云提供商的身份验证。

您可以编写自己的操作，也可以在 GitHub Marketplace 中找到要在工作流程中使用的操作。

执行者 (runner) 是运行工作流的服务器。每个执行者一次可以运行一个作业。 GitHub 提供 Ubuntu Linux、Microsoft Windows 和 macOS 运行器来运行您的工作流程；每个工作流程运行都在新预配的全新虚拟机（或者容器）中执行。

下面的图展示了 Github Actions 的架构：

![](https://images.jieyu.ai/images/2023/12/overview-actions.png)
## 3. 工作流语法概述
在了解了 Github Actions 的架构之后，我们通过一个例子，来讲解如何定义工作流。

我们先看 ppw 生成的一个工作流文件：

```yaml title="dev.yml"
name: dev build CI

# 定义哪些事件可以触发工作流，以及筛选条件
on:
  # 当存储库有 PUSH 或者 PULL_REQUEST 事件时触发
  push:
    branches:
      - '*'
  pull_request:
    branches:
      - '*'

# 定义作业集
jobs:
  # 工作流包含三个作业，分别是 TEST, PUBLISH_DEV_BUILD, NOTIFICATION
  test:
    # 定义作业的运行环境，这里使用了矩阵式定义
    strategy:
      matrix:
        python-versions: ['3.8', '3.9', '3.10']
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    # 将步骤的输出提升为作业的输出，以便它们可以在作业之间共享
    outputs:
      package_version: ${{ steps.variables_step.outputs.package_version }}
      package_name: ${{ steps.variables_step.outputs.package_name }}
      repo_name: ${{ steps.variables_step.outputs.repo_name }}
      repo_owner: ${{ steps.variables_step.outputs.repo_owner }}

    # 这是启用外部服务的一个示例
    # SERVICES:
    #   REDIS:
    #     IMAGE: REDIS
    #     OPTIONS: >-
    #       --HEALTH-CMD "REDIS-CLI PING"
    #       --HEALTH-INTERVAL 10S
    #       --HEALTH-TIMEOUT 5S
    #       --HEALTH-RETRIES 5
    #     PORTS:
    #       - 6379:6379

    # 步骤集代表了一系列的任务，这些任务将作为作业的一部分执行
    steps:
      # 作业是在容器里执行的，我们需要先将代码检出到这个干净的容器里
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-versions }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox tox-gh-actions poetry

      # 这一步里，我们设置了一些变量，将其输出到控制台，从而可以在第 85 行提升为 JOB 的输出
      - name: Declare variables for convenient use
        id: variables_step
        run: |
          echo "::set-output name=repo_owner::${GITHUB_REPOSITORY%/*}"
          echo "::set-output name=repo_name::${GITHUB_REPOSITORY#*/}"
          echo "::set-output name=package_name::`poetry version | awk '{print $1}'`"
          echo "::set-output name=package_version::`poetry version --short`"
        shell: bash

      # 执行单元测试和代码检查。
      - name: test with tox
        run: tox

      # 通过 CODECOV 上传测试覆盖率。
      - uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: true

  publish_dev_build:
    # 只有 TEST 作业完成，我们才开始本作业
    needs: test
    # 指定本作业运行的操作系统环境。
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          # 这一步只需要在任意一个 PYTHON 版本上运行
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry tox tox-gh-actions

      - name: build documentation
        run: |
          poetry install -E doc
          poetry run mkdocs build
          git config --global user.name Docs deploy
          git config --global user.email docs@dummy.bot.com
          poetry run mike deploy -p -f --ignore "`poetry version --short`.dev"
          poetry run mike set-default -p "`poetry version --short`.dev"

      - name: Build wheels and source tarball
        run: |
          poetry version $(poetry version --short)-dev.$GITHUB_RUN_NUMBER
          poetry lock
          poetry build

      - name: publish to Test PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.TEST_PYPI_API_TOKEN}}
          repository_url: https://test.pypi.org/legacy/
          skip_existing: true

  notification:
    needs: [test,publish_dev_build]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: martialonline/workflow-status@v2
        id: check

      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build successfully
          convert_markdown: true
          html_body: |
            ## Build Success
            ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version }} is built and published to test pypi

            ## Change Details
            ${{ github.event.head_commit.message }}

            For more information, please check change history at https://${{ needs.test.outputs.repo_owner }}.github.io/${{ needs.test.outputs.repo_name }}/${{ needs.test.outputs.package_version }}/history

            ## Package Download
            The pacakge is available at: https://test.pypi.org/project/${{ needs.test.outputs.package_name }}/

      - name: build failure notification via email
        if: ${{ steps.check.outputs.status == 'failure' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build failure
          convert_markdown: true
          html_body: |
            ## Change Details
            ${{ github.event.head_commit.message }}

            ## View Log
            https://github.com/${{ needs.test.outputs.repo_owner }}/${{ needs.test.outputs.repo_name }}/actions
```

这是一个名为 dev build CI 的作业，它将在任一分支发生提交和 pull request 时触发。它包含三个作业，即 test（执行单元测试）、publish_dev_build（构建并发布开发版本到 test_pypi) 和 notification（在构建成功或失败时发送邮件通知）。三者之间有依赖关系，如果 test 作业失败，publish_dev_build 会取消；但是无论 test/publish_dev_build 作业是否成功，notification 作业都会执行，并根据前两个作业的状态发送邮件通知。

这是一个比较简单的作业，但也涉及了我们在 CI 中需要做的几乎所有事情。在代码中我们加入了较多的注释，建议读者结合下面的讲解，仔细阅读代码。
### 3.1. 定义触发条件
第 4 行到第 14 行配置了工作流的触发条件。触发条件一节由关键字**'on'**引起。在它的下一层，我们可以定义多个触发事件，并为每个触发事件，指定类型和过滤器。一个完整的触发条件配置如下：

```yaml
on:
    push:
        branches: 
          - '*'
        tags:
          - v*
    label:
        branches:
            - main
        types:
            - created
    schedule:
        - cron: '30 5 * * 1,3'
```
在上面的示例中，'push', 'label', 'tags'和'schedule'都是事件关键字。可用的事件关键字可参见 [触发工作流的事件](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows)。

在事件的下一级，是定义活动类型和筛选器的地方。不是所有的事件都有活动类型，即使有，它们的活动类型也很可能不一样。比如，`push`事件就没有活动类型，而`label`事件有`created`, `edited`和`deleted`三种活动类型，而`issues`事件的活动类型则是`opened`和`labeled`等。要想知道事件有哪些活动类型，可以参考 [触发工作流的事件](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows)。

筛选器有 branches 和 tags 两种，分别用于指定分支和标签。从上面的示例可以看出，筛选器的值支持 glob 模式，即你可以使用*,**, +, ? 和！等通配符。除了示例中的正向匹配外，还可以使用 branches-ignore 或者 tags-ignore 来反向匹配。

上面的示例还展示了一种特殊的事件，即 'schedule' 事件。这将导致工作流周期性地运行。这可以用来运行一些安全性扫描、依赖升级扫描等工作。

### 3.2. 定义作业集
接下来工作流声明了三个作业，即 test, publish_dev_build 和 notification。作业定义一节由关键字**'jobs'**引起。在它的下一层，我们可以定义多个作业，并为每个作业，指定运行环境和运行步骤。

每个作业都有自己的 id 和名字。在上述例子中，test, publish_dev_build 和 notification 都是作业 id。作业 id 是必须的，但是作业名字是可选的。如果没有指定作业名字，那么作业名字将默认为作业 id。作业名字可以用来在 GitHub Actions 的界面上显示作业的名称。

在作业 publish_dev_build 中，我们通过关键字`needs`来定义了它对作业`test`的依赖。我们在第 114 行还看到，作业还可以依赖到一组作业。当我们指定作业依赖时，要注意只能使用作业的 id，而不是作业的名字。

接下来我们为作业定义执行环境。执行环境是通过关键字 'runs-on' 来定义的。有些任务只需要在一台机器上执行就可以了，比如Python包的构建和发布；有些任务则需要在所有的机器上、并以多个python运行时来运行，比如测试。

比如，publish_dev_build 作业只在 ubuntu_latest 和 python 3.9 这个组合上运行。我们是通过第 78 行和第 83 行来指定的。但对测试任务，我们希望它在所有机器上都运行，并且还要运行在不同的 python 版本上。为了表达简洁起见，github actions 引入了矩阵的概念。

我们通过 strategy.matrix 来定义测试矩阵。在示例第 20~23 行定义的矩阵中，我们定义了 python 版本和操作系统列表。这个定义随后就被使用了，在第 24 行，我们通过{{matrix.os}}来引用了其中的操作系统定义。第 22 行的 python-versions 是一个特殊的关键字，它用来指示我们要使用的 python 版本。如果我们的开发语言不是 python，这里的指定将没有意义。

接下来我们需要为作业定义具体执行哪些任务，它们被归类在步骤集 (steps) 中。步骤集是一个包含多个步骤的列表。而每一个步骤，要么是一个 shell 命令（或者一组 shell 命令），要么是一个 action。如果要运行 shell 命令，我们使用下面的语法：
```yaml
- name: <step name>
  run: <shell command>
```
如果要运行一组 shell 命令，我们使用：
```yaml
- name: <step name>
  run: |
    <shell command 1>
    <shell command 2>
    ...
```
注意上述两组语法的不同之处，不能混淆。

至于 action，我们前面已经讲过了，它是用于 GitHub Actions 平台的自定义应用程序。您可以自己编写 action，也可以在 Github 的应用市场上查找他人开发的应用。

每一个步骤都可以指定 python 运行时。我们在第 48 行看到，这里`{{ matrix.python-versions }}`使用的是矩阵中定义的 python 版本。而在第 84 行，我们则直接指定了一个 python 的版本。这里还要注意，版本号是一个字符串，q 我们可以使用`'3.10'`，但不能使用`3.10`，后者将会被 yaml 解析为`3.1`，从而出现找不到 python 版本的问题。

最后，我们介绍一下 job 运行时的条件控制。我们已经介绍过了 job 之间的依赖关系，这可以算作是一种条件。还有一种情况，比如示例中的 notification 作业，我们要求它只能在前两个作业都完成后才运行，但无论成功与否，都要运行，但会根据前面作业的状态，发出不同内容的通知邮件，此时，我们就需要引入`if`条件控制。

`if`条件控制可以作用于作业作用域（如第 116 行所示），也可以作用于步骤作用域（如第 123 行所示）。在作业作用域中，我们可以使用`success()`、`failure()`、`cancelled()`、`always()`等函数来指定在何种情况下才运行本作业。在步骤作用域中，我们则可以进行简单的条件判断，来指标本步骤是否运行。

在进行条件判断时，我们必然需要使用变量。现在，我们需要全面地介绍一下在工作流中变量的使用。通过变量，结合各种控制条件，我们才能实现一些高级的技巧。
Github 中的变量分为两种，一种是系统变量，一种是作业变量。系统变量是 Github 平台提供的，作业变量是我们自己定义的。无论那一种变量，我们都通过`${{ }}`来引用。

系统变量按级别可以定义在组织、存储库或者环境上。比如`secrets`就定义在存储库级别上，我们可以通过`${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}`来访问它的值，这需要我们在存储库里事先定义`BUILD_NOTIFY_MAIL_RCPT`这个变量。Github 提供了一些默认变量，比如`GITHUB_REPOSITORY`（你在第 59 行，声明变量那一节可以看到它的使用）等。

作业变量的使用比较特殊，我们看看下面的例子：
```yaml
  notification:
    needs: [test,publish_dev_build]
    steps:
      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          subject: ${{ needs.test.outputs.package_name }}.
```
例子中，我们通过${{ needs.test.outputs.package_name }}来引用在第 24 行声明的`package_name`变量。变量是通过`{job_id}.outputs.{variable}`来引用的，这并没有什么奇怪的地方。但是要注意它还有一个`needs`作用域。这表明，如果我们使用变量的地方，其所属的作业如果没有声明依赖到`test`作业，那么这个变量是无法被引用的。

示例中没有展示环境变量的用法，这里我们给一个示例，请读者结合注释自行研究：
```
env:
  # 声明了一个全局上下文的环境变量
  DAY_OF_WEEK: Monday

jobs:
  greeting_job:
    runs-on: ubuntu-latest
    env:
      # 声明了一个作业上下文的环境变量
      Greeting: Hello
    steps:
      - name: "Say Hello Mona it's Monday"
        # 使用时我们在变量前加一个`ENV.`的约束
        if: ${{ env.DAY_OF_WEEK == 'Monday' }}
        # 当使用的环境变量是在作业内声明时，我们可以省略`ENV.`的约束
        run: echo "$Greeting $First_Name. Today is $DAY_OF_WEEK!"
        env:
          # 声明了步骤上下文的环境变量
          First_Name: Mona
```
### 3.3. 连接其它服务
在示例的第 31 行到第 40 行，有一段被注释的代码，这是用来启用 redis 服务的。Github Actions 通过容器技术来提供这些服务。理论上，只要在 docker hub 上存在某个服务的 image（镜像），我们就可以在 Github Actions 中使用它。

!!! Attention
    要注意的是，如果我们要在 workflow 中使用服务，执行者 (runner) 必须是 ubuntu 操作系统，而不是能其它 Linux 系统，或者 windows 和 MacOS

我们的工作流可以运行在执行者 (runner) 上，也可以运行在容器里（该容器运行在 runner 上）。如果工作流运行在容器里，则需要通过自定义的桥接网络来连接运行在容器里的服务。如果工作流就运行在执行者 (runner) 上，那么我们可以将容器的端口映射到执行者上，这样我们就可以直接访问容器里的服务了。

在工作流中使用服务，一般需要等待容器完全启动被初始化成功。这就是第 96 行的工作。

## 4. 第三方应用和 Actions
我们已经在示例中看到了一些来自应用市场的 action，比如 actions/checkout, actions/setup-python, pypa/gh-action-pypi-publish, dawidd6/action-send-mail, codecove/Codecov 等等。这里'/'之前的是 action 的作者，其中 actions 是 Github 官方的 action，其它的都是第三方的 action。例子中的 action，它们的名字就已经说明了其功能，因此这里不再赘述。

下面介绍其它一些使用较多的第三方 actions，其中有一些我们进行了简要说明并举例了使用方法。如果我们没有进行特别说明，或者您想进一步了解相关信息，可以访问 [marketplace](https://github.com/marketplace/actions) 查看相关文档。

### 4.1. Github pages 部署
这个 action 可以用来将静态网站部署到 Github Pages 上。在 ppw 生成的项目中，它与 mkdocs/mike 配合使用。其 ID 是 JamesIves/github-pages-deploy-action，使用示例如下：
```
name: Build and Deploy
on: [push]
permissions:
  contents: write
jobs:
  build-and-deploy:
    concurrency: ci-${{ github.ref }} # Recommended if you intend to make multiple deployments in quick succession.
    runs-on: ubuntu-latest
    steps:
      - name: Checkout 🛎️
        uses: actions/checkout@v3

      - name: Install and Build 🔧 # This example project is built using npm and outputs the result to the 'build' folder. Replace with the commands required to build your project, or remove this step entirely if your site is pre-built.
        run: |
          npm ci
          npm run build

      - name: Deploy 🚀
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: build # The folder the action should deploy.
```

### 4.2. 构建和发布 docker 镜像
显然，作为持续部署的一个步骤，docker 镜像的构建也应该通过 CI/CD 服务器来完成并发布。这是 docker 官方的一个 action， id 是 docker/build-push-action。

### 4.3. Github Release
一般地，Python 项目的发布都是通过 PyPI 来完成的。但是，我们也可以将其发布到 Github Release 上。这个 action 的 id 是 softprops/action-gh-release。

### 4.4. 制订发布草案
编写 release notes 是一件枯燥乏味的事。这个 action 可以帮助我们自动生成 release notes。它的 id 是 relase-drafter/release-drafter。

这个 action 可以与 GH Release 一起使用。

还有一些好玩的 action，比如一个生成贪吃蛇游戏的 action，id 是 Platane/snk。它会生成如下的贪吃蛇游戏：

![](https://images.jieyu.ai/images/2023/12/github-contribution-grid-snake.svg)

### 4.5. 通知消息
我们已经介绍了邮件通知。在应用市场里，还有各种各样的通知 action，比如 Slack 通知，id 是 Ilshidur/action-slack。

### 4.6. Giscus
Giscus 是一个基于 Github Discussion 的评论系统。它的 id 是 giscus/giscus。如果你使用了 gitpages 作为博客和静态站系统，你可以在 Github 上安装它，并在博客和静态站系统中增加评论功能。

## 5. 通过 Github CI 发布 Python 库
我们在前面看到的例子来自于`ppw`生成的项目下的.github\workflows\dev.yml 文件。这个文件定义的工作流适用于所有的分支，在每次 push 时都会触发。它的作用是进行集成测试，构建测试包并发布到 testpypi，并发布非正式文档到 Github Pages 上。

正式的版本发布工作交给了 release.yml。这个工作流仅适用于 main 分支，并且只有当 main 分支上有打标签事件发生，并且标签是以'v'字线开头时，才会真正运行。下面是这个工作流的内容：
```yaml title="release.yml"
# PUBLISH PACKAGE ON RELEASE BRANCH IF IT'S TAGGED WITH 'V*'

name: build & release

# CONTROLS WHEN THE ACTION WILL RUN.
on:
  # TRIGGERS THE WORKFLOW ON PUSH OR PULL REQUEST EVENTS BUT ONLY FOR THE MASTER BRANCH
  push:
    branch: [main, master]
    tags:
      - 'v*'

  # ALLOWS YOU TO RUN THIS WORKFLOW MANUALLY FROM THE ACTIONS TAB
  workflow_dispatch:

# A WORKFLOW RUN IS MADE UP OF ONE OR MORE JOBS THAT CAN RUN SEQUENTIALLY OR IN PARALLEL
jobs:
  release:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-versions: ['3.9']

    # MAP STEP OUTPUTS TO JOB OUTPUTS SO THEY CAN BE SHARE AMONG JOBS
    outputs:
      package_version: ${{ steps.variables_step.outputs.package_version }}
      package_name: ${{ steps.variables_step.outputs.package_name }}
      repo_name: ${{ steps.variables_step.outputs.repo_name }}
      repo_owner: ${{ steps.variables_step.outputs.repo_owner }}

    # STEPS REPRESENT A SEQUENCE OF TASKS THAT WILL BE EXECUTED AS PART OF THE JOB
    steps:
      # CHECKS-OUT YOUR REPOSITORY UNDER $GITHUB_WORKSPACE, SO YOUR JOB CAN ACCESS IT
      - uses: actions/checkout@v2

      - name: build change log
        id: build_changelog
        uses: mikepenz/release-changelog-builder-action@v3.2.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-versions }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox-gh-actions poetry

        # DECLARE PACKAGE_VERSION, REPO_OWNER, REPO_NAME, PACKAGE_NAME SO YOU MAY USE IT IN WEB HOOKS.
      - name: Declare variables for convenient use
        id: variables_step
        run: |
          echo "::set-output name=repo_owner::${GITHUB_REPOSITORY%/*}"
          echo "::set-output name=repo_name::${GITHUB_REPOSITORY#*/}"
          echo "::set-output name=package_name::`poetry version | awk '{print $1}'`"
          echo "::set-output name=package_version::`poetry version --short`"
        shell: bash

      - name: publish documentation
        run: |
          poetry install -E dev
          poetry run mkdocs build
          git config --global user.name Docs deploy
          git config --global user.email docs@dummy.bot.com
          poetry run mike deploy -p -f --ignore `poetry version --short`
          poetry run mike set-default -p `poetry version --short`

      - name: Build wheels and source tarball
        run: |
          poetry lock
          poetry build

      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          body: ${{ steps.build_changelog.outputs.changelog }}
          draft: false
          prerelease: false

      - name: publish to PYPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.PYPI_API_TOKEN }}
          skip_existing: true
```
这个工作流用到的语法特性前面已经讲过了。这里就不再解释。
