---
title: 02 编程开发环境
---
尽管条条道路通罗马，但毕竟有的路走得更平稳更快捷，更不要说有的人甚至就住在罗马。对于程序员而言，你的开发环境有多好用，你离罗马就有多近。因此，我们的旅程从这里开始。

## 1. 选择哪一种操作系统？

看上去操作系统是一个与编程语言无关的话题，特别是像 Python 这样的开发语言，它编写的程序几乎可以运行在任何一种操作系统上。但是，仍然有一些微妙的差别需要我们去考虑。首先，Python 更适合于数据分析、人工智能和后台开发，而不是用于开发桌面和移动端应用。而无论是大数据分析和人工智能，还是后台开发，往往都部署在 Linux 服务器环境下。因而，这些应用所依赖的生态，也往往构建在 Linux 下（比如大数据平台和分布式计算平台）。一些重要的的程序库，尽管最终可能都会兼容多个操作系统，但由于操作系统之间的差异，它们在不同操作系统下的版本发布计划往往是不一样的。一些开源的程序和类库往往会优先考虑 Linux 操作系统，它们在 Linux 上的测试似乎也更充分。

我们可以举出很多这样的例子，比如，量化交易是 Python 最重要的应用领域之一。而 python talib则是其中常用的一个技术分析库。该库使用了一个 C 的模块，需要在安装时进行编译。在 Windows 下进行编译，需要下载和配置一系列的 Visual C++的编译工具，对 Python 程序员而言，这些操作会有一定难度，因为很多概念都是 Python 程序员并不熟悉的。而如果你使用的是 Linux 操作系统，尽管编译仍然是必须的，但安装和编译只需要运行一个脚本即可。

不仅仅是 Python 程序库如此。我们需要依赖的各种服务可能也是如此。比如，尽管你可以在 Windows 机器上安装桌面版的 Docker，然后运行一些 Linux 容器，但 Windows 下 Docker 对资源的利用远不如在 Linux 下来得充分 —  它们是在 Docker 服务启动时就从系统中划走的，无论当下是否有容器在运行，这些资源都无法被其它 Windows 程序使用。从根本上讲，这种差异是 Windows 不能提供容器级别的资源隔离造成的。

在本书的后面，我们将讲到 CI/CD，这些都需要使用容器技术。那时，您将更加体会到使用 Linux 的种种方便。比如，我们将会使用 Github Actions 提供的容器来运行测试，但是，因为授权的问题，免费版的 Github CI 提供的容器将不包括 Windows。

如果这些理由还不能说服您，我们还可以看看资深程序员是如何选择操作系统的。下图是 StackOverflow[^stackoverflow] 网站在 2022 年的一个调查：

