# 开发环境和工具

选择开发环境的第一步，是选择操作系统。对于一些新手程序员来讲，可能更熟悉Windows系统。但是，Python从诞生之初，就与开源社区结缘，Python中大量的第三方库，往往在类Unix环境下测试更充分，或者优先推出。类Unix系统似乎天生是程序员的首选平台。

这里所指的类Unix操作系统，是指各种Linux发行版和MacOS。这些操作系统在内核、文件系统的组织方式、用户接口等方面都有较多相似性。

如果您打算长期使用Python作为开发语言，并且想要开发一些严肃认真的项目，而不仅仅是在处理数据、完成一些自动化任务时临时用用Python的话，推荐您始终使用类Unix的操作系统来构建开发环境。更具体一点，如果您不是正在使用MacOs的话，那么我们推荐您使用Linux的一个发行版--Ubuntu来做为您的开发环境的操作系统。

???+ Readmore
    Unix, Linux，Windows和MacOs是主流的非移动端操作系统。

    Unix由Bell实验室发明，是最早出现的多用户服务器操作系统之一。现在比较常见和容易得到的Unix操作系统有FreeBSD，是由加州伯克利大学从1975年起开发的。
    
    进入20世纪80年代以来，出现了现代Windows和MacOS的雏形，分别由微软和苹果公司开发，现在已成为排名前列的桌面电脑操作系统。发展至今，Windows在桌面端和服务器市场都占据重要位置，MacOS则成为高端消费品领域的翘楚，成为重视性能和体验的开发者的选择。
    
    上世纪90年代，Linux操作系统异军突起，随着云计算的发展，Linux因为其开源带来的低成本特征，迅速占领了服务器操作系统的头把交椅。云计算的需求也大大促进了Linux各种虚拟化技术（如容器技术）的发展，也更加巩固了其在云计算领域的地位。现在，就连微软也在积极拥抱Linux了。有一句调侃的话说，最好的Linux发行版是哪一家的？微软。这是真的，通过Win10的WSL（Windows Subsystem for Linux)发行的Ubuntu，很可能已经是Ubuntu的发行量第一的渠道了。

    CentOs和Ubuntu是Linux的两个重要的免费发行版，CentOS的更新更为稳健，多用于服务器；Ubuntu更倾向于吸纳技术的最新进展，其桌面版在国内十分流行。

    从流派上看，除了Windows外，其它几种操作系统都深受Unix影响。比如类Unix操作系统都有一致的文件系统，而Windows则大异其趣；在进程启动和调度方式上，Windows也与其它家泾渭分明，比如没有Unix下的fork机制和信号机制。在用户接口上，类Unix系统有着强大的命令行和脚本功能，Windows则以图形界面见长，其命令行接口一直为人所诟病。在网络服务能力上，Windows很早推出了性能强大的完成端口，而类Uninx系统则落后一局，其select机制沿用了好久，后来才相继被kqueue/epoll技术取代。

    正是因为操作系统之间的这些重要差别，编写跨操作系统的应用从来就不是很容易的事。因此，一些偏重于服务器的应用或者程序库，往往优先推出Linux版本，尤其是一些开源社区软件。
    
    Python的主要应用领域，一是服务器应用及运维，二是人工智能和大数据领域，使用Python编写桌面端程序是比较少见的。因此，这也是我们推荐您使用Linux操作系统的原因。


当然，推荐使用Linux操作系统，并不意味着就要抛弃Windows。如果您只有Windows电脑，我们推荐一种融合式开发环境，即程序的运行和调试都发生成Linux环境下，而IDE本身运行在Windows之中。

在接下来的一节里，我们要简单介绍如何在Windows下构建一个基于虚拟化技术的Linux环境，以便作为Python程序的运行和调试环境。如果您已经有了一台Linux机器（或者MacOS)，则可以跳过这一节。
## Windows下的虚拟Linux环境

在Windows上构建虚拟的Linux环境，主要有三种方案，即WSL, Docker和虚拟机方案。

如果您使用的Windows版本是Win10专业版（及以上）版本，您就可以使用WSL方案。如果使用的是Win7，或者Win10家庭版，WSL是无法在这些操作系统上运行的，您可以选择使用docker或者虚拟机的方案。

在这里我们只介绍安装WSL来获得Linux虚拟机的方法。您也可以使用通过Docker，或者虚拟机（VMWare或者VirtualBox)来安装Linux的方法。这些技术方案已经成熟很多年，不需要特别介绍了。如果您还不熟悉，网上可以找到很多教程。

