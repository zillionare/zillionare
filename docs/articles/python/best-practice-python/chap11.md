---
title: 11 发布应用
---

我们的探索之旅，就要接近 Python 开发流水线的终点了。终点站的主题是如何打包和发布应用。

Python 开发项目的成果，可能是一个 Python 库 (package)，也可能是一个独立运行的应用程序（桌面应用程序或者后台服务）。

Python 库的分发可能大家比较熟悉了。 PyPA（PyPA 是 Python 软件基金会 -- Python Software Foundation，简称 PSF 资助的一个核心项目）通过 PyPI 和一系列工具，为 Python 库的分发提供了事实上的标准和基础设施。

分发应用程序则要复杂不少。取决于我们使用的框架、技术和用户的使用方式，我们的应用程序可能需要分发到服务平台（Serivce platforms）-- 这一般适用于构建托管的 SaaS 服务，比如那些部署在 Heroku， Google App Engine 平台上的服务；也可能是部署在云上（无论是公有云还是私有云）的单个或者一组相互合作的容器 -- 这些都是适合于服务的模式；也有可能这是个面向消费级用户的 App，需要通过 App store, Android 市场，或者 Windows 商店来分发 -- 这就还涉及向导式安装程序的制作，以及如何运行 Python 程序的问题。

Python 项目应该使用哪种方式进行分发，取决于用户的使用方式，以及是否涉及定制化安装。一些 Python 库可以通过 console script 的方式，在命令行下运行。如果一个 Python 库以 pip 的方式安装后无须配置即可运行，并且用户自己知道如何安装 Python（及可能会创建虚拟环境），这样来分发应用也是允许的。但对多数消费级应用的用户而言，他们恐怕并不懂得如何通过 pip 来安装应用，并在命令行下启动应用。此外，通过 pip 安装时，安装过程中无法接受用户输入，因此，安装过程无法定制（比如，无法让用户选择安装目的地、也无法让他们输入账户信息等）。

# 1. 以 PYTHON 库的方式分发

在程序库的分发上，很多语言都建立了中央存储库和包管理器生态，比如 Java 的 Maven，Ruby 的 RubyGems，Node.js 的 npm，Rust 的 Cargo，甚至 C/C++也有了 Conan。与其它语言类似，Python 库的分发也是通过一个中央索引库 (The Python Package Index) 来实现的，简称 PyPI，启用于 2003 年。PyPI 的启用是 Python 得以加速发展的重要因素，因为 Python 广受欢迎的原因之一就是它的生态系统非常丰富，PyPI 则正是构建这个生态系统的核心。

让我们把时间拉回到 2000 年。当 Python 1.6 发布时，它添加了一个有意思的功能，distutils，奠定了 Python 的打包工具的开端。彼时它的功能还很简单，只提供了简单的打包功能，没有声明依赖和自动安装依赖的功能。

2004 年， distutils 演化成为 setuptools，引入了新的打包格式 -- egg。把包格式命为 egg 是一种程序员式的浪漫和幽默，因为蟒蛇是通过下蛋来实现繁殖的，而 Python 库正是 Python 开枝散叶的一个重要载体。同样的类比在其它语言中也存在，比如 Ruby 语言与 gems 的关系。 egg 文件实际上就是一个 zip 包，只不过名字不同而已。这一阶段的 setuptools 还提供了一个新的命令，easy_install，用来安装 python eggs，不过这个命令在 2.7 之后就被移除了。

2008 年，PyPA 发布 pip，替换掉了 easy_install，随后将打包工具的行为标准化为 PEP 438。

在 2012 年时，随着 PEP 427 的通过，一种新的打包格式，即 Wheel 格式取代了 egg 格式，成为构建和打包（二进制）Python 库的标准格式。

尽管在《zen of Python》中写道，"永远都应该只有一种显而易见的解决之道"，但是，理想照进现实的过程总要经过曲折的投影。我们一路讲述下来，读者已经发现，Python 在虚拟环境、依赖解析和打包构建等领域都先后出现了好多个方案来解决相似的问题，出现了让人莫衷一是的“百花齐放”，如果没有经过系统的梳理，很多人会难免感到困惑，不知道哪一个方案能够通向未来，自己掌握的技术与资讯，是否已经被社区抛弃。好在 Python 社区现在已经通过一系列的 PEP 回答了标准问题，相关的工具和生态逐渐在遵循标准的基础上建立起来了，今后的这样的“百花齐放”，可能会少一些。是否遵循最新的 PEP，也正是 ppw 工具和本书选择某项技术的准则。

