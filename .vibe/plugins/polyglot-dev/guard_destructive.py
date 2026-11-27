"""Pre-tool guard: block destructive shell commands before they run.

Reads the tool-call JSON on stdin, looks for the bash command string in
common payload shapes, and exits non-zero (with a reason on stderr) when the
command matches a destructive pattern. Unrecognized payloads pass through so
the guard can never brick the session.

Environment overrides (for deliberate, informed use):
  POLYGLOT_GUARD_DISABLED=1              disable every block
  POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1  allow push to main/master/release/*
"""

import json
import os
import re
import sys

BLOCKED_PATTERNS = [
    (r"\bgit\s+reset\s+--hard", "git reset --hard: discards working tree"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean -f: deletes untracked files"),
    (r"\bgit\s+stash\s+(drop|clear)", "git stash drop/clear: loses stashed work"),
    (r"\bfind\b[^;|&]*\s--?delete\b", "find -delete: irreversible bulk delete"),
    (r"\bdd\b[^;|&]*\bof=/dev/(?!null\b)\S*", "dd writing to a block device: destroys the disk"),
    (r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*|--recursive)\b[^;|&]*\s777\b", "chmod -R 777: makes everything world-writable"),
    (r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*|--recursive)\b[^;|&]*\s/\S*", "chmod -R on an absolute path: recursive permission change outside the project"),
    (r"\bshred\s", "shred: overwrites file contents irreversibly"),
    (r"\btruncate\b[^;|&]*\s-s\s*0[a-zA-Z]*\b", "truncate -s 0: wipes the file"),
]

# git push to a protected branch, unless explicitly allowed via env.
PROTECTED_PUSH = re.compile(
    r"\bgit\s+push\b[^;|&]*\s(?:\S+\s+)?(?:main|master|release/\S+)(?:\s|$)"
)

# Boundaries of a command within a shell line: stop scanning at the first
# separator, so "rm -r dir; echo f" is not misread as rm -rf.
SEGMENT_SPLIT = re.compile(r"[;&|]")

# Quoted strings passed to `git commit -m` / `--message=` are data, never
# executed: strip them so a commit message that merely mentions a blocked
# command does not trip the guard. Quoted strings elsewhere (e.g.
# `bash -c "..."`) ARE executed and must stay in the scanned text.
COMMIT_MESSAGE = re.compile(
    r"(-m\s+|--message=)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')"
)


def extract_command(payload):
    """Find the command string in an unknown JSON shape."""
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return None
    for key in ("command", "cmd"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    for key in ("input", "arguments", "args", "tool_input", "toolInput"):
        found = extract_command(payload.get(key))
        if found:
            return found
    for value in payload.values():
        found = extract_command(value)
        if found:
            return found
    return None


def strip_commit_messages(command):
    """Remove commit-message payloads from a command before scanning it."""
    return COMMIT_MESSAGE.sub(r"\1", command)


def segment_after(command, start):
    """The part of the command after `start`, cut at the next shell separator."""
    return SEGMENT_SPLIT.split(command[start:], maxsplit=1)[0]


def is_bulk_rm(command):
    """True when any rm invocation combines recursive and force.

    Catches every flag spelling: -rf, -fr, -r -f, -fr --force, -r dir -f,
    --recursive --force, and rm invocations inside a command chain.
    """
    for match in re.finditer(r"\brm\b", command):
        segment = segment_after(command, match.end())
        recursive = False
        force = False
        for token in segment.split():
            if token in ("-", "--"):
                break  # end of options: everything after is a path
            if token.startswith("--"):
                if token == "--recursive":
                    recursive = True
                elif token == "--force":
                    force = True
            elif token.startswith("-") and len(token) > 1:
                if "r" in token[1:]:
                    recursive = True
                if "f" in token[1:]:
                    force = True
        if recursive and force:
            return True
    return False


def is_force_push(command):
    """True when any `git push` rewrites remote history.

    Token-based: --force always blocks; --force-with-lease blocks only when
    the expected ref is missing or malformed (e.g. =false). The safe forms
    --force-with-lease and --force-with-lease=<ref>:<sha> pass.
    """
    for match in re.finditer(r"\bgit\s+push\b", command):
        segment = segment_after(command, match.end())
        for token in segment.split():
            if token == "--force":
                return True
            if token.startswith("--force-with-lease") and "=" in token:
                expected = token.split("=", 1)[1]
                if not expected or ":" not in expected or expected == "false":
                    return True
            # bare --force-with-lease is the safe form
    return False


def is_protected_push(command):
    """True when `git push` targets main, master, or release/* explicitly."""
    if os.environ.get("POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH"):
        return False
    return bool(PROTECTED_PUSH.search(command))


def main():
    if os.environ.get("POLYGLOT_GUARD_DISABLED"):
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:  # noqa: BLE001 - fail open, never brick the session
        return 0  # never block on a payload we cannot read

    command = extract_command(payload)
    if not command:
        return 0

    scan_text = strip_commit_messages(command)

    checks = [
        (is_bulk_rm(scan_text), "rm with recursive+force: irreversible bulk delete"),
        (is_force_push(scan_text), "git push --force: rewrites remote history"),
        (is_protected_push(scan_text), "git push to a protected branch (main/master/release/*); set POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1 to allow"),
    ]
    for pattern, reason in BLOCKED_PATTERNS:
        checks.append((bool(re.search(pattern, scan_text)), reason))

    for hit, reason in checks:
        if hit:
            sys.stderr.write(
                f"blocked by polyglot-dev guard: {reason}\ncommand: {scan_text[:500]}\n"
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
