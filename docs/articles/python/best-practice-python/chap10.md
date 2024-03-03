---
title: 10 撰写技术文档
---

所有好的产品都应该有一份简洁易读的使用说明书，除了苹果。苹果用户天生就知道如何使用他们的产品，因此完全不需要文档。这是真的，几乎所有的苹果产品，都没有用户说明书。

但是对于软件来说，其复杂性往往要求必须有与之配套的详尽的技术文档，使用者才好上手。即使是开源产品，人们通常也是首先借助产品的技术文档快速上手。在一个速食时代，如果不是逼不得已，谁有时间去一行一行地看代码呢？

既然技术文档如此重要，那么，如何写好技术文档，有哪些工具可以帮助我们进行文档创作，好的技术文档有哪些评价标准，其评价标准能否象软件一样进行量化？

作者认为，除了要求技术作者本身有较好的文笔之外，一个好的技术文档常常还包括以下技术要求：

1. 规范的文档结构，简洁优美的格式
2. 内容准确无误：包括文档版本与代码实现始终保持一致（多版本）
3. 提供必要的导航和交叉引用，帮助读者进一步阅读，并且无死链
4. 文档在线托管，随时可阅读和可搜索
5. 在必要时能够生成各种格式，比如 html, PDF, epub 等。

这篇文章将探索常见的文档构建技术栈。作者的重点不在于提供一份大而全的操作指南，而在于探索各种可能的方案，并对它们进行比较，从而帮助您选择自己最适合的方案。至于如何一步步地应用这些方案，文章也提供了丰富的链接供参考。

通过阅读这一章，您将了解到：

1. 文档结构的最佳实践
2. 文档构建的两大门派
3. 如何自动生成 API 文档
4. 如何使用 GitHub Pages 进行文档发布
## 1. 技术文档的组成
一份技术文档通常有两个来源：一是我们在写代码的过程中按照一定风格进行注释，通过工具将其提取出来形成的所谓 API 文档，这部分文档深入到细节之中；二是在此之外，我们特别撰写的帮助文档，相比 API 文档，它们更加宏观概要，涵盖了 API 文档中不适合提及的部分，比如整个软件的设计理念与原则、安装指南、License 信息、版本历史、涵盖全局的示例等等。

