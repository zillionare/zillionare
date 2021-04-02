
# 大富翁产品矩阵

## Zillionare

统领大富翁各个子项目。Zillionare的一些功能往往是多个组件服务共同完成的，这些组件都有自己的版本编号，我们通过统一发布容器化部署版本的方式，将功能发布以一个完整、单一的视图呈现给用户。

除了容器化部署版本之外，您还可以在这里找到帮助文档和教程。
## Omega

[Omega](https://github.com/zillionare/omega>) 是基于Sanic构建的微服务，它通过行情适配器来收发数据，通过Omicron来将这些数据存储到本地。Omega也是行情同步任务的管理者。

通过前置Nginx，就可以负载均衡的方式提供分布式行情数据服务。此外，Omega还通过消息服务实现多进程之间的任务协作。这些进程可以运行在局域网内的不同的机器上。

[使用文档](https://zillionare-omega.readthedocs.io/zh_CN/latest) [项目地址](https://github.com/zillionare/omega)
## Omicron

[Omicron](https://github.com/zillionare/omicron>) 提供了数据的本地存储读写和其它基础功能，比如交易日历和时间，Triggers，类型定义等。它是zillionare各子项目依赖的数据访问sdk。在您安装了Omega服务器之后，就通过Omicron这个sdk来使用行情数据。

[使用文档](https://zillionare-omicron.readthedocs.io/zh_CN/latest/>) [项目地址](https://github.com/zillionare/omicron)

=========
开发指南
=========

本文档适用于Zillionare系列项目的协同开发者。

这一章详细讲解了大富翁的开发工具链，多数情况下，我们还讲述了选择这些工具的理由。

如果您参与开发大富翁相关项目，您很可能不需要从头配置这些工具链，因为相关的配置文件都会随代码clone时下载到本地，您只需要运行 ``pip install -r requirements_dev.txt`` , 绝大多数工具就完成了配置，只有两个例外：

1. 您需要运行 ``pre-commit install`` 来完成pre-commit hooks的安装
2. 您需要设置IDE，使之在代码保存时，自动运行lint工具。

尽管如此，理解我们为何选择这些工具，各项配置又如何起作用，在多人协作项目中，仍然是十分重要的。所以，我们推荐大富翁的协同开发者在进入开发之前，认真阅读这一章。Zillionare项目尽可能遵循Python工程最佳实践。我们通过采用社区内广泛认可的各种工具来保证实现最佳实践。因此，熟悉了本章的内容，也可以认为就熟练掌握了Python工程最佳实践。

.. hint::

    Poetry已经是官方推荐的构建工具。但大富翁项目中并未使用Poetry。
    原因有二：

    1. Poetry目前（2020年11月）还有较严重的性能 `bug <https://github.com/python-poetry/poetry/issues/2094>`_，在进行依赖解析时，一次运行可以长达半小时或者更久。这个问题可能由多重原因引起，也包括部分问题只出现在中国大陆；所以预期这个问题难以在短时间内完全解决。为避免降低开发效率，目前我们不推荐使用Poetry。

    2. 整个社区还没有准备好。Poetry的目标是成为all-in-one的配置工具，但整个社区还需要一定的时间，使得各种依赖包、代码检查工具、测试工具等都准备好。

1. 开发环境和工具
`````````````````

关于开发环境和工具的使用，可以参考解语科技的博客文章 `windows下如何构建Python开发环境 <http://blog.jieyu.ai/blog_2020/%E5%A6%82%E4%BD%95%E6%9E%84%E5%BB%BAPython%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83/>`_。

1.1 操作系统和IDE
-----------------

项目中使用的库和测试用例，均只保证在Linux下正确和高效运行。因此，推荐使用Windows + Linux的混合式开发环境，或者您可以使用Win10 + WSL的方式进行开发。不推荐使用纯粹的Windows进行开发。

.. csv-table:: 软件清单
    :header: "软件类别","软件","版本","说明"
    :widths: 20, 15, 15, 15

    操作系统,Ubuntu/WSL,18.04,
    IDE,vscode/pycharm,,pycharm专业版，以便远程调试
    运行时,Python,3.8,
    内存数据库,Redis,>4.0,
    数据库,Postgres,>10,存放市值数据
    负载均衡,Nginx,,选装
    行情服务,jqdatasdk,>1.8,
    日志服务,rsyslog,,在生产环境下使用
    容器,docker,,用于模拟生产环境部署

1.2 虚拟运行环境
----------------

每一个子项目，都应该在其对应的虚拟环境下运行。比如，开发Omega时，需要新建一个Omega的开发环境，将所有的依赖库均只安装到这个虚拟环境中（并且根据需要添加到setup.py中）。

推荐使用miniconda来构建虚拟环境。但项目中使用tox，所以virtual env也在使用之中。

1.3 工程模板
--------------

创建新的工程时，我们往往有一堆繁琐的搭架子的工作。一些IDE或者应用框架为此提供了相应的开发模板。在大富翁开发中，我们使用 Cookiecutter_ 库来创建新应用的基本框架。Cookiecutter_会为我们生成文档框架(Shpinx构建系统，各种文档模板）、多版本测试（Tox）、CI集成（Travis, code coverage)、版本发布（Twine，pypi等）。要完全从头开始手工配置所有这些工具，并使之协同工作是需要花较多时间的。

Omega, Omicron, Omega-jqadaptor等子项目都是通过 Cookiecutter_ 来创建的。如果需要创建新的子项目，推荐仍使用 Cookiecutter_ 来创建，以保证新的项目有同样的开发发布流程和质量标准。

在Cookiecutter创建模板时，还会指定是否创建Console script，并且推荐使用Click作为命令行工具的开发框架。在大富翁项目中，我们不使用Click，而是使用google出品的fire框架。Fire上手更容易，代码量更少。

1.4 文档构建
-------------

使用reStructuredTxt文档格式，并使用Sphinx来构建。构建的文档发布到 `readthedocs <https://readthedocs.org/>`_。

对于docstring，约定统一使用 `google style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_。

我们使用doc8来对文档时行测试。在tox中进行配置，详见本章中tox一节。


2. 代码质量
```````````````
大富翁通过约定代码风格、强制代码检查、集成测试、测试覆盖率等手段来保证代码质量。

2.1 代码风格
------------
1. 使用空格而不是制表键来实现缩进
2. 缩进大小为4
3. 换行符始终为lf
4. 每行长度最大不超88个字符

在大富翁的每一个子项目的根目录里，都有一个.editorconfig文件，用以约定上述规范:

.. code::

    # .editorconfig

    # http://editorconfig.org

    root = true

    [*]
    indent_style = space
    indent_size = 4
    trim_trailing_whitespace = true
    insert_final_newline = true
    charset = utf-8
    end_of_line = lf

    [*.bat]
    indent_style = tab
    end_of_line = crlf

    [LICENSE]
    insert_final_newline = false

    [Makefile]
    indent_style = tab

对于Python文件，我们使用`black <https://github.com/psf/black>`_ 来强制代码风格。

2.2 linting
-------------

大富翁在开发过程中，要求开发者在三个时机都进行代码检查。

第一个时机是保存代码时。需要设置您的IDE在保存代码时自动进行代码检查和格式化。如果您使用vscode，则应该按如下方式设置：

.. code::

    # settings.json
    "editor.codeActionsOnSave": {
        "source.fixAll": true,
        "source.sortImports": true
    },
    "editor.formatOnPaste": true,
    "editor.formatOnSave": true,

第二个时机是在提交代码时。大富翁的每一个子项目，都要求设置pre-commit hook：

pre-commit是一个Python库，安装后，您需要运行 ``pre-commit install`` 命令，并在工程根目录下放置如下配置文件：

.. code::

    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/pre-commit/mirrors-isort
        rev: v4.3.21
        hooks:
        - id: isort
        exclude: docs/conf.py
    -   repo: https://github.com/ambv/black
        rev: stable
        hooks:
        - id: black
    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v2.3.0
        hooks:
        - id: flake8

根据上述配置，每次您在提交代码前，git将自动运行isort, black和flake8。

2.2.1 isort
::::::::::::

isort是一个Python imports整理工具。它执行Python imports段的格式化、以及import的排序。它不能移虽导入、但未使用的import库。

如果您使用vscode，flake8会报告未使用的导入错误，然后您需要手动移除它（不要使用autoflake)_。
如果您使用Pycharm，Pycharm会提示并自动移除import错误。

我们使用工程根目录下的.isort.cfg来配置：

..code::

    # .isort.cfg
    [settings]
        multi_line_output = 3
        include_trailing_comma = True
        force_grid_wrap = 0
        use_parentheses = True
        ensure_newline_before_comments = True
        line_length = 88

        # 不检查docs/下的conf.py，这个文件中有一个不规范的导入，是必须的
        skip_glob = docs/conf.py

2.2.2 black
::::::::::::

black是一个Python代码格式化工具，相比其它代码格式化工具，以其代码风格强制统一、毫不妥协著称。它惟一能配置的选项就是每行最大字符数。在大富翁项目中，我们也使用其默认的88个字符。因此，对于black，无须任何配置即可使用。

2.2.3 flake8
:::::::::::::

大富翁选择flake8作为lint工具，而不使用pylint。在某些方面，pylint甚至表现比flake8更好。但在vscode中进行开发时，如果启用了pylance（推荐使用），pylance也会报一些lint相关的错误，pylint也会在同样位置报告lint错误。如果该错误经确认需要supress，则需要在同一行同时使用两种不同的语法来supress这个错误。而Pylint的语法比较繁琐（虽然更清晰），很容易导致行超长。

另外，pylint报告的错误信息过多，也会一定程度上使程序员陷入各种“纠错”中，但这些错误不见得真的就成为问题，因此影响了开发的效率，收获并不大。

我们通过在工程根目录下放置.flake8文件来进行配置，内容如下（注意有一部分是为了解决与black的兼容性问题）：

.. code::

   [flake8]
    # required by black, https://github.com/psf/black/blob/master/.flake8
    max-line-length = 88
    max-complexity = 18
    extend-ignore = E203, E266, E501
    select = B,C,E,F,W,T4,B9
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


第三个时机则是在使用tox进行测试时，其配置我们留到tox这一节再讲。

3. 测试
````````````
在大富翁中，我们使用这些工具来进行单元测试：

3.1 unittest
--------------
unittest、pytest和nose是Python中常用的单元测试框架。因为unittest是标准库的一部分，所以大富翁使用unittest来写单元测试用例。如果有必要，未来也可能更改为pytest。使用pytest作为测试工具现在更为流行。

3.2 pytest
-----------

大富翁使用pytest作为单元测试的运行工具。我们一般不单独运行pytest，而是通过tox来调用。

3.3 coverage
-------------

大富翁使用coverage和py-cov来衡量单元测试的覆盖率。通过在工程根目录下放置.coveragerc文件来实现对其配置：

.. code::

    # .coveragerc
    [run]
    omit =
        */config/schema.py
    [report]
    exclude_lines =
        pragma: no cover
        def __repr__
        if self.debug:
        if settings.DEBUG
        raise AssertionError
        raise NotImplementedError
        if 0:
        if __name__ == .__main__.:

上述配置是大富翁推荐的默认配置。其中config/schema.py是配置的schema文件，由cfg4py自动生成，无须测试。

3.4 tox
----------

大富翁使用 `tox <https://tox.readthedocs.io/en/latest/>`_ 来管理集成测试。大富翁中使用tox.ini来配置：

.. code::

    # tox.ini
    [tox]
    envlist = py38, lint

    [travis]
    python =
        3.8: py38

    [testenv:lint]
    basepython = python
    deps =
        flake8
        doc8
        black
    commands =
        black omega tests
        flake8 omega tests
        doc8 docs

    [testenv]
    basepython = python
    deps =
        pytest
        pytest-cov

    setenv =
        PYTHONPATH = {toxinidir}
        PYTHONWARNINGS = ignore
    passenv = *

    commands =
        pip install -r requirements_dev.txt
        pytest --cov=omega --cov-append --cov-report=term-missing --cov-config \
        .coveragerc tests

上述配置要求在运行tox时，对代码再进行一次检查（见lint一节）。这里请注意我们使用了doc8来对文档进行检查。

配置还要求在使用pytest运行测试时，对代码进行覆盖率检查。通过--cov-conig=.coveragerc来传入配置。


4. 开发流程
------------

如果您有意愿参与大富翁项目的开发，请从主分支上fork为自己的分支，完成功能开发、单元测试之后，发出merge requst，项目的owner经评估之后，将会及时merge回主分支。


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