???+ Readmore
    虚拟机在Windows下本身以应用程序运行，模拟出一个完全隔离的、资源独占的操作系统出来。虚拟机启动和关闭都有一定的时间占用。当没有客户机运行时，虚拟机软件也不需要运行，不占用计算资源。

    Docker是一种基于Linux容器隔离诞生的一种虚拟化技术。当其在Linux下运行时，可以与Host操作系统共享资源，因而是一种十分轻量的虚拟化技术。在Windows下使用Docker，Windows必须先模拟出来一个Linux的操作系统，然后在其之上，再运行docker层。这个操作系统层必须静态分割和独占主机的资源，比如CPU和内存。一旦Windows启动了Docker服务，无论您当前是否有容器在运行，都要占用相当一部分CPU和内存资源。因此，与虚拟机相比，即使没有客户机（在这里更准确的说法是容器）在运行，也要占用计算资源。但是容器的启动速度要远远快于虚拟机。

    WSL是Windows Subsystem for Linux的首字母简写，为Windows提供了一个Linux子系统。
    
    WSL是一种非常轻量的虚拟化技术，它根据需要动态分割主机资源，启动非常迅速。当不需要使用WSL时，只要退出所有的窗口，资源即释放。因此，在Windows下要开启Linux虚拟机，首先考虑的是安装WSL。

    针对无法安装WSL，选择使用Docker来运行Linux的用户，我们已在hub.docker.com上提供了一个Python的开发环境镜像，已经配置好了git, conda, ssh, redis, postgres等服务。您可以通过下面的命令来获得它的镜像：

    docker pull zillionare/python-dev-machine

    然后运行下面的命令将其启动起来：

    ```
    # 将这里的{host_port}替换成你主机上空闲的任何端口
    docker run -d -name dev -p {host}:22 python-dev-machine
    ```
    接下来，就可以通过Winows Terminal连接{host}端口，远程登录这台机器了。

### 安装WSL

WSL有两个版本。版本二更象传统的虚拟机技术，提供了完全的Linux体验（兼容所有系统调用），但与宿主机的融合体验要差一点。当在两个系统间来回读写文件时，版本二性能会弱一些，这也是我们推荐版本一的重要原因。当您使用版本一时，是可以在WSL里创建文件，然后在Windows中打开它的；反之亦然。

