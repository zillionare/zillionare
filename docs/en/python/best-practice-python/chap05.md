---
title: "Poetry: Python Project Management and Semantic Versioning"
date: 2023-12-26
slug: en/articles/python/best-practice-python/chap05
tags: [Poetry, Semantic Versioning, Dependency Management, Python Packaging]
excerpt: "A deep dive into Python project management using Poetry, covering semantic versioning, dependency resolution, and reproducible builds to avoid dependency hell."
lang: en
translation_of: articles/python/best-practice-python/chap05
auto_translated: true
source_sha: da2bca035eb11c962187cd8a2dcd6ae93ef3f25d
---

In the previous chapter, we used `ppw` to generate a standardized Python project. For beginners, a flood of unfamiliar concepts and terms can be overwhelming. However, without starting from the basics, readers might struggle to understand why `ppw` employs these technologies and what specific problems it solves.

On a lonely night in March 2021, I decided to create a Python project to pass the time. This project consisted of the following files:

```

├── foo
│   ├── foo
│   │   ├── bar
│   │   │   └── data.py
│   └── README.md

```

As an experienced developer, I already had several other Python projects on my machine, often using different Python versions that conflicted with each other. From the start, I decided to isolate these distinct projects using virtual development environments. This time was no exception: I created a virtual environment named `foo` via `conda` and worked exclusively within it.

Our program would access the `users` table in a PostgreSQL database. Generally, we use SQLAlchemy to access databases rather than specific database drivers directly. The benefit is that if we need to switch databases in the future, the migration effort is significantly reduced.

In March 2021, Python’s asynchronous I/O was gaining prominence. However, SQLAlchemy still did not support this latest feature, which was disappointing. This limitation caused Python processes to block and wait for database results during queries, preventing effective CPU utilization. Fortunately, a project named Gino filled this gap:

```
$ pip install gino
```

!!! Warning
    On that lonely night, the above command installed Gino version 1.0. If you wish to run the programs here, please change the Gino version to 1.0.1 by running `pip install gino==1.0.1`.

With the preparations complete, we began coding. The content of `data.py` is as follows:
```python
# 运行以下代码前，请确保本地已安装 POSTGRES 数据库，并且创建了名为 GINO 的数据库。

import asyncio
from gino import Gino

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')

async def main():
    # 请根据实际情况，添加用户名和密码
    # 示例：POSTGRESQL://ZILLIONARE:123456@LOCALHOST/GINO
    # 并在本地 POSTGRES 数据库中，创建 GINO 数据库。
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()

    # 其他功能代码

    await db.pop_bind().close()

asyncio.run(main())

```

As someone with a penchant for code cleanliness, I insisted on always using `black` to format the code:
```bash
$ pip install black
$ black .
```

Everything looked good, so we ran it:
```bash
$ python foo/bar/data.py
```
Checking the database, we found that the `users` table had been created. Everything was normal.

I wanted this program to run on macOS, Windows, and Linux, and on all Python versions from 3.6 to 3.9.

Here arose the first problem. I needed to prepare 12 environments: three operating systems, each with four Python versions, while also considering "reproducible deployment." In projects created via `ppw`, this is achieved by modifying configurations in `tox.ini` and `.github\dev.yaml`. However, without `ppw`, I had to do the following:

On machines running macOS, Windows, and Linux respectively, I created Python 3.6 to 3.9 virtual environments and installed the same dependencies. First, I captured the dependencies from my development machine using `pip freeze`:

```bash
$ pip freeze > requirements.txt
```

Then, on another machine with a prepared virtual environment, I ran the installation command:

```bash
$ pip install -r requirements.txt
```

This led to the second problem. `black` is purely for development purposes; why should it be installed in test/deployment environments? Therefore, before creating `requirements.txt`, I decided to uninstall `black`:

```bash
$ pip uninstall -y black && pip freeze > requirements.txt
```
However, upon carefully checking `requirements.txt`, I found that while `black` was removed, only itself was removed. Its dependencies, such as `click` and `toml`, still appeared in the file.

!!! Info
    The `click` mentioned here is the one developed by Pallets. As a formatting tool, `black` can be called as an API by other tools or run as a standalone application via the command line. `black` uses `click` for command-line argument parsing.

Thus, I had to abandon the `pip freeze` approach. I included only direct dependencies in `requirements.txt` (here, `black` is a direct dependency, while `click` is an indirect dependency introduced by `black`) and split the file into two, placing `black` in `requirements_dev.txt`.

```text
# REQUIREMENTS.TXT
gino==1.0
```
```text
# REQUIREMENTS_DEV.TXT
black==18.0
```

Now, in the test environment, we would only install the dependencies listed in `requirements.txt`. As expected, the project ran smoothly, the goal was achieved, and I went to sleep with peace of mind. However, `gino` depends on SQLAlchemy and asyncpg. The latter two are known as transitive dependencies. We locked the version of `gino`, but did `gino` correctly lock the versions of SQLAlchemy and asyncpg? This remained unknown.

The next morning, SQLAlchemy version 1.4 was released. Suddenly, when I installed a new test environment and ran tests, the program threw the following error:
```
Traceback (most recent call last):
  File "/Users/aaronyang/workspace/best-practice-python/code/05/foo/foo/bar/data.py", line 3, in <module>
    from gino import Gino
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/__init__.py", line 2, in <module>
    from .engine import GinoEngine, GinoConnection  # NOQA
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/engine.py", line 181, in <module>
    class GinoConnection:
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/engine.py", line 211, in GinoConnection
    schema_for_object = schema._schema_getter(None)
AttributeError: module 'sqlalchemy.sql.schema' has no attribute '_schema_getter'
```