![](https://images.jieyu.ai/images/2023/03/20230304160004.png)

从图中可以看出，如果把 Linux 自身的使用量与 WSL 的使用量（WSL 是一种 Linux）加在一起，Linux 已经是排名第一的操作系统。

基于上述原因，我们推荐使用 Linux 作为您开发 Python 项目的操作系统。本书中提到的工具、示例和程序库，除非特别说明，也都默认地使用 Linux 作为运行环境，并在 Linux 下测试通过。

但是，您很可能并不会喜欢这个建议，因为很可能您的电脑就是 MacOS 或者 Windows。

好消息是，MacOS 和 Linux 都是所谓的“类 Unix”操作系统，它们之间有极高的相似度。所以，如果您的电脑是 MacOS 操作系统，您大可不必另外安装一个 Linux。如果您的电脑是 Windows 操作系统，我们在下面也提供了三种方案，让您的机器也能运行一个虚拟的 Linux 操作系统用于开发。

## 2. Windows 下的 Linux 环境

在 Windows 下有三种构建 Linux 虚拟环境的方式。其中之一是 Windows 的原生方案，即使用 Windows Subsystem for Linux（以下简称 WSL），其它两种方案则分别是 Docker 和虚拟机方案。
### 2.1. WSL 方案
WSL 是 Windows 10 的一个新功能。通过 WSL，在 Windows 之上，运行了一个 GNU/Linux 环境。在这个环境里，绝大多数 Linux 命令行工具和服务都可以运行，而不需要设置双系统，或者承担虚拟机带来的额外代价。

当前有两个版本可用，即 v1 和 v2, 作者更推荐使用 v1。WSL v2 的体验更象一台真正的虚拟机，因此与 windows 集成性反而更差一些。

#### 2.1.1. 安装 WSL

如果您的 windows 10 是 2004 及更高版本，或者是 Windows 11，则安装只需要一条命令即可完成：

```shell
wsl --install --set-defalut-version=1
```

这将安装 WSL v1 版到您的机器上。如果是稍早一点的系统，则需要执行以下步骤：

1. 首先，启用“适用于 Linux 的 Windows 子系统”功能：

![](http://images.jieyu.ai/images/2020-05/20200503185200[1].png)

2. 设置后，需要重启一次电脑。
3. 从 Windows 应用商店搜索安装一个 Linux 发行版，在这里的示例中，我们使用 Ubuntu:

![](http://images.jieyu.ai/images/2020-05/20200503191417[1].png)

现在，在搜索栏输入 Ubuntu，就会打开 Ubuntu shell。由于是第一次运行，此时会提示我们输入用户名和口令。这样 WSL 就安装成功了。此后，也可以从搜索框输入`wsl`命令来启动这个系统。

#### 2.1.2. 定制 WSL
使用 WSL v1 版本是一种特殊的体验。它既象一个虚拟机，但又缺乏部分功能，比如，它没有后台服务 [^wsl] 这个概念。我们可以在其中安装一些服务，比如 Redis 或者数据库，但这些后台服务并不会随 WSL 一同启动，必须得经由我们手动启动。但是，我们可以通过一些定制，来使得 WSL 的使用体验更接近一台虚拟机。

我们的定制将实现两个功能，一是让 WSL 虚拟机随 Windows 自动启动。二是当 WSL 启动后，它能自动运行一个 ssh 服务，这样我们就可以随时连接使用这台 WSL 虚拟机。学会这个定制之后，读者当然也可以让 WSL 启动之后，自动运行更多的后台服务。

我们需要写三个脚本，一个 start.vbs，一个 control.bat 和一个 commands.txt，并且增加一个开机自动执行的计划任务。当 Windows 开机后，这个计划任务自动执行，调用 start.vbs 来执行 control.bat, 而 control.bat 则会启动 WSL（及其依赖的 Windows 服务），并在 WSL 环境下执行定义在 commands.txt 中的那些命令--即将要在 WSL 中运行的服务，比如 ssh server。整个过程如下图所示：

![](https://images.jieyu.ai/images/2023/03/20230304153221.png)

首先，我们在 commands.txt 文件中定义要在 WSL 中运行的后台服务：

```text
/etc/init.d/cron
/etc/init.d/ssh
```

然后，我们编写一个批处理脚本，用以启动 WSL，并执行上述命令：

```bat
REM 脚本来源于 https://github.com/troytse/wsl-autostart/
@echo off
REM Goto the detect section.
goto lxssDetect

:lxssRestart
    REM ReStart the LxssManager service
    net stop LxssManager

:lxssStart
    REM Start the LxssManager service
    net start LxssManager

:lxssDetect
    REM Detect the LxssManager service status
    for /f "skip=3 tokens=4" %%i in ('sc query LxssManager') do set "state=%%i" &goto lxssStatus

:lxssStatus
    REM If the LxssManager service is stopped, start it.
    if /i "%state%"=="STOPPED" (goto lxssStart)
    REM If the LxssManager service is starting, wait for it to finish start.
    if /i "%state%"=="STARTING" (goto lxssDetect)
    REM If the LxssManager service is running, start the linux service.
    if /i "%state%"=="RUNNING" (goto next)
    REM If the LxssManager service is stopping, nothing to do.
    if /i "%state%"=="STOPPING" (goto end)

:next
    REM Check the LxssManager service is started correctly.
    wsl echo OK >nul 2>nul
    if not %errorlevel% == 0 (goto lxssRestart)

    REM Start services in the WSL
    REM Define the service commands in commands.txt.
    for /f %%i in (%~dp0commands.txt) do (wsl sudo %%i %*)

:end
```

然后我们编写一个 start.vbs 脚本，来执行 control.bat：

```vb title="start.vbs"
' 脚本来源于 https://github.com/troytse/wsl-autostart/
' Start services
Set UAC = CreateObject("Shell.Application")
command = "/c """ + CreateObject("Scripting.FileSystemObject").
                GetParentFolderName(WScript.ScriptFullName) + "\control.bat"" start"
UAC.ShellExecute "C:\Windows\System32\cmd.exe", command, "", "runas", 0
Set UAC = Nothing
```

最后，我们向计划任务程序中添加一个新的开机启动任务：

![](http://images.jieyu.ai/images/202106/20210616215338.png)

![](http://images.jieyu.ai/images/202106/20210616215237.png)

需要说明的是，通过 Windows 应用商店安装的 Ubuntu 子系统，它应该已经安装好了 ssh-server，我们在上述操作中所做的事，只不过是让它随 WSL 一起启动而已。但是，如果您发现您的 WSL 中并没有安装 ssh-server，您也可以自行安装。毕竟，这就是一台 Linux 服务器，您可以在上面安装 Linux 上的绝大多数软件。

通过应用上述方案，您就在 Windows 上拥有了两个可以同时运行的操作系统。特别值得一提的是，在您不使用 WSL 的时候，它只占用很少的 CPU 和内存资源（仅限 WSL 1.0）。这是其它虚拟化方案所无法比拟的。

在本书写作时，WSL 2.0 已经有了支持图形化界面的预览版，称之为 [wslg](https://github.com/microsoft/wslg)。未来这个版本将合并到 WSL 中，随 Windows 一起发行的正式版发行。下图是 wslg 图形化界面的一个效果图：

![](http://images.jieyu.ai/images/202108WSLg_IntegratedDesktop.png)

虽然这与本书的主旨无关，但至少也给了我们一个使用 Linux 的理由，就连微软都这么认真地做 Linux[^Linux] 了，您还要继续使用 Windows 来做开发吗？

### 2.2. Docker 方案
WSL 的出现要比 Docker 晚。如果您购机时间较早，那么您的 Windows 可能不支持 WSL，但可以安装 Docker。在这种情况下，您可以尝试安装桌面版的 Docker，然后通过 Docker 来运行一个 Linux 虚拟机。

安装 Docker 可以从其官方网站 [^docker] 下载，安装完成后，首次运行需要手动启动。可以从搜索框中搜索"Docker"，然后选择"Docker Desktop"来启动，见下图：

![](http://images.jieyu.ai/images/202108docker-app-search.png)

当 Docker 启动后，就会在系统托盘区显示一个通知图标：

![](http://images.jieyu.ai/images/202108whale-icon-systray.png)

上图中第三个，鲸鱼图标，即是 Docker 正在运行的标志。点击它可以进入管理界面。首次运行时需要做一些设置，可以参考官方文档。

在 Windows 上运行 Docker，由于操作系统异构的原因，首先需要启用 Hyper-V 虚拟机，然后将 Docker 安装到这个虚拟机中。这就是为什么在 Windows 下安装运行 Docker，无论当前是否有容器在运行，系统资源也被静态分配切割的原因。但是大概从 2020 年 3 月起，Docker 开始支持运行基于 WSL2 的桌面版。基于 WSL2 的桌面版 Docker，Docker 后台服务启动更快，资源也仅在需要时才进行分配，因此在资源调度上更加灵活高效。

### 2.3. 虚拟机方案

也有可能您的机器既不支持安装 WSL，也不支持安装 Docker。这种情况下，您可以通过安装 VirtualBox[^virtualbox] 等虚拟机来运行 Linux。这方面的技术大家应该很熟悉了，因此不再赘述。

### 2.4. 小结

我们介绍了三种在 Windows 上构建 Linux 开发环境的方案。只要有可能，您首先应该安装的是 WSL。WSL 可以在运行在几乎所有的 Windows 10 以上的发行版上，包括 Win10 Home。

如果您的机器不支持安装 WSL，也可以考虑安装 Docker。即使您的机器支持 WSL，出于练习 CI/CD 的考虑，也可以安装 Docker，以便体验容器化构建和部署。当然，这需要您的机器有更强劲的 CPU 和内存。

对于较早的机型，在无法升级到较新版本的 Windows 时，可以考虑使用虚拟机，比如免费版的 VirtualBox。
## 3. 集成开发环境（IDE）

作为一种脚本语言，Python 可以无须编译即可运行，因此，几乎所有的文本编辑器都可以作为 Python 开发工具。然而，要进行真正严肃的开发，要在开发进度和开发质量之间取得最佳平衡，就需要一个更专业的工具。

集成开发环境（IDE）是一种提高开发效率的工具，它可以让开发者在编写代码时，得到各种代码提示，更早发现语法错误，还可以直接在编辑器中进行调试。

Pycharm 和 VS Code 是进行 Python 应用程序开发的两个首选工具。对于从事数据分析和人工智能领域的开发者，还可以考虑 Jupyter Lab（升级版的 Notebook）和 Anaconda 的 Spyder。

### 3.1. VS Code vs Pycharm：使用哪一个 IDE？

Pycharm 是用于开发 Python 的老牌 IDE，Visual Studio Code（通常被称为 VS Code）则是近几年的后起之秀。VS Code 完全免费，Pycharm 则提供了社区版和专业版两个版本，专业版本功能更强大，但需要付费。下表简要说明了两个 IDE 最重要的差异：

| 特性       | Pycharm      | VS Code          | 说明                                                                                                                                            |
| ---------- | ------------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 远程开发   | 仅专业版支持 | 支持             | 专业版的 Pycharm 中，文件在本地编辑，调试前将文件同步到远程机器上进行调试；VS Code 通过文件共享协议，直接在远程机器上编辑和调试                 |
| 三路归并   | 支持         | 支持             | VS Code 从 2022 年 7 月起提供了三路归并编辑器。三路归并编辑是在代码发生冲突时解决冲突的一种便捷方式                                             |
| 数据视图   | 支持         | 不支持           | PyCharm 中可以在图形化界面里查看数据库和来自 DataFrame 的数据；VS Code 需要插件支持，但功能较弱。一般可以通过第三方数据库工具查行数据查看和管理 |
| 启动速度   | 慢           | 很快             | VS Code 启动速度十分优异，这也使得它除了用作开发外，还可以用作文档撰写、日记等需要快速打开的场合。                                              |
| 多开发语言 | Python 为主  | 支持多种开发语言 | VS Code 可以支持很多种语言的开发，因此特别适合专业开发者                                                                                        |

还有一些小的差异，比如 VS Code 很多功能是通过插件实现的，每个插件都有自己的日志输出窗口。当你使用 VS Code 时，如果某个功能不能用，有可能是由插件引起的。这个错误可能只会静悄悄地在插件的日志窗口中输出，而不是输出在你熟悉的那些界面窗口中。这可能会让初学者感到困惑。而在 Pycharm 中，这些窗口、提示界面的安排似乎更符合我们的直觉。

总之，Pycharm 是一个开箱即用的 IDE，而 VS Code 安装之后，在正式开发之前，还得安装一系列插件，这可能要花费你一定的时间去比较、配置和学习。但是，如果你打算长期从事开发工作，那么在 VS Code 上投入一些时间则是值得的。VS Code 是一个免费产品，它的许可证允许您使用 VS Code 来进行任何商业开发。因此，无论您是个人开发者，还是受雇于某个组织，您都可以使用它。

由于我们更倾向于使用 VS Code，也由于 Pycharm 简单易上手，基本上无需教学，所以我们这里就略过对 Pycharm 的介绍，重点讲述如何配置 VS Code 开发环境。

### 3.2. VS Code 及扩展

VS Code 是一个支持多语言编辑开发的平台，它本身只提供了文本编辑器、代码管理（Git）、扩展管理等基础功能。具体到某个语言的开发，则是通过加载该语言的扩展来完成的。因此，安装 VS Code 之后，还需要配置一系列的扩展。

安装好 VS Code 之后，在侧边栏上就会出现如下图所示工具栏：

![](http://images.jieyu.ai/images/20210820210809145433.png)

被圆形框框住的图标对应着扩展管理。上部的矩形框可以用来搜索某个扩展，找到对应的扩展并点击，就可以在右边的窗口中看到该扩展的详细信息，如下图所示：

![](http://images.jieyu.ai/images/20210820210809145930.png)

在这个详细信息页，提供了安装按钮。

VS Code 扩展管理除了搜索之外，还提供了过滤、排序等功能，读者可以自行探索。如果读者要在多个开发环境下使用 VS Code，可能希望这些扩展在不同的环境下都能使用，针对这个需求，VS Code 还提供了扩展同步机制。在上图中，在扩展详情页的"Uninstall"按键右侧，有一个同步图标，点击后，VS Code 会自动将该扩展同步到其他环境。

下面，我们将讨论一些最常用、最重要的 VS Code 扩展。在使用这些扩展武装 VS Code 之后，您的开发效率将大大提高。
#### 3.2.1. Python 扩展

要在 VS Code 中开发 Python 应用程序，就需要安装 Python 扩展。该扩展如前图所示。

Python 扩展由微软开发，目前有超过1亿次下载。它提供了 IntelliSense、代码语法检查、调试、导航、格式化、重构和单元测试功能。此外，它还提供了 Jupyter Notebook 集成环境。

随 Python 扩展一起安装的，还有 Pylance，Python Test Explorer for Visual Studio Code，Jupyter 等扩展。

Pylance 是微软基于自身收购的 Pyright 静态检查工具开发的具有 IntelliSense 功能的 Languange Server。它提供语法高亮、代码自动完成、语法检查、参数建议等功能。

尽管 Pylance 提供了这些功能，但在使用中，我们常常把 Pylance 看成是一个 Language Server，上述功能中的语法检查、代码提示和自动完成等功能，还是应该通过更专业的专门扩展（或者第三方服务）来完成。在这里，Pylance 可以作为这些功能的一个扩展平台。

Test Explorer 的主要作用是发现和搜集项目中定义的单元测试用例，构建 TestSuite，提供测试执行入口，并在测试完成之后，报告测试执行情况。

Jupyter 是一个允许你在 VS Code 中阅读、开发 notebook 的扩展。与单独安装的 Jupyter notebook 相比，它能提供更强大的代码提示、变量查看和数据查看。此外，调试 notebook 一直是个比较麻烦的事。但在 VS Code 中，你可以象调试 Python 代码一样，逐行运行和调试 notebook。

在 Python 扩展安装完成之后，就可以进行 Python 开发了。在开发之前，需要为工程选择 Python 解释器。可以从命令面板中输入 Python: Select Interpreter 来完成，也可以点击状态栏中的选择图标，如下图所示：

![](http://images.jieyu.ai/images/20210820210806163607.png)

#### 3.2.2. Remote - SSH

这是一个非常有用的扩展，是微软官方开发的扩展之一。它可以让你在 VS Code 中直接打开远程机上的文件夹，编辑并调试运行。如果您使用过 Pycharm 等 IDE，就会知道，尽管这些 IDE 也支持远程开发，但它们是在本地创建文件，调试运行前先要上传同步到远程机器上。频繁同步不仅降低了效率，而且也常常出现未能同步，导致行为与预期不一致，浪费时间查找问题的情况。这也是也是 VS Code 优于 Pycharm 的一个重要特性。

![](http://images.jieyu.ai/images/20210820210809145039.png)

安装好这个扩展之后，在侧边栏会出现一个远程连接图标。同时，如果当前已经连接到远程机器，则在状态栏最左侧，还会显示该连接的概要信息。
#### 3.2.3. 版本管理相关扩展

VS Code 虽然提供了 git 的集成，但是许多功能并未通过 GUI 提供，我们还必须熟记 git 命令。此外，还有一些功能是 git 也没有的，比如以下功能：

1. 代码提交时，遵照指定的格式规范，以图形化的方式编辑 commit message
2. .gitignore 文件的管理
3. local history 的管理

为实现上述功能，我们需要继续安装扩展。首先是 GitLens。
##### 3.2.3.1. GitLens

![](https://images.jieyu.ai/images/2023/03/20230306194047.png)

Gitlens 的功能十分强大，是团队开发中常用的一个扩展。它的功能包括：

   1. 在文件修改历史中快速导航
   2. 在代码行中提示 blame 信息，如下图所示：
    
![](http://images.jieyu.ai/images/202108hovers-current-line.png)

   3. gutter change，如下图所示：
      
![](http://images.jieyu.ai/images/20210820210809160826.png)

    gutter change 是指在上图中，在编辑区行号指示的右侧，通过一个线条来指示当前区域存在变更，当你点击这个线条时，会弹出一个窗口，显示当前区域的变更历史，并且允许你回滚变更、或者提交变更。这个功能实际上是 git 的 interactive staging 功能，只不过在命令行下使用这个功能时，它的易用性不太好。
    
    如果你在编辑文件之前没有做好规划，引入了本应该隶属于多个提交的修改，gutter change 是最好的补救方案。它允许你逐块、而不是按文件提交修改。因此，你可以将一个文件里的不同块分几次进行提交。

   4. GitLens 在侧边栏提供了丰富的工具条，如下图所示：

     ![](http://images.jieyu.ai/images/202108views-layout-gitlens.png)

通过这些工具条，你不再需要记忆太多的 git 命令，并且这些命令的结果也以可视化的方式展示，这也会比控制台界面效率高不少。在这些工具栏里，提供了提交视图、仓库视图、分支视图、文件历史视图、标签视图等。

简单来说，GitLens 将几乎所有的 Git 功能进行了图形化展示和重构，提供了一个丰富的操作界面，让你可以更加方便地操作 Git 和理解代码变更。

##### 3.2.3.2. 编辑提交信息的扩展

常用 PyCharm 的程序员不会不记得它的 git commit 对话框。遗憾的是，到目前为止，VS Code 及其扩展都没能补充这一短板。不过，仍然有一些小众但好用的扩展，不仅可以帮助我们实现图形化界面下的 commit 消息编辑，还能帮助我们规范化地管理 commit message。

这里我们推荐一个名为 git-commit-plugin 的扩展：

![](https://images.jieyu.ai/images/2023/03/20230306195918.png)

这个扩展会将 commit message 进行分类，并且给每个类别加上 emoji 图标，以便我们更快捷地识别类别：

![](https://images.jieyu.ai/images/202109/20210926101451.png)

给代码正确地分类是非常重要的一个任务。如果我们在每一次代码提交时都进行了正确地分类，那么在发行新的版本时，我们就可以根据这些历史提交信息，自动生成 release notes。这样生成的 release notes 也许还需要稍微进行一些修改，但绝对可以避免遗漏重要的修改。

很显然，不是所有的提交信息都应该出现在 release notes 中，特别是像代码风格、文档修订、增加测试用例、以及构建相关的提交，往往都不是最终用户关心的，因此在 release notes 中不应该放入这些内容。如果我们对每一次提交都进行了正确的分类，那么，自动生成 release notes 的工具就可以按照我们指定的类别，只提取有效的信息到 release notes 中。

在后面，我们还会提及自动化生成 Release notes 的工具。我们通过工具来保证 Commit Message 格式的规范性，而 Release notes 也是通过工具来提取和分析这些信息，整个软件开发流程就会象流水线一样精确工作。

这正是本书的主旨所在：**软件开发流程不应该是一些抽象的理念，而应该是通过一系列工具，得以强制执行的软件生产流水线。**一旦流水线被调校好，生产出来的产品就能通过 6 sigma 的品质认证 [^6-sigma]。

##### 3.2.3.3. gitigore 扩展

代码仓库只应该保留有用的文件。然而在开发过程中，工作区有时候不可避免地会产生一些临时文件、垃圾文件和不适合通过代码仓库保管的文件类型，比如调试时产生的日志，编译后产生的二进制文件等。这些临时文件如果反复被上传，就会极大地浪费仓库的存储空间，降低性能。为了避免这些文件被提交到代码仓库，我们可以在代码仓库中创建一个.gitignore 文件，它包含了这些文件的相对路径或者匹配模式字符串。如此一来，git 在提交代码时，就会自动过滤掉这些文件。

.gitignore 文件的格式非常简单，每一行都是一个文件的相对路径。因此我们完全可以手动编辑这个文件。但是，gitignore 扩展能提供更多的功能：

   1. 根据模板生成.gitignore 文件。毕竟，一个.gitignore 文件可能有几十行之多，其中有大量在不同项目之间通用的部分，这些都没有必要记忆。
   2. 方便您从工作区中选择文件并自动加入到.gitignore 文件中。这样相对于手动编辑.gitignore 文件，可以避免出现路径错误，也更加快捷。

##### 3.2.3.4. 本地文件历史

尽管 git 提供了文件版本历史的管理，但对未提交的修改，git 是无法追踪的。然而，在代码提交之前，我们也可能对同一文件进行多次修改，并在某个时候，希望能查看和参考这些变动情况。这就需要有一个本地文件历史管理系统。

Pycharm 提供了一个非常好用的本地文件历史的功能。在 VS Code 中，必须通过扩展来实现这一功能。

读者可以安装这个扩展：

![](https://images.jieyu.ai/images/2023/03/20230306195816.png)

需要注意的是，这个扩展会在工作区生成一个名为.history 的文件夹，以存放本地文件历史。这个文件夹必须被加入到.gitignore 文件中，否则，您很可能会把这个文件夹提交到代码仓库中。这可是一大堆垃圾文件！

下图展示了这个扩展对代码变动的跟踪情况：

![](https://images.jieyu.ai/images/202109/20210926114236.png)
#### 3.2.4. 代码辅助与自动完成

代码辅助与自动完成是我们使用 IDE，而不是文本编辑器来编写代码最重要的原因。根据 Kite[^kite] 的统计，使用 kite 来进行辅助编程，可以省去最多 47%的代码键入，从而使得代码编写更加轻松和更为快速。

当然，您可能并不同意键入速度会左右编程效率这一观点，毕竟，在编程中，我们大量的时间都是在思考算法和功能如何实现、回忆某个库函数应该如何调用、以及我们自己定义的变量、常量名等。令人吃惊的是，随着人工智能能力的增强，现在这类工作的很大部分，都可以由代码辅助与自动完成工具来完成了。

!!! Info
    公司曾经有位女程序员。她妆容精致，长长的指甲上镌刻着一些美丽的图案，流光溢彩，敲起键盘来，指甲上的图案，就象蝴蝶一样翩翩起舞。我自己知道指甲刮蹭在键盘帽上的声音多让人难受，因此自己总是保持剪指甲的习惯，以保证键入时不受干扰，也因此会担心长指甲对键入速度的影响。但接触一段时间后，我发现她的工作效率一点也不低 — 尽管在键入速度上，可能还是会受到长指甲的影响。

    尽管 Kite 的数据表明他们帮码农省去了 47%的键入时间，但从上面的例子可以看出，由此带来的效率的提升，可能并没有 Kite 想像的那么大。后面我们还会有机会回顾 Kite 这家公司的故事：如果努力的方向错了，那么再勤奋也是无济于事。

就象我们可以把自动驾驶按自动化程度定义为 5 个级别一样，代码辅助也可以分为好多个级别。

最低级的级别，可能是普通文本编辑器所做到的那样，在单词级别上进行提示。只要你曾经输入过一个单词或者一个句子，那么下次当你输入这个单词或者句子的前面部分，IDE 就会自动提示这个单词或者句子。如果你常用 Excel，你就很容易明白这是一种什么样的辅助。但这种提示远远不够精确，很多时候，它不能提供我们真正想要的输入。

对于程序开发来说，由于有语法规则可以借助，因此这种提示可以做得更精确一些。比如，你定义了一个类，那么下次如果你输入了一个类（或者类的一个实例变量）的名字，并且键入一个提示符（可能是".", 或者"->", 依赖于程序语言），那么 IDE 就可以提示类的所有方法，或者属性，供我们选取。此外，如果导入了某个名字空间，IDE 也可以基于同样的逻辑，来提示空间中的所有变量、函数、类等。这些都是严格依赖于语法的，所以，对静态语言，IDE 的代码提示可以做得很棒。对于 Python 这样的动态语言，在没有使用类型标注时，要准确提示成员变量还是有一定困难的。

现在，有了人工智能的加持，代码辅助已进化到了令人惊叹的程度。实际上，这本书就是在 Github Copilot[^Github Copilot] 的帮助下完成的，我们可以看一下这个例子：

![](https://images.jieyu.ai/images/202109/20210926150605.png)

Copilot 根据前面的输入，自动生成了一个语法通顺的句子（这个句子在上图中显示为灰色），并且与上下文相当协调。这里我并不想使用它提示的用词（主要是担心读者并不愿意看一本机器写的书），但是，必须承认，除非是写诗，我们不必像象古人一样，吟安一个字，拈断数根须，文章并不是每一句都需要精雕细琢，有时候，完全可以使用 Copilot 提示的字句来进行过渡。更多的时候，在写文章时，Copilot 可以起到开拓思路的作用，这无疑是大有裨益的。

上面只是人工智能在普通文本辅助写作上的一例。当我们把领域限制在编程领域时，其结果就更加令人叹服。很多时候，只要你写下一行注释，Copilot 就会能帮你完成代码，实现这行注释的功能。特别是当我们要实现的功能，已经在某个库函数中实现了，或者存在某个著名的算法时，你就会发现这个功能非常好用。

关于 VS Code 的扩展还很多。比如，我们的工程中可能使用了 json, ymal 等文件，或者使用了 markdown/rst 来编写文档。在编辑这些文件时，还有一些很好的工具来进行辅助和功能增强。比如 Markdown 对表格的支持比较差，手动编辑 Markdown 表格是比较繁琐的事，我们可以使用一些扩展，通过它们将文档内的 csv 块内容转换成为 Markdown 表格。

除了扩展外，VS Code 还有其它一些定制项，比如主题。如果您长期对着电脑工作，推荐您安装一些所谓夜间模式的主题。这些主题当中，Dracula Pycharm Theme 是比较有意思的一个主题。这个主题的名字来源于德古拉伯爵。德古拉伯爵是爱尔兰作家布莱姆·斯托克同名小说中的人物 —— 一个嗜血、专挑年轻美女下手的吸血鬼。这部小说后来被多次改编成电影。考虑到吸血鬼只在夜间出来活动，一款暗夜模式的主题使用这个名字倒也恰如其份。

限于篇幅，我们不可能一一介绍这些扩展。除了那些下载量极大的流行扩展，本章也介绍了一些比较小众的扩展。这些小众扩展在未来可能会消失（比如 VS Code 直接实现了其功能），或者被取代。重要的是，它们实现的功能，极大地提高了生产效率，这些方法和功能，是我们应该熟知的。

## 4. 其他开发环境
### 4.1. Jupyter Notebook

Pycharm 和 VS Code 都是大型开发工具，适合开发大型复杂应用程序。但在 Python 领域中，有一类问题更适合探索式编程，比如数据分析任务。我们拿到一些数据，通过统计方法查看它们的特性，进行一些可视化的分析。然后对数据进行预处理，进而编写一些机器学习算法，如果结果不理想，则推倒重来，探索新的算法。

这种方法被称为探索式编程：探索式的工作重于遵循设计模式，代码中夹杂着大量的解释性文档和输出结果（包含图表和图像），它们都作为最终结果的一部分，而不是象传统的编程一样，代码、文档和输出结果是分离的。

Jupyter Notebook 是探索式编程的利器。它提供了一个基于网页的编辑器和运行环境，用户输入被组织成一个个单元格，每个单元格可以是代码单元，也可以是文本单元；代码单元还允许有输出结果，输出结果可以是文本，也可以是图表或图像，如下图所示：

![](https://images.jieyu.ai/images/202109/20210926164037.png)

一个正在运行的 Notebook 可以看成是一个进程，在此 Notebook 中的代码单元格里定义的变量和函数都具有全局作用域，每个代码单元格都可以单独执行。这种模式有它极其方便的一面，你可以随时随地在 Notebook 中运行代码，并且可以在不同的代码单元格中进行切换--无论是探索数据的特性，还是探索一个新的程序库的功能，都变得非常容易。

当前，Jupyter Notebook 的开发者在力推 Jupyter Lab，以替代 Jupyter Notebook。不过，由于 VS Code 和 Pycharm 对 Jupyter Notebook 的集成，因此 Notebook 还将存在相当长的时间。
### 4.2. Spyder

Spyder[^spyder] 是专门为科学家、数据分析师、工程师打造的一款开源的编程环境。它具有集成开发环境的高级编辑、分析、调试和 profiling 功能与科学库的数据探索、交互式执行、深度检查和精美可视化功能的独特组合。 我们很容易从它的界面上看出这一点：

![](https://images.jieyu.ai/images/202109/20210927163158.png)

Spyder 包含在 Anaconda 发行版之内，所以一旦安装了 Anaconda，就可以直接使用 Spyder 来编写 Python 代码。在它的官网上也提供了单独的安装包供下载。

我们主要介绍了三种类型的 Python 开发环境：适用于大型工程化开发的 Pycharm/VS Code，适用于探索式编程的 Jupyter Notebook，还有融合了两者特点的 Spyder。当然，在 Pycharm/VS Code 中，我们也可以打开和运行 Jupyter Notebook，这项功能集成到这两种 IDE 中已经有一段时间了。

如果我们经常性的开发工作是构建高复用的组件库、或者复杂的应用程序，Pycharm/VS Code 是绝对的不二之选。这两种工具都近乎完美地与负责测试、持续集成以及代码管理、文档构建的工具集成在一起。反之，如果你的工作更多的是探索性的，似乎只使用 Jupyter Notebook 就够了。而 Spyder 则为两方面需求都要兼顾的用户，提供了一种选择。

[^stackoverflow]: stackoverflow.com 是全球最知名的技术分享社区。程序员常常通过这个社区向他人请教自己遇到的技术问题。
[^Linux]: 有一种说法，Mac Os 是最好的 Linux， Windows 也是最好的 Linux，只有 Linux 做不好 Linux。
[^wsl]: 截止本书成稿时，这个概念可能已经发生了变化。在 WSL 下安装的 Ubuntu 20 以上的版本，可能已经有了服务的概念，请读者自行验证。
[^docker]: docker 的官方网站是：https://desktop.docker.com/
[^virtualbox]: Virutalbox 是目前最流行的桌面级虚拟机。它的使用完全免费。网站地址：https://www.virtualbox.org/
[^6-sigma]: 在统计学中，6 sigma 意味着置信度是 99.99966%，在质量检验场景下，表明产品达到了很高的质量标准。从 1970 年代开始，摩托罗拉发现了提高质量与降低生产成本之间的正相关关系，于是发展出一整套改善工业流程、消除残疵的方法。1986 年，摩托罗拉正式将其命名为 6-sigma。它强调持续改进，稳定和预测性地提高流程结果；生产和商业流程可以透过测量、分析、提高和控制进行改善等等。随着摩托罗拉影响力的衰落，6-sigma 的影响力也日渐式微，但它的核心观点和方法，比如持续改进等，仍然得到广泛认同和传播。
[^kite]: https://www.kite.com/
[^Github Copilot]: https://www.copilot.ai/
[^spyder]: https://www.spyder-ide.org/
