---
name: release-and-changelog
description: Load this skill when preparing or cutting a release: semantic versioning, Keep a Changelog entries, tagging, and release notes from a diff.
---

# Release & Changelog

## Semantic versioning

Given MAJOR.MINOR.PATCH:

- **PATCH**: backwards-compatible bug fixes.
- **MINOR**: backwards-compatible new functionality.
- **MAJOR**: breaking changes.

Pre-1.0 (`0.x.y`): MINOR may include breaking changes; say so explicitly in the changelog.

## Keep a Changelog format

```markdown
## [1.2.0] - 2026-11-27

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

- Sections used: Added, Changed, Deprecated, Removed, Fixed, Security.
- `[Unreleased]` section on top collects changes between releases.
- Link versions at the bottom: `[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0`.

## Cutting a release

1. Move `[Unreleased]` content into a new `## [x.y.z] - <date>` section (date = release date, ISO format).
2. Bump the version everywhere it lives (package.json, pyproject.toml, go.mod module docs, plugin.json).
3. Run the full verification suite on the release commit.
4. Commit `Release vX.Y.Z`, then tag: `git tag -a vX.Y.Z -m "vX.Y.Z"` (annotated tags for releases).
5. Push the branch and the tag explicitly: `git push origin main && git push origin vX.Y.Z`.

## Release notes from a diff

- Group entries by audience: user-facing changes first, then operator/developer notes.
- Mark breaking changes loudly (`**BREAKING:**`).
- Every entry states the behavior change, not the activity (`Add X` not `Worked on X`).

## Rollback plan

- A release must be reversible: know the previous tag, keep deploy artifacts, document the rollback command before shipping.

## Related

- `git-workflow-polyglot` — the tagging and branch mechanics releases build on.
- `ci-cd-polyglot` — the workflow that ships and verifies the release tag.
- Knowledge `ci-cd` — release pipeline shape and diagnostics.
