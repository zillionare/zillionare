**OpenClaw Gateway Healthcheck — 安装说明**

- 目标：在 `mini-one` 上运行一个守护脚本，当 `weixin getUpdates error` 连续出现时自动重启 `ai.openclaw.gateway`。

步骤（在 `mini-one` 上执行）：

1. 将脚本复制到合适位置（以 `openclaw` 用户登录）：

```bash
# 在 mini-one 上执行
mkdir -p ~/.openclaw/bin
# 假设你把仓库的脚本上传至 mini-one 的 /tmp 或通过 scp 复制
cp /path/to/openclaw_gateway_healthcheck.py ~/.openclaw/bin/
chmod +x ~/.openclaw/bin/openclaw_gateway_healthcheck.py
```

2. 复制 LaunchAgent plist（示例在 `launchd/ai.openclaw.gateway-healthcheck.plist`）到用户的 LaunchAgents：

```bash
mkdir -p ~/Library/LaunchAgents
cp /path/to/ai.openclaw.gateway-healthcheck.plist ~/Library/LaunchAgents/
# 编辑 plist 中的脚本路径，确保它指向 ~/.openclaw/bin/openclaw_gateway_healthcheck.py
```

3. 加载并启动 LaunchAgent：

```bash
# 以 openclaw 用户执行
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway-healthcheck.plist
launchctl enable gui/$(id -u)/ai.openclaw.gateway-healthcheck
# 或直接 kickstart 来立即运行一次
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway-healthcheck
```

4. 可选环境变量（通过编辑 plist 的 `ProgramArguments` 前面加入 `env` 或使用 `launchctl setenv`）：
- `OCW_THRESHOLD`：连续错误计数阈值（默认 `5`）
- `OCW_COOLDOWN`：重启后冷却时间（秒，默认 `60`）
- `OCW_LAUNCHD_LABEL`：要重启的 launchd label（默认 `ai.openclaw.gateway`）

5. 验证：

```bash
# 查看 healthcheck 日志
tail -f ~/.openclaw/logs/gateway-healthcheck.out.log
# 查看是否已加载
launchctl print gui/$(id -u)/ai.openclaw.gateway-healthcheck
```

备注：
- 这个脚本是“保守”的策略：仅在检测到连续 `weixin getUpdates error` 达到阈值时触发 restart，重启后会冷却一段时间以避免不断重启。
- 如果你更愿意将重启逻辑内嵌到 `openclaw-gateway` 代码中（例如在 weixin 监控模块中检测并 exit(1)），也可以修改扩展源；但通过外部守护脚本的方式更容易部署且无需改动运行的应用代码。
