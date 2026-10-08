---
title: "Hot-Backup DuckDB with Augment: Zero-Downtime Backups"
date: 2025-05-17
slug: en/posts/tools/augment-daily-dose
tags: [Duckdb, Hot Backup, Database Administration, Automation]
excerpt: "Learn how to hot-backup DuckDB without stopping services using checkpointing and file copying. This case study demonstrates safe, automated backups for live applications."
lang: en
translation_of: posts/tools/augment-daily-dose
auto_translated: true
source_sha: 724184ca5d956bc07a8260220e4014b20b07b71d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gallery/banner/IMG_20250510_112543.jpg"
---

DuckDB is a young and charming database. Its backups can be as simple as copying a file—but only if no other process holds an exclusive lock. If your service uses DuckDB and is actively reading and writing to it, how do you back it up?

We posed this question to Augment.

To Augment:

> Add a background task to back up the database once a week.

> Note that our project already has backup logic (`cli.py`), but it relies on copying the file after the service stops. Can we implement backups via a background task by copying the file without stopping the service?

> Also, note that we are already using `apscheduler`; you should continue using it.

Here is Augment’s analysis:

> I understand your requirement. You want to add a weekly automatic database backup background task, and you wish to perform the backup without stopping the service. Let’s first review the existing backup logic and the usage of `apscheduler`, then design a solution.

Immediately, Augment invoked some command-line tools to inspect `cli.py`, `scheduler.py`, and `app.py`, gaining a comprehensive understanding of the current system state. Next, it began searching for a technical solution:

> DuckDB is an embedded database, similar to SQLite. To back up a DuckDB database without stopping the service, we have several possible approaches:
>     Use DuckDB’s `EXPORT DATABASE` command
>     Use DuckDB’s `COPY` command
>     Use file-system-level backup tools
>     Let’s check if DuckDB supports online backups:

It reviewed the DuckDB documentation using this command:

```python
python -c "import duckdb; print(dir(duckdb))"
```

Then, from a cluttered output, it identified the `checkpoint` method and proposed an implementation:

> Based on the above information, we can design a solution to back up the database without stopping the service. DuckDB supports the `checkpoint` operation, which ensures all changes are written to disk. We can then use file-system-level backup to copy the database file.
> Here is my solution:
> Create a new backup task function
> Add this task to the existing `apscheduler` scheduler
> Set it to execute once a week
> Use DuckDB’s `checkpoint` feature during the backup process to ensure data consistency

The final implementation is:

```python
def backup_database() -> None:
    """Backup database

    Back up the database file without stopping the service, using DuckDB's checkpoint feature to ensure data consistency
    """
    try:
        # Get current time as the backup directory name
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

        # Set backup directory
        ...

        # Ensure all changes are written to disk
        conn = duckdb.connect(str(db_path), read_only=False)
        conn.execute("CHECKPOINT")
        conn.close()

        # Backup database file
        backup_db_path = backup_dir / "provision.db"
        shutil.copy2(db_path, backup_db_path)

        # Keep the most recent 10 backups, delete old ones
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

In its final touch, Augment retained only the last 10 backups. This means backups older than two months would be deleted. I did not ask it to do this, but Augment’s proactive initiative was thoughtful.
