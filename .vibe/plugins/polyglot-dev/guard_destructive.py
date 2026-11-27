"""Pre-tool guard: block destructive shell commands before they run.

Reads the tool-call JSON on stdin, looks for the shell command string
(bash, Git Bash, or PowerShell) in common payload shapes, and exits
non-zero (with a reason on stderr) when the command matches a destructive
pattern. Unrecognized payloads pass through so the guard can never brick
the session. One deliberate exception: an EMPTY stdin fails closed.
The hook runner always sends a JSON payload on stdin, so empty stdin
means this process is the fallback interpreter in a
`python x || python3 x` chain whose first run already consumed the
payload — allowing that would bypass the guard.

Environment overrides (for deliberate, informed use; only the exact
value "1" counts, "0" or any other value does not disable):
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
    (
        r"\bdd\b[^;|&]*\bof=/dev/(?!null\b)\S*",
        "dd writing to a block device: destroys the disk",
    ),
    (
        r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*|--recursive)\b[^;|&]*\s777\b",
        "chmod -R 777: makes everything world-writable",
    ),
    (
        r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*|--recursive)\b[^;|&]*\s/\S*",
        "chmod -R on an absolute path: recursive permission change outside the project",
    ),
    (r"\bshred\s", "shred: overwrites file contents irreversibly"),
    (r"\btruncate\b[^;|&]*\s-s\s*0[a-zA-Z]*\b", "truncate -s 0: wipes the file"),
    (
        r"\bmkfs(?:\.[a-z0-9]+)?\b",
        "mkfs: formats a filesystem, destroying all data on it",
    ),
    (
        r"\b(?:wipefs|mkswap)\b[^;|&]*\s/dev/\S+",
        "wipefs/mkswap on a device: destroys signatures/data",
    ),
    (
        r"\d?>>?\s*/dev/(?:sd[a-z]|hd[a-z]|vd[a-z]|xvd[a-z]|nvme\d+n\d+|mmcblk\d+)\w*",
        "redirect to a block device: overwrites the disk",
    ),
    (
        r"\b(?:cp|mv|tee|install)\b[^;|&]*\s/dev/(?:sd[a-z]|hd[a-z]|vd[a-z]|xvd[a-z]|nvme\d+n\d+|mmcblk\d+)\w*(?:\s|$)",
        "copying a file onto a block device: overwrites the disk",
    ),
    (
        r"\bkubectl\s+delete\b[^;|&]*\s--all(?:-namespaces)?\b",
        "kubectl delete --all: removes every resource in scope",
    ),
    (
        r"\bgit\s+push\b[^;|&]*\s--delete\b",
        "git push --delete: removes a remote branch",
    ),
    (r"\bgit\s+push\b[^;|&]*\s(?::\S+)", "git push :ref: deletes the remote branch"),
    # PowerShell equivalents, for the `powershell` shell tool on native
    # Windows. Long parameters only: -Recurse without -Force passes, like
    # `rm -r` does; `rm -Recurse -Force` is already caught by is_bulk_rm.
    (
        r"(?i:\b(?:remove-item|del|erase|rd|ri)\b(?=[^;|&]*\s-[a-z]*recurse)(?=[^;|&]*\s-[a-z]*force))",
        "Remove-Item -Recurse -Force: irreversible bulk delete",
    ),
    (
        r"(?i:\bformat-volume\b)",
        "Format-Volume: formats the volume, destroying all data on it",
    ),
    (
        r"(?i:\bclear-disk\b[^;|&]*\s-remove[a-z]*)",
        "Clear-Disk -RemoveData: wipes the disk",
    ),
]

# git push to a protected branch, unless explicitly allowed via env.
# Token-based (see is_protected_push): a refspec's destination decides, so
# `HEAD:main` is caught while `--dry-run` never counts.
PROTECTED_REFS = ("main", "master")


def is_protected_ref(ref):
    """True for main, master, release/* (also under refs/heads/)."""
    ref = ref.removeprefix("refs/heads/")
    return ref in PROTECTED_REFS or ref.startswith("release/")


# Boundaries of a command within a shell line: stop scanning at the first
# separator, so "rm -r dir; echo f" is not misread as rm -rf.
SEGMENT_SPLIT = re.compile(r"[;&|]")

# PowerShell long single-dash parameters that must not be parsed as short
# option clusters: -Confirm contains both "r" and "f" as letters but is a
# confirmation prompt, not recursive+force.
LONG_RM_FLAGS = {"recurse": "r", "force": "f"}

# GNU rm short options (-d -f -i -I -P -r -R -v), lowercased: a single-dash
# token made only of these letters is an option cluster of ANY length
# (-rf, -vrf, -irfv, -dvrf), not a long parameter.
RM_SHORT_FLAGS = set("dfiprv")

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
    clusters of any length (-vrf, -irfv, -dvrf), --recursive --force, the
    uppercase GNU -R, the capitalized PowerShell -Recurse/-Force long
    parameters, and rm invocations inside a command chain.
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
                name = token[1:].lower()
                if name in LONG_RM_FLAGS:
                    # PowerShell long parameter, matched by its full word:
                    # -Recurse/-Force count, -Confirm/-WhatIf do not.
                    if LONG_RM_FLAGS[name] == "r":
                        recursive = True
                    else:
                        force = True
                elif all(ch in RM_SHORT_FLAGS for ch in name):
                    # short option cluster of any length: -rf, -fr, -vrf,
                    # -irfv, -dvrf, -Rf
                    if "r" in name:
                        recursive = True
                    if "f" in name:
                        force = True
                # other single-dash words are long parameters
                # (e.g. -Confirm): not flag clusters, ignore them
        if recursive and force:
            return True
    return False


def is_force_push(command):
    """True when any `git push` rewrites remote history.

    Token-based: --force and the short -f (also inside clusters like -vf)
    always block; --force-with-lease blocks only when the expected ref is
    missing or malformed (e.g. =false). The safe forms --force-with-lease
    and --force-with-lease=<ref>:<sha> pass.
    """
    for match in re.finditer(r"\bgit\s+push\b", command):
        segment = segment_after(command, match.end())
        for token in segment.split():
            if token == "--force":
                return True
            if re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", token):
                return True  # short force flag: -f, -vf, ...
            if token.startswith("--force-with-lease") and "=" in token:
                expected = token.split("=", 1)[1]
                if not expected or ":" not in expected or expected == "false":
                    return True
            # bare --force-with-lease is the safe form
    return False


def is_protected_push(command):
    """True when any `git push` targets main, master, or release/*.

    Token-based: non-option arguments after `git push` are the remote
    followed by refspecs (or just a refspec when no remote is given). A
    refspec's destination — the part after the colon — decides, so
    `git push origin HEAD:main` is caught while `git push origin main:tmp`
    is not. `--dry-run` changes nothing on the remote, so a dry-run push
    is never treated as protected.
    """
    if os.environ.get("POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH") == "1":
        return False
    for match in re.finditer(r"\bgit\s+push\b", command):
        tokens = segment_after(command, match.end()).split()
        if any(token == "--dry-run" for token in tokens):
            continue
        for token in tokens:
            if token.startswith(("-", ":")):
                continue  # option, or a `:ref` delete refspec (handled below)
            destination = token.split(":", 1)[1] if ":" in token else token
            if destination and is_protected_ref(destination):
                return True
    return False


EMPTY = object()  # sentinel: stdin was empty, not merely unparseable


def read_payload():
    """Read the hook payload from stdin.

    Returns EMPTY when stdin has no payload at all, None on unparseable
    input. Empty stdin fails closed in main(): the hook runner always
    sends a JSON payload, so empty stdin means this process is the
    fallback interpreter in a `python x || python3 x` chain re-running
    the guard after the payload was consumed — allowing that would
    bypass the guard. Unparseable non-empty input fails open.
    """
    raw = sys.stdin.read()
    if not raw.strip():
        return EMPTY
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001 - fail open, never brick the session
        return None


def main():
    if os.environ.get("POLYGLOT_GUARD_DISABLED") == "1":
        return 0

    payload = read_payload()
    if payload is EMPTY:
        sys.stderr.write(
            "blocked by polyglot-dev guard: empty stdin, no payload to inspect "
            "(fail-closed)\n"
        )
        return 1
    if payload is None:
        return 0  # never block on a payload we cannot read

    command = extract_command(payload)
    if not command:
        return 0

    scan_text = strip_commit_messages(command)

    checks = [
        (is_bulk_rm(scan_text), "rm with recursive+force: irreversible bulk delete"),
        (is_force_push(scan_text), "git push --force: rewrites remote history"),
        (
            is_protected_push(scan_text),
            "git push to a protected branch (main/master/release/*); set POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1 to allow",
        ),
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
