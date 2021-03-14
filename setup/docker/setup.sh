#!/bin/bash

POSITIONAL=()

function help() {
    version=`cat version`
    echo "      大富翁安装脚本"
    echo "==========================="
    echo "    version $version    "
    cat << EOF

    Args:
        --jq_account: 聚宽账号，必选
        --jq_password: 聚宽账号密码，必选
        --postgres_user: postgres数据库用户名，默认为zillionare
        --postgres_password: postgres数据库密码，默认为123456
        --postgres_db: postgres数据库名，默认为zillionare
        --postgres_host: postgres数据库服务器，默认为postgres
        --postgres_port: postgres数据库服务器监听端口，默认为5432
        --redis_host: redis服务器名，默认为redis
        --redis_port: redis服务器监听端口，默认为6379
        --init_bars_months: 初始化导入的K线数据月数，默认13个月

    示例：
        ./zillionare.sh --jq_account=18688888888 --jq_password=my_secret
EOF
}


while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help)
            help
            shift
            ;;
        --jq_account)
            jq_account="$2"
            shift
            shift
            ;;
        --jq_password)
            jq_password="$2"
            shift
            shift
            ;;
        --init_bars_months) 
            init_bars_months="$2"
            shift
            shift
            ;;
        --postgres_host) 
            postgres_host="$2"
            shift
            shift
            ;;
        --postgres_port) 
            postgres_port="$2"
            shift
            shift
            ;;
        --postgres_db)
            postgres_host="$2"
            shift
            shift
            ;;
        --postgres_user)
            postgres_user="$2"
            shift
            shift
            ;;
        --postgres_password)
            postgres_password="$2"
            shift
            shift
            ;;
        --redis_host)
            redis_host="$2"
            shift
            shift
            ;;
        --redis_port)
            redis_port="$2"
            shift
            shift
            ;;
    esac
done

cat << EOF > .env
INIT_BARS_MONTHS=$init_bars_months
JQ_ACCOUNT=$jq_account
JQ_PASSWORD=$jq_password
POSTGRES_USER=$postgres_user
POSTGRES_PASSWORD=$postgres_password
POSTGRES_DB=$postgres_db
POSTGRES_HOST=$postgres_host
POSTGRES_PORT=$postgres_port
REDIS_HOST=$redis_host
REDIS_PORT=$redis_port
EOF
sudo -E docker-compose up --build -d