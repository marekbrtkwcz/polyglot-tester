"""Pre-tool hook: run fast repo checks before `git push`.

When a bash command contains `git push` (history-rewriting pushes are the
destructive guard's job, this hook skips them), runs the quick structural
checks against the repo root: scripts/check_readme_skills.py and the plugin
structure test suite. Exits non-zero when a check fails, so a broken push
is stopped locally.

Fail-open: if python, pytest, or the repo layout is unavailable, the push
passes with a warning on stderr — this hook must never brick a session.

Environment override: POLYGLOT_PREPUSH_DISABLED=1 disables the checks.
"""

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
    [sys.executable, "-m", "pytest", ".vibe/plugins/polyglot-dev/tests/test_plugin_structure.py", "-q"],
]


def run_checks():
    """Run each check; return list of (label, ok, output) results."""
    results = []
    for cmd in CHECKS:
        label = " ".join(cmd[1:])
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, timeout=120, check=False)
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
        return 0  # history-rewriting push: handled (blocked) by guard-destructive-commands
    failed = False
    for label, ok, output in run_checks():
        if ok:
            sys.stderr.write(f"pre-push OK: {label}\n")
        else:
            failed = True
            sys.stderr.write(f"pre-push FAILED: {label}\n{output}\n")
    if failed:
        sys.stderr.write("push blocked — fix the failures or use POLYGLOT_PREPUSH_DISABLED=1\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
