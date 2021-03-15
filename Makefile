clean:
	@rm docs/_attachment/zillionare.sh 2>/dev/null ||:
	@rm docs/_attachment/zillionare.tar.gz 2>/dev/null ||:
	cd setup/docker; make clean

config:
	cp version setup/docker/
	cd setup/docker; make config
release: clean config
	export VERSION=`cat version`;cd setup/docker; make release
# for develop build, use prepare-dev.sh to copy files
# files included defaults.yaml and *.whl listed in requirements.txt (without version)
dev: clean config
	cd setup/docker; make dev
dist: release
	# build installation script and publish it to www.jieyu.ai
	# currently `publish` just put it into docs/_attachment folder, then refer it in a
	# md file manually
	export VERSION=`cat version`;cd setup; make dist
	chmod +x docs/_attachment/zillionare.sh