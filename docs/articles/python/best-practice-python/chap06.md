---
title: 06 10倍速！高效编码
---
# 1. AI赋能的代码编写

传统上，IDE的重要功能之一，就是代码自动完成、语法高亮、文档提示、错误诊断等等。随着人类进入深度学习时代，AI辅助编码则让程序员如虎添翼。

我们首先介绍几个AI辅助编码的工具，然后再介绍常规的语法高亮、文档提示等功能。

## 1.1. github copilot
github copilot是github官方出品的AI辅助编码工具。它是基于大规模语料、超大规模的深度学习模型，结合了大量的编程经验，为开发者提供代码补全、代码片段联想、代码推荐等功能。copilot可以根据用户输入的一行注释，自动生成代码片段甚至整个函数，功能十分强大。

!!! info
    2023年12月，微软把他们基于chatGPT的人工智能搜索引擎技术也称为copilot，它是您在使用bing搜索引擎时，出现的一个对话机器人。Github现在也是微软的资产。

比如，我们写一段注释如下：
```python
# create a fibonacci series up to nth term
```
然后回车，copilot就会写出下面的代码:
```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```
这个函数还有一个尾递归版本，当然copilot也能提供。一般情况下，copilot能提供10个以内的备选答案。

我们再举一个例子，如果有以下注释：
```
设置npm中国加速镜像
```
你会立即得到以下代码：
```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
再也不用记忆这些奇怪的设置了！

我们再试一个例子:

```python
# 读取csv文件，并返回一个数组对象
def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

# 将数组对象转换为json字符串
def to_json(data):
    return json.dumps(data)

# 将json发送到github
def send_json(json_data):
    url = 'https://api.github.com/repos/udacity/ud120-projects/issues'
    headers = {
        'Authorization': ''  # 请填写你的token
    }
    r = requests.post(url, json_data, headers=headers)

def main():
    data = read_csv('foo.csv')
    json_data = to_json(data)
    send_json(json_data)
```
在上述例子中，我们只写了三行注释，copilot自动帮我们填充了代码。在send_json那个方法里，copilot在headers中提示输入'Authorization'字段，并提示这里要给出token，这个填充很有意思，它因为github这个API正好是通过token认证的。当然，由于信息过少，它给的url几乎肯定是错的，这也在情理之中。

比较有意思的是main函数。我只定义了main()方法的函数头，copilot居然自动完成了所有功能的串联，而且应该说，符合预期。

如果上面的例子过于简单，你可以写一些注释，请求copilot为你抓取加密货币价格，通过正则表达式判断是否是有效的邮箱地址，或者压缩、解压缩文件等等。你会发现，copilot的能力是非常强大的。

copilot的神奇之处，绝不只限于上面的举例。作者在实践中确实体验过它的超常能力，比如在单元测试中，自动生成数据序列，或者在生成的代码中，它的错误处理方案会比你自己能写出来的更细腻，等等。但是，要演示那样复杂的功能，已经超出了一本书所以展现的范围了。

这是一些使用者的感言：

!!! quote
    我的一部分工作内容从编写代码转成了策划。作为一个人类可以观察并修正一些代码，不必亲自动手做每一件事。

    我对冗余代码的容忍度变高了。让AI去做重复的工作，把代码写得更详细，可以提高可读性。

    我更愿意重构代码了。对于那些已经能用但写的不够理想的代码，Copilot可以灵活的完成重构，比如把复杂函数拆分或对关键部分抽象化。


所以，Don't fly solo（copilot广告语），如果有可能，当你在代码的世界里遨游时，还是让copilot来伴飞吧。当然，copilot也有其不足，其中最重要的一点是，不能免费使用（学生除外），而且每个月10美金的费用对中国程序员来讲可能并不便宜。不仅如此，目前它只接受信用卡和paypal付款，因此在支付上也不够方便。

## 1.2. tabnine

另一个选项是[tabnine](https://www.tabnine.com/)，与copilot一样，它也提供了从自然语言到代码的转换，以及整段函数的生成等功能。一些评论认为，它比copilot多出的一个功能是，它能基于语法规则在一行还未结束时就给出代码提示，而copilot只能在一行结束后给出整段代码，即copilot需要更多的上下文信息。

tabnine与copilot的值得一提的区别是它的付费模式。tabnine提供了基础版和专业版两个版本，而copilot只能付费使用。tabnine的专业版还有一个特色，就是你可以基于自己的代码训练自己的私有AI模型，从而得到更为个性化的代码完成服务。这个功能对于一些大型公司来说，可能是一个很好的选择。它的另一个优势就是，它在训练自己时只使用实行宽松开源许可证模式的代码，因此，你的代码不会因为使用了tabnine生成的代码，就必须开源出去。

[GPT code clippy](https://github.com/CodedotAl/gpt-code-clippy/wiki)是Github copilot的开源替代品，如果既不能用copilot，也不能使用tabnine，也可以试试这个。不过在我们成文的时候，它还没有提供一个发行版的vscode扩展，只能通过源码安装。

!!!Info
    说到AI辅助编码，不能不提到这一行的先驱 - Kite。Kite成立于2014年，致力于AI辅助编程，于2021年11月关闭。由于切入市场过早，kite的技术路线也必然相对落后一些，其AI辅助功能主要是基于关键词联想代码片段的模式。等到2020年github的copilot横空出世时，基于大规模语料、超大规模的深度学习模型被证明才是最有希望的技术路线。而此时kite多年以来的投入和技术积累，不仅不再是有效资产，反而成为了历史包袱。往新的技术路线上的切换的代价往往是巨大的 -- 用户体验也难免改变，而且新的模型所需要的钞能力，kite也并不具备。

    2021年11月16日，创始人Adam Smith发表了一篇告别演说，对kite为什么没有成功进行了反思，指出尽管Kite每个月有超过50万月活跃用户，但这么多月活跃用户基本不付费，这最终压垮了kite。当然，终端用户其实也没有错，毕竟copilot的付费模式能够行得通。人们不为kite付费，也确实是因为kite还不够好。

    属于kite的时代已经过去了，但正如Adam Smith所说，未来是光明的。AI必将引发一场编程革命。kite的试验失败了，但催生这场AI试验的所有人：投资人，开发团队以及最终用户，他们的勇气和贡献都值得被铭记。

    作为一个曾经使用过kite，也欠Kite一个会员的使用者，我也在此道声感谢与珍重！

尽管AI辅助编程的功能很好用，但仍然有一些场景，我们需要借助传统的工具，比如pylance。pylance是微软官方出品的扩展。vscode本身只是一个通用的IDE框架，对具体某个语言的开发支持（编辑、语法高亮、语法检查、调试等），都是由该语言的扩展及语言服务器（对python而言，有jedi和pylance两个实现）来实现的，因此，pylance是我们在vscode中开发python项目时，必须安装的一个扩展。

它可以随用户输入时，提示函数的签名、文档和进行参数的类型提示，如下图所示：
![](https://images.jieyu.ai/images/2023/01/20230112144603.png)

Pylance在上面提到的代码自动完成之外，还能实现依赖自动导入。此外，由于它脱胎于语法静态检查器，所以它还能提示代码中的错误并显示，这正是到目前为止，像copilot这样的人工智能还做不太好的地方。源码级的查错，使得我们可以尽早修正这些错误，这也正是静态语言程序员认为Python做不到的地方。

![](http://images.jieyu.ai/images/202104/20210413172416.png)

!!! Tips
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

# 2. Type Hint （Type Annotations)

很多人谈到Python时，会觉得它作为一种动态语言，是没有类型检查能力的。这种说法并不准确，Python是弱类型语言，变量可以改变类型，但在运行时，仍然会有类型检查，类型检查失败，就会抛出TypeError：

下面的例子演示了Python中变量是如何改变类型的，以及类型检查只在运行时进行的这一特点：

```python
>>> one = 1
... if False:
...     one + "two" # 这一行不会执行，所以不会抛出TypeError
... else:
...     one + 2
...
3

