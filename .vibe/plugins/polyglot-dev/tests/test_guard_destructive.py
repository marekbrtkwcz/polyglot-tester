"""Tests for the guard_destructive.py pre-tool hook script."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "guard_destructive.py"

spec = importlib.util.spec_from_file_location("guard_destructive", SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def run_hook(payload, env_extra=None):
    """Run the script as the hook runner would: JSON on stdin, exit code out."""
    env = None
    if env_extra:
        env = {**os.environ, **env_extra}
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        check=False,
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
    result = run_hook({"command": "git push origin feature/x --force-with-lease"})
    assert result.returncode == 0


@pytest.mark.parametrize(
    "command",
    [
        "git push origin main --force",
        "git push --force origin main",
        "git push origin --force main",
        "git push origin feature/x --force-with-lease=",
        "git push origin feature/x --force-with-lease=false",
    ],
)
def test_force_push_token_spellings_blocked(command):
    assert guard.is_force_push(command) is True


@pytest.mark.parametrize(
    "command",
    [
        "git push origin feature/x",
        "git push origin feature/x --force-with-lease",
        "git push origin feature/x --force-with-lease=main:abc123",
        "git push --force-with-lease=refs/heads/main:abc123 origin feature/x",
        "git push origin main --force-with-lease",  # safe lease, but see protected-push tests
    ],
)
def test_force_push_allowed_spellings(command):
    assert guard.is_force_push(command) is False


# --- protected branches -------------------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "git push origin main",
        "git push origin master",
        "git push origin release/2.0",
        "git push main",
        "git push origin main --force-with-lease",
    ],
)
def test_protected_push_blocked(command):
    result = run_hook({"command": command})
    assert result.returncode == 1
    assert b"protected branch" in result.stderr


@pytest.mark.parametrize(
    "command",
    [
        "git push origin feature/new-ui",
        "git push origin HEAD:main",  # refspec form is not the branch shorthand
        "git push",
    ],
)
def test_non_protected_push_allowed(command):
    result = run_hook({"command": command})
    assert result.returncode == 0


def test_protected_push_allowed_via_env():
    result = run_hook(
        {"command": "git push origin main"},
        env_extra={"POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH": "1"},
    )
    assert result.returncode == 0


def test_guard_disabled_via_env():
    result = run_hook(
        {"command": "rm -rf /"},
        env_extra={"POLYGLOT_GUARD_DISABLED": "1"},
    )
    assert result.returncode == 0


# --- other destructive commands ------------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "find . -name '*.log' -delete",
        "find /var -type f -delete",
        "sudo find . -delete",
        "find . -name x -delete; echo done",
        "dd if=/dev/zero of=/dev/sda bs=1M",
        "sudo dd if=image.iso of=/dev/sdb",
        "chmod -R 777 /var/www",
        "chmod -R 755 /",
        "shred -n 3 secret.txt",
        "shred -u secret.txt",
        "truncate -s 0 big.log",
        "truncate -s 0B big.log",
    ],
)
def test_other_destructive_blocked(command):
    result = run_hook({"command": command})
    assert result.returncode == 1
    assert b"blocked by polyglot-dev guard" in result.stderr


@pytest.mark.parametrize(
    "command",
    [
        "find . -name '*.log'",
        "find . -name '*.log' -print",
        "dd if=input.iso of=backup.img",
        "dd if=x of=/dev/null",
        "chmod -R u+x scripts/",
        "chmod 644 file.txt",
        "echo 'shred' in a commit message without -m is a word",
        "truncate -s 1M sparse.img",
    ],
)
def test_other_destructive_allowed(command):
    result = run_hook({"command": command})
    assert result.returncode == 0


# --- property-based: rm flag combinations --------------------------------------


try:
    from hypothesis import given, strategies as st
except ImportError:
    given = None


if given is not None:

    @given(
        flags=st.lists(
            st.sampled_from(["-r", "-f", "-rf", "-fr", "-v", "-i", "--recursive", "--force", "--", "-"]),
            max_size=5,
        ),
        path=st.sampled_from(["build", "dist", ".", "/tmp/x"]),
    )
    def test_bulk_rm_matches_reference_model(flags, path):
        command = "rm " + " ".join(flags) + " " + path
        end_markers = [i for i, t in enumerate(flags) if t in ("--", "-")]
        end_of_options = min(end_markers) if end_markers else len(flags)
        option_tokens = flags[:end_of_options]

        def has(tokens, long_name, letter):
            for t in tokens:
                if t.startswith("--"):
                    if t == long_name:
                        return True
                elif t.startswith("-") and len(t) > 1 and letter in t[1:]:
                    return True
            return False

        expected = has(option_tokens, "--recursive", "r") and has(option_tokens, "--force", "f")
        assert guard.is_bulk_rm(command) is expected


# --- commit messages are data, not commands ----------------------------------


@pytest.mark.parametrize(
    "command",
    [
        'git commit -m "document why rm -rf is dangerous"',
        "git commit -m 'notes on git reset --hard pitfalls'",
        'git commit --message="chore: mention git stash drop in docs"',
        'git commit -m "rm -rf build && git clean -fd"',
    ],
)
def test_commit_message_mentioning_blocked_commands_allowed(command):
    result = run_hook({"command": command})
    assert result.returncode == 0


def test_quoted_command_not_after_dash_m_still_blocked():
    # Quoted strings outside -m ARE executed: the guard must still fire.
    result = run_hook({"command": 'bash -c "rm -rf build"'})
    assert result.returncode == 1


def test_destructive_command_next_to_commit_still_blocked():
    command = 'git add -A && git commit -m "docs" && git clean -fd'
    result = run_hook({"command": command})
    assert result.returncode == 1


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
        check=False,
    )
    assert result.returncode == 0


def test_hook_allows_normal_command():
    result = run_hook({"command": "npm test"})
    assert result.returncode == 0
