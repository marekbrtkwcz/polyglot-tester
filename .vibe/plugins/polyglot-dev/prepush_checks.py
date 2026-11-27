"""Pre-tool hook: run fast repo checks before `git push`.

When a shell command contains `git push` (history-rewriting pushes are the
destructive guard's job, this hook skips them), runs the quick structural
checks against the repo root: scripts/check_readme_skills.py and the plugin
structure test suite. Exits non-zero when a check fails, so a broken push
is stopped locally.

The checks belong to this plugin's own repository. The hook looks at the
session folder named in the hook payload (falling back to its own location
when the payload has none) and stays a silent no-op anywhere else:
installed into another project it adds no noise and blocks nothing.

Fail-open: if python, pytest, or the repo layout is unavailable, the push
passes with a warning on stderr — this hook must never brick a session.

Environment override: POLYGLOT_PREPUSH_DISABLED=1 disables the checks.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    from guard_destructive import extract_command
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import extract_command

GIT_PUSH = re.compile(r"\bgit\s+push\b")
FORCE_PUSH = re.compile(r"--force(?:-with-lease(?:=\S*)?)?|--delete|\s:\S+")

REPO_ROOT = Path(__file__).resolve().parents[3]
CHECKS = [
    [sys.executable, "scripts/check_readme_skills.py"],
    [
        sys.executable,
        "-m",
        "pytest",
        ".vibe/plugins/polyglot-dev/tests/test_plugin_structure.py",
        "-q",
    ],
]
# Both must exist under the repo root for the checks to run; any other
# project that installs the plugin lacks them, and the hook stays quiet.
OWN_REPO_MARKERS = (
    "scripts/check_readme_skills.py",
    ".vibe/plugins/polyglot-dev/tests/test_plugin_structure.py",
)


def payload_cwd(payload):
    """The session folder named in the hook payload, if present."""
    if isinstance(payload, dict):
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd:
            return Path(cwd)
    return None


def is_own_repo(root):
    """True when `root` looks like this plugin's own repository."""
    return all((Path(root) / marker).is_file() for marker in OWN_REPO_MARKERS)


def pytest_available():
    """True when pytest is importable by this interpreter."""
    return importlib.util.find_spec("pytest") is not None


def run_checks(repo_root):
    """Run each check; return list of (label, ok, output) results."""
    results = []
    for cmd in CHECKS:
        label = " ".join(cmd[1:])
        if "pytest" in cmd and not pytest_available():
            results.append((label, True, "skipped (pytest not installed)"))
            continue
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=repo_root,
                timeout=120,
                check=False,
            )
            output = (proc.stdout + proc.stderr).strip()
            results.append((label, proc.returncode == 0, output))
        except Exception as exc:  # noqa: BLE001 - fail open
            results.append((label, True, f"skipped ({exc})"))
    return results


def main():
    if os.environ.get("POLYGLOT_PREPUSH_DISABLED") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001 - fail open
        return 0
    command = extract_command(payload)
    if not command or not GIT_PUSH.search(command):
        return 0
    if FORCE_PUSH.search(command):
        return (
            0  # history-rewriting push: handled (blocked) by guard-destructive-commands
        )
    repo_root = payload_cwd(payload) or REPO_ROOT
    if not is_own_repo(repo_root):
        return 0  # another project: the checks are not ours to run
    failed = False
    for label, ok, output in run_checks(repo_root):
        if ok:
            sys.stderr.write(f"pre-push OK: {label}\n")
        else:
            failed = True
            sys.stderr.write(f"pre-push FAILED: {label}\n{output}\n")
    if failed:
        sys.stderr.write(
            "push blocked — fix the failures or use POLYGLOT_PREPUSH_DISABLED=1\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