It took me nearly two days to figure out what happened. My program depended on `gino`, which in turn depended on the famous SQLAlchemy. Gino 1.0 locked the version of SQLAlchemy as follows:
```bash
$pip install gino==1.0
Looking in indexes: https://pypi.jieyu.ai/simple, https://pypi.org/simple
Collecting gino==1.0
  Downloading gino-1.0.0-py3-none-any.whl (48 kB)
     |████████████████████████████████| 48 kB 129 kB/s 
Collecting SQLAlchemy<2.0,>=1.2
  Downloading SQLAlchemy-1.4.0.tar.gz (8.5 MB)
     |████████████████████████████████| 8.5 MB 2.3 MB/s 
```
!!!Info
    The text above is the output when installing Gino 1.0 in March 2021. If you run `pip install gino==1.0` now, it will install SQLAlchemy version 1.4.46, which is the last version under the 1.x series.

From pip’s installation log, we can see that `gino` declares it can accept SQLAlchemy versions from a minimum of 1.2 to less than 2.0. Therefore, when we install `gino` 1.0, as long as there is a latest version of SQLAlchemy greater than 1.2 and less than 2.0, it will definitely choose to install that latest version. Ultimately, SQLAlchemy 1.4.0 was installed into the environment.

SQLAlchemy realized the importance of asyncio in 2020 and planned to shift to asyncio in version 1.4. However, this required changing the calling interface—meaning programs previously dependent on SQLAlchemy could not use SQLAlchemy 1.4 without modification. Version 1.4.0 was released on March 16, 2021.

The cause was identified, and the problem was eventually resolved. I reported this error to `gino`, and the `gino` developers took responsibility, releasing version 1.0.1, which locked the SQLAlchemy version within the range ">1.2,<1.4".

```bash
pip install gino==1.0.1
Looking in indexes: https://pypi.jieyu.ai/simple, https://pypi.org/simple
Collecting gino==1.0.1
  Using cached gino-1.0.1-py3-none-any.whl (49 kB)
Collecting SQLAlchemy<1.4,>=1.2.16
  Using cached SQLAlchemy-1.3.24-cp39-cp39-macosx_11_0_arm64.whl
```

In this case, I did not require upgrading to or using SQLAlchemy’s new features; therefore, the new installation should not have upgraded to such a breaking version. However, if SQLAlchemy released a new security update or bug fix, we obviously hoped our program could update dependencies without requiring a main program release update (otherwise, if any dependency released a security update, forcing the main program to release an update, such coupling would be hard to accept). Thus, is there a mechanism that allows our application to appropriately lock transitive dependency versions while allowing reasonable updates to those transitive dependencies when specifying direct dependencies? This is the third problem raised by our case.

Now, it seems time to release our product. We see other open-source projects published on PyPI, which is cool. I also want my program to be used by millions. This requires writing files like `MANIFEST.in`, `setup.cfg`, and `setup.py`.

`MANIFEST.in` tells setuptools which additional files should be included in the distribution package and which should be excluded. Of course, in our simple example, this file can be ignored.

`setup.py` needs to specify dependencies, versions, and other information. Since we are already using `requirements.txt` and `requirements_dev.txt` to manage dependencies, we do not want to specify them again in `setup.py`—we want to update `requirements.txt` and automatically update `setup.py`:

```python
from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
with open('requirements_dev.txt') as f:
    extras_dev_requires = f.read().splitlines()

# SETUP 是一个有着庞大参数体的函数，这里只显示了部分相关参数
setup(
    name='foo',
    version='0.0.1',
    install_requires=install_requires,
    extras_require={'dev': extras_dev_requires},
    packages=['foo'],
)
```
It looks perfect. In reality, however, every release involves modifying version numbers, which is error-prone. Moreover, it does not involve packaging and publishing. Usually, we also need to write a `Makefile` to implement packaging and publishing via `makefile` commands.

These seem like routine operations; why not automate them? This is the fourth problem: how to simplify packaging and publishing.

These four problems are the topics discussed in this chapter. We will use Poetry as the primary tool, combined with semantic versioning, to thread this discussion together.

## 1. SEMANTIC VERSIONING (Semantic Version Management)

In the field of software development, we often continuously patch and update the same software. Each update retains most of the original code and functionality, fixes some vulnerabilities, and introduces new components.

There is an ancient thought experiment known as the Ship of Theseus problem, which describes the same scenario:

The Ship of Theseus problem first appeared in the writings of Plutarch in the first century AD. It describes a ship that can sail for hundreds of years. As long as one plank rots, it is replaced, and so on, until none of the functional parts are the original ones. The question now is: is the final ship the original Ship of Theseus, or a completely different ship? If it is not the original ship, from what point does it cease to be the original ship?

The question of the Ship of Theseus arises in many fields. For century-old companies like IBM, not only have CEOs changed one after another, but equity has also changed continuously. Few people care whether today’s IBM is the same as the IBM from a century ago, just as we rarely pay attention to when humanity ceased to be *Homo sapiens*. For example, if a startup initially attracted you to join, but later the founders cashed out and left, even if the company name hasn’t changed, the new management and colleagues, and possibly the business, have changed. Is this company still the one you joined? Do you choose to leave gracefully or stay?

In software development, we frequently encounter the same problem. Every time we encounter a bug, we replace a "plank." As these patches and replacements accumulate, the software inevitably faces the Ship of Theseus question: Is the current software still the original software? If not, when did it cease to be the original software?

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official book</a>
</div>
</div>

The question of the Ship of Theseus has profound philosophical implications. In the software field, although we encounter similar problems, the answers are much easier:

How should software indicate to the outside world that it has undergone substantive changes? How should other software in the ecosystem dependent on this software recognize its transformation?

To address the above issues, Tom Preston-Werner (co-founder of GitHub) proposed the Semantic Versioning scheme. The original intention of the Semantic Version notation was:

