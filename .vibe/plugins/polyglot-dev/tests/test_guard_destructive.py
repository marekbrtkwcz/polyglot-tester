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


def assert_blocked(result, reason):
    """A blocked command exits 1 with the exact reason line on stderr."""
    assert result.returncode == 1
    assert result.stderr.startswith(b"blocked by polyglot-dev guard"), result.stderr
    expected = f"blocked by polyglot-dev guard: {reason}".encode()
    assert expected in result.stderr, (expected, result.stderr)


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
        "rm -Rf build",  # GNU uppercase-R spelling
        "rm -R -f build",
        "rm -Recurse -Force build",  # PowerShell long parameters
    ],
)
def test_bulk_rm_blocked(command):
    assert guard.is_bulk_rm(command) is True


# --- is_bulk_rm: allowed spellings ------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "rm build",  # single target, no flags
        "rm -f build.log",  # force without recursive
        "rm -r build",  # recursive without force
        "rm -- build",  # end of options, no flags
        "rm -r build; echo -f",  # -f belongs to echo, not rm
        "rm -r dir -- --force",  # after --, --force is a path
        "transform --force",  # rm is a substring, not a word
        "grep rm readme",  # rm as a plain argument
    ],
)
def test_bulk_rm_allowed(command):
    assert guard.is_bulk_rm(command) is False


# --- other blocked patterns --------------------------------------------------


@pytest.mark.parametrize(
    "command, reason",
    [
        ("git reset --hard HEAD~1", "git reset --hard: discards working tree"),
        ("git clean -fd", "git clean -f: deletes untracked files"),
        ("git push origin main --force", "git push --force: rewrites remote history"),
        ("git push --force-with-lease=false", "git push --force: rewrites remote history"),
        ("git stash drop", "git stash drop/clear: loses stashed work"),
        ("git stash clear", "git stash drop/clear: loses stashed work"),
    ],
)
def test_git_patterns_blocked(command, reason):
    assert_blocked(run_hook({"command": command}), reason)


def test_rm_rf_blocked_with_reason():
    assert_blocked(
        run_hook({"command": "rm -rf build"}),
        "rm with recursive+force: irreversible bulk delete",
    )


def test_force_with_lease_allowed():
    result = run_hook({"command": "git push origin feature/x --force-with-lease"})
    assert result.returncode == 0


# --- PowerShell equivalents (the powershell tool on native Windows) -----------


