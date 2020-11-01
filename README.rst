==========
大富翁
==========


.. image:: https://img.shields.io/pypi/v/zillionare.svg
        :target: https://pypi.python.org/pypi/zillionare

.. image:: https://img.shields.io/travis/zillionare/zillionare.svg
        :target: https://travis-ci.com/zillionare/zillionare

.. image:: https://readthedocs.org/projects/zillionare/badge/?version=latest
        :target: https://zillionare.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




AI量化交易平台

.. image:: http://images.jieyu.ai/images/2020-10/20201031231647.png

* Free software: MIT license
* Documentation: https://zillionare.readthedocs.io.


概览
--------

大富翁是一个模块化、微服务架构的开源AI量化工具。


它主要有以下几部分组成：

1. Omicron
^^^^^^^^^^^

Omicron是一个Python库，提供了数据的本地存储读写和其它基础功能，比如交易日历和时间，Triggers，类型定义等。

2. Omega
^^^^^^^^^

Omega是基于Sanic构建的微服务，它通过行情适配器来收发数据，通过Omicron来将这些数据存储到本地。Omega也是行情同步任务的管理者。

通过前置Nginx，就可以分布式方式提供行情数据服务。

3. Alpha
^^^^^^^^^

策略服务器。运行定义的各种策略，并发出交易信号。

4. Epsilon
^^^^^^^^^^^
控制台

5. Gamma（暂定）
^^^^^^^^^
交易网关。接收交易信号，并执行交易。这部分也可以集成在Alpha中。


开发者
------

大富翁是一个开源项目，欢迎更多的人加入这一社区！

1. 开发环境
^^^^^^^^^^^

操作系统和IDE
=============

推荐使用Windows + Linux的混合式开发环境，或者您可以使用Win10 + WSL的方式进行开发。不推荐使用纯粹的Windows进行开发。项目中使用的库和测试用例，均只保证在Linux下正确和高效运行。

推荐使用vscode来进行开发，但也可以选择Pycharm。注意如果因为要使用远程调试功能（如果Pycharm运行在windows上，而程序运行在Linux上），Pycharm必须选择专业版。注意Pycharm的功能要强于vscode，在代码格式化、Lint等方面必须设置为vscode能支持，或者有扩展支持。

虚拟运行环境
============

每一个子项目，都应该在其对应的虚拟环境下运行。比如，开发Omega时，需要新建一个Omega的开发环境，将所有的依赖库均只安装到这个虚拟环境中（并且根据需要添加到setup.py中）。

推荐使用miniconda来构建虚拟环境。但项目中使用tox，所以virtual env也在使用之中。

模板
============

创建新的工程时，我们往往有一堆繁琐的搭架子的工作。一些IDE或者应用框架为此提供了相应的开发模板。在大富翁开发中，我们使用 Cookiecutter_ 库来创建新应用的基本框架，包括Legal, 文档构建（Sphinx)、多版本测试（Tox）、CI集成（Travis, code coverage)、版本发布（Twine，pypi等）。要完全从头开始手工配置所有这些工具，并使之协同工作是需要花较多时间的。

Omega, Omicron, Omega-jqadaptor等子项目都是通过 Cookiecutter_ 来创建的。如果需要创建新的子项目，推荐仍使用 Cookiecutter_ 来创建，以保证新的项目有同样的开发发布流程和质量标准。

在Cookiecutter创建模板时，还会指定是否创建Console script，并且推荐使用Click作为命令行工具的开发框架。在大富翁项目中，我们不使用Click，而是使用google出品的fire框架。Fire上手更容易，代码量更少。

单元测试框架
============

目前大富公翁使用的是python unittest框架。未来新的项目也考虑使用pytest。

集成测试
========

使用`travis <https://travis-ci.org/dashboard>`_ 和`codecov <https://codecov.io/>`_。相应报告可以在其网站上看到，并通过badge将状态显示在文档中（比如github或者readthedocs)。

文档构建
========
使用reStructuredTxt文档格式，并使用Sphinx来构建。构建的文档发布到`readthedocs <https://readthedocs.org/>`_。

2. 代码风格
^^^^^^^^^^^

代码使用flake8进行lint和format。代码和文档每行最大长度为88个字符。Doc string使用google doc string风格。

不使用pylint作为lint工具。在某些方面，pylint甚至表现比flake8更好。但在vscode中进行开发时，如果启用了pylance（推荐使用），pylance也会报一些lint相关的错误，pylint也会在同样位置报告lint错误。如果该错误经确认需要supress，则需要在同一行同时使用两种不同的语法来supress这个错误。而Pylint的语法比较繁琐（虽然更清晰），很容易导致行超长。

3. 流程
^^^^^^^^^^^
开发者在开发之前，应该从主分支上fork为自己的分支，完成功能开发、单元测试和集成测试之后，发出merge requst，项目的owner经评估之后，将会及时merge回主分支。


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Travis CI: https://travis-ci.org/dashboard
