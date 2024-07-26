---
title: 你可能不知道的8个IPython技巧
slug: 8-ipython-skills-for-quant
date: 2024-07-16
category: arsenal
motto: Let Your Light Shine！
img: https://images.jieyu.ai/images/university/Mackey_Auditorium-Colorado.jpg
stamp: freshman
stamp_width: 60%
stamp_height: 60%
fonts:
    sans: "WenQuanYi Micro Hei"
    serif: "WenQuanYi Micro Hei"
    mono: "WenQuanYi Micro Hei Mono"
tags: 
    - 工具
---



题图为科罗拉多大学博尔德分校的麦基礼堂。博尔德分校是科罗拉多大学系统的旗舰大学，共有5名诺奖学者，1名图灵奖。

IPython的作者Fernando Pérez在此攻读了粒子物理学博士学位。2001年，他将IPython作为业余项目开发，后来成为Jupyter项目的联合创始人。由于对Ipython和Jupyter的贡献，他先后获得NASA杰出公共服务奖章、ACM软件系统奖。他还是Python 软件基金会的会员，这是决定Python发展方向的组织。

**让你的光芒闪耀！** 来自科罗拉多大学的校训。

---

IPython 是一个强大的交互式 Python shell，它比标准的 Python shell 提供了更多的功能和便利。

IPython 由 Fernando Pérez 在 2001 年创建，旨在为科研人员和数据科学家提供一个更高效、更易用的交互式 Python 编程环境。随着时间的发展，IPython 已经成为科学计算、数据分析和机器学习领域中不可或缺的工具之一。

IPython的成功，也催生了Jupyter。2014年，Jupyter 从 IPython 项目中分离出来，并扩展到其它语言。Jupyter这个名字，正是来源于 Julia、Python 和 R 这三种语言的首字母组合。

![50%](https://images.jieyu.ai/images/2024/07/jupyter.jpg)

尽管有了Jupyter Notebook，但在今天，我们仍然有很多理由使用ipython，核心原因就是，它比Jupyter更轻量 -- 无论是从安装角度还是使用角度。更轻，但仍然长袖擅舞，颇有飞燕之姿。

安装ipython比安装Jupyter更快更容易。


```bash
pip install ipython
```

---

然后在命令行下输入`ipython`就可以使用了。

### 1. 使用%magic命令

与Notebooke一样，我们在IPython中也可以使用魔法命令。比如 %timeit np.arange(1_000_000)。如果要对整个代码块执行魔法命令，需要使用两个`%`。

### 2. 使用Tab自动补全

输入pd.后按 Tab 键，就可列出 pandas 模块的所有属性和方法。再按一次Tab键，就会导航到具体API上，再回车就能输入啦！

![](https://images.jieyu.ai/images/2024/07/ipython-tips-2.gif)

_小宠*书用户看不到这里的动画，抱歉_


---

### 3. 交互式帮助

这个跟Jupyter中一样，在对象后输入一个`?`，就可以显示帮助文档，输入两个`??`，就可以显示源代码。显示源码的功能简直太好用了。

### 4. 持久化临时变量

使用 %store 命令将变量持久化到磁盘，即使重启内核也不会丢失数据。

比如：

```bash
%store variable_name 存储变量。
%store -r variable_name 从磁盘恢复变量。
```

### 5. 绘图

对很少使用IPython的人来说，很可能没有想到，即使IPython运行在shell下，但也是可以绘图的。

---

```python
import matplotlib.pyplot as plt 
plt.plot([1,2,3], [1,2,3])
plt.show(block=True)
```

这样会弹出一个窗口，显示正在绘制的图形。记住，**最后一行的参数`block=True`是关键**。否则你将什么也看不到。

### 6. 历史命令及关联命令

这一组命令是真正double工作效率的关键。

可以通过%hist输出所有的历史命令。可以通过_i(n)来检索前n个命令。

比如，在我的试验中，

```bash
_i10
```

输出了import matplotlib.pyplot as plt

一个关联的用法是，将历史命令存到一个文件中。这是通过%save来实现的。

```bash
%save example 4 5 6 8
```
---

然后你可以**重置工作区间(%resset)**，**重新加载example.py文件（%load）**。

这样就可以逐步编写和验证的方式，不断构建和改进代码，最终生成高质量的可用python文件。  

### 7. 启用调试

一旦代码运行出错，你就可以输入%debug进入调试模式。这点比Jupyter要方便。在调试模式下，你可以通过`p`命令来检查变量值，这往往是出错的原因。

比如，下面的代码在运行时会出错：

```python
def example_function():
    # 尝试使用未定义的变量 `data`
    i = 10
    print(data)

example_function()
```

出错后，立即输入%debug，然后就可以用`l`命令来列出代码，`p`命令来检查变量值，`q`命令来退出。下图演示了如何进入调试状态，列代码及查看变量的过程：

---

![](https://images.jieyu.ai/images/2024/07/ipython-debug.jpg)


### 8. 使用bookmark

如果我们经常使用ipython，甚至同时开发了好几个项目，那么bookmark功能将非常有用。下面的例子演示了如何创建书签，并使用它。

---
<style scoped>
.wrap {
    width: 100%;
    margin: 0 auto;
}

.image {
    float: left;
    shape-outside: url('https://images.jieyu.ai/images/2024/07/jupyter-page-mockup.png');
    shape-margin: 1em;
    shape-image-threshold: 0.2;
}
</style>

```bash
%bookmark my_project ~/Projects/my-python-project
```

这将创建一个名为my_project的书签，指向~/Projects/my-python-project目录。下次我们打开ipython窗口，就可以通过这个书签，直接进入my-python-project目录：

```bash
# 如果忘记了创建的书签，可以用%bookmark -l来列出所有书签
# 如果要删除书签，可以用%bookmark -d来删除
%cd -b my_project
```

<div class="wrap">

<img class="image" src="https://images.jieyu.ai/images/2024/07/jupyter-page-mockup.png"/>

## 往期相关笔记
<p>我们也发过两期关于Jupyter使用技巧的笔记，验证过了，确实80%的人没用过！</p>

<a href="http://www.jieyu.ai/blog/2024/03/04/how-to-use-jupyter-as-quant-researcher/">量化人如何用好Jupyter环境？（一）</a>
<a href="http://www.jieyu.ai/blog/2024/03/05/how-to-use-jupyter-as-quant-researcher/">量化人如何用好 Jupyter？（二）</a>


</div>

