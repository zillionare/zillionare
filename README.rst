=====
概览
=====


.. image:: http://images.jieyu.ai/images/hot/zillionworld.jpg

.. image:: https://readthedocs.org/projects/zillionare/badge/?version=latest
        :target: https://zillionare.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT


大富翁是一个模块化、微服务架构的开源AI量化框架，提供行情数据的本地化存储，高速分布式行情服务，回测框架，策略因子，也提供机器学习和深度学习策略模型。


它主要有以下几部分组成：

1. Omicron （可用)
^^^^^^^^^^^^^^^^^^^

Omicron提供了数据的本地存储读写和其它基础功能，比如交易日历和时间，Triggers，类型定义等。

2. Omega (可用)
^^^^^^^^^^^^^^^^^

Omega是基于Sanic构建的微服务，它通过行情适配器来收发数据，通过Omicron来将这些数据存储到本地。Omega也是行情同步任务的管理者。

通过前置Nginx，就可以分布式方式提供行情数据服务。


3. Alpha (开发中)
^^^^^^^^^^^^^^^^^^^^

策略服务器。运行定义的各种策略，并发出交易信号。

4. Epsilon (开发中）
^^^^^^^^^^^^^^^^^^^^
Web控制台

5. Gamma（规划中）
^^^^^^^^^^^^^^^^^^^
交易网关。接收Alpha发出的交易信号，执行交易。这部分也可以集成在Alpha中。


.. important::

    本项目用于统领Zillionare各子项目，主要目的是提供统领性文档、提供帮助信息。如果您现在是在Github上阅读此文档，建议您跳转到`readthedocs <https://zillionare.readthedocs.io/en/latest/>`_阅读，以获得最佳的导航体验。

    除非是协助撰写文档，请不要clone本项目库，也不要通过 ``pip install zillionare`` 来安装本项目。您应该根据自己的需求，安装zillionarer的子项目。

    当前可用的子项目是 `zillionare-omega <https://pypi.org/project/zillionare-omega/>`_ ，提供了高速分布式行情服务。