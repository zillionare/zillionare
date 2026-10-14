---
title: "02 Setting Up Your Python Dev Environment"
date: 2023-12-13
slug: en/articles/python/best-practice-python/chap02
tags: [Development Environment, Linux, WSL, Visual Studio Code]
excerpt: "Choosing the right OS and IDE is critical for quantitative developers. This chapter guides you through Linux, WSL, Docker, and VS Code configurations to streamline your workflow."
lang: en
translation_of: articles/python/best-practice-python/chap02
auto_translated: true
source_sha: bedba943f5c363c7a768a831348b1f47f26804a1
---

While all roads lead to Rome, some are smoother and faster, and some developers even live in Rome. For programmers, the better your development environment, the closer you are to Rome. Therefore, our journey begins here.

## 1. Choosing an Operating System

At first glance, the operating system seems unrelated to the programming language, especially for Python, whose programs can run on almost any OS. However, there are subtle differences to consider. First, Python is better suited for data analysis, artificial intelligence, and backend development rather than desktop or mobile applications. Both big data analysis and backend development are typically deployed on Linux servers. Consequently, the ecosystems they rely on are often built on Linux (e.g., big data platforms and distributed computing systems). Some critical libraries, while eventually compatible with multiple operating systems, often have different release schedules across platforms due to OS differences. Open-source programs and libraries often prioritize Linux, with more thorough testing on that platform.

We can cite many such examples. Quantitative trading is one of Python’s most important application areas, and `python-talib` is a commonly used technical analysis library within it. This library uses a C module that requires compilation during installation. Compiling on Windows requires downloading and configuring a series of Visual C++ build tools, which can be difficult for Python developers since many of these concepts are unfamiliar. If you use Linux, compilation is still required, but installation and building can be done with a single script.

This applies not only to Python libraries but also to various services we depend on. For instance, while you can install the desktop version of Docker on Windows and run some Linux containers, Docker’s resource utilization on Windows is far less efficient than on Linux—resources are allocated from the system when the Docker service starts, regardless of whether containers are running, making them unavailable to other Windows programs. Fundamentally, this difference arises because Windows cannot provide container-level resource isolation.

Later in this book, we will cover CI/CD, which requires container technology. At that point, you will appreciate the convenience of using Linux. For example, we will use containers provided by GitHub Actions to run tests, but due to licensing issues, the free version of GitHub CI containers will not include Windows.

If these reasons still do not convince you, consider how senior developers choose their operating systems. The following figure is from a 2022 survey on StackOverflow[^stackoverflow]:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/03/20230304160004.png)

The numbers to the right of each item indicate the percentage of respondents using that operating system. From the chart, if we combine Linux’s own usage with WSL usage (WSL is a type of Linux), the proportion of professional users reaches 54.23%, exceeding those who use Windows as their development platform (48.82%). Linux is now the number one operating system.

For the above reasons, we recommend using Linux as the operating system for your Python development projects. Unless otherwise specified, the tools, examples, and libraries mentioned in this book default to Linux as the runtime environment and have been tested on Linux.

However, you may not like this suggestion because your computer likely runs MacOS or Windows.

The good news is that MacOS and Linux are both "Unix-like" operating systems with high similarity. So, if your computer runs MacOS, you do not need to install Linux separately. If your computer runs Windows, we provide three solutions below to allow your machine to run a virtual Linux operating system for development.

## 2. Linux Environments on Windows

There are three ways to build a Linux virtual environment on Windows. One is Windows’ native solution, using Windows Subsystem for Linux (WSL for short). The other two are Docker and virtual machine solutions.

### 2.1. WSL Solution

WSL is a new feature in Windows 10. Through WSL, a GNU/Linux environment runs on top of Windows. In this environment, most Linux command-line tools and services can run without setting up a dual-boot system or incurring the extra costs of a virtual machine.

There are currently two versions available, v1 and v2. The author recommends using v1. WSL v2 feels more like a true virtual machine, so its integration with Windows is slightly worse.

#### 2.1.1. Installing WSL

If your Windows 10 is version 2004 or higher, or if you use Windows 11, installation can be completed with a single command:

```shell
wsl --install --set-defalut-version=1
```

This will install WSL v1 on your machine. For slightly older systems, you need to follow these steps:

1. First, enable the "Windows Subsystem for Linux" feature:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2020-05/20200503185200[1].png)

