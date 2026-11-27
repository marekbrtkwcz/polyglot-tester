---
name: security
description: Security cheatsheet across JavaScript/TypeScript, Python, and Go: OWASP Top 10 mapped to concrete per-language checks, secrets handling, and the tools that automate each check.
display_name: Security
icon: shield
---

# Security Reference (Polyglot)

## OWASP Top 10 → per-language checks

| Risk | JS/TS | Python | Go |
| --- | --- | --- | --- |
| Injection (SQL/cmd/HTML) | parameterized queries, no `eval`, `execFile` over `exec`, DOMPurify for HTML | bound params, no `eval`/`pickle`/`yaml.unsafe_load`, `subprocess` list form | `database/sql` params, `exec.Command` args (never shell string), `html/template` auto-escapes |
| Broken access control | server-side check per request/object; never trust client role | decorators/mixins + tests cross-role | middleware + per-handler checks, `errors.Is` on authz |
| Crypto misuse | `crypto` web/node API, no homebrew | `cryptography` lib, argon2-cffi for passwords | `crypto/*` stdlib, x/crypto argon2/bcrypt |
| Secrets | env + manager, redaction in logs, npm audit | env + keyring/manager, bandit, pip-audit | env, never hardcode; gitleaks/govulncheck |
| SSRF | allowlist hosts, block private IPs, no redirect-follow | same; validate URL scheme | `net/url` parse + IP range check |
| Deserialization | `JSON.parse` + schema validation (zod/valibot) | pydantic validation, no pickle | `encoding/json` + validation |
| XSS | `textContent`, CSP, sanitize rich text | template auto-escape (Jinja/Django), `\|safe` carefully | `html/template` context-aware escaping |
| CSRF | SameSite cookies + CSRF tokens on state-changing forms | Django/Flask built-ins | SameSite + token middleware |
| Dependencies | `npm audit`, Dependabot, osv-scanner | `pip-audit`, bandit, Dependabot | `govulncheck`, Dependabot |
| Auth/session | HttpOnly+Secure+SameSite, JWT verify (alg pin, JWKS), argon2 | same; Django auth battle-tested | same; constant-time compare |

## Universal rules

- Validate all input at the boundary (type, length, allowlist); reject early.
- Least privilege everywhere: DB users, IAM roles, file permissions.
- Defense in depth: validation + parameterization + output encoding + CSP + monitoring.
- Log security events (login fail, access denied, password change) with correlation IDs; never log secrets/PII.
- Incident readiness: know how to rotate a leaked secret before you need to.

## Automated tools per language

- JS/TS: `npm audit`, `osv-scanner`, `semgrep`, `gitleaks`, `helmet` (headers), DOMPurify.
- Python: `bandit`, `pip-audit`, `semgrep`, `safety`, `gitleaks`.
- Go: `govulncheck`, `gosec`, `gitleaks`, `staticcheck` (includes some security checks).

## Official sources

- OWASP Top 10: owasp.org/Top10 · OWASP Cheat Sheet Series: cheatsheetseries.owasp.org · Web Security Academy: portswigger.net/web-security · semgrep: semgrep.dev · gitleaks: github.com/gitleaks/gitleaks