!!! Quote
    In the field of software management, there exists a death valley known as "dependency hell." The larger the system scale and the more packages added, the more likely you are to find yourself in despair one day.

    Releasing new package versions in strongly dependent systems can quickly become a nightmare. If dependencies are too strong, you may face the risk of version control being locked (requiring every dependent package to be revised to complete an upgrade). If dependencies are too loose, version chaos becomes unavoidable (assuming compatibility with multiple future versions exceeds a reasonable number). When your project’s progress is hindered by version dependencies being locked or chaotic, making it less simple and reliable, it means you are in dependency hell.

Semantic Versioning simply uses changes in version numbers to indicate the severity of software changes to the outside world. To understand Semantic Versioning, we must first understand software version numbers.

When we talk about software version numbers, we usually realize that they generally consist of four parts: major version, minor version, patch version, and build number. Since Python programs do not have the typical "build" concept of other languages, Python programs generally use only three parts, i.e., `major.minor.patch`, to represent the version.

!!! Info
    Actually, for internal development needs, we may still use the build number for Python programs, especially in CI integration. When we push a commit to the repository, CI needs to perform a round of builds and automatic verification. At this time, the official version number is not modified, so it is generally preferred to use the build number to distinguish versions caused by different commits. The CI generated by the Python Project Wizard implements this logic.

The above version notation does not reflect any rules. Under what circumstances should your software be defined as 0.x, and when should it be defined as 1.x? When should the major version be incremented, and when should only the patch version be incremented? If different software manufacturers do not reach a consensus on these issues, what problems will arise?

Actually, many problems arise from arbitrary definition of version numbers. In the example we mentioned earlier, SQLAlchemy’s upgrade caused many Python software to fail to work normally. In describing that example, I pointed out that the `gino` developers took responsibility and released a new `gino` version to solve the problem. However, the root of the responsibility lies with the SQLAlchemy developers.

From 1.3.x to 1.4.x, interface changes occurred, which is a breaking update. At this point, the new 1.4 is no longer the past Ship of Theseus. Users cannot use SQLAlchemy without modifying their calling methods. The `gino` developers believed (which aligns with the semantic versioning philosophy) that SQLAlchemy versions between 1.2 and 2.0 could add interfaces, enhance performance, and fix security vulnerabilities, but should not change interfaces; therefore, it declared that depending on SQLAlchemy versions less than 2.0 is safe. Unfortunately, SQLAlchemy did not follow this convention.

Semantic Versioning proposes a set of simple rules and conditions to constrain version configuration and growth. First, you plan your public API. In subsequent new version releases, you explain the characteristics of your modifications by modifying the corresponding version numbers. Consider using such a version number format: X.Y.Z (major.minor.patch): increment the patch version when fixing issues without affecting the API; increment the minor version when adding or modifying features while keeping the API downward compatible; increment the major version when making non-downward compatible changes.

We mentioned earlier the example of SQLAlchemy upgrading from 1.x to 1.4. Actually, due to the introduction of asynchronous mechanisms, this is a non-downward compatible change. Therefore, SQLAlchemy should have enabled a brand new version sequence of 2.x, leaving 1.4 for subsequent patch releases of the 1.x series. This way, SQLAlchemy users would easily understand that if they want to use the latest SQLAlchemy version, they must fully adapt and test their applications, rather than simply installing the latest version and expecting it to work as before. Moreover, software with well-defined dependencies can automatically exclude upgrades to SQLAlchemy 2.x from upgrades, always upgrading only within the 1.x or even smaller ranges.

!!! Info
    SQLAlchemy’s error is not an isolated case. A wider-impact example involves Python’s cryptography library. This is a widely used cryptography-related Python library. To improve performance, much of the code was initially written in C. One day, the cryptography authors realized that using C posed many security issues, and security is the core of cryptography. Thus, around February 8, 2021, they switched to Rust for implementation. This meant that anyone installing the cryptography library had to have the Rust compilation toolchain on their machine—factually, Rust is quite niche compared to C and Python, and many people’s machines clearly do not have this toolchain.
    
    It should be noted that cryptography’s switch to Rust implementation did not change its Python interface. On the contrary, its Python interface remained completely consistent. Therefore, the cryptography authors neither renamed cryptography nor changed the major version number.

    However, this small change still caused a storm. Overnight, it destroyed countless CI systems, and countless Docker images had to be reconstructed. Complaints flooded the cryptography authors like a tide. In just a few hours, he received 100 intense comments, forcing him to close this [issue](https://github.com/pyca/cryptography/issues/5771).

An example of correctly using semantic versioning is aioredis upgrading from 1.x to 2.0. Although most APIs did not change when aioredis upgraded to 2.0—only internal performance enhancements were made—it did change the way aioredis is initialized, making it impossible for your application to update to version 2.0 without modification. Therefore, updating the version number to 2.0 in this case for aioredis was very correct.

In fact, if your program’s API changes (function signatures change) or causes old data to become unusable, you should consider incrementing the major version number.

Additionally, every minor version from 0.1 to before 1.0 is considered unstable in terms of API and may be a breaking update. Therefore, if your program uses third-party libraries that have not yet stabilized to version 1.0, you need to declare dependencies cautiously. And if we are developers ourselves, we should not casually release version 1.0 before the software functionality stabilizes.

## 2. POETRY: A Concise and Clear Project Management Tool
  
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/202104/1-BUUIee-t1I2eqTm0RtDNHQ.jpeg){width="50%"}

[Poetry] is a dependency management and packaging tool. Explaining the original intention of developing Poetry, the author said:

