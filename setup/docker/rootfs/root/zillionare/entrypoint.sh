#! /bin/sh
# wait for postgres, it's better to use other more reliable method
echo "containers envars are:"
printenv |grep -v 'PASSWORD'
sleep 5
omega start fetcher
sleep 5
if [ -f ~/.ARCHIVED ]; then
    echo "容器并非首次启动，跳过数据导入过程"
else
    echo "正在导入最近 $INIT_BARS_MONTHS 月的历史K线数据..."

    omega download $INIT_BARS_MONTHS
    touch ~/.ARCHIVED
fi

mkdir /tutorial ||:
wget -4 -N http://www.jieyu.ai/download/tutorial.tar.gz?latest -O /root/tutorial.tar.gz && tar -xzf /root/tutorial.tar.gz -C /tutorial/
nohup jupyter notebook  --ip='*' --NotebookApp.token='' --NotebookApp.password='' --port 8888 --allow-root --notebook-dir='/tutorial' &
python3 -m omega.jobs start
