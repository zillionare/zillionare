#! /bin/sh
omega start
echo "正在导入最近 $INIT_BARS_MONTHS 月的历史K线数据..."
omega download $INIT_BARS_MONTHS
python3 -m omega.jobs.main start