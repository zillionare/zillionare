---
title: "Zillionare 2.0 Docker Setup: Deploying a Quant Research Environment"
date: "2026-10-09"
slug: en/articles/products/zillionare_installation
tags: [Docker, Quant Research, Live Trading, Data Sync]
excerpt: "A step-by-step guide to deploying Zillionare 2.0 via Docker, covering container orchestration, data synchronization, and live trading integration."
lang: en
translation_of: articles/products/zillionare_installation
auto_translated: true
source_sha: 08124371d0f9dd862fe93dcc2bc9c8bf236fec2d
---

<style>

table {
    background-color: transparent;
    border-collapse: collapse;
    border-spacing: 0;

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

<h1>Zillionare 2.0 Installation Guide</h1>
!!! tip
    The installation package is currently available exclusively to Zillionare Quant Course students and key clients. To request access, please contact quantfans_99 (VIP) on WeChat.

We provide Zillionare 2.0 via a Docker cluster. This cluster comprises the following containers:

| NAMES                  | IMAGE                     | PORTS                                      |
| ---------------------- | ------------------------- | ------------------------------------------ |
| zillionare-omega       | zillionare/omega:2.0.1    | 0.0.0.0:3180->3180/tcp :::3180->3180/tcp   |
| zillionare-influxdb    | influxdb:2.4.0            | 0.0.0.0:58086->8086/tcp :::58086->8086/tcp |
| zillionare-backtesting | zillionare/backtest:0.5.1 | 0.0.0.0:7080->7080/tcp :::7080->7080/tcp   |
| zillionare-redis       | redis:7.0.4-alpine        | 0.0.0.0:56379->6379/tcp :::56379->6379/tcp |
| zillionare-lab         | zillionare/lab            | 0.0.0.0:8888->8888/tcp :::8888->8888/tcp   |


This system constitutes a complete research environment, pre-loaded with two years of daily and 30-minute data (approximately 1.3 GB). Once started, you can access the research environment via port 8888. For instance, if the machine hosting the cluster has the IP address 192.168.100.100, you can access it at http://192.168.100.100:8888/zillionare:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/lab.png)

!!! Info
    The default login password is `1234`. To change it, modify the `LAB_PASSWORD` option in the `.omega_env` file located in your Docker Compose installation directory.

For live trading, install the East Money (Dongfang Caifu) quantitative trading client and the `gm-adaptor` library. Please refer to [Live Trading](#live-trading) for details.

## Installation Steps
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

!!! Info
    Zillionare 2.0 is built on Docker container technology and can theoretically run on any operating system that supports containerization. However, we have only tested it on Ubuntu Focal and Ubuntu Focal on WSL 2.0 (Windows).
    If you plan to use it for production, we recommend the following hardware specifications:

    1. CPU: 8 cores or more
    2. Memory: 32 GB or more (our courseware environment uses a cluster; a single machine has 96 GB)
    3. Storage: 1 TB or more (it consumes significant disk space)

1. Install Docker and Docker Compose. If you are using Windows, we recommend installing WSL 2 first, then installing Docker/Docker Compose within the Ubuntu environment on WSL 2.
   
2. Extract `zillionare.tar` to your desired installation directory. Modify the `.omega.env` file within it. You must provide your JQData account credentials; other settings can remain unchanged.
   
3. Start the cluster using `docker-compose up -d`. During startup, data will be downloaded and imported. Depending on your network speed, this should complete within 10 minutes.

To stop the services later, run `docker-compose stop`; to restart, run `docker-compose start`. Both commands must be executed in the installation directory.

## Data Loading
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

The data included in this environment is limited to market research. If you need to use the **backtesting service**, you must supplement it with minute-level data.

Zillionare officially supports integration with JQData (JuQuan) data services. You need to purchase JQData's data service. Your daily quota must be at least 5 million records to ensure normal data synchronization and to gradually catch up on missing data (down to the minute level).

!!! Info
    Currently, there are nearly 6,000 stocks in China A-shares, generating nearly 1.4 million minute-level data points per day. Zillionare will request minute-level data for all stocks and common indices in real-time during trading hours. Additionally, around 2:00 AM each night, it will request minute-level, daily, and other data for the previous trading day. For error correction purposes, it will make two requests and perform data validation. Therefore, it will consume over 5 million quota records daily. However, to catch up on historical minute-level data, we recommend purchasing a quota level of 200 million records. This allows you to catch up approximately one month of market data per day.

## Live Trading
<div style="width:100%;border-top:1px solid rgba(0,0,0,.1)"/>

This environment supports live trading. You can write strategies in Lab and execute orders via `zillionare-trader-client`. Currently, Zillionare only provides the East Money (Dongfang Caifu) quantitative interface. The installation method is as follows:

1. Apply to East Money to enable the quantitative interface.
2. Install and configure the East Money EMC client on a Windows machine.
3. Install `gmadaptor` on the same Windows machine.
4. When placing orders via `trader-client`, point the URL to the Windows machine.

For installation and configuration details, please see the [East Money Live Trading Deployment Guide](docs/products/gm-adapter-installation.md).

## Configuration

### JQData Account

```
JQ_ACCOUNT=notset
JQ_PASSWORD=passwd
```

### Email Notifications
After configuring email notifications, some built-in system alerts will be sent via email. You can configure an email list so that operations personnel can receive notifications. After configuration, you can also use the `omicron.notify` method in your strategies to send email notifications. [Documentation](https://zillionare.github.io/omicron/latest/api/omicron/#omicron.notify.mail)

```
MAIL_FROM=user@example.com
MAIL_TO=user@example.com
MAIL_PASSWORD=passwd
MAIL_SERVER=127.0.0.1
```
### DingTalk Notifications

Email notifications are not real-time. If you require real-time alerts, you can create a DingTalk group, configure a bot in the group, and then set the token and secret in the configuration below:

```
DINGTALK_TOKEN=notset
DINGTALK_SECRET=notset
```

Similarly, this method is available under `omicron.notify`. [Documentation](https://zillionare.github.io/omicron/latest/api/omicron/#omicron.notify.mail)

### Research Interface

If you need to change the prefix of the research interface address, modify `LAB_USER`. To change the password, modify `LAB_PASSWORD`.
```
LAB_PASSWORD=1234
LAB_USER=zillionare
```

### Configuring Sector Data Tasks
Zillionare's sector data is sourced from Tonghuashun (10jqka) using web scraping techniques. These scrapers run as separate processes and are triggered by crontab.

We were unable to automatically add tasks to Docker containers during packaging. Therefore, to obtain Tonghuashun sector data, you must add tasks following these steps:

1. Enter the container's command-line mode via `docker exec -it zillionare-omega /bin/bash`.
2. Add the following task via `crontab -e`:
```
    # fetch members
    35 11 * * * /root/zillionare/cronjobs/fetch_industry_list.sh
    12 12 * * * /root/zillionare/cronjobs/fetch_concept_list.sh
    # fetch bars 
    15 18 * * * /root/zillionare/cronjobs/fetch_concept_bars.sh
    50 18 * * * /root/zillionare/cronjobs/fetch_industry_bars.sh
```

### Configuring Real-Time Price Scrapers

Although Zillionare requires JQData's market data service, JQData does not provide real-time quotes. Therefore, Zillionare uses `akshare` to scrape real-time prices. After installing Zillionare, this service should already be running. To ensure everything is working correctly, please check as follows:

1. Enter the `zillionare-omega` container.
2. Switch to the `app` user and navigate to the working directory `/home/app/zillionare/akshareprice`.
3. Check if `python app.py` is running. If it is, verify that `logs/server.log` is normal.
4. If there are any anomalies in the above steps, kill the process and start it using the following command:
```
    conda activate akshare
    nohup python app.py &
    #或者
    nohup /home/app/minissh conda3/envs/akshare/bin/python app.py &
```
5. Check the logs to confirm the program has started normally.

!!! warning
    Akshare does not provide historical sector data. If you need historical sector data, please request it from us. Running the following code without data will result in an error:
    ```python
    from omicron.models.board import Board, BoardType

    Board.init("omega")
    concepts = await Board.board_list()
    concepts[:10]

    --- raise TypeError ---
    TypeError: unhashable type: 'slice'
    ```

Sector data is stored in the `/data/zillionare/omega/boards.zarr` directory within the omega container. If the synchronization task runs normally, the following folders should exist:

![Alt text](ths-board-dir.png)

## Verifying Installation
After running `docker-compose up`, you should normally see the following output:

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
## Checking Runtime Logs
The logs for `zillionare-omega` are located in the `/data/zillionare/omega/logs` directory (on the host machine). If your JQData account is configured correctly and at least one trading day's midnight has passed, you should see the following logs:
```
2024-02-23 01:15:31,082 I 209 omega.master.tasks.calibration_task:sync_daily_bars_day:179 | daily_bars_sync_1d(2024-02-22 15:00:00)同步完成,参数为{'timeout': 600, 'name': 'daily_bars_sync_1d', 'frame_type': [<FrameType.DAY: '1d'>], 'end': datetime.datetime(2024, 2, 22, 15, 0), 'n_bars': None, 'state': 'master.task.daily_bars_sync_1d.state', 'scope': ['master.task.daily_bars_sync_1d.scope.stock.1d', 'master.task.daily_bars_sync_1d.scope.index.1d']}
2024-02-23 01:15:31,084 I 209 omega.master.tasks.calibration_task:get_sync_date:63 | 所有数据已同步完毕

```
This indicates that the data synchronization service is working correctly.

## Getting Started!

You can create a new notebook in the research interface and upload the following [notebook](/assets/getting-started.ipynb) to begin running.
