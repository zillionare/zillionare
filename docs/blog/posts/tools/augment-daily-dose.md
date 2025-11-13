---
title: Augment随手记
date: 2025-05-17
category: tools
slug: augment-daily-dose-1
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/banner/IMG_20250510_112543.jpg
tags:
  - AI
  - Augment
  - duckdb
---

Duckdb是一个年轻而迷人的数据库。它的备份可以简单到通过拷贝文件来完成 -- 但前提是，没有其它进程独占她。如果你的服务使用了duckdb，而且还在不停地读写她，你该怎么给她一个备份呢？

我们把这个问题抛给了Augment.


To Augment:

> 增加一个后台任务，每周备份一次数据库。

> 注意我们项目中，已经有过备份的逻辑（cli.py）但是，它是基于服务停止后，拷贝文件来实现的。如果我们通过后台任务来实现，在不停止服务的情况下，能否通过拷贝文件来实现备份呢？

> 另外要注意我们已经使用了apscheduler，你应该继续使用它。

这是 Augment的分析：

> 我理解您的需求。您希望增加一个每周自动备份数据库的后台任务，并且希望在不停止服务的情况下进行备份。让我们先查看现有的备份逻辑和 apscheduler 的使用情况，然后设计一个解决方案。

紧接着， Augment 调用一些命令行工具，查看了cli.py，scheduler.py, app.py，这样就对当前系统的状态了然于胸了。接下来，它开始寻找技术方案：

> DuckDB 是一个嵌入式数据库，类似于 SQLite。在不停止服务的情况下备份 DuckDB 数据库，我们有几种可能的方法：
    使用 DuckDB 的 EXPORT DATABASE 命令
    使用 DuckDB 的 COPY 命令
    使用文件系统级别的备份工具
    让我们查看 DuckDB 是否支持在线备份：

它查看duckdb文档的方式是通过这个命令：

```python
python -c "import duckdb; print(dir(duckdb))"
```

然后从一堆杂乱的输出中，找到了checkpoint方法，然后给出了实现方案：

> 基于以上信息，我们可以设计一个在不停止服务的情况下备份数据库的解决方案。DuckDB 支持 checkpoint 操作，这可以确保所有的更改都被写入磁盘。然后我们可以使用文件系统级别的备份来复制数据库文件。
> 以下是我的解决方案：
> 创建一个新的备份任务函数
> 将该任务添加到现有的 apscheduler 调度器中
> 设置每周执行一次
> 在备份过程中使用 DuckDB 的 checkpoint 功能确保数据一致性

最终的实现是：

```python
def backup_database() -> None:
    """备份数据库

    在不停止服务的情况下备份数据库文件，使用DuckDB的checkpoint功能确保数据一致性
    """
    try:
        # 获取当前时间作为备份目录名
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

        # 设置备份目录
        ...

        # 确保所有更改都写入磁盘
        conn = duckdb.connect(str(db_path), read_only=False)
        conn.execute("CHECKPOINT")
        conn.close()

        # 备份数据库文件
        backup_db_path = backup_dir / "provision.db"
        shutil.copy2(db_path, backup_db_path)

        # 保留最近的10个备份，删除旧的备份
        all_backups = sorted(backup_base.glob("*"), key=os.path.getmtime)
        if len(all_backups) > 10:
            for old_backup in all_backups[:-10]:
                if old_backup.is_dir():
                    shutil.rmtree(old_backup)
                    logger.info(f"Removed old backup: {old_backup}")

        logger.info(f"Database backup completed successfully: {backup_dir}")
    except Exception as e:
        logger.error(f"Failed to backup database: {e}")
```

Augment最后发挥了一下，只保留了最后10个备份。这相当于2个月前的备份会被删除。我并没有要求它这么做，但是，Augment的这份主动性很贴心。
