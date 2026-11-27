"""Pre-tool guard: block committing or writing likely secrets.

When a bash command contains `git add` or `git commit`, scans the staged
diff, the unstaged diff, and untracked files for known secret patterns
(AWS keys, GitHub/Slack/Stripe tokens, private key blocks, generic
api_key/secret assignments). Exits non-zero with the findings on stderr.

When a `write_file`/`edit` payload carries the text about to be written
(`content`/`new_string`), scans that text too, so a secret is caught the
moment it would land in a file — not only at the next `git add`.

Fail-open on anything unreadable: the guard must never brick a session.

Environment override: POLYGLOT_SECRETS_DISABLED=1 disables every block.
"""

import json
import os
import re
import subprocess
import sys

try:
    from guard_destructive import extract_command
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import extract_command


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
]

GIT_TRIGGER = re.compile(r"\bgit\s+(?:add|commit)\b")

SKIP_PATHS = re.compile(
    r"(?:^|/)(?:package-lock\.json|pnpm-lock\.yaml|yarn\.lock|go\.sum|Cargo\.lock|.*\.min\.js)$"
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


def collect_text():
    """Staged diff + unstaged diff + untracked file contents."""
    parts = [
        git_output(["diff", "--cached"]),
        git_output(["diff"]),
    ]
    for path in git_output(["ls-files", "--others", "--exclude-standard"]).splitlines():
        if SKIP_PATHS.search(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                parts.append(fh.read())
        except OSError:
            continue
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


def main():
    if os.environ.get("POLYGLOT_SECRETS_DISABLED"):
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:  # noqa: BLE001 - fail open, never brick the session
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

    # Only scan when we are actually inside a git repository.
    if not git_output(["rev-parse", "--is-inside-work-tree"]).strip():
        return 0

    findings = find_secrets(collect_text())
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
