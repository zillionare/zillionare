# 构建Python虚拟运行时环境

任何一个程序员都不可能从头到脚去开发程序的每一个模块。我们必然要借鉴和使用他人的开发成果，同时也希望我们的开发成果被更多的人使用。这样就必然引出一个问题： 如果我们的程序中使用了他人开发的模块，并且使用了它的早期版本；而另一个程序也使用了同样的模块，但使用的是晚期版本，这时候两个程序应该如何共存？

Python是我知道的最早通过创建虚拟运行时来解决这个问题的开发语言。开发者可以为自己的应用程序构建单独的虚拟运行时环境，在这个环境里，所有的第三方模块都只为这一个应用程序服务，因此它们的版本可以固定下来。在一台机器中，可以同时存在多个虚拟环境，也可以同时运行基于多个虚拟环境的多个应用程序。此外，用户安装您的应用程序时，通过创建虚拟Python运行时，也解决了权限问题--因为您不再需要去修改系统自带的Python环境了。

??? Readmore
    这个问题的出现至少可以追溯的Windows的早期。在Windows中，这些共享库以DLL（动态链接库）的形态出现。由于不同的版本相互冲突，导致出现了被称为DLL地狱的现象出现。为了解决这个问题，就出现了通过虚拟机从操作系统层面进行隔离的解决方案，随后又进化出基于docker的容器隔离方案。这些都是系统级的深度隔离，不仅程序文件之间不会冲突，就连网络资源和计算资源都是完全隔离的。运行在不同的虚拟环境中的程序，彼此无法看到对方的存在，它们可以打开同样的网络端口，读写同样路径中的文件而不会冲突--因为这些文件实际上并不是一个。

    Python的虚拟运行时只是程序文件这样的静态资源的隔离。同一主机上运行的不同Python虚拟运行时，彼此可以感知到对方的存在 -- 比如，可以在一个程序中去kill掉另一个程序；两个程序不能监听在同一个端口；如果读写相同位置的文件，则可能造成该文件损害等等。Python虚拟运行时能够保证的，就是运行在两个不同运行时中的程序库，可以有不同的版本。

Python中存在多种构建虚拟运行时的方案，在本教程中我们推荐使用conda，但是也会用到venv和virtual env。

