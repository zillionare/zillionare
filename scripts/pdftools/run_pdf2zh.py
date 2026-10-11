#!/usr/bin/env python3
"""批量跑 pdf2zh 翻译（当前唯一维护的翻译入口）。

取代已删除的 batch_translate.sh（它指向已不存在的 /tmp venv 与旧目录结构，
且不带术语表、会归档不需要的 dual 版）。

行为：
  - 从仓库 .env 读取 LLM_SMART_*（容错等号两侧空格），映射为 OPENAILIKED_*
  - 术语表提示词：docs/assets/2026/pdf2zh-prompt.txt
  - 每篇产出 translations/<名>/zh.pdf（mono 重命名）；-dual.pdf 删除（不做对照）
  - 逐篇日志 /tmp/pdf2zh_<名>.log；状态增量写入 /tmp/pdf2zh_batch_status.txt

前置（一次性）：
  uv tool install --python 3.12 pdf2zh --index-url https://mirrors.aliyun.com/pypi/simple/
  # 修 pdf2zh 1.9.11 的依赖 bug（新版 tencentcloud-tmt 删了 TextTranslateRequest）：
  uv pip install --python ~/.local/share/uv/tools/pdf2zh/bin/python \
      'tencentcloud-sdk-python-tmt<3.1' --index-url https://mirrors.aliyun.com/pypi/simple/

用法：
  python3 run_pdf2zh.py                     # 默认：originals 中尚无译文的论文
  python3 run_pdf2zh.py A B                 # 指定论文名（不含 .pdf）
  python3 run_pdf2zh.py A --ignore-cache    # 强制重译（旧译文升级术语表时用）
  python3 run_pdf2zh.py --dry-run A         # 只打印将执行的命令
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# 默认模块目录（后续模块可加 --module-dir 指向其它目录）
DEFAULT_MODULE = Path(
    '/Users/aaronyang/workspace/zillionare/docs/assets/2026/'
    '30-quant-papers-module2')
DEFAULT_PROMPT = Path(
    '/Users/aaronyang/workspace/zillionare/docs/assets/2026/'
    'pdf2zh-prompt.txt')
PDF2ZH = Path.home() / '.local/bin/pdf2zh'


def load_env(path: Path) -> dict:
    """容错解析 .env（等号两侧可有空格、值可带引号）。"""
    out = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, _, v = line.partition('=')
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def build_env(repo_root: Path) -> dict:
    env_file = load_env(repo_root / '.env')
    missing = [k for k in ('LLM_SMART_URL', 'LLM_SMART_API_KEY', 'LLM_SMART')
               if k not in env_file]
    if missing:
        sys.exit(f'[error] .env 缺少: {", ".join(missing)}')
    return {**os.environ,
            'HF_ENDPOINT': 'https://hf-mirror.com',   # 国内下载版面模型
            'OPENAILIKED_BASE_URL': env_file['LLM_SMART_URL'],
            'OPENAILIKED_API_KEY': env_file['LLM_SMART_API_KEY'],
            'OPENAILIKED_MODEL': env_file['LLM_SMART']}


def pending(module_dir: Path) -> list:
    """originals 里尚无 zh.pdf 的论文。"""
    out = []
    for pdf in sorted((module_dir / 'originals').glob('*.pdf')):
        if not (module_dir / 'translations' / pdf.stem / 'zh.pdf').exists():
            out.append(pdf.stem)
    return out


def run_one(name: str, module_dir: Path, prompt: Path, env: dict,
            ignore_cache: bool, dry_run: bool) -> bool:
    out_dir = module_dir / 'translations' / name
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [str(PDF2ZH), str(module_dir / 'originals' / f'{name}.pdf'),
           '-s', 'openailiked', '-li', 'en', '-lo', 'zh',
           '--prompt', str(prompt), '-o', str(out_dir), '-t', '4']
    if ignore_cache:
        cmd.append('--ignore-cache')
    if dry_run:
        print('  ' + ' '.join(cmd))
        return True
    log = open(f'/tmp/pdf2zh_{name}.log', 'w')
    rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT,
                        env=env).returncode
    mono = out_dir / f'{name}-mono.pdf'
    dual = out_dir / f'{name}-dual.pdf'
    if rc != 0 or not mono.exists():
        return False
    shutil.move(str(mono), str(out_dir / 'zh.pdf'))
    if dual.exists():
        dual.unlink()
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description='批量 pdf2zh 翻译')
    ap.add_argument('papers', nargs='*', help='论文名（默认：无译文的全部）')
    ap.add_argument('--module-dir', type=Path, default=DEFAULT_MODULE)
    ap.add_argument('--prompt', type=Path, default=DEFAULT_PROMPT)
    ap.add_argument('--ignore-cache', action='store_true',
                    help='强制重译（升级术语表后重跑用）')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[2]  # scripts/pdftools -> repo root
    env = build_env(repo_root)
    names = args.papers or pending(args.module_dir)
    if not names:
        print('没有待翻译的论文（originals 中的都有 zh.pdf）')
        return 0
    print(f'[cfg] model={env["OPENAILIKED_MODEL"]} 论文: {", ".join(names)}')
    status = Path('/tmp/pdf2zh_batch_status.txt')
    failures = 0
    for name in names:
        t0 = time.time()
        ok = run_one(name, args.module_dir, args.prompt, env,
                     args.ignore_cache, args.dry_run)
        if not args.dry_run:
            line = (f'{"OK " if ok else "FAIL"} {name} '
                    f'{(time.time() - t0) / 60:.1f}min')
            print(line, flush=True)
            with open(status, 'a') as f:
                f.write(line + '\n')
        failures += (not ok)
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())