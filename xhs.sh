cmd=$1
file=$2

if [ "$#" == 3 ]; then
    theme="/Users/aaronyang/slidev/themes/$3"
else
    theme="/Users/aaronyang/slidev/themes/excerpt"
fi

cd /Users/aaronyang/slidev/
echo "进入目录：`pwd`"
if [ $cmd = "serve" ]; then
  npx slidev /Users/aaronyang/workspace/zillionare/$file -t $theme --remote
else
    npx slidev export --format png -t $theme --output /tmp/xhs /Users/aaronyang/workspace/zillionare/$file
    rm -f ~/workspace/zillionare/xhs/*
    cp -r /tmp/xhs/* ~/workspace/zillionare/xhs/
fi
