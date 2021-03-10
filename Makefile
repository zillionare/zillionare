.DEFAULT_GOAL := all
.PHONY: clean

version:
	export VERSION=`cat version`
clean:
	rm -f rootfs/root/*.whl
	rm -f rootfs/root/zillionare/omega/config/defaults.yaml
	rm -f init.sql
	-sudo docker rm -f zillionare
	-sudo docker rmi -f zillionare/zillionare
	-sudo docker rmi -f $(sudo docker images -f "dangling=true" -q)

release: clean version
	pip download --no-deps -r ./requirements.txt --no-cache --only-binary ":all:" -d rootfs/root/
	wget https://raw.githubusercontent.com/zillionare/omega/release/omega/config/defaults.yaml -O rootfs/root/zillionare/omega/config/defaults.yaml
	sudo -E docker-compose up --build -d

# for develop build. You need copy files by your self.
# files included defaults.yaml and *.whl listed in requirements.txt (without version)
dev: clean version
	./prepare-dev.sh
	sudo -E docker-compose up --build -d
