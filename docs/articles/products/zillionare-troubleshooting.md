---
title: Zillionare 2.0 故障排除
slug: zillionare-2.0-troubleshooting
---

## 1. 在omega日志中出现failed to build unclosed bar for ...错误
这个错误如下图所示
![50%](rebuild-unclosed-bar-error.png)

出现这个错误的原因是因为安装后，初次启动的时间是在盘后，redis数据库中没有分钟线数据，因而也无法合成某些数据。等待下个交易日结束，数据补齐后，该日志会消息。详情见[数据维护](zillionare-maintain.md)


