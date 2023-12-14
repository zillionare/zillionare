
<style>

table {
    width: 100vw;
    background-color: transparent;
    border-collapse: collapse;
    border-spacing: 0;
    display: table !important;

    &>* {
        text-align: center;
    }

    th {
        background-color: #E7F7F5;
    }

    th,
    td {
        border: none;
    }

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

