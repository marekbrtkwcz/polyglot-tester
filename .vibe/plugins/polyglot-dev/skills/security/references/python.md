# Python Security

## Never trust input — injection classes

- **SQL**: parameterized queries only — `cursor.execute("SELECT ... WHERE id = %s", (user_id,))` (psycopg) or `:name` (SQLAlchemy). Never f-strings into SQL.
- **eval/exec**: never on user input. If you need dynamic config, use `ast.literal_eval` for literals only.
- **pickle**: never unpickle untrusted data — it executes arbitrary code. Use JSON. (Same for `marshal`, `shelve` on untrusted files.)
- **YAML**: `yaml.safe_load` only — `yaml.load` without Loader is unsafe (arbitrary object construction).
- **Shell**: `subprocess.run(["tool", arg], ...)` with a list — never `shell=True` with user input.
- **Path traversal**: `Path(user_input).resolve()` then verify `resolved.is_relative_to(BASE_DIR)` (3.9+) — don't string-concatenate paths from input.
- **Templates**: Jinja2 `autoescape=True` for HTML; never render user data with autoescape off.

## Secrets

- Env vars or a secret manager (never in code/git): `os.environ["API_KEY"]` with fail-fast at startup.
- `.env` only locally via `python-dotenv`, gitignored; different secrets per env.
- Redact secrets in logs (`logging.Filter` or structlog processor); never log request bodies with tokens.
- Rotate on suspicion; scan history with `gitleaks` / `trufflehog`.

## Dependencies

- `pip-audit` or `safety check` in CI; pin versions (`requirements.txt` hashes or `uv.lock`).
- `bandit -r src/` for static security linting (catches eval, pickle, shell=True, weak crypto).

## Crypto

- Passwords: `bcrypt`/`argon2-cffi` (via `passlib` or directly) — never hashlib for passwords.
- Tokens: `secrets.token_urlsafe()` — never `random` module for security values.
- TLS: `ssl` default context; verify certs (never `verify=False` in prod).

## HTTP (FastAPI/Django/Flask)

- Validate input with pydantic/models at the boundary; set body size limits; security headers (CSP, `X-Content-Type-Options: nosniff`).
- Auth on every route dependency; check object-level authorization (IDOR), not just login.

## Review checklist

- [ ] Any string-built SQL / eval / pickle / shell=True on input?
- [ ] Paths from user input sanitized?
- [ ] Secrets out of code, logs, and git?
- [ ] bandit + pip-audit green in CI?

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
