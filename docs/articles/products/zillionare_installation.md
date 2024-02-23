
<style>

table {
    background-color: transparent;
    border-collapse: collapse;
    border-spacing: 0;
    display: table !important;

    th {
        background-color: #E7F7F5;
    }

    th,
    td {
        border: none;
    }
}
pre code {
    white-space: pre-wrap;
}
</style>

<h1>大富翁2.0安装指南</h1>
!!! tip
    安装文件目前仅对大富翁量化课程学员及重要客户开放。联系请加 quantfans_99 (宽粉) 微信

我们通过docker集群向大家提供zillionare 2.0。该集群包含以下容器：

| NAMES                  | IMAGE                     | PORTS                                      |
| ---------------------- | ------------------------- | ------------------------------------------ |
| zillionare-omega       | zillionare/omega:2.0.1    | 0.0.0.0:3180->3180/tcp :::3180->3180/tcp   |
| zillionare-influxdb    | influxdb:2.4.0            | 0.0.0.0:58086->8086/tcp :::58086->8086/tcp |
| zillionare-backtesting | zillionare/backtest:0.5.1 | 0.0.0.0:7080->7080/tcp :::7080->7080/tcp   |
| zillionare-redis       | redis:7.0.4-alpine        | 0.0.0.0:56379->6379/tcp :::56379->6379/tcp |
| zillionare-lab         | zillionare/lab            | 0.0.0.0:8888->8888/tcp :::8888->8888/tcp   |


该系统是一个完整的研究环境，自带了两年的日线数据和30分钟数据（约1.3G）。启动后，通过8888端口访问研究环境。比如，如果安装该集群的机器IP为192.168.100.100，则可以通过 http://192.168.100.100:8888/zillionare 来访问研究环境：

