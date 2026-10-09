---
title: "How to Restart MiniQMT Without Manual Login"
date: 2023-12-14
slug: en/posts/tools/auto-restart-miniqmt
tags: [MiniQMT, QMT, Live Trading]
excerpt: "The xtquant package lacks auto-reconnect, so an unstable MiniQMT must be restarted with a new session ID. This guide shows how to enable password-free restart by preserving the linkMini auth file."
lang: en
translation_of: posts/tools/auto-restart-miniqmt
auto_translated: true
source_sha: fc5e1f4bcffdfbf9f1bfc5cc6223292554e74349
---

The live-trading interface MiniQMT can be unstable at times. The xtquant package does not yet provide automatic reconnection. When xtquant stops working properly, you need to restart MiniQMT and establish a new connection (be sure to use a new `sessionid`). The problem is that some QMT builds, such as the Sinolink Securities (国金) version, do not offer password-free login. What can you do?

<!--more-->

There is an undocumented workaround. When the Sinolink version of QMT logs in, it generates a file named linkMini. This file contains the password and other information, and as long as it exists in the `\bin.x64` directory, MiniQMT can start without manual login.

The linkMini file is generated after you log in to QMT (the full client, as opposed to MiniQMT, the lightweight mode). It exists only for a very short time before being deleted. So you need to copy it out in time:

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

This script must be run from inside the `\bin.x64` directory. Once the copy succeeds, the script exits automatically. Now exit QMT as well, go to the bin.x64 directory, make a copy of linkMini_copy named linkMini, and then modify its security attributes:

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/linkmini.png)

You need to clear all Allow permissions for the SYSTEM and Users groups, and check Deny for Write. After this change, the file becomes read-only and can no longer be deleted by QMT.

You can now restart MiniQMT automatically. Since an argument needs to be passed, you have to do it via a script:

``` batch
@echo on
title run MiniQmt without logon

set qmtPath=D:\QMT\bin.x64
CD /D %qmtPath%

taskkill /F /IM xtMiniQmt.exe /T

start "" "xtMiniQmt.exe" linkMini
```

This solution was contributed by a member of our quant community — special thanks!
