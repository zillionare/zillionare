---
title: 03 构建Python虚拟环境
---
在上一章里，我们讨论了构建开发环境的基本步骤，如选择操作系统、选择集成开发环境等。现在我们可以着手编写代码了，但要能运行和调试程序，还需要指定Python运行时（或者称之为解释器）。特别地，如果你使用的开发工具是VS Code，那么这一步是必须的：因为VS Code并不是只为开发Python应用程序而设计的，它支持好多种开发语言。因此，要使得VS Code知道你的工程项目是基于Python的，就必须为它指定Python运行时。

Python有两个主要的运行时版本，Python 2.x和Python 3.x。Python 3.x是对2.x版本的破坏性升级。当前，需要在3.x版本下运行的应用程序和组件越来越多了，然而，像MacOs或者Ubuntu这样的操作系统，它的一些老旧版本仍然依赖Python 2.x来运行一些核心功能，比如包管理。因此，在这些系统上，Python 2.x仍然是缺省安装的Python运行时版本。

!!!info
    Python 2.7是Python 2.x系列的最后一个版本，已于2020年1月1日终止维护；Python 3.7则于2023年6月27日终止维护。因此，当您开始一个新的项目时，应该尽可能避开这些老旧的Python版本。

这会是你在开发Python应用时的将会遇到的第一个问题：你想要开发一个Python应用程序，使用了最新的Python版本，有着大量酷炫的新特征和新功能。但当你的应用程序部署时，可能被部署到各种各样的机器上，这些机器上缺省安装的Python版本，并不是你开发时指定的版本。如果强行升级系统缺省安装的Python版本，则可能会破坏其它应用程序；而如果不进行升级，则又没办法运行你的程序。

即使目标机器和你的应用程序使用了同样的Python版本，类似的冲突还可能发生在其它组件上。比如Django是Python社区中最负盛名的web开发框架。它依赖于SQLAlchemy -- Python社区中另一个同样颇负盛名的开源orm框架。如果你的程序也依赖于SQLAlchemy，并且你使用了SQLAlchemy 1.4以上的版本，而Django使用了它的早期版本，那么很不幸，这两个应用程序将无法共用同一个Python环境： SQLAlchemy 1.4相对于之前的版本，是完全不兼容的破坏性更新。

这类问题被称之为依赖地狱。依赖地狱并不是Python独有的问题，它是所有的软件系统都会面临的问题。

# 1. 依赖地狱

在构建软件系统时，通常都会涉及功能复用的问题。毕竟，“重新发明轮子”是一种不必要的浪费。功能复用可能发生在源代码级别、二进制级别或者服务级别。源代码级别就是在我们的工程中，直接使用他人的代码源码；二进制级别是指在我们的应用中使用第三方库；服务级别的复用，则是程序功能以服务的方式独立运行，其它应用通过网络请求来使用这种功能。

当我们使用二进制级别的复用时，就常常会遇到依赖地狱问题。比如在上面Django的例子中，如果没有一种方法可以向Django和你的应用分别提供不同版本的SQLAlchemy，则这两个应用将无法同时运行在同一台机器上。

依赖地狱并不是Python独有的问题。所有的程序开发语言都会遇到类似的问题。解决这个问题的方法之一，就是将程序的运行环境彼此隔离起来。比如，应用程序所依赖的第三方库，不是安装到系统目录中，而是安装到单独的目录中：比如，随着该应用程序一起安装到该应用程序所占的目录中，并且，只从这个目录中加载依赖的第三方库。

Python解释器本身也可以看成一个普通的应用程序。因此，当我们安装一个Python应用程序时，可以将该程序依赖的Python运行时，及相关的第三方库，都安装到一个单独的目录中。这样，当我们运行该应用程序时，就从该目录中启动Python，如果Python只从（或者优先）该目录加载第三方库的话，我们就实现了某种程度的隔离。这种思想，就是虚拟运行环境的思想，它是解决Python依赖地狱问题的一个主要方法。

