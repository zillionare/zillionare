---
title: "Chapter 9: Continuous Integration & Automation with GitHub Actions"
date: "2026-10-09"
slug: en/articles/python/best-practice-python/chap09
tags: [Continuous Integration, Github Actions, Devops, Python Packaging]
excerpt: "Learn to implement robust CI/CD pipelines using GitHub Actions. This chapter covers workflow definitions, matrix builds, and automated publishing for Python libraries, ensuring code quality and streamlined releases."
lang: en
translation_of: articles/python/best-practice-python/chap09
auto_translated: true
source_sha: 60bcbe1591cfc95ed89e7ed130c5e0111bb1d4ea
---

When a team of developers collaborates on a project, conflicts seem inevitable. In Chapter 8, we introduced branching and the Gitflow workflow model to resolve code conflicts. However, merging code only achieves superficial harmony. Whether code developed by different people works together ultimately depends on testing.

In the development workflows described earlier, developers should pass unit tests and code checks executed by `tox` before checking in code and pushing it to the remote server. However, if a developer intentionally skips these steps, poor-quality code can still slip into the repository. Furthermore, even though we virtualized the testing environment, it is still possible for tests that pass on one developer’s machine to fail in another. For example, new configuration items might have been introduced that exist in the local environment but are unknown to others; or local databases were modified, but the corresponding migration scripts were not integrated, and so on. If all tests are automatically executed on a public machine whenever new code is checked in, it ensures code correctness and allows us to identify issues earlier, reducing later maintenance costs. This is the essence of **Continuous Integration (CI)**.

Continuous Integration is a DevOps software development practice. When adopting CI, developers regularly merge code changes into a central repository, after which the system automatically runs build and test operations. CI typically refers to the build or integration phase of the software release process, involving both automated components (e.g., CI or build services) and cultural components (e.g., organizational processes and norms, such as learning to integrate frequently). The primary goal of CI is to discover and resolve defects faster, improve software quality, and reduce the time required to verify and release new software updates.

!!! Info
    The culture emphasized by CI is: *Fail fast, fail often.* However, once a robust CI/CD pipeline and culture are established, the ultimate result is *Move fast and don't break things*.

## 1. Surveying CI Software and Online Services

Let’s first meet the leading players in the CI field. Jenkins is the veteran in the CI space, having evolved over nearly 20 years since its inception, with the most complete community and ecosystem. GitLab, originally a Git-based code hosting platform, began providing CI functionality starting from version 8.0. Its advantage is seamless integration with code repositories, natively supporting pipeline triggers for various code repository events. The downside is that both Jenkins and GitLab require self-hosted servers, which can be costly for open-source projects and individual developers.

The cost of building a CI server is expensive. Before virtual machines became widely used, this cost was even higher. You would need at least one machine for each operating system your application needs to deploy to. If your application needs to deploy across various versions of Windows, Linux, and macOS, you might need to prepare at least ten physical machines. The advent of virtualization significantly reduced CI costs, followed by containerization, which further lowered them. However, even with these advancements, the cost of self-hosting and maintaining a CI server remains high for open-source projects. For instance, if your application needs to deploy to macOS, you must have at least one Apple server, as macOS containers cannot be virtualized on other hardware.

This is why we recommend using online CI services. The good news is that many online CI services are free for open-source projects. Here, we will only introduce Travis CI and GitHub Actions.

Travis CI is a cloud-based continuous integration service that helps developers build and test code on GitHub, thereby reducing software release time. Travis CI provides a certain amount of service time for open-source projects; for private projects, payment is required, starting at $69 per month. This pricing itself illustrates the value of CI and the resources required to implement it.

GitHub Actions is a continuous integration service launched by GitHub around 2020. Its advantages, similar to GitLab CI, lie in its seamless integration with code hosting services. Regarding pricing, GitHub Actions is free for open-source projects, offering a more generous free quota compared to Travis CI, which is sufficient for most uses. Therefore, we will skip Travis CI in this chapter and directly introduce GitHub Actions.