2. After setting, you need to restart your computer.
3. Search for and install a Linux distribution from the Windows App Store. In this example, we use Ubuntu:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2020-05/20200503191417[1].png)

Now, typing Ubuntu in the search bar will open the Ubuntu shell. Since it is the first run, you will be prompted to enter a username and password. This completes the WSL installation. You can also start this system by typing the `wsl` command in the search box.

#### 2.1.2. Customizing WSL

Using WSL v1 offers a special experience. It resembles a virtual machine but lacks some features, such as the concept of background services[^wsl]. We can install some services, such as Redis cache or databases, but these background services will not start with WSL; they must be started manually. However, we can customize WSL to make its usage experience closer to that of a virtual machine.

Our customization will achieve two functions: first, to make the WSL virtual machine start automatically with Windows. Second, when WSL starts, it will automatically run an SSH service so that we can connect and use this WSL virtual machine at any time. After learning this customization, readers can certainly configure WSL to automatically run more background services after startup.

We need to write three scripts: `start.vbs`, `control.bat`, and `commands.txt`, and add a scheduled task for automatic startup. When Windows starts, this scheduled task executes automatically, calling `start.vbs` to run `control.bat`, which in turn starts WSL (and its dependent Windows services) and executes the commands defined in `commands.txt` within the WSL environment—such as the services to be run in WSL, like the SSH server. The entire process is shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/03/20230304153221.png)

First, we define the background services to be run in WSL in the `commands.txt` file:

```text
/etc/init.d/cron
/etc/init.d/ssh
```

Then, we write a batch script to start WSL and execute the above commands:

```bat
REM control.bat
REM 脚本来源于 https://github.com/troytse/wsl-autostart/
@echo off
REM Goto the detect section.
goto lxssDetect

:lxssRestart
    REM ReStart the LxssManager service
    net stop LxssManager

:lxssStart
    REM Start the LxssManager service
    net start LxssManager

:lxssDetect
    REM Detect the LxssManager service status
    for /f "skip=3 tokens=4" %%i in ('sc query LxssManager') do set "state=%%i" &goto lxssStatus

:lxssStatus
    REM If the LxssManager service is stopped, start it.
    if /i "%state%"=="STOPPED" (goto lxssStart)
    REM If the LxssManager service is starting, wait for it to finish start.
    if /i "%state%"=="STARTING" (goto lxssDetect)
    REM If the LxssManager service is running, start the linux service.
    if /i "%state%"=="RUNNING" (goto next)
    REM If the LxssManager service is stopping, nothing to do.
    if /i "%state%"=="STOPPING" (goto end)

:next
    REM Check the LxssManager service is started correctly.
    wsl echo OK >nul 2>nul
    if not %errorlevel% == 0 (goto lxssRestart)

    REM Start services in the WSL
    REM Define the service commands in commands.txt.
    for /f %%i in (%~dp0commands.txt) do (wsl sudo %%i %*)

:end
```

Next, we write a `start.vbs` script to execute `control.bat`:

```vb
' start.vbs
' 脚本来源于 https://github.com/troytse/wsl-autostart/
' Start services
Set UAC = CreateObject("Shell.Application")
command = "/c """ + CreateObject("Scripting.FileSystemObject").
                GetParentFolderName(WScript.ScriptFullName) + "\control.bat"" start"
UAC.ShellExecute "C:\Windows\System32\cmd.exe", command, "", "runas", 0
Set UAC = Nothing
```

Finally, we add a new startup task to the Task Scheduler:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202106/20210616215338.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202106/20210616215237.png)

It should be noted that the Ubuntu subsystem installed via the Windows App Store should already have the ssh-server installed. What we are doing in the above operation is simply to make it start with WSL. However, if you find that your WSL does not have the ssh-server installed, you can install it yourself. After all, it is a Linux server, and you can install most Linux software on it.

By applying the above solution, you will have two operating systems running simultaneously on Windows. It is particularly worth mentioning that when you are not using WSL, it consumes very little CPU and memory resources (limited to WSL 1.0). This is incomparable to other virtualization solutions.