既然我们提到了“隔离”一词，我们不妨再稍稍引申一下。在第二章我们提到了虚拟机和Docker容器，这些是解决资源冲突，对资源进行隔离的方法。现在，通过容器以(微)服务的方式来部署Python应用程序也越来越常见，其中也有简化安装环境、避免依赖地狱等方面的考虑。

在这一章我们主要讲如何构建虚拟运行环境，这样可以完全解决运行时与其它应用程序之间可能发生的依赖地狱问题。然而，依赖地狱还有其它多种表现形式，我们后面还会在讲述Poetry那一章再探讨这个问题。
# 2. 使用虚拟环境逃出依赖地狱
Python的虚拟环境方案可谓源远流长，种类繁多。如果你接触Python已经有一段时间了，那么你很可能听说过annaconda, virutalenv, venv, pip, pipenv, poetry, pyenv, pyvenv, pyenv-virtualenv, virtualenvwrapper, pyenv-virtualenvwrapper等相似概念。   

!!! Info
    在Zen of Python之中提到的一个重要原则就是：
    There should be one -- and preferably only one -- obvious way to do it.
    永远都应该只有一种显而易见的解决之道

    从Python的虚拟环境解决方案之多来看，要达到这样的境界似乎是困难的。人们试图建造巴别塔，但上帝会毁灭它。不过，类似的困境并非 Python 独有。比如， Javascript 在其高歌猛进、攻城掠寨式的行进中，自身的语法也在发生剧烈的改变，以至于有人不得不开发一个模块来翻译不同版的 Javascript 语法，这个模块就叫 Babel （巴别塔），倒也恰如其分。

在上面这些令人眼花缭乱的词语中，Annaconda(以下简称conda)和Virtualenv是一对儿对手，Pipenv则和Poetry相互竞争。而Venv则是其中血统最为纯正的一个，得到了Python官方的祝福。

pipenv和poetry，尽管常常被人在讨论虚拟环境的场合下提起，也确实与虚拟环境相关，但他们所做的工作都远远超过了虚拟环境本身——它们的主要功能是提供依赖管理，poetry还提供了构建和打包功能（我们将在第五章——Poetry那一章中来详细介绍）。

venv不是一个独立的工具，它只是一个模块。venv是从Python 3.8起，标准库里提供的一个模块，你可以使用`python -m venv`来运行它。它的目标与virtualenv比较接近，但只提供了virutalenv的一个命令子集。由于它是标准库提供的，因此许多工具，比如poetry, pyenv现在都是基于它来构建的。因此，如果你是某个工具的开发者，我想你需要掌握它；否则，你将在使用poetry等工具时，自然而然地接触和使用到它，但可能并不知道，幕后英雄其实是venv。

conda和Virtualenv都是用来创建和管理Python虚拟环境的工具，有着相似的命令行接口，不同之处在于：

1. Conda是一个多语言、跨平台的虚拟环境管理器，而Virtualenv则只用于Python。
2. 通过Conda可以管理（安装、升级）Python版本，而virtualenv则没有这个能力。
3. 缺省安装下，conda会占用大约100MB的磁盘空间，而virtualenv则只需要占用更少的空间（约10MB）。这可能既是优势，也是缺点。virtualenv通过使用对原生库的符号链接来减少对硬盘空间的使用，这使得对原生库的隔离并未真正实现--如果你的应用程序不仅仅依赖Python库，还依赖于原生库，则仍然可能产生依赖冲突，导致你的程序出现一些很难查找原因的错误。而在conda虚拟环境中，所有的依赖都是完全隔离的。
4. 缺省地，conda对虚拟环境进行集中式管理，所有的虚拟环境都在一个目录下，而virtualenv则倾向于将虚拟环境放在当前目录下。长期来看，非集中式管理可能导致这些虚拟环境呈碎片化而难于被追踪。

上述第3点可能是最重要的差异。我们很难保证Python应用程序永远只依赖于纯的Python库。事实上，一些性能相关的模块，往往是用c++或者其它语言来开发的。Lapack（一个常用的线性代数库，Python中最著名的科学计算库Numpy和scipy都依赖于此）或者OpenSSL都是常见的例子。

