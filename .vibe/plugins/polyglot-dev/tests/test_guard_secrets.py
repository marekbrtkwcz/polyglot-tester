"""Tests for the guard_secrets.py pre-tool hook script."""

import importlib.util
import io
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
        "openai = sk-proj-" + "a" * 30,
        "legacy = sk-" + "b" * 48,
        "anthropic = sk-ant-" + "c" * 30,
        "hf = hf_" + "d" * 34,
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
    # the pattern would match if scanned: SKIP_PATHS must exclude the
    # staged diff of a lockfile too, not only untracked files
    stage(repo, "package-lock.json", 'api_key = "abcdef1234567890abcd"\n')
    result = run_hook({"command": "git commit -m chore"}, cwd=repo)
    assert result.returncode == 0


def test_hook_skips_lockfile_in_unstaged_diff(repo):
    stage(repo, "main.py", "print('hello')\n")
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    (repo / "yarn.lock").write_text(
        'api_key = "abcdef1234567890abcd"\n', encoding="utf-8"
    )
    result = run_hook({"command": "git add yarn.lock"}, cwd=repo)
    assert result.returncode == 0


def test_hook_skips_modern_lockfiles_and_source_maps(repo):
    (repo / "web").mkdir()
    for name in ("uv.lock", "poetry.lock", "web/app.js.map"):
        stage(repo, name, 'api_key = "abcdef1234567890abcd"\n')
    result = run_hook({"command": "git commit -m chore"}, cwd=repo)
    assert result.returncode == 0


def test_hook_allows_commit_removing_a_secret(repo):
    # the fix commit deletes the leaked key: the `-` diff line must not block
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\nkeep = 1\n")
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    (repo / "config.py").write_text("keep = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "config.py"], cwd=repo, check=True)
    result = run_hook({"command": "git commit -m 'remove leaked key'"}, cwd=repo)
    assert result.returncode == 0


def test_hook_plain_commit_ignores_unstaged_secret(repo):
    # unstaged worktree changes are not staged by a plain `git commit`
    (repo / "main.py").write_text("print('hello')\n", encoding="utf-8")
    subprocess.run(["git", "add", "main.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    (repo / "main.py").write_text(
        "print('hello')\ntok = 'ghp_" + "E" * 36 + "'\n", encoding="utf-8"
    )
    result = run_hook({"command": "git commit -m 'msg'"}, cwd=repo)
    assert result.returncode == 0
    # `git commit -a` stages the worktree: the same change must block
    result = run_hook({"command": "git commit -am 'msg'"}, cwd=repo)
    assert result.returncode == 1
    assert b"GitHub token" in result.stderr
    # `git add` scans the unstaged diff too: must block
    result = run_hook({"command": "git add main.py"}, cwd=repo)
    assert result.returncode == 1
    assert b"GitHub token" in result.stderr


def test_hook_scans_payload_cwd_not_process_cwd(repo):
    # Plugin hooks are spawned from the plugin snapshot; the project repo is
    # named in the payload's cwd. A staged secret there must be caught even
    # when the process runs from elsewhere.
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    result = run_hook(
        {"command": "git commit -m init", "cwd": str(repo)}, cwd=PLUGIN_DIR
    )
    assert result.returncode == 1
    assert b"AWS access key" in result.stderr


def test_hook_untracked_secret_ignored_on_plain_commit(repo):
    # `git commit` never includes untracked files: scanning them would only
    # produce false positives. `git add` must still catch them.
    (repo / "notes.txt").write_text("tok: ghp_" + "B" * 36 + "\n", encoding="utf-8")
    result = run_hook({"command": "git commit -m x"}, cwd=repo)
    assert result.returncode == 0
    result = run_hook({"command": "git add ."}, cwd=repo)
    assert result.returncode == 1
    assert b"GitHub token" in result.stderr


def test_hook_env_override_requires_exact_1(repo):
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    result = run_hook(
        {"command": "git commit -m init"},
        cwd=repo,
        env_extra={"POLYGLOT_SECRETS_DISABLED": "0"},
    )
    assert result.returncode == 1


def test_hook_fails_closed_on_empty_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=b"",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert b"empty stdin" in result.stderr


def test_fallback_interpreter_cannot_bypass_block():
    # `python guard.py || python3 guard.py`: the second run sees the consumed
    # stdin and must fail closed, so the chain cannot wave a block through.
    cmd = f'"{sys.executable}" "{SCRIPT}" || "{sys.executable}" "{SCRIPT}"'
    payload = {"path": "config.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'\n"}
    result = subprocess.run(
        cmd,
        input=json.dumps(payload).encode(),
        capture_output=True,
        shell=True,
        check=False,
    )
    assert result.returncode == 1


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


# --- main() in process: payload reading, cwd resolution, env gate ----------


def run_main(monkeypatch, payload, env=None):
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    if env:
        for key, value in env.items():
            monkeypatch.setenv(key, value)
    return secrets_guard.main()


def test_main_in_process_empty_stdin_fails_closed(monkeypatch):
    assert run_main(monkeypatch, "") == 1
    assert run_main(monkeypatch, "  \n ") == 1


def test_main_in_process_garbage_fails_open(monkeypatch):
    assert run_main(monkeypatch, "not json") == 0


def test_main_in_process_env_gate_requires_exact_1(monkeypatch):
    payload = json.dumps({"path": "c.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'"})
    assert run_main(monkeypatch, payload, {"POLYGLOT_SECRETS_DISABLED": "1"}) == 0
    assert run_main(monkeypatch, payload, {"POLYGLOT_SECRETS_DISABLED": "0"}) == 1


def test_main_in_process_write_payload_blocks(monkeypatch):
    payload = json.dumps({"path": "c.py", "content": "key = 'AKIAIOSFODNN7EXAMPLE'"})
    assert run_main(monkeypatch, payload) == 1
    assert run_main(monkeypatch, json.dumps({"path": "c.py", "content": "ok"})) == 0


def test_main_in_process_git_scan_uses_payload_cwd(monkeypatch, repo):
    stage(repo, "config.py", "key = 'AKIAIOSFODNN7EXAMPLE'\n")
    payload = json.dumps({"command": "git commit -m x", "cwd": str(repo)})
    assert run_main(monkeypatch, payload) == 1
    # not a git repo in the payload cwd: pass
    payload = json.dumps({"command": "git commit -m x", "cwd": str(repo / "nope")})
    assert run_main(monkeypatch, payload) == 0
    # non-git command: pass
    assert run_main(monkeypatch, json.dumps({"command": "ls"})) == 0


def test_payload_root_outside_repo(tmp_path):
    assert secrets_guard.payload_root({"cwd": str(tmp_path)}) is None
    assert secrets_guard.payload_root({}) is None or isinstance(
        secrets_guard.payload_root({}), str
    )


def test_diff_and_untracked_helpers_skip_lockfiles(repo):
    stage(repo, "package-lock.json", 'api_key = "abcdef1234567890abcd"\n')
    stage(repo, "main.py", "print('hi')\n")
    assert "api_key" not in secrets_guard.diff_text(str(repo), cached=True)
    assert "print" in secrets_guard.diff_text(str(repo), cached=True)
    (repo / "go.sum").write_text('api_key = "abcdef1234567890abcd"\n', encoding="utf-8")
    (repo / "notes.txt").write_text("hello\n", encoding="utf-8")
    text = secrets_guard.untracked_text(str(repo))
    assert "api_key" not in text
    assert "hello" in text
