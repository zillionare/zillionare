#!/usr/bin/env python3
""".env 加载器：把仓库根目录的 .env 解析进环境变量，供子进程使用。

.env 里可能写成 `KEY = "value"`（等号带空格），bash 无法直接 source。
支持 --exec 直接以该环境运行命令。

用法:
  python3 tools/dotenv_run.py --python .venv/bin/python -- -m pdf2zh file.pdf
  python3 tools/dotenv_run.py --print-keys
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_ENV = Path(__file__).resolve().parents[2] / ".env"  # scripts/pdftools -> repo root


def load_env(path: Path, environ: dict | None = None) -> dict:
    env = dict(environ if environ is not None else os.environ)
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", s)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        env[key] = val
    return env


def main() -> int:
    ap = argparse.ArgumentParser(description="加载 .env 并以该环境执行命令")
    ap.add_argument("--env-file", type=Path, default=DEFAULT_ENV)
    ap.add_argument("--print-keys", action="store_true", help="只列出变量名，不显示值")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    if not args.env_file.exists():
        print(f"[warn] 未找到 {args.env_file}", file=sys.stderr)
    env = load_env(args.env_file)

    if args.print_keys:
        for k in sorted(k for k in env if k.startswith(("LLM_", "OPENAI_"))):
            print(k)
        return 0

    cmd = [c for c in args.cmd if c != "--"]
    if not cmd:
        print("未提供命令。示例: dotenv_run.py -- printenv LLM_MODEL", file=sys.stderr)
        return 2
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    sys.exit(main())