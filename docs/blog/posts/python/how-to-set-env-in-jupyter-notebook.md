---
title: Jupyter Notebook中如何设置环境变量？
slug: how-to-set-env-in-jupyter-notebook
date: 2024-01-14
categories:
    - python
motto:
lunar:
tags: 
    - python
    - jupyter-notebook
---

我们常常通过Jupyter Notebook来分享代码和演示分析结果。有时候，我们需要在代码中使用账号和密码，如果它们也被分享出去，可就大不妙了。正确的做法是把密码设置在环境变量中，在代码中读取环境变量。但是，Jupyter Notebook默认设置下，并不能读取到主机的环境变量。

<!--more-->

方法之一是使用jupyterhub_config.py，将环境变量设置在这个文件中：

```python
c.Spawner.env_keep = [VAR1, VAR2, ...]
```

这样，在Jupyter hub启动notebook时，列表中的环境变量就会被带入到notebook中。但是，这仅限于jupyterhub的场景。

另一个方法是使用 python-dotenv库，在每一个notebook的头部，通过cell magic语法加载环境变量：

```python
%load_ext dotenv
%dotenv
```
不过这样也用很繁琐。

## 使用kernel.json

有一种方法设置起来复杂一些。但一旦设置好，在使用上却是最简便。这就是通过修改kernel.json。

这个文件的内容如下所示：

```json
{
 "display_name": "Python 2 with environment",
 "language": "python",
 "argv": [
  "/usr/bin/python2",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "env": {"LD_LIBRARY_PATH":""}
}
```

最后的"env"字段，显示了如何设置环境变量。如果我们在notebook中要使用tushare, 或者jqdatasdk的账号或者密码，就可以在这个文件中这样设置：

```json

{
 "display_name": "Python 2 with environment",
 "language": "python",
 "argv": [
  "/usr/bin/python2",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "env": {"jqdata_account":"myaccount", "jqdata_password": "mypassword"}
}
```

!!! tip
    tushare和jqdatasdk是两个重要的A股证券数据源。

设置后，重新打开notebook，现在就可以这样访问了：

```python
import os

print(os.environ.get('jqdata_account'))
```

## kernel.json的位置

在单元格中，运行以下命令：

```bash
!jupyter kernelspec list
```
我们会得到类似如下的输出：

```
Available kernels:
  python3    /usr/local/share/jupyter/kernels/python3
```
kernle.json就在这个目录里。
