# 工程布局与向导工具

这一章介绍规范的项目布局应该遵循哪些结构，并在最后介绍了一个遵循社区最新规范的、生成Python工程框架的向导工具。

一个实用项目，必然在功能实现之外，还涉及到产品质量控制（包括单元测试、代码风格控制等），版权、发布历史、制作分发包等杂务，从而也就在实现功能的源代码之外，引入了许多其它文件。这些文件应该如何组织？有没有基本的命名规范？是否有工程模板可以套用，或者可以通过工具来生成？这一章将为您解答这些问题。

项目文件布局必须遵循一定的规范。这有两方面的考虑，一是项目文件布局是项目给人的第一印象，一个布局混乱的项目，会吓跑潜在的用户和贡献者；遵循规范的项目文件布局，可以让他人更容易上手；二来，构建工具、测试工具等工具也依赖于一定的文件结构。如果文件结构没有一定的规范，则必然要对每个工具进行一定的配置，才能使其工作。过多的配置项往往会引起错误，加重学习成本。

??? Readmore
    以依赖管理和构建工具Poetry为例，它会默认把构建生成的包放在dist目录下，tox在构建测试环境时，则会在这个目录下寻找安装包。这是一种约定。

在工程构建过程中，使用约定俗成的项目文件结构和规范的文件、文件夹名字，而不是通过繁琐的配置项目以允许过度自定义，这种原则被称为惯例优于配置(convention over configuration)，这不仅仅是Python,还是许多其它语言遵循的原则。

## 项目文件的组成

Python工程一般应该包含以下内容：

### 项目说明文档
一般使用readme作为文件名，大写。可使用rst文件格式或者markdown文件格式。用来向使用者概括性地介绍这个项目的基本情况，比如主要功能、优势、版本计划等。
### 许可证文档
一般使用license作为文件名，大写。可使用rst文件格式或者markdown文件格式。开源项目必须配置此文档。
### 版本历史文档
一般使用history作为文件名，大写，可使用rst文件格式或者markdown文件格式。

每一个版本发布，都可能引入新的功能、修复了一些bug和安全性问题，也可能带来一些行为变更，导致使用者必须也要做相应的修改才能使用。

如果没有一个清晰的版本说明，您的程序库的用户就不知道应该选用哪一个版本，或者是否应该升级到您的最新版本上。使用新的版本可能会有益处，但也带来很多测试的工作。因此，我们在使用其它人开发的程序库时，并不一定要选择最新的，有时候甚至升级到最新的版本会导致程序无法运行。比如SQLAlchemy是一个应用十分广泛的Python ORM框架，最近发布了1.4版本，这个版本与前面的版本有较多不兼容的问题。如果您的程序不加修改就直接升级到1.4，那么大概率程序会崩溃。
### 开发者介绍文档
一般使用authors作为文件名，大写。其目的是向用户介绍项目的开发者团队。
### 工程构建配置文件
不同的构建工具需要不同的配置文件。在Python工程中，主要有两种主流的构建工具，一是Python setup tools,另一种是符合PEP517，PEP518规范的新型构建工具，如Poetry等。

Python setup tools需要的配置文件有setup.py, MANIFEST.IN等文件，还可能会有requirements.txt和makefile；如果是使用Poetry,需要的配置文件则是pyproject.toml。

如果您开始新的项目，请使用Poetry。它的依赖管理可以锁定程序的运行时，避免很多问题。但是，您可能依然要能看懂基于setup tools的老式工程配置，它们将可能在未来的一两年里还继续存在。
### 代码目录
在其它开发语言，特别是编译型语言中，代码目录常常被称为源文件目录。由于Python是非编译型语言，代码源文件本身就是可执行文件，所以一般我们不把代码文件称作源文件。我们通常把发行的目标物称之为一个“包”（package)。因此，在下面的叙述中，我们将会把代码目录称之为包目录，或者package目录。

因此，如果您正在开发一个名为sample的package，那么您的代码就应该放在一个名为sample的目录下。结合我们已经提到的文件，现在我们的sample工程的布局应该如下所示：

