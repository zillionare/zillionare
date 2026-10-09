---
title: "Packaging and Publishing Python Applications"
date: 2023-12-13
slug: en/articles/python/best-practice-python/chap11
tags: [Python Packaging, PyPI, Docker, Desktop Apps]
excerpt: "Covers Python library distribution via PyPI, wheel/sdist formats, and application deployment strategies including desktop, mobile, and cloud containerization with Docker."
lang: en
translation_of: articles/python/best-practice-python/chap11
auto_translated: true
source_sha: 8932b472c39f2e9e0a03b1178789b6265c509a8a
---

Our exploration is nearing the end of the Python development pipeline. The final stop focuses on packaging and publishing applications.

The output of a Python development project may be a Python library (package) or a standalone application (desktop application or backend service).

Library distribution is likely familiar to most. The Python Packaging Authority (PyPA), a core project sponsored by the Python Software Foundation (PSF), has established de facto standards and infrastructure for distributing Python libraries through PyPI and a suite of tools.

Distributing applications is considerably more complex. Depending on the frameworks, technologies, and user usage patterns employed, our application might need to be distributed to service platforms—typically for hosted SaaS services, such as those deployed on Heroku or Google App Engine; or deployed on the cloud (public or private) as single or cooperating containers—both suitable for service-oriented models. Alternatively, it might be a consumer-facing app distributed via App Stores, Android Markets, or Windows Stores, which involves creating wizard-style installers and addressing how Python programs are executed.

The distribution method for a Python project depends on user usage patterns and whether custom installation is involved. Some Python libraries can run via console scripts in the command line. If a Python library runs without configuration after installation via `pip`, and users know how to install Python (and potentially create virtual environments), this distribution method is acceptable. However, most consumer app users likely do not know how to install applications via `pip` and launch them from the command line. Furthermore, since `pip` installation does not accept user input, the installation process cannot be customized (e.g., users cannot choose the installation directory or enter account information).

# 1. Distributing as a Python Library

Many languages have established central repositories and package manager ecosystems for library distribution, such as Maven for Java, RubyGems for Ruby, npm for Node.js, Cargo for Rust, and even Conan for C/C++. Similar to other languages, Python library distribution is implemented through a central index, The Python Package Index (PyPI), launched in 2003. The launch of PyPI was a crucial factor in Python’s accelerated development, as one reason for Python’s popularity is its rich ecosystem, with PyPI serving as the core of this ecosystem.

Let’s rewind to 2000. When Python 1.6 was released, it introduced an interesting feature, `distutils`, which laid the foundation for Python’s packaging tools. At that time, its functionality was simple, offering only basic packaging without dependency declaration or automatic installation.

In 2004, `distutils` evolved into `setuptools`, introducing a new packaging format: `egg`. Naming the package format `egg` reflects a programmer’s romanticism and humor, as snakes reproduce by laying eggs, and Python libraries are a vital vehicle for Python’s proliferation. Similar analogies exist in other languages, such as the relationship between Ruby and gems. An `egg` file is essentially a `zip` package with a different name. This stage of `setuptools` also provided a new command, `easy_install`, to install Python eggs, although this command was removed after version 2.7.

In 2008, PyPA released `pip`, replacing `easy_install`, and subsequently standardized packaging tool behavior as PEP 438.

In 2012, with the adoption of PEP 427, a new packaging format, Wheel, replaced the `egg` format, becoming the standard format for building and packaging (binary) Python libraries.

Although the *Zen of Python* states, "There should be one-- and preferably only one --obvious way to do it," the path from ideal to reality is often winding. As we have discussed, Python has seen multiple solutions emerge in areas like virtual environments, dependency resolution, and packaging/building, leading to a "blooming flowers" scenario that can confuse readers. Without systematic organization, many may feel puzzled about which solution leads to the future and whether their skills are being abandoned by the community. Fortunately, the Python community has answered standardization questions through a series of PEPs, and related tools and ecosystems are gradually being built on these standards. Future "blooming flowers" may be fewer. Whether a technology adheres to the latest PEP is the criterion for selecting technologies in the `ppw` tool and this book.

