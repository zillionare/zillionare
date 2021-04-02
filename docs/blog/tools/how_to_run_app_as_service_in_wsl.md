WSL是不会随Windows启动而启动的。如果您启用的是WSL 1.0，那么在WSL里安装了应用程序，它们也不能以服务方式运行。这里提供一个方案，以获得更好的自动化体验。

我们这里的方案来自于[gh://wsl-autostart](https://github.com/troytse/wsl-autostart/blob/master/README_zh.md)。

方案总共分四步：

1. 将该项目clone到本地
2. 修改commands.txt文件
3. 修改wsl里的sudoers文件
4. 添加任务计划，实现开机自启动

我们从第二步讲起。

# 配置跟随WSL启动的服务

commands.txt里是我们要在wsl里，自动启动的那些应用，比如：
```
/etc/init.d/cron
/etc/init.d/ssh
/etc/init.d/mysql
/etc/init.d/apache2
```
这里根据自己的情况来取舍。

# 设置sudoer文件

可能有一些服务必须以特别的权限来启动，因此直接执行上面的命令时，可能会提示输入root密码，这样就导致无法自动启动。

为了避免这种情况，可以设置sudoer文件

```
# /etc/sudoers
%sudo ALL=NOPASSWD: /etc/init.d/cron
%sudo ALL=NOPASSWD: /etc/init.d/ssh
%sudo ALL=NOPASSWD: /etc/init.d/mysql
%sudo ALL=NOPASSWD: /etc/init.d/apache2
```
通过如上配置，启动这些服务时，就不再需要输入密码了。

# 配置开机自启动
这里我们采用任务计划的方法。

- step 1
![](http://images.jieyu.ai/images/202104/20210402215128.png)
- step 2
    配置为随机启动
![](http://images.jieyu.ai/images/202104/20210402215237.png)
- step 3
    设置任务脚本，这里指向前面clone到本地的start.vbs
![](http://images.jieyu.ai/images/202104/20210402215325.png)
- step 4
    最后，设置为“勿启动新实例"
    ![](http://images.jieyu.ai/images/202104/20210402215505.png)

任务计划设置完成后，可以在任务计划中找到该任务，点击"启动"测试一下。
![](http://images.jieyu.ai/images/202104/20210402215623.png)
由于在服务中开启了ssh，所以可以使用ssh连接一下服务器。