>>> one + "two"     # 运行到此处时，将进行类型检查，抛出TypeError
TypeError: unsupported operand type(s) for +: 'int' and 'str'
... one = "one "    # 变量可以通过赋值改变类型
... one + "two"     # 现在类型检查没有问题
one two
```

但Python曾经确实缺少静态类型检查的能力，这是Python一直以来为人诟病的地方。毕竟，错误发现的越早，修复成本就越低。但这正在成为历史。

类型注解从python 3.0（2006年，PEP 3107，当时还叫function annotations）时被引入，但它的用法和语义并没有得到清晰定义，也没有引起广泛关注和运用。数年之后，PEP 484（type hints including generics）被提出，定义了如何给python代码加上类型提示，这样，type annotation就成为实现type hint的主要手段。因此，当今天人们提到type annotation和type hint时，两者基本上是同一含义。

PEP 484是类型检查的奠基石。但是，仍然有一些问题没有得到解决，比如如何对变量进行类型注解？比如下面的语法在当时还是不支持的：
```python
class Node:
        left: str
```

2016年8月，PEP 526(syntax for variable annotations)提出，从此，像上文中的注解也是允许的了。

!!! Info
    PEP 526从提出到被接受为正式标准不到1月的时间，可能是最快被接受的PEP之一。

PEP 563 (Postponed Evaluation of Annotations) 解决了循环引用的问题。在这个提案之后，我们可以这样写代码：
```python
from typing import Optional

class Node:
    #left: Optional[Node]  # 这会引起循环引用
    left:   Optional["Node"]
    right:  Optional["Node"]
```
注意到我们在类型Node还没有完成其定义时，就要使用它（即要使用Node来定义自己的一个成员变量的类型），这将引起循环引用。PEP 563的语法，通过在注释中使用字符串，而不是类型本身，解决了这个问题。

在这几个重要的PEP之后，随着Python 3.7的正式发布，社区也开始围绕Type Hint去构建一套生态体系，一些非常流行的python库开始补齐类型注解，在类型检查工具方面，除了最早的mypy之外，一些大公司也跟进开发，比如微软推出了pyright（现在是pylance的核心）来给vscode提供类型检查功能。google推出了pytype，facebook则推出了pyre。在类型注解的基础上，代码自动完成的功能也因此变得更容易、准确，推断速度也更快了。代码重构也因此变得更加容易。

类型检查功能将对Python的未来发展起到深远的影响，可能足够与typescript对js的影响类比。围绕类型检查，除了上面提到的几个最重要的PEP之外，还有：

1. PEP 483（解释了python中类型系统的设计原理，非常值得一读）
2. PEP 544 (定义了对结构类型系统的支持)
3. PEP 591 (提出了final限定符)
以及PEP 561等另外18个PEP。此外，还有PEP 692等5个PEP目前还未被正式接受。

Python的类型检查可能最早由Jukka Lehtosalo推动，Guido，Łukasz Langa和Ivan Levkivskyi也是最重要的几个贡献者之一。Jukka Lehtosalo出生和成长于芬兰，当他在剑桥大学计算机攻读博士时，在他的博士论文中，他提出了一种名为“类型注解”（Type Annotations）的语法，从而一统静态语言和动态语言。最初的实验是在一种名为Alore的语言上实现的，然后移植到Python上，开发了mypy的最初几个版本。不过很快，他的工作重心就完全转移到Python上面来，毕竟，Python庞大的用户群和开源库才能提供丰富的案例以供实践。
   
2013年，在圣克拉拉举行的PyCon会议上，他公布了这个项目，并且得到了与Guido交谈的机会。Guido说服他放弃之前的自定义语法，完全遵循Python 3的语法，即PEP 3107提出的函数注解）。在随后他与Guido进行了大量的邮件讨论，并提出了通过注释来对变量进行注解的方案（不过后来的PEP 526提出了更好的方案）。

在Jukka Lehtosalo从剑桥毕业后，受Guido邀请，加入了Dropbox，领导了mypy的开发工作。

这里也可以看出顶尖大学对待学术研究上的开放和不拘一格。大概在2016年前后，我看到斯坦福的网络公开课上还有讲授ios编程的课，当时也是同样的震撼。一是感叹他们选课之新，二是感叹这种应用型的课程，在国内的顶尖大学里，一般是不会开设的，因为大家会觉得顶尖的学术殿堂，不应该有这么“low”的东西。

在有了类型注解之后，现在我们应该这样定义一个函数：
```python
def foo(name: str) -> int:
    score = 20
    return score