```text
├── sample
│   ├── AUTHORS.md
│   ├── HISTORY.md
│   ├── LICENSE.md
│   ├── MANIFEST.in
│   ├── README.md
│   ├── makefile
│   ├── sample
|   |   ├── core.py
│   │   └── helper.py
│   └── setup.py
```
这里顶层的sample是项目名字，内层的sample是包名字。两级目录共用一个名字，这是会让人多多少少有一些困惑的地方。但是，在Python中,我们不能象其它语言那样，直接把package目录改为src目录，因为这样会导致生成的package名字也会叫src。

这样制作出来的发行包，包名字会是sample。当我们要使用sample中模块的功能时，可以这样导入：

```python
# 注意， `import *`一般来说是一种不好的语法，这里这样使用，是为了方便示例。
from sample.helper import *
```

??? readmore
    Pypa在[sampleproject](https://github.com/pypa/sampleproject)中给出了另一种文件结构，在这里`sample`放在src目录下。

    我们在上一章中提到过，pypa就是pypi的开发者，python分发包事实上的标准。因此他们的趣向也会影响到其它开发者。

    可以肯定的是，无论如何，代码目录名必须是package名字，而不能为其它。至于要不要在其上再加一层src/目录，目前还存在一些争议。但是，一旦您的工程确定了目录结构，此后就不要修改，否则，会涉及到大量文件需要修改，因为这跟导入密切相关。

    这个例子中我们使用了老式的构建工具。注意除了构建工具之外，其它部分仍然是一样的。

### 单元测试文件目录
单元测试文件的目录名一般为tests。这也是许多测试框架和工具默认的文件夹位置。

### Makefile
对Python程序员来说，可能并不太喜欢Makefile。Makefile最主要的功能，生成依赖，在Python构建中并不存在。所以在最新的基于Poetry的项目模板中，是没有Makefile的。但是有一些工具，比如sphinx文档构建中还需要Makefile；此外，Makefile的多target命令模式，也还有它的用处，因此，是否使用Makefile，可以取决于您项目的需要。

### 文档目录
一般使用docs这个名字。项目的帮助文档，也可能包含文档构建工具的配置，都放在这个目录下。更详细的内容，将在文档构建一章中讲解。

使用mkdocs来构建文档是现在比较流行的趋势。使用mkdocs来构建文档时，除了要使用docs目录来存放文档之外，一般还需要在根目录下放置mkdocs.yml这个配置文件。

### lint相关工具文档
项目可能使用工具如flake8来进行语法检查，使用black来进行格式化。这些工具都会引入配置文件。此外，为了保证签入服务器的代码的风格和质量，可能会配置pre-commit hooks。

### tox
如果一个项目同时支持多个Python版本，那么在发布之前，往往需要在各个Python环境下都运行单元测试。为单元测试自动化地构建虚拟运行环境并执行单元测试，这就是tox要做的工作。这也是上一章讲的虚拟运行环境的一个实际使用案例。

配置了tox的项目，会在根目录下引入tox.ini文件。

### CI
在项目中使用CI是尽早暴露问题，避免更大的损失的有效方法。通过使用CI，可以确保程序员签入的代码在并入主分支之前，是能够通过单元测试的。

有一些在线的CI服务，比如appVeyor, travis和后起之秀github actions. 作者没有使用过AppVeyor。如果使用travisr话，需要在根目录下放置travis.yml这个文件。如果使用github actions，则需要在根目录下的.github/workflows/中放置配置文件，github对配置文件的名字没有要求。

### codecoverage

我们需要通过code coverage来度量单元测试的强度。一些优秀的开源项目，其code coverage甚至可以做到100%（当然允许合理地排除一些代码）。在Python项目中，我们一般使用[coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/)来进行代码覆盖测试。测试框架比如pytest都会集成它，无须单独调用，但一般需要在根目录下配置.coveragerc。

作为开源项目，我们希望能够发布单元测试覆盖报告，以便给使用者更强的信心。[Codecov]就是这样一个平台。一般我们在CI中配置它。所以这部分配置会体现在CI的配置文档中。

## 项目生成向导 - cookiecutter

通过上面的介绍，您可能已经发现，要手动生成一个规范的项目框架并不容易。要理解每种工具的作用，并且配置好它们使之能协同工作，需要一定的经验，在许多开发组里，搭架子的工作一般由dev lead来进行，这也是有其依据的。

??? Readmore
    一些工具的默认配置可能会相互冲突，这也是非常常见的现象。因为大家对什么是最优的技术路线都有自己的理解。比如flak8与black之间，对什么是正确的代码，有一些地方看法就不一致，从而导致black格式化的代码，总是通不过flak8的检查。

    因此，如何使得工具之间相互协调，也是新建项目时比较费时费力的事。

如果您有其它语言的开发经验，您会发现象visual studio， 或者IntelliJ这样的开发工具有较好的向导，您只需要点击一些按钮，填写一些信息，就能立刻生成一个能编译的项目。在Python世界中，很遗憾没有任何一个开发工具（无论是vscode还是pycharm)提供这样的功能。