关于两者的区别的详细比较，可以阅读[WSL两个版本的比较](https://docs.microsoft.com/en-us/windows/wsl/compare-versions)


下面，我们正式介绍如何启用WSL：

首先，要通过"启用或关闭Windows功能"命令，来启用"适用于Linux的Windows子系统"功能：
![](http://images.jieyu.ai/images/2020-05/20200503185200[1].png)
接下来，从应用商店搜索安装Ubuntu：
![](http://images.jieyu.ai/images/2020-05/20200503191417[1].png)

??? Tips
    在Windows中，如果您不知道如何进入某个设置界面，一般可以直接在搜索框里搜索入口。

??? Tips
    如果启用WSL失败，请检查启用或者关闭Windows功能中，是否启用了"虚拟机平台”（有的Windows版本里，可能叫Hyper-v支持），并且检查BIOS里相关虚拟化支持。

    如果您的机器不是太老旧的话，一般无须关注BIOS选项。它们一般是打开虚拟化支持的。

安装完成后，可以在搜索栏输入`ubuntu`进入命令行窗口。这样就启动了WSL。如果您关闭了这个窗口，那么这个子系统，以及里面运行的程序，就一同关闭了。

如果您安装的是版本二，那么您可以完全按照自己掌握的Linux操作系统知识来使用WSL。如果是版本一的话，您要记住，WSL与Linux的主要区别是，它没有rc，init.d这样的系统。除此之外,似乎跟普通的Linux也没有什么区别，您一样可以运行所有的Linux原生应用程序，除了它们不能作为服务运行。

??? Tips
    在WSL里安装程序，一样要使用apt。因此，您也需要设置国内源。

    ```bash
    #vi /etc/apt/sources.list
    deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
    ```

??? Tips
    通过WSL安装的`ubuntu`本身不会随Windwows而启动。如果您在WSL里安装了Redis等应用的话，您一般也需要在WSL启动后，在命令行窗口中逐一启动它。为了得到更好的使用体验，我们可以设置WSL随Windows一起启动，并且自动启动指定的服务（比如redis)。请参见[WSL服务自启动技巧](blog/tools/how_to_run_app_as_service_in_wsl.md)

??? Tips
    在Windows下远程访问Linux机器，现在最好的终端当属微软推出的[Windows Terminal](https://github.com/microsoft/terminal)。您可以从微软应用商店下载安装这个程序。它是多Tab的，同时支持横向和纵向切分窗口。作为之前cmder的重度使用者，在使用了Windows Terminal一段时间之后，大有相见恨晚的遗憾。cmder性能太差，打字时容易吞字符，Windows Terminal则完全没有这个问题。

现在，操作系统已经设置好了，我们来看看IDE（集成开发环境）。

## 安装集成开发环境
### 如何选择IDE

Python最好的专业开发工具是Pycharm和Vscode。Pycharm更容易上手，但随着时间推移，您会发现，vscode可能是更适合开源项目开发。

这里就Pycharm与vscode的主要差异进行一个比较。Pycharm有两个版本，社区版免费，专业版需要支付费用。如果在中国区付款很方便的话，这个费用还是值得的。

| 功能         | vscode   | pycharm社区版 | pycharm专业版       |
| ---------- | -------- | ---------- | ---------------- |
| 开箱即用       | 需要安装各种插件 | Yes        | Yes              |
| 远程调试       | Yes      | No         | Yes              |
| 远程文件夹      | 直接编辑     | No         | 本地与远程映射，sftp部署模式 |
| scm        | 安装扩展     | Yes        | Yes              |
| code merge | 没有三路归并   | 三路归并       | 三路归并             |
| wsl支持      | Yes      | No         | Yes              |
|数据库支持| 通过第三方|集成|集成|
|作为其它语言的IDE|Yes|可用于js开发，支持常见框架|同社区版|
|作为文本编辑器|轻量、高速|启动较慢，不合适|同社区版|

总的来说，除了代码合并，数据库支持之外，Vscode基本上都可以通过插件配置到与Pycharm专业版近似的程度。Vscode在展示DataFrame之类的数据表格方面不如Pycharm，不过这项功能并不是所有人都需要。但是目前还没出现能跟Pycharm匹敌的支持三路归并的vscode扩展，这是在多人协作开发过程中不可或缺的功能。为了弥补这个缺撼，我会在机器上安装一份Pycharm社区版，在需要时通过它来完成代码合并。

Pycharm能很准确地识别未使用的导入并自动清除，关于这一点，Vscode还没有扩展可以实现。Pycharm自己提供了语法检查功能，有自己定义的rules。Vscode下一般通过扩展，使用开源社区广泛接受的规则，这一点上，vscode更适合开源项目开发。

基于保护投资的考虑，我们建议花一点时间来学习使用Vscode。之后用以其它语言开发也很容易切换。而且Vscode真的非常适合开源项目的开发，各种工具之间的协作性非常好。

### Vscode及扩展的安装

vscode从[这里](https://code.visualstudio.com/)下载安装。

安装完成后，最主要的工作就是配置各种扩展，否则，Vscode是无法用于Python开发的。

我们推荐的扩展有：

#### Python

扩展id为ms-python.python，由微软团队开发，系官方扩展。它提供了调试、语法检查、代码提示与自动完成、代码格式化、代码重构、单元测试管理器等功能。其中有一些功能需要其它扩展，比如Pylance来支持。

安装完成这个扩展之后，您的IDE还将具有Jupyter Notebook功能。

安装完成之后，最重要的配置，是配置Python解释器。关于这一点，我们在后面介绍配置虚拟运行环境之后，再来讲解。//TODO

#### Pylance
微软开发的Python语言支持工具，提供代码的静态检查，代码自动完成等。它能够提示代码中使用了未定义的变量、变量声明了但未使用等许多语法错误。

#### Kite AutoComplete AI

又一个代码自动完成工具。与Pylance相比，它可以提供更详细的帮助文档，还可以提示他人的代码供参考。比如，当你创建一个Redis Client时，可能会为如何初始化它而犯愁，Kite就会提示你，其它人一般都如何初始化这个对象，有时候这会比阅读文档更快捷。

在安装Kite的vs-code扩展时，还要注意同时安装kite服务器。

#### Remote ssh/Remote wsl

根据您使用的Linux版本，选择安装Remote wsl或者Remote ssh。这两个工具帮助我们实现在wsl/linux上的远程开发。如果您是使用的WSL方案，则需要安装remote wsl，否则，请安装remote ssh。如果您按照[WSL服务自启动技巧](blog/tools/how_to_run_app_as_service_in_wsl.md)里的方法将WSL设置为自启动，并开启了ssh server的话，也可以仅使用remote-ssh来进行远程开发。两者的体验几乎是一样的。

另外，如果您安装的是wsl v2,可以只使用Remote ssh，因为wsl v2就象一台虚拟机。

安装完成remote-ssh之后，在side bar上会出现一个连接电脑的icon。

![](http://images.jieyu.ai/images/202104/20210402225647.png)

Remote ssh的工作原理是，它把远程文件夹虚拟成本地文件夹。在您连接远程服务器后，可直接打开在远程服务器上的文件进行编程、调试和运行。在这个过程中，您只需要告诉扩展如何连接远程服务器就可以了。

这个扩展也是我喜欢vscode甚于Pycharm的地方。在Pycharm专业版中，配置远程开发比较繁琐，要配置ssh连接和sftp部署、以及文件夹映射等。文件都是在本地编辑的，在运行调试之前，必须先将其同步到远程服务器上。偶尔这种同步还会出错。

#### GitLens, Git Graph, Git commit plugin, gitignore, Github Pull Request
顾名思义，这几个扩展是跟代码管理相关的。

使用vscode的Python程序员中，大约有1/4会安装Gitlens。我们通过它来管理branches, commits，File history, tags等等。如果您还不太了解这些概念，我们会在后面专门介绍。

Gutter blame是我非常喜欢的一个Gitlens功能。很多时候，我们在开发某个功能时，可能顺手改了某个小bug。对于bug的修改，一般遵循一个bug一次提交的原则。如果某个文件同时涉及功能和bug修改，没有这个Gutter blame的话，我们就必须将同一文件的两处修改混在一起提交，而通过Gutter blame，则可以单独提交这个bug fix：

![](http://images.jieyu.ai/images/202104/20210403093433.png)

上述截图中，红色框显示了一个Gutter blame，黄色框显示了变更的详细情况，比如通过"-"显示被移除的代码，通过"+"显示新增的代码。绿色框中的"+"号，则是用于提交此单项修改的提示。

???Tips
    此项功能Pycharm是开箱即用。Pycharm在SCM管理这一块做的非常好，UI也做得很直观，符合直觉。

curent line hover则是另一个我非常喜欢的功能。当你把光标移动到一行代码的结尾部分，就可能出现类似下面的提示框：

![](http://images.jieyu.ai/images/202104/20210403094408.png)

Current line hover清楚地提示了这行代码的历史。

Git Grpah启动后，会独占一个完整的工作窗口，这样可以一次性把commit的相关信息展示全，因此与Git lens相比，查找更方便。比如，当我们准备某一个版本的发布时，可能需要列出上一个版本以来所有的bug fix,这在git graph中是比较容易实现的。当然，更好的方法是平时就做好project管理，在提交bug和功能需求后，通过评审，将其规划到指定的版本中。

Git commit plugin虽然人气没有前两款高，但也是很值得推荐的一款扩展。它的主要作用是编辑commit message。它提供了一个commit的标准分类（据说源自于angular js团队），并且按照分类，给每个commit带上了emoji功能。对commmit进行标准化分类，能够有效地提高code review和查找效率。比如我们在进行code review时，一般可以直接跳过标记为docs, build等类型的提交（当然提交者也必须严格按规范，只提交该类型的修改，而不要夹杂其它修改）。

gitignore扩展用来辅助.gitignore文件的编辑。您可以从侧边栏的Source Control的文件列表中，右键打开菜单，添加选中的文件到.gitignore文件中。

Github Pull Request则是一个管理Github issues的工具。通过这个扩展，可以让您直接从vscode连接、加载github issues, 以及创建新的github issues。另外，它还有一个很好的功能，就是可以只通过一个点击，就帮您为待修复的bug创建专门的bug修复分支。

#### Markdown相关插件

在软件开发过程中，当然也少不了文档写作。Markdown是现在更流行的文档格式。推荐的扩展有Markdown preview Enhanced, Markdown table from csv。前者用显示Markdonw文档。后者可以将一段csv格式的内容转换成Markdown格式的表格，反之亦然。

到此为止，Vscode及Python开发所需要的扩展就安装好了。但是，到目前为止，我们还不能开始代码的调试，因为我们还没有指定Python解释器。在下一章，构建Python虚拟运行环境中，我们会详细讲到。

# 思考题
1. 为什么做Python开发，推荐的工作环境要构建在类Unix环境下？
2. 要使用基于图形界面的开发工具，又要在Linux环境下运行和调试Python程序，有哪些方法？
3. 什么是WSL？它有哪几个版本？主要区别是什么？
4. 开发Python最流行的集成开发环境（IDE）有哪些？如何进行选择？
5. Vscode是什么？选择vscode来进行Python开发和调试，必须安装哪一个扩展？