## 2. GITHUB ACTIONS

GitHub Actions is a continuous integration and delivery platform that allows us to automate builds, tests, and deployments like a pipeline. You can create workflows to build and test every pull request to a repository, or deploy merged pull requests to production.

GitHub provides infrastructure for Linux, Windows, and macOS via cloud services, but also allows us to deploy locally on our own private clouds.

### 2.1. Architecture and Concepts of GitHub Actions

GitHub Actions consists of components such as workflows, events, jobs, actions, and runners.

A workflow is defined by a YAML file located in the `.github/workflows` directory at the root of the project. We can simply view this file as a script. It defines which events can trigger the workflow, what jobs the workflow should contain, and on which runners (containers) the jobs should run. A repository can have multiple workflows, each executing different sets of tasks.

An event is a specific occurrence that triggers a workflow, such as when someone creates a pull request or pushes a commit to the repository.

A job is a set of steps executed on the same runner within a workflow. Each step is either a shell script to be executed or an action to be run. Steps are executed sequentially and are interdependent. Since each step runs on the same runner, you can share data from one step to another. For example, a step testing the generated application can follow a step building the application.

A workflow can contain multiple jobs. Jobs have no default dependencies and run in parallel. However, we can configure a job to depend on another, meaning it will wait for the dependent job to complete before running. For example, you might have multiple test jobs for different architectures with no dependencies, and a packaging job that depends on these tests. The test jobs will run in parallel, but the packaging job will only run after they all succeed.

An action is a custom application for the GitHub Actions platform that performs complex but frequently repeated tasks. Using actions helps reduce the amount of repetitive code written in workflow files. Actions can pull git repositories from GitHub, set up the correct toolchain for your build environment, or set up authentication for cloud providers.

You can write your own actions or find actions to use in your workflows on the GitHub Marketplace.

A runner is the server that runs the workflow. Each runner can execute one job at a time. GitHub provides Ubuntu Linux, Microsoft Windows, and macOS runners to execute your workflows; each workflow run is executed on a newly provisioned virtual machine (or container).

The following diagram illustrates the architecture of GitHub Actions:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/overview-actions.png)

### 2.2. Workflow Syntax Overview

After understanding the architecture of GitHub Actions, let’s explain how to define a workflow using an example.

First, let’s look at a workflow file generated by `ppw`:

```yaml
name: dev build CI

# 定义哪些事件可以触发工作流，以及筛选条件
on:
  # 当存储库有 PUSH 或者 PULL_REQUEST 事件时触发
  push:
    branches:
      - '*'
  pull_request:
    branches:
      - '*'

# 定义作业集
jobs:
  # 工作流包含三个作业，分别是 TEST, PUBLISH_DEV_BUILD, NOTIFICATION
  test:
    # 定义作业的运行环境，这里使用了矩阵式定义
    strategy:
      matrix:
        python-versions: ['3.8', '3.9', '3.10']
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    # 将步骤的输出提升为作业的输出，以便它们可以在作业之间共享
    outputs:
      package_version: ${{ steps.variables_step.outputs.package_version }}
      package_name: ${{ steps.variables_step.outputs.package_name }}
      repo_name: ${{ steps.variables_step.outputs.repo_name }}
      repo_owner: ${{ steps.variables_step.outputs.repo_owner }}

    # 这是启用外部服务的一个示例
    # SERVICES:
    #   REDIS:
    #     IMAGE: REDIS
    #     OPTIONS: >-
    #       --HEALTH-CMD "REDIS-CLI PING"
    #       --HEALTH-INTERVAL 10S
    #       --HEALTH-TIMEOUT 5S
    #       --HEALTH-RETRIES 5
    #     PORTS:
    #       - 6379:6379

    # 步骤集代表了一系列的任务，这些任务将作为作业的一部分执行
    steps:
      # 作业是在容器里执行的，我们需要先将代码检出到这个干净的容器里
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-versions }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox tox-gh-actions poetry

      # 这一步里，我们设置了一些变量，将其输出到控制台，从而可以在第 85 行提升为 JOB 的输出
      - name: Declare variables for convenient use
        id: variables_step
        run: |
          echo "::set-output name=repo_owner::${GITHUB_REPOSITORY%/*}"
          echo "::set-output name=repo_name::${GITHUB_REPOSITORY#*/}"
          echo "::set-output name=package_name::`poetry version | awk '{print $1}'`"
          echo "::set-output name=package_version::`poetry version --short`"
        shell: bash

      # 执行单元测试和代码检查。
      - name: test with tox
        run: tox

      # 通过 CODECOV 上传测试覆盖率。
      - uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: true

  publish_dev_build:
    # 只有 TEST 作业完成，我们才开始本作业
    needs: test
    # 指定本作业运行的操作系统环境。
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          # 这一步只需要在任意一个 PYTHON 版本上运行
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry tox tox-gh-actions

      - name: build documentation
        run: |
          poetry install -E doc
          poetry run mkdocs build
          git config --global user.name Docs deploy
          git config --global user.email docs@dummy.bot.com
          poetry run mike deploy -p -f --ignore "`poetry version --short`.dev"
          poetry run mike set-default -p "`poetry version --short`.dev"

      - name: Build wheels and source tarball
        run: |
          poetry version $(poetry version --short)-dev.$GITHUB_RUN_NUMBER
          poetry lock
          poetry build

      - name: publish to Test PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.TEST_PYPI_API_TOKEN}}
          repository_url: https://test.pypi.org/legacy/
          skip_existing: true

  notification:
    needs: [test,publish_dev_build]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: martialonline/workflow-status@v2
        id: check

      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build successfully
          convert_markdown: true
          html_body: |
            ## Build Success
            ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version }} is built and published to test pypi

            ## Change Details
            ${{ github.event.head_commit.message }}

            For more information, please check change history at https://${{ needs.test.outputs.repo_owner }}.github.io/${{ needs.test.outputs.repo_name }}/${{ needs.test.outputs.package_version }}/history

            ## Package Download
            The pacakge is available at: https://test.pypi.org/project/${{ needs.test.outputs.package_name }}/

      - name: build failure notification via email
        if: ${{ steps.check.outputs.status == 'failure' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build failure
          convert_markdown: true
          html_body: |
            ## Change Details
            ${{ github.event.head_commit.message }}

            ## View Log
            https://github.com/${{ needs.test.outputs.repo_owner }}/${{ needs.test.outputs.repo_name }}/actions
```

This is a job named `dev build CI`, which triggers on commits and pull requests to any branch. It contains three jobs: `test` (executes unit tests), `publish_dev_build` (builds and publishes a development version to test_pypi), and `notification` (sends an email notification upon build success or failure). There are dependencies among them: if the `test` job fails, `publish_dev_build` is canceled; however, regardless of whether `test`/`publish_dev_build` succeeds, the `notification` job will execute and send emails with different content based on the status of the previous two jobs.

This is a relatively simple job, but it involves almost everything we need to do in CI. The code includes many comments; readers are advised to read the code carefully in conjunction with the following explanation.

#### 2.2.1. Defining Trigger Conditions

Lines 4 to 14 configure the workflow’s trigger conditions. The trigger conditions section is introduced by the keyword **'on'**. Under this, we can define multiple trigger events and specify types and filters for each. A complete trigger condition configuration is as follows:

```yaml
on:
    push:
        branches: 
          - '*'
        tags:
          - v*
    label:
        branches:
            - main
        types:
            - created
    schedule:
        - cron: '30 5 * * 1,3'
```

In the above example, `'push'`, `'label'`, `'tags'`, and `'schedule'` are all event keywords. Available event keywords can be found in [Events that trigger workflows](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows).