幸运的是，有一个开源的项目，[cookiecutter](https://cookiecutter.readthedocs.io)，可以帮我们生成各种项目的架子。

??? Readmore
    现在的趋势是，除了IDE之外，一些框架和工具本身也在提供生成向导。比如js中的vue。本文中多次提到的Poetry也有生成框架程序的功能，不过，它并不能提供上文介绍的所有这些文件的模板，更不要提自定义它们。

cookiecutter本意是饼干制造机。在这里，cookiecutter是一个生产项目模板的基础框架，理论上可用以生成任何开发语言的项目框架。通过cookiecutter,结合各种事先定义好的工程模板，就可以快速定制出自己想要的项目框架。

cookiecutter-pypackage是遵循cookiecutter规范开发的一个生成Python项目的模板，它在github上有3k的stars。

在`pypackage`生成项目的过程中，会询问开发者名字、电邮、项目名称，许可证类型（会让你在MIT，BSD等好几种知名的许可证模式中选择，并提供标准的LICENSE文本），是否集成click这个命令行接口，是否生成console script等。回答完成这些问题之后，您就能得到一个框架程序，您可以立刻编译并发布它，包括文档。

cookiecutter-pypackage 所使用的技术并不符合现在的社区规范，所以作者基于这个repo，开发了一个全新的模板，它具有这些功能：

1. 使用[Poetry]来管理版本、依赖，进行构建和发布
2. 使用[Mkdocs]和`Markdown`来写文档，替换掉繁琐的sphinx和reStructuredText。本系列教程也是使用的Mkdocs + Markdown
3. 使用[Pytest]来进行单元测试。您仍然可以使用Python的标准库unittest来开发测试用例
4. 生成codecoverage report,并自动上传到[Codecov]
5. 使用[Tox]来进行单元测试的矩阵覆盖，这个阶段还同时进行lint, code formatting和artifact测试。
6. Format with [Black] and [Isort]
7. Lint code with [Flake8] and [Flake8-docstrings]
8. 通过[Pre-commit hooks]在代码签入时，强制进行lint和format
9. 通过[Mkdocstrings]来自动生成API文档
10. 使用[Python Fire]来生成命令行接口（console script)。[Python Fire]要比[Click]更简单易用。您基本上无须进行学习即可上手。
11. 使用[Github Actions]来进行CI，并在CI通过之后，从release分支上自动发布
12. 使用[Git Pages]来托管您的文档

??? Readmore
    什么时artifact测试？当您发布构建好的程序库到PyPI时，有可能因为格式问题被拒绝。Twine工具可以对artifact进行检查，提前发现这种错误。

    console script是Python的分发包的一种功能，允许在安装过程中，将指定的python脚本安装到用户可执行程序路径下,直接从命令行调用，就象原生的shell命令一样。

    为什么要通过CI来进行发布？从开发机器上进行发布有很大的随意性，难以确保发布包的质量。当您的代码签入到release分支，通过测试后，您给分支打上tag，这时就会触发自动发布。这样发布的包可以确保质量。