At the time of this book’s writing, WSL 2.0 already had a preview version supporting graphical interfaces, called [wslg](https://github.com/microsoft/wslg). This version will be merged into WSL and released as an official version with Windows. The following figure is an effect image of the wslg graphical interface:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202108WSLg_IntegratedDesktop.png)

Although this is unrelated to the main theme of this book, it at least gives us another reason to use Linux. Even Microsoft is taking Linux seriously[^Linux]. Are you still going to use Windows for development?

### 2.2. Docker Solution

WSL appeared later than Docker. If you purchased your machine earlier, your Windows may not support WSL but can install Docker. In this case, you can try installing the desktop version of Docker and then run a Linux virtual machine through Docker.

You can download Docker from its official website[^docker]. After installation, you need to start it manually for the first run. You can search for "Docker" from the search box and then select "Docker Desktop" to start it, as shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202108docker-app-search.png)

When Docker starts, a notification icon will appear in the system tray:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202108whale-icon-systray.png)

The third icon in the above figure, the whale icon, indicates that Docker is running. Clicking it will take you to the management interface. Some settings need to be made for the first run; you can refer to the official documentation.

Running Docker on Windows, due to OS heterogeneity, first requires enabling the Hyper-V virtual machine and then installing Docker into this virtual machine. This is why, when installing and running Docker on Windows, system resources are statically allocated and cut off regardless of whether containers are currently running. However, since approximately March 2020, Docker has supported running desktop versions based on WSL2. Desktop Docker based on WSL2 starts the Docker backend service faster, and resources are allocated only when needed, making resource scheduling more flexible and efficient.

### 2.3. Virtual Machine Solution

It is also possible that your machine does not support installing WSL or Docker. In this case, you can run Linux by installing a virtual machine such as VirtualBox[^virtualbox]. The technology here should be familiar to everyone, so we will not elaborate further.

### 2.4. Summary

We have introduced three solutions for building a Linux development environment on Windows. Whenever possible, you should first install WSL. WSL can run on almost all Windows 10 and above distributions, including Windows 10 Home.

If your machine does not support installing WSL, you can consider installing Docker. Even if your machine supports WSL, for the purpose of practicing CI/CD, you can also install Docker to experience containerized building and deployment. Of course, this requires your machine to have a more powerful CPU and memory.

For older machines, when upgrading to newer versions of Windows is not possible, you can consider using a virtual machine, such as the free version of VirtualBox.

## 3. Integrated Development Environment (IDE)

As a scripting language, Python can run without compilation, so almost any text editor can serve as a Python development tool. However, to conduct serious development and achieve the best balance between development progress and quality, a more professional tool is needed.

An Integrated Development Environment (IDE) is a tool that improves development efficiency. It allows developers to receive various code hints, discover syntax errors earlier, and debug directly in the editor.

PyCharm and VS Code are the two preferred tools for Python application development. For developers engaged in data analysis and artificial intelligence, you can also consider Jupyter Lab (an upgraded version of Notebook) and Anaconda’s Spyder.

### 3.1. VS Code vs PyCharm: Which IDE to Use?

PyCharm is an established IDE for Python development, while Visual Studio Code (commonly known as VS Code) is a rising star in recent years. VS Code is completely free, while PyCharm offers both Community and Professional editions. The Professional edition has more powerful features but requires payment. The following table briefly outlines the most important differences between the two IDEs:

| Feature         | PyCharm             | VS Code              | Description                                                                                                                            |
| --------------- | ------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Remote Dev      | Professional only   | Supported            | In Professional PyCharm, files are edited locally and synced to the remote machine for debugging before debugging; VS Code edits and debugs directly on the remote machine via file-sharing protocols |
| 3-Way Merge     | Supported           | Supported            | VS Code has provided a 3-way merge editor since July 2022. 3-way merge editing is a convenient way to resolve conflicts when code conflicts occur |
| Data View       | Supported           | Not Supported        | PyCharm allows viewing database and DataFrame data in a graphical interface; VS Code requires plugins with weaker functionality, but data can be viewed and managed via third-party tools |
| Startup Speed   | Slow                | Very Fast            | VS Code’s startup speed is excellent, making it suitable not only for development but also for document writing, diaries, and other scenarios requiring quick opening |
| Multi-Language  | Python-centric      | Supports Multiple Languages | VS Code can support development in many languages, making it particularly suitable for professional developers |

There are some minor differences. For example, many VS Code features are implemented through plugins, each with its own log output window. When using VS Code, if a feature does not work, it may be caused by a plugin. This error may be silently output in the plugin’s log window rather than in the interface windows you are familiar with. This may confuse beginners. In PyCharm, the arrangement of these windows and prompt interfaces seems more intuitive.

