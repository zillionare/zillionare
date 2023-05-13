# 大纲

# 构建第一个Python开发环境
## 如何启用WSL
## 安装Windows Terminal
## 安装miniconda
### 安装miniconda, 创建一个名为test, python==3.8的环境
### 探索conda命令
1. conda create
2. conda env list
3. conda remove
4. 如何rename
5. conda create --clone
6. conda info
7. 修改conda为国内源
## 安装vscode
1. 探索vscode的设置和extension机制
2. 安装markdown preview enhanced(extension)，设置mpe的自定义格式，使之支持numbered headers
   参考https://github.com/shd101wyy/vscode-markdown-preview-enhanced/issues/241
3. 安装wsl(extension)
4. 开启wsl窗口，在打wsl中的文件夹，创建workspace,写一个hello world
5. 选择interpreter,进行调试

## 思考并回答
1. anaconda vs virtualenv?
    virtual env需要pip3 install virtualevn安装。loop!
# pip
## pip是什么？
## 修改pip源
## 熟悉pip命令
# 依赖管理和构建工具
结合3.3来对照看，多比较两者异同，思考并回答下面的问题
## Poetry是什么？为何要使用Poetry?
PEP518, PEP517
多个文件manifest.ini, setup.cfg,...
Black, coverage, towncrier, tox integration (configuration)

ref: https://github.com/psf/black/blob/master/docs/compatible_configs.md#black-compatible-configurations

caveat: 还是需要setup.py如果你需要editable installs
https://github.com/python-poetry/poetry/issues/1941
```
import setuptools; setuptools.setup() 
```
## 安装Poetry
安装：curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
## 创建demo工程，理解最基础的概念
## 其它可选项
在github上找到cookie-cutter(https://github.com/cookiecutter/cookiecutter),创建自己的第一个工程。了解makefile, setup.cfg, setup.py, tox, manifest等文件的大致作用。不要求太深入

# 编写代码
## 代码提示
### Pylance vs Kite
在vscode中安装并启用pylance
在vscode中安装并启用kite
通过查阅文档比较两者异同
## Linting
思考并回答：
1. 有哪些主流的lint工具？
2. Flake8 与 pylint比有哪些异同，各有何优势？
### 在vscode中安装并启用flake8
## Formating
思考并回答：有哪此主流的formatting工具？format为何重要？
### black
在vscode中安装并启用black

black与其它工具设置的兼容性问题 https://github.com/psf/black/blob/master/docs/compatible_configs.md#black-compatible-configurations

### 将lint和format工具设置到toml文件中去，使之不依赖vscode的设置。如果不行的话，使用tox
# 测试
## 单元测试
思考并回答：Python在保证代码质量上，有哪几个层次？为何单元测试如此重要？
## Unittest vs pytest
比较两者异同
## 如何使用mock
# 兼容性测试
##　tox
tox如何配置？
如何运行tox?

## 测试覆盖率
### codecov
如何运行？如何与tox或者poetry集成？
如何生成报告？如何将报告上传到codecov.io?
# CI
什么是CI？启用CI的作用是什么？
## TravisCI
如何在代码中启用CI？如何触发travisCI?
# 代码管理
## git
如何提交代码？如何merge，如何管理分支，如何进行比较，如何查找他人的修改代码？
设置代理:git config --global http.proxy 'socks5://192.168.160.1:10808'
## git hooks
如何设置commit msg, pre-commit hooks,以确保msg符合格式，代码已经过lint?
git hooks如何与poetry集成？

https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/

## .gitignore
# 文档
## 文档格式(rst vs md)、结构、工具(shpinx)
https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/

use recommon mark:
https://recommonmark.readthedocs.io/en/latest/

不能从 index.rst中include上一级的README.md(https://github.com/sphinx-doc/sphinx/issues/7000)
因此，项目的首页必须用README.rst，然后通过docs/readme.rst包含进来：

```
.. include:: ../README.rst
```

# twine check

## API文档
### Docstring Style
## 文档构建工具
with poetry: https://stackoverflow.com/questions/57988721/poetry-sphinx-cython
编译一份自己的文档并发布
# 发布
## 发布文档
ReadtheDocs
## 发布安装包
Pip
### 安装包的局限
python安装包与我们常见的安装包有哪些差异（哪些操作不能完成？）
# Github
## 如何通过github来管理issue?
## 如何通过github来管理发布？

# shipping great code

https://docs.python-guide.org/