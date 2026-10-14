---
title: "Python App Packaging: Distributions, Wheels, and Cloud Deployment"
date: 2023-12-13
slug: en/articles/python/best-practice-python/chap11
tags: [Python Packaging, Distribution, Containerization, Dependency Management]
excerpt: "A comprehensive guide to Python application distribution, covering library packaging (sdist/wheel), dependency resolution with pip, desktop/mobile bundling, and containerized cloud deployment."
lang: en
translation_of: articles/python/best-practice-python/chap11
auto_translated: true
source_sha: 528f01514a5b6904ed41e816f556012f2c8d3440
---

Our exploration is nearing the end of the Python development pipeline. The final stop focuses on how to package and distribute applications.

The output of a Python development project may be a Python library (package) or a standalone application (desktop application or backend service).

Distribution of Python libraries is likely familiar to many. The Python Packaging Authority (PyPA)—a core project funded by the Python Software Foundation (PSF)—has established de facto standards and infrastructure for distributing Python libraries via PyPI and a suite of tools.

Distributing applications is considerably more complex. Depending on the frameworks and technologies used, as well as how users interact with the application, distribution might involve service platforms—typically for hosted SaaS services, such as those deployed on Heroku or Google App Engine; it might involve deploying single or cooperating containers on the cloud (public or private)—suitable for service-oriented architectures; or it could be a consumer-facing app distributed via App Stores, Android Markets, or the Windows Store—requiring wizard-style installers and handling how Python programs are executed.

The distribution method for a Python project depends on user interaction patterns and whether customized installation is required. Some Python libraries can be run via command-line console scripts. If a Python library runs without configuration after installation via `pip`, and users know how to install Python (and potentially create virtual environments), this distribution method is acceptable. However, most consumer app users likely do not know how to install applications via `pip` and launch them from the command line. Furthermore, `pip` installation does not accept user input, preventing customized installation (e.g., selecting installation destinations or entering account information).

# 1. Distributing as a Python Library

Many languages have established central repositories and package manager ecosystems, such as Java’s Maven, Ruby’s RubyGems, Node.js’s npm, Rust’s Cargo, and even C/C++’s Conan. Similar to other languages, Python library distribution is achieved through a central index repository, the Python Package Index (PyPI), launched in 2003. The advent of PyPI was a critical factor in Python’s accelerated growth, as one reason for Python’s popularity is its rich ecosystem, with PyPI serving as the core infrastructure.

Let’s rewind to 2000. When Python 1.6 was released, it introduced an interesting feature, `distutils`, laying the foundation for Python’s packaging tools. At that time, its functionality was simple, offering basic packaging without dependency declaration or automatic installation.

In 2004, `distutils` evolved into `setuptools`, introducing a new packaging format: `egg`. Naming the package format "egg" reflects a programmer’s romanticism and humor, as snakes reproduce by laying eggs, and Python libraries are a key vehicle for Python’s proliferation. Similar analogies exist in other languages, such as the relationship between Ruby and gems. An `egg` file is essentially a ZIP archive with a different name. This stage of `setuptools` also provided a new command, `easy_install`, to install Python eggs, though this command was removed after Python 2.7.

In 2008, PyPA released `pip`, replacing `easy_install`, and subsequently standardized packaging tool behavior via PEP 438.

In 2012, with the adoption of PEP 427, a new packaging format, Wheel, replaced the `egg` format, becoming the standard format for building and packaging (binary) Python libraries.

Although the *Zen of Python* states, "There should be one-- and preferably only one --obvious way to do it," the path from ideal to reality is often winding. As we have discussed, Python has seen multiple solutions emerge for similar problems in virtual environments, dependency resolution, and packaging/building, leading to a "blossoming of a hundred flowers" that can confuse developers. Without systematic organization, many may feel lost, unsure which solution points to the future or if their current skills are being abandoned by the community. Fortunately, the Python community has addressed standardization through a series of PEPs, and related tools and ecosystems are gradually building upon these standards. Future "blossoming" may be less chaotic. Adherence to the latest PEPs is the criterion for choosing technologies in the `ppw` tool and this book.

