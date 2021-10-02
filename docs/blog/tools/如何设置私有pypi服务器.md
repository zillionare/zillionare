有好些个场景需要我们设置自己的私有pypi服务器，比如，公司要在内部发布具有知识产权的python库，所以不希望通过pypi来发布；有时候我们为了调试需要，需要临时预发布某个依赖包供其它模块使用等等。比如最近在apple m1机器上频繁遇到此类问题，一些macos arm64的原生库只在miniforge上存在，pypi反应要慢很多。我们在本地编译生成原生包之后，由于无法上传到pypi，像poetry这样的软件仍然无法使用，这会导致很多CI/CD过程无法正常执行。

有好几个架设私有pypi服务器的方案，功能比较强劲的有[devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html)，它提供了一个兼容pypi的服务器，并且支持搜索。不过它的配置略微复杂一些，我们这里介绍一个更简单的方案：[python-pypi-mirror](https://pypi.org/project/python-pypi-mirror/)库。它的工作原理很简单，它主要用来生成符合pypi repo结构的本地目录，然后我们就可以使用第三方的web server来发布这个目录，使之模拟pypi服务器。

安装之后，它提供了以下几个命令：
```
    list             list packages
    download         download packages and their dependencies
    create           create the mirror
    delete           delete a package, use at your own risk!
    write-metadata   create metadata files
    query            query PyPI to retrieve the versions of a package
```
这里最重要的是create命令：
```
pypi-mirror create -d /path/to/packages -m simple
```
这里”-m simple"将会在当前目录下生成一个名为simple的目录（名字可以为任意），pypi-mirror会在这个目录下构建一些子目录，生成index.html文件，以及建立到packages中文件的连接。

因此，我们在使用pypi-mirror时，只要把私有包放置在/path/to/packages目录下，然后运行上述命令，这个目录及相应的结构就生成好了（每次放置新包后，都需要重新运行上述命令）。

然后我们需要运行web server来通过http的方式来提供服务（比如python -m http.server)。假设web server地址如下：
http://localhost/simple,那么我们需要个性~/.conf/pip/pip.conf文件如下：

```
[global]
index-url = http://localhost/simple
trusted-host = mirrors.aliyun.com
               pypi.org
               localhost
extra-index-url = https://pypi.org/simple
                  https://mirrors.aliyun.com/pypi/simple
```
pip目录还能接受http服务，但像poetry这样的客户端，只能接受https服务了，因此，我们需要寻找能提供https服务的web server，比如nginx。加密证书可以在letsencrypt上申请。letsencrypt提供了好用的客户端工具,certbot，它不仅能自动生成证书，还能对应修改服务器配置（比如nginx.conf),用户体验非常好。

如果要mirror pypi, 你需要使用它的download命令来从pypi上下载包。不过，经由上述配置，多数情况下，我们并不需要在本地拥有一个pypi的镜像。


