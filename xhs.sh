cmd=$1
file=$2

cd /apps/slidev_themes
if [ $cmd = "serve" ]; then
  npx slidev /apps/zillionare/$file -t /apps/slidev_themes/theme-excerpt --remote
else
    npx slidev export --format png -t /apps/slidev_themes/theme-excerpt --output /tmp/xhs /apps/zillionare/$file
    rm -f /apps/zillionare/xhs/*
    cp -r /tmp/xhs/* /apps/zillionare/xhs/
fi
