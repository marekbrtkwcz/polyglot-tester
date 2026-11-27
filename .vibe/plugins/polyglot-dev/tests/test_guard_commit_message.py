"""Tests for the guard_commit_message.py pre-tool hook script."""

import importlib.util
import io
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


def test_blocks_wip_with_combined_short_flags():
    # -am is `git commit -a -m`: the message must still be scanned
    assert wip_guard.is_wip_commit('git commit -am "WIP: refactor"') is True
    assert wip_guard.is_wip_commit("git commit -am 'wip fix'") is True
    assert wip_guard.is_wip_commit('git commit -a -m "WIP: x"') is True
    assert wip_guard.is_wip_commit('git commit --amend -m "WIP: x"') is True
    assert wip_guard.is_wip_commit('git commit -am "Add feature"') is False


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


def test_ignores_dash_m_of_other_tools_in_same_line():
    # `-m wip` belongs to pytest here, not to git commit
    assert wip_guard.is_wip_commit('pytest -m wip && git commit -m "fix bug"') is False
    assert wip_guard.is_wip_commit('git commit -m "fix bug" && pytest -m wip') is False
    assert wip_guard.is_wip_commit('git commit -m "fix bug"; pytest -m wip') is False


def test_blocks_wip_in_any_commit_of_a_chain():
    assert (
        wip_guard.is_wip_commit('git commit -m "ok" && git commit -m "WIP: x"') is True
    )


def test_blocks_wip_subject_with_separator_inside_quotes():
    assert wip_guard.is_wip_commit('git commit -m "WIP: foo; bar"') is True
    assert wip_guard.is_wip_commit("git commit -m 'wip && wip'") is True


def test_blocks_parenthesized_wip():
    assert wip_guard.is_wip_commit('git commit -m "(wip) stuff"') is True


def test_quoted_flags_of_other_tools_do_not_leak_into_commit():
    assert wip_guard.is_wip_commit('pytest -m "wip; x" && git commit -m "ok"') is False


def test_blocks_wip_subject_with_escaped_quote_before_separator():
    assert wip_guard.is_wip_commit('git commit -m "WIP: \\"a; b"') is True


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
    proc = run_hook(
        {"command": 'git commit -m "WIP: x"'}, env_extra={"POLYGLOT_WIP_DISABLED": "1"}
    )
    assert proc.returncode == 0


def test_hook_fails_open_on_garbage():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=b"not json",
        capture_output=True,
        cwd=PLUGIN_DIR,
        check=False,
    )
    assert proc.returncode == 0


def test_hook_fails_closed_on_empty_stdin():
    # a fallback interpreter in `python x || python3 x` re-runs the guard on
    # the consumed stdin; that must not wave a payload through
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=b"",
        capture_output=True,
        cwd=PLUGIN_DIR,
        check=False,
    )
    assert proc.returncode == 1


# --- main() in process -------------------------------------------------------


def run_main(monkeypatch, stdin_text, env=None):
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))
    if env:
        for key, value in env.items():
            monkeypatch.setenv(key, value)
    return wip_guard.main()


def test_main_in_process_empty_stdin_fails_closed(monkeypatch):
    assert run_main(monkeypatch, "") == 1


def test_main_in_process_garbage_fails_open(monkeypatch):
    assert run_main(monkeypatch, "not json") == 0


def test_main_in_process_blocks_wip_and_env_gate(monkeypatch):
    wip = json.dumps({"command": 'git commit -am "WIP: x"'})
    assert run_main(monkeypatch, wip) == 1
    assert run_main(monkeypatch, wip, {"POLYGLOT_WIP_DISABLED": "1"}) == 0
    assert run_main(monkeypatch, wip, {"POLYGLOT_WIP_DISABLED": "0"}) == 1
    ok = json.dumps({"command": 'git commit -m "Add feature"'})
    assert run_main(monkeypatch, ok) == 0
    assert run_main(monkeypatch, json.dumps({})) == 0