In short, PyCharm is an IDE ready to use out of the box, while VS Code requires installing a series of plugins before formal development, which may take some time to compare, configure, and learn. However, if you plan to engage in development work for a long time, investing time in VS Code is worthwhile. VS Code is a free product, and its license allows you to use VS Code for any commercial development. Therefore, whether you are an individual developer or employed by an organization, you can use it.

Since we prefer to use VS Code and because PyCharm is simple and easy to use, requiring basically no teaching, we will skip the introduction of PyCharm here and focus on how to configure the VS Code development environment.

### 3.2. VS Code and Extensions

VS Code is a platform supporting multi-language editing and development. It only provides basic functions such as a text editor, code management (Git), and extension management. Specific language development is completed by loading the language’s extensions. Therefore, after installing VS Code, you need to configure a series of extensions.

After installing VS Code, a toolbar will appear on the sidebar as shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/20210820210809145433.png)

The icon circled corresponds to extension management. The rectangular box at the top can be used to search for a specific extension. After finding the corresponding extension and clicking it, you can see the extension’s detailed information in the right window, as shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/20210820210809145930.png)

On this detailed information page, an installation button is provided.

VS Code’s extension management provides not only search but also filtering and sorting functions. Readers can explore these on their own. If readers want to use VS Code across multiple development environments and hope these extensions can be used in different environments, VS Code also provides an extension synchronization mechanism. On the extension detail page in the above figure, to the right of the "Uninstall" button, there is a synchronization icon. Clicking it will automatically synchronize the extension to other environments.

Below, we will discuss some of the most commonly used and important VS Code extensions. After arming VS Code with these extensions, your development efficiency will significantly improve.

#### 3.2.1. Python Extension

To develop Python applications in VS Code, you need to install the Python extension, as shown in the previous figure.

The Python extension is developed by Microsoft and has over 100 million downloads. It provides IntelliSense, code syntax checking, debugging, navigation, formatting, refactoring, and unit testing features. Additionally, it provides a Jupyter Notebook integrated environment.

Along with the Python extension, extensions such as Pylance, Python Test Explorer for Visual Studio Code, and Jupyter are also installed.

Pylance is a Language Server developed by Microsoft based on its acquired Pyright static checking tool, featuring IntelliSense. It provides syntax highlighting, code auto-completion, syntax checking, and parameter suggestions.

Although Pylance provides these features, in practice, we often treat Pylance as a Language Server. Functions such as syntax checking, code hints, and auto-completion should still be completed through more specialized dedicated extensions (or third-party services). Here, Pylance can serve as an extension platform for these features.

Test Explorer’s main role is to discover and collect unit test cases defined in the project, build a TestSuite, provide a test execution entry, and report test execution results after testing is completed.

Jupyter is an extension that allows you to read and develop notebooks in VS Code. Compared to separately installed Jupyter Notebook, it provides more powerful code hints, variable viewing, and data viewing. Additionally, debugging notebooks has always been a troublesome matter. But in VS Code, you can run and debug notebooks line by line, just like debugging Python code.

After the Python extension is installed, you can proceed with Python development. Before development, you need to select a Python interpreter for the project. You can complete this by entering `Python: Select Interpreter` in the command palette or by clicking the selection icon in the status bar, as shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/20210820210806163607.png)

#### 3.2.2. Remote - SSH

This is a very useful extension, one of Microsoft’s official extensions. It allows you to directly open folders on a remote machine in VS Code, edit, and debug runs. If you have used IDEs like PyCharm, you would know that although these IDEs also support remote development, they create files locally and must upload and sync to the remote machine before debugging and running. Frequent syncing not only reduces efficiency but also often results in failure to sync, causing behavior inconsistent with expectations and wasting time looking for issues. This is also an important feature where VS Code is superior to PyCharm.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/20210820210809145039.png)

After installing this extension, a remote connection icon will appear on the sidebar. Additionally, if currently connected to a remote machine, the status bar on the far left will display a summary of that connection.

Next, we need to install version control-related extensions.

Although VS Code provides Git integration, many features are not provided through the GUI, and we must still memorize Git commands. Additionally, there are some features that Git does not have, such as the following:

1. When submitting code, follow specified format specifications to edit commit messages graphically.
2. Management of `.gitignore` files.
3. Management of local history.

To achieve the above functions, we need to continue installing extensions. First is GitLens.

