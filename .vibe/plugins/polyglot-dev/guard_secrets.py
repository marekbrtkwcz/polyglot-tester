"""Pre-tool guard: block committing or writing likely secrets.

When a bash command contains `git add` or `git commit`, scans the ADDED
lines of the staged diff — plus the unstaged diff for `git add` and
`git commit -a`, and untracked files for `git add` — for known secret
patterns (AWS keys, GitHub/Slack/Stripe tokens, AI-provider keys, private
key blocks, generic api_key/secret assignments). Removed (`-`) diff lines
are never scanned: a commit that deletes a leaked key must pass. Exits
non-zero with the findings on stderr.

When a `write_file`/`edit` payload carries the text about to be written
(`content`/`new_string`), scans that text too, so a secret is caught the
moment it would land in a file — not only at the next `git add`.

Fail-open on anything unreadable: the guard must never brick a session.
One deliberate exception: an EMPTY stdin fails closed — the hook runner
always sends a JSON payload, so empty stdin means this process is the
fallback interpreter in a `python x || python3 x` chain whose first run
already consumed the payload.

Git commands run in the session folder named in the hook payload's `cwd`
(plugin hooks are spawned from the plugin's read-only snapshot, not from
the project), resolved to the repository top level. Lockfiles matched by
SKIP_PATHS are excluded from the staged diff, the unstaged diff, and the
untracked files. Untracked files are only read for `git add` (a plain
`git commit` never includes them), and the unstaged diff is only scanned
for `git add` / `git commit -a` — a plain `git commit` stages nothing from
the worktree, so unstaged content cannot leak into it.

Environment override: POLYGLOT_SECRETS_DISABLED=1 disables every block
(only the exact value "1" counts).
"""

import json
import os
import re
import subprocess
import sys

try:
    from guard_destructive import extract_command, segment_after
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import extract_command, segment_after


SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b")),
    (
        "GitHub token",
        re.compile(
            r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|github_pat_[A-Za-z0-9_]{22,}"
        ),
    ),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Stripe key", re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{16,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("GitLab PAT", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20}\b")),
    ("SendGrid key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b")),
    (
        "Slack webhook",
        re.compile(
            r"\bhttps://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+\b"
        ),
    ),
    (
        "JWT",
        re.compile(
            r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b"
        ),
    ),
    (
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    ),
    (
        "generic secret assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|secret[_-]?key)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9/+_.~\-]{16,}[\"']?"
        ),
    ),
    (
        "OpenAI key",
        re.compile(
            r"\bsk-(?:proj|svcacct)-[A-Za-z0-9_\-]{20,}\b|\bsk-[A-Za-z0-9]{40,}\b"
        ),
    ),
    ("Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("HuggingFace token", re.compile(r"\bhf_[A-Za-z0-9]{30,}\b")),
]

GIT_TRIGGER = re.compile(r"\bgit\s+(?:add|commit)\b")
GIT_ADD = re.compile(r"\bgit\s+add\b")
GIT_COMMIT = re.compile(r"\bgit\s+commit\b")

SKIP_PATHS = re.compile(
    r"(?:^|/)(?:package-lock\.json|pnpm-lock\.yaml|yarn\.lock|go\.sum|Cargo\.lock|"
    r"uv\.lock|poetry\.lock|bun\.lockb?|.*\.min\.js|.*\.map)$"
)


def git_output(args, cwd=None):
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False,
            timeout=15,
        )
    except Exception:  # noqa: BLE001 - fail open
        return ""
    return result.stdout if result.returncode == 0 else ""


def payload_root(payload):
    """Repository top level for the session folder named in the payload.

    Plugin hooks are spawned from the plugin's read-only snapshot, so the
    process cwd is not the project: use the payload's `cwd` when present
    and resolve it to the git top level. None when not inside a work tree.
    """
    root = None
    if isinstance(payload, dict):
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd:
            root = cwd
    if not git_output(["rev-parse", "--is-inside-work-tree"], cwd=root).strip():
        return None
    return git_output(["rev-parse", "--show-toplevel"], cwd=root).strip() or None


