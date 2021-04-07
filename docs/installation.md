---
disqus: jieyu
---

大富翁提供了两种安装方式。

推荐新手使用Docker发行版的安装方式。这种方式下，您只需要非常简单的配置即可快速使用大富翁。

高级安装模式允许您配置复杂的网络环境和多机部署，以充分施展大富翁的性能。关于高级安装模式，请参考 ==[TODO](404.md)==
# 1. 安装大富翁Docker发行版
## 1.1. 确认安装环境

在安装大富翁之前，请先确认您的安装环境中已经安装了 **docker engine** 和 **docker-compose**。前者是一个Native程序，后者是一个Python module，可以通过`pip`来安装。

??? Info

      大富翁使用了`docker-compose`来进行容器编排，编排配置文件的版本是`v3.6`。对应要求的`docker engine`的版本是18.02，对应的`docker-compose`版本是`1.27.0+`。

      大富翁1.0进行测试时，使用的`docker engine`的版本是`19.03`, `docker-compose`的版本是`1.28.5`。一般而言，只要您使用的版本满足上面的要求，都应该可以安装成功。

此外，由于大富翁当前只提供了对聚宽数据源的对接，所以您还需要在[聚宽官网](https://www.joinquant.com)上申请一个账号。

## 1.2. 运行安装程序

### 安装到Linux操作系统
您可以在这里下载[大富翁安装程序](download/zillionare.sh?latest)，并在命令行界面运行以下命令：
```bash
# 下载安装程序到本地
curl http://www.jieyu.ai/download/zillionare.sh?latest -o zillionare.sh

# 运行安装程序
sudo -E bash zillionare.sh --target /usr/local/zillionare -- --jq_account $JQ_ACCOUNT --jq_password $JQ_PASSWORD
```

您需要将这里的`$JQ_ACCOUNT`和`$JQ_PASSWORD`替换成您申请的聚宽账号。

??? Info

      执行以上命令，安装程序就会将一些文件拷贝到/usr/local/zillionare目录下，并且调用`docker-compose`命令来启动服务。
      
      一般情况下，`/usr/local`目录是`root`权限，但可以通过`sudo`授权访问。而`docker engine`也常常是通过`sudo`命令来安装的，因此在调用`docker`命令时，如果是非`root`用户，也就需要通过`sudo`来授权。

      `--target`指定了安装程序存放文件的位置。一般建议就使用我们推荐的`/usr/local/zillionare`目录。`/usr/local`目录是Linux下安装用户程序的标准目录。如果您**忽略**了这个参数，那么zillionare将会安装到您当前位于的目录。

      然后是分割符"--"。我们使用了[makeself](https://github.com/megastep/makeself)来进行打包。这是一个广泛使用的生成自解压shell程序的应用。根据`makeself`的要求，在`--`之后的是传递给安装脚本的运行参数，而在`--`之前的参数，都将传递给`makeself`自己使用。这个"--"一定不能省略。

      然后是运行zillionare需要的参数。核心参数是`jq_account`和`jq_password`。

??? Warning

      如果您输入的安装命令格式不正确，可能产生高CPU的情况。常见的命令格式错误有：

      1. 缺少用以分割的"--"。 注意命令行中，在--target与--jq_account之间多出来的`--`。这个一定不能省略。

      2. 安装程序的参数与它们的取值之间，使用**空格**，而不是**等号**来连接。


在安装过程中，您将从控制台看到构建docker镜像和容器的一些信息。如果一切正常，最终将输出以下信息：
```console
Successfully built 96ac04414e07
Successfully tagged zillionare/zillionare:1.0.0.a3
redis is up-to-date
Creating postgres ... done
Creating zillionare ... done
```

??? Tip
      在安装过程中，您的控制台可能出现以红色字体输出的日志信息。如果它们属于nbextension安装过程中的输出，则无需担心。这是nbextension的一个易用性问题。

      nbextension的安装日志类似如下：
      ```
      [I 15:36:07 InstallContribNbextensionsApp] Up to date: /root/.local/share/jupyter/nbextensions/ruler/main.js
      [I 15:36:07 InstallContribNbextensionsApp] Up to date: /root/.local/share/jupyter/nbextensions/ruler/ruler_editor.yaml
      [I 15:36:07 InstallContribNbextensionsApp] - Validating: OK
      ```

在安装结束后，大富翁服务将自动启动。

现在，您可以跳转到[检查安装结果和管理服务](#安装到其它操作系统)继续阅读。

### 安装到其它操作系统
如果您使用其它操作系统，您需要从源文件开始安装。不过，安装过程也很简单。

首先，从[这里](http://www.jieyu.ai/download/zillionare.tar.gz)下载压缩包。然后将其解压到某个**空**文件夹。

接下来，您需要进入该文件夹，新建一个名为.env的文件，文件内容如下：
```text
JQ_ACCOUNT=%replace_with_your_account%
JQ_PASSWORD=%replace_with_your_password
```

???+ Warning

      注意这里的JQ_ACCOUNT等变量必须为大写。

然后，通过运行`docker-compose up`命令启动服务。注意您需要在安装文件夹位置下运行这个命令。

# 检查安装结果和管理服务
## Linux安装版
在Linux安装版下，我们提供了一些便捷的命令来管理服务。
```bash
sudo zillionare

-- output --
     命令格式: zillionare args
     Args:
        start: 启动zillionare服务
        stop: 停止zillionare服务
        restart: 重启zillionare服务
        down: 中止zillionare服务，并删除相关容器
        log: 显示zillionare日志
        status: 显示zillionare容器运行状态
```

所以，您可以通过`start`, `stop`, `restart`来启动和停止服务。由于我们刚刚完成安装，所以您可能希望知道服务的状态：

```bash
      sudo zillionare status
```
这会显示类似下面的信息：
```console
   Name                 Command               State                                   Ports                                 
----------------------------------------------------------------------------------------------------------------------------
postgres     docker-entrypoint.sh postgres    Up      5432/tcp                                                              
redis        docker-entrypoint.sh sh -c ...   Up      6379/tcp                                                              
zillionare   /root/zillionare/entrypoint.sh   Up      0.0.0.0:3180->3180/tcp, 0.0.0.0:3181->3181/tcp, 0.0.0.0:8888->8888/tcp
```

您还可以通过`sudo zillionare log`来更进一步地观察大富翁当前的状态。

```bash
sudo zillionare log
```
如果您是在安装之后立刻运行的上述命令，那么输出的最后几行很可能是：
```console
正在启动zillionare-omega fetcher...
启动的jqadaptor实例少于配置要求（或尚未启动），正在启动中。。。
   impl   |     port   |  pids
jqadaptor |     3181   |  [48]
正在导入最近 13 月的历史K线数据...
```

## 其它操作系统
我们没有在其它操作系统上提供类似Linux版下提供的那些命令。不过，那些命令最终都是通过`docker-comose`或者`docker`来实现的。

这里我们给一个命令对照表供参考：

| 功能      | Linux                   | 其它操作系统                    | 说明         |
| ------- | ----------------------- | ------------------------- | ---------- |
| 启动服务    | sudo zillionare start   |  docker-compose up        | 需要在安装目录下运行 |
| 暂停服务    | sudo zillionare stop    | docker-compose stop       | 需要在安装目录下运行 |
| 重启服务    | sudo zillionare restart | docker-compose restart    | 需要在安装目录下运行 |
| 停止并删除容器 | sudozillioare down      | docker-compose down       | 需要在安装目录下运行 |
| 获取状态    | sudo zillionare status  | docker-compose status     | 需要在安装目录下运行 |
| 获取日志    | sudo zillionare log     | docker logs -f zillionare |            |

## 检查服务状态

在安装中，我们一共创建了5个服务，一般来说，有三个您需要关注一下它们的状态，即Quotes fetcher服务， jobs服务和Notebook服务。另外两个， redis和postgres都是从官方镜像创建的，一般情况下并不会出现问题。

### 服务端口
在host机器上运行一下命令，以查看各种服务的监听端口：
```
sudo docker ps -a
```
下面是输出示例：
```console
Names        PORTS
zillionare   0.0.0.0:32771->3180/tcp, 0.0.0.0:32770->3181/tcp, 0.0.0.0:8888->8888/tcp
```
为了输出美观，这里省略了一些列，并重排了次序。

这里可以看到有三个映射的端口，32771映射到了3180，这个是jobs进程的监听端口；32770映射到了3181，这个是Quotes Fetcher的监听端口；8888映射到了8888端口，这个是Jupyter notebook的监听端口。

### Quotes Fetcher服务
Zillionare架构在微服务之上，因此行情数据获取（Quotes fetcher)也是一个服务。可以通过以下命令来查看其状态：

```
curl -L ip_of_your_docker_host:32771/sys/version
```
或者在浏览器中打开上面的地址。您应该看到一个纯文本的版本信息。注意您要根据[](#服务端口)中的结果来调整这里的端口。

### Jobs服务

Zillionare使用jobs来管理各种任务，jobs本身也是一个服务。您可以通过以下命令来查看其状态：
```
curl -L ip_of_your_docker_host:32770/jobs/status
```
或者在浏览器上打开上面的地址。如果没有任何错误信息，则说明一切工作正常。注意您要根据[](#服务端口)中的结果来调整这里的端口。

### Notebook 服务

随容器发布的除了大富翁应用外，还有一个Jupyter Notebook服务及相关教程。在您安装完成后，请打开浏览器，输入以下网址：

`http://ip_of_your_docker_host:8888/`

这里请将zillionare替换成您刚刚运行安装程序的那台机器的IP。页面打开后，会显示我们的量化交易教程。

![](http://images.jieyu.ai/images/202103/20210321104648.png){: style="width:300px"}

# 如何定制您的安装

您可以通过安装时传入参数（如果是非Linux平台，则是通过修改.env文件）来进行一些定制。

大富翁允许您在初始化时，导入历史行情数据。当前默认为导入13个月（含30分钟及以上K线）。如果您对数据要求比较高，并且机器硬件性能足够（全市场每1000条k线需要0.75GB内存），也可以修改参数，以导入更多的k线数据。

如果是Linux发行版，您需要在运行安装脚本时指定`--init_bars_months`参数：

```bash
sudo -E bash zillionare.sh --target ... -- --jq_account my_account --jq_password my_passwd --init_bars_months 24
```
上面的命令将导入24个月的K线数据。

如果是其它操作系统，您需要修改安装目录下的.env文件（参见[](#安装到其它操作系统):
```text
INIT_BARS_MONTHS=24
```

???+ Warning

      注意这里的变量必须为大写，以下同

其它参数的定制，在使用语法上类似，所以下面就简单列出这些参数，至于如何修改，请参见上面的内容：

| 参数名               | 作用                   | 默认值        | 说明                                           |
| ----------------- | -------------------- | ---------- | -------------------------------------------- |
| JQ_ACCOUNT        | 聚宽账号，必须提供            | 无          |                                              |
| JQ_PASSWORD       | 聚宽账号密码，必须提供          | 无          |                                              |
| INIT_BARS_MONTHS  | 初始化数据的月数             | 13         |                                              |
| POSTGRES_USER     | 数据库用户名               | zillionare | 允许使用现有的数据库，下同                                |
| POSTGRES_PASSWORD | 数据库密码                | 123456     |                                              |
| POSTGRES_DB       | 数据库名                 | zillionare | 即使使用现有数据库，也推荐单独创建名为zillionare的schema，以单独存放数据 |
| POSTGRES_HOST     | 数据库服务器               | postgres   |                                              |
| POSTGRES_PORT     | 数据库服务器监听端口           | 5432       |                                              |
| REDIS_HOST        | redis服务器             | redis      | 允许您使用现有的redis服务器                             |
| REDIS_PORT        | redis服务器监听端口         | 6379       |                                              |
| NOTEBOOK_PORT     | Jupyter Notebook监听端口 | 8888 | 允许您自定义notebook的端口，以便在端口冲突时使用 |

??? Info
      一般情况下，您不需要配置数据库服务器和Redis缓存服务器。大富翁提供上述定制参数的主要目的有二，一是避免服务器端口冲突；二是如果您确实已经部署了这两种服务器，希望能够复用。

      数据库复用是比较常见的。但不推荐对Redis缓存服务器复用。Redis没有数据库那样丰富的层次结构，无法辟出一块空间来单独存放zillionare的相关数据，因此可能产生数据冲突。为了避免键冲突，请尽量为zillionare单独分配Redis服务器。

# 排查安装错误
由于使用了Docker容器来进行部署，一般来说不太容易出现错误。但也可能因为以下原因导致安装或者运行失败：

1. 没有提供聚宽账号，或者当日Quota不足
2. Notebook端口冲突，请增加环境变量NOTEBOOK_PORT，设置为其它值
3. 在安装过程中遇到网络错误，导致镜像和容器生成失败
4. 在安装Linux版本时，命令格式错误。这在前面特别提到过了。

如果确实遇到了这些问题，请参考 ==[大富翁量化框架深度解析](404.md)== 中的 ==常见故障部分== 进行排查。

# 下一步

现在，大富翁已经在正常运行了。我们为您准备了[大富翁量化交易教程](zillionare/tutorial/preface.ipynb)，通过这个教程，您能了解到如何使用大富翁来获取数据，以及提取量化因子，构建基于机器学习（深度学习）的交易策略。

这部教程是使用Jupyter Notebook来写的。在您刚刚安装好的大富翁里，已经内置了这部教程（请参见[](#检查Notebook工作状态)。您也可以打开Notebook的页面来阅读，并运行里面的代码片段，这样上手可能会更快一些。