这个向导工具的文档在[这里](https://zillionare.github.io/cookiecutter-pypackage/)。

## 如何使用项目生成向导

### 1. 安装cookecutter
```
pip install cookiecutter
```

### 2. 生成项目

```
cookiecutter https://github.com/zillionare/cookiecutter-pypackage.git
```
这里会提示输入一些信息。注意project_slug是github repo的名字，默认也是您的程序库的名字。不能有空格和"-"。

### 3. 构建虚拟运行时环境
由于使用了Poetry来进行管理，这一步并不是必须的。但推荐为您的项目通过conda构建一个集中式管理的虚拟运行时，并在之后一直使用它。

```
conda create -n mypackage python=3.8 #请根据项目需求选择正确的版本
conda activate mypackage
```

### 4. 安装开发依赖

模板使用Poetry来进行项目管理，并将项目的依赖分成dev, test, doc三个组，这样依赖的粒度更小一些。作为开发者，应该同时安装这三组依赖。

```
pip install poetry
poetry install -E doc -E test -E dev
tox
```
在安装好开发依赖之后，我们立即运行了`tox`命令，对新生成的框架程序进行测试。命令最后会给出一个测试报告和lint report。不出意外，这里不应该有任何错误（但可能会有重新格式化的警告).

### 5. 创建Github Repo
登录到github,创建一个名为mypackage的repo（mypackage即为project_slug)。然后在本机进入mypackage目录，执行以下操作：

```
cd mypackage

# !!! uncomment the following line, if you didn't choose install pre-commit hooks at 
# last step. If you chose 'yes', then cookiecutter have already done that for you, since 
# pre-commit install need repo exist.

# git init
git add .
git commit -m "Initial skeleton."
git branch -M main
git remote add origin git@github.com:myusername/mypackage.git
git push -u origin main
```

???+ Warning
    如果您在生成项目时，没有选择启用pre-commit hooks，那么您需要去掉第7行的注释。如果您启用过pre-commit hooks的话，这个命令就已经运行过了。

### 6. 进行发布测试

您可以通过向testpypi进行发布来测试构建过程，您也可以忽略这一步。

关于这一步，请参见[文档](https://zillionare.github.io/cookiecutter-pypackage/tutorial/)

### 7. 设置Github CI

您也可以暂时忽略这一步，但是强烈建议您完成它。

向导生成的项目中已经包括了必要的CI步骤，如调用tox进行测试，发布文档和发行包。但是需要您配置一些账户。您需要生成github的personal token，并在repo > settings > secrets中，新增一个名为``PESONAL_TOKEN``的环境变量，其值设置为您的token。

您需要在[test pypi](https://test.pypi.org/manage/account/)和[pypi](https://pypi.org/manage/account/)上申请部署用token，并象刚刚设置github token一样，新增``TEST_PYPI_API_TOKEN``和``PYPI_API_TOKEN``这两个变量。

模拟设置为，当您向master, main或者release分支签入代码时，会启动CI，并在测试通过后，自动向testpypi进行发布；当release分支签入代码，并且打了tag时，则在测试通过后，自动向pypi进行发布。

### 8. 设置Codecov

CI已设置为自动发布codecoverage report，但需要您在[codecov]上导入您的repo并授权。

现在，一个规范的新项目就已经创建好，您已经拥有了很多fancy的功能，比如CI，codecov, git pages，poetry，基于markdown的文档等等。

接下来，我们将带领您深入这些工具，了解为什么在众多工具中，选择了这一种，应该如何配置，如何使用等等。

# 思考题

1. 为什么要写版本历史？写版本历史文件有哪些好的实操？
2. 为什么要使用CI？为什么要通过CI来进行版本发布？
3. 为什么向导生成的模板中，配置了testpypi发布？这样有哪些好处？
4. 为什么要选择Github Actions作为CI工具？试与AppVeyor、Travis进行比较。
5. 为什么要使用Mkdocs，而不是Sphinx来进行文档构建？试从支持的文件格式、托管平台等方面进行比较。

[poetry]: https://python-poetry.org/
[mkdocs]: https://www.mkdocs.org
[pytest]: https://pytest.org
[codecov]: https://codecov.io
[tox]: https://tox.readthedocs.io
[black]: https://github.com/psf/black
[isort]: https://github.com/PyCQA/isort
[flake8]: https://flake8.pycqa.org
[flake8-docstrings]: https://pypi.org/project/flake8-docstrings/
[mkdocstrings]: https://mkdocstrings.github.io/
[Python Fire]: https://github.com/google/python-fire
[github actions]: https://github.com/features/actions
[Git Pages]: https://pages.github.com
[Pre-commit hooks]: https://pre-commit.com/