#### 3.2.3. GitLens

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/03/20230306194047.png)

GitLens is a very powerful extension and is commonly used in team development. Its functions include:

   1. Quickly navigating through file modification history.
   2. Prompting blame information in code lines, as shown in the figure below:
    
![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202108hovers-current-line.png)

   3. Gutter change, as shown in the figure below:
      
![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/20210820210809160826.png)

    Gutter change refers to the line on the right side of the line number indicator in the editing area in the above figure, which indicates that there are changes in the current area. When you click this line, a window will pop up displaying the change history of the current area, and you can roll back changes or submit changes. This function is actually Git’s interactive staging function, but its usability is not very good when used in the command line.
    
    If you did not plan well before editing the file and introduced modifications that should belong to multiple commits, gutter change is the best remedy. It allows you to submit changes block by block, rather than by file. Therefore, you can submit different blocks in a file in several commits.

   4. GitLens provides a rich toolbar in the sidebar, as shown in the figure below:

     ![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202108views-layout-gitlens.png)

Through these toolbars, you no longer need to memorize too many Git commands, and the results of these commands are also displayed visually, which is much more efficient than the console interface. These toolbars provide commit views, repository views, branch views, file history views, tag views, etc.

In simple terms, GitLens graphically displays and reconstructs almost all Git functions, providing a rich operation interface that allows you to operate Git and understand code changes more conveniently.

#### 3.2.4. Extension for Editing Commit Messages

Programmers who frequently use PyCharm will not forget its Git commit dialog. Unfortunately, so far, neither VS Code nor its extensions have filled this shortcoming. However, there are still some niche but useful extensions that can not only help us achieve graphical interface commit message editing but also help us manage commit messages in a standardized manner.

Here we recommend an extension called `git-commit-plugin`:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/03/20230306195918.png)

This extension will classify commit messages and add emoji icons to each category, allowing us to identify categories more quickly:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202109/20210926101451.png)

Correctly classifying code is a very important task. If we correctly classify every code submission, we can automatically generate release notes based on these historical submission information when releasing a new version. The generated release notes may need some slight modification, but they will absolutely avoid missing important changes.

Obviously, not all submission information should appear in release notes, especially submissions related to code style, document revisions, adding test cases, and build-related submissions, which are often not of concern to end users and should not be included in release notes. If we correctly classify every submission, then tools for automatically generating release notes can extract only valid information into release notes according to our specified categories.

Later, we will mention tools for automatically generating Release notes. We use tools to ensure the standardization of Commit Message formats, and Release notes also extract and analyze this information through tools. The entire software development process will work precisely like an assembly line.

This is exactly the main theme of this book: **Software development processes should not be abstract concepts, but software production assembly lines enforced through a series of tools.** Once the assembly line is calibrated, the products produced can pass 6 Sigma quality certification[^6-sigma].

#### 3.2.5. Gitignore Extension

Code repositories should only keep useful files. However, during development, the workspace inevitably generates some temporary files, junk files, and file types unsuitable for storage in code repositories, such as logs generated during debugging or binary files generated after compilation. If these temporary files are repeatedly uploaded, they will greatly waste repository storage space and reduce performance. To prevent these files from being submitted to the code repository, we can create a `.gitignore` file in the code repository, which contains the relative paths or matching pattern strings of these files. In this way, Git will automatically filter out these files when submitting code.

The format of the `.gitignore` file is very simple, with each line being a relative path of a file. Therefore, we can manually edit this file. However, the gitignore extension provides more functions:

   1. Generate `.gitignore` files based on templates. After all, a `.gitignore` file may have dozens of lines, with a large number of parts common across different projects, which do not need to be memorized.
   2. Conveniently select files from the workspace and automatically add them to the `.gitignore` file. This avoids path errors compared to manually editing the `.gitignore` file and is faster.

#### 3.2.6. Local File History

Although Git provides file version history management, it cannot track uncommitted modifications. However, before code submission, we may also make multiple modifications to the same file, and at some point, we may want to view and refer to these changes. This requires a local file history management system.

PyCharm provides a very useful local file history feature. In VS Code, this feature must be implemented through extensions.

Readers can install this extension:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/03/20230306195816.png)

It should be noted that this extension will generate a folder named `.history` in the workspace to store local file history. This folder must be added to the `.gitignore` file, otherwise, you are very likely to submit this folder to the code repository. This is a lot of junk files!

