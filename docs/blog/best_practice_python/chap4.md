从这一章开始，我们逐一介绍在第三章里引入的那些工具和技术。

# Poetry
  
![](http://images.jieyu.ai/images/202104/1-BUUIee-t1I2eqTm0RtDNHQ.jpeg)

[Poetry]是一个Python项目的依赖管理和打包工具。Poetry的作者解释开发Poetry的初衷时说：

???+ Quote
    Packaging systems and dependency management in Python are rather convoluted and hard to understand for newcomers. Even for seasoned developers it might be cumbersome at times to create all files needed in a Python project: setup.py, requirements.txt, setup.cfg, MANIFEST.in and the newly added Pipfile. So I wanted a tool that would limit everything to a single configuration file to do: dependency management, packaging and publishing.

我们在上一章中已经看到，在Poetry出现之前，打包一个Python程序库，需要有setup.py, setup.cfg, MANIFEST.in, requirements.txt等文件。在那一章里，我们没有详细介绍这些文件的作用和配置。实际上这些文件的管理是十分混乱的。

需求依赖散布于requirements.txt和setup.py之中；当您将依赖加入到工程时，无法确定它是否与既存的依赖能够和平共处；所以一般的做法是，先将它们加进来，完成开发和测试，在打包之前，运行``pip freeze > requirements.txt``来锁定依赖库的版本。但这也将一些你的工程中并不直接依赖的包加入进来--你可能甚至并不清楚它是做什么的。

项目的版本管理也是一个问题。一般我们使用bumpversion来管理版本，它需要使用三个文件。在我的日常使用时，它常常会因为单双引号的问题，导致把``__version__=0.1``当成一个版本号，而不是``0.1``。这样打出来的包名也会奇怪地多一个无意义的version字样。单双引号则是因为你的format工具对字符串常量应该使用什么样的引号规则有自己的意见。

Poetry解决了所有这些问题。它提供了版本管理、虚拟运行环境、依赖解析、构建和发布的一站式服务，并将所有的配置，集中到一个文件中，即pyproject.toml。此外，Poetry还提供了一个简单的工程向导。不过这个向导的功能比较简单，我们推荐使用上一章介绍的cookiecutter-pyproject。

??? Readmore
    实际上Poetry还会用到另一个文件，即poetry.lock。这个文件并非独立文件，而是Poetry根据pyproject.toml生成的。

## 版本管理
假设您已经使用[cookiecutter-pyproject]来生成了一个工程框架，那么应该可以在根目录下找到pyproject.toml文件，其中有一项：

```
version = 0.1
```
如果您现在运行``poetry version``这个命令，就会显示``0.1``这个版本号。

Poetry使用[semantic version]表示法。 Semantic version由Tom Preston-Werner提出，他是Github的共同创始人。Semantic version表示法提出初衷是：

???+ Quote
    在软件管理的领域里存在着被称作“依赖地狱”的死亡之谷，系统规模越大，加入的包越多，你就越有可能在未来的某一天发现自己已深陷绝望之中。

    在依赖高的系统中发布新版本包可能很快会成为噩梦。如果依赖关系过高，可能面临版本控制被锁死的风险（必须对每一个依赖包改版才能完成某次升级）。而如果依赖关系过于松散，又将无法避免版本的混乱（假设兼容于未来的多个版本已超出了合理数量）。当你专案的进展因为版本依赖被锁死或版本混乱变得不够简便和可靠，就意味着你正处于依赖地狱之中。

Sematic version提议用一组简单的规则及条件来约束版本号的配置和增长。首先，你规划好公共 API，在后面的新版本发布中，透过修改相应的版本号来向大家说明你的修改。考虑使用这样的版本号格式：X.Y.Z （主版本号.次版本号.修订号）：修复问题但不影响API 时，递增修订号；API 保持向下兼容的新增及修改时，递增次版本号；进行不向下兼容的修改时，递增主版本号。

在Poetry中，你通过``poetry version semver``来修改版本。``semver``可以是``patch``, ``minor``, ``major``, ``prepatch``, ``preminor``, ``premajor``和 ``prerelease``。

``semver``结合您当前的版本号，通过运算，就得出了新的版本号：

| rule       | before        | after         |
| ---------- | ------------- | ------------- |
| major      | 1.3.0         | 2.0.0         |
| minor      | 2.1.4         | 2.2.0         |
| patch      | 4.1.1         | 4.1.2         |
| premajor   | 1.0.2         | 2.0.0-alpha.0 |
| preminor   | 1.0.2         | 1.1.0-alpha.0 |
| prepatch   | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.3-alpha.0 | 1.0.3-alpha.1 |
| prerelease | 1.0.3-beta.0  | 1.0.3-beta.1  |

[Poetry]: https://python-poetry.org/
[cookiecutter-pyproject]: https://zillionare.github.io/cookiecutter-pypackage/

## 依赖管理

在Poetry管理的工程中，当我们向工程中加入依赖时，总是使用``poetry add``命令，比如：``poetry add cfg4py``

这里可以指定，也可以不指定版本号。命令在执行时，会对``cfg4py``所依赖的库进行解析，直到找到合适的版本为止。如果您指定了版本号，该版本与工程里已有的其它库不兼容的话，命令失败。

我们在添加依赖时，一般要指定较为准确的版本号，界定上下界，从而避免意外升级带来的各种风险。在指定依赖库的版本范围时，有以下各种语法：
```
poetry add SQLAlchemy=*             # 使用最新版本
poetry add SQLAlchemy               # 使用最新的版本
poetry add SQLAlchemy=1.*           # 使用>1.0, <2.0的版本
poetry add SQLAlchemy@^1.2.3       # 使用>=1.2.3, <2.0的版本
poetry add SQLAlchemy@>=1.2,<1.4    # 使用>=1.2,<1.4的版本
poetry add SQLAlchemy~1.2           # 使用>=1.2.0,<1.3的版本
poetry add SQLAlchemy~1.2.3         # 使用>=1.2.3，<1.3的版本
poetry add SQLAlchemy==1.2.3        # 使用1.2.3版本
```
从上到下，指定的上下界越来越具体清晰。

如果有可能，我们推荐总是使用最后一行的语法。这不仅会加快依赖解析和安装速度，也会解决很多依赖升级带来的意外问题。比如，如果使用了上面第4行的语法，你已经发行出去的安装包，会在SQLAlchemy 1.4版本推出前可用，而在之后变得不可用：这当中你既没有更改代码，也没有发行新的安装包。这个情况当时很多Python程序库都有报告。比如广泛使用的异步ORM框架Gino就出现了这一问题。

原因在于，``poetry add SQLAlchemy@^1.2.3``这一句没有锁定SQLAlchemy的上界，因此，你默许了可以安装直到2.0以前的所有版本。而pip在安装时，总是会自动寻找符合条件的最新包，于是1.4这个跟之前版本不兼容的版本就被安装上了，导致你的程序崩溃。

这也看出来SQLAlchemy的发行并不完全符合Semantic的标准。一旦出现API不兼容的情况，是需要对主版本升级的。如果SQLAlchemy不是将版本升级到1.4，则是升级到2.0，则不会导致程序出现问题。

始终遵循社区规范进行开发，这是每一个开源程序开发者都应该重视的问题。

在向工程中增加依赖时，如果我们直接指定了具体的版本，有可能因为依赖冲突的原因，无法直接指定成功。此时可以指定一个较宽泛一点的版本范围，待解析成功和测试通过后，再改为固定版本。

在上一章里，我们已经提到了依赖分组。最新的Python规范允许你的程序使用发布依赖和extra requirements。在上一章向导创建的工程中，我们把extra reuqirement分为了三个组，即dev, test, doc。

```

[tool.poetry.dependencies]
python = ">=3.6.1,<4.0"

black  = { version = "20.8b1", optional = true}
isort  = { version = "5.6.4", optional = true}
flake8  = { version = "3.8.4", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
pytest  = { version = "6.1.2", optional = true}
pytest-cov  = { version = "2.10.1", optional = true}
tox  = { version = "^3.20.1", optional = true}
virtualenv  = { version = "^20.2.2", optional = true}
pip  = { version = "^20.3.1", optional = true}
mkdocs  = { version = "^1.1.2", optional = true}
mkdocs-include-markdown-plugin  = { version = "^1.0.0", optional = true}
mkdocs-material  = { version = "^6.1.7", optional = true}
mkdocstrings  = { version = "^0.13.6", optional = true}
mkdocs-material-extensions  = { version = "^1.0.1", optional = true}
twine  = { version = "^3.3.0", optional = true}
mkdocs-autorefs = {version = "0.1.1", optional = true}
pre-commit = {version = "^2.12.0", optional = true}
toml = {version = "^0.10.2", optional = true}

[tool.poetry.extras]
test = [
    "pytest",
    "black",
    "isort",
    "flake8",
    "flake8-docstrings",
    "pytest-cov"，
    "twine"
    ]

dev = ["tox", "pre-commit", "virtualenv", "pip",  "toml"]

doc = [
    "mkdocs",
    "mkdocs-include-markdown-plugin",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-material-extension",
    "mkdocs-autorefs"
    ]
```
这里tox， pre-commit等是我们开发过程中使用的工具；pytest等是测试时需要的依赖；而doc则是构建文档时需要的工具。通过这样划分，可以使CI或者文档托管平台只安装必要的依赖；同时也容易让开发者分清每个依赖的具体作用。

## 虚拟运行时

Poetry自己管理着虚拟运行时环境。当你执行``poetry install``命令时，Poetry就会安装一个基于venv的虚拟环境，然后把项目依赖都安装到这个虚拟的运行环境中去。此后，当你通过poetry来执行其它命令时，比如``poetry pytest``，也会在这个虚拟环境中执行。反之，如果你直接执行``pytest``，则会报告一些模块无法导入，因为你的工程依赖并没有安装在当前的环境下。

我们推荐在开发过程中，使用conda来创建集中式管理的运行时。在调试Python程序时，都要事先给IDE指定解析器，这里使用集中式管理的运行时，可能更方便一点。Poetry也允许这种做法。当Poetry检测到当前是运行在虚拟运行时环境下时，它是不会创建新的虚拟环境的。

但是Poetry的创建虚拟环境的功能也是有用的，主要是在测试时，通过virtualenv/venv创建虚拟环境速度非常快。

## 打包和发布

我们通过运行``poetry build``来打包，打包的文件约定俗成地放在dist目录下。

发布前，我们需要对poetry进行一些配置，主要是repo和token。

```
# publish to test pypi
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config testpypi-token.pypi my-token
poetry publish -r testpypi

# publish to pypi
poetry config pypi-token.pypi my-token
poetry publish
```
上面的命令分别对发布到testpypi和pypi进行了演示。由于默认地Poetry支持PyPI发布，所以有些参数就不需要提供了。

这里的介绍主要是解释Poetry的运行原理。通过我们上一章提供的向导生成的项目，发布是在CI中自动完成的。


## 思考题

1. 为何要使用Semantic Version?
2. 当前版本是``0.1``,执行``poetry version pre-release``，新的版本号是?
3. 为何要尽可能精确地锁定依赖的版本号？锁定版本号后，依赖失去自动升级能力，这样做是好是坏？
4. 如何查看项目安装的依赖库（使用Poetry)?
5. 如果在使用Poetry过程中，依赖解析和安装较慢，如何修改Poetry源？

[semantic version]: https://semver.org/