![](https://images.jieyu.ai/images/2023/12/lab.png)

!!! Info
    登录密码默认为1234。如果您需要修改，请修改docker-compose安装目录下的.omega_env文件中的LAB_PASSWORD选项。

实盘交易安装东财量化交易客户端及gm-adaptor库，请情参见[实盘交易](#实盘交易)

## 安装步骤
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

!!! Info
    Zillionare 2.0基于docker容器技术构建，理论上可以运行于任何支持容器技术的操作系统上。但我们只测试了Ubunut Focal和Ubuntu Focal on WSL 2.0（即Windows）。
    如果您打算正式使用，建议硬件规格：

    1. 8核CPU以上
    2. 32GB内存以上（大家的课件环境是集群，单机96GB）
    3. 硬盘1T以上（很占空间）

1. 先安装docker和docker-compose工具。如果只有windows机器，建议先安装 wsl2，再在wsl2下的ubunut环境中，安装docker/docker-compose
   
2. 将zillionare.tar解压缩到安装目录（自定），修改其中的 .omega.env，该文件中，jqdata相关的账号和密码是需要提供的，其它的可以不变
   
3. 通过docker-compose up -D 启动集群。启动时会进行下载和数据导入。视您的网络定，应该在10分钟以内完成。

此后如果需要停止服务，运行docker-compose stop; 重新启动 docker-compose start；都需要在安装目录下运行。

## 数据加载
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

该环境自带的数据仅限于行情研究。如果需要使用**回测服务**，需要补齐分钟线数据。

Zillionare官方提供对聚宽数据服务的集成支持。您需要购买聚宽的数据服务。每天要至少有500万以上的quota。这样才能实现数据正常同步，并将缺失数据逐步追赶起来（到分钟级）。

!!! Info
    当前A股仅股票就有接近6000支，每天的分钟线数据接近140万条。Zillionare会在盘中实时请求所有股票和常用指数的分钟线数据，此外，还会在每晚2：00左右，再次请求前一交易日的分钟线、日线等数据，并且出于纠错的目的，会进行两次请求并进行数据校验。因此，每天会消耗quota 500万条以上。但如果要补齐历史分钟线数据，建议购买2亿条quota级别的数据。这样一天大概能向前追赶一个月的行情数据。

## 实盘交易
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

该环境支持实盘交易。您可以通过lab编写策略，通过zillionare-trader-client执行下单。目前zillionare只提供了东财的量化接口。安装方式如下：

1. 向东财申请开通量化接口
2. 在Windows机器上安装东财EMC客户端，并进行配置。
3. 在同一台Windows机器上安装 gmadaptor
4. 通过trader-client下单时，将url指向windows机器。

安装和配置详情，请见[东财实盘交易部署指南](docs/products/gm-adapter-installation.md)

## 配置

### 聚宽账号

```
JQ_ACCOUNT=notset
JQ_PASSWORD=passwd
```

### 邮件通知
配置邮件通知后，系统自带的一些报警消息会通过邮件发送出来。你可以将邮件配置成邮件列表，以便运维人员可以收到通知。配置后，您也可以在策略中，使用`omicron.notify`里的方法，发出邮件通知。[文档](https://zillionare.github.io/omicron/latest/api/omicron/#omicron.notify.mail)

```
MAIL_FROM=user@example.com
MAIL_TO=user@example.com
MAIL_PASSWORD=passwd
MAIL_SERVER=127.0.0.1
```
### 钉钉通知

邮件通知的实时性不太强，如果对实时性有要求，可以创建钉钉群，在群里配置机器人，然后将token和secret设置在下面的配置中：

```
DINGTALK_TOKEN=notset
DINGTALK_SECRET=notset
```

同样地，该方法也存在于`omicron.notify`下。[文档](https://zillionare.github.io/omicron/latest/api/omicron/#omicron.notify.mail)

### 研究界面

如果需要更改研究界面地址的前缀，请更改LAB_USER。如果要变更密码，请更改LAB_PASSWORD。
```
LAB_PASSWORD=1234
LAB_USER=zillionare
```

### 配置获取板块数据任务
Zillionare的板块数据来自同花顺，使用的是爬虫技术。这些爬虫通过单独的进程运行，它们由crontab来启动。

在我们容器打包时，未能实现给docker容器自动增加任务，因此，要获取同花顺板块数据，必须按以下步骤增加任务：

1. 通过`docer exec -it zillionare-omega /bin/bash`进行容器的命令行模式
2. 通过`crontab -e`来增加以下任务：
```
    # fetch members
    35 11 * * * /root/zillionare/cronjobs/fetch_industry_list.sh
    12 12 * * * /root/zillionare/cronjobs/fetch_concept_list.sh
    # fetch bars 
    15 18 * * * /root/zillionare/cronjobs/fetch_concept_bars.sh
    50 18 * * * /root/zillionare/cronjobs/fetch_industry_bars.sh
```

### 配置实时价格爬虫

尽管Zillionare要求使用聚宽的行情服务，但聚宽并不能提供实时行情。因此，Zillionare借助akshare来实时爬取实时价格。在Zillionare安装后，这个服务应该已经启动了。为了放心起见，请按以下步骤进行检查：

1. 进入到zillionare-omega容器中。
2. 切换到app账号，进入工作目录/home/app/zillionare/akshareprice
3. 检查python app.py是否已经运行，如果已经运行，检查logs/server.log是否正常
4. 上述步骤有任何异常，kill删掉该进程，然后执行下面的命令启动
```
    conda activate akshare
    nohup python app.py &
    #或者
    nohup /home/app/minissh conda3/envs/akshare/bin/python app.py &
```
5. 检查日志，确定程序正常启动

!!! warning
    Akshare不能提供历史的板块数据。如果需要历史板块数据，可以向我们索取。在没有数据的时候，运行以下代码会出错：
    ```python
    from omicron.models.board import Board, BoardType

    Board.init("omega")
    concepts = await Board.board_list()
    concepts[:10]

    --- raise TypeError ---
    TypeError: unhashable type: 'slice'
    ```

板块数据存放在omega容器的/data/zillionare/omega/boards.zarr目录下。如果同步任务正常运行，则会存在以下文件夹：

![Alt text](ths-board-dir.png)

## 验证安装
运行`docker-compose up`之后，正常情况下应该输出：

```
zillionare-lab | [I 2024-02-23 05:55:30.463 ServerApp] Skipped non-installed server(s):...
zillionare-backtesting | 2024-02-23 05:55:30,693 I 6 pyemit.emit:_listen:135 | listening on <aioredis.client.PubSub object at 0x7fab65abbd00>
...
zillionare-omega | waiting for influxdb start...
zillionare-omega |   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
...
zillionare-omega | 正在初始化系统数据...
zillionare-omega | 系统数据初始化完毕...
zillionare-omega | prepare to start Omega real price process for stock ...
zillionare-omega | Omega stock price process started ...
...
```
## 检查运行日志
zillionare-omega的日志在/data/zillionare/omega/logs（宿主机）目录下。如果聚宽账号配置正确，经过了至少一个交易日的午夜，则应该可以看到以下日志：
```
2024-02-23 01:15:31,082 I 209 omega.master.tasks.calibration_task:sync_daily_bars_day:179 | daily_bars_sync_1d(2024-02-22 15:00:00)同步完成,参数为{'timeout': 600, 'name': 'daily_bars_sync_1d', 'frame_type': [<FrameType.DAY: '1d'>], 'end': datetime.datetime(2024, 2, 22, 15, 0), 'n_bars': None, 'state': 'master.task.daily_bars_sync_1d.state', 'scope': ['master.task.daily_bars_sync_1d.scope.stock.1d', 'master.task.daily_bars_sync_1d.scope.index.1d']}
2024-02-23 01:15:31,084 I 209 omega.master.tasks.calibration_task:get_sync_date:63 | 所有数据已同步完毕

```
这表明数据同步服务正常工作。

## 从这里开始！

可以在研究界面下新建一个notebook，上传以下[notebook](/assets/getting-started.ipynb)，开始运行。
