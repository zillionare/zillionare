# 单元测试

静态语言在编译期就能查出好多错误。对于象Python这样的动态语言，代码lint虽然也能查出许多错误，但只有完全的单元测试，才能较全面的发现错误。

Python当中最主流的单元测试框架有三种，Pytest, nose和Unittest，其中Unittest是标准库，其它两种是第三方工具。在向导生成的项目中，就使用了Pytest来驱动测试。

测试框架的主要功能是，发现和组装测试suite，收集测试报告，提供测试基础设施（断言、mock、setup和teardown等）。

本章主要以标准库unittest为例来讲解如何编写、组织测试用例。一些基本概念在其它框架中也是一样适用的。

## 测试代码的组织

我们一般将所有的测试代码都归类在项目根目录下的tests文件夹中。每个测试文件的名字，要么使用test_*.py，要么使用*_test.py。这是测试框架的要求。如此以来，当我们执行命令如``pytest tests``时，测试框架就能从这些文件中发现测试用例，并组合成一个个待执行的suite。

在test_*.py中，函数名一样要遵循一定的模式，比如使用test_xxx。不遵循规则的测试函数，不会被执行。

一般来说，我们测试文件的组织，应该对应功能代码，即一个模块一个测试文件，如果被测代码有多重文件夹，对应的测试代码也应该按同样的目录来组织。这样做的目的，是为了方便查找对应的测试代码，方便我们添加新的测试用例。

## Unittest

一个常规的Unittest测试文件如下：

```python
import unittest

class TestModuleA(unittest.TestCase):
    def setUp(self)->None:
        # this will be called for every test_foo
        pass

    def tearDown(self)->None:
        # this will be called for every test_foo
        pass

    def test_foo(self):
        pass
```

因为执行测试之前，可能需要做一些初始化工作，测试之后，需要释放资源，所以unittest测试框架为我们准备了setUp和tearDown函数，供我们执行通用的初始化和退出操作，以节省我们自己编写的代码。

上面的代码只适合对同步函数进行测试。如果是异步函数，在Python 3.8之后，我们可以这样写：

```python
import unittest

class TestModuleA(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self)->None:
        pass

    async def asyncTearDown(self)->None:
        pass

    async def test_foo(self):
        pass
```
每个`asyncSetup`会在测试函数之前执行，并且保证它们处于同一个event loop之中。

如果是Python 3.6和Python 3.7，上面的代码虽然执行了，但不会有结果。因为它们不会被放在event loop中调度，执行的结果只是生成了一些协程而已。要使这些测试函数得到执行，必须自己实现wrapper。实现这个wrapper的难点在于，它要把测试函数（比如test_foo)和初始化(setUp)、退出函数(tearDown)包含在同一个event loop之中。由于这些函数都是成员函数，所以这种包装是很困难的。

??? Readmore
    对成员函数写装饰器是很困难的，原因在于self关键字只在运行时才赋值；而装饰器是在模块加载时就执行了，此时一般对象还未生成，也就不存在self。所以给成员函数加装饰器，会导致self无法取值的问题。

正确的做法是使用[aiounittest](https://github.com/kwarunek/aiounittest)这个库，它提供了一个可执行异步测试的基类，当你的测试类继承于这个类时，很显然，也就自然获得了异步测试的能力。

???+ Tips
    对于3.6.1以下的Python版本，任何新的Python工程都没有必要考虑兼容了。特别是在asyncio这一块，语法变化较大，直到3.8才稳定下来。

    实际上，只要有可能，最好只兼容Python 3.8以上的版本，特别是使用了asyncio模块的话。

## Mock

在单元测试时，我们希望测试环境尽可能单纯、可控。因此我们不希望依赖于用户输入，不希望连接数据库或者真实的第三方微服务等。这时候，我们需要通Mock来模拟这些外部接口。

??? Readmore
    感谢容器技术！现在单元测试中，越来越多地连接数据库、缓存和第三方微服务了。因为有一些接口mock的代价，已经超过了launch一个容器，初始化数据库再开始测试了。

在unittest中，我们使用mock这个接口实现上述功能。

```python
import unittest
from unittest import mock

class TestModuleA(unitest.TestCase):
    def test_foo(self):
        with mock.patch('builtins.input', return_value = 'Y') as m:
            self.assertEqual('Y', input('continure or not? [Y]/n'))
```

上面的代码中，我们通过mock拦截了内置的input函数，使得下面对input的调用，变成对mock的调用。又由于我们通过return_value为其指定了返回值为"Y"，所以这个测试可以通过。

我们通过context manager语法，在执行完上面的测试之后，将input调用还原成系统内置函数，从而不影响其它部分的功能。

??? Readmore
    作为一句题外话，象Python这种动态语言要做mock，要比java,c这样的语言容易太多了。对Python使用越多，你就会对单元测试越熟练，从而使得代码质量大为提高。

mock不仅仅能模拟函数调用的返回值，还能模拟异常，这时要通过`side_effect`来指定：

```python

with mock.patch('builtins.input', side_effect = ValueError) as m:
    self.assertRaises(ValueError)
```
上述代码不仅模拟出了一个ValueError，还检测这个异常是否抛出。通过这种方式，异常处理代码现在也可以轻松覆盖到了。

如果我们对mock函数要执行多次调用，则可以分别用``return_values``和``side_effects``来代替``return_value``和``side_effect``。

上面的方法中，我们是完全拦截了某个方法。如果我们只想拦截某个对象的某个方法，而对同类型的其它对象的方法不做拦截，又该怎么做呢？请看下面的示例代码：

```
# foo.py

def bar():
    logger = logging.getLogger(__name__)
    logger.info("please check if I was called")

    root_logger = logging.getLogger()
    root_logger.info("this is not intercepted")

# test_bar.py
from foo import bar

logger = logging.getLogger('foo')
with mock.patch.object(logger, 'info') as m:
    bar()
    m.assert_called_once_with("please check if I was called")
```
两个logger都被调用，但我们只拦截了对应于'foo'的那个logger的`info`方法，结果验证它被调用，且仅被调用一次。

如果被mock的函数是异步的，情况则要复杂一些。在Python 3.8之前，我们使用第三方的库来完成mock，比如[asynctest](https://github.com/Martiusweb/asynctest).在3.8及之后的版本中，引入了AsyncMock。当我们无法判断被mock的对象是异步还是同步时，可以仅使用Mock，3.8版本之后的Mock有能力自己判断应该使用同步的Mock，还是异步的Mock。

对异步的Mock对象，当你通过`await`调用它之后，将获得`return_value`和`side_effect`，然后就可以用上面同样的方法来判断执行结果。





