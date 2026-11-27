"""Pre-tool guard: block WIP commit messages.

When a bash command contains `git commit`, extracts the commit subject —
from the first -m/--message argument, or the first line of a -F/--file
message file — and exits non-zero when the subject starts with WIP
(optionally bracketed: [WIP], (wip)). Everything else passes.

Fail-open on anything unreadable or unrecognized: the guard must never
brick a session. `git commit` without -m/-F opens an editor; nothing to
scan, so it passes.

Environment override: POLYGLOT_WIP_DISABLED=1 disables every block.
"""

import json
import os
import re
import sys

try:
    from guard_destructive import extract_command
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import extract_command

GIT_COMMIT = re.compile(r"\bgit\s+commit\b")

# -m "msg" / -m 'msg' / -m msg / --message=... / --message "..."
MESSAGE_ARG = re.compile(
    r"(?:-m\s+|--message[= ])(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|\S+)"
)

# -F file / --file=file
MESSAGE_FILE = re.compile(r"(?:-F\s+|--file=)(\S+)")

WIP_SUBJECT = re.compile(r"^\s*\[?\s*wip\s*\]?\b|^\s*do not merge\b", re.IGNORECASE)


def unquote(token):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    return token


def subject_from_command(command):
    """Best-effort commit subject from -m args (first wins); None if absent."""
    messages = [unquote(m) for m in MESSAGE_ARG.findall(command)]
    return messages[0] if messages else None


def subject_from_file(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.strip():
                    return line.strip()
    except OSError:
        return None
    return None


def is_wip_commit(command):
    """True when a git commit in the command carries a WIP subject."""
    if not GIT_COMMIT.search(command):
        return False
    subject = subject_from_command(command)
    if subject is None:
        for path in MESSAGE_FILE.findall(command):
            subject = subject_from_file(path)
            if subject:
                break
    if subject is None:
        return False
    return bool(WIP_SUBJECT.match(subject))


def main():
    if os.environ.get("POLYGLOT_WIP_DISABLED") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001 - fail open
        return 0
    command = extract_command(payload)
    if not command:
        return 0
    if is_wip_commit(command):
        sys.stderr.write(
            "blocked: commit subject starts with WIP — finish the work or use "
            "POLYGLOT_WIP_DISABLED=1 to override\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