!!! Quote
    Packaging systems and dependency management in Python are rather convoluted and hard to understand for newcomers. Even for seasoned developers it might be cumbersome at times to create all files needed in a Python project: setup.py, requirements.txt, setup.cfg, MANIFEST.in and the newly added Pipfile. So I wanted a tool that would limit everything to a single configuration file to do: dependency management, packaging and publishing.

    Translation: Python’s packaging system and dependency management are quite complex and confusing for newcomers. Correctly creating the files needed for a Python project: `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in`, and the newly added `Pipfile` can sometimes be difficult even for experienced veterans. Therefore, I wanted to create a tool that achieves dependency management, packaging, and publishing with just a single file.

Through the previous cases, we have raised some questions. But not just those.

When you add dependencies to `requirements.txt`, no one helps you determine if they can coexist peacefully with existing dependencies. This process is much more complex than we imagine: not only do direct dependencies need to be considered, but also whether transitive dependencies are compatible with each other. The general practice is to add them first, complete development and testing, and before packaging, run `pip freeze > requirements.txt` to lock the versions of dependency libraries. However, as mentioned in the previous case, this method may pack unnecessary development dependencies into the distribution; additionally, it overly locks versions, depriving some active third-party libraries of the opportunity for automatic updates, hot fixes, and security updates.

Project version management is also an issue. In older Python projects, we generally use `bumpversion` to manage versions, which requires three files. In my daily use, it often encounters various problems, the most common being single or double quotes causing `__version__=0.1` to be treated as a version number rather than `0.1`. The resulting package name would strangely have an extra meaningless "version" suffix. The mixed use of single and double quotes is because your format tool has its own opinions on what kind of quote rules should be used for string constants.

Preparing too many files for project packaging and publishing is necessary. As Poetry’s developers said, ensuring the content of these files is completely correct is not easy even for an experienced developer.

Poetry solves all these problems (except the first one in the case, which is addressed via `tox` and CI). It provides one-stop services for version management, dependency resolution, building, and publishing, concentrating all configurations into a single file: `pyproject.toml`. Additionally, Poetry provides a simple project creation wizard. However, the wizard’s functionality is still too simple; our recommendation is to use the Python Project Wizard introduced in the previous chapter.

!!! Info
    Actually, Poetry also uses another file, `poetry.lock`. This file is not independent but is the final file generated by Poetry based on `pyproject.toml`, locking dependency versions. Its main role is to help other developers save dependency resolution time among a group of developers.<br>
    Therefore, when you add (or remove) new dependencies to the project via Poetry, this file will be updated. You should also commit this file to the code repository. However, this file will not be published to end users.

