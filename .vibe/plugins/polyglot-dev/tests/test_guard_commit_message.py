"""Tests for the guard_commit_message.py pre-tool hook script."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_DIR / "guard_commit_message.py"

spec = importlib.util.spec_from_file_location("guard_commit_message", SCRIPT)
wip_guard = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(PLUGIN_DIR))
spec.loader.exec_module(wip_guard)


def run_hook(payload, env_extra=None):
    env = {**os.environ, **env_extra} if env_extra else None
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        cwd=PLUGIN_DIR,
        env=env,
        check=False,
    )


def test_blocks_wip_subject_double_quotes():
    assert wip_guard.is_wip_commit('git commit -m "WIP: refactor"') is True


def test_blocks_wip_subject_single_quotes():
    assert wip_guard.is_wip_commit("git commit -m 'wip add tests'") is True


def test_blocks_bracketed_wip_and_unquoted():
    assert wip_guard.is_wip_commit('git commit -m "[WIP] stuff"') is True
    assert wip_guard.is_wip_commit("git commit -m WIP") is True


def test_blocks_do_not_merge():
    assert wip_guard.is_wip_commit('git commit -m "DO NOT MERGE"') is True


def test_allows_normal_subject():
    assert wip_guard.is_wip_commit('git commit -m "Add login endpoint"') is False


def test_wip_inside_body_is_not_subject():
    assert wip_guard.is_wip_commit('git commit -m "Add login" -m "WIP notes"') is False


def test_allows_commit_without_message_args():
    assert wip_guard.is_wip_commit("git commit") is False
    assert wip_guard.is_wip_commit("git commit --amend --no-edit") is False


def test_ignores_non_commit_commands():
    assert wip_guard.is_wip_commit('echo "WIP"') is False


def test_subject_from_file(tmp_path):
    msg = tmp_path / "msg.txt"
    msg.write_text("\nWIP: from file\n", encoding="utf-8")
    assert wip_guard.is_wip_commit(f"git commit -F {msg}") is True


def test_unreadable_message_file_passes(tmp_path):
    assert wip_guard.is_wip_commit(f"git commit -F {tmp_path}/missing.txt") is False


def test_hook_blocks_via_stdin():
    proc = run_hook({"command": 'git commit -m "WIP: x"'})
    assert proc.returncode == 1
    assert b"WIP" in proc.stderr


def test_hook_passes_normal_commit():
    proc = run_hook({"command": 'git commit -m "Add feature"'})
    assert proc.returncode == 0


def test_env_override_disables():
    proc = run_hook({"command": 'git commit -m "WIP: x"'}, env_extra={"POLYGLOT_WIP_DISABLED": "1"})
    assert proc.returncode == 0


def test_hook_fails_open_on_garbage():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], input=b"not json", capture_output=True, cwd=PLUGIN_DIR, check=False
    )
    assert proc.returncode == 0
