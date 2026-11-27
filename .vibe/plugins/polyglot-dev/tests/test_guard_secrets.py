"""Tests for the guard_secrets.py pre-tool hook script."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_DIR = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_DIR / "guard_secrets.py"

spec = importlib.util.spec_from_file_location("guard_secrets", SCRIPT)
secrets_guard = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(PLUGIN_DIR))
spec.loader.exec_module(secrets_guard)


def run_hook(payload, cwd=None, env_extra=None):
    env = None
    if env_extra:
        env = {**os.environ, **env_extra}
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        cwd=cwd,
        env=env,
        check=False,
    )


@pytest.fixture()
def repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


def stage(repo, name, content):
    (repo / name).write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", name], cwd=repo, check=True)


# --- pattern unit tests ------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "aws_key = AKIAIOSFODNN7EXAMPLE",
        "token = ghp_" + "A" * 36,
        "slack = xoxb-123456789012-abcdefghijkl",
        "stripe = sk_live_" + "a1B2" * 6,
        "google = AIza" + "a" * 35,
        "npm = npm_" + "a" * 36,
        "gitlab = glpat-" + "a" * 20,
        "sendgrid = SG." + "a" * 22 + "." + "b" * 43,
        "hook = https://hooks.slack.com/services/T12345678/B12345678/abcdef1234567890abcd",
        "jwt = eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
        "-----BEGIN RSA PRIVATE KEY-----",
        'config: api_key: "abcdef1234567890abcd"',
    ],
)
def test_find_secrets_detects_known_patterns(text):
    assert secrets_guard.find_secrets(text), text


@pytest.mark.parametrize(
    "text",
    [
        "password = short",
        "api_key = changeme",
        "token = ${ENV_TOKEN}",
        "-----BEGIN CERTIFICATE-----",
    ],
)
def test_find_secrets_ignores_non_secrets(text):
    assert not secrets_guard.find_secrets(text), text


# --- hook behavior in a real repo --------------------------------------------


def test_hook_blocks_staged_aws_key(repo):
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    result = run_hook({"command": "git commit -m init"}, cwd=repo)
    assert result.returncode == 1
    assert b"AWS access key" in result.stderr


def test_hook_blocks_untracked_github_token(repo):
    (repo / "notes.txt").write_text("tok: ghp_" + "B" * 36 + "\n", encoding="utf-8")
    result = run_hook({"command": "git add ."}, cwd=repo)
    assert result.returncode == 1
    assert b"GitHub token" in result.stderr


def test_hook_allows_clean_commit(repo):
    stage(repo, "main.py", "print('hello')\n")
    result = run_hook({"command": "git commit -m init"}, cwd=repo)
    assert result.returncode == 0


def test_hook_ignores_non_git_command(repo):
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    result = run_hook({"command": "npm test"}, cwd=repo)
    assert result.returncode == 0


def test_hook_passes_outside_git_repo(tmp_path):
    result = run_hook({"command": "git add ."}, cwd=tmp_path)
    assert result.returncode == 0


def test_hook_env_override_disables(repo):
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    result = run_hook(
        {"command": "git commit -m init"},
        cwd=repo,
        env_extra={"POLYGLOT_SECRETS_DISABLED": "1"},
    )
    assert result.returncode == 0


def test_hook_skips_lockfiles(repo):
    stage(repo, "package-lock.json", '"api_key": "abcdef1234567890abcd"\n')
    result = run_hook({"command": "git commit -m chore"}, cwd=repo)
    assert result.returncode == 0


# --- write/edit payload mode -------------------------------------------------


def test_hook_blocks_write_file_with_aws_key():
    result = run_hook(
        {"path": "config.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'\n"}
    )
    assert result.returncode == 1
    assert b"AWS access key" in result.stderr


def test_hook_blocks_edit_inserting_github_token():
    result = run_hook(
        {
            "file_path": "settings.py",
            "old_string": "token = None",
            "new_string": "token = 'ghp_" + "C" * 36 + "'",
        }
    )
    assert result.returncode == 1
    assert b"GitHub token" in result.stderr


def test_hook_blocks_nested_write_payload():
    result = run_hook(
        {"tool_input": {"path": "x.py", "content": "k = 'AKIAIOSFODNN7EXAMPLE'"}}
    )
    assert result.returncode == 1


def test_hook_allows_clean_write_file():
    result = run_hook({"path": "main.py", "content": "print('hello')\n"})
    assert result.returncode == 0


def test_hook_allows_edit_removing_a_secret():
    # old_string carries the secret being deleted — the file ends up
    # cleaner, so the write must pass
    result = run_hook(
        {
            "file_path": "settings.py",
            "old_string": "token = 'ghp_" + "D" * 36 + "'",
            "new_string": "token = os.environ['TOKEN']",
        }
    )
    assert result.returncode == 0


def test_hook_write_file_skips_lockfile_paths():
    result = run_hook(
        {
            "path": "package-lock.json",
            "content": '"api_key": "abcdef1234567890abcd"\n',
        }
    )
    assert result.returncode == 0


def test_hook_write_file_env_override_disables():
    result = run_hook(
        {"path": "config.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'\n"},
        env_extra={"POLYGLOT_SECRETS_DISABLED": "1"},
    )
    assert result.returncode == 0


def test_hook_write_mode_works_outside_git_repo(tmp_path):
    result = run_hook(
        {"path": "config.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'\n"},
        cwd=tmp_path,
    )
    assert result.returncode == 1
