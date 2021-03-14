output_file := $(shell echo "`pwd`/../docs/_attachment/zillionare.sh")
archive := $(shell echo "`pwd`/docker/")
dist:
	makeself --current --tar-quietly ${archive} ${output_file} "zillionare_${VERSION}" ./setup.sh