The following figure shows this extension’s tracking of code changes:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202109/20210926114236.png)

#### 3.2.7. Code Assistance and Auto-Completion

Code assistance and auto-completion are the most important reasons we use IDEs instead of text editors to write code. According to statistics from Kite[^kite], using Kite for assisted programming can save up to 47% of code typing, making code writing easier and faster.

Of course, you may not agree with the view that typing speed determines programming efficiency. After all, in programming, we spend a lot of time thinking about how to implement algorithms and functions, recalling how to call certain library functions, and naming our own variables and constants. Surprisingly, with the enhancement of artificial intelligence capabilities, a large part of this work can now be completed by code assistance and auto-completion tools.

!!! Info
    A female programmer once worked in our company. She had exquisite makeup, and beautiful patterns were engraved on her long nails, shimmering. When typing on the keyboard, the patterns on her nails danced like butterflies. I knew how unpleasant the sound of nails scraping on keyboard caps was, so I always kept my nails short to ensure uninterrupted typing, and thus worried about the impact of long nails on typing speed. But after contacting her for a period of time, I found that her work efficiency was not low at all—although her typing speed might still be affected by long nails.

    Although Kite’s data indicates that they saved coders 47% of typing time, from the above example, it can be seen that the efficiency improvement brought by this may not be as large as Kite imagined. We will have the opportunity to review the story of Kite later: if the direction of effort is wrong, then diligence is useless.

Just as we can define autonomous driving in five levels based on automation degree, code assistance can also be divided into many levels.

The lowest level might be what ordinary text editors can do, providing prompts at the word level. As long as you have entered a word or a sentence once, the next time you enter the first part of this word or sentence, the IDE will automatically prompt this word or sentence. If you frequently use Excel, you will easily understand what kind of assistance this is. But such prompts are far from precise enough; often, they cannot provide the input we truly want.

For program development, since there are syntax rules to rely on, such prompts can be made more precise. For example, if you define a class, the next time you enter the name of a class (or an instance variable of a class) and type a prompt symbol (possibly ".", or "->", depending on the programming language), the IDE can prompt all methods or attributes of the class for us to select. Additionally, if a namespace is imported, the IDE can also prompt all variables, functions, classes, etc., in the space based on the same logic. These are strictly dependent on syntax, so IDE code prompts for static languages can be excellent. For dynamic languages like Python, without using type annotations, accurately prompting member variables is somewhat difficult.

Now, with the support of artificial intelligence, code assistance has evolved to an astonishing degree. In fact, this book was completed with the help of Github Copilot[^Github Copilot]. We can look at this example:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202109/20210926150605.png)

Copilot automatically generates a grammatically correct sentence based on previous input (this sentence is displayed in gray in the above figure) and coordinates well with the context. Here, I do not want to use the words it prompts (mainly worried that readers do not want to read a machine-written book), but I must admit that unless writing poetry, we do not need to, like ancients, grind one word and break several mustaches. Articles do not need every sentence to be meticulously crafted; sometimes, we can completely use Copilot’s prompted words and sentences for transitions. More often, when writing articles, Copilot can play a role in opening up ideas, which is undoubtedly very beneficial.

The above is just one example of artificial intelligence in general text-assisted writing. When we restrict the domain to the programming field, the results are even more astonishing. Often, as long as you write a comment, Copilot can help you complete the code to implement the function of this comment. Especially when the function we want to implement has already been implemented in a certain library function, or when a famous algorithm exists, you will find this feature very useful.

There are still many extensions for VS Code. For example, our projects may use json, ymal, etc., files, or use markdown/rst to write documents. When editing these files, there are also some good tools for assistance and functional enhancement. For example, Markdown’s support for tables is relatively poor, and manually editing Markdown tables is a tedious matter. We can use some extensions to convert csv block content in documents into Markdown tables through them.

In addition to extensions, VS Code has other customizations, such as themes. If you work in front of a computer for a long time, it is recommended that you install some so-called night mode themes. Among these themes, Dracula PyCharm Theme is a particularly interesting one. The theme’s name comes from Count Dracula, a character in Bram Stoker’s同名 novel of the same name—a bloodthirsty vampire who specifically targets young women. This novel was later adapted into movies multiple times. Considering that vampires only come out at night, using this name for a dark mode theme is quite appropriate.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