Under the event level is where activity types and filters are defined. Not all events have activity types, and even if they do, their types may differ. For instance, the `push` event has no activity type, while the `label` event has three activity types: `created`, `edited`, and `deleted`. The `issues` event has activity types like `opened` and `labeled`. To see what activity types an event has, refer to [Events that trigger workflows](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows).

Filters come in two types: `branches` and `tags`, used to specify branches and tags, respectively. As seen in the example, filter values support glob patterns, meaning we can use wildcards like `*`, `**`, `+`, `?`, and `!` to match branch and tag names. In addition to the positive matching in the example, we can also use `branches-ignore` or `tags-ignore` for negative matching.

The above example also demonstrates a special event: the `'schedule'` event. This causes the workflow to run periodically. This can be used to run security scans, dependency upgrade scans, and other tasks.

#### 2.2.2. Defining Job Sets

Next, the workflow declares three jobs: `test`, `publish_dev_build`, and `notification`. The job definition section is introduced by the keyword **'jobs'**. Under this, we can define multiple jobs and specify the runtime environment and execution steps for each job.

Each job has its own ID and name. In the above example, `test`, `publish_dev_build`, and `notification` are all job IDs. The job ID is mandatory, but the job name is optional. If no job name is specified, the job name defaults to the job ID. The job name is used to display the job’s name on the GitHub Actions interface.

In the job `publish_dev_build`, we define its dependency on the job `test` using the keyword `needs`. In line 114, we also see that a job can depend on a set of jobs. When specifying job dependencies, note that only job IDs can be used, not job names.

Next, we define the execution environment for the job. The environment is defined via the keyword `runs-on`. Some tasks only need to run on one machine, such as building and publishing Python packages; others need to run on all machines and with multiple Python runtimes, such as testing.

For example, the `publish_dev_build` job only needs to run on the combination of `ubuntu-latest` and Python 3.9, as the results should be identical regardless of the combination. Lines 78 and 84 are examples of specifying a single execution environment. However, for test tasks, we want them to run on all machines and across different Python versions. To express this concisely, GitHub Actions introduced the concept of a matrix.

We define the test matrix via `strategy.matrix`. In the matrix defined in lines 20–23 of the example, we defined lists of Python versions and operating systems. This definition is subsequently used in line 24, where we reference the operating system definition via `{{matrix.os}}`. The `python-versions` in line 22 is a special keyword indicating the Python versions we want to use. If our development language is not Python, this specification would be meaningless.

Next, we need to define the specific tasks for the job, which are categorized under the steps set (`steps`). The steps set is a list containing multiple steps. Each step is either a shell command (or a set of shell commands) or an action. To run shell commands, we use the following syntax:

```yaml
- name: <step name>
  run: <shell command>
```

To run a set of shell commands, we use:

```yaml
- name: <step name>
  run: |
    <shell command 1>
    <shell command 2>
    ...
```

Note the differences between these two syntaxes; do not confuse them.

As mentioned earlier, actions are custom applications for the GitHub Actions platform. You can write your own actions or find applications developed by others in the GitHub Marketplace.

Each step can specify a Python runtime. In line 48, we see that `{{ matrix.python-versions }}` uses the Python version defined in the matrix. In line 84, we directly specify a Python version. Note that the version number is a string; we can use `'3.10'`, but not `3.10`, as the latter would be parsed by YAML as `3.1`, leading to a "Python version not found" error.

Finally, we introduce runtime condition controls for jobs. We have already discussed dependencies between jobs, which can be considered a type of condition. Another scenario, such as in the example’s `notification` job, requires it to run only after the first two jobs are completed (regardless of success or failure), but to send different content notification emails based on the status of previous jobs. In this case, we need to introduce `if` conditional controls.