def diff_text(root, cached):
    """ADDED lines of the staged or unstaged diff, excluding SKIP_PATHS.

    Only `+` lines (never `+++` headers) are returned: a commit that
    REMOVES a leaked secret shows it as a `-` line, and the file gets
    cleaner — that must pass, not block.
    """
    args = ["diff", "--cached"] if cached else ["diff"]
    paths = [
        p
        for p in git_output([*args, "--name-only"], cwd=root).splitlines()
        if p and not SKIP_PATHS.search(p)
    ]
    if not paths:
        return ""
    raw = git_output([*args, "--", *paths], cwd=root)
    return "\n".join(
        line
        for line in raw.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def untracked_text(root):
    """Contents of untracked files (excluding SKIP_PATHS), relative to root."""
    parts = []
    for path in git_output(
        ["ls-files", "--others", "--exclude-standard"], cwd=root
    ).splitlines():
        if not path or SKIP_PATHS.search(path):
            continue
        try:
            with open(
                os.path.join(root, path), encoding="utf-8", errors="replace"
            ) as fh:
                parts.append(fh.read())
        except OSError:
            continue
    return "\n".join(parts)


def commit_stages_worktree(command):
    """True when a `git commit` segment carries -a/--all.

    `git commit -a` stages worktree changes, so the unstaged diff is about
    to be committed and must be scanned; a plain `git commit` stages
    nothing from the worktree.
    """
    for match in GIT_COMMIT.finditer(command):
        for token in segment_after(command, match.end()).split():
            if token == "--all" or re.fullmatch(r"-[a-zA-Z]*a[a-zA-Z]*", token):
                return True
    return False


def collect_text(root, scan_untracked=False, scan_unstaged=False):
    """Staged added lines, plus unstaged added lines and/or untracked
    contents when asked (git add / git commit -a)."""
    parts = [diff_text(root, cached=True)]
    if scan_unstaged:
        parts.append(diff_text(root, cached=False))
    if scan_untracked:
        parts.append(untracked_text(root))
    return "\n".join(parts)


def find_secrets(text):
    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                masked = match.group(0)[:6] + "..." + match.group(0)[-4:]
                findings.append(f"{label}: line {lineno}: {masked}")
    return findings


CONTENT_KEYS = ("content", "new_string")
PATH_KEYS = ("path", "file_path")


def extract_written_strings(payload, keys=CONTENT_KEYS):
    """Collect the text a write/edit payload is about to write.

    `new_string` only, never `old_string`: an edit that replaces a secret
    with a clean value must pass.
    """
    found = []
    if not isinstance(payload, dict):
        return found
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str):
            found.append(value)
    for value in payload.values():
        found.extend(extract_written_strings(value, keys))
    return found


def extract_written_path(payload):
    """The target file path from a write/edit payload, when present."""
    if not isinstance(payload, dict):
        return None
    for key in PATH_KEYS:
        value = payload.get(key)
        if isinstance(value, str):
            return value
    for value in payload.values():
        found = extract_written_path(value)
        if found:
            return found
    return None


def scan_written_text(payload):
    """Secrets in the text a write/edit payload is about to write."""
    written = extract_written_strings(payload)
    if not written:
        return []
    path = extract_written_path(payload)
    if path and SKIP_PATHS.search(path.replace("\\", "/")):
        return []
    return find_secrets("\n".join(written))


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
    if os.environ.get("POLYGLOT_SECRETS_DISABLED") == "1":
        return 0

    payload = read_payload()
    if payload is EMPTY:
        sys.stderr.write(
            "blocked by polyglot-dev secrets guard: empty stdin, no payload to "
            "inspect (fail-closed)\n"
        )
        return 1
    if payload is None:
        return 0

    if isinstance(payload, dict):
        findings = scan_written_text(payload)
        if findings:
            sys.stderr.write(
                "blocked by polyglot-dev secrets guard: likely secret(s) in the file being written:\n"
                + "\n".join(f"  - {f}" for f in findings[:20])
                + "\nIf this is a false positive (test fixture, docs), set POLYGLOT_SECRETS_DISABLED=1.\n"
            )
            return 1

    command = extract_command(payload)
    if not command or not GIT_TRIGGER.search(command):
        return 0

    # Plugin hooks run from the plugin snapshot, not the project: resolve
    # the repository from the session folder named in the payload.
    root = payload_root(payload)
    if not root:
        return 0  # not inside a git repository: nothing to scan

    scan_unstaged = bool(GIT_ADD.search(command)) or commit_stages_worktree(command)
    findings = find_secrets(
        collect_text(
            root,
            scan_untracked=bool(GIT_ADD.search(command)),
            scan_unstaged=scan_unstaged,
        )
    )
    if findings:
        sys.stderr.write(
            "blocked by polyglot-dev secrets guard: likely secret(s) would be committed:\n"
            + "\n".join(f"  - {f}" for f in findings[:20])
            + "\nIf this is a false positive (test fixture, docs), set POLYGLOT_SECRETS_DISABLED=1.\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