foo(10)
```
foo函数要求传入字符串，但我们在调用时，错误地传入了一个整数。这在运行时并不会出错，但pylance将会发现这个错误，并且给出警告，当我们把鼠标移动到出错位置，就会出现如下提示：

![](https://images.jieyu.ai/images/2023/01/20230114102202.png)

下面，我们简要地介绍一下type hint的一些常见用法：

```python
# 声明变量的类型
age: int = 1

# 声明变量类型时，并非一定要初始化它
child: bool

# 如果一个变量可以是任何类型，也最好声明它为Any。zen of python: explicit is better than implicit
dummy: Any = 1
dummy = "hello"

# 如果一个变量可以是多种类型，可以使用Union
dx: Union[int, str]
# 从python 3.10起，也可以使用下面的语法
dx: int | str

# 如果一个变量可以为None,可以使用Optional
dy: Optional[int]

# 对python builtin类型，可以直接使用类型的名字，比如int, float, bool, str, bytes等。
x: int = 1
y: float = 1.0
z: bytes = b"test"

# 对collections类型，如果是python 3.9以上类型，仍然直接使用其名字：
h: list[int] = [1]
i: dict[str, int] = {"a": 1}
j: tuple[int, str] = (1, "a")
k: set[int] = {1}

# 注意上面的list[], dict[]这样的表达方式。如果我们使用list()，则这将变成一个函数调用，而不是类型声明。

# 但如果是python 3.8及以下版本，需要使用typing模块中的类型：
from typing import List, Set, Dict, Tuple
h: List[int] = [1]
i: Dict[str, int] = {"a": 1}
j: Tuple[int, str] = (1, "a")
k: Set[int] = {1}

# 如果你要写一些decorator，或者是公共库的作者，则可能会常用到下面这些类型
from typing import Callable, Generator, Coroutine, Awaitable, AsyncIterable, AsyncIterator

def foo(x:int)->str:
    return str(x)

# Callable语法中，第一个参数为函数的参数类型，因此它是一个列表，第二个参数为函数的返回值类型
f: Callable[[int], str] = foo

def bar() -> Generator[int, None, str]:
    res = yield
    while res:
        res = yield round(res)
    return 'OK'
    
g: Generator[int, None, str] = bar

# 我们也可以将上述函数返回值仅仅声明为Iterator:
def bar() -> Iterator[str]:
    res = yield
    while res:
        res = yield round(res)
    return 'OK'

def op() -> Awaitable[str]:
    if cond:
        return spam(42)
    else:
        return asyncio.Future(...)

h: Awaitable[str] = op()

# 上述针对变量的类型定义，也一样可以用在函数的参数及返回值类型声明上，比如：
def stringify(num: int) -> str:
    return str(num)

# 如果函数没有返回值，请声明为返回None
def show(value: str) -> None:
    print(value)

# 你可以给原有类型起一个别名
Url = str
def retry(url: Url, retry_count: int) ->None:
    pass

