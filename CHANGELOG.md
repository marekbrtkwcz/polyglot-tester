# Changelog

All notable changes to the polyglot-dev plugin are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic.

## [Unreleased]

### Added

- `tests/test_plugin_structure.py`: CI-validated plugin invariants — every
  skill dir has a `SKILL.md` with `name`/`description` frontmatter matching
  the directory (kebab-case, unique), `plugin.json` is valid with semver
  version, agent TOMLs parse with snake_case keys only, every knowledge
  folder has `KNOWLEDGE.md`, `hooks.toml` is well-formed. CI job renamed to
  `tests` since it now runs guard + structure suites.
- Four cross-language skills: `database-polyglot`, `api-design-polyglot`,
  `observability-polyglot`, `docs-polyglot`.
- Three new agents: `security-auditor` (read-only), `doc-writer`,
  `refactorer` (test-first, small green steps).
- Three new knowledge folders: `testing`, `docker`, `databases`.
- Guard blocks more destructive commands: `mkfs`, `wipefs`/`mkswap` on a
  device, redirects and `cp`/`mv`/`tee` onto block devices (`/dev/sd*`,
  `/dev/nvme*`, ...), `kubectl delete --all[--namespaces]`, and
  `git push --delete` / `git push :ref`. 23 new test cases.

## [1.3.0] - 2026-11-27

### Added

- Seven Go-specific skills covering the depth of the samber/cc-skills-golang
  collection, written natively for this plugin: `golang-error-handling`,
  `golang-concurrency`, `golang-testing-advanced`, `golang-security`,
  `golang-performance`, `golang-project-structure`,
  `golang-libraries-and-patterns`.
- Ten more Go skills completing the topic range: `golang-design-and-data`,
  `golang-refactoring`, `golang-stay-updated`, `golang-safety`,
  `golang-context`, `golang-database`, `golang-graphql`, `golang-how-to`,
  `golang-pkg-go-dev`, `golang-samber-libs`.
- Two more skills from the cxuu/golang-skills topic range: `golang-language-idioms`
  (control flow, declarations, generics, function style) and `golang-logging`
  (slog, levels, structured attributes, zap/zerolog comparison).
- Thirteen Python-specific skills mirroring the Go set: `python-idioms`,
  `python-typing`, `python-error-handling`, `python-concurrency`,
  `python-context`, `python-testing-advanced`, `python-security`,
  `python-performance`, `python-project-structure`, `python-logging`,
  `python-web-and-apis`, `python-data-and-validation`, `python-ecosystem`.
- Fourteen TypeScript/JavaScript-specific skills completing the JS/TS side:
  `typescript-idioms`, `typescript-typing-advanced`,
  `typescript-async-concurrency`, `typescript-error-handling`,
  `typescript-testing-advanced`, `typescript-security`,
  `typescript-performance`, `typescript-project-structure`,
  `typescript-lint-format-tooling`, `typescript-node-runtime`,
  `typescript-web-and-dom`, `typescript-ecosystem-and-packages`,
  `typescript-build-and-bundling`, `typescript-stay-updated`.

## [1.2.0] - 2026-11-27

### Added

- Skills `git-workflow-polyglot`, `release-and-changelog`, `dependency-audit`.
- Agent `polyglot-dev:planner`: turns a goal into an ordered, executable plan.
- Knowledge folder `polyglot-dev:ci-cd` (GitHub Actions) with a diagnostics
  reference; `reference.md` cheatsheets for JS/TS, Python, and Go extended
  with everyday and CI-debugging commands.
- CI: test matrix over Python 3.11–3.14 plus a ruff lint gate; property-based
  guard test runs when `hypothesis` is installed.
- Guard blocks additional destructive commands: `find -delete`,
  `dd of=/dev/<device>`, `chmod -R 777` / `chmod -R` on absolute paths,
  `shred`, `truncate -s 0`, and `git push` to `main`/`master`/`release/*`.
- Guard env overrides: `POLYGLOT_GUARD_DISABLED=1`,
  `POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1`.
- README "Development" section documenting conventions and the release process.

### Changed

- `git push --force` detection is now token-based (any argument position);
  safe `--force-with-lease` forms still pass.

## [1.1.0] - 2026-11-27

### Added

- Skill `debugging-polyglot`: failure classification, reproduction loop,
  and per-language debugging (JS/TS, Python, Go).
- Agent `polyglot-dev:explorer`: read-only code exploration and stack
  detection before planning changes.
- `reference.md` diagnostics cheatsheets in all three knowledge folders.
- CI workflow (GitHub Actions) running the guard's pytest suite on push
  and pull requests.
- CHANGELOG.md and this release process.

### Fixed

- Guard false positive: commit messages passed via `git commit -m` are
  data, not commands — a message that merely mentions a blocked command
  (`rm -rf`, hard resets, force push) no longer blocks the commit.
  Quoted commands elsewhere (e.g. `bash -c "..."`) are still scanned.
  Regression tests included (34 → 40 cases).

## [1.0.0]

- Initial release: 3 skills (feature-workflow, testing-polyglot,
  code-review-polyglot), 2 agents (code-reviewer, test-runner), 3 language
  knowledge folders, and the destructive-command guard with a pytest
  suite (34 cases).
