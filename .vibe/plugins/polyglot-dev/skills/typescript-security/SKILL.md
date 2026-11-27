---
name: typescript-security
description: Load this skill for JS/TS application security: XSS and injection, prototype pollution, unsafe deserialization, secrets handling, dependency auditing (npm audit), and safe HTTP headers. If the language is not JavaScript/TypeScript, prefer golang-security or python-security.
---

# Security in JS/TS

## Injection

- Never concatenate input into SQL/HTML/shell. Use parameterized queries (pg, Prisma, knex placeholders), template engines with auto-escaping, `execFile` over `exec`.
- XSS: escape on output; prefer `textContent` over `innerHTML`; sanitize HTML with DOMPurify when rich text is required; use CSP headers.
- No `eval`, `new Function`, or `child_process.exec` with user input.

## Prototype pollution

- `obj[userKey] = value` with user-controlled key is dangerous (`__proto__`, `constructor`).
- Use `Object.create(null)` or `Map` for user-keyed dictionaries; validate keys; sanitize with `Object.fromEntries` after filtering.

## Deserialization

- `JSON.parse` is safe; never `eval`-based parsing. Validate parsed data against a schema (zod, valibot, arktype, or hand-rolled guards) before use.

## Secrets

- Never commit secrets; use env vars + a secrets manager; add `.env` to `.gitignore`.
- Redact `Authorization`, cookies, API keys from logs.
- `npm audit` / `pnpm audit` in CI; Dependabot or Renovate for updates; check `osv-scanner` for transitive CVEs.

## HTTP hardening (server)

- Helmet (or manual headers): CSP, `X-Content-Type-Options: nosniff`, `X-Frame-Options`/frame-ancestors, HSTS.
- Validate and limit input: body size limits, rate limiting, request timeouts.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Strict/Lax`.

## Supply chain

- Lockfiles committed; review new dependencies (`npm view <pkg>`, check maintainer activity, weekly downloads).
- Be wary of install scripts (`--ignore-scripts` where feasible); pin versions for critical deps.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
