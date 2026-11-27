"""Tests for the prepush_checks.py pre-tool hook script."""

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_DIR / "prepush_checks.py"

spec = importlib.util.spec_from_file_location("prepush_checks", SCRIPT)
prepush = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(PLUGIN_DIR))
spec.loader.exec_module(prepush)


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


def test_ignores_non_push_commands():
    proc = run_hook({"command": "git commit -m 'x'"})
    assert proc.returncode == 0


def test_skips_force_push():
    # history-rewriting pushes belong to the destructive guard
    assert prepush.FORCE_PUSH.search("git push --force origin main")
    assert prepush.FORCE_PUSH.search("git push -f origin main")  # short flag
    assert prepush.FORCE_PUSH.search("git push origin main -f")
    proc = run_hook({"command": "git push --force origin main"})
    assert proc.returncode == 0
    proc = run_hook({"command": "git push -f origin main"})
    assert proc.returncode == 0


def test_env_override_disables_push_checks():
    proc = run_hook(
        {"command": "git push origin main"},
        env_extra={"POLYGLOT_PREPUSH_DISABLED": "1"},
    )
    assert proc.returncode == 0


def test_plain_push_runs_checks_and_passes_on_clean_repo():
    proc = run_hook({"command": "git push origin main"})
    assert proc.returncode == 0
    assert b"pre-push OK" in proc.stderr


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
    # a fallback interpreter in `python x || python3 x` re-runs the hook on
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
    return prepush.main()


def test_main_in_process_empty_stdin_fails_closed(monkeypatch):
    assert run_main(monkeypatch, "") == 1


def test_main_in_process_garbage_fails_open(monkeypatch):
    assert run_main(monkeypatch, "not json") == 0


def test_main_in_process_env_and_push_gates(monkeypatch, tmp_path):
    push = json.dumps({"command": "git push origin main", "cwd": str(tmp_path)})
    assert run_main(monkeypatch, push) == 0  # foreign project: silent no-op
    assert run_main(monkeypatch, push, {"POLYGLOT_PREPUSH_DISABLED": "1"}) == 0
    force = json.dumps({"command": "git push -f origin main"})
    assert run_main(monkeypatch, force) == 0  # destructive guard's job
    other = json.dumps({"command": "git commit -m x"})
    assert run_main(monkeypatch, other) == 0


def test_own_repo_detected_via_markers():
    assert prepush.is_own_repo(prepush.REPO_ROOT) is True


def test_foreign_root_rejected(tmp_path):
    assert prepush.is_own_repo(tmp_path) is False


def test_silent_noop_in_foreign_project(tmp_path):
    # A plugin install in another project: no markers, so the hook must
    # pass silently — no "skipped" noise, no blocked push. Covers both
    # the payload-cwd path and the script-location fallback.
    install = tmp_path / ".vibe" / "plugins" / "polyglot-dev"
    install.mkdir(parents=True)
    for name in ("prepush_checks.py", "guard_destructive.py"):
        shutil.copy(PLUGIN_DIR / name, install / name)
    payloads = (
        {"command": "git push origin main", "cwd": str(tmp_path)},
        {"command": "git push origin main"},  # falls back to script location
    )
    for payload in payloads:
        proc = subprocess.run(
            [sys.executable, str(install / "prepush_checks.py")],
            input=json.dumps(payload).encode(),
            capture_output=True,
            cwd=install,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert proc.stderr == b""


def test_missing_pytest_fails_open(monkeypatch):
    monkeypatch.setattr(prepush, "pytest_available", lambda: False)
    results = prepush.run_checks(prepush.REPO_ROOT)
    pytest_results = [r for r in results if "pytest" in r[0]]
    assert pytest_results, "expected the pytest structure check in CHECKS"
    for label, ok, output in pytest_results:
        assert ok is True, (label, output)
        assert "pytest not installed" in output
