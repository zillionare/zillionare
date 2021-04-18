
# use safe-rm to avoid delete important files accidentaly
rm := safe-rm

update_config:=1
export VERSION:=$(shell cat version)
image_name:=zillionare:${VERSION}

requirements := setup/requirements.txt
repo_omega_tar := https://api.github.com/repos/zillionare/omega/tarball/release
Headers_Accept := 'Accept: application/vnd.github.v3.raw'
Headers_Auth := 'Authorization: token ${GH_TOKEN}'

image_root := setup/docker/rootfs/

omega_config_dir := ${image_root}/root/zillionare/omega/config
postgres_init_dir := ${image_root}/../init/postgres

tutorial_src := ${shell pwd}/docs/zillionare/tutorial/
tutorial_dst := ${shell pwd}/docs/download/tutorial.tar.gz

# build artifacts
artifact_exe := docs/download/zillionare.sh
artifact_tar := $(shell pwd)/docs/download/zillionare.tar.gz

# from where to build artifact_tar?
archive_src := ${image_root}/..

# installation dir for dist test
install_to := /usr/local/zillionare

clean:
	sudo apt update
	sudo apt install safe-rm
	# clean image rootfs
	if [ -n "${image_root}" ]; then sudo ${rm} -f ${image_root}/*.whl ||: ; fi

	if [ -n "${postgres_init_dir}" ]; then sudo ${rm} -rf ${postgres_init_dir}/*; fi
	if [ -n "${omega_config_dir}" ]; then sudo ${rm} -rf ${omega_config_dir}/*; fi

	mkdir -p ${image_root}/root/zillionare/omega/config
	mkdir -p ${postgres_init_dir}

	# remove docker related
	# remove containers created if exists
	sudo zillionare down 2 > /dev/null ||:
	sudo docker rm -f zillionare 2 > /dev/null ||:
	sudo docker rmi ${image_name} 2>/dev/null ||:
	sudo docker image prune -f --filter dangling=true 2>/dev/null||:
	
config_release:
	# get the tar ball from gh://zillionare/omega/release
	curl -H $(Headers_Auth) -H $(Headers_Accept) -L $(repo_omega_tar) -o /tmp/omega.src.${VERSION}.tar.gz
	# omega config
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${omega_config_dir} --wildcards "*/config/defaults.yaml" --strip-components=3
	# postgres init scripts
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${postgres_init_dir} --wildcards "*/config/sql/*" --strip-components=4
	# artifacts/deps
	pip download -i https://pypi.org/simple --no-deps -r ${requirements} --no-cache --only-binary ":all:" -d ${image_root}

config_dev:
	# omega config
	sudo docker cp dev:/apps/omega/omega/config/defaults.yaml ${omega_config_dir}
	sudo chmod -R 777 ${omega_config_dir}
	# postgres init scripts
	for f in $(shell sudo docker exec -it dev bash -c "ls /apps/omega/omega/config/sql/*"); do sudo docker cp dev:$$f ${postgres_init_dir};done
	# omega build artifact
	for f in $(shell sudo docker exec -it dev bash -c "ls /apps/omega/dist/*.whl"); do sudo docker cp dev:$$f ${image_root};done
	# copy deps
	for f in $(shell sudo docker exec -it dev bash -c "ls /apps/omega/tests/packages/*.whl"); do sudo docker cp dev:$$f ${image_root};done

	# use latest jq-adaptors, Be aware that sometimes we should use local jq-adaptor build
	pip download -i https://pypi.org/simple --no-deps zillionare-omega-adaptors-jq==1.0.2 --no-cache --only-binary ":all:" -d ${image_root}

ifeq (${update_config}, 1)
release: clean config_release build
dev: clean config_dev build
else
release: build
dev: build
endif

build:
	echo ${VERSION} > ${image_root}/../version
	cd ${image_root}/..; sudo -E docker-compose build --force-rm
	sudo docker rmi ${image_name}

# set local variables for test target
test: tmp_artifact=/tmp/zillionare_${VERSION}.sh
test: tmp_installation_dir=/tmp/zillionare

test: dev
	export tmp_artifact=/tmp/zillionare_${VERSION}.sh
	export tmp_installation_dir=/tmp/zillionare_${VERSION}

	makeself --current --tar-quietly ${archive_src} ${tmp_artifact} "zillionare_${VERSION}" ./setup.sh
	chmod +x ${tmp_artifact}
	sudo -E ${tmp_artifact} --target ${tmp_installation_dir} -- --jq_account ${JQ_ACCOUNT} --jq_password ${JQ_PASSWORD} --redis_host redis --postgres_host postgres
	sudo zillionare log

dist: release
	makeself --current --tar-quietly ${archive_src} ${artifact_exe} "zillionare_${VERSION}" ./setup.sh
	cd setup/docker \
	&& tar -zvcf ${artifact_tar} . \
	&& cd -
	chmod +x ${artifact_exe}
	sudo -E ${artifact_exe} --target ${install_to} -- --jq_account ${JQ_ACCOUNT} --jq_password ${JQ_PASSWORD} --redis_host redis --postgres_host postgres
	cd ${tutorial_src} \
	&& tar -zvcf ${tutorial_dst} ./* \
	&& cd -

publish:
	echo "Make sure your run make dist and check result first"
	mkdocs gh-deploy