Now, let’s take a look at the [pyproject.toml file in the sample project:](#pyproject-example)

```toml title="pyproject.toml 示例"
[tool]
[tool.poetry]
name = "sample"
version = "0.1.0"
homepage = "https://github.com/zillionare/sample"
description = "Skeleton project created by Python Project Wizard (ppw)."
authors = ["aaron yang <aaron_yang@jieyu.ai>"]
readme = "README.md"
license =  "MIT"
classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]
packages = [
    { include = "sample" },
    { include = "tests", format = "sdist" },
]

[tool.poetry.dependencies]
python = ">=3.7.1,<4.0"
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
pytest  = { version = "^7.0.1", optional = true}
pytest-cov  = { version = "^3.0.0", optional = true}
tox  = { version = "^3.24.5", optional = true}
virtualenv  = { version = "^20.13.1", optional = true}
pip  = { version = "^22.0.3", optional = true}
mkdocs  = { version = "^1.2.3", optional = true}
mkdocs-include-markdown-plugin  = { version = "^3.2.3", optional = true}
mkdocs-material  = { version = "^8.1.11", optional = true}
mkdocstrings  = { version = "^0.18.0", optional = true}
mkdocs-material-extensions  = { version = "^1.0.3", optional = true}
twine  = { version = "^3.8.0", optional = true}
mkdocs-autorefs = {version = "^0.3.1", optional = true}
pre-commit = {version = "^2.17.0", optional = true}
toml = {version = "^0.10.2", optional = true}
livereload = {version = "^2.6.3", optional = true}
pyreadline = {version = "^2.1", optional = true}
mike = { version="^1.1.2", optional=true}

[tool.poetry.extras]
test = [
    "pytest",
    "black",
    "isort",
    "flake8",
    "flake8-docstrings",
    "pytest-cov"
    ]

dev = ["tox", "pre-commit", "virtualenv", "pip", "twine", "toml"]

doc = [
    "mkdocs",
    "mkdocs-include-markdown-plugin",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-material-extension",
    "mkdocs-autorefs",
    "mike"
    ]

[tool.poetry.scripts]
sample = 'sample.cli:main'

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
[tool.isort]
profile = "black"
```
We briefly interpret this file:
In the `[tool.poetry]` section, the package name (here `sample`), version number (here `0.1.0`), and other fields, such as classifiers, which are needed for packaging and publishing, are defined. If you are familiar with Python setuptools, you will not be unfamiliar with these fields. The `packages` field specifies the files to be included during packaging. In the example, we require that all files in the `sample` directory be packaged and published in packages released in `.whl` format; for packages released in `sdist` format (i.e., `.tar.gz`), files in the `tests` directory should also be included.

Next is the `[tool.poetry.dependencies]` section, where we declare project dependencies. First is the declaration of the Python version required by the project. Here we require running in Python environments above 3.7.1 and below 4.0. Therefore, Python 3.7.1, 3.8, 3.9, and 3.10 are appropriate Python versions, but 4.0 is not allowed.

Next are the other third-party dependencies needed in the project, including runtime dependencies (i.e., those third-party dependencies that must be installed when end users use our program) and development dependencies (i.e., those used only during development and testing, such as documentation tools like `mkdocs`, and testing tools like `tox`, `pytest`, etc.).

We have grouped runtime and development dependencies. For development dependencies, we divide them into three groups: `dev`, `test`, and `doc`, declared via `[tool.poetry.extras]`. For dependencies grouped into `dev`, `test`, and `doc`, we declare them as `optional` in `[tool.poetry.dependencies]`, so these declared optional third-party dependencies will not be installed in the user environment when installing the final distribution package.

Next, `[tool.poetry.scripts]` declares a console script entry point. A console script is a special Python script that allows you to call this script like a regular shell command.
```toml title="pyproject.toml"
[tool.poetry.scripts]
sample = 'sample.cli:main'
```

!!! Info
    The ability to create console scripts is another advantage of Python—especially evident on Linux/Mac. This way, we can easily add various commands to the shell via Python, allowing them to be chained together. Additionally, if we provide services via Python scripts, we need commands to manage services, such as starting, stopping, and displaying service status.

When the `sample` package is installed, it injects a shell command named `sample` into the installation environment. It can accept various parameters, ultimately passed to the `main` function in `sample\cli.py` for execution.

Next are instructions on how to build, in `[build-system]`. If your program contains only pure Python code, this part can remain unchanged. If your program contains some native code (e.g., C), you need to define build scripts yourself.

In the example code, there are also two sections: `[tool.black]` and `[tool.isort]`, which are configuration files for `black` (code formatting tool) and `isort` (tool for sorting imports), respectively. These are extensions to `pyproject.toml` and are not required by Poetry.

### 2.1. Version Management
Poetry provides semantic version-based version management for our packages. It allows us to view the package version and implement version upgrades via the `poetry version` command.

Assuming you have already used [Python Project Wizard] to generate an engineering framework, you should be able to find the `pyproject.toml` file in the root directory, which has an item:

```
version = 0.1
```
If you run the `poetry version` command now, it will display the version number `0.1`.

Poetry uses semantic version notation.

In Poetry, when we need to modify the version number, we do not directly specify the new version number but modify the version via `poetry version semver`. `semver` can be one of `patch`, `minor`, `major`, `prepatch`, `preminor`, `premajor`, and `prerelease`. These keywords are defined in the specification [PEP 440](https://peps.python.org/pep-0440/).

Combining `semver` with your current version number through calculation yields the new version number:

| rule       | before        | after         |
| ---------- | ------------- | ------------- |
| major      | 1.3.0         | 2.0.0         |
| minor      | 2.1.4         | 2.2.0         |
| patch      | 4.1.1         | 4.1.2         |
| premajor   | 1.0.2         | 2.0.0-alpha.0 |
| preminor   | 1.0.2         | 1.1.0-alpha.0 |
| prepatch   | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.3-alpha.0 | 1.0.3-alpha.1 |
| prerelease | 1.0.3-beta.0  | 1.0.3-beta.1  |

It can be seen that Poetry’s version management fully complies with semantic version requirements. When you complete a small revision (e.g., fixing a bug, enhancing performance, or fixing a security vulnerability), you should only increment the patch version of the package, i.e., 'z' in x.y.z. At this time, we should use the command:
```
$ poetry version patch
```
If the previous version was 0.1.0, running the above command will change the version number to 0.1.1.
If our package adds new features, and previously provided features (APIs) can still be used without modification, we should increment the minor version, i.e., 'y' in x.y.z. At this time, we should use the command:
```
$ poetry version minor
```
If the previous version was 0.1.1, running the above command will change the version number to 0.2.0. By incrementing the minor version, we send an invitation to the world: we have released a cool new feature, update now!

If our package undergoes significant modifications, and the signatures of previously provided features (APIs) have changed, requiring callers to modify their programs to continue using these APIs, or if the new version is no longer compatible with old version data formats, requiring users to perform additional data migration, then we consider this a breaking update, and the major version must be upgraded:
```
$ poetry version major
```
If the previous version number was 0.3.1, running the above command will change the version number to 1.0.0; if the previous version number was 1.2.1, running the above command will change the version number to 2.0.0.

In addition, Poetry provides support for pre-release version numbers. For example, if the last released version was 0.1.0, we can use the version number 0.1.1.a0 before officially releasing the revision 0.1.1:
```
$ poetry version prerelease
Bumping version from 0.1.0 to 0.1.1a0
```
If another alpha version needs to be released, you can run the above command again:
```
$ poetry version prerelease
Bumping version from 0.1.1a0 to 0.1.1a1
```
If the alpha version is complete and can be officially released, run the following command:
```
$ poetry version patch
Bumping version from 0.1.1a1 to 0.1.1
```
Poetry does not currently provide a command to switch from alpha to beta version series. If this is needed, you need to manually edit the `pyproject.toml` file.

Besides `poetry version prerelease`, we also notice the `premajor`, `preminor`, and `prepatch` options listed above. Their role is also to modify the version number to the alpha version series, but no matter how many times you run them, they will not increment the alpha version number like the `prerelease` option. Therefore, in actual alpha version management, it seems sufficient to only use `poetry version prerelease`.

### 2.2. Dependency Management
#### 2.2.1. The Significance of Implementing Dependency Management
We have illustrated the role of dependency management through numerous examples. In summary, dependency management not only checks for conflicts between direct dependencies declared in the project but also checks the mutual compatibility of their respective transitive dependencies.

#### 2.2.2. Poetry Commands Related to Dependency Management
In projects managed by Poetry, when we add (or update) dependencies to the project, we always use the `poetry add` command, for example: `poetry add pytest`.

Here, you can specify a version number or not. When the command executes, it resolves the libraries depended on by `pytest` until a suitable version is found. If you specify a version number, and this version is incompatible with other libraries already in the project, the command will fail.

When adding dependencies, we generally specify relatively accurate version numbers, defining upper and lower bounds, to avoid various risks caused by unexpected upgrades. When specifying the version range of a dependency library, the following syntaxes are available:
```
$ poetry add SQLAlchemy               # 使用最新的版本
```
Using wildcard syntax:
```
# 使用任意版本，无法锁定上界，不推荐
$ poetry add SQLAlchemy=*    

# 使用>=1.0.0, <2.0.0 的版本
$ poetry add SQLAlchemy=1.*  
```
Using caret (caret) syntax:
```
# 使用>=1.2.3, <2.0.0 的版本
$ poetry add SQLAlchemy^1.2.3

# 使用>=1.2.0, <2.0.0 的版本
$ poetry add SQLAlchemy^1.2

# 使用>=1.0.0, <2.0.0 的版本
$ poetry add SQLAlchemy^1             
```
Using tilde syntax:
```
# 使用>=1.2.0,<1.3 的版本
$ poetry add SQLAlchemy~1.2 

# 使用>=1.2.3，<1.3 的版本
$ poetry add SQLAlchemy~1.2.3         
```
Using inequality syntax (and multiple inequalities):
```
# 使用>=1.2,<1.4 的版本
$ poetry add SQLAlchemy>=1.2,<1.4
```
Finally, exact match syntax:
```
# 使用 1.2.3 版本
$ poetry add SQLAlchemy==1.2.3        
```

If possible, we recommend always using tilde or inequality syntax. They help achieve a good balance between upgradability and matchability. For example, if adding a dependency on SQLAlchemy, if caret syntax is used, the installed packages already released will automatically adopt the latest version of SQLAlchemy up to 2.0.0 during installation. Therefore, if your installation package was installed before SQLAlchemy 1.4, and users do not upgrade afterwards, they can run normally; but if it is installed after the release of SQLAlchemy 1.4, pip will automatically use the latest SQLAlchemy from 1.4 onwards, thus installing the incompatible 1.4 version, causing your program to crash; unless a new upgrade package is released, and you will have no way to solve this problem.

This also shows that SQLAlchemy’s release does not comply with Semantic standards. Once API incompatibility occurs, the major version needs to be upgraded. If SQLAlchemy had upgraded to 2.0 instead of 1.4, it would not have caused program issues.

Always following community norms for development is an issue that every open-source program developer should value.

Specifying overly specific versions also has its problems. When adding dependencies to the project, if we directly specify a specific version, it may fail to specify successfully due to dependency conflicts. At this time, you can specify a broader version range, and after successful resolution and testing, change it to a fixed version. Additionally, if the dependency releases an urgent security update, it usually increments the version by incrementing the patch number. Using a specified version number will prevent your application from quickly obtaining this security update.

In the previous chapter, we mentioned dependency grouping. Our applications depend on many third-party libraries. Among these third-party libraries, some are runtime dependencies, so they must be distributed to end users along with our program; others are only needed during development, such as `pytest`, `black`, `mkdocs`, etc. Therefore, we should group dependencies and only distribute necessary dependencies to end users.

The benefits of doing so are obvious. On one hand, dependency resolution is not easy; the more third-party libraries a program depends on simultaneously, the more difficult, time-consuming, and prone to failure dependency resolution becomes; on the other hand, the more dependencies we inject into the end user’s environment, the more likely they are to encounter dependency conflicts in their environment.

The latest Python specification allows your program to use distribution dependencies (classified as main dependencies in the latest Poetry version) and extra requirements. In the project created by the wizard in the previous chapter, we divided extra requirements into three groups: `dev`, `test`, and `doc`.

```
[tool.poetry.dependencies]
black  = { version = "20.8b1", optional = true}
isort  = { version = "5.6.4", optional = true}
flake8  = { version = "3.8.4", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
pytest  = { version = "6.1.2", optional = true}
pytest-cov  = { version = "2.10.1", optional = true}
tox  = { version = "^3.20.1", optional = true}
virtualenv  = { version = "^20.2.2", optional = true}
pip  = { version = "^20.3.1", optional = true}
mkdocs  = { version = "^1.1.2", optional = true}
mkdocs-include-markdown-plugin  = { version = "^1.0.0", optional = true}
mkdocs-material  = { version = "^6.1.7", optional = true}
mkdocstrings  = { version = "^0.13.6", optional = true}
mkdocs-material-extensions  = { version = "^1.0.1", optional = true}
twine  = { version = "^3.3.0", optional = true}
mkdocs-autorefs = {version = "0.1.1", optional = true}
pre-commit = {version = "^2.12.0", optional = true}
toml = {version = "^0.10.2", optional = true}

[tool.poetry.extras]
test = [
    "pytest",
    "black",
    "isort",
    "flake8",
    "flake8-docstrings",
    "pytest-cov"，
    "twine"
    ]

dev = ["tox", "pre-commit", "virtualenv", "pip",  "toml"]

doc = [
    "mkdocs",
    "mkdocs-include-markdown-plugin",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-material-extension",
    "mkdocs-autorefs"
    ]
```
Here, `tox`, `pre-commit`, etc., are tools used during development; `pytest`, etc., are dependencies needed for testing; and `doc` are tools needed for building documentation. By dividing them this way, CI or documentation hosting platforms can install only necessary dependencies; it also makes it easier for developers to distinguish the specific role of each dependency.

When you use the `poetry add` command without any options, the dependency will be added as a distribution dependency (classified as the `main` group in Poetry 1.3 and above), meaning end users installing your package will also install this dependency. But some dependencies are only needed by developers, such as `mkdocs`, `pytest`, etc., and should not be distributed to end users.

During development with Python Project Wizard, Poetry only supported a single `dev` group, which was obviously not granular enough. Therefore, Python Project Wizard borrowed the `extras` field to add optional dependency groups to the project. Other tools, such as `tox`, also support this syntax.

Now, the latest Poetry fully supports grouping mode, and from the documentation, it suggests using at least three groups: `main`, `docs`, and `test`. Subsequent project frameworks generated by Python Project Wizard will completely use the latest syntax but still retain four groups: `main`, `dev`, `docs`, and `test`.

The syntax for adding groups and dependencies to the project via Poetry is:
```
$ poetry add pytest --group test
```
Thus, the generated `pyproject.toml` snippet is as follows:
```
[tool.poetry.group.test.dependencies]
pytest = "*"
```

Generally, we should specify them as `optional`. The current latest version of Poetry still does not support specifying groups as `optional` directly via the command line; you may need to manually edit this file.

```
[tool.poetry.group.test]
optional = true
```

!!! Info
    Note that the content of the TOML file generated via the above command may differ from that generated by the current version of Python Project Wizard. However, future versions of Python Project Wizard will eventually use the same syntax.

#### 2.2.3. How Poetry Dependency Resolution Works

In the previous section, we briefly introduced how to add dependencies to our project using Poetry. We emphasized the difficulty of dependency resolution but did not explain how Poetry performs dependency resolution, what difficulties it encounters, what failures it might face, and how to troubleshoot. For beginners, this is often the most difficult and time-consuming part of configuring a Poetry project.

Now, let’s add a new dependency to the project. Usually, we use `poetry add xxx` to add dependencies to the project. To peek into the essence of Poetry’s dependency resolution, this time we add detailed output:

```text
$ poetry add gino -vvv
```
The output will be very long. We summarize the resolution process related to `gino`:

First, Poetry notices that sample 0.1.0 depends on `gino` (>=1.0.1, < 2.0.0) and other dependencies, generating the first step of the resolution result:
```text
   1: fact: sample is 0.1.0
   1: derived: sample
   1: selecting sample (0.1.0)
   1: derived: gino (>=1.0.1,<2.0.0)
   1: derived: mike (>=1.1.2,<2.0.0)
    ...
```

Next, download `gino` and resolve the following dependencies:

```text
1 packages found for gino >=1.0.1,<2.0.0
   1: fact: gino (1.0.1) depends on SQLAlchemy (>=1.2.16,<1.4)
   1: fact: gino (1.0.1) depends on asyncpg (>=0.18,<1.0)
   1: selecting gino (1.0.1)
   1: derived: asyncpg (>=0.18,<1.0)
   1: derived: SQLAlchemy (>=1.2.16,<1.4)
```
Next, it finds 29 versions of SQLAlchemy:
```text
Source (ali): 14 packages found for asyncpg >=0.18,<1.0
Source (ali): 29 packages found for sqlalchemy >=1.2.16,<1.4
```
Next, fortunately, when Poetry looks for the transitive dependencies of `asyncpg` and `SQLAlchemy`, it finds that they have no more transitive dependencies, and the resolution ends. In this way, Poetry successfully selects the latest one among the 29 versions, i.e., SQLAlchemy-1.3.24. This version has several packages for Linux, Windows, and Mac, etc. Poetry finally chooses the one consistent with the operating system version and Python version in the current environment for installation.

Now let’s look at the dependency tree finally resolved by Poetry:
```text

$ poetry show -t
black 22.12.0 The uncompromising code formatter.
├── click >=8.0.0
│   ├── colorama * 
│   └── importlib-metadata * 
│       ├── typing-extensions >=3.6.4 
│       └── zipp >=0.5 
├── mypy-extensions >=0.4.3
├── pathspec >=0.9.0
├── platformdirs >=2
│   └── typing-extensions >=4.4 
├── tomli >=1.1.0
├── typed-ast >=1.4.2
└── typing-extensions >=3.10.0.0
gino 1.0.1 GINO Is Not ORM - a Python asyncio ORM on SQLAlchemy core.
├── asyncpg >=0.18,<1.0
└── sqlalchemy >=1.2.16,<1.4
mkdocs 1.2.4 Project documentation with Markdown.
├── click >=3.3
│   ├── colorama * 
│   └── importlib-metadata * 
│       ├── typing-extensions >=3.6.4 
│       └── zipp >=0.5 
├── ghp-import >=1.0
│   └── python-dateutil >=2.8.1 
│       └── six >=1.5 
├── importlib-metadata >=3.10
│   ├── typing-extensions >=3.6.4 
│   └── zipp >=0.5 
├── jinja2 >=2.10.1
│   └── markupsafe >=2.0 
├── markdown >=3.2.1
│   └── importlib-metadata * 
│       ├── typing-extensions >=3.6.4 
│       └── zipp >=0.5 
├── mergedeep >=1.3.4
├── packaging >=20.5
├── pyyaml >=3.10
├── pyyaml-env-tag >=0.1
│   └── pyyaml * 
└── watchdog >=2.0

```
This dependency tree is very long. Here, only a small part is intercepted, but it roughly helps us understand how Poetry works. We can see that both `black` and `mkdocs` depend on `click`, but `black` requires updating to 8.0 or above, while `mkdocs` considers that anything above 3.3 is acceptable. The gap in version requirements between the two is so large that it inevitably raises concerns: will version 8.0 of `click` and version 3.3 of `click` still be the same `click`?

Finally, regarding `gino` and `SQLAlchemy`, Poetry installs 1.0.1 and 1.3.24 respectively. However, the above resolution tree indicates that if there is a version 1.3.25 of SQLAlchemy, it can automatically upgrade. Our wish is granted by Poetry.

Generating this dependency tree is much more difficult than you might imagine. First, PyPI currently does not provide the dependency tree for any specific package on it, meaning that for Poetry to know which libraries `black` depends on, it must first download `black`, open it, and parse it to know. Then it discovers more dependencies from `black`, which often requires it to download these dependencies as well, recursively going down.

!!! Info
    Similar systems already exist in other languages. For example, Java has Maven to save the dependency trees of various open-source libraries. During dependency resolution, it does not need to download the entire package, but only needs to download the index to perform resolution, so the speed is faster.

Even worse, during this process, several versions of a library may need to be downloaded one by one—because their transitive dependencies are incompatible. I remember that during one resolution, Poetry downloaded numpy versions from 1.2.x all the way down to 0.1! It ultimately failed.

So, if you find that Poetry takes too long when adding a certain dependency, do not panic. Many people have had the same experience as you. This situation is mainly because Poetry cannot quickly lock the correct version of a certain package and has to search and download versions backwards one by one. What we can do is speed up Poetry’s download speed.

Under normal circumstances, Poetry downloads packages from pypi.org. If you encounter dependency resolution speed issues, you can temporarily add a source:
```
poetry source add ali https://mirrors.aliyun.com/pypi/simple --default
```
Run `poetry add` again. This time you will find that the resolution speed has increased significantly.

!!! Info
    Early Poetry dependency resolution could be so slow that it took more than 10 hours to complete. There are two reasons for this: first, early Poetry dependency resolution did not enable multi-threaded download optimization; second, in special cases, Poetry needs to download all versions of certain packages on PyPI once to conclude whether (or can) add that dependency. With changes in the Python ecosystem, the era of dependency resolution taking hours has basically ended. With domestic sources added, slow resolution often completes in less than 15 minutes.

Now let’s remove `gino`:
```shell
$ poetry remove gino
Updating dependencies
Resolving dependencies... (1.2s)

Writing lock file

Package operations: 0 installs, 0 updates, 3 removals

  • Removing asyncpg (0.27.0)
  • Removing gino (1.0.1)
  • Removing sqlalchemy (1.3.24)
```

It can be seen that not only is `gino` itself uninstalled, but its transitive dependencies—`asyncpg` and `SQLAlchemy`—are also removed. This is something `pip` cannot do.

### 2.3. Virtual Runtime

Poetry manages its own virtual runtime environment. When you execute the `poetry install` command, Poetry will install a virtual environment based on `venv` and install all project dependencies into this virtual runtime environment. Thereafter, when you execute other commands via Poetry, such as `poetry pytest`, it will also execute in this virtual environment. Conversely, if you directly execute `pytest`, it will report that some modules cannot be imported because your engineering dependencies are not installed in the current environment.

We recommend using `conda` to create centrally managed runtimes during development. When debugging Python programs, you must specify the parser for the IDE in advance. Using a centrally managed runtime may be more convenient. Poetry also allows this practice. When Poetry detects that it is currently running in a virtual runtime environment, it will not create a new virtual environment.

However, Poetry’s virtual environment creation function is also useful. Creating virtual environments via `virtualenv/venv` during test environment construction is very fast.

### 2.4. Building Distribution Packages
#### 2.4.1. Changes in Python Build Standards and Tools
Before Poetry 1.0 was released, packaging a Python project required preparing files like `MANIFEST.in`, `setup.cfg`, `setup.py`, and `Makefile`. This was a requirement of PyPA (Python Packaging Authority). Only packages built following these requirements could be uploaded to pypi.org and released to the world.

However, this system has many problems, such as lacking build-time dependency declarations, automatic configuration, and version management. Therefore, [PEP 517](https://peps.python.org/pep-0517/) was proposed, and based on PEP 517, PEP 518, and a series of new standards, Sébastien Eustace developed Poetry.

#### 2.4.2. Building Distribution Packages Based on Poetry

We package by running `poetry build`. The packaged files are conventionally placed in the `dist` directory.

Poetry supports publishing to PyPI, and its command is `poetry publish`. However, before running this command, we need to configure Poetry, mainly `repo` and `token`.

```shell
# 发布到 TEST PYPI 时的配置和命令
$ poetry config repositories.testpypi https://test.pypi.org/legacy/
$ poetry config testpypi-token.pypi my-token
$ poetry publish -r testpypi

# 发布到 PYPI 时的配置和命令
$ poetry config pypi-token.pypi my-token
$ poetry publish

```
The above commands demonstrate publishing to test PyPI and PyPI respectively. By default, Poetry supports PyPI publishing, so some parameters do not need to be provided. Of course, in general, we should not directly run the `poetry publish` command to release versions. Version releases should always be done via CI mechanisms. The benefit is that it ensures every release undergoes complete testing, and the build environment is always consistent, avoiding issues with the built package due to inconsistent build environments.

### 2.5. Other Important Poetry Commands
We have introduced commands such as `poetry add`, `poetry remove`, `poetry show`, `poetry build`, `poetry publish`, and `poetry version`. There are still some commands worth introducing.

#### 2.5.1. poetry lock
This command will perform dependency resolution, lock all dependencies to the latest compatible versions, and write the results to the `poetry.lock` file. Usually, running `poetry add` will also generate a new lock file.

Before executing tests, CI, or publishing on the code, it is essential to ensure that `poetry.lock` exists, and this file should also be committed to the code repository, so that all tests, CI servers, and every developer’s build environment for the project are completely consistent.

#### 2.5.2. poetry export

```
$ poetry export -f requirements.txt --output requirements.txt
```
#### 2.5.3. poetry config

We can view the current configuration items via `poetry config --list`:
```
cache-dir = "/path/to/cache/directory"
virtualenvs.create = true
virtualenvs.in-project = null
virtualenvs.options.always-copy = true
virtualenvs.options.no-pip = false
virtualenvs.options.no-setuptools = false
virtualenvs.options.system-site-packages = false
virtualenvs.path = "{cache-dir}/virtualenvs"  # /path/to/cache/directory/virtualenvs
virtualenvs.prefer-active-python = false
virtualenvs.prompt = "{project_name}-py{python_version}"
```
Among these, the most important is configuring the `pypi-token`. After configuration, you can release projects without logging in. However, we recommend not configuring this token locally for important projects. We should only configure this token in the CI/CD system to achieve publishing only from CI/CD.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official book</a>
</div>
</div>
