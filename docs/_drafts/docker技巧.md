
1. 如何进入运行中的容器排查错误？
    可以使用``sudo docker exec -it container /bin/bash``来进入容器内部，再运行一些查错工具。但如果容器本身不带查错工具的话，还需要安装。这种情况下，最好是在原来镜像的基础上构建一个dev镜像，安装这些工具，以免影响原有容器的大小。
2. docker-compose中变量的顺序？
    docker-compose中定义的优先级最高，其次是运行docker-compose命令时的shell变量，再次是.env文件，再次是dockerfile里定义的变量。如果都找不到，则为未定义。
    只要在Dockerfile或者docker-compose.yml中声明了变量（即没有赋值），当运行docker-compose命令时，只要shell中有此变量，即可自动传递进容器。
3. 如何给build过程设置变量？
    可以在docker-compose.yml中的build项下这样设置:
    ```yaml
        build:
      context: .
      args:
        PYPI_INDEX_URL: ${PYPI_INDEX_URL:-https://mirrors.aliyun.com/pypi/simple/}
    ```
    这里${key:-default}语法是当环境变量中没有设置PYPI_INDEX_URL时，则使用缺省值。