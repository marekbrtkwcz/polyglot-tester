"""Tests for the prepush_checks.py pre-tool hook script."""

import importlib.util
import json
import os
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
    # history-rewriting pushes belong to guard-destructive-commands
    assert prepush.FORCE_PUSH.search("git push --force origin main")
    proc = run_hook({"command": "git push --force origin main"})
    assert proc.returncode == 0


def test_env_override_disables_push_checks():
    proc = run_hook({"command": "git push origin main"}, env_extra={"POLYGLOT_PREPUSH_DISABLED": "1"})
    assert proc.returncode == 0


def test_plain_push_runs_checks_and_passes_on_clean_repo():
    proc = run_hook({"command": "git push origin main"})
    assert proc.returncode == 0
    assert b"pre-push OK" in proc.stderr


def test_hook_fails_open_on_garbage():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], input=b"not json", capture_output=True, cwd=PLUGIN_DIR, check=False
    )
    assert proc.returncode == 0
