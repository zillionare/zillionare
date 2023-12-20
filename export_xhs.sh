cd /apps/slidev_themes
npx slidev export --format png --output /tmp/xhs /apps/zillionare/$1
rm -f /apps/zillionare/xhs/*
cp -r /tmp/xhs/* /apps/zillionare/xhs/
