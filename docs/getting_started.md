
安装时需要指定环境变量
必选：
JQ_ACCOUNT
JQ_PASSWORD

可选:
      - INIT_BARS_MONTHS=13
      - JQ_ACCOUNT
      - JQ_PASSWORD
      - LANG=C.UTF-8
      - POSTGRES_USER=zillionare
      - POSTGRES_PASSWORD=123456
      - POSTGRES_DB=zillionare
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379

安装时需要带--keep选项。因为docker-compose需要这个compose文件

```
./zillionare.sh --target ./zillionare --keep -- --jq_account aaron --jq_password 123
```
这样程序将安装到./zillionare目录下。