The `if` conditional control can apply at the job scope (as shown in line 116) or the step scope (as shown in line 123). At the job scope, we can use functions like `success()`, `failure()`, `cancelled()`, and `always()` to specify under what conditions this job should run. At the step scope, we can perform simple conditional judgments to indicate whether this step should run.

Conditional judgments inevitably require variables. Now, we will comprehensively introduce the use of variables in workflows. By combining variables with various control conditions, we can achieve advanced techniques.

Variables in GitHub are divided into two types: system variables and job variables. System variables are provided by the GitHub platform, while job variables are defined by us. Regardless of the type, we reference them via `${{ }}`.

System variables can be defined at the organization, repository, or environment level. For example, `secrets` are defined at the repository level. We can access its value via `${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}`, which requires us to pre-define the variable `BUILD_NOTIFY_MAIL_RCPT` in the repository. GitHub provides some default variables, such as `GITHUB_REPOSITORY` (the value of this variable is the repository owner and name, e.g., octocat/Hello-World; line 59 of the example uses this variable and demonstrates a string extraction technique).

The following code demonstrates the usage of job variables (excerpted from lines 122–132 of the example):

```yaml
  notification:
    needs: [test,publish_dev_build]
    steps:
      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          subject: ${{ needs.test.outputs.package_name }}.
```

First, in the job `test`, the output of the step `variable_step` (lines 57–63) is promoted to the job’s output (lines 24–28), effectively declaring four variables such as `package_name`. Then, in the code above, we reference these variables (e.g., `package_name`) via `${{ needs.test.outputs.package_name }}`. Variables are referenced via `{job_id}.outputs.{variable}`, which is straightforward. However, note that it also has a `needs` scope. This indicates that if the job where we use the variable does not declare a dependency on the `test` job, this variable cannot be referenced.

The example does not show the usage of environment variables. Here is an example for readers to study with the comments:

```
env:
  # 声明了一个全局上下文的环境变量
  DAY_OF_WEEK: Monday

jobs:
  greeting_job:
    runs-on: ubuntu-latest
    env:
      # 声明了一个作业上下文的环境变量
      Greeting: Hello
    steps:
      - name: "Say Hello Mona it's Monday"
        # 使用时我们在变量前加一个`ENV.`的约束
        if: ${{ env.DAY_OF_WEEK == 'Monday' }}
        # 当使用的环境变量是在作业内声明时，我们可以省略`ENV.`的约束
        run: echo "$Greeting $First_Name. Today is $DAY_OF_WEEK!"
        env:
          # 声明了步骤上下文的环境变量
          First_Name: Mona
```

#### 2.2.3. Connecting to Other Services

In lines 31 to 40 of the example, there is commented-out code used to enable the Redis service. GitHub Actions provides these services via container technology. Theoretically, as long as an image for a certain service exists on Docker Hub, we can use it in GitHub Actions.

!!! Attention
    Note that if we want to use services in a workflow, the runner must be the Ubuntu operating system, not other Linux systems, Windows, or macOS.

Our workflows can run on the runner or in a container (which runs on the runner). If the workflow runs in a container, we need to connect to services running in the container via a custom bridge network. If the workflow runs directly on the runner, we can map the container’s ports to the runner, allowing us to access the services in the container directly.

Using services in a workflow generally requires waiting for the container to fully start and initialize. This is the purpose of line 35 (`REDIS-CLI PING`).

## 3. Third-Party Applications and Actions

We have already seen some actions from the marketplace in the example, such as `actions/checkout`, `actions/setup-python`, `pypa/gh-action-pypi-publish`, `dawidd6/action-send-mail`, `codecove/Codecov`, and so on. The part before the '/' is the action’s author. Actions authored by `actions` are official GitHub actions; others are third-party actions. The names of these actions already indicate their functions, so we will not elaborate further here.

Below, we introduce some commonly used third-party actions, some of which we have briefly explained with usage examples. If we have not specified otherwise, or if you wish to learn more, you can visit the [marketplace](https://github.com/marketplace/actions) to view relevant documentation.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>


### 3.1. GitHub Pages Deployment

This action can be used to deploy static websites to GitHub Pages. In projects generated by `ppw`, it is used in conjunction with `mkdocs/mike`. Its ID is `JamesIves/github-pages-deploy-action`. A usage example is as follows:

```
name: Build and Deploy
on: [push]
permissions:
  contents: write
jobs:
  build-and-deploy:
    concurrency: ci-${{ github.ref }} # Recommended if you intend to make multiple deployments in quick succession.
    runs-on: ubuntu-latest
    steps:
      - name: Checkout 🛎️
        uses: actions/checkout@v3

      - name: Install and Build 🔧 # This example project is built using npm and outputs the result to the 'build' folder. Replace with the commands required to build your project, or remove this step entirely if your site is pre-built.
        run: |
          npm ci
          npm run build

      - name: Deploy 🚀
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: build # The folder the action should deploy.
```

### 3.2. Building and Publishing Docker Images

Obviously, as a step in continuous deployment, the building of Docker images should also be completed and published by the CI/CD server. Docker officially provides an action for this purpose, with the ID `docker/build-push-action`.

### 3.3. GitHub Release

Generally, Python projects are published via PyPI. However, we can also publish them to GitHub Releases. The ID for this action is `softprops/action-gh-release`.

### 3.4. Drafting Release Notes

Writing release notes is a tedious task. `release-drafter/release-drafter` can help us automatically generate draft release notes. It automatically finds useful information from code commit logs to organize a release note.

When writing release notes, we usually only need to record functional changes, bug fixes, and performance enhancements that affect external usage. However, during code commits, there are various types of commits. In addition to the aforementioned categories, there are document revisions, code formatting, CI process changes, and so on. How does Release-drafter automatically filter out this useless information? This requires us to strictly categorize commits and follow standardized formats when committing. In Section 2 of Chapter 2, we introduced an extension for editing commit messages. By using such tools, we can ensure that our commit logs are well-categorized, allowing Release-drafter to perform automatic information extraction to form a draft. Even if manual editing is still required, the workload will be significantly reduced.

As we stated at the beginning, good development habits cannot rely solely on cultivating programmers’ awareness. More importantly, we must use a series of interlinked tools to streamline our processes, thereby enforcing compliance.

There are also some fun actions, such as an action that generates a Snake game, with the ID `Platane/snk`. It generates the following Snake game:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/github-contribution-grid-snake.svg)

### 3.5. Notification Messages

We have introduced email notifications. In the marketplace, there are various notification actions, such as Slack notifications, which can be found via the ID `Ilshidur/action-slack`.

### 3.6. Giscus

Giscus is a comment system based on GitHub Discussions. Its ID is `giscus/giscus`. If you use GitHub Pages as your blog and static site system, you can install it on GitHub and add comment functionality to your blog and static site system.

## 4. Publishing Python Libraries via GitHub CI

The examples we saw earlier come from the `.github\workflows\dev.yml` file in the `ppw`-generated project. This workflow applies to all branches and triggers on every push. Its purpose is to perform integration tests, build test packages, and publish them to testpypi, as well as publish informal documentation to GitHub Pages.

Formal version releases are handled by `release.yml`. This workflow applies only to the `main` branch and runs only when a tag event occurs on the `main` branch, and the tag starts with the letter 'v'. Below is the content of this workflow:

```yaml title="release.yml"
# PUBLISH PACKAGE ON RELEASE BRANCH IF IT'S TAGGED WITH 'V*'

name: build & release

# CONTROLS WHEN THE ACTION WILL RUN.
on:
  # TRIGGERS THE WORKFLOW ON PUSH OR PULL REQUEST EVENTS BUT ONLY FOR THE MASTER BRANCH
  push:
    branch: [main, master]
    tags:
      - 'v*'

  # ALLOWS YOU TO RUN THIS WORKFLOW MANUALLY FROM THE ACTIONS TAB
  workflow_dispatch:

# A WORKFLOW RUN IS MADE UP OF ONE OR MORE JOBS THAT CAN RUN SEQUENTIALLY OR IN PARALLEL
jobs:
  release:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-versions: ['3.9']

    # MAP STEP OUTPUTS TO JOB OUTPUTS SO THEY CAN BE SHARE AMONG JOBS
    outputs:
      package_version: ${{ steps.variables_step.outputs.package_version }}
      package_name: ${{ steps.variables_step.outputs.package_name }}
      repo_name: ${{ steps.variables_step.outputs.repo_name }}
      repo_owner: ${{ steps.variables_step.outputs.repo_owner }}

    # STEPS REPRESENT A SEQUENCE OF TASKS THAT WILL BE EXECUTED AS PART OF THE JOB
    steps:
      # CHECKS-OUT YOUR REPOSITORY UNDER $GITHUB_WORKSPACE, SO YOUR JOB CAN ACCESS IT
      - uses: actions/checkout@v2

      - name: build change log
        id: build_changelog
        uses: mikepenz/release-changelog-builder-action@v3.2.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-versions }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox-gh-actions poetry

        # DECLARE PACKAGE_VERSION, REPO_OWNER, REPO_NAME, PACKAGE_NAME SO YOU MAY USE IT IN WEB HOOKS.
      - name: Declare variables for convenient use
        id: variables_step
        run: |
          echo "::set-output name=repo_owner::${GITHUB_REPOSITORY%/*}"
          echo "::set-output name=repo_name::${GITHUB_REPOSITORY#*/}"
          echo "::set-output name=package_name::`poetry version | awk '{print $1}'`"
          echo "::set-output name=package_version::`poetry version --short`"
        shell: bash

      - name: publish documentation
        run: |
          poetry install -E dev
          poetry run mkdocs build
          git config --global user.name Docs deploy
          git config --global user.email docs@dummy.bot.com
          poetry run mike deploy -p -f --ignore `poetry version --short`
          poetry run mike set-default -p `poetry version --short`

      - name: Build wheels and source tarball
        run: |
          poetry lock
          poetry build

      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          body: ${{ steps.build_changelog.outputs.changelog }}
          draft: false
          prerelease: false

      - name: publish to PYPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.PYPI_API_TOKEN }}
          skip_existing: true
```

The syntax features used in this workflow have been explained previously, so we will not explain them here.

<div style="width:70%;height:380px">
<div style="width:100%; height: 360px; margin: 0 auto;background-image:url('https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/book-with-flower.png');background-size:contain;background-repeat:no-repeat">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/mybook-0914.png" style="position:relative; width: 20%;top:62%;left:35%"/>
</div>
<div style="margin-top: 10px;text-align:right;padding-right:10px;">
<a style="border: 0px solid blue;" href="https://union-click.jd.com/jdc?e=618%7Cpc%7C&p=JF8BAQIJK1olXwMKVllVD0kUB18IHlwcXgYHVW4ZVxNJXF9RXh5UHw0cSgYYXBcIWDoXSQVJQwYHU1deCE4WHDZNRwYlOXleFilHbwl3CzdxcxxqDW9dMyEfaEcbM244G1oUXwMFU1hZC3snA2g4STXN67Da8e9B3OGY1uefK1olXQABVF9YCkMWCmgAHmsSXQ8yDQ0NWAhJXF84K1glWgYLQFgvSRkDBR04K1slXjYCVV5VC04VAGsKEkcVXQ8KVFhBCE0UA24NG1MWWwILVG5fCUoTCl84Kz5lDQVbDhslfANDdRQKXQJVLWUEDFY1fCUVAw8PYRxjVVF2AAo4eDZqWBg4Hms">Click this link to purchase the official version of this book</a>
</div>
</div>
