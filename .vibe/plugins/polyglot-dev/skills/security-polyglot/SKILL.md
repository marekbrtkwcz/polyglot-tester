---
name: security-polyglot
description: Load this skill when writing or reviewing security-sensitive code in JavaScript/TypeScript, Python, or Go — injection, secrets, crypto, HTTP hardening, and dependency auditing across all three languages. When the task names one language prefer its golang-security, python-security, or typescript-security skill; for a focused dependency-vulnerability audit prefer dependency-audit.
---

# Security (Polyglot)

## Injection — treat all input as data

- **SQL**: parameterized queries only, in every language. Never string-build SQL (Go `fmt.Sprintf`, Python f-strings, JS/TS template literals).
- **Shell/OS commands**: argument lists, never a shell string with user input. Go `exec.Command("tool", arg)`, Python `subprocess.run([...])` without `shell=True`, JS/TS `execFile` over `exec`.
- **Path traversal**: resolve, then verify the result stays under the base dir — Go `filepath.Join` + prefix check (or `filepath.Localize`), Python `Path.resolve()` + `is_relative_to(BASE_DIR)`, JS/TS `path.resolve` + `startsWith(base + sep)`.
- **Templates**: auto-escaping engines only for HTML — Go `html/template`, Jinja2 `autoescape=True`, React/JSX escaping; never `text/template`, autoescape-off, or `innerHTML` with user data. Sanitize rich text with DOMPurify.
- **Deserialization**: JSON everywhere. Never `pickle`/`marshal` (Python), `eval`/`new Function` (JS/TS), or `text/template` into HTML (Go) on untrusted data. Validate parsed data against a schema (zod/valibot, pydantic).
- **Prototype pollution** (JS/TS): never `obj[userKey] = value` with user-controlled keys (`__proto__`, `constructor`) — use `Map` or `Object.create(null)`.
- **YAML** (Python): `yaml.safe_load` only.

## Secrets

- Never in code or git: env vars or a secret manager, fail fast at startup if missing.
- `.env` local only, gitignored; different secrets per environment.
- Redact tokens/cookies/API keys from logs in all languages; scan history with gitleaks/trufflehog. This repo's `guard-secrets-in-git` hook blocks secret patterns on `git add`/`git commit`.
- Rotate on suspicion.

## Crypto

- Passwords: argon2id (preferred) or bcrypt — never MD5/SHA-1/SHA-256 for passwords. Python `argon2-cffi`/`bcrypt`, Go `golang.org/x/crypto/argon2|bcrypt`, JS/TS `argon2`/`bcrypt` npm packages.
- Randomness for tokens/IDs: `secrets.token_urlsafe()` (Python), `crypto/rand` (Go), `crypto.randomBytes`/`crypto.randomUUID` (JS/TS) — never `random`/`math/rand`.
- TLS: verify certificates, minimum TLS 1.2 (Go `MinVersion`, Python default context, Node defaults) — never `InsecureSkipVerify`/`verify=False`/`rejectUnauthorized: false` in production.
- Token comparison: HMAC verification or constant-time compare — never plain string equality.

## HTTP hardening

- Security headers: CSP, `X-Content-Type-Options: nosniff`, `X-Frame-Options`/frame-ancestors, HSTS. JS/TS servers: Helmet; others: set manually.
- Limit request body size, set server read/header timeouts (slowloris), rate-limit sensitive routes.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`.
- Auth checks on every route, including object-level authorization (IDOR), not just login.

## Dependency auditing

- CI gate per language: `npm audit`/`osv-scanner` (JS/TS), `pip-audit`/`safety` (Python), `govulncheck ./...` (Go). See `dependency-audit`.
- Static security lint: `bandit -r src/` (Python); review new deps before adding (maintainer activity, downloads).
- Lockfiles committed; pin critical deps; be wary of install scripts.

## Review checklist

- [ ] Any string-built SQL/shell/path from user input?
- [ ] Any secret in code, committed config, or logs?
- [ ] TLS verified, versions pinned?
- [ ] Dependency audit + security lint green in CI?
- [ ] Auth on every route, object-level checks included?

## Per-language depth

`golang-security`, `python-security`, `typescript-security`; see also `auth-polyglot` for auth-specific controls.

## Related

- Knowledge `security` — the OWASP → per-language cheatsheet plus the audit pack's grep hunts and tool gates.