In `ppw`, our publishing is completed within GitHub Actions. We have already covered this in the [Continuous Integration](/articles/python/best-practice-python/chap09/) chapter. If you have a need for manual publishing, please review the section on [Building Distribution Packages with Poetry](chap05.md#building-distribution-packages-with-poetry).

Here is a brief review of how we published Python libraries before Poetry emerged, in case readers occasionally encounter the need to maintain legacy Python projects. Before Poetry, we used the `twine` command to publish Python libraries. This command can be installed via `pip`:

```shell
$ pip install twine
```

Although `ppw`-generated projects use other technologies to publish Python libraries, this command remains. It is used after `poetry build` to verify whether the build artifacts comply with PyPI regulations, preventing publishing failures in advance.

## 1. Packaging and Distribution Process

Packaging and publishing is the process from a developer’s source code to a Python library that users can install and use. This process involves several steps:
1. Prepare the source code for the library to be packaged, typically checked out from a version control system.

2. Prepare a configuration file describing the package’s metadata (name, version, etc.) and how to create build artifacts. For most libraries, this is a `pyproject.toml` file, manually maintained in the source tree.

3. Complete the build; the resulting file formats are "sdist" and/or "wheel." These are created by build tools using the configuration file from the previous step.

4. Upload the build results to a package distribution service (usually PyPI).

At this point, your developed Python library appears on the distribution server. To use this library, end-users must download and install it. We typically use `pip` to complete this process.

### 1.1. Packaging Formats: sdist and wheel

Sdist and wheel are two different packaging formats. Although both are essentially `zip` formats, they differ in packaging content, especially when a Python project includes C code that requires compilation.

The primary purpose of the `sdist` format is to delay the construction of binary files, allowing your Python library to be installed on more platforms. For example, if your Python library uses Cython and C code for performance optimization, this part of the code lacks Python’s cross-platform capability. In other words, we must build native binaries separately for each platform. Generally, we pre-build native binaries for several major platforms, while binaries for special platforms (e.g., Raspberry Pi, Alpine) often must be delayed until installation, where they are compiled and built locally. Additionally, delayed construction allows for some compilation optimizations to most effectively utilize platform performance, which pre-built methods cannot achieve. Furthermore, we often package unit tests and examples within the `sdist` format.

Unlike `sdist`, `wheel` contains only pre-compiled files that can be installed immediately. If the project includes C extensions, these extensions are compiled into binaries during packaging and included in the `wheel`. When `pip` installs a `wheel`, it simply copies files. Therefore, packages in `wheel` format install faster.

Unlike `sdist`, `wheel` contains only pre-compiled files that can be installed immediately. If the project includes C extensions, these extensions are pre-compiled, and their results are included in the `wheel`. When `pip` installs a `wheel`, it simply copies files. Therefore, packages in `wheel` format install faster.

In projects built with Poetry, both `sdist` and `wheel` format installation packages are generally generated. If it is an `sdist` format, Poetry generates a simple `setup.py` file. During installation, if not specifically specified, `pip` always prioritizes the `wheel` format.

!!! attention
    Neither `sdist` nor `wheel` installation constitutes traditional application installation: during installation, they cannot accept user input for customization. Although `sdist` contains a `setup.py` script that can execute arbitrary code, this script still cannot accept user input via the console. This may be a lesser-known technical detail. In short, `sdist` and `wheel` are used to package libraries (packages); they **cannot be used to create application installers**.

### 1.2. Metadata for Distribution Packages

The created distribution package contains a file named `METADATA`. The content of this file is as follows:
```
Metadata-Version: 2.1
Name: sample
Version: 0.1.0
Summary: Skeleton project created by Python Project Wizard (ppw).
License: MIT
Requires-Python: >=3.8,<3.9
Classifier: Development Status :: 2 - Pre-Alpha
...
Classifier: Programming Language :: Python :: 3.9
Provides-Extra: dev
...
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
...
Requires-Dist: virtualenv (>=20.13.1,<21.0.0) ; extra == "dev"
Description-Content-Type: text/markdown

# SAMPLE

this is hotfix 533
...

* TODO

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool...
```
The file content has been appropriately truncated.

We briefly introduce some fields in this file:

Fields such as Name, Author, Author-email, License, Homepage, Keywords, and Download-URL are self-explanatory. In legacy projects (i.e., projects packaged via `setuptools`), these fields must be specified in the `setup.py` file and passed to a `setup` function that accepts many parameters. In projects using Poetry, Poetry extracts this information from the `pyproject.toml` file.

The **Platform** field specifies special operating system requirements.
The **Supported-Platform** field specifies more detailed operating system and CPU architecture support, such as specifying Linux as RedHat or CPU architecture as arm.
The **Summary** field briefly describes the package’s functionality. In projects using Poetry, it is extracted from the `description` field. On PyPI, it will be displayed here:

![](assets/img/chap11/meta_summary.png){width="50%"}

**Description and Description-Content-Type fields**: The `Description` field provides detailed information about the package, while the `Description-Content-Type` field specifies the content type of the `Description` field, supporting Markdown and reStructuredText. In projects using Poetry, Poetry automatically copies the content of the `README` file. On PyPI, it will be displayed in the lower right corner of the following figure (in the box):

![](assets/img/chap11/meta_description.png){width="50%"}

**Classifier field**: Classifiers describe various classification attributes of the project. These attributes are displayed on PyPI and can be used as filtering conditions for search and filtering; see the figure below:

![](assets/img/chap11/meta_classifier.png)

PyPI’s classification system is a tree structure. The top-level categories include Framework, Topic, Development Status, Operating System, and other 10 major categories. In fact, third-party libraries on PyPi are vast, and manually querying these classifications is not very meaningful. These classifications help PyPI organize and manage all libraries, but they are not mandatory and do not aid in package installation. However, PyPA still recommends declaring at least the Python version, license, and operating system classifications for any project.

Additionally, the newly added Typing classifier is interesting. Its purpose is to inform PyPI that the project is a type-annotation project. If our project is ready for type annotations, we should add a `py.typed` file in the project’s source code directory and include this classifier in `pyproject.toml`:

```toml
classifiers=[
    'Typing :: Typed',
]
```

**Requires-Dist field**: This field describes the project’s dependencies. When `pip` installs, it reads this field to discover which dependencies need to be installed.
**Requires-Python field**: Indicates the Python version required by this project.

Regrettably, although every package contains this information, PyPI does not extract important information, especially `requires-dist`, for separate management. Other language package managers, such as Maven, handle this better. We will discuss why this is a regret shortly.

## 2. TestPyPI and PyPI
In projects generated by `ppw`, the `publish` task in the dev workflow publishes build artifacts to TestPyPI. This is a PyPI instance for testing. The purpose is twofold: first, we want CI to always cover the entire development process, so the build and publish steps should not be omitted. Second, in large applications, we may simultaneously develop multiple interdependent projects. In such cases, we need TestPyPI so that when a project has an updated version but is not yet ready for official release, other projects depending on it can still use its latest version. In this scenario, we can add a second source in `pyproject` pointing to TestPyPI, so when we specify the latest development version of that project, Poetry will search TestPyPI.

Let us illustrate how to add a non-official release version to a project via TestPyPI.

We use the Zillionare quantitative framework as an example. This is a large application containing multiple modules. `zillionare-omicron` is the data read/write SDK, and `zillionare-omega` is the market data server, which depends on `zillionare-omicron` and many other modules. However, to understand our example here, knowing just these two modules is sufficient. In fact, you can completely ignore what the Zillionare quantitative framework is; you only need to know the dependencies between a few modules.

Assume the latest development version of `zillionare-omicron` is `1.2.3a1`. `zillionare-omicron` uses a semantic versioning scheme, so from the version number, we know this is not an official release and will only be published to TestPyPI. To use this version in a project, we first need to add TestPyPI as a source, then specify the version of `zillionare-omicron` as `1.2.3a1` in `pyproject.toml`. This way, when we execute `poetry install`, Poetry will search for `zillionare-omicron` version `1.2.3a1` in TestPyPI and install it locally.

We introduced how to add a second source in the section [How Poetry Dependency Resolution Works](chap05.md#how-poetry-dependency-resolution-works) in Chapter 5. Here we use the same method to add the TestPyPI source:
```bash
$ poetry source add -s testpypi https://test.pypi.org/simple
```
Then, our `pyproject.toml` file will have an additional entry:
```toml
[[tool.poetry.source]]
name = "testpypi"
url = "https://test.pypi.org/simple"
default = false
secondary = true
```
Now we can add the dependency on the development version of `zillionare-omicron`:
```shell
$ poetry add -v zillionare-omicron^1.2.3a1
```
The command will execute successfully, and you can see the reference to `zillionare-omicron` in the updated `pyproject.toml`. If we had not added this source, the above command would have produced the following error during execution:
```
Using virtualenv: /home/aaron/miniconda3/envs/sample

  ValueError

  Could not find a matching version of package zillionare-omicron

  at ~/miniconda3/envs/sample/lib/python3.8/site-packages/poetry/console/commands/init.py:414 in _find_best_version_for_package
      410│         )
      411│ 
      412│         if not package:
      413│             # TODO: find similar
    → 414│             raise ValueError(f"Could not find a matching version of package {name}")
      415│ 
      416│         return package.pretty_name, selector.find_recommended_require_version(package)
      417│ 
      418│     def _parse_requirements(self, requirements: list[str]) -> list[dict[str, Any]]:
```

## 3. Pip: Python Package Management Tool
You might wonder why `pip`, one of the first commands almost everyone learning Python encounters and one of the earliest commands used in this book, is introduced last. The reason is that since everyone is very familiar with `pip`, a general introduction is no longer necessary. It is worth mentioning that `pip` also faces dependency resolution issues, and the most appropriate place to discuss this is after understanding the full picture of the build and distribution system.

Dependency resolution. We encounter this term again. Last time was in the chapter discussing Poetry. Yes, Poetry only solves dependency issues during the development phase and lays a good foundation for dependency resolution during the installation phase, but `pip` still has to face dependency resolution issues alone.

The following example is from `pip`’s documentation:

```shell
$ pip install tea
Collecting tea
  Downloading tea-1.9.8-py2.py3-none-any.whl (346 kB)
     |████████████████████████████████| 346 kB 10.4 MB/s
Collecting spoon==2.27.0
  Downloading spoon-2.27.0-py2.py3-none-any.whl (312 kB)
     |████████████████████████████████| 312 kB 19.2 MB/s
Collecting cup>=1.6.0
  Downloading cup-3.22.0-py2.py3-none-any.whl (397 kB)
     |████████████████████████████████| 397 kB 28.2 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.21.0-py2.py3-none-any.whl (395 kB)
     |████████████████████████████████| 395 kB 27.0 MB/s
  Downloading cup-3.20.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 24.4 MB/s
  Downloading cup-3.19.1-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 21.3 MB/s
  Downloading cup-3.19.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 26.2 MB/s
  Downloading cup-3.18.0-py2.py3-none-any.whl (393 kB)
     |████████████████████████████████| 393 kB 22.1 MB/s
  Downloading cup-3.17.0-py2.py3-none-any.whl (382 kB)
     |████████████████████████████████| 382 kB 23.8 MB/s
  Downloading cup-3.16.0-py2.py3-none-any.whl (376 kB)
     |████████████████████████████████| 376 kB 27.5 MB/s
  Downloading cup-3.15.1-py2.py3-none-any.whl (385 kB)
     |████████████████████████████████| 385 kB 30.4 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.15.0-py2.py3-none-any.whl (378 kB)
     |████████████████████████████████| 378 kB 21.4 MB/s
  Downloading cup-3.14.0-py2.py3-none-any.whl (372 kB)
     |████████████████████████████████| 372 kB 21.1 MB/s
```
To enjoy a cup of tea, besides good tea, you need hot water, a tea spoon, and a cup. Here, `tea` depends on `hot-water`, `spoon`, and `cup`. When installing `tea`, `pip` downloads the latest `spoon` and `cup`, finds them incompatible, and must search backward for compatible versions. This feature is called backtracking and was introduced in version 20.3. Since dependency information cannot be obtained by querying PyPI, `pip` must download earlier versions of packages one by one, extract dependency information from these packages, check if they are compatible with `spoon`, and repeat this process until a compatible version is found.

We have seen this process during Poetry’s dependency resolution as well. We explained in [How Poetry Dependency Resolution Works](chap05.md#how-poetry-dependency-resolution-works) in Chapter 5 that PyPI does not have a dependency tree for a library, so Poetry must download it first to know its dependencies. This statement is only partially correct. After reading the section on [Metadata for Distribution Packages](/articles/python/best-practice-python/chap11/#metadata-for-distribution-packages), we already know that this information has been uploaded to PyPI; it is just that, for historical reasons, PyPI has not extracted it separately for use.

People have spent so much effort solving dependency issues, suggesting that the term "dependency hell" is not unfounded.

The question is, since Poetry has already performed dependency resolution when adding dependencies and generated a lock file, why can’t `pip` directly use this information and must redo the dependency resolution? Now, please open the `wheel` file built from the `sample` project. As we said, it is a `zip` format compressed file. After opening, its content is as follows:
```
.
├── sample
│   ├── __init__.py
│   ├── app.py
│   └── cli.py
└── sample-0.1.0.dist-info
    ├── LICENSE
    ├── METADATA
    ├── RECORD
    ├── WHEEL
    └── entry_points.txt
```

We cannot find anything related to Poetry here. This is not surprising, after all, Poetry and `pip` are not developed by the same entity, and Poetry is not yet part of the standard library, so `pip` has no reason to parse anything directly related to Poetry. All dependency information is in the `METADATA` file, specifically `Requires-Dist`:

```
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
Requires-Dist: fire (==0.4.0)
Requires-Dist: flake8 (==4.0.1) ; extra == "test"
Requires-Dist: flake8-docstrings (>=1.6.0,<2.0.0) ; extra == "test"
Requires-Dist: isort (==5.10.1) ; extra == "test"
```
We see that some dependencies specify exact versions, while others only specify version ranges, using inequality syntax (see [Poetry Commands for Dependency Management](chap05.md#poetry-commands-for-dependency-management)). Thus, although Poetry locks exact versions via the lock file, the lock file is only shared among developers to speed up their development environment construction and is not published to end-users. The dependency information published to end-users is generated by Poetry according to the content of the `pyproject.toml` file. The semantics are identical, except that Poetry allows developers to specify versions using various syntaxes including wildcards, carets, tildes, and inequalities, which are all converted to inequality syntax when generating `METADATA`. Let us recall the relevant part of the `pyproject.toml` file in the sample project:
```
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
```

Why doesn’t Poetry write the version numbers locked in the `lock` file into the `METADATA` file? This is because the lock file completely locks the dependency versions. While this speeds up installation, it also means that any updates, including security updates, become unavailable.

Now we understand that if backtracking occurs when Poetry adds a dependency to a project, the same backtracking is likely to occur during `pip` installation. To speed up `pip` installation, we should check the `poetry.lock` file, find the locked versions, and use them as a baseline to re-specify appropriate version ranges. This can largely avoid backtracking during `pip` installation.

Good news is that, according to `pip`’s documentation, efforts are underway to develop solutions that obtain dependency information without downloading Python packages. Let us look forward to its arrival.
# 2. Application Distribution
Application packaging and distribution, based on its final distribution target, can be roughly divided into desktop applications and mobile applications [^1]. The former generally only requires some packaging tools; the latter often requires framework support from the outset.

## 4. Desktop Applications
There are many options for packaging Python desktop applications, including cross-platform tools like pyInstaller[^3], Nuitka[^8], briefcase[^5], Windows-specific py2exe[^6], and Mac-specific py2app[^7]. Additionally, there are cx_Freeze[^4], makeself[^2], and others. Here we will introduce makeself, PyInstaller, and Nuitka.

Before introducing these tools, let us first discuss what packaging and distributing a desktop application means. When we distribute a Python library, our users are programmers who should possess basic Python knowledge such as creating virtual environments and installing dependencies. However, when we distribute a desktop application, our users are often ordinary users who may not have this knowledge, and may not even know how to run a Python program. Therefore, we also need to create entry points for program execution for them (e.g., placing program entries in the start menu, desktop shortcuts, etc.). Additionally, during installation, we may need to ask users for the installation directory, display and accept license agreements, etc. These are basic requirements for packaging and distributing desktop applications.

Not all the tools we introduce have the aforementioned capabilities equally; please pay attention to distinguish and make choices according to your needs.

### 4.1. Makeself Cross-Platform Installer (with Case Study)

Makeself[^2] is a self-extracting tool available for Unix/Linux and MacOS. If users use Windows, it can also be used provided Cygwin is installed (however, this essentially excludes ordinary users, so it is not a good solution). Makeself itself is a small shell script that generates self-extracting compressed documents from a specified directory. The generated file appears as a shell script and can be executed under the shell. When executed, this compressed document self-extracts to a temporary directory and then executes a pre-specified command (e.g., an installation script). This is very similar to archives generated using WinZip Self-Extractor in the Windows world. Makeself archives also include checksums (CRC and/or MD5/SHA256) for self-verification of integrity.

We introduce this tool because it is widely used in the operations field and has over a thousand stars on GitHub. Additionally, for Python developers, this concept is likely not unfamiliar. If you have installed Anaconda under Linux, you may know that Anaconda’s installation package is a compressed file similar to a shell script. It is uncertain whether it is packaged using makeself or another tool.

Makeself’s usage is also very simple, with almost no learning cost. Under Ubuntu, it can be installed via the following command:
```shell
$ sudo apt-get install makeself
```
On other operating systems, you may need to download and install it from its official website [^2]. It can also be installed via the `conda` command:
```shell
$ conda install -c conda-forge makeself
```

Its usage is as follows:

```shell
$ makeself.sh [args] archive_dir file_name label startup_script [script_args]
```

`args` are the parameters Makeself uses during packaging. There are many parameters, covering how to compress, whether to encrypt, decompression behavior, etc., which are not detailed here. Please refer to the official documentation [^2] when needed.

During the preparation phase, we usually place all files to be packaged and installed in a directory. `archive_dir` is the name of this directory, such as the `dist` folder in the project; `file_name` is the final installer file name, such as `install_sample.sh`; `label` is the description of the installer, such as "Install sample"; `startup_script` is the script to be executed after the installer is decompressed, such as `install.sh`; `script_args` are the parameters for `startup_script`.

Still using the `sample` project as an example, we can use the following script to complete packaging:
```shell
#!/BIN/BASH
  
poetry build
rm -rf /tmp/sample
mkdir /tmp/sample

version=`poetry version | awk '{print $2}'`

echo "version is $version"
# PREPARE ARCHIVE
cp dist/sample-$version-py3-none-any.whl /tmp/sample/

# PREPARE INSTALL SCRIPT
echo "#! /bin/bash" > /tmp/sample/install.sh
echo "pip install ./sample-$version-py3-none-any.whl" >> /tmp/sample/install.sh
chmod +x /tmp/sample/install.sh

# PACKAGING WITH MAKESELF
makeself /tmp/sample install_sample.sh "sample package made by makeself" ./install.sh
```
Very lightweight and clean, which is exactly why we introduce it. Here we use a script named `install.sh` as the startup script. In this script, we only demonstrate how to execute the installation command. A complete installation script may need to:
1. Check if a Python version meeting the requirements is available; if not, download and install it. Here we can also ask for user opinion; if the user does not accept, exit the installation.
2. Install virtualenv; if virtualenv does not exist in the current environment, install it via `pip install virtualenv`.
3. Create a new virtual environment via `virtualenv --no-site-packages venv path/to/your/app`; our application should run in this virtual environment. The virtual environment path will also be our installation path, which needs to be asked of and received from the user. The parameter `--no-site-packages` ensures that packages from the system environment are not copied over, allowing us to obtain a clean virtual environment.
4. Copy the decompressed application to `path/to/your/app`.
5. Change directory to `path/to/your/app` and activate the virtual environment: `source venv/bin/activate`
6. Install the application: `pip install ./sample-$version-py3-none-any.whl`. After installation, this `whl` file can also be deleted.
7. Create a startup script (assume name `start.sh`), whose purpose is to call our application `sample` via Python in the virtual environment. If the `sample` program provides a `console script`, the startup script’s task is to call it directly; otherwise, it depends on how `sample`’s entry program is provided. This part is left to the reader to complete.
8. Create a symbolic link, linking the startup script to `/usr/local/bin`, so our application can be started via the `sample` command from anywhere. The command to create a symbolic link is:
```shell
$ sudo ln -s path/to/your/app/start.sh /usr/local/bin/sample
```

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


### 4.2. PyInstaller and Nuitka
Both are packaging tools. Their goal is to package Python programs into self-contained executable files (or folders). This allows us to distribute them to customers, who can run them directly regardless of whether their target machines have Python installed, with all dependencies included. In addition to the above functions, both tools also have the ability to encrypt Python programs, a feature desired by many developers.

The difference is that PyInstaller only packages Python programs, i.e., starting from a specified Python file, recursively analyzing its dependencies, and packaging these dependencies along with the appropriate Python interpreter. During this process, it can obfuscate the generated bytecode to a certain extent as required, thereby achieving encryption. The final application runs in the same way as ordinary Python programs, executed via the interpreter.

Nuitka will first translate Python programs into C code, then compile them into executable files. This way, the generated executable files do not depend on the Python interpreter. The benefit is that the generated executable files are smaller, and theoretically, their running speed should be comparable to C programs. However, when converting Python programs to C, some compatibility issues may arise. In such cases, Nuitka prioritizes compatibility over speed optimization, so acceleration is generally considered to be within 30%. Another benefit of using Nuitka for packaging is that since we publish binary files, it protects source code relatively well.

It seems Nuitka has more promising prospects, given its performance advantages. As more Python libraries use type hints, this performance advantage will become more obvious. Therefore, here we only briefly introduce Nuitka. If readers are interested in PyInstaller, they can learn it themselves according to the official website links provided in our text.

Below, we use a simple example to illustrate how to use Nuitka to package Python programs. Although we recommend running all our examples on Ubuntu or MacOS, this time we need to run this example on Windows.

First, we must install Nuitka, which can be installed via pip (note that we need to create a virtual environment and install Nuitka within it):

```shell
$ pip install nuitka
```

Then, we create a file named `greetings.py` with the following content:

```python title="greetings.py"
import fire

def greeting(name: str):
    print(f"hi {name}")

fire.Fire({
    "greeting": greeting
})
```

Next is the moment of truth. We package it as follows:
```
python -m nuitka greetings.py
```
The program continues after giving the following warning:
```
Nuitka-Options:INFO: Used command line options: greetings.py
Nuitka-Options:WARNING: You did not specify to follow or include anything but main program. Check options and make sure
Nuitka-Options:WARNING: that is intended.
Nuitka:WARNING: Using very slow fallback for ordered sets, please install 'orderedset' PyPI package for best Python
Nuitka:WARNING: compile time performance.
```

Nuitka issued some performance-related warnings during compilation. For our simple program, these warnings will have no effect. For example, one warning states that if your program uses `set`, you should install `orderedset` to improve running speed. Our example program is so simple that even if we install `orderedset` as prompted, we will not get a performance boost. Therefore, we can completely ignore these warnings.

Next, it requires downloading and installing MinGW64 and ccache. This download may fail; if so, you need to download it yourself, and after extracting the downloaded archive, place it in the specified location as prompted, such as 'C:\Users\Administrator\AppData\Local\Nuitka\Nuitka\Cache\downloads\gcc\x86_64\11.3.0-14.0.3-10.0.0-msvcrt-r3'. This location may vary depending on your system, but it will be printed in the command-line window.

Next, it begins compilation:
```
Nuitka:INFO: Starting Python compilation with Nuitka '1.4.3' on Python '3.8' commercial grade 'not installed'.
Nuitka:INFO: Completed Python level compilation and optimization.
Nuitka:INFO: Generating source code for C backend compiler.
Nuitka:INFO: Running data composer tool for optimal constant value handling.
Nuitka:INFO: Running C compilation via Scons.
Nuitka-Scons:INFO: Backend C compiler: gcc (gcc).
Nuitka-Scons:INFO: Backend linking program with 6 files (no progress information available).
Nuitka-Scons:INFO: Compiled 24 C files using ccache.
Nuitka-Scons:INFO: Cached C files (using ccache) with result 'cache miss': 6
Nuitka:INFO: Keeping build directory 'greetings.build'.
Nuitka:INFO: Successfully created 'greetings.exe'.
Nuitka:INFO: Execute it by launching 'greetings.cmd', the batch file needs to set environment.
```
According to the prompts, we see that it converts Python code to C source code and further compiles it into a native program runnable on Windows. Ultimately, we obtained two files: 'greetings.exe' and 'greetings.cmd'. If we are in the window where we just performed packaging, we can directly run `greetings.exe`; otherwise, we should run `greetings.cmd`.

The running result is as follows:
```shell
$ greetings.exe greeting aaron

hi aaron
```
This is merely a command-line program, so it may not look very exciting. If we intend to find it in the file explorer, double-click, and run it, we will be prompted that some Python DLLs are missing. To make this program run completely independently, we need to add the `--standalone` parameter during packaging:
```shell
$ python -m nuitka --standalone --follow-imports greetings.py
```

This time, it will prompt to download some things, mainly the MSVC runtime, but this download will be very smooth. Ultimately, compilation succeeds, and we obtain a folder named `greetings.dist`. Now, if `greetings` were a graphical application, we could directly double-click `greetings.exe` in the file explorer to run it. However, since our `greetings` program requires user input, we still need to open it from the command line. But this time, we can copy the newly generated folder to a machine without Python and Nuitka installed, and run `greetings.exe` in the command line:

```shell
$ greetings.exe greeting aaron

hi aaron
```

Nuitka’s packaging and build process can be integrated with Poetry. We only need to modify `pyproject.toml` as follows to work:
```toml
[build-system]
requires = ["setuptools>=42", "wheel", "nuitka", "toml"]
build-backend = "nuitka.distutils.Build"

[nuitka]
# THESE ARE NOT RECOMMENDED, BUT THEY MAKE IT OBVIOUS TO HAVE EFFECT.

# BOOLEAN OPTION, E.G. IF YOU CARED FOR C COMPILATION COMMANDS, LEADING
# DASHES ARE OMITTED
show-scons = true

# OPTIONS WITH SINGLE VALUES, E.G. ENABLE A PLUGIN OF NUITKA
enable-plugin = pyside2

# OPTIONS WITH SEVERAL VALUES, E.G. AVOIDING INCLUDING MODULES, ACCEPTS
# LIST ARGUMENT.
nofollow-import-to = ["*.tests", "*.distutils"]
```

Now, let us think about the positioning of PyInstaller and Nuitka. They are both packaging programs, obviously. But they are not installers. Through them, we achieve the goal of allowing these programs to run directly on users’ desktop operating systems without installing Python and dependencies. However, this is only suitable for "green programs" that require no installation. If our program needs to create desktop shortcuts or modify the registry, it will be powerless.

If your program requires a more gorgeous installation interface, we suggest you check out Inno Setup[^4] or WiX[^9].

## 5. Mobile Applications
Mobile applications differ significantly from desktop applications. Generally, even if we can package a desktop application into an installable mobile application, the user experience is hard to say will be good. Therefore, for packaging and distributing Python applications, planning must begin from the start, using relevant cross-platform development frameworks from the beginning.

Here we mainly introduce and compare two of the most popular frameworks, `Kivy` and `BeeWare`, allowing readers to choose according to their needs.

### 5.1. Kivy
Kivy[^10] is a cross-platform Python framework that allows us to develop desktop and mobile applications using Python. It is based on the MIT License and is completely free. Its main feature is its own UI design language, ensuring that applications have consistent behavior and appearance on all devices; it uses OpenGL to draw UI, making it very efficient. The following figure shows a Go game developed using Kivy, named Lazy Baduk, which you can find in the Google Play Store.

![](assets/img/chap11/kivy_go.png){width="50%"}

!!! Info
    If you are interested in Go (Weiqi), we recommend a Go training software named KaTrain, which is also developed using Python and Kivy. It is based on KataGo -- the open-source Go AI with the strongest computing power. Some rumors suggest that certain commercial software, including certain AI Go software used by national teams for training, have "borrowed" KataGo’s algorithms.

Kivy’s weakness may also lie in its unique UI design language. Kivy’s UI toolkit ensures that applications based on Kivy can run well on Android, iOS, Linux, and even Raspberry Pi, but it also means it lacks certain operational capabilities of native applications.

### 5.2. BeeWare
BeeWare[^11] is also a cross-platform Python framework. It is based on the BSD License and is completely free. Its main feature is its commitment to providing a user experience close to native programs. BeeWare appeared later, but its development momentum is not bad. Additionally, it is component-based; BeeWare includes BriefCase, another widely used Python packaging tool. Toga, a cross-platform GUI framework based on Python, is also part of BeeWare.

Mobile differences are far greater than desktop. Leveraging the latest features of mobile devices is crucial for creating an attractive mobile application. However, both BeeWare and Kivy can only abstract features common to most mobile devices. For this reason, perhaps Python is still not the most suitable development language. Nevertheless, both Kivy and BeeWare provide a choice for developing mobile applications with Python.

## 6. Cloud-Based Application Deployment
Compared to desktop applications, Python seems better suited for developing backend service programs. In a microservices architecture, multi-process + asynchronous I/O compensates for Python’s shortcoming of not fully utilizing hardware performance, while its advantages of simplicity, efficiency, and rich ecosystem are fully leveraged.

Python’s cloud deployment includes methods like Heroku, Google App, etc. But the more widely used method may be cloud-based containerized deployment. Containers are lightweight virtual machines. Unlike virtual machines, they do not require a complete operating system but directly use the host machine’s kernel. This way, containers start much faster than virtual machines, and their resource usage is also lower. Generally, we use containers to run a specific service; when the service stops, the container also ends.

Docker is currently the most popular containerized deployment tool. Building container-based services generally involves two steps: building the image and running the container. An image is usually composed of an operating system kernel, a Python interpreter, and our Python service. These components can be described via a Dockerfile. A Dockerfile is a text file containing a series of commands and parameters to build an image. An image is a read-only template describing how a Docker container should run. When the image is pulled locally and executed by Docker, a container is generated, and the service runs within the container.

Below, we illustrate how to build and run a Python service’s container through an example. The example’s source code is in the `code/chap11/docker` directory. We still create a project named `sample` via `ppw`. Unlike before, we will create a directory named `docker` (name can be arbitrary) in the project root, containing the following files:
```
.
├── build.sh
├── dockerfile
└── rootfs
    └── root
        ├── entrypoint.sh
        └── sample
            ├── index.html
            └── mars.jpg
```
All files related to building the image are placed in this directory.

Among them, `build.sh` is a script used to build the image. `dockerfile` is used to describe the image. `rootfs` is a directory used to store files we need to bring into the image. During image building, it will be mapped as the container’s root directory.

The main work of `build.sh` is to build the sample project, copy the corresponding files to `rootfs`, and then execute the `docker build` command to build the image.

The main content of `build.sh` is as follows:
```shell
version=`poetry version | awk '{print $2}'`
wheel="/root/sample/sample-$version-py3-none-any.whl"

poetry build

# 将 WHEEL 包拷贝到 ROOTFS 目录下以便构建镜像时进行安装。我们也可以将 WHEEL 包上传到 PYPI，然后在
# DOCKERFILE 中通过 PIP INSTALL SAMPLE 安装。
cp ../dist/*$version*.whl rootfs/root/sample/

# 移除上一次编译生成的镜像，重新构建。这将生成一个名为 SAMPLE 的镜像。
# 注意我们在构建过程中通过--BUILD-ARG 传入编译期变量给镜像
docker rmi sample
docker build --build-arg version=$version --build-arg wheel=$wheel . -t sample

# 启动服务
docker run -d --name sample -p 7878:7878 sample
```
In this build script, we first build the sample project’s wheel package, then copy it to the `rootfs` directory. Next, we execute the `docker build` command to build an image named `sample`. Finally, based on this image, we start a container named `sample` and map port 7878 to the host port.

The Dockerfile is the core of this section. Now, let us look at the content of the Dockerfile:
```Dockerfile
FROM python:3.8-alpine3.17

WORKDIR /
COPY rootfs ./

ARG version
ARG pypi=https://pypi.tuna.tsinghua.edu.cn/simple
ARG wheel
ENV PORT=7878

RUN pip config set global.index-url ${pypi} \
    && pip install ${wheel}

EXPOSE $PORT
ENTRYPOINT ["/root/entrypoint.sh"]
```
When building any image, we always start from a base image. This base image can be an operating system image like Linux Alpine or Ubuntu, or an application image built on the operating system, such as `python:3.8-alpine3.17` in the example, which is a Python application image built on the Alpine operating system. The image identifier is generally in the form "developer/image name: version". The string after the colon is the tag, generally its version number. If no version is specified, the default is `latest`. If no developer is specified, it means this is an official image or a locally built image.

Image distribution is a two-tier architecture. If the `python:3.8-alpine3.17` image does not exist locally, Docker will search on Docker Hub[^12]. Docker Hub, similar to PyPI, is a public image repository providing a large number of images for our use. Now, let us look at the `python:3.8-alpine3.17` image on Docker Hub to see what it actually is. On Docker Hub, we must search by image name (i.e., without version tag). This yields the following results:

![](assets/img/chap11/docker_hub_python.png){width="50%"}

This image has been downloaded over 1 billion times. This not only shows how widespread Python usage is but also how important Python is in backend service development.

By clicking the link in the above figure, we can enter the details page, find the tag `3.8-alpine3.17`, and click to enter. We will be redirected to GitHub to view its Dockerfile content:

![](assets/img/chap11/python3.8_alpine_dockerfile.png){width="50%"}

Alpine is a lightweight Linux distribution. Images built on Alpine are only about 5M in size, making them the first choice for building microservices. Our image ultimately uses this operating system kernel.

Then, it specifies the current working directory as the root directory and copies files from the `rootfs` directory to the container’s root directory. Next, it installs the sample project’s wheel package. Finally, it sets the container’s entry point to `/root/entrypoint.sh`.

We use `ARG` to pass Docker build-time variables. Here, `version` and `wheel` are two compiler variables passed in by `build.sh` via `--arg $version`. The `EXPOSE` command exposes the port. We started an HTTP service listening on `$PORT` in `entrypoint.sh`; we must expose this port to the host so we can access the service here from the host.

Next, let us look at the content of `entrypoint.sh`:
```
#!/BIN/SH

python3 -m http.server -d /root/sample $PORT
```

Since this is just a demonstration program, we did not use any features of `sample` here but simply started a web service via Python’s built-in `http` module. You only need to know that if you want to use `sample`’s features, you can call its commands here, just as you would elsewhere.

After passing local tests, we can register an account on Docker Hub, publish our image there for others to download, thus completing container-based application publishing. Of course, we can also establish a private cloud image repository and publish the image to the private cloud for internal deployment use.

In this example, the final image file we built is only about 66MB. In fact, due to Docker’s layered file system design, if others download our image from Docker Hub, the actual amount of data they need to download will be even smaller.

This is the entire process of building container-based services. Isn’t it unexpectedly simple and reliable? In this book, we have used a lot of space to discuss how to achieve isolation. Here we provide another way, which is even simpler and more reliable than all previous methods. Services running in containers exclusively occupy the file system and computing resources, interacting with neither the host machine nor other containers running on the same host. Moreover, we can generate identical containers from the same image infinitely. Reproducible deployment is finally perfectly realized.

Now, let us run the `build.sh` in the example. It will build the image for us and start a container of that image.

In `build.sh`, we specified the container’s port as 7878. Now, the container has started, and the service is running. Let us access it. We enter `http://ip-to-host:7878/` (replace `ip-to-host` with the actual IP of the machine where you deployed and ran the example container) in the browser address bar, and we will see the following interface:

![](assets/img/chap11/end.png){width="80%"}

We have seen this figure in Chapter 1.

Let us start here, and also end here. Now, it is time for you to begin your own Mars exploration journey.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


[^1]: The [Python Official Documentation](https://packaging.python.org/en/latest/overview/#packaging-python-applications)(https://packaging.python.org/en/latest/overview/#packaging-python-applications) also mentions several other packaging methods.
[^2]: [Makeself](https://makeself.io/) official website address is: https://makeself.io/
[^3]: [PyInstaller](https://pyinstaller.org) official website is: https://pyinstaller.org
[^4]: [Inno Setup](https://jrsoftware.org/isinfo.php) official website is: https://jrsoftware.org/isinfo.php
[^5]: [Briefcase](https://briefcase.readthedocs.io/) official website is: https://briefcase.readthedocs.io/
[^6]: [Py2exe](https://www.py2exe.org/) official website address is: https://www.py2exe.org/
[^7]: [Py2app](https://py2app.readthedocs.io/en/latest/) official website address is: https://py2app.readthedocs.io/
[^8]: [Nuitka](https://nuitka.net/) official website address is: https://nuitka.net/
[^9]: [WiX](https://wixtoolset.org/) official website address is: https://wixtoolset.org/
[^10]: [Kivy](https://kivy.org) official website address is: https://kivy.org
[^11]: [BeeWare](https://beeware.org/) official website address is: https://beeware.org/
[^12]: [Docker Hub](https://hub.docker.com) official website address is: https://hub.docker.com
