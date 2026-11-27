---
name: golang-security
description: Load this skill when writing or reviewing security-sensitive Go code: input validation, SQL/command injection, path traversal, secrets, crypto, and HTTP security headers.
---

# Go Security

## Injection — treat all input as data

- **SQL**: always parameterized (`db.Query("SELECT ... WHERE id = $1", id)`). Never `fmt.Sprintf` into SQL. With ORMs, use their placeholder API, not raw string building.
- **OS commands**: prefer library APIs over `exec.Command`. If you must: `exec.Command("tool", arg1, arg2)` — never `exec.Command("sh", "-c", userInput)`.
- **Path traversal**: `filepath.Clean` + verify the result stays under the base dir:
  `dest := filepath.Join(base, userPath); if !strings.HasPrefix(dest, base+string(os.PathSeparator)) { reject }` — note `filepath.Join` already cleans, so check *after* joining. Or use `filepath.Localize` (Go 1.23+ / `io/fs` semantics).
- **HTML/templates**: `html/template` auto-escapes; `text/template` does not — never render user data with `text/template` into HTML.

## Secrets

- Never hardcode; read from env or a secret manager at startup, fail fast if missing.
- Never log secrets, tokens, or full request bodies with credentials. Redact in logs.
- `.env` files only locally; add to `.gitignore`; use different secrets per environment.

## Crypto

- Passwords: `golang.org/x/crypto/bcrypt` (or argon2id) — never MD5/SHA1 for passwords.
- TLS: `crypto/tls` with `MinVersion: tls.VersionTLS12`+; never `InsecureSkipVerify: true` in production code.
- Randomness: `crypto/rand`, never `math/rand` for tokens/IDs.
- Tokens: constant-time comparison (`subtle.ConstantTimeCompare`) if you must compare manually — better: use HMAC verification.

## HTTP handlers

- Set headers: `Content-Type` explicitly, `X-Content-Type-Options: nosniff`, and CSP where applicable.
- Limit request body size (`http.MaxBytesReader`), set server timeouts (`ReadHeaderTimeout` — slowloris).
- Validate and sanitize all inputs at the boundary; don't trust client-side validation.
- Run `govulncheck ./...` in CI; audit deps with `govulncheck` + `go mod verify`.

## Quick checklist for review

- [ ] Any string-built SQL / shell / file path from user input?
- [ ] Any secret in code, config committed, or logs?
- [ ] TLS verified, versions pinned?
- [ ] Auth checks on every handler route, not just the happy path?

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
