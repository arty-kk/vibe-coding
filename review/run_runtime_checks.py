#!/usr/bin/env python3
"""Replay deterministic HTTP and invocation regression checks; no model execution."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    result = subprocess.run([sys.executable, '-B', str(ROOT/'review/check_mcp_http_boundary.py'),
                             '--fixture', str(ROOT/'review/fixtures/mcp-http-valid')],
                            capture_output=True, text=True, check=True)
    print(result.stdout.strip().splitlines()[-1])
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory)/'serverless'
        shutil.copytree(ROOT/'review/fixtures/serverless', target)
        original = (target/'handler.mjs').read_bytes()
        subprocess.run(['git', 'apply', str(ROOT/'review/evaluations/1.2.0-serverless.patch')], cwd=target, check=True)
        fixed = (target/'handler.mjs').read_bytes()
        (target/'handler.mjs').write_bytes(original)
        before = subprocess.run(['node', '--test'], cwd=target, capture_output=True, text=True)
        if before.returncode == 0:
            raise RuntimeError('Invocation regressions failed to detect the original defect')
        print('Original invocation with regression checks: rejected as expected')
        (target/'handler.mjs').write_bytes(fixed)
        subprocess.run(['node', '--test'], cwd=target, check=True)

if __name__ == '__main__':
    main()
