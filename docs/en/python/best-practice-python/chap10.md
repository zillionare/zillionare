---
title: "Writing Technical Docs: Sphinx vs MkDocs"
date: 
slug: en/articles/python/best-practice-python/chap10
tags: [Technical Documentation, Sphinx, MkDocs, Python]
excerpt: "A practical guide to Python technical documentation, comparing Sphinx and MkDocs workflows, formats, and deployment strategies for modern software projects."
lang: en
translation_of: articles/python/best-practice-python/chap10
auto_translated: true
source_sha: 85f26fb6a7a6f3c5c3835515ce158077e9392468
---

Every good product should have a concise, easy-to-read user manual, with the exception of Apple. Apple users intuitively know how to use their products, so they don’t need documentation at all. This is true: almost all Apple products lack user manuals.

However, for software, its complexity often demands detailed technical documentation to help users get started. Even for open-source products, people typically rely on technical documentation to get up to speed quickly. In this fast-paced era, who has time to read code line by line unless absolutely necessary?

Given the importance of technical documentation, how can we write it well? What tools can assist in documentation creation? What are the evaluation criteria for good technical documentation, and can these criteria be quantified like software metrics?

The author believes that, in addition to requiring technical authors to have good writing skills, a good technical document often includes the following technical requirements:

1. Standardized documentation structure with clean, elegant formatting.
2. Accurate content: Document versions must always align with code implementations (across multiple versions).
3. Necessary navigation and cross-references to help readers explore further, with no broken links.
4. Online hosting for immediate access and searchability.
5. The ability to generate various formats when necessary, such as HTML, PDF, and EPUB.

This article explores common documentation building technology stacks. The focus is not on providing a comprehensive operational guide, but on exploring various possible solutions, comparing them, and helping you choose the one that best suits your needs. For step-by-step application of these solutions, the article provides abundant reference links.

By reading this chapter, you will learn:

1. Best practices for documentation structure.
2. The two major schools of documentation building.
3. How to automatically generate API documentation.
4. How to publish documentation using GitHub Pages.

## 1. Composition of Technical Documentation
Technical documentation typically has two sources:

1. Comments written in a specific style during the coding process, extracted by tools to form so-called API documentation. This part dives into details.
2. Help documentation specifically written outside the code. Compared to API documentation, it is more macroscopic and summary-oriented, covering parts unsuitable for API documentation, such as the entire software’s design philosophy and principles, installation guides, license information, version history, and global examples.

