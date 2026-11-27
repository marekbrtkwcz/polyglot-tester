---
name: auth-polyglot
description: Load this skill when implementing or reviewing authentication and authorization in JavaScript/TypeScript, Python, or Go — passwords, sessions, JWT, OAuth2/OIDC, MFA, and access control patterns across languages. For reviewing the crypto choices behind credential storage themselves (hashing, KDFs, parameter choices) prefer security-polyglot.
---

# Auth & Access Control (Polyglot)

## Passwords

- Hash with a memory-hard algorithm: **argon2id** (preferred) or bcrypt. Never MD5/SHA-1/SHA-256 for passwords.
- Per-language: Python `argon2-cffi` / `bcrypt`; Go `golang.org/x/crypto/argon2|bcrypt`; JS/TS `argon2` (npm) or `bcrypt`.
- Enforce a sane password policy (length floor, blocklist of common passwords) at the boundary, not just the client.

## Sessions & cookies

- Server-side sessions or signed tokens; cookie flags: `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict` for sensitive apps).
- Rotate the session ID on login and on privilege change; invalidate server-side on logout (a deleted cookie alone is not logout).
- Idle timeout + absolute timeout; cap concurrent sessions per user.

## JWT

- Verify signature, `exp`, `nbf`, `iss`, `aud` on every request; pin the expected algorithm (reject `none`, reject alg confusion).
- Fetch keys from JWKS with caching + refresh; never hardcode symmetric secrets in client-side JS.
- Keep tokens short-lived; use refresh tokens with rotation and reuse detection.

## OAuth2 / OIDC

- Use authorization code flow + PKCE for SPAs and mobile; client credentials only for service-to-service.
- Validate `state` and `nonce`; map identity-provider claims to your own user model at the boundary.
- Scope enforcement on the resource server, not only the auth server.

## Authorization

- Default deny: check permission on every request, object-level (IDOR) and function-level.
- RBAC for roles, ABAC when ownership matters; keep the policy in one place and test the matrix cross-role.
- Never trust the client for identity or role — read them from the verified token/session server-side.

## MFA

- TOTP (RFC 6238) with backup codes; WebAuthn/passkeys for phishing resistance.
- Step-up auth: require fresh MFA for sensitive actions (password change, payouts), not just login.

## Common failures to check in review

- Timing-safe comparison for tokens (`subtle.compare` / `hmac.compare_digest` / `ConstantTimeCompare`).
- Rate limiting + lockout on login, reset, and MFA endpoints; generic error messages (no user enumeration).
- Secure password reset: single-use, expiring token sent out-of-band; invalidate sessions after reset.

## Related

- `security-polyglot` — the broader hardening pass (headers, injection, secrets) around auth.
- Knowledge `security` — per-language checks for sessions, JWT, and crypto.