@pytest.mark.parametrize(
    "command, reason",
    [
        ("Remove-Item -Recurse -Force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("Remove-Item -Force -Recurse build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("Remove-Item build -Recurse -Force", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("Remove-Item -Path build -Recurse -Force", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("remove-item -recurse -force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("Remove-Item -Recurse -Force build; echo done", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("del -Recurse -Force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("erase -Recurse -Force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("rd -Recurse -Force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("ri -Recurse -Force build", "Remove-Item -Recurse -Force: irreversible bulk delete"),
        ("rm -Recurse -Force build", "rm with recursive+force: irreversible bulk delete"),
        ("Format-Volume -DriveLetter D", "Format-Volume: formats the volume, destroying all data on it"),
        ("Clear-Disk -Number 0 -RemoveData", "Clear-Disk -RemoveData: wipes the disk"),
        ("Clear-Disk -Number 0 -RemoveData -RemoveOEM", "Clear-Disk -RemoveData: wipes the disk"),
    ],
)
def test_powershell_destructive_blocked(command, reason):
    assert_blocked(run_hook({"command": command}), reason)


@pytest.mark.parametrize(
    "command",
    [
        "Remove-Item build",  # no flags
        "Remove-Item -Force build.log",  # force without recurse
        "Remove-Item -Recurse build",  # recurse without force, like `rm -r`
        "rm -Recurse build",  # alias, recurse only
        "Remove-Item -Recurse build; echo -Force",  # -Force belongs to echo
    ],
)
def test_powershell_near_misses_allowed(command):
    result = run_hook({"command": command})
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


PROTECTED_REASON = (
    "git push to a protected branch (main/master/release/*); "
    "set POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1 to allow"
)


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
    assert_blocked(run_hook({"command": command}), PROTECTED_REASON)


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
    "command, reason",
    [
        ("find . -name '*.log' -delete", "find -delete: irreversible bulk delete"),
        ("find /var -type f -delete", "find -delete: irreversible bulk delete"),
        ("sudo find . -delete", "find -delete: irreversible bulk delete"),
        ("find . -name x -delete; echo done", "find -delete: irreversible bulk delete"),
        ("dd if=/dev/zero of=/dev/sda bs=1M", "dd writing to a block device: destroys the disk"),
        ("sudo dd if=image.iso of=/dev/sdb", "dd writing to a block device: destroys the disk"),
        ("chmod -R 777 /var/www", "chmod -R 777: makes everything world-writable"),
        ("chmod -R 777 data", "chmod -R 777: makes everything world-writable"),
        ("chmod -R 755 /", "chmod -R on an absolute path: recursive permission change outside the project"),
        ("shred -n 3 secret.txt", "shred: overwrites file contents irreversibly"),
        ("shred -u secret.txt", "shred: overwrites file contents irreversibly"),
        ("truncate -s 0 big.log", "truncate -s 0: wipes the file"),
        ("truncate -s 0B big.log", "truncate -s 0: wipes the file"),
    ],
)
def test_other_destructive_blocked(command, reason):
    assert_blocked(run_hook({"command": command}), reason)


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
            st.sampled_from(
                [
                    "-r",
                    "-f",
                    "-rf",
                    "-fr",
                    "-v",
                    "-i",
                    "--recursive",
                    "--force",
                    "--",
                    "-",
                ]
            ),
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

        expected = has(option_tokens, "--recursive", "r") and has(
            option_tokens, "--force", "f"
        )
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


# --- mkfs / block-device writes / kubectl --all / push --delete -------------


@pytest.mark.parametrize(
    "command, reason",
    [
        ("mkfs /dev/sda1", "mkfs: formats a filesystem, destroying all data on it"),
        ("mkfs.ext4 /dev/nvme0n1p2", "mkfs: formats a filesystem, destroying all data on it"),
        ("sudo mkfs.xfs /dev/sdb", "mkfs: formats a filesystem, destroying all data on it"),
        ("wipefs -a /dev/sda", "wipefs/mkswap on a device: destroys signatures/data"),
        ("mkswap /dev/sda3", "wipefs/mkswap on a device: destroys signatures/data"),
        ("cat os.img > /dev/sdb", "redirect to a block device: overwrites the disk"),
        ("echo data >> /dev/nvme0n1", "redirect to a block device: overwrites the disk"),
        ("dd if=iso of=/dev/sdc bs=4M", "dd writing to a block device: destroys the disk"),
        ("cp backup.img /dev/sda", "copying a file onto a block device: overwrites the disk"),
        ("kubectl delete --all pods", "kubectl delete --all: removes every resource in scope"),
        ("kubectl delete all --all-namespaces", "kubectl delete --all: removes every resource in scope"),
        ("kubectl delete deployment x -n prod --all", "kubectl delete --all: removes every resource in scope"),
        ("git push --delete origin feature", "git push --delete: removes a remote branch"),
        ("git push origin --delete feature", "git push --delete: removes a remote branch"),
        ("git push origin :main", "git push :ref: deletes the remote branch"),
    ],
)
def test_new_destructive_commands_blocked(command, reason):
    assert_blocked(run_hook({"command": command}), reason)


@pytest.mark.parametrize(
    "command",
    [
        "echo hi > /dev/null",
        "cat log 2> /dev/null",
        "dd if=file of=backup.img",  # regular file output is fine
        "kubectl delete pod my-pod",
        "kubectl delete pod my-pod -n dev",
        "git push origin main:feature",  # local:remote push is not a delete
        "git push origin feature",
        "git push --force-with-lease origin feature",
    ],
)
def test_new_near_misses_allowed(command):
    result = run_hook({"command": command})
    assert result.returncode == 0, command


# --- payload key priority: the right string must win ------------------------


@pytest.mark.parametrize(
    "payload",
    [
        {"description": "rm -rf build", "command": "ls"},
        {"description": "rm -rf build", "cmd": "ls"},
        {"z": "rm -rf build", "input": {"command": "ls"}},
        {"z": "rm -rf build", "arguments": {"command": "ls"}},
        {"z": "rm -rf build", "args": {"command": "ls"}},
        {"z": "rm -rf build", "tool_input": {"command": "ls"}},
        {"z": "rm -rf build", "toolInput": {"command": "ls"}},
    ],
)
def test_payload_key_priority_keeps_safe_command_first(payload):
    # the named command key wins over a sibling string that merely mentions
    # a destructive command
    result = run_hook(payload)
    assert result.returncode == 0, payload


def test_tool_input_preferred_over_tool_value():
    result = run_hook({"tool": "bash", "tool_input": {"command": "rm -r -f build"}})
    assert result.returncode == 1


def test_payloads_without_command_pass():
    assert run_hook({}).returncode == 0
    assert run_hook({"count": 5}).returncode == 0


def test_filename_containing_flag_letters_is_not_a_flag():
    # "draft.txt" contains both r and f; a recursive-only rm stays allowed
    result = run_hook({"command": "rm -r draft.txt"})
    assert result.returncode == 0
