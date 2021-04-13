# 高效编码

这一章介绍如何在VsCode中高效地编码，包括如何使用代码自动完成、自动检查错误和格式化代码。错误检查和代码格式化看起来更像是高质量的规范编码的一部分。但是俗话说，欲速则不达，所以正确的做事，本身也是高效的一部分。另外，既然教程的每一章都是关于如何规范地进行Python工程开发的，所以，如果专门突出某一章与“规范”的关系，反倒奇怪。

## 代码自动完成

IDE的重要功能就是提供代码自动完成。Vscode中这项功能是通过扩展来完成的。有两个主要的扩展，Pylance和Kite,当前建议都安装上。Pylance是微软官方的扩展，基于静态分析工具pyright，目前比之Kite，功能略显不足。

Kite自我评估可以完成87-95%的表达式，并且可以实现自动插入代码片段：

![](http://images.jieyu.ai/images/202104/kite.gif)

另一个比较好的功能，就是函数的文档提示。Kite的提示界面比较大，有时候还会提示一些其它人的用法示例。很多时候，看其他人怎么用，可能比阅读文档更快捷，这也是所谓的copy & paste编程方法。

还有一个比较神奇的功能，就是似乎安装了kite的话，在终端上写代码，也能得到提示。不知道这是Ipython的功能，还是kite的功能，没有进一步去查证了。

Pylance在上面提到的代码自动完成之外，还能实现依赖自动导入。此外，由于它脱胎于语法静态检查器，所以它还能提示代码中的错误并显示。这样我们可以尽早修正这些错误。

![](http://images.jieyu.ai/images/202104/20210413172416.png)

??? Tips
    Pylance安装后，需要进行配置。配置文件是pyrightconfig.json，放置在项目根目录下。
    ```
    {
        "exclude": [
        ".git",
        ".eggs"
        ],
        "ignore": [],
        "reportMissingImports": true,
        "reportMissingTypeStubs": false,
        "pythonVersion": "3.8"
    }
    ```
    这些配置项也可以在vscode中配置，但为了使开发成员使用一致的配置，建议都采用文件配置，并且使用git来管理。

??? Tips
    在程序中使用配置项是个容易出错的地方。你需要记住配置项名称，如果输入错误，没有任何工具能够发现，直到运行时出错，报告Key error错误。 [cfg4py](https://pypi.org/project/cfg4py/)提供了一个比较好的解决方案。它把配置文件编译成python class，从而使得IDE可以进行代码自动完成和查错。

## Type annotation

很多人谈到Python时，会觉得作为动态语言，因为没有强类型约束，所以没法做代码检查。实际上这正在成为历史。Python 3很早就加上type annotation语法，现在你应该这样定义一个函数：

```
def foo(name: str)->int:
    score = 20
    return score
```
type annotation并不是运行时的约束，只能用于IDE进行辅助检查。但有了这个约束，现在IDE已经能够比较容易地检查出一些调用错误了，并且代码重构也变得可能。

## 重构

如果您的代码都做好了type annotation，那么IDE基本上能够提供和强类型语言类似的重构能力。需要强调的是，在重构之前，你应该先进行单元测试，代码lint和format，在没有错误之后，再进行重构。

## Lint工具

Lint工具对代码进行逻辑检查和风格检查。逻辑检查是指象使用了未定义的变量，或者定义的变量未使用，没有按type annotation的约定传入参数等等；风格检查是指变量命名风格、空白符、空行符的使用等。

Python社区有很多Lint工具，比如Plint, PyFlakes, pycodestyle, bandit, Mypy等。此外，还有Flake8和Pylama这样，将这些工具组合起来使用的工具。

在选择Lint工具时，重要的指标是报告错误的完全度和速度。过于完备的错误报告有时候也不见得就是最好，有时候会把你的大量精力牵涉到无意义的排查中 -- 纯粹基于静态分析的查错，有时也不可避免会出现错误；同时也使得运行速度降低。

这也是在我们的向导中，选择flake8的原因，它基于的Pyflake，一个重要原则就是尽可能减少False Positive的报告。与Pylint相比，它在运行速度上也明显占优。

配置flake8，可以在根目录下放置.flake8文件。尽管可以把配置整合到pyproject.toml文件中，我们仍然推荐使用单独的配置文件。对后面将提到的其它工具的配置文件，我们也是一样的态度。

.flak8是一个ini格式的文件，以下是一个示例：

```
[flake8]
# required by black, https://github.com/psf/black/blob/master/.flake8
max-line-length = 88
max-complexity = 18
ignore = E203, E266, E501, W503, F403, F401
select = B,C,E,F,W,T4,B9
docstring-convention=google
per-file-ignores =
    __init__.py:F401
exclude =
    .git,
    __pycache__,
    setup.py,
    build,
    dist,
    releases,
    .venv,
    .tox,
    .mypy_cache,
    .pytest_cache,
    .vscode,
    .github,
    docs/conf.py,
    tests
```

我们排除了对test文件进行lint，这也是flake8开发者的推荐。这里最初几行配置，是为了与black兼容。如果不这样配置，那么经black格式化的文件，flake8总会报错，而这种报错并无任何意义。

毕竟，风格并不是一种错误。它只是一种多样性。如果不是在二进制的世界，丰富多彩总是最好的。

## Formatter工具

Formatter工具也有很多种，但是我们几乎不用去考查其它的formatter,就选择了black,只因为它的logo:
<figure>
    <img src="https://raw.githubusercontent.com/psf/black/master/docs/_static/logo2-readme.png" width="250"/>
    <figcaption> The Uncompromising Code Formatter</figcaption>
</figure>

与其它Formatter工具提供了体贴入微的自定义配置不同，Black坚持不让您做任何自定义（几乎）。这样做是有道理的，允许定制只会让团队陷入到无意义地争辩当中，而风格并无对错，习惯就好。我们常常看到在团队里，一些人为代码风格争论，其实他们反对的并不是风格本身，他们只是在反对对手而已。

当然Black还是开了一个小窗口，允许你定义代码行的换行长度，Black的推荐是88字符。有的团队会把这个更改为120字符宽，按照阴谋论的观点，幕后的推手可能是生产带鱼屏的资本力量。不过，手机屏越来越长，电脑显示屏越来越宽，似乎是一种趋势。

另外一个值得一提的工具是isort。它的作用是对代码中的`import`语句进行格式化，包括排序，将一行里的多个导入拆分成每行一个导入；始终把导入语句置于正式代码之前等等。通过向导生成的项目，这个工具也配置好了。

比较遗憾的是，在vscode下没有一个好的工具可以自动移除没有使用的导入。Pycharm是可以做到这一点的。开源的工具中有可以做到这一点的，但是因为容易出错，这里也就不推荐了。

在vscode中，Lint工具可以检查出未使用的导入，然后您需要手动移除。移除未使用的`import`是必要的，它可以适当加快程序启动速度，并降低内存占用。

## pre-commit hooks

我们把[pre-commit hooks](https://pre-commit.com)放在这一章里。

这个工具的作用，是为了防止你签入不符合规范的代码，从而污染代码库。如果使用向导生成项目的话，向导已经为您安装了pre-commit hooks,当您运行``git commit``命令时，就会看到这样的输出：

![](http://images.jieyu.ai/images/202104/20210413181638.png)

可以看出，pre-commit hooks对换行符进行了检查和修复，调用black进行了格式化，以及调用flake8进行了查错，并报告对f-string的错误使用。

当出现错误进，您必须进行修复，才能进行再次提交。

这一章的主题是高效编码。我们先是介绍了代码自动完成工具，然后讲述了如何利用语法检查工具尽早发现并修复错误，避免把这些错误带入到测试甚至生产环境中。在我们介绍的方案中，语法检查是随着您的coding实时展开的，并在向代码库提交时，强制执行一次检查。后面您还会看到，在运行测试时，还会再做一次检查。

## 思考题
1. 如何利用Pylance的错误报告？如何定制pylance，以排除无效文件？
2. 在vscode下安装kite扩展，尝试一下它的自动完成和文档提示功能。
3. 为什么推荐使用flake8?错误检查为什么不是报的越多越好？
4. 为什么推荐使用black作为格式化工具？
5. pre-commit hooks是什么？为什么要使用这个工具？
