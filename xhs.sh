cmd=$1
file=$2

if [ "$#" == 3 ]; then
    theme="/apps/slidev_themes/themes/$3"
else
    theme="/apps/slidev_themes/themes/excerpt"
fi

cd /apps/slidev_themes
if [ $cmd = "serve" ]; then
  npx slidev /apps/zillionare/$file -t $theme --remote
else
    npx slidev export --format png -t $theme --output /tmp/xhs /apps/zillionare/$file
    rm -f /apps/zillionare/xhs/*
    cp -r /tmp/xhs/* /apps/zillionare/xhs/
fi
