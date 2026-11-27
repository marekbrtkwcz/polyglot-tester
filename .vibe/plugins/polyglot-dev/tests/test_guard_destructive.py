"""Tests for the guard_destructive.py pre-tool hook script."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "guard_destructive.py"

spec = importlib.util.spec_from_file_location("guard_destructive", SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def run_hook(payload):
    """Run the script as the hook runner would: JSON on stdin, exit code out."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload).encode(),
        capture_output=True,
    )


# --- is_bulk_rm: blocked spellings -------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf build",
        "rm -fr build",
        "rm -r -f build",
        "rm -f -r build",
        "rm -r build -f",
        "rm --recursive --force build",
        "rm -r --force build",
        "rm --recursive -f build",
        "rm -vrf build",
        "sudo rm -rf /",
        "echo hi && rm -rf build",
        "cd /tmp && rm -rf .cache",
        "xargs rm -rf",
        "rm -rf build; echo done",
        "rm  -rf  build",
    ],
)
def test_bulk_rm_blocked(command):
    assert guard.is_bulk_rm(command) is True


# --- is_bulk_rm: allowed spellings ------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "rm build",               # single target, no flags
        "rm -f build.log",        # force without recursive
        "rm -r build",            # recursive without force
        "rm -- build",            # end of options, no flags
        "rm -r build; echo -f",   # -f belongs to echo, not rm
        "rm -r dir -- --force",   # after --, --force is a path
        "transform --force",      # rm is a substring, not a word
        "grep rm readme",         # rm as a plain argument
    ],
)
def test_bulk_rm_allowed(command):
    assert guard.is_bulk_rm(command) is False


# --- other blocked patterns --------------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "git reset --hard HEAD~1",
        "git clean -fd",
        "git push origin main --force",
        "git push --force-with-lease=false",  # not the safe lease form
        "git stash drop",
        "git stash clear",
    ],
)
def test_git_patterns_blocked(command):
    result = run_hook({"command": command})
    assert result.returncode == 1
    assert b"blocked by polyglot-dev guard" in result.stderr


def test_force_with_lease_allowed():
    result = run_hook({"command": "git push origin main --force-with-lease"})
    assert result.returncode == 0


# --- end-to-end hook behavior -------------------------------------------------


def test_hook_blocks_rm_rf_in_nested_payload():
    payload = {"tool": "bash", "input": {"arguments": {"command": "rm -r -f build"}}}
    result = run_hook(payload)
    assert result.returncode == 1


def test_hook_passes_unrecognized_payload():
    result = run_hook({"something": "else"})
    assert result.returncode == 0


def test_hook_never_blocks_on_unparseable_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=b"not json at all",
        capture_output=True,
    )
    assert result.returncode == 0


def test_hook_allows_normal_command():
    result = run_hook({"command": "npm test"})
    assert result.returncode == 0
