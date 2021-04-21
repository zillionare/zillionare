#! /bin/sh
# wait for postgres, it's better to use other more reliable method
echo "containers envars are:"
printenv |grep 'POSTGRES\|JQ_ACCOUNT\|REDIS'
sleep 5
omega start fetcher
if [ -f ~/.ARCHIVED ]; then
    echo "容器并非首次启动，跳过数据导入过程"
else
    echo "正在导入最近 $INIT_BARS_MONTHS 月的历史K线数据..."

    omega download $INIT_BARS_MONTHS
    touch ~/.ARCHIVED
fi

mkdir /tutorial ||:
rm /root/tutorial.tar.gz ||:
cd /root; wget -4 -c http://www.jieyu.ai/download/tutorial.tar.gz?latest -O /tutorial.tar.gz && tar -xzf /root/tutorial.tar.gz -C /tutorial/
nohup jupyter notebook  --ip='*' --NotebookApp.token='' --NotebookApp.password='' --port 8888 --allow-root --notebook-dir='/tutorial' &
python3 -m omega.jobs start