在`ppw`中，我们的发布是在 Github Actions 中完成的。这部分我们已经在 [持续集成](chap09.md) 那一章讲过了。万一你存在手工发布的需求，那么请回顾 [基于 Poetry 进行发行包的构建](chap05.md#基于 Poetry 进行发行包的构建)那一节。

这里简要地回顾一下，在 Poetry 出现之前，我们是如何发布 Python 库的，以防读者偶尔还会遇到需要维护老旧的 Python 项目的情况。在 Poetry 之前，我们需要通过 twine 这个命令来发布 Python 库。这个命令可以通过 pip 来安装：

```shell
$ pip install twine
```

尽管`ppw`生成的项目中，我们使用了别的技术来发布 Python 库，但这个命令也保留了下来。用在`poetry build`之后，检查构建物是否合乎 PyPI 的规定，以提前预防发布失败。

## 1. 打包和分发流程

打包和发布是一个从开发者的源代码起，到用户可以安装并使用的 Python 库的过程。这个过程中，我们需要经历以下几个步骤：
1. 准备一份包含将要打包的库的源代码，通常是从版本控制系统检出。

2. 准备一个描述包的元数据（名称、版本等）以及如何创建构建工件的配置文件。对于大多数库，这将是一个 pyproject.toml 文件，在源代码树中手动维护。

3. 完成构建；生成结果的文件格式是"sdist"和（或）"wheel"。这些是由构建工具使用上一步中的配置文件创建的。

4. 将构建的结果上传到包分发服务（通常是 PyPI）。

此时，您开发的 Python 库就出现在了分发服务器上。要使用这个库，最终用户必须下载和安装它。通常我们使用 pip 来完成这个过程。

### 1.1. 打包格式：sdist 和 wheel
Sdist 和 wheel 是两种不同的打包格式，虽然本质上，它们都是 zip 格式，但两者在打包内容上有所不同，特别是当 Python 项目中包含需要编译的 c 代码时，这种区别就更明显。

Sdist 格式的主要作用是通过推迟二进制文件的构建，使得您的 Python 库有可能安装到更多平台上去。比如，如果您的 Python 库中使用了 Cython 和 c 代码来进行性能优化，这部分代码是不具备 Python 那样的跨平台能力的。换言之，我们必须为每一个平台单独构建原生二进制文件。一般我们会为几个主要的平台预构建一些原生二进制文件，而能一些特殊平台（比如 Raspberry Pi, Alpine）运行上的二进制文件，往往就必须推迟到安装时，在本机进行编译构建。此外，延迟构建也允许在构建时，进行一些编译优化，以最有效地利用平台的性能，这也是预构建方法所做不到的。此外，我们常常还会把单元测试、示例都打包在 Sdist 格式中。

与 sdist 不同，wheel 中只包含已经编译好，可以立即安装的文件。如果项目中包含 c 扩展，这些扩展将在打包时被编译成二进制文件，再将其结果包含在 wheel 中。Pip 在安装 wheel 时，只是简单的文件拷贝。因此，wheel 格式的包在安装时会更快一些。

与 sdist 不同，wheel 中只包含已经编译好，可以立即安装的文件。如果项目中包含 c 扩展，这些扩展将被事先编译后，再将其结果包含在 wheel 中。Pip 在安装 wheel 时，只是简单的文件拷贝。因此，wheel 格式的包在安装时会更快一些。

在 Poetry 构建的项目中，一般会同时生成 sdist 和 wheel 格式的安装包，如果是 sdist 格式，poetry 会生成一个简单的 setup.py 文件。在安装上，如果没有特别指定，pip 总是优先选择 wheel 格式。

!!! attention
    无论是 sdist 还是 wheel，它们的安装都不是传统意义上的应用程序安装：在安装过程中，都不能接受用户输入，实现定制。尽管 sdist 当中存在 setup.py 这个脚本可以执行任意代码，但该脚本仍然无法接受用户通过控制台的输入。这可能是不太为人所知的一个冷知识。总之，sdist 和 wheel 是用来打包程序库 (package) 的，它们**不能用来制作应用安装程序**。

### 1.2. 分发包的元数据

在创建的分发包中，包含了一个名为 METADATA 的文件。这个文件的内容如下所示：
```
Metadata-Version: 2.1
Name: sample
Version: 0.1.0
Summary: Skeleton project created by Python Project Wizard (ppw).
License: MIT
Requires-Python: >=3.8,<3.9
Classifier: Development Status :: 2 - Pre-Alpha
...
Classifier: Programming Language :: Python :: 3.9
Provides-Extra: dev
...
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
...
Requires-Dist: virtualenv (>=20.13.1,<21.0.0) ; extra == "dev"
Description-Content-Type: text/markdown

# SAMPLE

this is hotfix 533
...

* TODO

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool...
```
文件内容进行了适当的删节。

这个文件中有一些字段我们需要简单介绍一下

Name，Author，Author-email，License， Homepage, Keywords, Download-URL 等字段的含义不言自明，无须解释。在旧式的项目（即通过 setuptools 来打包的项目）中，这些字段都要指定在 setup.py 文件中，并传递给一个名为`setup`的可以接受非常多参数的函数。在使用了 Poetry 的项目中，Poetry 会从 pyproject.toml 文件中提取这些信息。

**Platform 字段**用来指定特殊的操作系统要求。
**Supported-Platform 字段**，用来指定更详细的操作系统和 CPU 架构支持，比如指定 Linux 为 RedHat，或者 cpu 架构为 arm 等。
**Summary 字段**来用简要地描述包的功能。在使用了 Poetry 的项目中，它提取自 description 字段。在 PyPI 上，它将显示在这里：

![](assets/img/chap11/meta_summary.png){width="50%"}

**Description 和 Description-Content-Type 字段**：Description 字段用来详细描述包的一些信息，Description-Content-Type 字段用来指定 Description 字段的内容类型，支持的类型有 Markdown 和 reStructuredText 两种。在使用了 Poetry 的项目中，Poetry 将自动把 README 的内容复制进来。在 PyPI 上，它将显示在下图中的右下侧（方框中）：

![](assets/img/chap11/meta_description.png){width="50%"}

**Classifier 字段：**分类符描述了这个项目的一些分类属性。这些属性会在 PyPI 上显示，并且可以作为筛选条件来进行查找和过滤，请参见下图：

![](assets/img/chap11/meta_classifier.png)

PyPI 的分类系统是一个树形结构。最顶层的分类是框架（Framework），主题（Topic），开发状态（Development Status），操作系统（Operating System）等 10 个大类别。其实，PyPi 上的第三方库可谓浩如烟海，人工查询这些分类意义并不大。这些分类有助于 PyPI 组织和管理所有的库，但并不是强制的，对包的安装也没有帮助。但是，PyPA 仍然推荐在任何项目中，都至少声明该库工作的 Python 版本、license, 操作系统等分类。

此外，新加入的 Typing 分类符比较有意思。它的作用是告诉 PyPI 这个项目是一个类型注解的项目。如果我们的项目是一个类型注解就绪的项目，那么我们应该在项目的源代码目录下加入 py.typed 文件，并在 pyproject.toml 中加入这个分类符：

```toml
classifiers=[
    'Typing :: Typed',
]
```

**Requires-Dist 字段：**这个字段用来描述项目的依赖关系。`pip`在安装时，需要读取这个字段以发现哪些依赖需要安装。
**Requires-Python 字段：**表明这个项目需要的 Python 版本。

遗憾的是，尽管每一个包都包含了这些信息，但是对于一些重要的信息，特别是象 requires-dist 这样的信息，PyPI 并没有将其提取出来单独管理。其它语言的库管理器，比如 maven，在这一点上做得更好。为什么这是一个遗憾，我们将在很快讲到。

## 2. TestPyPI 和 PyPI
在 ppw 生成的项目中，dev 工作流中的 publish 任务会将构建物发布到 TestPyPI。这是一个供测试用的 PyPI。这么做的目的有两个，一来我们希望 CI 总是覆盖到开发全过程，因此构建和发布这两步也不应该缺失。二来，在一个大型应用中，我们可能同时开发着多个相互依赖的项目，此时我们就需要借助 testpypi，使得当某个项目有了更新的版本、但又不到正式发布阶段之前，其他依赖于此的项目也能够使用到这个项目的最新的版本。在这种情况下，我们可以在 pyproject 中添加第二个源，指向 testpypi，这样当我们指定该项目的最新开发版本时，poetry 就会从查找 testpypi。

我们来举例说明如何通过 testpypi 向项目添加一个非正式发布版本。

我们以大富翁量化框架为例。这是一个包含了多个模块的大型应用。其中，zillionare-omicron 是数据读写的 sdk， zillionare-omega 是行情数据服务器，它依赖于 zillionare-omicron，还有许多其他模块。不过要理解我们这里的示例，只需要知道这两个模块就够了。实际上，你可以完全不知道什么是大富翁量化框架，只需要知道几个模块之间的依赖关系就可以了。

假设`zillionare-omicron`当前最新的开发版本是 1.2.3a1。`zillionare-omicron`使用了基于语义的版本管理方案，因此从版本号上我们得知，这不是正式版本，只会发布到 testpypi 上去。如果要在项目中使用这个版本，我们需要先将 testpypi 添加为一个源，然后在`pyproject.toml`中指定`zillionare-omicron`的版本为`1.2.3a1`。这样，当我们执行`poetry install`时，poetry 就会从 testpypi 中查找`zillionare-omicron`的 1.2.3a1 版本，然后安装到本地。

我们在 [第 5 章 poetry 依赖解析的工作原理](chap05.md#poetry 依赖解析的工作原理)那一节介绍过如何增加第二个源。我们这里用同样的方法来增加 testpypi 源：
```bash
$ poetry source add -s testpypi https://test.pypi.org/simple
```
然后我们的 pyproject.toml 文件中将会多这样一项：
```toml
[[tool.poetry.source]]
name = "testpypi"
url = "https://test.pypi.org/simple"
default = false
secondary = true
```
现在我们就可以把对 zillionare-omicron 的开发中版本的依赖加进来：
```shell
$ poetry add -v zillionare-omicron^1.2.3a1
```
命令将成功执行，你可以从更新后的 pyproject.toml 中看到对`zillionare-omicron`的引用。如果我们没有添加这个源，则上述命令在执行时会报出以下错误：
```
Using virtualenv: /home/aaron/miniconda3/envs/sample

  ValueError

  Could not find a matching version of package zillionare-omicron

  at ~/miniconda3/envs/sample/lib/python3.8/site-packages/poetry/console/commands/init.py:414 in _find_best_version_for_package
      410│         )
      411│ 
      412│         if not package:
      413│             # TODO: find similar
    → 414│             raise ValueError(f"Could not find a matching version of package {name}")
      415│ 
      416│         return package.pretty_name, selector.find_recommended_require_version(package)
      417│ 
      418│     def _parse_requirements(self, requirements: list[str]) -> list[dict[str, Any]]:
```

## 3. Pip: Python 包管理工具
你可能感到好奇，`pip`几乎是所有学习 Python 的人最早接触的几个命令之一，也是本书最早使用的那些命令之一，为什么我们却安排到了最后来介绍？原因是，因为大家非常熟悉`pip`了，所以对`pip`的一般性介绍已经不太有必要。值得一提的是，`pip`同样面临着依赖解析的问题，最适合讨论这个问题的地方，则是在了解了构建和分发系统的全貌之后。

依赖解析。这是我们又一次接触到这个词。上一次还是在讲 Poetry 的那一章。是的，Poetry 只解决了开发阶段的依赖问题，并为安装阶段的依赖解析打下了良好基础，但是，`pip`仍然要独自面临依赖解析问题。

下面的示例来自于`pip`的文档：

```shell
$ pip install tea
Collecting tea
  Downloading tea-1.9.8-py2.py3-none-any.whl (346 kB)
     |████████████████████████████████| 346 kB 10.4 MB/s
Collecting spoon==2.27.0
  Downloading spoon-2.27.0-py2.py3-none-any.whl (312 kB)
     |████████████████████████████████| 312 kB 19.2 MB/s
Collecting cup>=1.6.0
  Downloading cup-3.22.0-py2.py3-none-any.whl (397 kB)
     |████████████████████████████████| 397 kB 28.2 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.21.0-py2.py3-none-any.whl (395 kB)
     |████████████████████████████████| 395 kB 27.0 MB/s
  Downloading cup-3.20.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 24.4 MB/s
  Downloading cup-3.19.1-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 21.3 MB/s
  Downloading cup-3.19.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 26.2 MB/s
  Downloading cup-3.18.0-py2.py3-none-any.whl (393 kB)
     |████████████████████████████████| 393 kB 22.1 MB/s
  Downloading cup-3.17.0-py2.py3-none-any.whl (382 kB)
     |████████████████████████████████| 382 kB 23.8 MB/s
  Downloading cup-3.16.0-py2.py3-none-any.whl (376 kB)
     |████████████████████████████████| 376 kB 27.5 MB/s
  Downloading cup-3.15.1-py2.py3-none-any.whl (385 kB)
     |████████████████████████████████| 385 kB 30.4 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.15.0-py2.py3-none-any.whl (378 kB)
     |████████████████████████████████| 378 kB 21.4 MB/s
  Downloading cup-3.14.0-py2.py3-none-any.whl (372 kB)
     |████████████████████████████████| 372 kB 21.1 MB/s
```
要品一口香茗，除了好茶，你还得有热水，茶匙和杯子。在这里，`tea`依赖于`hot-water`, `spoon`和`cup`。当安装`tea`时，`pip`下载了最新的`spoon`和`cup`，发现两者不兼容，于是它不得不向前搜索兼容的版本，这个功能被称之为回溯，是从 20.3 起才有的功能。由于依赖信息不能通过查询 PyPI 得到，所以它不得不一次又一次的下载早前版本的包，从这些包中提取依赖信息，看是否与`spoon`兼容，不断重复这个过程直到找到一个兼容的版本。

这个过程我们在 Poetry 进行依赖解析时也看到过。我们在 [第 5 章 poetry 依赖解析的工作原理](chap05.md#poetry 依赖解析的工作原理）中解释过，PyPI 上并没有某个库的依赖树，所以，Poetry 要知道某个库的依赖项，就必须先把它下载下来。这个说法其实只是部分正确。在读过 [分发包的元数据](chap11.md#分发包的元数据)那一节之后，我们已经知道，这些信息已经上传到了 PyPI，只是由于某些历史原因，PyPI 并没有把它们单独提取出来以供使用而已。

人们花了这么多功夫来解决依赖问题，看来“依赖地狱”一说，并非虚妄。

问题是，既然 Poetry 在添加依赖时，已经进行过了依赖解析，又生成了 lock 文件，为何`pip`不能直接使用些信息，还要重新进行一次依赖解析呢？现在请你打开`sample`工程构建出来的 wheel 文件。我们说过，它是`zip`格式的压缩文件。打开后，其内容如下：
```
.
├── sample
│   ├── __init__.py
│   ├── app.py
│   └── cli.py
└── sample-0.1.0.dist-info
    ├── LICENSE
    ├── METADATA
    ├── RECORD
    ├── WHEEL
    └── entry_points.txt
```

我们在这里找不到任何跟 poetry 有关的东西。这并不奇怪，毕竟，poetry 与 pip 不属于同一个开发者，而 poetry 还不是标准库的一部分，所以 pip 没有理由去解析任何 poetry 直接相关的东西。所有的依赖信息都在 METADATA 这个文件里，特别是 Requires-Dist:

```
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
Requires-Dist: fire (==0.4.0)
Requires-Dist: flake8 (==4.0.1) ; extra == "test"
Requires-Dist: flake8-docstrings (>=1.6.0,<2.0.0) ; extra == "test"
Requires-Dist: isort (==5.10.1) ; extra == "test"
```
我们看到，有一些依赖指定了精确的版本，有的则只指定了版本范围，这里使用的是不等式语法（请见 [Poetry 进行依赖管理的相关命令](chap05.md#Poetry 进行依赖管理的相关命令）)。所以，尽管 Poetry 通过 lock 文件锁定了精确的版本，但 lock 文件只会在开发者之间共享，以加快他们的开发环境构建速度，而不会发布给终端用户。发布给终端用户的依赖信息，是 Poetry 按照 pyproject.toml 文件的内容生成的，两者语义完全一致，只不过 Poetry 允许开发者使用包括通配符、插字符、波浪符、不等式等多种语法来指定版本号，而在生成 METADATA 时，都被转换成不等式语法而已。我们再来回忆一下 sample 项目中的 pyproject.toml 文件的相关部分：
```
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
```

Poetry 为何不将`lock`文件中锁定的版本号写入到 METADATA 文件中呢？这是因为，lock 文件完全锁死了依赖的版本号，这样虽然安装速度变快，但也会导致任何更新，就连安全更新也不可用。

现在我们明白了，在 Poetry 向项目中增加一个依赖时，如果发生了回溯，那么极有可能在`pip`安装时也发生同样的回溯。要加快`pip`安装的速度，我们应该查看`poetry.lock`文件，找出其锁定的版本，以它为基点，重新指定一个恰当的版本范围，这样可以极大程度上避免在`pip`安装时发生回溯。

一个好消息是，根据`pip`的文档，致力于不下载 Python package 就能得到其依赖信息的方案正在工作当中。让我们期待它的到来吧。
# 2. 应用程序分发
应用程序的打包分发，按它最终分发的目标，又可大致分为桌面应用程序和移动应用程序 [^1]。前者一般只需要借助一些打包工具；后者往往要在一开始，就要从框架入手进行支持。
## 4. 桌面应用程序
Python 打包桌面应用程序的选项非常之多，包括跨平台的如 pyInstaller[^3], Nuitka[^8]，briefcase[^5]，专用于 Windows 的 py2exe[^6] 和专用于 Mac 的 py2app[^7] 等。此外，还有 cx_Freeze[^4]，makeself[^2] 等。这里我们将介绍 makeself, PyInstaller，Nuikta。

在介绍这些工具之前，我们先讨论下，打包分发一个桌面应用程序意味着什么？当我们分发一个 Python 库时，我们的用户是程序员，他们应该掌握诸如创建虚拟环境、安装依赖等基本的 Python 知识。而当我们分发一个桌面应用程序时，我们的用户常常是普通用户，他们很可能不具备这些知识，甚至可能都不知道如何运行一个 Python 程序。因此，我们还需要帮他们创建程序运行的入口（比如，将程序入口放到启动菜单、桌面快捷方式等）。此外，在安装时，可能还需要询问用户安装目录、显示并接受许可协议等。这些都是打包分发桌面应用程序的基本要求。

不是所有我们将介绍的工具，都同样具有上述能力，请读者注意辨别，根据需要做出选择。
### 4.1. makeself 的多平台安装包（内含案例）

Makeself[^2] 是一个可用以 Unix/Linux 和 MacOs 下的自解压工具。如果用户使用 Windows，则在安装了 cygwin 的前提下，也可使用（不过这样一来，基本上就将普通用户排除在外了，所以并不是好的方案）。Makeself 本身是一个小型 shell 脚本，可从指定目录生成可自解压的压缩文档。生成的文件显示为 shell 脚本，并且可以在 shell 下启动执行。执行时，这个压缩文档将自行解压缩到一个临时目录，然后执行事先指定好的命令（例如安装脚本）。这与在 Windows 世界中使用 WinZip Self-Extractor 生成的档案非常相似。Makeself 档案还包括用于完整性自我验证的校验和（CRC 和/或 MD5/SHA256 校验和）。

我们介绍这个工具，是因为在运维领域它应用非常广泛，在 Github 上也有过千 stars。另外，对于 Python 开发者来说，这个概念很可能并不陌生。如果你在 Linux 下安装过 Anaconda，你可能知道，Anaconda 的安装包就是一个类似于 shell 脚本的压缩包，不确定的是，它是用 makeself 打包的，还是用其它工具打包的。

Makeself 的使用方法也非常简单，几乎没有学习成本。在 Ubuntu 下，它可以通过以下命令安装：
```shell
$ sudo apt-get install makeself
```
在其它操作系统上，您可能需要从其官网 [^2] 下载安装。也可以通过`conda`命令来安装：
```shell
$ conda install -c conda-forge makeself
```

它的用法如下：

```shell
$ makeself.sh [args] archive_dir file_name label startup_script [script_args]
```

args 是 Makeself 自己在打包时要使用的参数。参数比较多，涵盖了如何压缩、是否加密、解压缩行为等，这里就不一一详述。请读者在需要时参考官方文档 [^2]。

在准备阶段，我们通常把要打包安装的文件都放在一个目录下。archive_dir 就是这个目录的名字，比如项目下的 dist 文件夹；file_name 是最终制作出的安装文件名，比如 install_sample.sh；label 则是对安装文件的描述，比如“Install sample”; startup_script 是安装文件解压后要执行的脚本，比如 install.sh；script_args 是 startup_script 的参数。

仍以`sample`项目为例，我们可以使用以下脚本来完成打包：
```shell
#!/BIN/BASH
  
poetry build
rm -rf /tmp/sample
mkdir /tmp/sample

version=`poetry version | awk '{print $2}'`

echo "version is $version"
# PREPARE ARCHIVE
cp dist/sample-$version-py3-none-any.whl /tmp/sample/

# PREPARE INSTALL SCRIPT
echo "#! /bin/bash" > /tmp/sample/install.sh
echo "pip install ./sample-$version-py3-none-any.whl" >> /tmp/sample/install.sh
chmod +x /tmp/sample/install.sh

# PACKAGING WITH MAKESELF
makeself /tmp/sample install_sample.sh "sample package made by makeself" ./install.sh
```
非常轻巧和干净，这正是我们介绍它的原因。我们这里使用了一个名为 install.sh 的脚本作为启动脚本。在这个脚本里，我们仅仅演示了如何执行安装命令，一个安整的安装脚本可能需要：
1. 检查符合版本要求的 Python 是否可用，如果不可用，下载并安装。这里也可以询问用户意见，如果用户不接受，则退出安装。
2. 安装 virtualenv，如果 virtualenv 在当前环境下不存在的话，还要通过 pip install virtualenv 安装。
3. 通过`virtualenv --no-site-packages venv path/to/your/app`创建一个新的虚拟环境，我们的应用程序应该在此虚拟环境下运行。虚拟环境的路径也将是我们的安装路径，这需要向用户询问并接收输入。这里的参数`--no-site-packages`的作用是不将系统环境中的包拷贝过来，这样我们可以得到一个干净的虚拟环境。
4. 将解压后的应用程序拷贝`path/to/your/app`中。
5. 切换目录到`path/to/your/app`下，激活虚拟环境：`source venv/bin/activate`
6. 安装应用程序：`pip install ./sample-$version-py3-none-any.whl`。安装完成后，这个 whl 文件也可以删除。
7. 创建一个启动脚本（假设名字为 start.sh），这个启动脚本的作用是通过虚拟环境中的 python 来调用我们的应用程序`sample`。如果`sample`程序提供了`console script`，那么启动脚本的任务就是直接调用它；否则，就要看`sample`的入口程序是如何提供的了。这部分只能交给读者自行完成了。
8. 创建一个软链接，将启动脚本链接到`/usr/local/bin`下，这样就可以在任何地方通过`sample`命令来启动我们的应用程序了。创建软链接的命令是：
```shell
$ sudo ln -s path/to/your/app/start.sh /usr/local/bin/sample
```

### 4.2. PyInstaller 和 Nuitka
这两者都是打包工具。其目标都是将 Python 程序打包成一个自包含的可执行文件（也可能是文件夹）。这样，我们就可以将其分发给客户，无论客户的目标机器上是否安装有 Python，都可以直接运行，并且所有的依赖都已经包含了。除了上述功能外，两个工具都还有加密 Python 程序的能力，这也是不少开发者所需要的功能。

不同的是，PyInstaller 只对 Python 程序进行打包，即从指定的 python 文件开始，递归分析它的依赖项，将这些依赖项和适配的 Python 解释器一并打包。在这个过程中，它可以按要求对生成的字节码进行一定的混淆，从而起到加密的作用。最终应用程序的运行方式跟普通的 Python 程序一样，通过解释器来执行。

Nuitka 则会先将 Python 程序翻译成 C 代码，然后再编译成可执行文件。这样，生成的可执行文件就不依赖于 Python 解释器了。这样做的好处是，生成的可执行文件更小，理论上运行速度应该比肩 c 程序。不过 Python 程序转换为 c 时可能会遇到一部分兼容性问题，在这种情况下，Nuitka 会优先考虑兼容性问题，而不是优化速度，因此一般认为加速在 30%以内。使用 Nuitka 打包的另一个好处是，由于我们发布的是二进制文件，所以能比较好地保护源代码。

看上去 Nuitka 似乎更有发展前景，毕竟，它有性能加成的因素。随着使用 Type hint 的 Python 库越来越多，这种性能加成将会越来越明显。因此，这里我们只对 Nuitka 进行简单介绍。如果读者对 PyInstaller 感兴趣，可以按照我们文中给出的官网链接，自行学习。

下面，我们以一个简单的例子来说明如何使用 Nuitka 打包 Python 程序。尽管我们所有的示例都推荐在 Ubunutu 或者 MacOS 上运行，但这一次，我们需要在 windows 上运行这个示例。

首先，我们要安装 nuitka，可以通过 pip 安装（注意我们需要创建一个虚拟环境，在其中安装 nuitka）：

```shell
$ pip install nuitka
```

然后，我们创建一个名为`greetings.py`的文件，内容如下：

```python title="greetings.py"
import fire

def greeting(name: str):
    print(f"hi {name}")

fire.Fire({
    "greeting": greeting
})
```

接下来就是见证奇迹的时刻，我们这样进行打包：
```
python -m nuitka greetings.py
```
这会在给出以下警示后，程序继续：
```
Nuitka-Options:INFO: Used command line options: greetings.py
Nuitka-Options:WARNING: You did not specify to follow or include anything but main program. Check options and make sure
Nuitka-Options:WARNING: that is intended.
Nuitka:WARNING: Using very slow fallback for ordered sets, please install 'orderedset' PyPI package for best Python
Nuitka:WARNING: compile time performance.
```

Nuitka 在编译中给出了一些性能相关的警告。对我们这个简单的程序，这些警告不会有任何影响。比如，其中的一条是，如果你的程序中使用了`set`，那么你应该安装`orderedset`，这样可以提高运行速度。我们的示例程序是如此简单，以致于即使我们按提示安装了 orderedset，也不会得到性能上的提升。因此，我们可以完全忽略这些警告。

接下来，它要求下载并安装 MinGW64 和 ccache。这个下载可能会失败，如果是这样，你需要自行下载，并且将下载的压缩包解压缩后，按提示放到指定的位置，比如'C:\Users\Administrator\AppData\Local\Nuitka\Nuitka\Cache\downloads\gcc\x86_64\11.3.0-14.0.3-10.0.0-msvcrt-r3'。这个位置可能会因为你的系统不同而不同，但都会打印在命令行窗口中。

接下来，它开始进行编译：
```
Nuitka:INFO: Starting Python compilation with Nuitka '1.4.3' on Python '3.8' commercial grade 'not installed'.
Nuitka:INFO: Completed Python level compilation and optimization.
Nuitka:INFO: Generating source code for C backend compiler.
Nuitka:INFO: Running data composer tool for optimal constant value handling.
Nuitka:INFO: Running C compilation via Scons.
Nuitka-Scons:INFO: Backend C compiler: gcc (gcc).
Nuitka-Scons:INFO: Backend linking program with 6 files (no progress information available).
Nuitka-Scons:INFO: Compiled 24 C files using ccache.
Nuitka-Scons:INFO: Cached C files (using ccache) with result 'cache miss': 6
Nuitka:INFO: Keeping build directory 'greetings.build'.
Nuitka:INFO: Successfully created 'greetings.exe'.
Nuitka:INFO: Execute it by launching 'greetings.cmd', the batch file needs to set environment.
```
根据提示，我们看到它将 python 代码转换成 c 的源码，并进一步编译成 windows 上可以运行的原生程序。最终，我们得到了两个文件，一个是'greetings.exe'，另一个是'greetings.cmd'。如果我们是在刚刚进行打包的窗口中，则可以直接运行`greetings.exe`，否则，我们应该运行`greetings.cmd`。

运行结果如下：
```shell
$ greetings.exe greeting aaron

hi aaron
```
这仅仅是一个命令行程序，所以看上去可能不那么令人兴奋。如果我们打算从资源管理器里找到它，双击并运行它，我们会被提示缺少某些 python 的 dll。为了使这个程序能完全独立运行，我们需要在打包时加上--standalone 参数：
```shell
$ python -m nuitka --standalone --follow-imports greetings.py
```

这一次，又会提示下载一些东西，主要是 msvc 的运行时，但这次下载会非常顺利。最终，编译成功，我们得到了一个名为 greetings.dist 的文件夹。现在，如果 greetings 是一个带图形界面的应用，我们就可以在资源管理器中，直接双击其中的 greetings.exe 运行了。不过，由于我们的 greetings 程序需要接收用户输入，所以我们还是得从命令行中打开它。但这次，我们可以将新生成的文件夹拷贝到没有安装 python 和 nuitka 的机器上，然后在命令行下运行 greetings.exe：

```shell
$ greetings.exe greeting aaron

hi aaron
```

Nuitka 的打包构建过程已经可以和 poetry 整合，我们只需要这样修改`pyproject.toml`即可工作：
```toml
[build-system]
requires = ["setuptools>=42", "wheel", "nuitka", "toml"]
build-backend = "nuitka.distutils.Build"

[nuitka]
# THESE ARE NOT RECOMMENDED, BUT THEY MAKE IT OBVIOUS TO HAVE EFFECT.

# BOOLEAN OPTION, E.G. IF YOU CARED FOR C COMPILATION COMMANDS, LEADING
# DASHES ARE OMITTED
show-scons = true

# OPTIONS WITH SINGLE VALUES, E.G. ENABLE A PLUGIN OF NUITKA
enable-plugin = pyside2

# OPTIONS WITH SEVERAL VALUES, E.G. AVOIDING INCLUDING MODULES, ACCEPTS
# LIST ARGUMENT.
nofollow-import-to = ["*.tests", "*.distutils"]
```

现在，我们来思考一下，PyInstaller 和 Nuitka 的定位。它们都是打包程序，显然。但他们并不是安装程序。通过它们打包，我们实现的目标是让这些程序可以在用户的桌面操作系统上，在不安装 Python 和依赖的情况下，就可以直接运行，但是，它只适合无须安装的“绿色程序”，如果我们的程序需要创建桌面快捷方式，修改注册表，那么它将无能为力。

如果您的程序需要有一个较华丽的安装界面，建议您查看一下 Inno Setup[^4] 或者 Wix[^9]。
## 5. 移动应用程序
移动应用程序与桌面应用有很大的不同，一般来说，即使我们能把一个桌面应用打包成能安装的移动应用，其用户体验也很难说会有多好。因此，对于 Python 应用程序的打包和分发，必须从一开始就进行规划，必须一开始就使用上相关的跨平台开发的框架。

这里我们主要介绍和比较两个最流行的框架，`Kivy`和`BeeWare`，读者可以根据自己的需要进行选择。

### 5.1. Kivy
Kivy[^10] 是一个跨平台的 Python 框架，它可以让我们使用 Python 来开发桌面应用程序和移动应用程序。它基于 MIT License，完全免费。它的主要特点是，有自己的 UI 设计语言，因此在所有的设备上，应用程序都有一致的行为和外观；它使用 OpenGL 来绘制 UI，因此十分高效。 下图是使用 Kivy 开发的一个围棋游戏，名为 Lazy Baduk，你可以在谷歌应用商店中找到它。

![](assets/img/chap11/kivy_go.png){width="50%"}

!!! Info
    如果你对围棋感兴趣，这里推荐一个名为 KaTrain 的围棋训练软件，它也是用 Python 和 Kivy 开发的。它基于 KataGo -- 最强算力的开源围棋 AI，一些谣传认为，某些商业软件，包括某些国家队用以训练的 AI 围棋软件，都“借鉴”了 KataGo 的算法。

Kivy 的短板可能也在于它的独特的 UI 设计语言。Kivy 的 UI toolkit 保证了基于 Kivy 的应用程序可以很好在运行在 Android, iOS, Linux 甚至 Raspberry Pi 上，但是也使得它缺少了原生应用程序的某些操作能力。
### 5.2. BeeWare
BeeWare[^11] 同样是一个跨平台的 Python 框架。它基于 BSD License，完全免费。它的主要特点是，它致力于提供接近原生程序的用户体验。BeeWare 的出现时间要晚一些，不过它的发展势头也不差。另外，它是组件式的，BeeWare 包含了 BriefCase，这是另一个为人广泛使用的 Python 打包工具。Toga，一个基于 Python 的跨平台 GUI 框架，也是 BeeWare 的一部分。

移动端的差异远大于桌面端。能利用移动设备的最新特性，对打造一款吸引人的移动应用是十分重要的。但无论是 BeeWare 还是 Kivy，都只能针对多数移动设备共同具有的特性进行抽象化。出于这个考虑，也许 Python 目前仍不是最适合的开发语言。但是，不管是 Kivy，还是 BeeWare，都为 Python 开发移动应用提供了一种选择。
## 6. 基于云的应用部署
比起桌面应用程序，Python 似乎更擅长开发后台服务程序。在微服务架构下，多进程+异步 IO，使得 Python 无法充分利用硬件性能的短板被补齐，而它简洁、高效和丰富的生态的优势则得到了充分的发挥。

Python 的云部署有 Heroku, GoogleApp 等方式。但更广泛使用的方式可能是基于云的容器化部署。容器是一种轻量化的虚拟机，它与虚拟机不同的是，它不需要一个完整的操作系统，而是直接使用宿主机的内核。这样，容器的启动速度比虚拟机快很多，而且它们的资源占用也更少。一般地，我们使用容器来运行某个服务，当该服务停止时，容器也就终结了。

Docker 是目前最流行的容器化部署工具。构建基于容器的服务，一般分为两个步骤：构建镜像和运行容器。镜像是通常由一个操作系统内核，一个 Python 解释器，以及我们的 Python 服务组成。这些组件可以通过 Dockerfile 来描述。Dockerfile 是一个文本文件，它包含了一系列命令和参数，用以构建一个镜像。镜像是一个只读的模板，它描述了一个 Docker 容器应该如何运行。当镜像被 Docker 运行时拉取到本地并执行时，就会生成一个容器，并且服务就在容器中运行。

下面我们通过一个例子来说明如何构建和运行一个 Python 服务的容器。示例的源代码在 code/chap11/docker 目录下。我们仍然是通过`ppw`来创建一个名为 sample 的项目。与以往不同的是，我们将在项目根目录下创建一个名为`docker`（名字可任意）的目录，其中包含以下文件：
```
.
├── build.sh
├── dockerfile
└── rootfs
    └── root
        ├── entrypoint.sh
        └── sample
            ├── index.html
            └── mars.jpg
```
所有跟构建镜像相关的文件都放在这个目录下。

其中，build.sh 是一个脚本，用于构建镜像。dockerfile 用于描述镜像。rootfs 是一个目录，用于存放我们需要带到镜像中的文件。在构建镜像时，它将被映射为容器的根目录。

build.sh 主要的工作是构建 sample 项目，将相应的文件拷贝到 rootfs 下，再执行`docker build`命令来构建镜像。

以下是 build.sh 的主要内容：
```shell
version=`poetry version | awk '{print $2}'`
wheel="/root/sample/sample-$version-py3-none-any.whl"

poetry build

# 将 WHEEL 包拷贝到 ROOTFS 目录下以便构建镜像时进行安装。我们也可以将 WHEEL 包上传到 PYPI，然后在
# DOCKERFILE 中通过 PIP INSTALL SAMPLE 安装。
cp ../dist/*$version*.whl rootfs/root/sample/

# 移除上一次编译生成的镜像，重新构建。这将生成一个名为 SAMPLE 的镜像。
# 注意我们在构建过程中通过--BUILD-ARG 传入编译期变量给镜像
docker rmi sample
docker build --build-arg version=$version --build-arg wheel=$wheel . -t sample

# 启动服务
docker run -d --name sample -p 7878:7878 sample
```
在这个构建脚本里，我们首先构建了 sample 项目的 wheel 包，然后将它拷贝到 rootfs 目录下。接着，我们执行`docker build`命令，构建了一个名为 sample 的镜像，最后，我们以此镜像为基础，启动了一个名为 sample 的容器，并且将端口 7878 映射为主机端口。

Dockerfile 是这一节的核心，现在，我们来看看 Dockerfile 的内容：
```Dockerfile
FROM python:3.8-alpine3.17

WORKDIR /
COPY rootfs ./

ARG version
ARG pypi=https://pypi.tuna.tsinghua.edu.cn/simple
ARG wheel
ENV PORT=7878

RUN pip config set global.index-url ${pypi} \
    && pip install ${wheel}

EXPOSE $PORT
ENTRYPOINT ["/root/entrypoint.sh"]
```
构建任何镜像时，我们都是从一个基础的镜像开始。这个基础镜像可以是像 Linux Alpine 或者 Ubuntu 这样的操作系统镜像，也可以是构建在操作系统之上的应用镜像，比如示例中的 python:3.8-alphine3.17 就是一个构建在 Alpine 操作系统之上的 Python 应用镜像。镜像的标识符一般是"开发者/镜像名：版本"的形式。这里冒号之后的字符串是标签，一般是其版本号，如果不指定版本，那么默认是 latest。如果没有指定开发者，意味着这是一个来自于官方的镜像，或者是我们自己构建的本地镜像。

镜像的分发是一个二级架构。如果在本地不存在 python:3.8-alpine3.17 这个镜像，docker 就会去 Docker Hub[^12] 上查找。Docker Hub，类似于 PyPI，是一个公共的镜像仓库，它提供了大量的镜像供我们使用。现在，我们来看看 Docker Hub 上的 python:3.8-alpine3.17 这个镜像，它究竟是什么。在 Docker Hub 上，我们要通过镜像名（即不带版本标签）来搜索。这样我们得到如下结果：

![](assets/img/chap11/docker_hub_python.png){width="50%"}

这个镜像被下载超过 10 亿次。这不仅说明 Python 的使用有多么广泛，也说明了 Python 在后台服务开发上有多重要。

点击上图中的链接，我们可以进入详情页，找到 3.8-alpine3.17 这个标签，点击进去，我们会跳转到 Github 上，查看其 Dockerfile 的内容：

![](assets/img/chap11/python3.8_alpine_dockerfile.png){width="50%"}

Alpine 是一个轻量级的 Linux 发行版，基于 Alpine 构建的镜像，其大小只有 5M 左右，因此常常是构建微服务的首选。我们的镜像，最终也是使用的这个操作系统内核。

然后我们指定当前的工作目录为根目录，并将 rootfs 目录下的文件拷贝到容器的根目录下。接着，它安装了 sample 项目的 wheel 包。最后，它设置了容器的入口点为/root/entrypoint.sh。

我们用`ARG`来传递 docker 编译期变量。这里的 version 和 wheel 是两个编译器变量，它们是由 build.sh 通过`--arg $version`传递进来的。`EXPOSE`命令是将端口暴露出来。我们在`entrypoint.sh`中启动了一个监听在$PORT 上的 HTTP 服务，我们必须把这个端口暴露给主机，以便我们可以从主机上访问这里的服务。

接下来，我们来看看`entrypoint.sh`的内容：
```
#!/BIN/SH

python3 -m http.server -d /root/sample $PORT
```

由于这只是个演示性的程序，我们在这里就没有用到 sample 的任何功能，而是简单地通过 python 内置`http`模块来启动了一个 web 服务。您只需要知道，如果您想使用 sample 的功能，您可以在这里调用它的命令即可。这与我们在别的地方调用它没有任何不同。

当我们在本地测试通过后，就可以在 Docker Hub 上注册账号，将我们的镜像发布上去，供其它人下载，这样就完成了基于容器的应用发布。当然，我们也可以建立一个私有云的镜像仓库，将镜像发布到私有云上，供内部部署使用。

在这个示例中，最终我们构建的镜像文件只有 66MB 左右。实际上，由于 docker 文件系统的分层设计，如果其他人从 Docker Hub 上下载我们的镜像，他们实际上要下载的数据量会更小。

这就是构建基于容器的服务的全部过程，是不是出人意料地简单和可靠？在本书中，我们用了非常多的篇幅来讲如何进行隔离，这里提供了又一种方式，它甚至比之前所有的方式都更加简单和可靠。运行在容器中的服务，独占了文件系统和计算资源，无论是与宿主机、还是与运行在同一宿主机上的其它容器都互不干扰。而且，我们可以无限次地从同一镜像，生成相同的容器。可复现的部署终于得到完美的实现。

现在，让我们运行示例中的 build.sh。它将为我们构建镜像，并启动该镜像的一个容器。

我们在 build.sh 中，指定了容器的端口为 7878。现在，容器已经启动，服务也正在运行，让我们访问它吧。我们在浏览器地址栏中输入 http://ip-to-host:7878/（需要将 ip-to-host 替换为你实际部署运行示例容器的机器 ip），我们将看到以下界面：

![](assets/img/chap11/end.png){width="80%"}

我们在第一章里看到过这张图。

就让我们从这里开始，也在这里结束。现在，是你开始自己的火星探索之旅的时刻了。

[^1]: 在 [Python 官方文档](https://packaging.python.org/en/latest/overview/#packaging-python-applications)(https://packaging.python.org/en/latest/overview/#packaging-python-applications) 中，还提到了其它几种打包。
[^2]: [Makeself](https://makeself.io/) 的官网地址是：https://makeself.io/
[^3]: [PyInstaller](https://pyinstaller.org) 的官网是：https://pyinstaller.org
[^4]: [Inno Setup](https://jrsoftware.org/isinfo.php) 的官网是：https://jrsoftware.org/isinfo.php
[^5]: [Briefcase](https://briefcase.readthedocs.io/) 的官网是：https://briefcase.readthedocs.io/
[^6]: [Py2exe](https://www.py2exe.org/) 的官网地址是：https://www.py2exe.org/
[^7]: [Py2app](https://py2app.readthedocs.io/en/latest/) 的官网地址是：https://py2app.readthedocs.io/
[^8]: [Nuitka](https://nuitka.net/) 的官网地址是：https://nuitka.net/
[^9]: [WiX](https://wixtoolset.org/) 的官网地址是：https://wixtoolset.org/
[^10]: [Kivy](https://kivy.org) 的官网地址是：https://kivy.org
[^11]: [BeeWare](https://beeware.org/) 的官网地址是：https://beeware.org/
[^12]: [Docker Hub](https://hub.docker.com) 的官网地址是：https://hub.docker.com