??? Readmore
    Python中创建虚拟运行时的工具众多，包括pyenv, pyvenv, pipenv, virtualenv, pyenv-virtualenv, virtualenvwrapper,pyenv-virtualenvwrapper,pipenv, conda等。如此众多的工具存在，既反应了Python社区的活跃度，也反应了Python长期以来在打包、发行方面缺乏标准的现实。不过，情况正在起变化。

    Python为什么能支持虚拟运行时？这主要是因为，Python解释器被设计成为这样运行：当它根据import指令去查找module时，首先从自身所在的路径的相对路径下查起。因此，只要把应用程序的依赖库与Python安装在一起，那么Python就会首先使用这些依赖库，而不是安装在别的什么地方的依赖库。

    如此众多的工具，大致可以分为四个流派：

    pyenv及其变种（pyenv-*)主要基于shell script hook技术，仅能工作在Linux机器上。它将许多不同版本的Python安装在~/.pyenv路径下，并向系统路径中的Python插入一个楔子。然后您通过.python-version来指定应该使用哪一个Python，这样在调用Python时，这个楔子就能根据您指定的Python版本，来调用真正的Python解释器。基于pyenv的工作原理，可以看出，它不能完全满足我们创建Python虚拟运行时的那些要求，即为每一个应用创建自己专门的、与其它应用完全隔离的运行时。

    [Virtualenv](https://virtualenv.pypa.io/en/latest/)及venv是第二个流派。Virtualenv允许你为每一个应用程序都创建自己专门的、与其它应用程序完全隔离的运行时，这个运行时，一般就与您的应用程序文件安装在一起。从Python 3.3起，Virtualenv的一部分代码进入到标准库，即venv。随Python 3.3还一起发布了一个pyvenv的script，不过在3.6版本时就被标记为depreacted了。因此，Virtualenv和venv现在是创建Python虚拟运行时的主流工具，也被其它广泛使用的工具如tox，poetry所接纳。

    在venv成为标准库之后，为什么还需要使用Virtualenv呢？Virtualenv的官方说明是，Virtualenv性能更好，速度快，可以通过pip升级，以及更好扩展，API更丰富（毕竟venv只是它的一个子集）。

    pipenv是第三个流派，它的功能主要是两点，一是创建虚拟环境，二是进行依赖管理。不过pipenv在2018年11月到2020年4月间没有任何更新，这也导致了一部分用户流失（最近一段时间似乎又开始维护了）。现在社区更认可的依赖管理工具已经是Poetry了。

    第四个流派则是[conda[(https://docs.conda.io/projects/conda/en/latest/index.html)。Conda不完全是一个Python的虚拟环境构建工具，它是一个服务于Python，R，Ruby，Lua，Scala，Java等语言的发行包、依赖管理和运行时环境管理工具。
    
    与Virtualenv相比，conda提供的功能相当于Virtualenv + pip，当然您也可以在conda环境下使用pip。conda构建虚拟环境默认是集中式的，virtualenv则是分散式的，与应用程序安装在一起。两者在空间占用上也有较大区别，一个空的conda环境会占用122MB左右的空间，而空的virtualenv环境则只占用12MB空间，显然，使用virtualenv创建虚拟运行环境会更快。

    在我们的工作中，应该如何选择呢？首先，如果您在开发跟tox, poetry类似的软件，即需要随时构建新的一次性虚拟环境的，应该使用virtualenv或者venv；在我们自己的开发及应用程序部署中，推荐使用conda，毕竟这种长期使用的虚拟环境，更适合conda这种集中式管理模式。这种情况下，conda所占用的空间、以及创建虚拟环境所用的时间也可以忽略不计了。

## 安装conda

Conda共有两个版本，anaconda和miniconda。

多数从事数据科学的人会安装完整的anaconda。这一般会占用你硬盘上好几个G的初始空间，并且随着虚拟环境的创建持续增长。对从事工程开发的人来说，则可以从miniconda开始。两者的区别是，前者包含了很多科学计算用的工程包，比如numpy, scipy， sklearn等等，还有一个名为spyder的集成开发工具。后者只包含了包和虚拟环境管理系统。

Miniconda的下载地址在[这里](https://docs.conda.io/en/latest/miniconda.html)。一般是50M上下，包含了一个基本的Python解释器。Miniconda的python版本并不重要，因为后面我们都将为虚拟环境安装特定版本的Python。

我们将Miniconda安装到WSL中，因此，我们应该运行下面的命令（如果您使用Ubuntu，这些命令也是一样的，下同）：
```bash
sh <(curl -s https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)
```

![](http://images.jieyu.ai/images/2020-10/20201012220906.png)

如果WSL上没有安装curl，请先通过`suod apt install curl`来安装。

从anaconda官网上下载miniconda可能较慢，也可以先通过下载工具将上述文件下载下来，再传入到WSL中去。

## 修改源

与apt一样，在国内使用时，我们先要配置一下conda源，否则安装速度会很慢，甚至无法安装成功。

修改~/.condarc如下：

```
channels:
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
ssl_verify: true
```
上面的配置使用了清华的源，也可以使用如下中科大的源：
```
channels:
    - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
    - https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
    - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
ssl_verify: true
```

??? Tips
    配置源需要记忆一些URL，我们也可以使用[cfg4py](https://pypi.org/project/cfg4py/)来帮助我们。
    首先，安装cfg4py:

    ```bash
    # 首先安装cfg4py
    pip install cfg4py

    # 让cfg4py提示我们如何更改conda源
    cfg4py hint conda --usage
    ```

    我们将得到以下输出：
    ```bash
    Usage: execute command:
    conda config --add channels %url
    or edit your ~/.condarc to add the following:

    - tsinghua:
        channels:
        - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
        - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
        - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
        - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
        ssl_verify: true
    - ustc:
        channels:
        - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
        - https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
        - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
        ssl_verify: true
    ```
    cfg4py还可以提示如何配置pip源，apt源等。

## 创建虚拟环境
我们使用conda来创建虚拟环境：

```bash
conda create -n your_env_name python=3.8
```

上面的命令将在你的miniconda安装目录的envs目录下，创建一个名为your_env_name的文件夹，并将python 3.8及相关文件安装到这个目录下。安装完成时，conda会提示你使用以下命令：
```bash
conda activate your_env_name  #激活python虚拟环境
conda deactivate              #退出当前的虚拟环境
```

当虚拟环境激活时，命令提示符一般会显示为虚拟环境名字；此时运行python，会启动当前虚拟环境下安装的Python版本，而此后加载的Python库，都来自于该虚拟环境下通过conda或者pip命令安装的库。

关于conda还有一些常见的命令，这里一并提一下：
1. conda env list, 显示本机上所有的虚拟环境
2. conda env remove, 移除一个虚拟环境
3. conda create -n your_virutal_env --clone your_another_env，从另一个已存在的虚拟环境中创建。Conda没有改名的操作，所以如果要给一个虚拟环境改名，我们可以先clone，再删除掉旧的虚拟环境。
4. conda install, 安装软件到当前环境
5. conda search， 查找是否存在某个软件

??? Tips
    在上面的创建命令中，使用的是CPython发行版。conda还允许您使用特殊的Python版本，比如Intel发行版：
    ```bash
    conda update conda
    conda config --add channels intel
    conda create -n idp intelpython3_core python=3
    ```

    使用Intel版的Python的一个原因是，它可能提供了更强性能的数学计算功能。具体可以看[这里](https://software.intel.com/en-us/articles/using-intel-distribution-for-python-with-anaconda)。这对从事数据分析为主的程序员还是比较有帮助的。

# pip

构建虚拟环境当然少不了安装第三方库。前面提过了可以通过conda来安装Python库，但是，Python库最重要的发行系统是[pypi](https://pypi.org)，它的客户端则是pip。pypi整个系统由[中央服务器(central repo)](https://pypi.org/simple)及分布在各地的镜像服务器组成服务器；pip客户端用来从服务器上搜索和下载python库；此外，客户端还提供安装、卸载、查询本地已安装库的功能。

pip和pipenv都是[pypa(Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/)的产品。

# 思考题
1. 有哪三个重要原因，使得我们需要创建Python虚拟运行环境？
2. 什么是virtualenv? 它与venv是什么关系？
3. 什么是pipenv?现在一般使用什么工具来替换pipenv?
4. 什么是conda？conda有哪两个发行版本？如何进行选择？
5. 为什么要替换conda源？国内有哪些conda源可以使用？
6. conda与virtualenv有何区别？
7. 要使用一个python库，我们应该如何去搜索和安装？