Today, in the Python world, there are roughly two popular technical documentation building stacks: **Sphinx** and **MkDocs**. Below is a file list based on the Sphinx stack:
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
This layout is recommended in the book *[Python Best Practices Guide](https://docs.python-guide.org/writing/structure/)*. Its original source is a best practice for Python project layout recommended by [Kenneth Reitz](https://kennethreitz.org/essays/repository-structure-and-python) in 2013. To adapt to the needs of open-source projects, I have added two files here: `CONTRIBUTING.rst` and `AUTHORS.rst`. Its characteristics are that the document type is `.rst` files, and the document directory contains a `conf.py` Python file and a `Makefile`.

!!! Info
    Kenneth Reitz is a software architect, the author of the famous Python library `requests`. His Python ORM library `records` and virtual environment management tool `PipEnv` are also widely popular. He is dedicated to designing highly abstract, cognitively unburdened, and easy-to-use software.

If you use [Cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) to generate the project framework, you will find that the generated project exactly includes these files.

The other technical route is MkDocs. This is also the technical route adopted by `ppw`. Although Chapter 4 has provided a complete file list, for the convenience of readers, we still provide a streamlined list here, focusing only on document construction:

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

This technical route uses the Markdown file format, with `mkdocs.yml` providing the master document and configuration, without requiring any other configuration.

First, let’s introduce the two document formats: RST and Markdown.

## 2. Two Main Document Formats
Technical documents are generally written using a superset of plain text formats. Common formats include [reStructuredText](https://docutils.sourceforge.io/rst.html) (hereinafter referred to as RST) and [Markdown](https://zh.wikipedia.org/zh-hans/Markdown). The former is older, with complex syntax but powerful features; the latter is newer, with very concise syntax, and its features have gradually caught up with the support of third-party plugins.

## 3. reStructured Text
This section briefly introduces the common syntax of reStructured Text (hereinafter referred to as RST). If readers are interested in comprehensively understanding RST syntax, they can refer to the [reStructuredText Official Documentation](https://docutils.sourceforge.io/docs/user/rst/quickref.html).

### 3.1. Section Headings (section)
In RST, section headings are formed by text followed by an equal number of punctuation marks (limited to `#=-~:'"^_*+<>`). An example is as follows:

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
The above text will render in the following format:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/rst_headings.png){width="50%"}

The tedious and difficult aspect of this syntax lies in the fact that the number of characters in the heading must match the number of punctuation marks below. If non-monospaced characters are used (e.g., using Chinese headings), matching becomes very difficult. You can try finding an editor that supports RST (e.g., installing the "RST Preview" extension in VS Code) and manually typing the above example to verify this.

In addition to being less concise in input, the level of headings is unrelated to the symbols themselves but depends only on the order in which the symbols appear, which is also a source of errors. Users must remember the correspondence between each symbol and the heading level; otherwise, the generated document will have incorrect heading levels.

### 3.2. Lists (list)
In RST, unordered lists are formed using `*`, `-`, or `+` as bullet points; ordered lists are formed using numbers, letters, or Roman numerals followed by `.` or parentheses. Please see the following example:
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
In the example, ordered lists can use right parentheses or fully enclosed parentheses, but not only left parentheses. The above example renders as follows:

![](assets/img/chap10/rst_list.png){width="50%"}

### 3.3. Tables
RST core syntax supports two table representation methods: grid tables and simple tables. Grid tables are formed using some symbols to create tables, as shown below:
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
Creating tables this way is obviously tedious and difficult to maintain. Simple tables simplify this to some extent, no longer requiring vertical lines to be inserted between columns, but their functionality is limited. Therefore, RST extends to CSV tables and list tables through directive syntax. Here is an example of a CSV table:
```
.. csv-table:: 物理内存需求表
    :header: "行情数据","记录数（每品种）","时长（年）","物理内存（GB）"
    :widths: 12, 15, 10, 15

    日线，1000,4,0.75
```
Here, lines 1-3 are directives, and line 5 is CSV data. The above syntax will generate the following table:

![](assets/img/chap10/rst_csv_to_table.png){width="50%"}

Comparatively, this syntax is much simpler when inputting large amounts of data.

### 3.4. Images
Inserting images into documents requires directive syntax, for example:
```
.. image:: img/p0.jpg
    :height: 400px
    :width: 600px
    :scale: 50%
    :align: center
    :target: https://docutils.sourceforge.io/docs/ref/rst/directives.html#image
```
The example inserts the image `p0.jpg` from the `img` directory, displaying it at 400px height, 600px width, with a scaling ratio of 50%, center-aligned, and clicking the image will jump to the specified link.

### 3.5. Code Blocks
Inserting code blocks into documents requires directive syntax, for example:
```
.. code:: python

  def my_function():
      "just a test"
      print 8/2
```

### 3.6. Admonitions
Admonitions are typically used to emphasize important information, such as hints (error), important (important), tips (tip), warnings (warning), notes (note), etc.

Similarly, we use directive syntax to display admonitions, for example:

```
.. DANGER::
   Beware killer rabbits!
```
Displaying as follows:

![](assets/img/chap10/rst_admonition.png "Admonition Text"){width="50%"}

There are also some other common syntaxes, such as bolding, italicizing, displaying mathematical formulas, superscripts, subscripts, footnotes, citations, and hyperlinks. Introducing all RST syntax is far beyond the scope of this book. Interested readers can refer to the [Official Documentation](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html). Regarding RST, we must remember that although the syntax is tedious, it provides very powerful typesetting functions. It can be used not only for online documents but also for direct publication into books, a capability currently only rivaled by LaTeX.

## 4. Markdown
Markdown originated in the 2000s. Around 2000, John Gruber had a blog called [Daring Fireball](https://daringfireball.net). At that time, online editing tools were not as developed as they are now, and webpage text formatting still needed to be implemented through HTML code. Although he fully mastered HTML syntax, he felt that this syntax was definitely not suitable for most people, so he had the idea of inventing a simplified markup language. This language would be simpler than HTML but could be converted to HTML. Finally, drawing on some conventions of plain text email markup and some features of Setext and atx markup languages, he invented the Markdown language in 2004 and released the first tool to convert Markdown to HTML.

In 2007, GitHub developer Chris Wanstrath encountered the Markdown language. In 2014, GitHub announced that it would use Markdown to write documentation on GitHub. This move made the Markdown language even more popular. The core syntax of Markdown is very simple, with only dozens of rules, and some common formats still cannot be implemented. Therefore, Github, Reddit, and Stack Exchange made some of their own extensions to Markdown, known as "Flavors," such as Github Markdown Flavor, which added tables, code snippets, etc. These extensions greatly enhanced the expressive power of Markdown.

!!! Readmore
    After big players like Github and Reddit got involved with Markdown, the standardization problem of Markdown emerged. In 2014, John MacFarlane, a philosophy professor at the University of California, Jeff Atwood, co-founder of Discourse, and representatives from Reddit, Github, and Stackoverflow, jointly formed a working group to begin the standardization of Markdown. Surprisingly, the founder of Markdown, John Gruber, opposed the standardization work and prohibited them from using the name Markdown. Ultimately, the result of this standardization became [CommonMark](https://commonmark.org), considered a de facto standard.

    John Gruber’s opposition to the standardization of Markdown and his prohibition of the working group using the name Markdown is somewhat regrettable. One wonders if this can be considered another instance of the dragon-slaying boy eventually becoming the dragon. However, this is not an isolated case in the tech industry. Some people also believe that the biggest obstacle to solving Python’s performance issues actually comes from its creator, Guido, because he believes Python’s performance is already good enough: if someone thinks Python’s performance is not good enough, they should switch to another language. In the process of improving Python’s performance, incompatible phenomena like those during the upgrade from version 2 to version 3 are not allowed.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


Next, let’s look at Markdown syntax with examples. Note that here we do not strictly distinguish between core syntax and CommonMark extended syntax, because so far, CommonMark extensions have been supported by most editors.

### 4.1. Section Headings
Markdown section headings are initiated with `#`, and the number of `#` indicates the heading level, for example:
```txt
# 1. 这是一级标题
## 1.1 这是二级标题
### 1.1.1 这是三级标题
### 1.1.2 另一个三级标题
## 1.2 另一个二级标题
```
It can be seen that this is more intuitive, memorable, and concise than RST. In the example, we manually numbered the headings. This is not mandatory; many Markdown rendering tools can automatically number headings via CSS. Additionally, many Markdown editors have the ability to automatically insert and update numbering for headings.

### 4.2. Lists
Markdown lists are similar to RST. Unordered lists are initiated with `-` or `*`, for example:
``` {linenums="0"}
- 无序列表 1
- 无序列表 2
```
The final rendered effect is as follows:

- Unordered List 1
- Unordered List 2

Ordered lists are initiated with numbers followed by `.`, for example:
```
1. 有序列表 1
3. 有序列表 2
```
The final rendered effect is as follows:

1. Ordered List 1
2. Ordered List 2

Note that in the above example, the serial numbers of the ordered list are not continuous. In Markdown syntax, it does not matter what numbers we provide; the Markdown rendering tool will ultimately adjust them correctly. This is a very good feature.

### 4.3. Tables

Compared to RST, Markdown’s table syntax is still somewhat complex:
```
| Header1 | Header2 | Header3 |
| :------ | :-----: | ------: |
| data1   |  data2  |   data3 |
| data11  | data12  |  data13 |
```
The characteristic of the syntax is that each row of the table starts and ends with `|`, and data between columns is separated by `|`. The separator line between the header and the table is represented by `-`. The number of separator lines and table columns can be inconsistent, but must be greater than or equal to the number of columns in the table. The rendering effect of the table is as follows:

| Header1 | Header2 | Header3 |
| :------ | :-----: | ------: |
| data1   |  data2  |   data3 |
| data11  | data12  |  data13 |

Note the colons in the above table syntax. Their role here is to indicate the alignment of the column. When a colon is used on the left side of the separator line, the column is left-aligned; when a colon is used on the right side of the separator line, the column is right-aligned; when colons are used on both sides, the column is center-aligned. When no colon is used, the column is left-aligned.

Markdown does not have directive syntax like RST, so extending features beyond core syntax is not easy. As an example, CSV data cannot be directly rendered as tables in Markdown. If we find it difficult to create tables in Markdown, the general approach is to use the editor’s extension features to convert CSV data into Markdown tables.

!!! Tip
    VS Code has extensions that can achieve this function.

### 4.4. Inserting Links
Inserting links in Markdown is simple, with the following syntax:
```
[链接名](https://example.com)
```
That is, the symbols `[]()` define a link, where `[]` contains the display text of the link, and `()` contains the link target.

### 4.5. Inserting Images
The syntax for inserting images is similar to inserting links:
```
![alt text](image url "image Title")
```
The difference is that image links must be initiated with an exclamation mark. The text in `[]` becomes the alternative text for the image, which screen readers use to describe the image to visually impaired readers. The text in `()` is the URL of the image, which can be a relative or absolute path. Finally, double quotes can be added, containing the title of the image, which will be displayed when the mouse hovers over the image.

Here is an example:
```
![这是一段警示文本](img/markdown.png)
```
The generated effect is as follows:

![](assets/img/chap10/markdown_logo.png "Admonition Text Example"){width="50%"}

Markdown core syntax does not support specifying width and height, alignment, etc., like RST. If we have these needs, there are generally two ways to solve them. One is that we can use HTML syntax to achieve this, for example:
```
<img src="img/markdown.png" width="30%">
```
The effect is shown in the figure below:
![](assets/img/chap10/markdown.png){width="30%"}

The second is that the Markdown editor you use may support extended syntax. When writing this article, I used the relevant extension features in Mkdocs-Material. The following example is its usage:
```
 ![](assets/img/chap10/markdown_logo.png "警示文本示例"){width="30%"}
```

### 4.6. Code Blocks
We use three backticks `` ` `` to define code blocks, for example:
```
    ```python
        def foo():
            print('hello world')
    ```
```
After the initial backticks, a language definition can be added. In this way, the code block can obtain syntax highlighting. For the above code block, we used `python` as the language definition, so the code block will obtain Python syntax highlighting, as shown below:
```python
    def foo() -> None:
        print('hello world')
```

### 4.7. Admonitions
In Markdown, we can initiate admonitions with three exclamation marks, with the following syntax:
```
!!! type "双引号定义标题"
    Any number of other indented markdown elements.

    This is the second paragraph.
```

This is an extension syntax of CommonMark. The English word after the exclamation mark is the type of admonition. CommonMark does not limit what types there are. In implementation, these types are all CSS classes, so the specific display effect depends on the renderer’s decision. For example, the web version of this book uses the `mkdocs-material` theme. The types supported by Material include `note`, `abstract`, `info`, `tip`, `success`, `question`, `warning`, `example`, `quote`, etc. If a type not in the above list is used, Mkdocs-Material will use the default style to display this admonition text.

For example, here is an example of quoting someone else’s words:
```
    !!! quote "罗曼. 罗兰"
        世上只有一种英雄主义，就是认清生活的真相之后依然热爱生活。
```
Its effect is as follows:

!!! quote "Romain Rolland"
    There is only one heroism in the world: to see the world as it is and to love it.

Human biological evolution is measured in millennia, but our society has long entered the era of information explosion and overload. This is one of the reasons why modern people feel tired. When we write technical documentation, we should make more use of styles like admonitions to highlight the key points of the article, thereby reducing the reading burden; at the same time, its graphical layout brings a touch of lightness to the somewhat rigid text.

### 4.8. Other Syntax
Text between two `**` will be displayed in **bold**, and text between two `_` will be displayed in _italic_ (text can also be enclosed by two `*`). If text is enclosed in three groups of `***`, the text will be displayed in ***bold + italic***.

Inline mathematical formulas are enclosed in a pair of `\$`, for example: `\$x\^2\$`, which will display as: x<sup>2</sup>. Here we also demonstrate the use of superscripts, i.e., using `^`. If you want to generate subscripts, you can use `_`, for example: `\$x\_2\$`, which will display as: x<sub>2</sub>.

When we introduced the syntax for inserting images, we mentioned that some features, such as specifying width, are not supported by Markdown core syntax. We can use HTML syntax. This applies not only to images. In fact, in any part of a Markdown document, we can use HTML to enhance the display effect. Since HTML syntax supports superscripts and subscripts, we can also rewrite the above example using HTML syntax. Superscripts and subscripts can be implemented using HTML `<sup>` and `<sub>` tags, for example, x<sup>2</sup> will display as x^2. H<sub>2</sub>O will display as subscript H_2 O.

Superscripts and subscripts can be implemented using HTML `<sup>` and `<sub>` tags, for example, x\<sup\>2\</sup\> will display as x<sup>2</sup>. H\<sub\>2\</sub\>O will display as subscript H<sub>2</sub>O.

## 5. Sphinx vs MkDocs: Two Main Building Tools

RST and Markdown are both great inventions. They allow us to save information based on text file formats. Even without relying on any commercial software, we can edit and read these documents. Imagine if we saved a large amount of document information in Word, a commercial software. If one day the commercial software terminates service or raises fees, how great would the migration cost be due to this technology lock-in effect?!

However, RST and Markdown are just simple text formats. Direct reading does not have good visual effects. Additionally, large documents often consist of multiple sub-documents, so we also need tools to organize documents to provide readers with functions like tables of contents and navigation. This leads to the need for documentation building tools.

The main role of documentation building tools is to integrate documents scattered in different places, present a certain structure, allow different parts of the document to link and navigate to each other, and render simple text formats into more beautiful rich text formats. In the Python world, the most important documentation building tools are Sphinx and MkDocs.

[Sphinx](https://www.sphinx-doc.org/en/master/) is a documentation building tool that started in May 2008, with the current version 7.2. Its main functions are to integrate various sub-documents through a master document, generate document structures (toctree), API documentation, implement in-document and cross-file, cross-project references, and interface theme functions.

In early versions, Sphinx did not have the function of generating API documentation. We needed to use third-party tools, such as `sphinx-apidoc`, to achieve this function. Around 2018, Sphinx implemented the function of generating API documentation through the `autodoc` extension. In current projects, it is no longer necessary to use the `sphinx-apidoc` tool (Note: In projects generated by `cookiecutter-pypackage`, the `sphinx-apidoc` tool is still in use).

[intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) is its featured function. It allows you to link between two different documents. For example, if you override an implementation in the Python standard library in your own project and have already written documentation for the new features, but you do not want to rewrite the help documentation for the unchanged parts, you will have the need to link to the Python standard library documentation. For example, through intersphinx, you can use `\:py\:class:\`zipfile.ZipFile\`_` to jump to the documentation of the `ZipFile` class in the Python standard library. Although you can also directly use an HTML hyperlink to achieve such a jump, undoubtedly, the syntax of intersphinx is more concise.

[MkDocs](https://www.mkdocs.org) appeared in 2014, with the current version 1.5. In addition to building project documentation, MkDocs can also be used to build static sites. In building project documentation, it mainly provides document integration functions, interface themes, and plugin systems. Compared to Sphinx, it provides **better real-time preview capabilities**. Sphinx itself does not provide this capability. Some third-party tools (such as the RST plugin in VS Code) provide single-article preview functions.

Both of these documentation building tools are supported by documentation hosting platforms [ReadTheDocs](https://readthedocs.org/) and Git Pages. In most cases, the author recommends using MkDocs and Markdown syntax, which is also the technical route currently used by `ppw`.

## 6. Building Documentation with Sphinx

### 6.1. Initializing Documentation Structure

After installing Sphinx, initialize the documentation through the following command:

``` bash
$ pip install sphinx 

# 此命令必须在项目根目录下执行！
$ shpinx-quickstart

```
Sphinx will prompt you to enter project name, author, version, and other information, ultimately generating the `docs` directory and the following files:
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
If the document uses image files, they should be placed in the `_static` directory.

Now, running ``make html`` will generate a document. You can open ``_build/index.html`` through a browser to read it, or through ``python -m http.server -d _build/index``, and then access and read it through a browser.

### 6.2. File Redirection

We generally place `README.rst`, `AUTHOR.rst`, and `HISTORY.rst` in the project root directory, i.e., at the same level as the Sphinx documentation root directory. This is a requirement of Python project management and also a convention for hosting platforms like Github. However, according to Sphinx’s requirements, documents must be placed in the `docs` directory. We certainly do not want to place copies of the same file in two directories. To solve this problem, we generally use the ``include`` syntax to include files of the same name from the parent directory. For example, the `history` file in the above `index.rst`:

```
# CONTENT OF DOCS/HISTORY.RST

.. include:: ../HISTORY.rst
``` 
This avoids the situation where the same file appears in multiple copies.

### 6.3. Master Document and Toolchain

If you initialize through Sphinx-quickstart, its wizard will guide you through some toolchain configurations, such as configuring `autodoc` (used to generate API documentation). For completeness, we will mention this topic again.

Sphinx requires a master document when building documentation, generally `index.rst`:

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

Sphinx connects individual documents through the master document. Each entry in the above `toctree` (e.g., `deployment`) corresponds to a document (e.g., `deployment.rst`). Additionally, it includes index and search entries.

For documents like `deployment` and `usage`, we write them according to RST syntax, which we have already introduced. Here we need to specifically introduce API documentation, which is generated through `autodoc` and has its own special syntax requirements.

### 6.4. Generating API Documentation

To automatically generate API documentation, we need to configure the `autodoc` extension. We need to specially add the 2nd line and lines 5~9 in the Sphinx configuration document `docs/conf.py`:

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
We also need to write the `api.rst` document according to Autodoc’s requirements and reference this document in `index.rst`. The role of the `api.rst` document is to serve as the document entry for `autodoc`. The following figure is an example of `api.rst`:

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
Here, a fictional program named `Crawler` is created, which has two modules: ``main`` and ``util``.

In a document, ordinary RST syntax, autodoc directives, and doctest directives can be mixed. In the above document, we see some familiar RST syntax, such as the primary heading "Crawler Python API" and the secondary heading "crawler.main". In addition, we also see some autodoc directives and doctest directives.

We introduce the `crawler.main` module through the extension directive `automodule` (line 10), so that `autodoc` will automatically extract the docstring of that module. Note the `:members:` syntax here: we can follow it with the names of submodules in `crawler.main`, indicating that API documentation is generated only for these modules. If it is blank after it, it indicates that we will recursively generate API documentation for all modules under `crawler.main`. We can also use `:undoc-members:` to exclude members that do not need to generate API documentation.

In addition to `automodule`, the directives that can be used include `autoclass`, `autodata`, `autoattribute`, `autofunction`, and `automethod`. The usage of these directives is similar to `automodule`, but they are used for generating documentation for classes, data, attributes, functions, and methods, respectively.

Starting from line 16, this section mixes autodoc and doctest directives. The `testsetup` directive is used for pre-test preparation in doctest. Here, the preparation is to import the `crawler.utils` module. The `doctest` directive is used to execute doctest. Here, we execute a test case to test the functionality of the `crawler.utils.should_ignore` function.

Finally, when Sphinx performs document construction, it will execute the autodoc and doctest directives in sequence when parsing the `api.rst` document, and insert the generated documents into the `api.rst` document.

Sphinx’s functions are very powerful, and its learning curve is also relatively steep. When learning, you can refer to the [Sphinx Tutorial](https://sphinx-tutorial.readthedocs.io/) and the [source code of the Sphinx tutorial](https://github.com/ericholscher/sphinx-tutorial/) side by side, which makes it easier to understand.

API documentation generated using Autodoc requires us to manually add entries one by one, like the above ``.. automodules:: cralwer.main``. For larger projects, this undoubtedly introduces a certain workload. The official recommendation of Sphinx is to use the [sphinx.ext.autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) extension to automate this task. As mentioned earlier, in the early days, Sphinx had a CLI tool called `sphinx-apidoc` that could complete this task. But according to [this article](https://romanvm.pythonanywhere.com/post/autodocumenting-your-python-code-sphinx-part-ii-6/), we should switch to using the ``sphinx-ext.autosummary`` extension.

In addition, the official ReadTheDocs has developed an extension called [sphinx-autoapi](https://sphinx-autoapi.readthedocs.io/en/latest/tutorials.html). Unlike autosummary, it does not require importing our project when building API documentation. So far, apart from not needing to import the project, no one has specifically mentioned any advantages of this extension compared to autosummary. Here, we simply mention it, and everyone can continue to track the progress of this project.

### 6.5. Docstring Styles

Obviously, in order for API documentation to be automatically extracted from code comments, code comments must meet certain format requirements.

If no configuration is made, Sphinx will use the RST docstring style. Here is an example of RST-style docstring:
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
RST-style docstrings are slightly verbose. For simplicity, we generally use Google style (the most concise) or NumPy style.

Here is an example of Google-style docstring:
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
Obviously, Google style uses fewer words and is visually more concise. Google style is also the official recommended style by Khan Academy[^khan].

Let’s look at NumPy-style docstring again:
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
This style is also much more complex than Google style.

To use these two styles of docstrings in documentation, you need to enable the [Napolen](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) extension. For examples of these two styles, the best examples come from [MkApi’s documentation](https://mkapi.daizutabi.net/examples/google_style/), which will not be repeated here.

Note that after Sphinx 3.0, if you use Type Hints, you do not need to declare types for parameters and return values when writing docstrings. The extension will automatically add type declarations for you.

### 6.6. Mixing Markdown

Most people feel that RST syntax is too tedious, so naturally, we hope to write some documents using Markdown (if not all of them). Around 2018, ReadTheDocs developed an extension called [recommonmark](https://recommonmark.readthedocs.io/en/latest/) to support using Markdown partially during Sphinx construction.

One issue to note in this scenario is that Markdown files must all be in the `docs` directory and its subdirectories, and cannot appear in the project root directory. In this way, documents like `README` and `HISTORY` must still be written in RST (to utilize the ``include`` syntax to include `README` from the upper level). If you want to use Markdown, you must use symbolic links to connect `README.md` from the parent directory to the `docs` directory (recommonmark’s own documentation uses this method); or use third-party tools like `Makefile` to copy these documents to the `docs` directory before Sphinx build.

There is also a project on Github called `m2r` and its fork `m2r2`, which can solve these problems, but the developers are lazy in maintaining it. With the upgrade of Sphinx versions, it is basically unusable.

If your project must use RST, you can enable `recommonmark` in the project to achieve a mix of both methods. By enabling a sub-component called `autostructify` in `recommonmark`, Markdown files can be pre-compiled into RST files and then passed to Sphinx for processing; even better, the `autostructify` component supports embedding RST syntax in Markdown, so even if some features are not supported by Markdown, they can be remedied by locally using RST.

## 7. Building Documentation with MkDocs

[mkdocs](https://www.mkdocs.org) is an efficient and easy-to-use technical documentation building tool, and also a static website building tool, very suitable for building blogs and technical documentation sites. The documents it builds can be hosted by almost any website hosting service, including GitHub Pages, ReadTheDocs, etc. It uses Markdown as the document format, supports custom themes, and supports real-time preview. MkDocs has powerful customization features (through plugins and themes), so it can generate sites with diverse styles.

After installing MkDocs, you can look at its basic commands:

![](assets/img/chap10/mkdocs_features.png){width="40%"}

[mkdocs](https://www.mkdocs.org) provides two out-of-the-box themes: `readthedocs` and `mkdocs`. We can also look for more themes in the community. Among the many themes, [material](https://squidfunk.github.io/mkdocs-material/) is currently the most popular theme. It supports responsive design, so whether the document is opened on a PC, mobile phone, or tablet, it has a quite good experience. In addition, it comes with SEO optimization, and the official website of this theme has been optimized by themselves to exceed MkDocs’ ranking. [This article](https://www.mkdocs.org/user-guide/writing-your-docs/) provides a good tutorial.

First, let’s introduce how to install.

```
$ pip install --upgrade pip
$ pip install mkdocs
# 安装 MATERIAL 主题。如果忽略，将使用 READTHEDOCS 默认主题。
$ pip install mkdocs-material 

# 创建文档结构，在项目根目录下执行
$ mkdocs new PROJECT_NAME
$ cd PROJECT_NAME
```

Now, there should be a `docs` directory and a file named `mkdocs.yaml` in the project root directory. There is also a file named `index.md` in the `docs` directory. If you run ``mkdocs serve -a 0.0.0.0:8000`` at this time and open it in a browser, you will see the interface shown in the figure below:

![](assets/img/chap10/mkdocs_new.png){width="70%"}

!!! Tip
    Please note that MkDocs can provide real-time preview of documents, and has a very fast response speed. Therefore, when you are writing documents, you can open the browser to preview the effect of the document in real time.

### 7.1. Configuring MkDocs
Next, let’s look at the configuration file syntax of MkDocs through the example of the `mkdocs.yml` file generated by `ppw`.

```yaml
site_name: sample
site_url: https://blog.quantide.cn/
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

The configuration of `mkdocs.yml` can be roughly divided into site settings, document layout, theme settings, build tool settings, and additional information.

Document layout is initiated by the keyword `nav`, followed by a YAML list, defining the global site navigation menu and submenu structure. Each item in the list is a document title and the corresponding file name. Here, the file name is relative to the `docs` directory. For example, in the above example, the file corresponding to `home` is `docs/index.md`, the file corresponding to `usage` is `docs/usage.md`, and so on.

Note the `baselevel` in the `toc` configuration item here. The default value is `2-4`. In the HTML5 specification, there can only be one H1 tag (or Article tag), so the levels in the TOC list can only start from the 2nd level. Not only here, but when you write Markdown documents anywhere, you should follow this convention.

Document layout supports multi-level nesting, for example:
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
The above configuration defines three top-level menus: Home, User Guide, and About. User Guide and About each contain two submenus. Of course, how to finally display these contents is determined by the theme you choose.

The theme configuration in the example is initiated by the keyword `theme`, generally including general options such as theme name, language, site logo, and icons, as well as some custom configuration items for the theme.

Build tool settings mainly enable some features of Markdown extensions and plugins.

MkDocs uses Python-Markdown to execute the conversion from Markdown to HTML, and Python-Markdown itself implements some common functions beyond the core syntax of Markdown through extensions. Therefore, if we need to use these syntax extensions in the process of building technical documentation, we need to enable these features under this section.

In the above configuration example, `attr_list`, `admonition`, `toc`, and `meta` are built-in extensions of Python-Markdown. We can enable them directly as shown in the example. For which official extensions Python-Markdown provides, you can refer to [here](https://python-markdown.github.io/extensions/). As mentioned earlier, specifying the width of images in Markdown requires either using HTML tags or through the Python-Markdown extension. Here, `attr_list` is used to achieve this function. Regarding `admonition`, we have already introduced it in the Markdown syntax section. Readers who are not familiar with it can go back to that section to review it. `toc` is used to generate the table of contents, and `meta` is used to extract document metadata.

Using third-party extensions is the same as using third-party themes. We must first install these extensions. For example, line 22 `pymakdownx.critic` comes from the third-party extension `pymdown-extensions`. We need to install this extension first, and then we can enable it in `mkdocs.yml`. `critic` provides annotation functions for documents, such as the following example:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/critics_markup.jpg)

Its display effect is as follows:

{~~ One ~>Only one ~~} thing is impossible for God: To find {++any++} sense in any.

{==Truth is stranger than fiction==}, but it is because Fiction is obliged to stick to possibilities; Truth isn’t.

Now, let’s see how to customize MkDocs to make it more suitable for generating technical documentation. These customizations mainly include:

1. Changing the theme.
2. Document redirection.
3. Enhancing Markdown features.
4. Automatically generating API documentation.

### 7.2. Changing the Theme
MkDocs provides two out-of-the-box themes: MkDocs and ReadTheDocs. The latter is a copy of the default theme of the Read the Docs website. The theme used on the MkDocs official website is MkDocs, so readers considering choosing this theme can learn about the style and appearance of this theme through its official website.

In addition to these two themes, [Material](https://squidfunk.github.io/mkdocs-material/) is currently a relatively popular theme. This theme also received high praise from FastAPI developers:

!!! Quote
    One of the reasons many people like FastAPI, Typer, and SQLModel is their documentation. I spent a lot of time making the documentation for these projects easy to learn and quickly understandable. The key factor here is that Material for MkDocs provides a rich variety of methods, making it easy for me to explain and present various content to readers. Similarly, structuring is also easy in Material. Simple to use, naturally beautiful, and immersive for readers.

To change the theme to Material, first we need to install the `mkdocs-material` package, and then specify the theme as `material` in `mkdocs.yaml`:

```
pip install mkdocs-material
```
Then we need to specify the theme as `material` in `mkdocs.yml`:
```
site_name: An amazing site!

nav: 
  - Home: index.md
  - 安装：installation.md
theme: material
```
!!! Info
    If you use the project created by `ppw`, the default theme is already Material, and all dependencies are installed.

Material for MkDocs also provides many customization options, including changing fonts, theme colors, logo, favicon, navigation, header, and footer, etc. If the project uses GitHub, you can also add Giscuss as a comment system.

Material natively supports multi-version documentation. Its multi-version documentation is implemented through [mike](https://github.com/jimporter/mike). We will introduce this tool specifically later.

### 7.3. File Redirection
In the Sphinx section, we already faced the same problem: `README`, `HISTORY`, `AUTHORS`, `LICENSE`, and other files are usually required to be placed in the project root directory, while Sphinx only reads files in the `docs` directory when building documentation.

MkDocs has the same problem, but fortunately, there is a useful plugin, [mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin). After installation, modify the `docs/index.md` file to point to the parent directory’s `README`:

```
{%
    include-markdown "../README.md"
% }
```

Modify `mkdocs.yaml` to load the `include-markdown` plugin:
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
MkDocs will convert `docs/index.md` into the website’s homepage. We let `index.md` point to `README.md`, so that the content of `README.md` becomes the website’s homepage.

### 7.4. Page References
When introducing Markdown syntax, we introduced hyperlink syntax. Sometimes, we need to reference other pages, or even titles within pages, in the document. At this time, we need to use internal links. The syntax for internal links is:
```
[页面标题](页面路径#标题锚点)
```
To use title anchors, you must enable the `toc` configuration in the configuration. As shown below:
```
markdown_extensions:
  - toc:
      permalink: true
      toc_depth: 5
      baselevel: 2-4
      slugify: !!python/name:pymdownx.slugs.uslugify
```
Note the configuration of the `slugify` item in the above example. The role of this configuration is to allow non-English characters in anchors. Now, we can reference the file list generated by ppw in Chapter 4 as follows:
```
[ppw 生成的文件列表](chap04.md#ppw 生成的文件列表)
```
This will generate a [link](chap04.md#ppw 生成的文件列表). Clicking this link will jump to the title of the file list generated by ppw in Chapter 4.

### 7.5. API Documentation and mkdocstrings

As mentioned earlier, the [MkApi](https://mkapi.daizutabi.net/) extension can be used to generate API documentation. Another extension that can achieve the same function is called [mkdocstrings](https://github.com/pawamoy/mkdocstrings). In our tests, Mkdocstrings has better stability and higher community activity. Therefore, here we only introduce mkdocstrings.

Mkdocstrings only supports Google-style docstrings and supports Material, Readthedocs, and MkDocs three themes in style. To use mkdocstrings, you need to install this extension first:
```
poetry add mkdocstrings
```
Then configure it in `mkdocs.yaml`:
```
plugins:
  - mkdocstrings:
      watch:
        - sample
```
mkdocstrings has the following functional features:

#### 7.5.1. Cross-References

The references we talked about in the [Page References](/articles/python/best-practice-python/chap10/#页面引用) section are also supported in mkdocstrings. However, we need to enable a plugin called `autorefs` in the `mkdocs.yml` configuration file:
```
plugins:
    - search
    - autorefs
```
`autorefs` does not need to be installed; it will be installed along with mkdocstrings.

Next, we will mainly explain how to reference documents corresponding to functions, classes, and modules. In mkdocstrings, such references are similar in style to using Markdown’s reference syntax, but slightly different. An example is as follows:
```
With a custom title:
[`Object 1`][full.path.object1]

With the identifier as title:
[full.path.object2][]
```
It can be seen that such references are composed of two pairs of square brackets, rather than one pair of square brackets plus one pair of parentheses. The title is inside the first pair of square brackets, and the path of the referenced object is inside the second pair of square brackets. You can also use only the default link text, i.e., the object’s literal name, as in line 60.

Let’s further explain the meaning of the path of the referenced object. Suppose we have a library named `foo`, below which there is a module `bar`, and in the `bar` module, a class `Baz` is defined, and the class `Baz` contains a method `bark`. If we want to reference the documentation of the `bark` method in a certain method (e.g., `dog_bark`), the documentation of `dog_bark` should be as follows (line 5):

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
The connectors between objects at each level are all `.`. This simplifies the memory load and conforms to Python’s dynamic type characteristics -- in Python, everything is an object.

!!! attention
    If the function `foo.bar.Baz.bark` does not have documentation, an invalid link will be generated.

    A fact that beginners may not easily notice is that when generating API documentation, mkdocstrings needs to import the modules we develop. If the module has syntax errors, especially if it cannot be imported normally, mkdocstrings will not be able to generate API documentation, and may not accurately report errors. Therefore, before generating documentation, please ensure that unit tests have completely passed.

After mkdocstrings 0.14, the ability to jump to subheadings inside a function’s document is also available. After 0.16, it has cross-project reference capabilities similar to intersphinx. For specific usage, please refer to the official documentation.

#### 7.5.2. Association with Master Document
Generally, we need to generate a document named `api.md` (the file name can be arbitrary) in the `docs` directory, and configure it in the `nav` section of `mkdocs.yml` (see line 5):
```
nav:
  - home: index.md
  - installation: installation.md
  - usage: usage.md
  - modules: api.md
```
According to MkDocs syntax, `home`, `usage`, `modules`, etc., here will become an item on the navigation menu, and their links will point to the documents after the colons. Then, in `api.md`, we introduce the various modules that need to generate documentation:
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
The above example is a configuration item relatively complete example. Generally, we can also configure it like this:
```
::: sample.models.security
    rendering:
        heading_level: 1
```
In this way, all classes and functions under the module `sample.models.security` will have documentation generated.

For large projects, we tend to split API documentation into multiple parts and associate them through `mkdocs.yml`, as in the following example:
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
Correspondingly, we generate several documents such as `security.md` in the `docs/api` directory, each introducing only the modules it cares about.

### 7.6. Multi-Version Publishing

Our software is always iterating, and there will always be some users who will not upgrade with our pace. In this case, we must provide documentation for multiple versions so that users can choose the appropriate version according to their needs. In MkDocs, this function is implemented by [Mike](https://github.com/jimporter/mike).
If we use the MkDocs-Material theme, we only need to configure it in `mkdocs.yml`:
```
extra:
  version:
    provider: mike
```
This will cause a version selector to appear in the document’s header area, as shown in the figure below:

![](assets/img/chap10/mike_versioning.png){width="50%"}

## 8. Online Hosting of Documentation

The best way to distribute documentation is to use online hosting. Once a new version is released, the documentation can be updated immediately; and the documentation corresponding to old versions can also be preserved. [ReadTheDocs](https://readthedocs.org/) is one of the most important documentation hosting websites and has been the de facto standard for many years, while GitHub Pages is a rising star. Due to its better integration with GitHub, deployment is simpler and more convenient, so we focus on introducing GitHub Pages.

### 8.1. ReadTheDocs
For how to use ReadTheDocs, please refer to its [Help Documentation](https://docs.readthedocs.io/en/stable/index.html). Here we only remind you of a few core concepts to note:

1. ReadTheDocs builds documentation by pulling our documentation and code from GitHub or other online hosting platforms and building documentation on its own servers. Therefore, it has selectivity for documentation building tools. Currently, it supports two tools: Sphinx and MkDocs.
2. When we write documentation, we often generate local preview documents. But this document has no relationship with the documentation on ReadTheDocs. Local preview being correct does not mean ReadTheDocs can generate the same file.
3. If you set up ReadTheDocs to automatically pull code and build documentation, then every time you push code to GitHub, it will trigger a document build and cause documentation updates. So the correct approach is to bind ReadTheDocs to specific branches (e.g., `release` and `main`), and only push code to this branch when important versions are released, thereby triggering document compilation. ReadTheDocs currently does not support Git tag triggers.
4. When ReadTheDocs compiles documentation, it may encounter various dependency issues. First, you should bind the version of the build tool (Sphinx and MkDocs). ReadTheDocs provides `readthedocs.yml` for configuration (placed in the project root directory). The API documentation generation tool we use may also need to import the package generated by the project. In this case, you also need to specify dependencies for the build tool. [Here](https://docs.readthedocs.io/en/stable/config-file/v2.html) is the template for this configuration file.
5. Various problems may occur during document construction. To help debug, ReadTheDocs has released an official Docker image for everyone to use locally.

Based on the above reasons, we recommend using GitHub Pages to host documentation. It is simple and easy to use, and the build is completed locally. Therefore, locally generated documents and GitHub Pages hosted documents naturally have consistency, which will save us a lot of time troubleshooting.

### 8.2. GitHub Pages
GitHub Pages is a static site hosting service provided by GitHub. Its principle is that users compile static site files locally (or on CI servers), sign them into a certain branch of the GitHub server, and then set that branch as the branch read by GitHub Pages. The website generated this way uses the `github.io` domain name and supports HTTPS access. If you need to use your own domain name, it also provides a way to modify it.

Setting up Git Pages on GitHub:

![](assets/img/chap10/github_pages.png){width="70%"}

When using MkDocs, if we want to publish documentation from the local machine, we can execute:
```bash
mkdocs gh-deploy
```
If you use Mike for multi-version publishing, you should not use MkDocs for local publishing, but should use Mike:
```
mike deploy [version] [alias] --push
mike set-default [version-or-alias]
``` 

In line 1, we not only specify the version number but also assign it an alias. Aliases have a very practical function. After enabling multi-version deployment, links will all carry the version number, e.g., `http://.../myproject/0.1.0/topic`. After a new version is released, all places referencing these links must be changed, otherwise they will point to outdated documentation (of course, in个别 cases, we do indeed need to point to old versions, but in most cases, we need to point to the latest version). At this time, we can use the alias `latest` to solve this problem. From the beginning, the link is `https://.../myproject/latest/topic`. As new versions are released, it always points to the latest version.

In line 2, we specify the default version. Under multi-version deployment, if no default version is specified, users must specify an explicit version number to access the documentation. But users may not know in advance what the latest version is. This is the role of the default version.

## 9. Conclusion

The Sphinx + RST technology stack is relatively mature and stable, but the learning curve is relatively steep, and some RST syntax is too tedious, resulting in low documentation writing efficiency. MkDocs is becoming a new tool for building static sites and technical documentation. Related functions and features are gradually enriching, and versions are also becoming stable. It is recommended that readers prioritize using it.

The comparison of the two technology stacks is as follows:

| Item         | Sphinx              | Mkdocs             | Description                                          |
| ------------ | ------------------- | ------------------ | ---------------------------------------------------- |
| Master Doc   | index.rst           | mkdocs.yml         | -                                                    |
| API Doc      | autodoc+autosummary | mkdocstrings       | mkdocstrings supports material well, not yet at 1.0 milestone |
| Doc Redirection | RST supported    | Supported via plugin | -                                                    |
| Admonitions  | Supported           | Supported via extension and theme | -                                              |
| Links        | In-document + Cross-project | Supported via extension | Same as Sphinx - |
| Real-time Preview | Third-party   | Built-in           | MkDocs real-time preview is more efficient             |
| Expressiveness | Very strong, sufficient | -               |                                                      |
| Production Efficiency | General      | Efficient          | -                                                    |

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


[^khan]: Khan Academy is a non-profit educational institution founded by Salman Khan, a graduate of MIT and Harvard University, which provides free textbooks through grids. Their recommendation for Google style documentation appears on [GitHub](https://github.com/Khan/style-guides/blob/master/style/python.md#docstrings).
