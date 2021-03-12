#!/bin/bash -v

# script for prepare files needed by build dev docker images
# this script is variable according to each build

sudo docker cp dev:/apps/omega/omega/config/defaults.yaml rootfs/root/zillionare/omega/config/
#sudo docker cp dev:/apps/omega/omega/config/sql/*
# copy postgres init scripts
for f in $(sudo docker exec -it dev bash -c "ls /apps/omega/omega/config/sql/*"); do sudo docker cp dev:`echo $f | sed 's/\r//g'` init/postgres/;done
# copy omega build artifact
for f in $(sudo docker exec -it dev bash -c "ls /apps/omega/dist/*.whl"); do sudo docker cp dev:`echo $f | sed 's/\r//g'` rootfs/root;done
# copy deps
for f in $(sudo docker exec -it dev bash -c "ls /apps/omega/tests/packages/*.whl"); do sudo docker cp dev:`echo $f | sed 's/\r//g'` rootfs/root;done

# use latest jq-adaptors, Be aware that sometimes we should use local jq-adaptor build
pip download --no-deps zillionare-omega-adaptors-jq==0.3.5 --no-cache --only-binary ":all:" -d rootfs/root/