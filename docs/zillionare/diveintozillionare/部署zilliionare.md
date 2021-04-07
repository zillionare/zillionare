# 如何使用zillionare docker images
    ## 安装docker/docker-compose
    ## 安装makeself
    ## 启动zillionare
    ## 检查zillionare是否正常工作
        ### 查看log
        ### 通过notebook来访问
        ### 修改同步配置？
    ## 高级功能
        ### 使用自定义的文件夹来存放数据
    安装数据库
    sudo su postgres
    psql
    create user zillionare with password '123456';
    create database zillionare owner zillionare;
    grant all privileges on database zillionare to zillionare;

    vi /etc/postgresql/12/main/postgresql.conf, listen=改为listen='*'
    vi /etc/postgresql/12/main/pg_hba.conf，将host all all 127.0.0.1/32 md5改为
    host all all 0.0.0.0/0 md5
    安装dbeaver

    ![](http://images.jieyu.ai/images/202103/20210331105246.png)