```
此外，type hint还支持一些高级用法，比如TypeVar, Generics, Covariance和contravariance等，这些概念在[PEP484](https://peps.python.org/pep-0484)中有定义，另外，[PEP483](https://peps.python.org/pep-0483/)和[understanding typing](https://github.com/microsoft/pyright/blob/main/docs/type-concepts.md)可以帮助读者更好地理解类型提示，建议感兴趣的读者深入研读。

如果您的代码都做好了type hint，那么IDE基本上能够提供和强类型语言类似的重构能力。需要强调的是，在重构之前，你应该先进行单元测试、代码lint和format，在没有错误之后，再进行重构。如此一来，如果重构之后，单元测试仍然能够通过，则基本表明重构是成功的。

# 3. PEP8 - python代码风格指南
PEP8是2001年由Guido等人拟定的关于python代码风格的一份提案。PEP8的目的是为了提高python代码的可读性，使得python代码在不同的开发者之间保持一致的风格。PEP8的内容包括：代码布局，命名规范，代码注释，编码规范等。PEP8的内容非常多，在实践中，我们不需要专门去记忆它的规则，只要用对正确的代码格式化工具，最终呈现的代码就一定是符合PEP8标准的。在后面的小节里，我们会介绍这一工具 -- black，因此，我们不打算在此处过多着墨。

# 4. Lint工具

Lint工具对代码进行逻辑检查和风格检查。逻辑检查是指象使用了未定义的变量，或者定义的变量未使用，没有按 type hint 的约定传入参数等等；风格检查是指变量命名风格、空白符、空行符的使用等。

Python社区有很多Lint工具，比如Plint, PyFlakes, pycodestyle, bandit, Mypy等。此外，还有Flake8和Pylama这样，将这些工具组合起来使用的工具。

在选择Lint工具时，重要的指标是报告错误的完全度和速度。过于完备的错误报告有时候也不见得就是最好，有时候会把你的大量精力牵涉到无意义的排查中 -- 纯粹基于静态分析的查错，有时也不可避免会出现错误；同时也使得运行速度降低。

## 4.1. flake8

``ppw``选择了flake8和mypy作为lint工具。flake8实际上是一组lint工具的组合，它由pycodestyle, pyflakes, mcccab组成。

### pycodestyle
pycodestyle用来检查代码风格（空格、缩进、换行、变量名、字符串单双引号等）是否符合PEP8标准。

### pyflakes
pyflakes用来检查语法错误，比如，定义但未使用的局部变量，变量重定义错误，未使用的导入，格式化错误等等。人们通常拿它与pylint相对照。pyflakes与pylint相比，所能发现的语法错误会少一些，但误报率更低，速度也更快。在有充分单元测试的情况下，我们更推荐初学者使用pyflakes。

下面是一个pylint报告错误，而pyflakes不能报告的例子：
```
def add(x, y):
    print(x + y)

value: None = add(10, 10)
```
显然，代码作者忘了给add函数加上返回语句，因此，将value赋值为add(10, 10)的结果是None。pylint会报告错误，但是pyflakes不会。

但是pylint存在一定的误报率，上面的代码交给pylint来进行语法检查，其结果是：
```
xxxx:1:0: C0114: Missing module docstring (missing-module-docstring)
xxxx:1:0: C0116: Missing function or method docstring (missing-function-docstring)
xxxx:1:8: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
xxxx:1:11: C0103: Argument name "y" doesn't conform to snake_case naming style (invalid-name)
xxxx:5:0: E1111: Assigning result of a function call, where the function has no return (assignment-from-no-return)
xxxx:5:0: C0103: Constant name "value" doesn't conform to UPPER_CASE naming style (invalid-name)
```
这里第1，2和第5行报告都是正确的。但第3和第4行的报告很难说正确，为了代码的简洁性，我们使用单个字母作为局部变量是很常见的事。PEP8规范也只要求我们不得使用"l"（小写的字母L）, "O"（字母o的大写，很难与数字0区分）, "I"（字母i的大写）。

而最后一行的报告则显然是错误的，这里函数add没有返回值的错误，导致pylint误以为value是一个常量，而不是一个变量。事实上，当你修复掉add函数没有返回值的错误时，pylint就不会报告这个错误了。

这是为什么我们推荐初学者使用pyflakes，而不是pylint的原因。初学者很容易淹没在pylint抛出的一大堆错夹杂着误报的错误报告中，花费大量时间来解决这些误报，却茫然无计。另外，pylint过于严格的错误检查，对还未养成良好编程习惯的初学者，可能会使他们感到沮丧。比如，上面关于缺少文档的错误报告，尽管是正确的，但对初学者来说，要一下子达到所有这些标准，会使得学习曲线变得过于陡峭，从而导致学习的热情降低。

mccabe用来检查代码的复杂度，它把代码按控制流处理成一张图，从而代码的复杂度可以用下面的公式来计算：
$M = E - N + P$，其中E是路径数，N是节点数，P则是决策数。

以下面的代码为例：
```python
if (c1())
    f1();
else
    f2();

if (c2())
    f3();
else
    f4();
```
对应的控制流图可以绘制成为：
![](https://images.jieyu.ai/images/2023/01/20230115111237.png){height="30%"}

上述控制流图中，有9条边，7个结点，1个连接，因此它的复杂度为3。

### mccabe
mccabe的名字来源于Thomas J. McCabe，他于1976年在IEEE上发表了"A Complexity Measure"这篇论文，这篇重要文章，被其它学术论文引用超过8000次，被认为是软件工业领域最重要和最有影响力的论文之一，影响了一代人。33年之后，Thomas J. McCabe于2019年被ACM授予最有影响力论文奖。这个奖一年只授予一次，只有授奖当年11年之前的论文才有资格入选，迄今也只颁发了15届，约40人拿到了这个奖项。

Tom McCabe提出，如果这个复杂度在10以下，该段代码就只是一段简单的过程，风险较低；11-20为中等风险；21-50属于高风险高复杂度；如果大于50，则该段代码是不可测试的，具有非常大的风险。

### flake8的配置
配置flake8，可以在根目录下放置.flake8文件。尽管可以把配置整合到pyproject.toml文件中，多数情况下，我们都推荐使用单独的配置文件，以减少pyproject.toml的复杂度。对后面将提到的其它工具的配置文件，我们也是一样的态度。

.flake8是一个ini格式的文件，以下是一个示例：
```ini title=".flake8"
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

我们排除了对test文件进行lint，这也是flake8开发者的推荐，尽管代码可读性十分重要，但是我们不应该在test代码的风格上花太多宝贵时间。这里最初几行配置，是为了与black兼容。如果不这样配置，那么经black格式化的文件，flake8总会报错，而这种报错并无任何意义。
## 4.2. Mypy
flake8承担了代码风格、部分语法错误和代码复杂度检查的工作。但是，它没有处理类型检查方面的错误，这项工作我们只能留给mypy来完成。

