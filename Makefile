clean:
	cd docker; make clean

config:
	cd docker; make config
release: 
	cd docker; make release
# for develop build, use prepare-dev.sh to copy files
# files included defaults.yaml and *.whl listed in requirements.txt (without version)

dev:
	cd docker; make dev
