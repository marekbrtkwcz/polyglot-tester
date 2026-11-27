---
name: python-stay-updated
description: Load this skill when upgrading Python or its toolchain: version EOL schedule, reading release notes, safe migration between versions, and deprecation handling. If the language is not Python, prefer golang-stay-updated or typescript-stay-updated.
---

# Staying Updated (Python)

## Version lifecycle

- Check python.org/downloads for the support status: each minor (3.x) gets ~5 years (security fixes only after the first couple).
- Plan upgrades before a version goes security-only; CI matrix should cover all supported versions you ship on.
- `python_requires` in pyproject.toml is the floor, not the target.

## Reading a release (PEP + What's New)

- Read `docs.python.org/3/whatsnew/3.x.html` for the minor you're jumping to — not just the changelog.
- Watch the **Deprecated** and **Removed** sections: pending-deprecation warnings become errors on upgrade.
- Run the suite with `-W error::DeprecationWarning` on the new version in CI to surface what will break next.

## Safe upgrade routine

1. Upgrade locally first: `uv python install 3.13`, switch venv, run full tests + mypy + ruff.
2. Fix deprecations one category at a time so failures are attributable.
3. Update CI matrix, Docker base image (`python:3.13-slim`), `python_requires`, and pre-commit `default_language_version`.
4. Check dependency compatibility (many libs lag a release behind); `pip-audit` / `uv` can list outdated pins.

## Dependency upgrades

- `uv pip list --outdated` or `pip list --outdated`; read changelogs for major bumps of pinned libs (SQLAlchemy 2.x, pydantic v2, Django LTS jumps).
- Renovate/Dependabot PRs: review, run E2E, watch the error tracker after deploy.

## Official sources

- Releases & EOL: python.org/downloads · What's New: docs.python.org/3/whatsnew · PEP index: peps.python.org

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
