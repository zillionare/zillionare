# 工程布局与向导工具

一个实用项目，必然在功能实现之外，还涉及到产品质量控制（包括单元测试、代码风格控制等），版权、发布历史、制作分发包等杂务，从而也就在实现功能的源代码之外，引入了许多其它文件。这些文件应该如何组织？有没有基本的命名规范？是否有工程模板可以套用，或者可以通过工具来生成？这一章将为您解答这些问题。

项目文件布局必须遵循一定的规范。这有两方面的考虑，一是项目文件布局是项目给人的第一印象，一个布局混乱的项目，会吓跑潜在的用户和贡献者；遵循规范的项目文件布局，可以让他人更容易上手；二来，构建工具、测试工具等工具也依赖于一定的文件结构。如果文件结构没有一定的规范，则必然要对每个工具进行一定的配置，才能使其工作。过多的配置项往往会引起错误，加重学习成本。

在工程构建过程中，使用约定俗成的项目文件结构和规范的文件、文件夹名字，而不是通过繁琐的配置项目以允许过度自定义，这种原则被称为惯例优于配置(convention over configuration)，不仅仅是Python,也是许多其它语言遵循的原则。

## 项目文件的组成

Python工程一般应该包含以下内容：

### 项目说明文档
一般使用readme作为文件名，大写。可使用rst文件格式或者markdown文件格式。
### 许可证文档
一般使用license作为文件名，大写。可使用rst文件格式或者markdown文件格式。
### 版本历史文档
一般使用history作为文件名，大写，可使用rst文件格式或者markdown文件格式。清晰的版本说明是十分重要的，用户需要根据自己的情况，来选择使用哪一个版本，或者决定是否要升级到新的版本。
### 开发者介绍文档
一般使用authors作为文件名，大写。其目的是向用户介绍项目的开发者团队。
### 工程构建配置文件
不同的构建工具需要不同的配置文件。在Python工程中，主要有两种主流的构建工具，一是Python setup tools,二是符合PEP517，PEP518规范的新型构建工具，如Poetry等。

Python setup tools需要的配置文件有setup.py, MANIFEST.IN等文件；如果是使用Poetry,需要的配置文件则是pyproject.toml。

除此之外，使用Python setup tools的工程可能还需要requirements.txt和makefile。
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

### 单元测试文件目录
单元测试文件的目录名一般为tests。

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

### CI/CD
一些项目启用了CI/CD，这样就可能引入travis.yml或者github actions等。

### codecoverage

一些项目启用了code coverage report,可能引入.coveragerc这个配置文件。


## 项目生成向导 - cookiecutter

使用微软Visual Studio的开发者都会很熟悉它的各种工程向导。通过这些工程向导，你可以快速新建一个工程，或者创建一个新的类，新的链接库等。使用IntelliJ IDEA产品的java开发者也都很熟悉它的project wizard。我们之所以需要这些工具，是因为搭建一个项目的架子是一个既繁琐无味，又容易出错的过程。而且，一个项目真正的价值却并不在这些地方。

在Python世界中，很遗憾没有任何一个开发工具（无论是vscode还是pycharm)提供这样的功能。幸运的是，有一个开源的项目，[cookiecutter](https://cookiecutter.readthedocs.io)，可以帮我们生成各种项目的架子。

cookiecutter本意是饼干制造机。在这里，cookiecutter是一个生产项目模板的基础框架，理论上可用以生成任何开发语言的项目框架。通过cookiecutter,结合各种事先定义好的工程模板，就可以快速定制出自己想要的项目框架。

[cookiecutter.pypackages](https://github.com/audreyfeldroy/cookiecutter-pypackage)（以下简称pypackages)是遵循cookiecutter规范开发的一个生成Python项目的模板。

在`pypackages`生成项目的过程中，会询问开发者名字、电邮、项目名称，许可证类型（会让你在MIT，BSD等好几种知名的许可证模式中选择，并提供标准的LICENSE文本），是否集成click这个命令行接口，是否生成console script等。

通过`pypackages`生成的项目文件，几乎包括了前面提到的项目文件中的所有内容。需要指出的是，它使用的构建工具是setup tools，所以会有`setup.py`, `MANIFEST.in`, `makefile`这些文件存在；其文档构建工具使用sphinx，所以在docs目录下，会存在conf.py和Makefile。

下面的截图显示的是通过`pypackages`生成的项目框架的文件列表：


关于如何使用`pypackages`，这里有它的帮助文档和[教程](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html)

??? Readmore
    console script是Python的分发包的一种功能，允许在安装过程中，将指定的python脚本安装到用户可执行程序路径下,直接从命令行调用，就象原生的shell命令一样。

需要注意的是，上述模板中使用的打包工具是setup tools，它的依赖管理功能较弱，现在已逐渐被Poetry替代。[briggySmalls](https://github.com/briggySmalls/cookiecutter-pypackage)的这个模板，在上述模板的基础上，采用了Poetry.



