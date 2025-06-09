import os
import sys
import subprocess
import base64
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV['PYTHONPATH'] = str(PROJECT_ROOT / 'src')


def run_cli(*args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, '-m', 'crypto_universal', *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=True, env=ENV, cwd=PROJECT_ROOT)


def test_generate_keys_cli() -> None:
    result = run_cli('generate-keys')
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 2
    assert all(lines)

    priv = base64.b64decode(lines[0].encode())
    pub = base64.b64decode(lines[1].encode())
    token = run_cli('encrypt', base64.b64encode(pub).decode(), 'hi').stdout.strip()
    out = run_cli('decrypt', base64.b64encode(priv).decode(), token).stdout.strip()
    assert out == 'hi'


def test_cli_no_args() -> None:
    result = subprocess.run([sys.executable, '-m', 'crypto_universal'], capture_output=True, text=True, env=ENV, cwd=PROJECT_ROOT)
    assert 'usage:' in result.stdout

def test_cli_module_entrypoint():
    result = subprocess.run([sys.executable, '-m', 'crypto_universal.cli', '--help'], capture_output=True, text=True, env=ENV, cwd=PROJECT_ROOT)
    assert 'Crypto Universal CLI' in result.stdout
