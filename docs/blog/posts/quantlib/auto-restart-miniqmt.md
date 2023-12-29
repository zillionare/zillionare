---
title: 如何免登录重启miniqmt?
categories:
    - quantlib
date: 2023-12-14
tags:
    - quantlib
    - python
    - xtquant
---

实盘交易接口miniqmt在使用中，难免会遇到不稳定的时候。目前，xtquant包还没有提供自动重连的功能。当我们发现xtquant工作不正常的时候，需要重启miniqmt，重建新的连接（一定要使用新的sessionid）。问题是，有些版本的qmt，比如国金的版本，并没有提供免密登录，怎么办？

<!--more-->

有一个非公开的方法。国金版的qmt在登录时，会生成一个linkMini的文件。该文件包含了密码及其它信息，当该文件存在于\bin.x64目录下时，miniqmt就能免登录启动。

linkMini文件是在qmt（注意和miniqmt，即极简模式相对应）登录后生成的，它只存在很短的时间，立刻又被删除了。因此，我们需要把这个文件copy出来：

```batch
:loop
if exist linkMini (
    copy linkMini linkMini_copy 
    echo finish
    goto end
)
if exist linkmini (
    copy linkmini linkMini_copy 
    echo finish
    goto end
)
echo continue
timeout /t 0.1 >nul
goto loop
:end
```

这个脚本需要放到\bin.x64目录下运行。copy成功后，脚本就会自动退出。此时，我们也退出QMT，进入到bin.x64目录，复制一份linkMini_copy为linkMini，然后修改其安全属性：

![50%](https://images.jieyu.ai/images/2023/12/linkmini.png)

我们需要将system及users用户组下的权限中的允许完全取消，在拒绝部分，选中写入。这样设置之后，该文件变成只读，不会被qmt删除掉。

此时我们就可以自动重启miniqmt了，因为有参数传递，所以，我们要通过脚本来实现：

``` batch
@echo on
title run MiniQmt without logon

set qmtPath=D:\QMT\bin.x64
CD /D %qmtPath%

taskkill /F /IM xtMiniQmt.exe /T

start "" "xtMiniQmt.exe" linkMini
```

该方案由量化群里小伙伴提出，特别感谢！
