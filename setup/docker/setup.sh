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
        sudo ./setup.sh --jq_account 18688888888 --jq_password my_secret
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
            echo "JQ_ACCOUNT=$2" >> .env
            # TO AVOID enviroment variable conflict by chance
            export JQ_ACCOUNT=$2
            shift
            shift
            ;;
        --jq_password)
            echo "JQ_PASSWORD=$2" >> .env
            export JQ_PASSWORD=$2
            shift
            shift
            ;;
        --init_bars_months) 
            echo "INIT_BARS_MONTHS=$2" >> .env
            export INIT_BARS_MONTHS=$2
            shift
            shift
            ;;
        --postgres_host) 
            echo "POSTGRES_HOST=$2" >> .env
            export POSTGRES_HOST=$2
            shift
            shift
            ;;
        --postgres_port) 
            echo "POSTGRES_PORT=$2" >> .env
            export POSTGRES_PORT=$2
            shift
            shift
            ;;
        --postgres_db)
            echo "POSTGRES_DB=$2" >> .env
            export POSTGRES_DB=$2
            shift
            shift
            ;;
        --postgres_user)
            echo "POSTGRES_USER=$2" >> .env
            export POSTGRES_USER=$2
            shift
            shift
            ;;
        --postgres_password)
            echo "POSTGRES_PASSWORD=$2" >> .env
            export POSTGRES_PASSWORD=$2
            shift
            shift
            ;;
        --redis_host)
            echo "REDIS_HOST=$2" >> .env
            export REDIS_HOST=$2
            shift
            shift
            ;;
        --redis_port)
            echo "REDIS_PORT=$2" >> .env
            export REDIS_PORT=$2
            shift
            shift
            ;;
    esac
done

# 将INSTALLATION_DIR替换为当前工作路径
sed -i "s|INSTALLATION_DIR|${PWD}|g" zillionare
cp $PWD/zillionare /usr/local/bin/zillionare
docker-compose up --build -d