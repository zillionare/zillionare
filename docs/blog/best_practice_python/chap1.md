# 开发环境和工具

如果您打算长期使用Python作为开发语言，并且想要开发一些严肃认真的项目，而不仅仅是在处理数据、完成一些自动化任务时临时用用Python的话，推荐您始终使用类Unix的操作系统来构建开发环境。

这里所指的类unix操作系统，是指各种Linux发行版和MacOS。如果您正在使用FreeBSD等一些正宗的Unix操作系统，当然也是可以的。不过从使用人数、社区活跃度来讲，使用MacOs，或者Ubuntu都是不错的选择。

对于新手来讲，可能更熟悉Windows系统。但是，Python从诞生之初，就与开源社区结缘，Python中大量的第三方库，往往在类Unix环境下测试更充分，或者优先推出。类Unix系统似乎天生是程序员的首选平台。

现在，就连Windows自身也在积极拥抱Linux了。有一句调侃的话说，最好的Linux发行版是哪一家的？微软。这是真的，通过Win10的WSL发行的Ubuntu，已经得到相当数量的下载，很可能已经是Ubuntu的发行量第一的渠道了。

所以，如果您只有Windows电脑，我也建议您基于Linux来构建开发环境。当然，您并不需要重装系统。您只需要使用虚拟化技术，就可以同时工作在两种操作系统下了。

???+ Readmore
    Unix是最早出现的多用户服务器操作系统之一。由Bell实验室发明。现在比较常见和容易得到的Unix操作系统有加州伯克利大学从1975年起开发的FreeBSD。进入20世纪80年代以来，出现了现代Windows和MacOS的雏形，分别由微软和苹果公司开发，现在已成为排名第一和第三的桌面电脑操作系统。上世纪90年代，Linux操作系统异军突起，随着云计算的发展，Linux因为其开源带来的低成本特征，迅速占领了服务器操作系统的头把交椅。

    Ubuntu是Linux的一个重要的发行版，其桌面版在国内十分流行。

## Windows下的虚拟Linux环境

如果您已经有了一台Linux机器（或者MacOS),请跳过这一节阅读。

如果您使用的Windows版本是Win10专业版（及以上）版本，您就可以使用wsl方案。如果使用的是Win7，或者Win10家庭版，WSL无法在这些操作系统上运行，您可以选择使用docker或者虚拟机的方案。

在这里我们只介绍安装WSL来获得Linux虚拟机的方法。您也可以使用通过Docker，或者虚拟机（VMWare或者VirtualBox)来使用Linux的方法。这些技术方案已经成熟很多年，不需要特别介绍了。如果您还不熟悉，网上可以找到很多教程。

### 安装WSL

WSL是Windows Subsystem for Linux的首字母简写。它是基于Windows的Hyper-v架构一种比Docker更为轻量级的虚拟化技术。

???+ Readmore
    Docker最初是一种基于Linux容器隔离技术诞生的一种虚拟化技术。当其在Linux下运行时，可以与Host操作系统共享资源，因此是一种十分轻量的虚拟化技术。在Windows下使用Docker，Windows必须先模拟出来一个Linux的操作系统，这个操作系统层必须静态分割和独占主机的资源，比如CPU和内存。因此，在Windows一旦启动了Docker服务，无论您当前是否有容器在运行，都要占用相当一部分CPU和内存资源。

    因此，在Windows下要开启Linux虚拟机，首先考虑的是安装WSL。

WSL有两个版本。版本二更象是虚拟机技术，提供了完全的Linux体验（兼容所有系统调用），但与宿主机的隔离性更强一些，融合体验要差一点。当在两个系统间来回读写文件时，版本二性能会弱一些，这也是我们推荐版本一的重要原因。当您使用版本一时，是可以在WSL里创建文件，然后在Windows中打开它的；反之亦然。版本二要么不能这么使用，要么有严重的性能问题。

关于两者的区别的详细比较，可以阅读[WSL两个版本的比较](https://docs.microsoft.com/en-us/windows/wsl/compare-versions)


首先，要启用"适用于Linux的Windows子系统“功能：
![](http://images.jieyu.ai/images/2020-05/20200503185200[1].png)
接下来，从应用商店搜索安装Ubuntu就可以了：
![](http://images.jieyu.ai/images/2020-05/20200503191417[1].png)

??? Tips
    如果启用WSL失败，请检查启用或者关闭Windows功能中，是否启用了"虚拟机平台”（有的Windows版本里，可能叫Hyper-v支持），并且检查BIOS里相关虚拟化支持。

    如果您的机器不是太老旧的话，一般无须关注BIOS选项。它们一般是打开虚拟化支持的。

安装完成后，可以在搜索栏输入ubuntu进入命令行窗口。这样就启动了WSL。如果您关闭了这个窗口，那么这个子系统，以及里面运行的程序，就一同关闭了。

如果您安装的是版本二，那么您可以完全按照自己掌握的Linux操作系统知识来使用WSL。如果是版本一的话，您要记住，WSL与Linux的主要区别是，它没有rc，init.d这样的系统。除此之外，几乎所有应用程序都是可以运行的，除了它们不能以服务的方式启动之外。

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