ppw中已经集成了mypy模块，并会在tox运行时，自动进行类型检查。看上去，只要我们按照PEP484及几个关联的PEP来做好类型注解，然后简单地运行mypy，似乎就应该万事大吉？然而，实践总是比理论要丰富得多，深刻得多。mypy在运行检查时，常常会遇到第三方库还不支持类型注解的情况，或者因为配置错误，导致mypy得不到预期的结果。遇到这些问题时，就需要我们理解mypy的工作原理，并且对mypy进行一些配置，以便让它能够更好地工作。

!!! Info
    为什么ppw选择了mypy？如果你使用vscode编程，那么很可能已经使用了pyright作为类型检查器。因为pylance给出的类型检查错误，都来自于pyright。那么ppw为什么还要推荐另一个类型检查器呢？

    这是因为，pyright并不是一个纯粹的python解决方案。要安装pyright，还必须安装node。我们认为，在开发环境下，一般只需要安装一次，而且vscode可以帮我们完成安装。但在由tox驱动的矩阵测试环境中，任何非纯python的解决方案都可能带来额外的复杂性。

首先，让我们从`Any`这个特殊的类型说起。`Any`类型用来表明某个变量/值具有动态类型。在代码中，如果存在过多的`Any`类型，将降低mypy进行代码检查的有效性。

难点在于，`Any`类型的指定，并不一定来源于我们自己代码中的显式声明（对这一部分，我们可以自行修改，只在非常必要时才小心使用`Any`）。在mypy中，它还会自动获得和传播。mypy的规则是，在函数体内的局部变量，如果它们没有被显式地声明为某种类型，无论它们是否被赋初值，mypy都会将其推导为`Any`。而在函数体外的变量，mypy则会依据其初值将其推导为某种类型。mypy这样处理的原因，可能是因为它无法在检查时真正运行这个函数。

我们先看函数体里的变量自动获得`Any`类型的例子：
```python title="test.py"
def bar(name):
    x = 1
    # reveal_type是mypy的一个调试方法，用以揭示某个变量的类型。它仅在mypy检查时才会有定义，并会打印出变量类型。你需要在调试完成后，手动移除这些代码，否则会引起python报告NameError错误。
    reveal_type(x)
    x.foo()
    return name
```
我们将上述代码存为test.py，然后通过mypy来运行检查，我们会得到以下输出：
```
test.py:12: note: Revealed type is "Any"
```
除此之外，并没有其它别的错误。在上述代码中，尽管x被赋值为整数1，但它的类型仍然被mypy推导为`Any`，因此，我们可以在x上调用任何方法，而不会引起mypy的错误提示。

下面的例子，揭示了函数体外的变量，mypy是如何推导其类型的：
```python
from typing import Any

s = 1           # Statically typed (type int)
reveal_type(s)  # output: Revealed type is "builtins.int"
d: Any = 1      # Dynamically typed (type Any)
reveal_type(d)  # output: Revealed type is "Any"

s = 'x'         # Type check error
d = 'x'         # OK
```
其它获得`Any`类型的情况还包括导入错误。当mypy遇到import语句时，它将首先尝试在文件系统中定位该模块或者其类型桩(type stub)文件。然后 Mypy 将对导入的模块进行类型检查。但是，可能存在导入库不存在（比如名字错误、没有安装到mypy运行的环境中），或者该库没有类型注解信息等情况，这样，mypy就会将导入的模块的类型推导为`Any`。

!!! Info
    注意到在第4章中，我们生成的样板工程中，在sample\sample目录下，存在一个名为py.typed的空文件。这个文件会在poetry打包过程中，被复制到打包后的包中。这个文件的作用是，告诉类型检查器(type checker)，这个包中的模块都是具有类型注解的，可以进行类型检查。如果你的包中没有这个文件，那么类型检查器将不会对你的包进行类型检查。

    py.typed并不是mypy的发明，而是PEP 561的规定。所有类型检查器都应该遵循这个规定。

需要注意的是，mypy寻找导入库的方式与python寻找导入库的方式并不完全相同。首先，mypy 有自己的搜索路径。这是根据以下条目计算得出的：

1. MYPYPATH环境变量（目录列表，在 UNIX 系统上以MYPYPATH冒号分隔，在 Windows 上以分号分隔）。
2. 配置文件中的mypy_path配置项。
3. 命令行中给出的源的目录。
4. 标记为类型检查安全的已安装包（请见PEP561）。
5. typeshed repo的相关目录。

其次，除了常规的 Python 文件和包之外，mypy 还会搜索存根文件。搜索模块的规则foo如下：

1. 搜索查找搜索路径（见上文）中的每个目录，直到找到匹配项。
2. 如果找到名为的包foo（即foo包含__init__.py或__init__.pyi文件的目录），则匹配。
3. 如果找到名为的存根文件foo.pyi，则匹配。
4. 如果找到名为的 Python 模块foo.py，则匹配。