在本书中，我们只推荐使用Annaconda。但对virtualenv和venv，读者需要知道的是，如果正在开发一个生成和构建虚拟环境的工具（或者模块）—— 比如，为一个容器构建一个虚拟环境，或者为分布式程序动态构建一个远程的虚拟环境--那么venv或者virtualenv将是不二之选，因为conda并不是一个轻量级的工具。

对上面没有提到的那些技术，我们将不会在本书中详细介绍它，这里仅对它们做一个概括性的描述：

1. pyenv是一个脚本，不能在windows环境下使用。它的作用是拦截你对python工具链的调用，为你选择正确的python版本。此外，你也可以使用它来安装多个版本的python。它的功能完全可以诸如annaconda之类的工具替代。但如果你使用virtualenv的话，那么很有可能你仍然需要使用pyenv来安装和选择python版本。它目前在github上有超过28k的star。
2. pyenv-virtualenv则是pyenv的一个插件，它将pyenv和virtualenv结合在一起，从而使得我们可以同时方便地使用两者的命令。如果不在乎这种便利性，也可以分别使用pyenv和virtualenv。
3. Virtualenv wrapper是virtualenv的一个扩展集，提供了诸如mkvirtualenv, lssitepackages, workon等命令。workon是用来在不同的virtualenv目录中进行切换的命令。
4. pyenv-virutalenvwrapper则是pyenv的另一个插件，由pyenv的作者开发，它将pyenv和virtualenvwrapper的功能集成在一起。基于这些扩展，virtualenv就拥有了类似conda的全部功能。
5. pyvenv（请不要与pyenv相混淆）是仅在python3.3到python3.7才有的一个官方脚本，但从python3.8开始，它已经被标准库venv代替了。
   