时至今日，在 Python 世界里，大致有两种流行的技术文档构建技术栈，即 sphinx 和 mkdocs。下面是基于 sphinx 技术栈构建的一份文件清单：
```
.
├── AUTHORS.rst
├── CONTRIBUTING.rst
├── HISTORY.rst
├── LICENSE
├── README.rst
├── docs
│   ├── conf.py
│   ├── Makefile
│   ├── make.bat
│   └── index.rst
└── Makefile
```
这个布局是《[Python 最佳实践指南](https://docs.python-guide.org/writing/structure/)》一书中推荐的，它的最初出处是 [Knnedth Reitz](https://kennethreitz.org/essays/repository-structure-and-python) 在 2013 年推荐的一个 Python 项目布局的最佳实践，为适应开源项目的需要，我在这里增加了 CONTRIBUTING.rst 和 AUTHORS.rst 两个文件。其特点是，文档的类型是 rst 文件，文档目录下包含了一个 conf.py 的 python 文件和一份 Makefile 文件。

!!! Info
    Knnedth Reitz 是一名软件架构师，著名的 Python 库 requests 的作者，他的 Python ORM 库 records，以及虚拟环境管理工具 PipEnv 也同样广受欢迎。他致力于设计高度抽象、降低认知负担和易于使用的软件。

如果你使用 [Cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) 来生成项目的框架，你会发现它生成的项目正好就包括了这些文件。

另一条技术路线则是 mkdocs。这也正是 ppw 所采用的技术路线。尽管第 4 章已经给出了一个完整的文件清单，但为了便于读者理解，在这里我们还是给出一个经过精简的、仅与文档构建相关的清单如下：

```txt
.
├── AUTHORS.md
├── CONTRIBUTING.md
├── HISTORY.md
├── LICENSE
├── README.md
├── docs
│   ├── api.md
│   ├── authors.md
│   ├── contributing.md
│   ├── history.md
│   ├── index.md
│   ├── installation.md
│   └── usage.md
└── mkdocs.yml
```

这条技术路线使用 markdown 的文件格式，由 mkdocs.yml 提供主控文档和配置，除此之外，并不需要别的配置。

首先，我们来介绍下 rst 和 markdown 两种文档格式。

## 2. 两种主要的文档格式
技术文档一般使用纯文本格式的超集来书写。常见的格式有 [reStructuredText](https://docutils.sourceforge.io/rst.html)（以下称为 rst) 和 [Markdown](https://zh.wikipedia.org/zh-hans/Markdown)。前者历史更为久远，语法复杂，但功能强大；后者比较新颖，语法十分简洁，在一些第三方插件的支持下，功能上也已逐渐追赶上来。
## 3. reStructured Text
这一节我们简要地介绍 reStructured Text（以下简称为 rst）的常用语法。如果读者有兴趣全面了解 rst 的语法，可以参考 [reStructuredText 官方文档](https://docutils.sourceforge.io/docs/user/rst/quickref.html)。
### 3.1. 章节标题 (section)
在 rst 中，章节标题是通过文本加上等数量的下缀标点（限#=-~:'"^_*+<>`) 来构成的。示例如下：

```rst
一级标题
####

restructured text example

1. 二级标题
=====

1.1 三级标题
-------

1.1.1 四级标题
^^^^^^^^^

1.1.2 四级标题
^^^^^^^^^
1.1.1.2.1 五级标题
+++++++++++++

1.1.1.2.1.1 六级标题
***************
1.2 三级标题
-------
```
上述文本将渲染为以下格式：

![](https://images.jieyu.ai/images/2023/12/rst_headings.png){width="50%"}

这种语法的烦琐和难用之处在于，标题字符数与下面的标点符号数必须匹配。如果使用了非等宽字符（比如使用了中文标题），匹配将十分困难，您可以自行寻找一个支持 rst 的编辑器（比如在 vscode 中，安装"RST Preview"扩展），手动键入上面的例子，验证这一点。

除了在输入上不够简洁外，标题的级别与符号无关，而只与符号出现的顺序有关，也是容易出错的地方。使用者必须记住每个符号与标题级别的对应关系，否则生成的文档就会出现标题级别错误。
### 3.2. 列表 (list)
在 rst 中，使用*,-,+做项目符号构成无序列表；有序列表则以数字、字母、罗马数字加上'.'或者括号来构成。请见以下示例：
```
*   无序 1
*   无序 2

-   无序 1
-   无序 2

+   无序 3

1.  有序 1
2.  有序 2

2)  有序 2)
3)  有序 3）

(3) 有序 (3)
(4) 有序 (4)

i.  有序 一
ii.  有序 二

II.  有序 贰
III.  有序 叁

c.  有序 three
d.  有序 four
```
示例中，有序列表可以使用右括号，或者完全包围的括号，但不能只使用左括号。上述示例显示如下：

![](assets/img/chap10/rst_list.png){width="50%"}

### 3.3. 表格
rst 核心语法支持两种表格表示方法，即网格表格和简单表格。网格表格就是使用一些符号来构成表格，如下所示：
```txt
+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+---------------------+
```
这样制表显然十分烦琐，不易维护。简单表格在此基础上做了一些简化，不再要求列之间插入竖线进行分割，但是功能又受到限制。于是 rst 通过指令语法，扩展出来 csv 表格和 list 表格。下面是 csv 表格一例：
```
.. csv-table:: 物理内存需求表
    :header: "行情数据","记录数（每品种）","时长（年）","物理内存（GB）"
    :widths: 12, 15, 10, 15

    日线，1000,4,0.75
```
这里 1-3 行是指令，第 5 行则是 csv 数据。上面的语法将生成下面的表格：

![](assets/img/chap10/rst_csv_to_table.png){width="50%"}

相比较而言，这种语法在输入大量数据的情况下，会简单不少。

### 3.4. 图片
在文档中插入图片要使用指令语法，例如：
```
.. image:: img/p0.jpg
    :height: 400px
    :width: 600px
    :scale: 50%
    :align: center
    :target: https://docutils.sourceforge.io/docs/ref/rst/directives.html#image
```
示例在文档中插入了 img 目录下的 p0.jpg 图片，并且显示为 400px 高，600px 宽，缩放比例为 50%，图片居中对齐，点击图片会跳转到指定的链接。

### 3.5. 代码块
在文档中插入代码块要使用指令语法，例如：
```
.. code:: python

  def my_function():
      "just a test"
      print 8/2
```

### 3.6. 警示文本
警示文本通常用于强调一些重要的信息，比如提示错误 (error)、重要 (important)、小贴士 (tip)、警告 (warning)、注释 (note) 等。

同样我们用指令语法来显示警示文本，例如：

```
.. DANGER::
   Beware killer rabbits!
```
显示如下：

![](assets/img/chap10/rst_admonition.png "警示文本"){width="50%"}

此外还有一些常用的语法，比如对字体加粗、斜体显示，显示数学公式、上下标、脚注、引用和超链接等。要介绍完全部 rst 的语法，已经远远超出了本书的范围，感兴趣的读者可以参考 [官方文档](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html)。关于 rst，我们要记住的是，尽管语法繁琐，但它提供了非常强大的排版功能，不仅可以用来写在线文档，还可以直接付梓成书，这一点，目前仅有 latex 可以媲美。

## 4. Markdown
Markdown 起源于 2000 年代。在 2000 年前后，John Gruber 有一个博客，叫 [勇敢的火球 (Daring Fireball)](https://daringfireball.net)。当时在线编辑工具还没有现在这样发达，网页文本的格式化功能还需要通过 HTML 代码来实现。尽管他本人完全掌握 HTML 的语法，但感觉这种语法肯定不适用大多数人，于是萌生了发明一种简化的标记语言 (markup) 的想法。这种语言要比 HTML 简单，但能转换成 HTML。最终，在借鉴了纯文本电子邮件标记的一些惯例，以及 Setext 和 atx 形式的标记语言的一些特点后，他于 2004 年发明了 Markdown 语言，并发布了第一个将 markdown 转换成 HTML 的工具。

在 2007 年，GitHub 的开发者 Chris Wanstrath 接触到了 Markdown 语言。在 2014 年，GitHub 宣布，将会在 GitHub 上使用 Markdown 语言来编写文档。这一举动，使得 Markdown 语言更加流行起来。Markdown 的核心语法非常简单，只有几十个规则，仍有一些常用的格式无法实现，于是 Github, Reddit 和 Stack Exchange 对 Markdown 做了一些自己的扩展，这些扩展被称为"风味"(Flavors)，比如 Github Markdown Flavor，就增加了表格、代码段等。这些扩展大大增强了 Markdown 的表达能力。

!!! Readmore
    象 Github, Reddit 这样的大玩家染指 Markdown 之后，Markdown 的标准化问题就出现了。2014 年，加州大学的哲学教授 John MacFarlane， Discourse 的联合创始人 Jeff Atwood，以及 Reddit, Github， Stackoverflow 的代表共同组成了一个工作组，开始了 Markdown 的标准化工作。出人意料的是，Markdown 的创始人 John Gruber 反对 Markdown 的标准化工作，并禁止他们使用 Markdown 这个名字，最终，这个标准化的结果就变成了 [commonmark](https://commonmark.org)，被认为是一个事实上的标准。

    John Gruber 反对 Markdown 的标准化工作，并且不允许工作组使用 Markdown 这个名字，不能不说令人遗憾。不知道这能不能算是屠龙少年终成龙的另一个实例。不过，在技术界这也并非孤例。一些人也认为，解决 Python 性能问题的最大阻碍，其实就来自于创建者 Guido，因为他认为 Python 的性能已经够好：如果有人认为 Python 性能不够好，那么他应该改用别的语言。提升 Python 语言的性能的过程中，决不允许出现版本 2 到版本 3 升级时的那种不兼容现象。

下面，我们就结合例子来看看 Markdown 的语法。注意，这里我们没有严格区分哪些是核心语法，哪些是 commonmark 扩展的语法，因为到目前为止，commonmark 的扩展已经为大多数编辑器所支持了。
### 4.1. 章节标题
Markdown 的章节标题使用'#'来引起，‘#’的个数表示标题的级别，例如：
```txt
# 1. 这是一级标题
## 1.1 这是二级标题
### 1.1.1 这是三级标题
### 1.1.2 另一个三级标题
## 1.2 另一个二级标题
```
可以看出，这比 rst 要直观、易记忆和简洁。在示例中，我们给标题进行了手工编号。这不是必须的，许多 Markdown 渲染工具都可以通过 css 来自动给标题加上编号。另外，很多 Markdown 编辑器也具有给标题自动插入和更新编号的能力。

### 4.2. 列表
Markdown 的列表与 rst 差不多，无序列表使用'-'或者'*'引起，例如：
``` {linenums="0"}
- 无序列表 1
- 无序列表 2
```
最终渲染的效果如下所示：

- 无序列表 1
- 无序列表 2

有序列表使用数字加'.'引起，例如：
```
1. 有序列表 1
3. 有序列表 2
```
最终渲染的效果如下所示：

1. 有序列表 1
2. 有序列表 2
   
注意，在上面的示例中，我们给有序列表的序号并不是连续的。在 markdown 语法中，并不在意我们给出的数字是多少，markdown 的渲染工具最终都会自动帮我们调整正确。这是一个非常好的功能。

### 4.3. 表格

与 rst 相比，markdown 的表格语法还是稍嫌复杂：
```
| Header1 | Header2 | Header3 |
| :------ | :-----: | ------: |
| data1   |  data2  |   data3 |
| data11  | data12  |  data13 |
```
语法的特点是，表格的每一行都是以'|'开头和结尾的，每一列的数据之间用'|'分隔，表头和表格的分隔线使用'-'表示。表头和表格的分隔线的数量可以不一致，但是必须大于等于表格的列数。表格的渲染效果如下：

| Header1 | Header2 | Header3 |
| :------ | :-----: | ------: |
| data1   |  data2  |   data3 |
| data11  | data12  |  data13 |

注意上述表格语法中的冒号。它在这里的作用是指示该列的对齐方式。当在分隔线的左侧使用一个冒号时，该列为左对齐；如果在分隔线的右侧使用一个冒号时，该列为右对齐；如果在两端同时使用冒号，则该列为居中对齐。在不使用冒号的情况下，该列为左对齐。

markdown 没有 rst 那样的指令语法，因此对超出核心语法的特性，扩展并不容易。作为一个例子，在 markdown 中不能直接将 csv 数据渲染为表格。如果我们对在 markdown 中制作表格感到困难，一般的作法是通过编辑器的扩展功能，将 csv 数据转换为 markdown 的表格。

!!! Tip
    vscode 中有扩展可以实现这一功能。
### 4.4. 插入链接
在 markdown 中插入链接很简单，语法如下：
```
[链接名](https://example.com)
```
即由符号"\[\]\(\)"定义了一个链接，其中"[]"中是链接的显示文字，"()"中则是链接的 target。
### 4.5. 插入图片
插入图片的语法与插入链接类似：
```
![alt text](image url "image Title")
```
不同的是，图片链接必须由一个感叹号引起。'[]'中的文字此时成为图像的替代文本，屏幕阅读工具用它来向视觉障碍读者描述图像。'()'中的文字则是图像的 URL，可以是相对路径，也可以是绝对路径。最后，还可以加上一个双引号，其中的文字则是图像的标题，鼠标悬停在图像上时会显示出来。

下面是一个示例：
```
![这是一段警示文本](img/markdown.png)
```
生成效果如下：

 ![](assets/img/chap10/markdown_logo.png "警示文本示例"){width="50%"}

 markdown 核心语法不能象 rst 那样支持指定宽度和高度、对齐方式等。如果我们有这些需要，一般有两种方式可以解决。一是我们可以使用 html 语法来实现，例如：
 ```
 <img src="img/markdown.png" width="30%">
 ```
 效果如下图所示：
![](assets/img/chap10/markdown.png){width="30%"}

二是可能您使用的 markdown 编辑器支持扩展语法。本文撰写时，就使用了 Mkdocs-Material 中的相关扩展功能，下面的例子是它的用法举例：
```
 ![](assets/img/chap10/markdown_logo.png "警示文本示例"){width="30%"}
```
### 4.6. 代码块
我们使用三个反引号'`'来定义代码块，例如：
```
    ```python
        def foo():
            print('hello world')
    ```
```
起头的反引号之后，可以加上语言定义。如此以来，代码块就可以获得语法高亮了。上面的代码块，我们使用了'python'作为语言定义，这样代码块就会获得 python 的语法高亮，如下所示：
```python
    def foo() -> None:
        print('hello world')
```
### 4.7. 警示文本
在 markdown 中，我们可以用三个感叹号来引起警示文本，语法如下：
```
!!! type "双引号定义标题"
    Any number of other indented markdown elements.

    This is the second paragraph.
```

这是 commonmark 的扩展语法。感叹号后面的英文单词是警示文本的类型，commonmark 并没有限定有哪些类型。在实现上，这些类型都是 css 的一个 class，因此具体显示效果如何实现，取决于渲染器的决定。比如，本书的网页版使用了 mkdocs-material 主题，material 支持的类型有 note, abstract, info, tip, success, question, warning, example, quote 等。如果使用了不在上述列表之中的类型，mkdocs-material 就会使用默认的样式来显示这段警示文本。

比如，下面是引用它人文字的一例：
```
    !!! quote "罗曼. 罗兰"
        世上只有一种英雄主义，就是认清生活的真相之后依然热爱生活。
```
其效果如下：

!!! quote "罗曼. 罗兰"
    世上只有一种英雄主义，就是认清生活的真相之后依然热爱生活。

人的生物学进化是以千年为单位，但我们的社会却早就进入了信息爆炸，信息过载的时代，这是现代人感觉活得很累的原因之一。在我们编写技术文档时，应该多多使用 admonition 这样的样式，把文章的重点提示出来，以减轻阅读负担；同时，它图形化的排版也给略显呆板的文字，带来一抹轻松的色彩。

### 4.8. 其它语法
两个'\*\*'之间的文本将显示为加粗，两个'\_'之间的文本将显示为 _斜体_（也可以使用两个'\*'包含文本）。如果文本被包含在两组'\*\*\*'之中，则文本将以 ***加粗+斜体***方式显示。

行内数学公式使用一对'\$'包含，例如：\$x\^2\$，这将显示为：x<sup>2</sup>。这里我们还演示了上标的用法，即使用'^'。如果是要生成下标，则可以用'_'，例如：\$x\_2\$，这将显示为：x<sub>2</sub> 。

我们在介绍插入图片的语法时提到，有一些特性，比如指定宽度，markdown 核心语法不支持，我们可以使用 html 语法。这不仅仅对图片适用。实际上，在 markdown 文档的任何地方，我们都可以使用 html 来增强显示效果。由于 html 语法支持上下标，因此，我们也可以用 html 语法来重写上面的例子。上下标可以使用 html 的<sup>和<sub>标签来实现，比如 x<sup>2</sup>将显示为 x^2。H<sub>2</sub>O 将显示为下标 H_2 O。

上下标可以使用 html 的、<sup\>和、<sub\>标签来实现，比如 x\<sup\>2\</sup\>将显示为 x<sup>2</sup>。H\<sub\>2\</sub\>O 将显示为下标 H<sub>2</sub>O。

## 5. Sphinx vs Mkdocs：两种主要的构建工具

rst 和 markdown 都是伟大的发明，它使得我们可以基于文本文件格式来保存信息，即使不依赖任何商业软件，我们也可以编辑、阅读这些文档。试想，如果我们把大量的文档信息保存在 word 这种商业软件中，一旦有一天商业软件终止服务、或者提高收费标准，这种技术锁定效应将带来多大的迁移成本？！

但是，rst 和 markdown 毕竟只是简单文本格式，直接阅读，视觉效果并不好。此外，大型文档往往由多篇子文档组成，因此我们也需要有能把文档组织起来的工具，以便向读者提供目录和导航等功能。这就引出了文档构建工具的需求。

文档构建工具的主要作用，就是将散落在不同地方的文档统合起来，呈现一定的结构，文档各部分能够相互链接和导航，并且将简单文本格式渲染成更加美观的富文本格式。在 Python 的世界中，最重要的文档构建工具就是 Sphinx 和 Mkdocs。

[Sphinx](https://www.sphinx-doc.org/en/master/) 是始于 2008 年 5 月的一种文档构建工具，当前版本 7.2。其主要功能是通过主控文档来统合各个子文档，生成文档结构 (toctree)、API 文档，实现文档内及跨文件、跨项目的引用，以及界面主题功能。

在早期的版本中，Sphinx 并没有生成 API 文档的功能，我们需要通过第三方工具，比如 sphinx-apidoc 来实现这一功能。大约从 2018 年起，Sphinx 通过 autodoc 这一扩展来实现了生成 API 文档的功能。现在的项目中，已经没有必要再使用 sphinx-apidoc 这一工具了（注：在 cookiecutter-pypackage 生成的项目中，仍然在使用 sphinx-apidoc 这一工具）。

[intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) 是其特色功能，它允许你在两个不同的文档中相互链接。比如，你在自己的项目中重载了 Python 标准库中的某个实现，并已经对新增的功能撰写了文档，但对于未做改变的那部分功能，你并不希望将它的帮助文档重写一遍，这样就有了链接到 Python 标准库文档的需求。比如，通过 intersphinx，你可以使用 _\:py\:class:\`zipfile.ZipFile\`_ 来跳转到 Python 标准库的`ZipFile`类的文档上。虽然也可以直接使用一个 HTML 超链接来实现这样的跳转，但毫无疑问，intersphinx 的语法更为简洁。

[Mkdocs](https://www.mkdocs.org) 出现于 2014 年，当前版本 1.5。除了构建项目文档外，Mkdocs 还可以用来构建静态站点。在构建项目文档方面，它主要提供文档统合功能、界面主题和插件体系。与 Sphinx 相比，它提供了**更好的实时预览能力**。Sphinx 自身没有提供这一能力，有一些第三方工具（比如 vscode 中的 rst 插件，提供了单篇文章的预览功能。

这两种文档构建工具都得到了文档托管平台 [readthedocs](https://readthedocs.org/) 和 git pages 的支持。在多数情况下，作者更推荐使用 mkdocs 及 Markdown 语法，这也是 ppw 正在使用的技术路线。
## 6. 使用 Sphinx 构建文档
### 6.1. 初始化文档结构

在安装 sphinx 之后，通过下面的命令来初始化文档：

``` bash
$ pip install sphinx 

# 此命令必须在项目根目录下执行！
$ shpinx-quickstart

```
Sphinx 会提示你输入项目名称、作者、版本等信息，最终生成 docs 目录及以下文件：
```
docs/
docs/conf.py
docs/index.rst
docs/Makefile
docs/make.bat
docs/_build
docs/_static
docs/_templates
```
如果文档中使用了图像文件，应该放在_static 目录下。

现在运行 ``make html``就可以生成一份文档。你可以通过浏览器打开``_build/index.html``来阅读，也可以通过``python -m http.server -d _build/index``，然后再通过浏览器来访问阅读。

### 6.2. 文件重定向

我们一般把 README.rst, AUTHOR.rst, HISTORY.rst 放在项目的根目录下，即与 Sphinx 的文档根目录同级，这是 Python 项目管理的需求，也是像 Github 这样的托管平台的惯例。而按 Sphinx 的要求，文档又必须放置在 docs 目录下。我们当然不想同样的文件，在两个目录下各放置一份拷贝。为解决这个问题，我们一般使用``include``语法，来将父目录中的同名文件包含进来。比如上述 index.rst 中的 history 文件：

```
# CONTENT OF DOCS/HISTORY.RST

.. include:: ../HISTORY.rst
``` 
这样就避免了同一份文件，出现多个拷贝的情况。

### 6.3. 主控文档和工具链

如果您是通过 Sphinx-quickstart 来进行初始化的，它的向导会引领您进行一些工具链的配置，比如象配置 autodoc（用于生成 API 文档）。为了完备起见，我们还是再提一下这个话题。

Sphinx 在构建文档时，需要一个主控文档，一般是 index.rst:

```

文档 Title
==========

.. toctree::
   :maxdepth: 2

   deployment
   usage
   api
   contributing
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

Sphinx 通过主控文档，把单个文档串联起来。 上面的 toctree 中的每一个入口（比如 deployment)，都对应到一篇文档（比如 deployment.rst)。此外，还包含了索引和搜索入口。

象 deployment, usage 这样的文档，我们依照 rst 的语法来撰写就好，这部分我们已经介绍过了。这里我们需要特别介绍的是 api 文档，它是通过 autodoc 来生成的，有自己特殊的语法要求。

### 6.4. 生成 API 文档

要自动生成 API 文档，我们需要配置 autodoc 扩展。我们需要在 Sphinx 的配置文档 docs/conf.py 中，特别加入下面的第 2 行和第 5~9 行：

```python title="docs/conf.py"
# 要实现 AUTODOC 的功能，你的模块必须能够导入，因此先声明导入路径
sys.path.insert(0, os.path.abspath('../src'))

# 声明 AUTODOC 扩展
extensions = [
  'sphinx.ext.intersphinx',
  'sphinx.ext.autodoc',
  'sphinx.ext.doctest'
]
```
我们还要按 Autodoc 的要求，编写 api.rst 文档，并在 index.rst 中引用这个文档。api.rst 文档的作用是用作 autodoc 的文档入口。下图是 api.rst 的一个示例：

```python
Crawler Python API
==================

Getting started with Crawler is easy.
The main class you need to care about is :class:`~crawler.main.Crawler`

crawler.main
------------

.. automodule:: crawler.main
   :members:

crawler.utils
-------------

.. testsetup:: *

   from crawler.utils import should_ignore, log

.. automethod:: crawler.utils.should_ignore

.. doctest::

	>>> should_ignore(['blog/$'], 'http://example.com/blog/')
	True
```
这里虚构了一个名为 Crawler 的程序，它共有``main``和``util``两个模块。

在一篇文档里，普通 rst 语法、autodoc 指令和 doctest 指令是可以相互混用的，在上面的文档里，我们看到了一些已经熟悉的 rst 语法，比如一级标题"Crawler Python API"和二级标题"crawler.main"等。此外，我们还看到了 autodoc 的一些指令和 doctest 的指令。

我们通过扩展指令 automodule（第 10 行）将 crawler.main 模块引入，这样 autodoc 就会自动提取该模块的 docstring。注意这里的 :members: 语法：我们可以在其后跟上 crawler.main 中的子模块名字，表明只为这些模块生成 API 文档。如果其后为空白，则表明我们将递归生成 crawler.main 下所有模块的 API 文档。我们还可以通过 :undoc-members: 来排除那些不需要生成 API 文档的成员。

可以使用的指令除了 automodule 之外，还有 autoclass, autodata, autoattribute, autofunction, automethod 等。这些指令的用法与 automodule 类似，只是它们分别用于类，数据，属性，函数和方法的文档生成。

第 16 行起，这里混杂了 autodoc 与 doctest 指令。testsetup 指令用于在 doctest 中进行测试前的准备工作，这里的准备工作是导入 crawler.utils 模块。doctest 指令用于执行 doctest，这里我们执行了一个测试用例，测试了 crawler.utils.should_ignore 函数的功能。

最后，在 Sphinx 进行文档构建时，就会在解析 api.rst 文档时，依次执行 autodoc 和 doctest 指令，将生成的文档插入到 api.rst 文档中。

Sphinx 的功能十分强大，其学习曲线也比较陡峭。在学习时，可以将其 [sphinx 教程](https://sphinx-tutorial.readthedocs.io/) 与 [sphinx 教程的源码](https://github.com/ericholscher/sphinx-tutorial/) 对照起来看，这样更容易理解。

使用 Autodoc 生成的 API 文档，需要我们逐个手动添加入口，就象上面的``.. automodules:: cralwer.main``那样。对比较大的工程，这样无疑会引入一定的工作量。Sphinx 的官方推荐使用 [sphinx.ext.autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) 扩展来自动化这一任务。前面已经提到，在较早的时候，Sphinx 还有一个 cli 工具，叫 sphinx-apidoc 可以用来完成这一任务。但根据 [这篇文章](https://romanvm.pythonanywhere.com/post/autodocumenting-your-python-code-sphinx-part-ii-6/)，我们应该转而使用``sphinx-ext.autosummary``这个扩展。

除此之外，readthedocs 官方还开发了一个名为 [sphinx-autoapi](https://sphinx-autoapi.readthedocs.io/en/latest/tutorials.html) 的扩展。与 autosummary 不同，它在构建 API 文档时，并不需要导入我们的项目。目前看，除了不需要导入项目之外，没有人特别提到这个扩展与 autosummary 相比有何优势，这里也就简单提一下，大家可以持续跟踪这个项目的进展。

### 6.5. docstring 的样式

显然，为了使得 API 文档能够从代码注释中自动提取出来，代码注释必须满足一定的格式要求。

如果不做任何配置，Sphinx 会使用 rst 的 docstring 样式。下面是 rst 风格的 docstring 示例：
```python
def abc(a: int, c = [1,2]):
    """_summary_

    :param a: _description_
    :type a: int
    :param c: _description_, defaults to [1,2]
    :type c: list, optional
    :raises AssertionError: _description_
    :return: _description_
    :rtype: _type_
    """
    if a > 10:
        raise AssertionError("a is more than 10")

    return c
```
rst 风格的 docstring 稍显冗长。为简洁起见，我们一般使用 google style（最简洁），或者 numpy style。

下面是 google style 的 docstring 示例：
```python
def abc(a: int, c = [1,2]):
    """_summary_

    Args:
        a (int): _description_
        c (list, optional): _description_. Defaults to [1,2].

    Raises:
        AssertionError: _description_

    Returns:
        _type_: _description_
    """
    if a > 10:
        raise AssertionError("a is more than 10")

    return c
```
显然，google style 使用的字数更少，视觉上更简洁。google style 也是可罕学院（khan academy）[^khan] 的官方推荐风格。

我们再来看看 numpy 风格的 docstring:
```python
def abc(a: int, c = [1,2]):
    """_summary_

    Parameters
    ----------
    a : int
        _description_
    c : list, optional
        _description_, by default [1,2]

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    AssertionError
        _description_
    """
    if a > 10:
        raise AssertionError("a is more than 10")

    return c
```
这种风格也比 google style 要繁复许多。

要在文档中使用这两种样式的 docstring，你需要启用 [Napolen](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) 扩展。关于这两种样式的示例，最好的例子来自于 [MkApi 的文档](https://mkapi.daizutabi.net/examples/google_style/)，这里不再赘述。

注意在 Sphinx 3.0 以后，如果你使用了 Type Hint，则在书写 docstring 时，不必在参数和返回值上声明类型。扩展将自动为你加上类型声明。

### 6.6. 混合使用 Markdown

多数人会觉得 rst 的语法过于繁琐，因此很自然地，我们希望部分文档使用 Markdown 来书写（如果不能全部使用 Markdown 的话）。大约从 2018 年起，readthedocs 开发了一个名为 [recommonmark](https://recommonmark.readthedocs.io/en/latest/) 的扩展，以支持在 Sphinx 构建过程中部分使用 Markdown。

在这种场景下要注意的一个问题是，Markdown 文件必须都在 docs 目录及其下级目录中，而不能出现在项目的根目录下。这样一来，象 README，HISTORY 这样的文档，就必须仍然使用 rst 来写（以利用``include``语法来包含来自上一级的 README)。如果要使用 Markdown 的话，就必须使用符号连接将父目录中的 README.md 连接到 docs 目录下（recommenmark 自己的文档采用这种方式）；或者通过 Makefile 等第三方工具，在 sphinx build 之前，将这些文档拷贝到 docs 目录。

在 github 上还有一个 m2r 的项目，及其 fork m2r2，可以解决这些问题，不过开发者怠于维护，随着 Sphinx 版本升级，基本上不可用了。

如果您的项目必须使用 rst，那么可以在项目中启用 recommonmark，实现两种方式的混用。通过在 recommonmark 中启用一个名为 autostructify 的子组件，可以将 Markdown 文件事前编译成 rst 文件，再传给 Sphinx 处理；更妙的是，autostructify 组件支持在 Markdown 中嵌入 rst 语法，所以即使一些功能 Markdown 不支持，也可以通过局部使用 rst 来补救。
## 7. 使用 Mkdocs 构建文档

[mkdocs](https://www.mkdocs.org) 是一个高效易用的技术文档构建工具，同时也是一个静态网站构建工具，非常适合构建博客、技术文档站点。它构建的文档几乎可以被任何网站托管服务所托管，包括 github pages，readthedocs 等。它使用 Markdown 作为文档格式，支持自定义主题，支持实时预览。Mkdocs 有强大的自定义功能（通过插件和主题），从而可以生成风格多样的站点。

安装 mkdocs 之后，可以看一下它的基本命令：

![](assets/img/chap10/mkdocs_features.png){width="40%"}

[mkdocs](https://www.mkdocs.org) 提供了两种开箱即用的主题，readthedocs 和 mkdocs。我们也可以在社区里寻找更多的主题 。在众多主题之中，[material](https://squidfunk.github.io/mkdocs-material/) 是当前最受欢迎的一个主题。它支持 responsive 设计，所以文档无论在 pc 端、还是手机和平板上打开，都有相当不错的体验。此外，它自带了 SEO 优化，该主题的官方网站也被他们自己优化到超过了 Mkdocs 的排名。 [这篇文章](https://www.mkdocs.org/user-guide/writing-your-docs/) 给出了一个不错的教程。

首先，我们介绍如何安装。

```
$ pip install --upgrade pip
$ pip install mkdocs
# 安装 MATERIAL 主题。如果忽略，将使用 READTHEDOCS 默认主题。
$ pip install mkdocs-material 

# 创建文档结构，在项目根目录下执行
$ mkdocs new PROJECT_NAME
$ cd PROJECT_NAME
```

现在，在项目根目录下应该多了一个 docs 目录，和一个名为 mkdocs.yaml 的文件。docs 目录下还有一个名为 index.md 的文件。如果此时运行``mkdocs serve -a 0.0.0.0:8000``, 在浏览器中打开，你会看到如下图所示界面：

![](assets/img/chap10/mkdocs_new.png){width="70%"}

!!! Tip
    请注意，Mkdocs 能提供实时预览文档，而且有很快的响应速度。因此在您编写文档时，可以打开浏览器，实时预览文档的效果。

### 7.1. 配置 Mkdocs
下面，我们通过`ppw`生成的 mkdocs.yml 文件的例子来看看 mkdocs 的配置文件语法。

```yaml
site_name: sample
site_url: http://www.jieyu.ai
repo_url: https://github.com/zillionare/sample
repo_name: sample
site_description: A great mkdocs sample site
site_author: name of the author

nav:
  - home: index.md
  - usage: usage.md
  - modules: api.md
theme:
  name: material
  language: en
  logo: assets/logo.png
markdown_extensions:
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg
  - pymdownx.critic
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde
  - pymdownx.tabbed
  - attr_list
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight:
      linenums: true
  - pymdownx.superfences
  - pymdownx.details
  - admonition
  - toc:
      baselevel: '2-4'
      permalink: true
      slugify: !!python/name:pymdownx.slugs.uslugify
  - meta
plugins:
  - include-markdown
  - search:
      lang: en
  - mkdocstrings:
      watch:
        - sample
extra:
  version:
    provider: mike
```

mkdocs.yml 的配置大致可以分为站点设置、文档布局、主题设置、构建工具设置和附加信息这么几项。

文档布局以关键字`nav`引起，后面跟随一个 yaml 的列表，定义了全局站点导航菜单及子菜单结构。列表中的每一项都是一个文档的标题和对应的文件名。这里的文件名是相对于 docs 目录的。例如，上面的例子中，`home`对应的文件是`docs/index.md`，`usage`对应的文件是`docs/usage.md`，等等。

注意这里的 toc 配置项中的 baselevel。默认值为`2-4`。在 HTML5 规范中，只能存在一个 H1 标签（或者 Article 标签），所以，Toc 列表中的层级，只能从第 2 级开始列。不止在这里，您在任何地方撰写 Markdown 文档时，都应该遵循这个约定。

文档布局支持多级嵌套，比如：
```
nav:
    - Home: 'index.md'
    - 'User Guide':
        - 'Writing your docs': 'writing-your-docs.md'
        - 'Styling your docs': 'styling-your-docs.md'
    - About:
        - 'License': 'license.md'
        - 'Release Notes': 'release-notes.md'
```
上述配置定义了三个顶级菜单，分别是 Home、User Guide 和 About。User Guide 和 About 又分别包含两个子菜单。当然，最终如何展示这些内容，由你选择的主题来决定。

示例中的主题配置由关键字'theme'引起，一般包括了主题名、语言、站点 logo 和图标等通用选项，也有一些主题自定义的配置项。

构建工具设置主要是启用 markdown 扩展的一些特性和插件。

Mkdocs 使用了 Python-Markdown 来执行 markdown 到 html 的转换，而 Python-Markdown 本身又通过扩展来实现 markdown 核心语法之外的一些常用功能。因此，如果我们构建技术文档的过程中需要使用这些语法扩展，我们需要在这一节下启用这些特性。

在上述配置示例中，attr_list, admonition, toc, meta 是 Python-Markdown 的内置扩展，我们直接象示例那样启用就可以了。关于 Python-Markdown 提供了哪些官方扩展，可以参考 [这里](https://python-markdown.github.io/extensions/)。前面提到，Markdown 中的图片要指定宽度，要么使用 html 标签，要么通过 python-markdown 扩展。这里的 attr_list 就是用来实现这个功能的。关于 admonition，我们在 markdown 的语法中已经介绍过了，不熟悉的读者可以回到那一节再看一遍。toc 是用来生成目录的，meta 是用来提取文档元数据的。

使用第三方的扩展跟使用第三方主题一样，我们必须先安装这些扩展。比如，第 22 行的 pymakdownx.critic 就来自于第三方扩展 pymdown-extensions，我们需要先安装这个扩展，然后才能在 mkdocs.yml 中启用它。critic 给文档提供了批注功能，比如下面的示例：

![](https://images.jieyu.ai/images/2023/12/critics_markup.jpg)

其显示效果如下：

{~~ One ~>Only one ~~} thing is impossible for God: To find {++any++} sense in any.

{==Truth is stranger than fiction==}, but it is because Fiction is obliged to stick to possibilities; Truth isn’t.

现在，我们来看看如何定制 mkdocs，使之更适合生成技术文档。这些定制主要包括：

1. 更换主题
2. 文档重定向
3. 增强 markdown 功能
4. 自动生成 API 文档
   
### 7.2. 更换主题
MkDocs 提供了两种开箱即用的主题，即 MkDocs 和 readthedocs。后者是对 Read the Docs 网站默认主题的复制。MkDocs 的官网使用的主题就是 MkDocs，所以，考虑选择这个主题的读者，可以通过它的官网来了解这种主题的风格和样式。

除了这两种主题外，[material](https://squidfunk.github.io/mkdocs-material/) 是当前比较受欢迎的一个主题。这个主题也得到了 FastAPI 开发者的高度评价：

!!! Quote
    许多人喜欢 FastAPI, Typer 和 SQLModel 的原因之一是其文档。我花了很多时间，来使得这些项目的文档易于学习、能被快速理解。这里的关键因素是 Material for Mkdocs 提供了丰富多样的方法，使得我很容易向读者解释和展示各种各样的内容。同样地，结构化在 Material 中也很容易。使用简单、天生美观，让读者沉浸其中。

要更换主题为 Material，首先我们得安装 mkdocs-material 包，再在 mkdocs.yaml 中指定主题为 material:

```
pip install mkdocs-material
```
然后我们需要在 mkdocs.yml 中指定主题为 material:
```
site_name: An amazing site!

nav: 
  - Home: index.md
  - 安装：installation.md
theme: material
```
!!! Info
    如果您是使用`ppw`创建的工程，则默认主题已经是 material，并且依赖都已安装好了。

Material for Mkdocs 还提供了许多定制项，包括更改字体、主题颜色、logo、favicon、导航、页头 (header) 和页脚 (footer) 等。如果项目使用 Github 的话，还可以增加 Giscuss 作为评论系统。

Material 天生支持多版本文档。它的多版本文档是通过 [mike](https://github.com/jimporter/mike) 来实现的。后面我们还要专门介绍这个工具。

### 7.3. 文件重定向
在 Sphinx 那一节，我们已经面临过同样的问题： READEME, HISTORY, AUTHORS, LICENSE 等几个文件，通常必须放在项目根目录下，而 sphinx 在构建文档时，又只读取 docs 目录下的文件。

Mkdocs 也存在同样的问题，不过好在有一个好用的插件，[mkdocs-include-mkdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin)，在安装好之后，修改 docs/index.md 文件，使之指向父目录的 README:

```
{%
    include-markdown "../README.md"
% }
```

修改 mkdocs.yaml，加载 include-markdown 插件：
```yaml
site_name: Omicron

nav: 
  - Home: index.md
  - 安装：installation.md
  - History: history.md

theme: readthedocs

plugins:
  - include-markdown
```
Mkdocs 会将 docs/index.md 转换成网站的首页。我们让 index.md 指向 README.md，从而使得 README.md 的内容成为网站的首页。

### 7.4. 页面引用
在介绍 Markdown 语法时，我们介绍了超链接语法。有时候，我们需要在文档中引用其他页面，甚至是页面内的标题，这时候就需要用到内部链接。内部链接的语法是：
```
[页面标题](页面路径#标题锚点)
```
要使用标题锚点，必须在配置中启用 toc 的配置。如下所示：
```
markdown_extensions:
  - toc:
      permalink: true
      toc_depth: 5
      baselevel: 2-4
      slugify: !!python/name:pymdownx.slugs.uslugify
```
注意在上面的示例中 slugify 项的配置。这个配置的作用是允许在锚点中使用非英文字符。现在，我们可以这样引用第 4 章 ppw 生成的文件列表：
```
[ppw 生成的文件列表](chap04.md#ppw 生成的文件列表)
```
这将生成一个 [链接](chap04.md#ppw 生成的文件列表)。点击这个链接，将跳转到第 4 章的 ppw 生成的文件列表的标题处。

### 7.5. API 文档和 mkdocstrings

前面已经提到过 [MkApi](https://mkapi.daizutabi.net/) 这个扩展，它可以用来生成 API 文档。另一个能实现同样功能的扩展叫 [mkdocstrings](https://github.com/pawamoy/mkdocstrings)。在我们的测试中，Mkdocstrings 的稳定性更好，社区活跃度也更高一些。因此这里我们仅介绍 mkdocstrings。

Mkdocstrings 只支持 google style 的 docstring, 在样式上支持了 Material, Readthedocs 和 mkdocs 三种主题。要使用 mkdocstrings，需要先安装这个扩展：
```
poetry add mkdocstrings
```
再在 mkdocs.yaml 中配置：
```
plugins:
  - mkdocstrings:
      watch:
        - sample
```
mkdocstrings 有以下功能特性：
#### 7.5.1. 交叉引用

我们在 [页面引用](chap10.md#页面引用)那一节里讲到的那些引用，在 mkdocstrings 中也是支持的。不过，我们需要在 mkdocs.yml 配置文件中，启用一个名为 autorefs 的插件：
```
plugins:
    - search
    - autorefs
```
autorefs 并不需要安装，它会随 mkdocstrings 的安装而安装。

接下来主要讲解一下，如何引用到函数、类、模块对应的文档。在 mkdocstrings 中，此类引用类似使用 markdown 的引用语法的风格，但略有不同。举例如下：
```
With a custom title:
[`Object 1`][full.path.object1]

With the identifier as title:
[full.path.object2][]
```
可以看出，此类引用是由两对方括号，而不是由一对方括号加一对圆括号组成。其中第一对方括号里面是标题，第二对方括号里面是引用的对象的路径。也可以像第 60 行一样，只使用默认的链接文字，即对象字面名。

我们再来解释一下，引用对象的路径的含义。假设我们有一个库，名为 foo，下面有一个模块 bar, 在 bar 模块中又定义了类 Baz，而类 Baz 又包含了方法 bark。如果我们要在某个方法（比如 dog_bark）中引用 bark 方法的文档，则 dog_bark 的文档应该如下（第 5 行）：

```python
def dog_bark(msg: str) -> None:
    """ Bark like a dog

        See Also:
            [Baz.bark][foo.bar.Baz.bark]
        Args:
            msg: The message to bark
    """
    ...
```
这里各层级对象之间的连接符都是"."。这既简化了记忆量，也符合 Python 的动态类型特征 -- 在 Python 中，一切都是对象。

!!! attention
    如果 foo.bar.Baz.bark 这个函数并没有文档，那么将产生一个无效链接。
    
    一个初学者不易觉察的事实是，mkdocstrings 在生成 API 文档时，需要导入我们开发的模块。如果模块有语法错误，特别是不能正常导入的话，则 mkdocstring 将无法生成 API 文档，并且不一定能准确报告错误。所以，在生成文档之前，请确保单元测试已经完全通过了。

在 mkdocstrings 0.14 之后，跳转到某个函数文档内部的子标题的能力也具备了。在 0.16 之后，它又有了类似 intersphinx 那样跨工程引用的能力。具体如何使用，请参考官方文档。

#### 7.5.2. 与主控文档建立关联
一般地，我们要在 docs 目录下生成一个名为 api.md 的文档（文件名可以任意取），并在 mkdocs.yml 中`nav`一节中配置进来（见第 5 行）：
```
nav:
  - home: index.md
  - installation: installation.md
  - usage: usage.md
  - modules: api.md
```
根据 mkdocs 的语法，这里的 home, usage, modules 等，将成为导航菜单上的一项，它们的链接将指向冒号后面的文档。然后，在 api.md 中，我们引入需要生成文档的各个模块：
```
::: my_package.my_module.MyClass
    handler: python
    options:
      members:
        - method_a
        - method_b
      show_root_heading: false
      show_source: false
```
上面的示例是一个配置项比较完全的例子。一般地，我们也可以象这样配置：
```
::: sample.models.security
    rendering:
        heading_level: 1
```
这样在模块 sample.models.security 下的所有类和函数都会被生成文档。

对于大型工程，我们倾向于将 API 文档拆成多个部分，再通过 mkdocs.yml 关联起来，比如下面的例子：
```
# MKDOCS.YML
nav:
  - 简介：index.md
  - 安装：installation.md
  - 教程：usage.md
  - API 文档：
    - timeframe: api/timeframe.md
    - triggers: api/triggers.md
    - security: api/security.md
```
对应地，我们在 docs/api 目录下生成了 security.md 等几个文档，每个文档中都只引入了自己关心的模块。
### 7.6. 多版本发布

我们的软件始终在不断地迭代，总有一些用户可能并不会随着我们的步伐升级。在这种情况下，我们必须要提供多个版本的文档，以便用户能够根据自己的需要选择合适的版本。在 mkdocs 中，这一功能是由 [Mike](https://github.com/jimporter/mike) 来实现的。
如果我们使用 mkdocs-material 主题，则只需要在 mkdocs.yml 中进行配置即可：
```
extra:
  version:
    provider: mike
```
这会使得在文档的 header 区域出现一个版本选择器，如下图所示：

![](assets/img/chap10/mike_versioning.png){width="50%"}

## 8. 在线托管文档

最好的文档分发方式是使用在线托管，一旦有新版本发布，文档能立即得到更新；并且，旧的版本对应的文档也能得到保留。[Reade the Docs](https://readthedocs.org/) 是最重要的文档托管网站之一，也是多年以来事实上的标准，而 github pages 则是后起之秀。由于它与 github 有较好的集成性，部署更为简单方便，因此我们以介绍 github pages 为主。
### 8.1. Read the docs
关于如何使用 read the docs, 请参考它的 [帮助文档](https://docs.readthedocs.io/en/stable/index.html)。这里只提示一下需要注意的几个核心概念：

1. read the docs 构建文档的方式是，它从 github 或者其他在线托管平台拉取我们的文档和代码，在它自己的服务器上进行文档构建。所以，它对文档构建技术有选择性，目前它支持的工具有 Sphinx 和 MkDocs 两种。
2. 我们在撰写文档时，往往会生成本地预览文档。但这份文档与 read the docs 上的文档没有任何关系。本地预览正确不代表 read the docs 能生成同样的文件。
3. 如果设置了 Read the Docs 自动拉取代码并构建文档的功能，那么每次往 GitHub 上 push 代码时，都会触发一次文档构建，并导致文档更新。所以正确的做法是将 Read the Docs 绑定到特定的分支上（比如 release 和 main），只有重要的版本发布时，才往这个分支上 push 代码，从而触发文档编译。Read the Docs 目前并不支持 Git 标签触发。
4. read the docs 编译文档时，可能会遇到各种依赖问题。首先应该绑定构建工具 (Sphinx 和 Mkdocs) 的版本。read the docs 提供了 readthedocs.yml 以供配置（放在项目根目录下）。我们使用的 API 文档生成工具可能还需要导入项目生成的 package，这种情况下，还需要为构建工具指定依赖。[在这里](https://docs.readthedocs.io/en/stable/config-file/v2.html) 有这个配置文件的模板。
5. 在文档构建中可能出现各种问题，为了帮助调试，read the docs 发布了官方 docker image，供大家在本地使用。

基于上述原因，我们更推荐使用 GitHub Pages 来托管文档，它简单易用，构建在本地完成，因此本地生成文档与 github pages 托管文档天然具有一致性，这将会为我们节省不少查错时间。

### 8.2. Github Pages
Github Pages 是 Github 提供的静态站点托管服务，它的原理是，由用户在本地（或者 CI 服务器上）编译好静态站点文件，签入 github 服务器的某个分支，再设置该分支为 github pages 读取的分支即可。这样生成的网站使用 github.io 的域名，支持 https 访问。如果你需要使用自己的域名，它也提供了修改方式。

在 github 上设置 git pages：

![](assets/img/chap10/github_pages.png){width="70%"}

当使用了 mkdocs 之后，如果我们要从本地发布文档，可以执行：
```bash
mkdocs gh-deploy
```
如果你使用 mike 进行多版本发布，则我们不应该使用 mkdocs 来进行本地发布，而是应该使用 mike:
```
mike deploy [version] [alias] --push
mike set-default [version-or-alias]
``` 

第 1 行中，我们不仅指定了版本号，还给它指定了一个别名。别名有着非常实用的功能。在启用多版本部署之后，链接都会带上版本号，比如，http://.../myproject/0.1.0/topic。新版本发布后，引用这些链接的地方必须要全部更改，否则就会指向过时的文档（当然个别情况下，我们也确实需要指向旧的版本号，但大多数情况下，都需要指向最新的版本）。这时，我们就可以使用叫 latest 的别名来解决这个问题，从一开始，链接就是 https://.../myproject/latest/topic，随着新版本发布，它总是指向最新的那个版本。

第 2 行中，我们指定了默认版本。在多版本部署下，如果不指定默认版本，则用户必须指定明确的版本号才能访问文档。但用户可能事先并不知道最新的版本是哪一个。这就是默认版本的作用。

## 9. 结论

Sphinx + rst 这条技术栈比较成熟稳定，但学习曲线比较陡峭，rst 的一些语法过于烦琐，文档撰写的效率不高。Mkdocs 正在成为构建静态站点和技术文档的新工具，相关功能、特性逐渐丰富，版本也趋于稳定，建议读者优先使用。

两种技术栈的比较如下：

| 项目       | Sphinx              | Mkdocs             | 说明                                                   |
| ---------- | ------------------- | ------------------ | ------------------------------------------------------ |
| 主控文档   | index.rst           | mkdocs.yml         | -                                                      |
| API 文档   | autodoc+autosummary | mkdocstrings       | mkdocstrings 对 material 支持较好，还未达到 1.0 里程碑 |
| 文档重定向 | rst 可支持          | 通过插件支持       | -                                                      |
| 警示文本   | 支持                | 通过扩展和主题支持 | -                                                      |
| 链接       | 文档内+跨项目       | 通过扩展支持       | 同 Sphinx                                              | - |
| 实时预览   | 第三方              | 内置               | mkdocs 实时预览更高效                                  |
| 表达能力   | 非常强，够用        | -                  |
| 生产效率   | 一般                | 高效               | -                                                      |

[^khan]: 可罕学院是麻省理工及哈佛大学毕业生萨尔曼. 可汗创建的非营利教育机构，通过网格提供免费教材。他们对 Google style 文档风格的推荐出现在 [github](https://github.com/Khan/style-guides/blob/master/style/python.md#docstrings)
