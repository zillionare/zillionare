---
title: 当我在星巴克连上家里的服务器，IPV6，你是值得的
slug: ipv6-how-to
date: 2024-07-29
img: https://images.jieyu.ai/images/hot/mybook/by-swimming-pool.jpg
category: others
tags:
  - network
  - tools
lineNumbers: true  
---

我们的课程环境是构建在一个256GB内存，192核CPU的集群上，学员可以通过浏览器，输入地址访问。要在阿某云上租这样一个服务器，价格并不便宜。所以，这些服务器一直放在公司里，创业期间，公司也就是租的民用宽带，没有公网IP，所以，在阿某云上租了个机器，做的端口转发。

有了这个端口转发，也就把VPN装上了，这样一来，也可以在回家或者外出时，连回公司办公。但最近VPN不知为啥，坏了。

刚好今年国家政策在推IPV6。于是决定试一把。IPV6最大的优点，就是地址管够，所以，每一台设备都可以获得一个公有的IPV6地址。



花了4小时左右，把IPV4和IPV6都弄通了，并且增加了免费的DDNS，这样，就可以在星巴克办公了。

意外的惊喜，我之前开的阿某云服务器带宽是5M。用了IPV6后，直连的效果真棒，现在我们的教学网站是秒开了。

!!! info
    如果你的路由器支持IPv6桥接模式（一般在网络、或者Wan设置里），那么可能直接打开它、打开光猫中的IPv6就ok了。直接跳转到第3节检查是否获得了IPV6地址。

## 光猫改桥接

IPV6地址也有公网和私域之分。公网地址以2开头，私域地址以F开头。如果你的设备用的是F开头的IPV6，仍然是不可通的。

新装的宽带，民用的基本上都默认开通了IPV6。我们要做的是，其实是如何打通光猫与内部路由器之间的IPV6屏蔽。

这主要是，

1. 你的路由器太旧，不支持IPV6
2. 路由器设置没有支持IPV6


首先，我们将光猫的连接方式由PPPoE改成桥接模式。这一步完成后，光猫就不再担任路由器的功能，因此拨号的工作也交给你自己的路由器。

!!! info
    这一步需要超级管理员密码，跟负责片区的宽带师傅要，只要你能证明自己懂网络，他们一定会给。

在网络配置中，找到宽带设置，找到最符合当前网络设置的那一项。比如，在我这里，这一项如下图所示：



![](https://images.jieyu.ai/images/2024/07/original-connection.jpg)

我们要修改的正是红框内的连接，而不是其它连接。当前它的连接方式是PPPoE，一般来说，其它模式，比如桥接，也会在这个单选框下。另外，IP协议版本这里要注意，一定要选择IPv4/IPv6。

在同一个对话框中，还显示了PPPoE的账号。我们必须把这个账号及其密码记录下来。因为我们改为桥接模式之后，建立连接的任务将由你的路由器来完成，路由器需要知道这个账号。

密码是以mask的方式显示的。如果你不知道密码，可以在chrome中打开开发者模式，找到密码框，将它的type="password"去掉，这样密码就还原显示了。




下图就是我们修改后的配置：

![](https://images.jieyu.ai/images/2024/07/20240729094230.png)



注意核心点就是IP协议版本、模式，其它保持不变即可。

## 配置路由器

!!! notice
    注意路由器与光猫的物理连接。要用线缆将路由器的wan口连接到光猫的lan口，而不是lan对lan。如果是后者，那么路由器将无法进行拨号。

路由器的配置中，我们要调整wan与lan的设置。有的路由器本身有IPv6桥接模式，在将光猫改为桥接之后，我们是要禁掉这里的格桥接模式的。

在WAN设置中，我们将连接方式改为PPPoE，并填写光猫的IP地址、用户名和密码。如果它同时提供了IPv4和IPv6两个选项，我们在IPv6中，选择启用，并且设置为复用IPv4拨号线路即可。其它的都保持默认。

![](https://images.jieyu.ai/images/2024/07/ipv6-router-settings.jpg)

再转到LAN设置，我们需要对IPv6进行一些设置。

![](https://images.jieyu.ai/images/2024/07/ipv6-lan-router.jpg)

我们还要开启DHCPv6服务，并设置IPv6地址池，重点是设置DNS：


![](https://images.jieyu.ai/images/2024/07/ipv6-dns-settings.jpg)


## 测试是否获得公网IPv6地址

ipw.cn网站提供了测试服务。喜欢命令行的可以使用以下命令：

```bash
curl 6.ipw.cn
```

如果你的机器有了IPv6地址，它就会返回你的IPv6地址。再检查如果它是以2开头的，则说明是公网IP。如果是以F开头的，那你的设置仍然是在私域。

通过下面的命令检测IPv4是否仍然工作：

```bash
curl 4.ipw.cn
```
这会返回你的IPv4地址。

如果不习惯使用命令行，也可以登录ipw.cn的网站。它将返回你当前的IP地址。如果使用了IPv6，它将提示IPv6优先，否则，就是配置不成功。

## 配置DDNS

尽管IPv6地址是公网地址，而且很充裕，但也不排除ISP有时候会更换你的IPv6地址。因此，我们需要DDNS服务，及时更新变化后的IP。平常只使用域名来访问。

最好用的DDNS服务是Cloudflare。要做到这一点，首先，你要在Cloudflare上已有托管的域名。然后，在[dashboard](https://dash.cloudflare.com/profile/api-tokens)中，申请一个API token。

DDNS使用go-ddns的容器就好。每一个需要在外网能独立访问的设备都需要安装。

```bash
sudo docker run -d --name ddns-go --restart=always --net=host -v /opt/ddns-go:/root jeessy/ddns-go
```

然后打开 http://ip:9876 更新配置即可。由于于API token，所以不需要在Cloudflare上事先创建子域名。直接在这里的界面输入子域名，go-ddns会自动帮你创建。

设置完成后，看一下日志就好了。

## 注意事项

不要通过域名暴露你的http服务。有可能被ISP封。据说使用https服务和高于40000的端口会降低风险。

