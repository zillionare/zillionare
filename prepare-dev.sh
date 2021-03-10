# script for prepare files needed by build dev docker images
# this script is variable according to each build

sudo docker cp dev:/apps/omega/omega/config/defaults.yaml rootfs/root/zillionare/omega/config/
sudo docker cp dev:/apps/omega/omega/config/sql/init.sql init.sql
for f in $(sudo docker exec -it dev bash -c "ls /apps/omega/dist/*.whl"); do sudo docker cp dev:`echo $f | sed 's/\r//g'` rootfs/root;done
for f in $(sudo docker exec -it dev bash -c "ls /apps/omega/tests/packages/*.whl"); do sudo docker cp dev:`echo $f | sed 's/\r//g'` rootfs/root;done
pip download --no-deps zillionare-omega-adaptors-jq==0.3.5 --no-cache --only-binary ":all:" -d rootfs/root/