Due to space limitations, we cannot introduce all these extensions one by one. In addition to those popular extensions with huge downloads, this chapter also introduces some relatively niche extensions. These niche extensions may disappear in the future (e.g., if VS Code directly implements their functions) or be replaced. The important thing is that the functions they implement significantly improve production efficiency. These methods and functions are what we should be familiar with.

## 4. Other Development Environments

### 4.1. Jupyter Notebook

PyCharm and VS Code are large development tools suitable for developing large, complex applications. However, in the Python field, there is a type of problem better suited for exploratory programming, such as data analysis tasks. We obtain some data, view their characteristics through statistical methods, perform some visual analysis, then preprocess the data, and further write some machine learning algorithms. If the results are not ideal, we start over and explore new algorithms.

This method is called exploratory programming: exploratory work is heavier than following design patterns, and code is interspersed with a large amount of explanatory documentation and output results (including charts and images), which are part of the final result, rather than, like traditional programming, separating code, documentation, and output results.

Jupyter Notebook is a powerful tool for exploratory programming. It provides a web-based editor and runtime environment. User input is organized into cells, each of which can be a code cell or a text cell; code cells also allow output results, which can be text, charts, or images, as shown in the figure below:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202109/20210926164037.png)

A running Notebook can be seen as a process. Variables and functions defined in the code cells of this Notebook have global scope, and each code cell can be executed separately. This mode has its extremely convenient aspects. You can run code in the Notebook at any time and switch between different code cells—whether exploring data characteristics or exploring the functionality of a new library becomes very easy.

Currently, Jupyter Notebook developers are pushing Jupyter Lab to replace Jupyter Notebook. However, due to the integration of Jupyter Notebook in VS Code and PyCharm, Notebook will still exist for a considerable time.

### 4.2. Spyder

Spyder[^spyder] is an open-source programming environment specifically designed for scientists, data analysts, and engineers. It has a unique combination of advanced editing, analysis, debugging, and profiling functions of an integrated development environment with data exploration, interactive execution, deep inspection, and beautiful visualization functions of scientific libraries. We can easily see this from its interface:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/202109/20210927163158.png)

Spyder is included in the Anaconda distribution, so once Anaconda is installed, you can directly use Spyder to write Python code. Its official website also provides standalone installation packages for download.

We have mainly introduced three types of Python development environments: PyCharm/VS Code suitable for large-scale engineering development, Jupyter Notebook suitable for exploratory programming, and Spyder, which combines the characteristics of both. Of course, in PyCharm/VS Code, we can also open and run Jupyter Notebook. This feature has been integrated into these two IDEs for a period of time.

If our frequent development work is to build highly reusable component libraries or complex applications, PyCharm/VS Code is definitely the best choice. These two tools are almost perfectly integrated with tools responsible for testing, continuous integration, code management, and document building. Conversely, if your work is more exploratory, it seems that only using Jupyter Notebook is sufficient. Spyder provides a choice for users who need to balance both aspects.


[^stackoverflow]: stackoverflow.com is the world’s most well-known technical sharing community. Programmers often use this community to ask others about technical problems they encounter.
[^Linux]: There is a saying that MacOS is the best Linux, Windows is also the best Linux, only Linux does not do Linux well.
[^wsl]: As of the time this book was written, this concept may have changed. Versions of Ubuntu 20 and above installed under WSL may already have the concept of services; please verify this yourself.
[^docker]: Docker’s official website is: https://desktop.docker.com/
[^virtualbox]: Virtualbox is currently the most popular desktop-level virtual machine. Its use is completely free. Website address: https://www.virtualbox.org/
[^6-sigma]: In statistics, 6 sigma means a confidence level of 99.99966%. In quality inspection scenarios, it indicates that products have reached a very high quality standard. Starting from the 1970s, Motorola discovered the positive correlation between improving quality and reducing production costs, thus developing a complete set of methods to improve industrial processes and eliminate defects. In 1986, Motorola officially named it 6-sigma. It emphasizes continuous improvement, stable and predictable improvement of process results; production and business processes can be improved through measurement, analysis, improvement, and control, etc. With the decline of Motorola’s influence, the influence of 6-sigma has also gradually declined, but its core viewpoints and methods, such as continuous improvement, are still widely recognized and disseminated.
[^kite]: https://www.kite.com/
[^Github Copilot]: https://www.copilot.ai/
[^spyder]: https://www.spyder-ide.org/
