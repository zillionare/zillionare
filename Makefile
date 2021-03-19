update_config:=1
clean:
	@rm docs/assets/zillionare.sh 2>/dev/null ||:
	@rm docs/assets/zillionare.tar.gz 2>/dev/null ||:
	cd setup/docker; make clean

config:
	cp version setup/docker/
	cd setup/docker; make config

ifeq (${update_config}, 1)
release: clean config
endif

release:
	export VERSION=`cat version`;cd setup/docker; make release

# for develop build, use prepare-dev.sh to copy files
# files included defaults.yaml and *.whl listed in requirements.txt (without version)
dev: clean config
	cp -r tutorial setup/docker/rootfs/
	cd setup/docker; make dev

dist: release
	# build installation script and publish it to www.jieyu.ai
	# currently `publish` just put it into docs/assets folder, then refer it in a
	# md file manually
	export VERSION=`cat version`;cd setup; make dist
	chmod +x docs/assets/zillionare.sh