"""Tests for the guard_all.py single-process pre-tool entrypoint."""

import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_DIR / "guard_all.py"

spec = importlib.util.spec_from_file_location("guard_all", SCRIPT)
guard_all = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(PLUGIN_DIR))
spec.loader.exec_module(guard_all)


def run_hook(payload, env_extra=None):
    env = {**os.environ, **env_extra} if env_extra else None
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        check=False,
    )


def test_blocks_destructive_command():
    result = run_hook({"command": "rm -rf build"})
    assert result.returncode == 1
    assert b"rm with recursive+force" in result.stderr


def test_blocks_wip_commit():
    result = run_hook({"command": 'git commit -m "WIP: x"'})
    assert result.returncode == 1
    assert b"WIP" in result.stderr


def test_blocks_write_with_secret():
    result = run_hook({"path": "c.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'\n"})
    assert result.returncode == 1
    assert b"AWS access key" in result.stderr


def test_allows_clean_command():
    assert run_hook({"command": "ls"}).returncode == 0


def test_allows_clean_write():
    assert run_hook({"path": "m.py", "content": "print('hi')\n"}).returncode == 0


def test_first_block_wins():
    # destructive runs before the WIP check, as in the old hook order
    result = run_hook({"command": 'git commit -m "WIP: x" && rm -rf build'})
    assert result.returncode == 1
    assert b"rm with recursive+force" in result.stderr


def test_env_overrides_still_work_per_guard():
    wip = {"command": 'git commit -m "WIP: x"'}
    assert run_hook(wip, {"POLYGLOT_WIP_DISABLED": "1"}).returncode == 0
    rm = {"command": "rm -rf build"}
    assert run_hook(rm, {"POLYGLOT_GUARD_DISABLED": "1"}).returncode == 0


def test_fails_closed_on_empty_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], input=b"", capture_output=True, check=False
    )
    assert result.returncode == 1
    assert b"empty stdin" in result.stderr


def test_fallback_interpreter_cannot_bypass_block():
    # `python guard_all.py || python3 guard_all.py`: the second run sees the
    # consumed stdin and must fail closed too
    cmd = f'"{sys.executable}" "{SCRIPT}" || "{sys.executable}" "{SCRIPT}"'
    result = subprocess.run(
        cmd,
        input=json.dumps({"command": "rm -rf /"}).encode(),
        capture_output=True,
        shell=True,
        check=False,
    )
    assert result.returncode == 1


def test_fails_open_on_garbage_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=b"not json",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0


def run_main(monkeypatch, stdin_text, env=None):
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))
    if env:
        for key, value in env.items():
            monkeypatch.setenv(key, value)
    return guard_all.main()


def test_main_in_process(monkeypatch):
    assert run_main(monkeypatch, "") == 1
    assert run_main(monkeypatch, "  \n ") == 1
    assert run_main(monkeypatch, "not json") == 0
    assert run_main(monkeypatch, json.dumps({"command": "ls"})) == 0
    assert run_main(monkeypatch, json.dumps({"command": "rm -rf /"})) == 1
    wip = json.dumps({"command": 'git commit -m "WIP: x"'})
    assert run_main(monkeypatch, wip) == 1
    assert run_main(monkeypatch, wip, {"POLYGLOT_WIP_DISABLED": "1"}) == 0
