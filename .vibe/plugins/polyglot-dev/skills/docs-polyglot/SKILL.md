---
name: docs-polyglot
description: Load this skill when writing or updating project documentation in any language — READMEs, docstrings, ADRs, API docs, and changelogs that a new teammate can follow verbatim.
---

# Documentation (Polyglot)

## README structure

1. What it is (one paragraph) + link to deeper docs.
2. Quickstart: the shortest path from clone to running — commands copy-pasteable.
3. Development: how to run tests, lint, typecheck; how to add a feature (link to workflow).
4. Configuration: env vars table (name, required, default, description).
5. Links: architecture, API reference, changelog, contributing.

## Docstrings / code docs

- **JS/TS**: JSDoc/TSDoc on exported symbols — `@param`, `@returns`, `@throws`, `@example`; keep them next to the code so they rot together.
- **Python**: docstrings per convention (Google or NumPy style — pick one per repo); document raises, not returns obvious from type hints.
- **Go**: doc comments start with the identifier name ("`Foo` does ..."); package comment on one file; examples in `example_test.go` are compiled and run by `go test`.

## ADRs (Architecture Decision Records)

- One decision per file: `NNN-title.md` in `docs/adr/`; status (proposed/accepted/deprecated/superseded), context, decision, consequences (positive AND negative).
- Never rewrite history — supersede with a new ADR.

## API docs

- Generate from source where possible: OpenAPI spec for REST, proto comments for gRPC, TypeDoc/pdoc/mkdocstrings for code references.
- Keep examples tested (doctest / executed examples) so they don't lie.

## Changelog

- Keep a Changelog format: Added/Changed/Deprecated/Removed/Fixed/Security per version, newest first, `[Unreleased]` on top.
- Write for the reader who upgrades: breaking changes first and loud.

## Testing docs

- Follow the quickstart verbatim in a clean environment; every step that fails or assumes hidden knowledge is a bug in the docs — fix the doc, not the reader.
