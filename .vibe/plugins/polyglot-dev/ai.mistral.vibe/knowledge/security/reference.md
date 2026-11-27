# Security Audit Pack Reference

Companion to the security knowledge: ripgrep hunts that surface the
dangerous patterns across all three languages, and the tool commands that
automate the pass. Grep narrows the field; a human decides.

## Live pattern hunts

- TLS verification disabled (any language):
  `rg "InsecureSkipVerify|verify=False|rejectUnauthorized: false"`
- Dynamic code execution on untrusted data:
  `rg "eval\(|new Function\(|pickle\.loads"`
- Shell built from strings:
  `rg "shell=True|child_process\.exec\(|exec\.Command\(.{0,60}\+"`
- String-built SQL:
  `rg "(SELECT |INSERT INTO|UPDATE ).{0,60}(\+|\{|%s\")"`
- Hardcoded secrets (heuristic, expect false positives):
  `rg -i "(api_key|secret|password|token).{0,24}[\"':=][A-Za-z0-9_\-]{16,}"`
- Weak password hashing: `rg "(md5|sha1)\(" src/` — then check whether the
  input is a password (those need argon2id/bcrypt).

## Automated gates

- JS/TS dependencies: `npm audit --omit=dev` and
  `osv-scanner --lockfile package-lock.json`.
- Python: `pip-audit` plus `bandit -r src/`.
- Go: `govulncheck ./...` plus `gosec ./...`.
- Secrets in history: `gitleaks detect --source .`
- Cross-language rules: `semgrep --config=auto`.
- Pre-push, this repo also blocks secret patterns via its
  `polyglot-dev-guards` hook — the scan above is the CI-side net.

## Live HTTP header check

- `curl -sI https://host` — then look for `content-security-policy`,
  `strict-transport-security`, `x-frame-options`/`frame-ancestors`,
  `x-content-type-options: nosniff`; their absence is the finding.

## Triage order when the gates scream

- Exploitable from the Internet with user input → blocker, fix before merge.
- Secrets/credentials found → rotate first, then remove from history —
  deleting the file does not un-leak the commits.
- Dependency CVEs: check reachability — an unused package's critical CVE
  is urgent for the build, not necessarily for users.