规则比较复杂，不过一般情况下，我们也只需要大致了解即可，在遇到问题时，我们可以通过查阅mypy的文档[如何找到导入库](https://mypy.readthedocs.io/en/latest/running_mypy.html#finding-imports)来解决。总之，我们需要了解，如果某个导入库在上面的搜索之后不能找到，mypy就会将该模块的类型推导为`Any`。

除了上述获得`Any`的情况外，mypy还会自动将`Any`类型传播到其他变量上。比如，如果一个变量的类型是`Any`，那么它的任何属性的类型也是`Any`，并且任何对类型为`Any`的调用，也将获得`Any`类型。请看下面的例子：
```python
def f(x: Any) -> None:
    # x具有Any类型，foo是x的一个属性，所以x.foo的类型也是`Any`
    # 既然x.foo的类型是`Any`，那么对x.foo的调用，也将导致mypy将y的类型推导为`Any`
    y = x.foo()  
    y.bar()      # 因此，mypy会认为这个调用是合法的
```

从PEP 484开始建构Python的类型提示大厦，直到PEP 563基本完成大厦的封顶之时，仍有大量的第三方库还不支持类型注解。针对这个现实，Python的类型注解是渐进式的(见PEP 483)，任何类型检查器都必须面对这个现实，并给出解决方案。

Mypy提供了大量的配置项来解决这个问题。这些配置项既可以通过命令行参数传入，也可以通过配置文件传入。

默认地，mypy使用工程目录下的mypy.ini作为其配置文件；如果这个文件找不到，则会依次寻找.mypy.ini（注意前面多一个'.')，pyproject.toml, setup.cfg, $XDG_CONFIG_HOME/mypy/config， \~/.config/mypy/config，最后是\~/.mypy.ini。

一个典型的mypy配置文件包括全局配置和针对特定模块、库的设置，示例如下：
```ini
[mypy]
warn_redundant_casts = true
warn_unused_ignores = true
warn_unused_configs = true

disallow_any_unimported = true
ignore_missing_imports = false

# 禁止未注解的函数、或者注解不完全的函数。
disallow_untyped_defs = true
# 当disallow_untyped_defs为真时，下面的配置无意义
#disallow_incomplete_defs = true
disallow_untyped_calls = true
disallow_untyped_decorators = true
# 不允许使用`x: List[Any]` 或者 x: List`
disallow_any_generics = true

# 显示错误代码
show_error_codes = true

# 如果函数返回值声明不为Any，但实际返回Any，则发出警告
warn_return_any = true

[mypy-fire]
# cli.py中引入了python-fire库，但它没有py.typed文件，这里我们要对该库单独设置允许导入缺失
ignore_missing_imports = true

```

示例中给出的配置项目是我们认为较为重要，并且与默认值不同的那些。关于mypy所有配置项目及其含义可以参考[官方文档](https://mypy.readthedocs.io/en/stable/config_file.html)。这些配置项，既可以通过配置文件设置，也可以通过命令行方式直接传递给mypy。当然，使用命令行方式传递时，这些配置将在全局范围内发生作用。

### 4.2.1. disallow_untyped_defs
默认情况下，mypy的类型检查相当宽松，以便兼容一些陈旧的项目。如果我们想要更严格的类型检查，可以将disallow_untyped_defs设置为true。我们可以来测试一下：
```python title="test.py"
def bar(name):
    return name
```
函数bar没有加任何类型注解，显然，应该无法通过mypy的类型检查。但如果我们在命令行下执行：
```
$ mypy test.py
```
mypy不会给出任何错误提示。如果我们带上--disallow-untyped-defs参数：
```
$ mypy --disallow-untyped-defs test.py
```
这会提示以下错误：
```
test.py:7: error: Function is missing a type annotation  [no-untyped-def]
```
如果是通过配置文件来设置disallow_untyped_defs，象这种布尔量，分别设置为true或false即可。通过命令行传入参数一定是全局生效，而通过配置文件，则可以在更细致的粒度上进行配置。

### allow-incomplete-defs
在上面的配置中，还存在一个名为allow-incomplete-defs的选项，它针对的是函数参数只完成了部分注解的情况。有时候我们需要允许这种情况发生。此时，我们需要mypy仅针对个别场合进行以下配置：
```init
[mypy-special_module]
disallow_untyped_defs = false
allow_incomplete_defs = true
```
### 4.2.2. check_untyped_defs
在下面的代码中，我们把字符串与一个整数相加。这显然并不合理。
```python
def bar()->None:
    not_very_wise = "1" + 1
```
如果存在全局设置disallow_untyped_defs = True。这种情况下，mypy将报告以下错误：
```
error: Unsupported operand types for + ("str" and "int")  [operator]
```
但事事有例外。在例外情况下，我们也可以退而求其次，通过设置check_untyped_defs = True将可以检查出上述问题。
### 4.2.3. disallow_any_unimported和ignore_missing_imports
我们在前面介绍过，如果mypy无法追踪一个导入库，就会将该模块的类型推断为`Any`，从而进一步传播到我们的代码里，使得更多的类型检查无法进行。如果我们想要禁止这种情况，可以将disallow_any_unimported设置为True。该参数的缺省值是false。

一般地，我们应该在全局范围内将disallow_any_unimported设置为True，然后针对mypy报告出来的无法处理导入的错误，逐个解决。在ppw生成的项目中，如果我们选择了fire作为命令行工具，则会遇到以下错误：
```
error: Skipping analyzing 'fire': found module but no type hints or library stubs  [import]
```
一般情况下，如果是知名的第三方库，往往在typeshed上注册过类型存根文件，类型检查器（比如mypy)应该能自动找到。如果是不知名的第三方库，我们可以升级它，看最新版本是否支持，或者在pypi上搜索它的存根库。比如，对`fire`，如果pypi上存在它的存根库，则它的名字一定是`types-fire`，于是我们可以这样纠正上述问题：
```
$ pip install types-fire
```
到成书时为止，fire的开发者并没有上传存根文件。在这种情况下，我们还可以自己写一个`fire.pyi`文件，然后将它放到项目的根目录下。关于如何写.pyi文件，请读者自行搜索。

但如果既找不到合适的存根库，我们也没时间来写pyi文件，那么，我们可以将ignore_missing_imports设置为True，这样mypy就不会报错了。请参考上面的配置文件中的第24~26行，不过，我们应该尽力避免使用这个选项。

### 4.2.4. implicit_optional
如果有以下的代码：
```python
def foo(arg: str = None) -> None:
    reveal_type(arg)  # Revealed type is "Union[builtins.str, None]"
