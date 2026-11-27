"""Pre-tool guard: block destructive shell commands before they run.

Reads the tool-call JSON on stdin, looks for the bash command string in
common payload shapes, and exits non-zero (with a reason on stderr) when the
command matches a destructive pattern. Unrecognized payloads pass through so
the guard can never brick the session.
"""

import json
import re
import sys

BLOCKED_PATTERNS = [
    (r"\bgit\s+reset\s+--hard", "git reset --hard: discards working tree"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean -f: deletes untracked files"),
    (r"\bgit\s+push[^\n]*\s--force(?!\S)(?!-with-lease)", "git push --force: rewrites remote history"),
    (r"\bgit\s+push[^\n]*\s--force-with-lease=(?![^\s=]+:[^\s=]+)", "git push --force-with-lease with no/bad expected ref: rewrites remote history"),
    (r"\bgit\s+stash\s+(drop|clear)", "git stash drop/clear: loses stashed work"),
]

# Boundaries of a command within a shell line: stop scanning rm flags at the
# first separator, so "rm -r dir; echo f" is not misread as rm -rf.
RM_SEGMENT_SPLIT = re.compile(r"[;&|><`$(\s]")


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


# Boundaries of a command within a shell line: stop scanning rm flags at the
# first separator, so "rm -r dir; echo f" is not misread as rm -rf.
RM_SEGMENT_SPLIT = re.compile(r"[;&|]")

# Quoted strings passed to `git commit -m` / `--message=` are data, never
# executed: strip them so a commit message that merely mentions a blocked
# command does not trip the guard. Quoted strings elsewhere (e.g.
# `bash -c "..."`) ARE executed and must stay in the scanned text.
COMMIT_MESSAGE = re.compile(
    r"(-m\s+|--message=)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')"
)


def strip_commit_messages(command):
    """Remove commit-message payloads from a command before scanning it."""
    return COMMIT_MESSAGE.sub(r"\1", command)


def is_bulk_rm(command):
    """True when any rm invocation in the command combines recursive and force.

    Catches every flag spelling: -rf, -fr, -r -f, -fr --force, -r dir -f,
    --recursive --force, and rm invocations inside a command chain.
    """
    for match in re.finditer(r"\brm\b", command):
        # Only scan the rm segment, cut at the next shell separator.
        segment = RM_SEGMENT_SPLIT.split(command[match.end():], maxsplit=1)[0]
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


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0  # never block on a payload we cannot read

    command = extract_command(payload)
    if not command:
        return 0

    scan_text = strip_commit_messages(command)

    if is_bulk_rm(scan_text):
        sys.stderr.write(
            "blocked by polyglot-dev guard: rm with recursive+force: "
            "irreversible bulk delete\ncommand: %s\n" % scan_text[:500]
        )
        return 1

    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, scan_text):
            sys.stderr.write(
                "blocked by polyglot-dev guard: %s\ncommand: %s\n"
                % (reason, command[:500])
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
