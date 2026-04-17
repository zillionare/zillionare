#!/usr/bin/env python3
"""
Simple healthcheck that tails OpenClaw gateway logs and restarts the launchd job
`ai.openclaw.gateway` when `weixin getUpdates error` appears consecutively.

Usage (on mini-one):
  - Copy this script to e.g. ~/.openclaw/bin/openclaw_gateway_healthcheck.py
  - Make executable: `chmod +x ~/.openclaw/bin/openclaw_gateway_healthcheck.py`
  - Create and load the accompanying LaunchAgent plist (see launchd/)

Behavior:
  - Tails `~/.openclaw/logs/gateway.err.log` (falls back to gateway.log)
  - Increments a counter each time a line matches the error pattern
  - If the counter reaches `THRESHOLD`, it will run a launchctl restart and
    sleep for `POST_RESTART_COOLDOWN` seconds to avoid flapping.
  - The counter resets when a line mentioning `weixin` without `error` appears
    (best-effort). This is intentionally conservative.

Notes:
  - This script assumes the gateway is managed by launchd with label
    `ai.openclaw.gateway` and should be run as the `openclaw` user.
"""

from __future__ import annotations
import os
import sys
import time
import re
import subprocess
from pathlib import Path

# Config
LOG_CANDIDATES = [Path.home() / '.openclaw' / 'logs' / 'gateway.err.log',
                  Path.home() / '.openclaw' / 'logs' / 'gateway.log']
PATTERN_ERROR = re.compile(r"weixin getUpdates error", re.IGNORECASE)
PATTERN_WEIXIN = re.compile(r"weixin", re.IGNORECASE)
THRESHOLD = int(os.environ.get('OCW_THRESHOLD', '5'))
CHECK_INTERVAL = float(os.environ.get('OCW_CHECK_INTERVAL', '0.5'))
POST_RESTART_COOLDOWN = int(os.environ.get('OCW_COOLDOWN', '60'))
LAUNCHD_LABEL = os.environ.get('OCW_LAUNCHD_LABEL', 'ai.openclaw.gateway')


def choose_log_file() -> Path:
    for p in LOG_CANDIDATES:
        if p.exists():
            return p
    # fallback to first candidate (may be created later)
    return LOG_CANDIDATES[0]


def restart_gateway() -> None:
    uid = os.getuid()
    # Use kickstart -k gui/<uid>/label to restart per-user LaunchAgent
    cmd = ['launchctl', 'kickstart', '-k', f'gui/{uid}/{LAUNCHD_LABEL}']
    print(f"[healthcheck] restarting {LAUNCHD_LABEL} via: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"[healthcheck] launchctl failed: {e}; will try unload/load fallback")
        try:
            subprocess.run(['launchctl', 'stop', LAUNCHD_LABEL], check=False)
            subprocess.run(['launchctl', 'start', LAUNCHD_LABEL], check=False)
        except Exception:
            pass


class FileFollower:
    def __init__(self, path: Path):
        self.path = path
        self._ino = None
        self._fp = None
        self._pos = 0

    def reopen_if_rotated(self):
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            return
        ino = stat.st_ino
        if ino != self._ino:
            if self._fp:
                try:
                    self._fp.close()
                except Exception:
                    pass
            self._fp = open(self.path, 'r', encoding='utf-8', errors='ignore')
            self._fp.seek(0, os.SEEK_END)
            self._ino = ino
            self._pos = self._fp.tell()

    def read_new_lines(self):
        if not self._fp:
            try:
                self.reopen_if_rotated()
            except Exception:
                return []
            if not self._fp:
                return []
        lines = []
        while True:
            line = self._fp.readline()
            if not line:
                break
            lines.append(line.rstrip('\n'))
        return lines


def main():
    log = choose_log_file()
    print(f"[healthcheck] watching log: {log}")
    follower = FileFollower(log)
    error_count = 0
    last_restart = 0

    while True:
        follower.reopen_if_rotated()
        lines = follower.read_new_lines()
        for ln in lines:
            # quick debug print
            # print(f"[healthcheck] log: {ln}")
            if PATTERN_ERROR.search(ln):
                error_count += 1
                print(f"[healthcheck] detected error ({error_count}/{THRESHOLD}): {ln}")
            elif PATTERN_WEIXIN.search(ln):
                # if it's a weixin-related line but not an error, reset counter
                if not PATTERN_ERROR.search(ln):
                    if error_count != 0:
                        print(f"[healthcheck] resetting error counter due to weixin activity: {ln}")
                    error_count = 0
            # otherwise ignore

            if error_count >= THRESHOLD:
                now = time.time()
                if now - last_restart < POST_RESTART_COOLDOWN:
                    print(f"[healthcheck] recent restart detected, skipping to avoid flapping")
                    error_count = 0
                    continue
                print(f"[healthcheck] threshold reached ({THRESHOLD}), restarting gateway")
                restart_gateway()
                last_restart = time.time()
                error_count = 0
                print(f"[healthcheck] sleeping {POST_RESTART_COOLDOWN}s post-restart")
                time.sleep(POST_RESTART_COOLDOWN)
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[healthcheck] exiting on KeyboardInterrupt')
        sys.exit(0)
