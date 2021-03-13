.PHONY: clean
repo_omega_tar := https://api.github.com/repos/zillionare/omega/tarball/release
repo_omega_file := https://api.github.com/repos/zillionare/omega/contents
Headers_Accept := 'Accept: application/vnd.github.v3.raw'
Headers_Auth := 'Authorization: token $(GH_TOKEN)'

url_defaults_yaml := $(repo_omega_file)/omega/config/defaults.yaml
config_dir := rootfs/root/zillionare/omega/config

clean:
	sudo rm -rf docker-compose.yml
	sudo rm -f rootfs/root/*.whl
	sudo rm -rf init/postgres/*
	sudo rm -rf init/redis/*
	sudo rm -rf rootfs/root/zillionare/omega/config/*
	@sudo docker rm -f zillionare 2>/dev/null ||:
	@sudo docker images | grep "zillionare/zillionare" |awk '{print $1 ":" $2}' |xargs sudo docker rmi -f 2>/dev/null ||:
	@sudo rm -rf rootfs/tutorial/* 2>/dev/null ||:

config:
	# download latest config file for omega
	cd $(config_dir); curl -H $(Headers_Auth) -H $(Headers_Accept) -L $(url_defaults_yaml) -O
	# download all postgres init scripts into init/postgres/
	curl -H $(Headers_Auth)  -H $(Headers_Accept) -L $(repo_omega_tar) | tar -C init/postgres/ -xz --wildcards "*/config/sql/*" --strip-components=3
	cp -r ../docs/tutorial/* rootfs/tutorial/

release: clean config
	pip download -i https://pypi.org/simple --no-deps -r ./requirements.txt --no-cache --only-binary ":all:" -d rootfs/root/
	export VERSION=`cat ../version`; cat docker-compose.tpl | sed "s/zillionare:NOTAG/zillionare:${VERSION}/g" > docker-compose.yml
	sudo -E docker-compose up --build -d
	scp -P 31822 docker-compose.yml c.jieyu.ai:/var/www/stocks/release/docker/docker-compose-${VERSION}.yml

dev: clean
	# for develop build, use prepare-dev.sh to copy files
	# files included defaults.yaml and *.whl listed in requirements.txt (without version)
	./prepare-dev.sh
	cp -r tutorial/* rootfs/tutorial/
	export VERSION=`cat version`;cat docker-compose.tpl | sed "s/zillionare:NOTAG/zillionare:${VERSION}_DEV/g" > docker-compose.yml
	sudo -E docker-compose up --build -d
