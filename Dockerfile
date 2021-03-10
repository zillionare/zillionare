# vim:set ft=dockerfile:
FROM ubuntu:20.04 
ENV TZ=Asia/Shanghai
WORKDIR /
COPY rootfs ./
ENV __cfg4py_server_role__ PRODUCTION
RUN	ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
	&& apt-get update\
	&& apt-get install -y --no-install-recommends python3.8 python3-pip build-essential python3.8-dev vim iputils-ping \ 
	&& pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
	&& for file in `ls ./root/*.whl`; do pip3 install --no-cache-dir $file;done \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm /root/*.whl \
	&& mkdir -p /var/log/zillionare

#	&& pip3 install jupyter jupyter_contrib_nbextensions \
#   && jupyter contrib nbextension install --user \
EXPOSE 3180
EXPOSE 3181
EXPOSE 8888
ENTRYPOINT ["/root/zillionare/entrypoint.sh"]