在读过上面这段文字之后，你可以在之后完全忽略这些奇奇怪怪的方言。几乎你需要的任何管理虚拟环境的功能，都可以从本书推荐的方案中得到。
## 2.1. Anaconda：一站式管理的虚拟环境
Anaconda包揽了从安装python版本、创建虚拟环境和切换虚拟环境的所有功能。它的官方网站是[Anaconda.org](https://www.anaconda.org/)。它是所有从事数据科学或者深度学习的人的当然之选。它自带的包管理系统，提供了许多流行的机器学习库预编译版本，因此你不用自己去熟悉gcc和c/c++代码的编译过程。
### 2.1.1. 安装Anaconda
安装Anaconda请从这里[^anaconda]页面下载安装包。除非您使用Anaconda进行科学计算，否则建议您下载最新的miniconda[^miniconda]安装包。

以Ubuntu为例，无论是Ananconda还是Miniconda，其安装文件都是一个包含了安装数据文件的shell脚本，您可以通过wget或者curl将其下载下来，然后执行这个脚本进行安装。

安装过程中，首先要求你阅读并接受Anaconda的服务条款，然后选择将要安装的目录。在完成文件拷贝之后，会询问你是否要运行conda init以初始化conda环境，推荐选择yes，这样conda会修改你的shell初始化脚本。要使用conda，这一步是必须的。

conda安装完成后，就会在你的系统上生成第一个虚拟环境，称为`base`。现在可以列一下刚刚安装了conda的目录，这里面最重要的目录是envs，后面创建的新的python虚拟环境都会在这里。但现在它是空的，尽管已经有了一个名为base的虚拟环境，但这个虚拟环境，指向的是安装目录下的/bin目录下的python。
### 2.1.2. 配置conda环境
conda安装后，一般情况下，无须配置即可使用。但是，如果我们需要使用代理服务器，或者变更conda源以加快下载速度，则需要配置conda。

conda的配置文件是用户目录下的.condarc，它是一个YAML格式的文件。这个文件直到你第一次调用conda config时才会产生，比如，增加一个conda源：

```shell
conda config --add channels conda-forge
```

我们也可以直接编辑.condarc文件:
```yaml title=".condarc"
channels:
  - https://mirrors.aliyun.com/anaconda/pkgs/free/
  - https://mirrors.aliyun.com/anaconda/pkgs/main/
  - file:///some/local/directory
  - defaults
proxy_servers:
    http: http://user:pass@corp.com:8080
    https: https://user:pass@corp.com:8080
    ssl_verify: False
```
上述示例中，首先配置了conda源。我们添加了国内常用的阿里镜像，并且添加了一个本地目录。如果我们有一些内部安装包，就可以放在这个目录下。当conda无法从阿里镜像服务器上找到这些包时（显然会找不到），就会搜索这个目录。上面所有的路径都失效时，conda最后会使用系统默认的源来搜索。这种情况多见于某个包有了最新的版本，但镜像服务器还没有同步过去的情形。

有时候访问conda的官方源时，我们需要使用代理服务器来进行加速。上面的示例显示了如何进行这些配置。有一些代理服务器对ssl验证支持的不是太好，这种情况下，你需要设置ssl_verify为False,正如以上示例所示。

conda还允许其它一些配置，如果有需要，推荐读者进一步阅读配置conda[^config]。
### 2.1.3. 创建和管理虚拟环境
现在，我们来创建一个虚拟环境，并且通过conda的一些命令来看看如何管理它。

```shell
$ conda create -n test python=3.8
```
上述命令创建了一个名为test的虚拟环境，并且安装python=3.8。现在我们查看一下，当前系统中，都存在哪些虚拟环境：

```shell
$ conda env list

# 输出应该类似于：
# conda environments:
#
base           /root/miniconda3
test           /root/miniconda3/envs/test
```
上面的输出表明，我们在/root下安装了一个miniconda，并且还创建了一个名为test的虚拟环境。这个虚拟环境的文件夹是/root/miniconda3/envs/test。

现在让我们切换到新创建的这个虚拟环境中：
```shell
$ conda activate test
```
现在，你的shell提示符应该修改为类似于：
```
(test) root@ubuntu:~# 
```
我们的测试是在一个ubuntu虚拟机上，直接使用了root账户来进行测试。所以，上面的提示符中，root是当前用户名。在当前用户名之前的(test)，表明我们当前处在test虚拟环境中。

要往这个虚拟环境中安装一个包，可以使用conda install命令：
```sheel
$ conda install PACKAGENAME
```

现在，假设我们要移除这个虚拟环境：
```shell
# 退出当前的虚拟环境test，以便可以删除它
$ conda deactivate
$ conda env remove --name test
```
上述命令不会给你确认的机会，所以，在使用这个命令之前，必须小心。当然，conda这样设计并没有任何问题，虚拟环境本身就应该是可以随时创建和随时销毁的。如果不小心删除错误，那么重建一个就好了。后悔药一直都在。

在结束这一节内容之前，我们还想介绍一些高级使用方法，掌握这些方法，会在出现疑难问题时，更加容易解决问题。

首先，我们可以通过conda info命令来检查conda安装的一些关键信息：
```shell
$ conda info

     active environment : base
    active env location : /root/miniconda3
       user config file : /root/.condarc
          conda version : 4.13.0
         python version : 3.8.12.final.0
       base environment : /root/miniconda3  (writable)
      conda av data dir : /root/miniconda3/etc/conda
           channel URLs : https://mirrors.aliyun.com/anaconda/pkgs/main/linux-64
                          https://mirrors.aliyun.com/anaconda/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/main/linux-64
                          https://repo.anaconda.com/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/r/linux-64
                          https://repo.anaconda.com/pkgs/r/noarch
          package cache : /root/miniconda3/pkgs
                          /root/.conda/pkgs
       envs directories : /root/miniconda3/envs
                          /root/.conda/envs
```
上面的内容是conda info的输出（为了简洁起见，删掉了一些不重要的内容），它揭示了一些关键信息：

1. 当前我们处于base虚拟环境下。这是当你安装了conda之后，就默认存在的一个虚拟环境。它的文件目录是/root/miniconda3。如果你是在test虚拟环境下，则active env location应该指向/root/miniconda3/envs/test
2. 配置文件在/root/.condarc下。前面我们介绍配置conda时，已经用过这个文件了，但是为简洁起见，在那里并没有告诉读者这个文件的位置。现在你就知道，如果不清楚conda配置文件的位置，可以使用conda info命令来查看。
3. 上述输出还显示了conda源的配置。
4. conda下载安装包时，会将其缓存。package cache告诉我们conda缓存安装包的位置。当我们发现安装包的行为不正常时，有可能要清除这个缓存。
5. 最后，envs directories告诉我们，所有虚拟环境的文件目录位置何在。我们可以列一下/root/miniconda3/envs目录：
```
ls /root/miniconda3/envs
# 输出中包含test
ls /root/miniconda3/envs/test
# 输出中将包含以下重要目录：
bin # 在bin目录下，存放有python, pip等重要命令
lib # 在lib下，存放有python3.x目录，site-packages等安装包将最终安装到这里。
```

另一个对查错有用的重要命令，是conda list。它将列出当前conda环境下已安装的库（package）。

### 2.1.4. 几个常见问题

1. 可以重命名一个虚拟环境吗？
从conda 4.14起，conda支持重命名虚拟环境：
```
$ conda rename -n old_name -d new_name
```
不过，上述命令其实只是conda create和conda remove的简单组合，所以，在旧的conda版本下，你可以：
```
$ conda create --name new_name --clone old_name
$ conda env remove --name old_name
```
2. 如何追踪一个虚拟环境的变更？
这是conda提供的一个有用的功能之一，即可以追踪一个虚拟环境的变更历史：
```
# 切换到关注的虚拟环境，并运行以下命令：
$ conda list --revisions

# 恢复变更到某个镜像点
$ conda install --revision 2
```
注意区分conda list与conda env list。后者是列出虚拟环境，前者则是列出当前虚拟环境里安装的packages和版本。

如果想全面而快速地了解conda命令，可以参考conda小抄[^cheatsheet]。

## 2.2. 轻量的Python包安装工具Pip
在上一节，我们介绍了如何往虚拟环境中安装程序库：
```
$ conda install PACKAGENAME
```
您也可以使用pip来安装程序库：
```
$ pip install PACKAGENAME
```
实际上，以您前面创建的test环境为例，conda已经把pip安装到了/root/miniconda3/test/bin目录下：
```
$ ls /root/miniconda3/envs/test/bin
```

Pip有很多有用的功能，这里简单介绍一些：
1.	从wheel文件或者github进行安装。
2.	从本地文件目录进行安装。这在开发调试阶段中非常有用。它的命令是 pip install -e path/to/your/source。这里的 ‘-e’ 是关键。这样一来，我们每一次对源代码的修改，都会自动生效，而不再次安装。
3.	仅下载wheel文件，而不进行安装。
4.	安装非正式发布的文件，比如某个alpha版本。需要使用选项’--pre’。
如果我们执行pip安装命令时，提示找不到某个包，在排除了键入错误之后，那么很可能是在当前使用的Python版本下，不存在该包。

## 2.3. 配置VS Code中的解释器

我们已经创建了一个虚拟环境，安装了python。但要在VS Code下开发python应用程序，我们还得在VS Code中完成相关的配置。

在VS Code中，打开命令面板(在mac下是cmd+shift+p, 其它操作系统中是ctrl + shift + p)，输入 Python: select Interpreter，如下图所示：

![](https://images.jieyu.ai/images/20220820220821195956.png)


就会出现如下图所示的列表（您的电脑上显示会有所不同）：

![](https://images.jieyu.ai/images/20220820220821200119.png)

如果要选择前面创建的test环境，也可以直接在这里输入：
```
/root/miniconda3/envs/test/bin/python
```

此外，您也可以在VS Code的状态栏中，寻找类似下面的提示文字：

![](https://images.jieyu.ai/images/202211/20221224143053.png)
然后点击它，也可进入"python: Select Interpreter"菜单。

大功告成！

至此，您就完成了最基础的开发环境设置：IDE已经安装好，并且要使用的python版本也已经指定！现在，您就可以编写一个最简单的python程序：
```python title="helloworld.py"
print("Hello World")
```
把这个程序存为helloworld.py，然后可以在命令行下，通过`python helloworld.py`来运行它！

[^anaconda]: https://www.anaconda.com/products/distribution
[^miniconda]: https://docs.conda.io/en/latest/miniconda.html
[^config]: https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html
[^cheatsheet]: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf
