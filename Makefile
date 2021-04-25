
# use safe-rm to avoid delete important files accidentaly
rm := safe-rm
pypi := https://pypi.org/simple
dev_build_pypi := https://pypi.org/simple

init_bars_month := 1

server_role := DEV
update_config:=1
export VERSION:=$(shell cat version)
image_name:=zillionare:${VERSION}

requirements := setup/requirements.txt

req_jq_adaptor := ${shell cat setup/requirements.txt |grep 'adaptors-jq' |tr -d '\n'}
req_omega := ${shell cat setup/requirements.txt |grep -e 'omega==' -e 'omega$$' |tr -d '\n'}
req_omicron := ${shell cat setup/requirements.txt |grep -e 'omicron==' -e 'omicron$$' |tr -d '\n'}

dev_repo_omega_tar := https://api.github.com/repos/zillionare/omega/tarball/master
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

tools:
	sudo apt-get update
	sudo apt-get install -y safe-rm
	sudo apt-get install -y makeself

clean: tools
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

	sudo rm -rf /tmp/zillionare_*
	sudo rm -rf ${install_to}
	
config_release:
	# get the tar ball from gh://zillionare/omega/release
	curl -H $(Headers_Auth) -H $(Headers_Accept) -L $(repo_omega_tar) -o /tmp/omega.src.${VERSION}.tar.gz
	# omega config
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${omega_config_dir} --wildcards "*/config/defaults.yaml" --strip-components=3
	# postgres init scripts
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${postgres_init_dir} --wildcards "*/config/sql/*" --strip-components=4
	# artifacts/deps
	pip download -i https://pypi.org/simple --no-deps -r ${requirements} --no-cache --only-binary ":all:" -d ${image_root}

	$(eval server_role=PRODUCTION)
	$(eval pypi=https://mirrors.aliyun.com/pypi/simple)
	$(eval init_bars_month=13)

config_dev:
	# omega config
	curl -H $(Headers_Auth) -H $(Headers_Accept) -L $(dev_repo_omega_tar) -o /tmp/omega.src.${VERSION}.tar.gz
	# omega config
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${omega_config_dir} --wildcards "*/config/defaults.yaml" --strip-components=3
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${omega_config_dir} --wildcards "*/config/dev.yaml" --strip-components=3
	sudo chmod -R 777 ${omega_config_dir}

	# postgres init scripts
	tar -xzf /tmp/omega.src.${VERSION}.tar.gz -C ${postgres_init_dir} --wildcards "*/config/sql/*.sql" --strip-components=4

	pip download --no-deps ${req_jq_adaptor} --no-cache --only-binary ":all:" -d ${image_root}

	# download omega/omicron
	pip download -i ${dev_build_pypi} --no-deps ${req_omega} --no-cache --only-binary ":all:" -d ${image_root}
	pip download -i ${dev_build_pypi} --no-deps ${req_omicron} --no-cache --only-binary ":all:" -d ${image_root}

	ls -l ${image_root}

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
test: export PYPI_INDEX_URL := ${pypi} 
test: export __cfg4py_server_role__ := ${server_role}
test: export INIT_BARS_MONTHS := ${init_bars_month}

test: dev
	export tmp_artifact=/tmp/zillionare_${VERSION}.sh
	export tmp_installation_dir=/tmp/zillionare_${VERSION}

	makeself --current --tar-quietly ${archive_src} ${tmp_artifact} "zillionare_${VERSION}" ./setup.sh
	chmod +x ${tmp_artifact}
	sudo -E ${tmp_artifact} --target ${tmp_installation_dir} -- --jq_account ${JQ_ACCOUNT} --jq_password ${JQ_PASSWORD} --redis_host redis --postgres_host postgres
	sudo docker logs zillionare

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
