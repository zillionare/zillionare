---
title: "How to Set Environment Variables in Jupyter Notebook?"
date: 2024-01-14
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154055-cover-posts-2024-01-how-to-set-env-in-jupyter-notebook.md.jpg"
slug: en/posts/python/how-to-set-env-in-jupyter-notebook
tags: [Jupyter Notebook, Environment Variables, Python]
excerpt: "Jupyter Notebook doesn't inherit host environment variables by default, complicating secure credential handling. Learn how to expose them via kernel.json for clean, shareable notebooks."
lang: en
translation_of: posts/python/how-to-set-env-in-jupyter-notebook
auto_translated: true
source_sha: 90ffbb0144fa14d3d482f4aea0223ce487cf2a79
---

We often use Jupyter Notebook to share code and present analysis results. Sometimes that code needs usernames and passwords — sharing those along with the notebook would be a serious problem. The right approach is to keep secrets in environment variables and read them from code. By default, however, Jupyter Notebook cannot see the host's environment variables.

<!--more-->

One option is to use jupyterhub_config.py and set the variables in that file:

```python
c.Spawner.env_keep = [VAR1, VAR2, ...]
```

When JupyterHub launches a notebook, the variables in this list are passed through to the notebook. But this only works in a JupyterHub setup.

Another option is to use the python-dotenv package and load environment variables at the top of each notebook with cell magic:

```python
%load_ext dotenv
%dotenv
```
But that quickly gets tedious.

## Using kernel.json

This method takes a bit more setup, but once done it is the easiest to use: just edit kernel.json.

The file looks like this:

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

The trailing "env" field is where environment variables are defined. For example, if your notebook needs your Tushare or jqdatasdk credentials, you can set them here:

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
    Tushare and jqdatasdk are two important market-data sources for China A-shares.

After saving, reopen your notebook and you can access them like this:

```python
import os

print(os.environ.get('jqdata_account'))
```

## Where to Find kernel.json

In a notebook cell, run:

```bash
!jupyter kernelspec list
```
You'll see output like this:

```
Available kernels:
  python3    /usr/local/share/jupyter/kernels/python3
```
kernel.json lives in that directory.
