---
name: project-structure
description: Load this skill when starting or reorganizing a project in JavaScript/TypeScript, Python, or Go — standard layout, packaging, toolchain, and lint/format gates a new teammate can follow. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for that stack's layout and toolchain.
---

# Project Structure

- Pick the standard layout for the ecosystem; don't invent a new one.
- Toolchain gates (lint, format, typecheck) wired into pre-commit and CI, and able to fail.
- Config lives at the root and is documented; the README takes a new teammate from zero to a green test run.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | standard layout, package naming, code style, modern Go idioms, documentation conventions |
| Python | `references/python.md` | src layout, pyproject.toml, uv/venv, ruff, packaging, pre-commit hooks |
| JavaScript/TypeScript | `references/ts.md` | package.json hygiene, tsconfig, monorepos (workspaces/Nx/Turborepo), lint/format gates, folder conventions |
