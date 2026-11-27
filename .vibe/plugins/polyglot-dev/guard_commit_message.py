"""Pre-tool guard: block WIP commit messages.

When a bash command contains `git commit`, extracts the commit subject —
from the first -m/--message argument of that `git commit` segment (flags of
other tools in the same line, e.g. `pytest -m wip`, are ignored), or the
first line of a -F/--file message file — and exits non-zero when the
subject starts with WIP
(optionally bracketed: [WIP], (wip)). Everything else passes.

Fail-open on anything unreadable or unrecognized: the guard must never
brick a session. `git commit` without -m/-F opens an editor; nothing to
scan, so it passes. One deliberate exception: an EMPTY stdin fails
closed — the hook runner always sends a JSON payload, so empty stdin
means this process is the fallback interpreter in a `python x || python3 x`
chain whose first run already consumed the payload.

Environment override: POLYGLOT_WIP_DISABLED=1 disables every block
(only the exact value "1" counts).
"""

import json
import os
import re
import sys

try:
    from guard_destructive import extract_command, segment_after
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import extract_command, segment_after

GIT_COMMIT = re.compile(r"\bgit\s+commit\b")

# -m "msg" / -m 'msg' / -m msg / --message=... / --message "..."
# Combined short flags count too: -am "msg" is `git commit -a -m "msg"`.
MESSAGE_ARG = re.compile(
    r"(?:--message[= ]|-[a-zA-Z]*m\s+)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|\S+)"
)

# -F file / --file=file
MESSAGE_FILE = re.compile(r"(?:-F\s+|--file=)(\S+)")

WIP_SUBJECT = re.compile(
    r"^\s*[\[\(]?\s*wip\s*[\]\)]?\b|^\s*do not merge\b", re.IGNORECASE
)


def unquote(token):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    return token


def commit_segments(command):
    """Each `git commit` argument segment, cut at the next shell separator.

    `-m` flags of other tools in the same line (e.g. `pytest -m wip`) must
    not be read as a commit message.
    """
    for match in GIT_COMMIT.finditer(command):
        yield segment_after(command, match.end())


def subject_from_command(command):
    """First commit subject found in a `git commit` segment; None if absent."""
    for segment in commit_segments(command):
        messages = [unquote(m) for m in MESSAGE_ARG.findall(segment)]
        if messages:
            return messages[0]
    return None


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
    """True when any `git commit` segment carries a WIP subject.

    Per segment the first -m wins (later -m args are the body); -F files
    are consulted only when the segment has no -m.
    """
    if not GIT_COMMIT.search(command):
        return False
    for segment in commit_segments(command):
        messages = [unquote(m) for m in MESSAGE_ARG.findall(segment)]
        subject = messages[0] if messages else None
        if subject is None:
            for path in MESSAGE_FILE.findall(segment):
                subject = subject_from_file(path)
                if subject:
                    break
        if subject and WIP_SUBJECT.match(subject):
            return True
    return False


EMPTY = object()  # sentinel: stdin was empty, not merely unparseable


def read_payload():
    """Read the hook payload from stdin; EMPTY on empty stdin.

    Empty stdin fails closed in main(): the hook runner always sends a
    JSON payload, so empty stdin means this process is the fallback
    interpreter in a `python x || python3 x` chain re-running the guard
    after the payload was consumed — allowing that would bypass the
    guard. Unparseable non-empty input fails open.
    """
    raw = sys.stdin.read()
    if not raw.strip():
        return EMPTY
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001 - fail open
        return None


def run_payload(payload):
    """Run the WIP-commit check against an already-read payload."""
    if os.environ.get("POLYGLOT_WIP_DISABLED") == "1":
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


def main():
    payload = read_payload()
    if payload is EMPTY:
        sys.stderr.write("blocked: empty stdin, no payload to inspect (fail-closed)\n")
        return 1
    if payload is None:
        return 0
    return run_payload(payload)


if __name__ == "__main__":
    sys.exit(main())
