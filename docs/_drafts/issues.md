1. 如果jq_account quota不足，初次启动也会失败。
    原因： 初次启动时，缓存为空。此时需要从jq加载证券列表。因为quota不足，所以加载失败。此时继续运行也没有意义。由于证券列表需要每日更新，所以jieyu不提供这个服务。
2. 需要加一行日志，即jq使用的是哪一个账号登录的。对容器来说，容易在变量传递中失败。
3. zillionare error: AttributeError: module 'sqlalchemy.sql.schema' has no attribute '_schema_getter'. It caused by SQLAlchemy's version changed to 1.4.1. It should be 1.3.23
4. 如果机器有较多内核，而postgresql配置的max_connections不足，则在omega download时可能失败。pg_conftool来查看
   ```
   pg_conftool show max_connections
   ```
    在32核机器上，100是不够的。
5. omega download在某些网络环境下超时严重
   禁止ipv6以后，速度达到了1.35MB/s。
   ```
   sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
   sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
   ```

6. 对K线应该设置过期缓存