```
我们通过reveal_type得知，mypy将`arg`的类型推导为Optional[str]。这个推导本身没有错，但是，考虑到zen of python的要求， explicit is better than implicit，我们应该将arg的类型声明为`arg: Optional[str]`。从0.980起，mypy默认将implicit_optional设置为Flase（即禁止这样使用），因此，这个选项也没有出现在我们的示例中。

### 4.2.5. warn_return_any
一般情况下，我们不应该让函数返回类型为`Any`（如果真有类型不确定的情况，应该使用泛型）。因此，mypy应该检查这种情况并报告为错误。但是，mypy的缺省配置并不会禁止这种行为，我们需要自行修改。

为了便于理解，我们给出以下错误代码：
```python
from typing import Any

def baz() -> str:
    return something_that_returns_any()

def something_that_returns_any() -> Any:
    ...
```
当warn_return_any = True时，mypy将针对上述代码报告如下：
```
error: Returning Any from function declared to return "str"  [no-any-return]
```

### 4.2.6. show_errors_codes and warn_unused_ignores
当我们使用了type ignore时，我们一般仍然希望mypy能够报告出错误消息（但不会使类型检查失败）。这可以通过设置show_errors_codes = True来实现，显示错误代码。这对于理解错误原因很有帮助。

随着代码的不断演进，有时候type ignore会变得不再必要。比如，我们依赖的某个第三方库，随着新版本的发布，补全了类型注解。这种情况下，针对它的type ignore就不再必要。及时清理这些陈旧的设置是一种良好习惯。

### 4.2.7. inline comment
我们还可以通过在代码中添加注释来控制mypy的行为。比如，我们可以通过在代码中添加`# type: ignore`来忽略mypy的检查。如果该注释添加在文件的第一行，那么它将会忽略整个文件的检查。如果添加在某一行的末尾，那么它将会忽略该行的检查。

一般我们更倾向于指定忽略某个具体的错误，而不是忽略整行检查。其语法是 `# type: ignore[<error-code>]`。

# 5. Formatter工具
Formatter工具也有很多种，但是我们几乎没有去考查其它的formatter，就选择了black，只因为它的logo:
<figure>
    <img src="https://images.jieyu.ai/images/2023/01/20230116214626.png" width="250"/>
    <figcaption> The Uncompromising Code Formatter</figcaption>
</figure>

与其它Formatter工具提供了体贴入微的自定义配置不同，Black坚持不让您做任何自定义（几乎）。这样做是有道理的，允许定制只会让团队陷入到无意义地争辩当中，而风格并无对错，习惯就好。我们常常看到在团队里，一些人为代码风格争论，其实他们反对的并不是某种风格本身，他们只是在反对自己的同事而已。

当然Black还是开了一个小窗口，允许你定义代码行的换行长度，Black的推荐是88字符。有的团队会把这个更改为120字符宽，按照阴谋论的观点，幕后的推手可能是生产带鱼屏的资本力量。

在ppw生成的项目中，我们把black的设置放在pyproject.toml中：
```toml title="pyproject.toml"
[tool.black]
line-length = 88
include = '\.pyi?$'
```

另外一个值得一提的工具是isort。它的作用是对代码中的import语句进行格式化，包括排序，将一行里的多个导入拆分成每行一个导入；始终把导入语句置于正式代码之前等等。通过 ppw向导生成的项目，这个工具也开箱即用的：
```toml title="pyproject.toml"
[tool.isort]
profile = "black"
```
这里的配置是防止isort与black相冲突。实际上flake8、black和isort都的配置需要精心同步才能避免冲突。一时发生冲突，就会出现这样的情况，被A工具改过的代码，又被B工具改回去，始终无法收敛。

比较遗憾的是，在vscode下没有一个好的工具可以自动移除没有使用的导入。Pycharm是可以做到这一点的。开源的工具中有可以做到这一点的，但是因为容易出错，这里也就不推荐了。

在vscode中，Lint工具可以检查出未使用的导入，然后您需要手动移除。移除未使用的`import`是必要的，它可以适当加快程序启动速度，降低内存占用，并且避免导入带来的副作用。

!!! Tips
    导入不熟悉的第三方库可能是危险的！一些库会在全局作用域加入一些可执行代码，因此当你导入这些库时，这些代码就会被执行。

# 6. pre-commit hooks

