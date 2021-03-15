output_file := $(shell echo "`pwd`/../docs/_attachment/zillionare.sh")
archive := $(shell echo "`pwd`/docker/")
dist: 
	makeself --current --tar-quietly ${archive} ${output_file} "zillionare_${VERSION}" ./setup.sh
	cd docker \
	&& tar -zvcf ../zillionare.tar.gz . \
	&& cd - \
	&& mv -f zillionare.tar.gz ../docs/_attachment/