In `ppw`, our releases are completed via GitHub Actions. We covered this in the [Continuous Integration](/articles/python/best-practice-python/chap09/) chapter. If you have a need for manual releases, please review the section on [Building Distribution Packages with Poetry](chap05.md#building-distribution-packages-with-poetry).

Here, we briefly review how we released Python libraries before Poetry emerged, in case readers occasionally encounter the need to maintain legacy Python projects. Before Poetry, we used the `twine` command to release Python libraries. This command can be installed via `pip`:

```shell
$ pip install twine
```

Although the project generated by `ppw` uses different technologies to release Python libraries, this command is retained. It is used after `poetry build` to verify that the build artifacts comply with PyPI specifications, preventing release failures in advance.

## 1. Packaging and Distribution Process

Packaging and releasing is the process from a developer’s source code to a Python library that users can install and use. This process involves the following steps:
1. Prepare the source code containing the library to be packaged, typically checked out from a version control system.

2. Prepare a configuration file describing the package’s metadata (name, version, etc.) and how to build the artifacts. For most libraries, this is a `pyproject.toml` file, manually maintained in the source tree.

3. Complete the build; the resulting file formats are "sdist" and/or "wheel." These are created by build tools using the configuration file from the previous step.

4. Upload the build results to the package distribution service (typically PyPI).

At this point, your developed Python library appears on the distribution server. To use this library, end users must download and install it. We typically use `pip` to accomplish this.

### 1.1. Packaging Formats: sdist and Wheel

Sdist and wheel are two different packaging formats. Although both are essentially ZIP formats, they differ in content, especially when a Python project includes C code that requires compilation.

The primary purpose of the `sdist` format is to delay binary file construction, allowing your Python library to be installed on more platforms. For example, if your Python library uses Cython and C code for performance optimization, this part lacks Python’s cross-platform capability. In other words, we must build native binaries for each platform separately. Generally, we pre-build native binaries for several major platforms, while binaries for specific platforms (e.g., Raspberry Pi, Alpine) often require delayed compilation during installation on the local machine. Additionally, delayed construction allows for compilation optimizations to best utilize platform performance, which pre-built methods cannot achieve. Furthermore, we often package unit tests and examples within the `sdist` format.

Unlike `sdist`, `wheel` contains only pre-compiled files ready for immediate installation. If the project includes C extensions, these extensions are compiled into binaries during packaging and included in the wheel. When `pip` installs a wheel, it performs simple file copying. Therefore, packages in wheel format install faster.

Unlike `sdist`, `wheel` contains only pre-compiled files ready for immediate installation. If the project includes C extensions, these extensions are pre-compiled, and their results are included in the wheel. When `pip` installs a wheel, it performs simple file copying. Therefore, packages in wheel format install faster.

Projects built with Poetry generally generate both `sdist` and `wheel` installation packages. If an `sdist` format is generated, Poetry creates a simple `setup.py` file. During installation, if no specific format is specified, `pip` always prioritizes the wheel format.

!!! attention
    Neither `sdist` nor `wheel` installation constitutes traditional application installation: neither accepts user input or allows customization during the process. Although `sdist` contains a `setup.py` script that can execute arbitrary code, this script still cannot accept user input from the console. This may be a lesser-known fact. In short, `sdist` and `wheel` are for packaging libraries (packages); they **cannot be used to create application installers**.

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
The file content has been appropriately abbreviated.

We briefly introduce some fields in this file.

Fields such as Name, Author, Author-email, License, Homepage, Keywords, and Download-URL are self-explanatory. In legacy projects (i.e., projects packaged via `setuptools`), these fields must be specified in the `setup.py` file and passed to the `setup` function, which accepts many parameters. In projects using Poetry, Poetry extracts this information from the `pyproject.toml` file.

The **Platform** field specifies special operating system requirements.
The **Supported-Platform** field specifies more detailed operating system and CPU architecture support, such as specifying Linux as RedHat or CPU architecture as ARM.
The **Summary** field provides a brief description of the package’s functionality. In projects using Poetry, it is extracted from the `description` field. On PyPI, it will display here:

![](assets/img/chap11/meta_summary.png){width="50%"}

**Description and Description-Content-Type fields**: The Description field provides detailed information about the package, while the Description-Content-Type field specifies the content type of the Description field, supporting Markdown and reStructuredText. In projects using Poetry, Poetry automatically copies the README content. On PyPI, it will display in the bottom right corner of the figure below (in the box):

![](assets/img/chap11/meta_description.png){width="50%"}

**Classifier field**: Classifiers describe the project’s classification attributes. These attributes display on PyPI and can be used as filter conditions for search and filtering; see the figure below:

![](assets/img/chap11/meta_classifier.png)

PyPI’s classification system is a tree structure. The top-level categories include Framework, Topic, Development Status, Operating System, and other major categories. In fact, third-party libraries on PyPi are vast, and manually querying these classifications is not very meaningful. These classifications help PyPI organize and manage all libraries but are not mandatory and do not aid in package installation. However, PyPA still recommends declaring at least the Python version, license, and operating system classifications for any project.

Additionally, the newly added Typing classifier is interesting. Its purpose is to inform PyPI that the project is a type-annotation-ready project. If our project is ready for type annotations, we should add a `py.typed` file in the project’s source code directory and include this classifier in `pyproject.toml`:

```toml
classifiers=[
    'Typing :: Typed',
]
```

**Requires-Dist field**: This field describes the project’s dependencies. When installing, `pip` reads this field to discover which dependencies need to be installed.
**Requires-Python field**: Indicates the Python version required by this project.

Regrettably, although every package contains this information, PyPI does not extract important information, such as `requires-dist`, for separate management. Other language package managers, like Maven, handle this better. We will explain why this is a regret shortly.

## 2. TestPyPI and PyPI
In projects generated by `ppw`, the `publish` task in the dev workflow releases build artifacts to TestPyPI. This is a test version of PyPI. The purpose is twofold: first, we want CI to always cover the entire development process, so the build and release steps should not be omitted. Second, in large applications, we may simultaneously develop multiple interdependent projects. In such cases, we rely on TestPyPI so that when a project has an updated version but is not yet ready for official release, other projects depending on it can still use the latest version. In this scenario, we can add a second source in `pyproject` pointing to TestPyPI, so when we specify the latest development version of that project, Poetry will search TestPyPI.

Let us illustrate how to add a non-official release version to a project via TestPyPI.

We use the Zillionare quantitative framework as an example. This is a large application containing multiple modules. Here, `zillionare-omicron` is the data read/write SDK, and `zillionare-omega` is the market data server, which depends on `zillionare-omicron` and many other modules. However, to understand our example here, knowing just these two modules is sufficient. In fact, you can completely ignore what the Zillionare quantitative framework is; you only need to know the dependencies between a few modules.

Assume the current latest development version of `zillionare-omicron` is 1.2.3a1. `zillionare-omicron` uses semantic versioning, so from the version number, we know this is not an official release and will only be published to TestPyPI. To use this version in a project, we must first add TestPyPI as a source, then specify the version of `zillionare-omicron` as `1.2.3a1` in `pyproject.toml`. When we execute `poetry install`, Poetry will search for version 1.2.3a1 of `zillionare-omicron` from TestPyPI and install it locally.

We introduced how to add a second source in the section [How Poetry Dependency Resolution Works](chap05.md#how-poetry-dependency-resolution-works). We use the same method here to add the TestPyPI source:
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
The command will execute successfully, and you can see the reference to `zillionare-omicron` in the updated `pyproject.toml`. If we had not added this source, the above command would have failed with the following error:
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
You might wonder why `pip`, one of the first commands every Python learner encounters and one of the earliest commands used in this book, is introduced last. The reason is that since everyone is very familiar with `pip`, a general introduction is unnecessary. It is worth noting that `pip` also faces dependency resolution issues, and the most appropriate place to discuss this is after understanding the full picture of the build and distribution system.

Dependency resolution. We encounter this term again. Last time, it was in the chapter on Poetry. Yes, Poetry only solves dependency issues during the development phase and lays a good foundation for dependency resolution during installation, but `pip` still faces dependency resolution issues independently.

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
To enjoy a cup of tea, besides good tea, you need hot water, a spoon, and a cup. Here, `tea` depends on `hot-water`, `spoon`, and `cup`. When installing `tea`, `pip` downloads the latest `spoon` and `cup`, finds them incompatible, and must search backward for compatible versions. This feature, called backtracking, was introduced in version 20.3. Since dependency information cannot be obtained by querying PyPI, `pip` must repeatedly download earlier versions of packages, extract dependency information from these packages, and check compatibility with `spoon`, repeating this process until a compatible version is found.

We have seen this process during Poetry’s dependency resolution. We explained in the section [How Poetry Dependency Resolution Works](chap05.md#how-poetry-dependency-resolution-works) that PyPI does not host dependency trees for libraries, so Poetry must download a library to know its dependencies. This statement is only partially correct. After reading the section [Metadata for Distribution Packages](/articles/python/best-practice-python/chap11/#metadata-for-distribution-packages), we already know this information has been uploaded to PyPI; it is just that, for historical reasons, PyPI has not extracted it separately for use.

People have spent so much effort solving dependency issues, suggesting that "dependency hell" is not an exaggeration.

The question is, since Poetry performs dependency resolution when adding dependencies and generates a lock file, why can’t `pip` directly use this information and must perform dependency resolution again? Now, please open the wheel file built from the `sample` project. As we said, it is a ZIP-format compressed file. Upon opening, its contents are as follows:
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

We find nothing related to Poetry here. This is not surprising, as Poetry and pip are not developed by the same entity, and Poetry is not part of the standard library, so pip has no reason to parse anything directly related to Poetry. All dependency information is in the METADATA file, specifically `Requires-Dist`:

```
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
Requires-Dist: fire (==0.4.0)
Requires-Dist: flake8 (==4.0.1) ; extra == "test"
Requires-Dist: flake8-docstrings (>=1.6.0,<2.0.0) ; extra == "test"
Requires-Dist: isort (==5.10.1) ; extra == "test"
```
We see that some dependencies specify exact versions, while others specify only version ranges, using inequality syntax (see [Poetry Dependency Management Commands](chap05.md#poetry-dependency-management-commands)). Thus, although Poetry locks exact versions via the lock file, the lock file is shared only among developers to accelerate their development environment construction and is not released to end users. The dependency information released to end users is generated by Poetry based on the `pyproject.toml` file, with semantics identical to the original, except Poetry allows developers to use various syntaxes including wildcards, carets, tildes, and inequalities to specify versions, which are converted to inequality syntax when generating METADATA. Let’s recall the relevant part of the `pyproject.toml` file in the sample project:
```
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
```

Why doesn’t Poetry write the locked versions from the `lock` file into the METADATA file? Because the lock file completely locks down dependency versions, which speeds up installation but also prevents any updates, including security updates.

Now we understand that if backtracking occurs when Poetry adds a dependency to a project, the same backtracking is likely to occur during `pip` installation. To accelerate `pip` installation, we should examine the `poetry.lock` file, identify the locked versions, and use them as a baseline to specify appropriate version ranges, largely avoiding backtracking during `pip` installation.

Good news: according to `pip`’s documentation, efforts are underway to obtain dependency information without downloading Python packages. Let’s look forward to its arrival.
# 2. Application Distribution
Application packaging and distribution, based on the final distribution target, can be broadly divided into desktop applications and mobile applications [^1]. The former generally only requires some packaging tools; the latter often requires framework support from the outset.
## 4. Desktop Applications
There are many options for packaging Python desktop applications, including cross-platform tools like pyInstaller[^3], Nuitka[^8], and briefcase[^5]; Windows-specific tools like py2exe[^6]; and Mac-specific tools like py2app[^7]. Additionally, there are cx_Freeze[^4] and makeself[^2]. Here, we will introduce makeself, PyInstaller, and Nuitka.

Before introducing these tools, let’s discuss what it means to package and distribute a desktop application. When we distribute a Python library, our users are programmers who should possess basic Python knowledge, such as creating virtual environments and installing dependencies. When we distribute a desktop application, our users are often ordinary users who may lack this knowledge, or may not even know how to run a Python program. Therefore, we must also help them create entry points for the program (e.g., placing the entry point in the start menu or desktop shortcuts). Additionally, during installation, we may need to ask users for the installation directory, display and accept license agreements, etc. These are basic requirements for packaging and distributing desktop applications.

Not all the tools we introduce possess the above capabilities equally; please distinguish and choose according to your needs.
### 4.1. Makeself Cross-Platform Installer (with Case Study)

Makeself[^2] is a self-extracting tool usable on Unix/Linux and MacOS. If users use Windows, it can also be used provided Cygwin is installed (though this essentially excludes ordinary users, making it not an ideal solution). Makeself itself is a small shell script that generates self-extracting compressed archives from a specified directory. The generated file appears as a shell script and can be executed under the shell. Upon execution, the compressed archive self-extracts to a temporary directory and then executes a pre-specified command (e.g., an installation script). This is very similar to archives generated by WinZip Self-Extractor in the Windows world. Makeself archives also include checksums for integrity self-verification (CRC and/or MD5/SHA256 checksums).

We introduce this tool because it is widely used in the operations field and has over a thousand stars on GitHub. Additionally, this concept may not be unfamiliar to Python developers. If you have installed Anaconda on Linux, you may know that Anaconda’s installation package is a compressed archive similar to a shell script; it is uncertain whether it is packaged with makeself or another tool.

Makeself’s usage is also very simple, with almost no learning curve. On Ubuntu, it can be installed via the following command:
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

`args` are the parameters Makeself uses during packaging. There are many parameters, covering how to compress, whether to encrypt, decompression behavior, etc., which we will not detail here. Please refer to the official documentation [^2] when needed.

During the preparation phase, we typically place all files to be packaged and installed in a directory. `archive_dir` is the name of this directory, such as the `dist` folder in the project; `file_name` is the name of the final installer file, such as `install_sample.sh`; `label` is the description of the installer, such as "Install sample"; `startup_script` is the script to be executed after the installer is decompressed, such as `install.sh`; `script_args` are the parameters for `startup_script`.

Using the `sample` project as an example again, we can use the following script to complete packaging:
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
Very lightweight and clean, which is why we introduce it. Here, we use a script named `install.sh` as the startup script. In this script, we merely demonstrate how to execute the installation command. A complete installation script might need to:
1. Check if a Python version meeting the requirements is available; if not, download and install it. Here, you can also ask for user opinion; if the user declines, exit the installation.
2. Install virtualenv; if virtualenv does not exist in the current environment, install it via `pip install virtualenv`.
3. Create a new virtual environment via `virtualenv --no-site-packages venv path/to/your/app`; our application should run in this virtual environment. The virtual environment’s path will also be our installation path, requiring user input. The parameter `--no-site-packages` ensures system packages are not copied over, resulting in a clean virtual environment.
4. Copy the decompressed application to `path/to/your/app`.
5. Change directory to `path/to/your/app` and activate the virtual environment: `source venv/bin/activate`.
6. Install the application: `pip install ./sample-$version-py3-none-any.whl`. After installation, this `.whl` file can also be deleted.
7. Create a startup script (assume name `start.sh`); this script’s role is to call our application `sample` via Python in the virtual environment. If the `sample` program provides a `console script`, the startup script’s task is to call it directly; otherwise, it depends on how `sample`’s entry program is provided. This part is left to the reader to complete.
8. Create a symbolic link, linking the startup script to `/usr/local/bin`, allowing our application to be launched via the `sample` command from anywhere. The command to create a symbolic link is:
```shell
$ sudo ln -s path/to/your/app/start.sh /usr/local/bin/sample
```

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


### 4.2. PyInstaller and Nuitka
Both are packaging tools. Their goal is to package Python programs into self-contained executable files (or folders). This allows us to distribute them to customers, who can run them directly regardless of whether their target machines have Python installed, with all dependencies included. In addition to the above functions, both tools also have the ability to encrypt Python programs, a feature required by many developers.

The difference is that PyInstaller only packages Python programs, i.e., starting from a specified Python file, it recursively analyzes its dependencies and packages these dependencies along with the appropriate Python interpreter. During this process, it can obfuscate the generated bytecode to some extent, providing encryption. The final application runs like a normal Python program, executed via the interpreter.

Nuitka first translates Python programs into C code, then compiles them into executable files. Thus, the generated executable files do not depend on the Python interpreter. The benefit is that the generated executable files are smaller, and theoretically, their running speed should be comparable to C programs. However, Python programs converted to C may encounter some compatibility issues. In such cases, Nuitka prioritizes compatibility over speed optimization, so acceleration is generally considered to be within 30%. Another benefit of using Nuitka for packaging is that since we release binary files, it protects source code relatively well.

It seems Nuitka has more development prospects, given its performance advantages. As more Python libraries use type hints, this performance advantage will become more obvious. Therefore, we only briefly introduce Nuitka here. If readers are interested in PyInstaller, they can study it themselves via the official website links provided in the text.

Below, we use a simple example to illustrate how to use Nuitka to package Python programs. Although we recommend running all our examples on Ubuntu or MacOS, this time, we need to run this example on Windows.

First, we must install Nuitka, which can be done via pip (note that we need to create a virtual environment and install Nuitka within it):

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

Next, it’s time to witness the miracle. We package it as follows:
```
python -m nuitka greetings.py
```
The program continues after issuing the following warnings:
```
Nuitka-Options:INFO: Used command line options: greetings.py
Nuitka-Options:WARNING: You did not specify to follow or include anything but main program. Check options and make sure
Nuitka-Options:WARNING: that is intended.
Nuitka:WARNING: Using very slow fallback for ordered sets, please install 'orderedset' PyPI package for best Python
Nuitka:WARNING: compile time performance.
```

Nuitka issued some performance-related warnings during compilation. For our simple program, these warnings will have no impact. For example, one warning states that if your program uses `set`, you should install `orderedset` to improve runtime speed. Our example program is so simple that even if we install `orderedset` as prompted, we will not gain performance improvements. Therefore, we can completely ignore these warnings.

Next, it requests to download and install MinGW64 and ccache. This download may fail; if so, you need to download it yourself, decompress the downloaded archive, and place it in the specified location as prompted, such as 'C:\Users\Administrator\AppData\Local\Nuitka\Nuitka\Cache\downloads\gcc\x86_64\11.3.0-14.0.3-10.0.0-msvcrt-r3'. This location may vary depending on your system, but it will be printed in the command-line window.

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
According to the prompts, we see it converts Python code to C source code and further compiles it into a native program runnable on Windows. Ultimately, we obtain two files: 'greetings.exe' and 'greetings.cmd'. If we are in the window where we just packaged it, we can run `greetings.exe` directly; otherwise, we should run `greetings.cmd`.

The execution result is as follows:
```shell
$ greetings.exe greeting aaron

hi aaron
```
This is merely a command-line program, so it may not look exciting. If we intend to find it in the file explorer, double-click, and run it, we will be prompted that certain Python DLLs are missing. To make this program fully independent, we need to add the `--standalone` parameter during packaging:
```shell
$ python -m nuitka --standalone --follow-imports greetings.py
```

This time, it will prompt to download some items, mainly the MSVC runtime, but this download will go very smoothly. Ultimately, compilation succeeds, and we obtain a folder named `greetings.dist`. Now, if `greetings` were a graphical application, we could double-click `greetings.exe` in the file explorer to run it. However, since our `greetings` program requires user input, we still need to open it from the command line. But this time, we can copy the newly generated folder to a machine without Python and Nuitka installed and run `greetings.exe` from the command line:

```shell
$ greetings.exe greeting aaron

hi aaron
```

Nuitka’s packaging and build process can be integrated with Poetry; we only need to modify `pyproject.toml` as follows to work:
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

Now, let’s think about the positioning of PyInstaller and Nuitka. They are both packaging programs, obviously. But they are not installers. Through them, we achieve the goal of allowing these programs to run directly on users’ desktop operating systems without installing Python and dependencies. However, they are only suitable for "green programs" that require no installation; if our program needs to create desktop shortcuts or modify the registry, they are powerless.

If your program requires a more splendid installation interface, we recommend checking out Inno Setup[^4] or WiX[^9].
## 5. Mobile Applications
Mobile applications differ significantly from desktop applications. Generally, even if we can package a desktop application into an installable mobile application, the user experience is hard to say will be good. Therefore, for Python application packaging and distribution, planning must begin from the start, using relevant cross-platform development frameworks from the beginning.

Here, we mainly introduce and compare the two most popular frameworks, `Kivy` and `BeeWare`, allowing readers to choose according to their needs.

### 5.1. Kivy
Kivy[^10] is a cross-platform Python framework that allows us to develop desktop and mobile applications using Python. It is based on the MIT License and is completely free. Its main feature is its own UI design language, ensuring consistent behavior and appearance of applications across all devices; it uses OpenGL to draw UI, making it very efficient. The figure below shows a Go game developed using Kivy, named Lazy Baduk, which you can find in the Google Play Store.

![](assets/img/chap11/kivy_go.png){width="50%"}

!!! Info
    If you are interested in Go, we recommend a Go training software named KaTrain, also developed with Python and Kivy. It is based on KataGo -- the strongest open-source Go AI in terms of computing power. Some rumors suggest that certain commercial software, including AI Go software used by national teams for training, have "borrowed" KataGo’s algorithms.

Kivy’s weakness may also lie in its unique UI design language. Kivy’s UI toolkit ensures that applications based on Kivy can run well on Android, iOS, Linux, and even Raspberry Pi, but it also lacks certain operational capabilities of native applications.
### 5.2. BeeWare
BeeWare[^11] is also a cross-platform Python framework. It is based on the BSD License and is completely free. Its main feature is its commitment to providing a user experience close to native programs. BeeWare appeared later, but its development momentum is not bad. Additionally, it is component-based; BeeWare includes BriefCase, another widely used Python packaging tool. Toga, a cross-platform GUI framework based on Python, is also part of BeeWare.

Mobile differences are far greater than desktop ones. Leveraging the latest features of mobile devices is crucial for creating attractive mobile applications. However, both BeeWare and Kivy can only abstract features common to most mobile devices. For this reason, Python may currently not be the most suitable development language. However, both Kivy and BeeWare provide options for developing mobile applications with Python.
## 6. Cloud-Based Application Deployment
Compared to desktop applications, Python seems better suited for developing backend service programs. Under microservice architecture, multi-process + asynchronous I/O compensates for Python’s shortcoming of not fully utilizing hardware performance, while its advantages of simplicity, efficiency, and rich ecosystem are fully leveraged.

Python’s cloud deployment includes methods like Heroku and Google App. However, the more widely used method may be cloud-based containerized deployment. Containers are lightweight virtual machines. Unlike virtual machines, they do not require a complete operating system but directly use the host machine’s kernel. Thus, container startup speed is much faster than virtual machines, and their resource consumption is lower. Generally, we use containers to run specific services; when the service stops, the container also terminates.

Docker is currently the most popular containerized deployment tool. Building container-based services generally involves two steps: building the image and running the container. The image usually consists of an operating system kernel, a Python interpreter, and our Python service. These components can be described via Dockerfile. Dockerfile is a text file containing a series of commands and parameters to build an image. An image is a read-only template describing how a Docker container should run. When the image is pulled locally and executed by Docker, a container is generated, and the service runs within the container.

Below, we illustrate how to build and run a container for a Python service via an example. The example’s source code is in the `code/chap11/docker` directory. We still create a project named `sample` via `ppw`. Unlike before, we will create a directory named `docker` (name can be arbitrary) in the project root, containing the following files:
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

Among them, `build.sh` is a script used to build the image. `dockerfile` describes the image. `rootfs` is a directory used to store files we need to bring into the image. During image building, it will be mapped as the container’s root directory.

`build.sh`’s main work is to build the `sample` project, copy the corresponding files to `rootfs`, and then execute the `docker build` command to build the image.

Here is the main content of `build.sh`:
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
In this build script, we first build the `sample` project’s wheel package, then copy it to the `rootfs` directory. Next, we execute the `docker build` command to build an image named `sample`. Finally, based on this image, we start a container named `sample` and map port 7878 to the host port.

Dockerfile is the core of this section. Now, let’s look at the content of Dockerfile:
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
When building any image, we start from a base image. This base image can be an operating system image like Linux Alpine or Ubuntu, or an application image built on the operating system, such as `python:3.8-alpine3.17` in the example, which is a Python application image built on the Alpine operating system. The image identifier is generally in the form "developer/image name: version." The string after the colon is the tag, generally its version number; if no version is specified, the default is `latest`. If no developer is specified, it means this is an official image or a locally built image.

Image distribution is a two-tier architecture. If the `python:3.8-alpine3.17` image does not exist locally, Docker will search on Docker Hub[^12]. Docker Hub, similar to PyPI, is a public image repository providing a large number of images for our use. Now, let’s look at what the `python:3.8-alpine3.17` image on Docker Hub actually is. On Docker Hub, we must search via image name (i.e., without version tag). This yields the following results:

![](assets/img/chap11/docker_hub_python.png){width="50%"}

This image has been downloaded over 1 billion times. This not only illustrates how widespread Python usage is but also how important Python is in backend service development.

Clicking the link in the figure above, we can enter the details page, find the tag `3.8-alpine3.17`, and click to enter, jumping to GitHub to view its Dockerfile content:

![](assets/img/chap11/python3.8_alpine_dockerfile.png){width="50%"}

Alpine is a lightweight Linux distribution. Images built on Alpine are only about 5MB in size, making them the first choice for building microservices. Our image ultimately uses this operating system kernel.

Then, we specify the current working directory as the root directory and copy files from the `rootfs` directory to the container’s root directory. Next, it installs the `sample` project’s wheel package. Finally, it sets the container’s entry point to `/root/entrypoint.sh`.

We use `ARG` to pass Docker build-time variables. Here, `version` and `wheel` are two compiler variables, passed in by `build.sh` via `--arg $version`. The `EXPOSE` command exposes the port. We start an HTTP service listening on `$PORT` in `entrypoint.sh`; we must expose this port to the host so we can access the service from the host.

Next, let’s look at the content of `entrypoint.sh`:
```
#!/BIN/SH

python3 -m http.server -d /root/sample $PORT
```

Since this is just a demonstration program, we do not use any features of `sample` here; instead, we simply start a web service via Python’s built-in `http` module. You only need to know that if you want to use `sample`’s features, you can call its commands here, just as you would elsewhere.

After local testing passes, we can register an account on Docker Hub, publish our image there for others to download, thus completing container-based application release. Of course, we can also establish a private cloud image repository and publish the image to the private cloud for internal deployment.

In this example, the final image file we built is only about 66MB. In fact, due to Docker’s layered file system design, if others download our image from Docker Hub, the actual data they need to download will be even smaller.

This is the entire process of building container-based services. Isn’t it unexpectedly simple and reliable? In this book, we have used a lot of space to discuss how to isolate environments; here is another method, which is even simpler and more reliable than all previous methods. Services running in containers exclusively occupy file systems and computing resources, interacting with neither the host machine nor other containers running on the same host. Moreover, we can generate identical containers from the same image infinitely. Reproducible deployment is finally perfectly realized.

Now, let’s run the `build.sh` in the example. It will build the image for us and start a container of that image.

In `build.sh`, we specified the container’s port as 7878. Now, the container has started, and the service is running; let’s access it. We enter `http://ip-to-host:7878/` (replace `ip-to-host` with the actual IP of the machine where you deployed and ran the example container) in the browser address bar, and we will see the following interface:

![](assets/img/chap11/end.png){width="80%"}

We have seen this figure in Chapter 1.

Let’s start here, and also end here. Now, it is time for you to begin your own Mars exploration journey.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


[^1]: The [Python Official Documentation](https://packaging.python.org/en/latest/overview/#packaging-python-applications)(https://packaging.python.org/en/latest/overview/#packaging-python-applications) also mentions several other packaging methods.
[^2]: [Makeself](https://makeself.io/)'s official website is: https://makeself.io/
[^3]: [PyInstaller](https://pyinstaller.org)'s official website is: https://pyinstaller.org
[^4]: [Inno Setup](https://jrsoftware.org/isinfo.php)'s official website is: https://jrsoftware.org/isinfo.php
[^5]: [Briefcase](https://briefcase.readthedocs.io/)'s official website is: https://briefcase.readthedocs.io/
[^6]: [Py2exe](https://www.py2exe.org/)'s official website is: https://www.py2exe.org/
[^7]: [Py2app](https://py2app.readthedocs.io/en/latest/)'s official website is: https://py2app.readthedocs.io/
[^8]: [Nuitka](https://nuitka.net/)'s official website is: https://nuitka.net/
[^9]: [WiX](https://wixtoolset.org/)'s official website is: https://wixtoolset.org/
[^10]: [Kivy](https://kivy.org)'s official website is: https://kivy.org
[^11]: [BeeWare](https://beeware.org/)'s official website is: https://beeware.org/
[^12]: [Docker Hub](https://hub.docker.com)'s official website is: https://hub.docker.com