我们把[pre-commit hooks](https://pre-commit.com)放在这一章里介绍，是因为高效的编码也必须是正确的编码。有时候我们会觉得国内的公司不需要计划和文档，需求、设计和编码各方之间不需要反复协商和沟通，一个指令下来，就很快得到执行。这被认为是执行力强，是一大体制优势，但这些“执行力”强的公司，却又累得要死。方向不正确，累死又有何益？

pre-commit是一个python包，可以通过pip安装：
```
$ pip install pre-commit
```
pre-commit安装后，会在你的项目目录下创建一个.git/hooks目录，里面有一个pre-commit文件。这个文件是一个shell脚本，它会在你执行git commit命令时被调用。pre-commit hooks的作用是在你提交代码之前，对代码进行检查，如果有错误，就会阻止你提交代码，从而保证代码库不被这些错误的、不合规范的代码污染。

如果使用向导生成项目的话，向导已经为您安装了pre-commit hooks,当您运行``git commit``命令时，就会看到这样的输出：

![](http://images.jieyu.ai/images/202104/20210413181638.png)

可以看出，pre-commit hooks对换行符进行了检查和修复，调用black进行了格式化，以及调用flake8进行了查错，并报告对f-string的错误使用。

当出现错误时，您必须进行修复后，才能进行再次提交。

## 6.1. pre-commit hooks的配置
在ppw生成的项目中，我们已经集成了这些配置：
```yaml
repos:
-   repo: https://github.com/Lucas-C/pre-commit-hooks
    rev: v1.1.13
    hooks:
    -   id: forbid-crlf
    -   id: remove-crlf
    -   id: forbid-tabs
        exclude_types: [csv]
    -   id: remove-tabs
        exclude_types: [csv]
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0
    hooks:
    - id: trailing-whitespace
    - id: check-merge-conflict
    - id: check-yaml
      args: [--unsafe]
    - id: end-of-file-fixer
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.10.1
    hooks:
    - id: isort
-   repo: https://github.com/ambv/black
    rev: 22.3.0
    hooks:
    - id: black
      language_version: python3.8
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.9.2
    hooks:
    -  id: flake8
       additional_dependencies: [flake8-typing-imports==1.10.0]
       exclude: ^tests
-   repo: local
    hooks:
    -   id: mypy
        name: mypy
        entry: mypy
        exclude: ^tests
        language: python
        types: [python]
        require_serial: true
        verbose: true
```
第一组是pre-commit提供的开箱即用的钩子。首先，它禁止使用windows的换行符，并且将windows的换行符都替换为unix/linux下的换行符。这么做的原因是，如果文件使用unix/linux下的换行符，这些文件基本上都能被windows下的编辑软件正确处理；反之则不然。比如，如果你有一个bash或者perl脚本，但使用了windows换行符，那么，它将不能在unix/linux下运行。

其次，它禁止在文件中使用tab键，并且将tab键替换为空格。从语法上看，只要不混合使用tab键和空格键，这两种方式都是可以的。但是，不同的编辑器（特别是unix/linux下）在对文件进行视觉呈现时，会将tab键展开成不同的宽度，这使得同一份文件，在不同的编辑器里，看上去并不一致，而如果使用space，则不会有这个问题。此外，只使用空格还有另外一个好处，就是赚钱更多：根据stackoverflow对2.8万名专业开发者（排除了学生）的调查，使用空格的开发者的薪资总体上要比使用Tab键的开发都高8.6%。这项报告发表在stackoverflow的2017年6月5日的[博客](https://stackoverflow.blog/2017/06/15/developers-use-spaces-make-money-use-tabs/)。

需要注意的是，并非所有的文件中的tab键被需要被替换。典型的例子是在csv文件中，我们可能使用Tab键作为字段之间的分隔符，因此它们必须被保留。因此在上述配置中，我们将csv文件排除在外。

第二组仍然是pre-commit提供的开箱即用的钩子。它首先移除了行尾的多余的空格。关于为什么要移除行尾多余的空格，在PEP8中有简要地说明。然后它检查是否存在未完成合并的代码文件，检查yaml文件是否合乎规范。
    
注意到这里有一个end-of-file-fixer钩子，这个钩子的作用是，在文件末尾添加一个仅含换行符的空行。相信很少有人真正理解它的含义。实际上，相关的问题在quora和stackoverflow上有很多提问，答案也莫衷一是。

其中一个说法是，POSIX标准中，对一行文本的定义就是零个或多个非换行符加上终止换行符的序列。因此，如果一行文本不以换行符结尾，它就可能被各种工具当成二进制文件。但这并不能解释为什么我们需要给文件末尾添加一个空行。
    
作者更倾向于这种观点：这主要是为了照顾使用Unix和Linux的人。如果你用vi打开一个文件，想在后面添加一些新的内容，如果该文件以一个空行结尾，那么Ctrl+G就可以直接跳转到文件结尾，立即开始工作。反之，Ctrl+G只能跳到最后一行的开头。

另外一个原因是，如果你想使用cat拼接几个文件文件，如果文件都不是以空行（带换行符）结尾，那么前一个文件的最后一行将会与后一个文件的第一行混合在一起，而不是像期待的那样，各占一行。
    
在文件尾加上一个空行并不是什么重要的功能，只是unix/linux生态圈里几乎所有的工具都是这么运作的。我们尊重这个习惯就好。

接下来都是在pre-commit中调用第三方工具实现相关功能的配置。我们配置了isort，black， flake8和mypy。

mypy的配置有点与众不同。它没有使用远程的repo，而是使用了local。mypy官方并没有提供与pre-commit的集成，所以我们采用了直接在pre-commit中调用本地mypy命令的方法。

这一章的主题是高效编码。我们先是介绍了代码自动完成工具，然后讲述了如何利用语法检查工具尽早发现并修复错误，避免把这些错误带入到测试甚至生产环境中。在我们介绍的方案中，语法检查是随着您的coding实时展开的，并在向代码库提交时，强制执行一次检查。后面您还会看到，在运行测试时，还会再做一次检查，通过这样分层式的设防与检查，帮助您的项目避免出现重大错误。
