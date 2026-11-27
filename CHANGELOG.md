# Changelog

All notable changes to the polyglot-dev plugin are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic.

## [1.5.0] - 2026-11-27

### Added

- Seven cross-language skills closing the symmetry gaps between the per-language sets:
  `security-polyglot`, `performance-polyglot`, `error-handling-polyglot`,
  `refactoring-polyglot`, `ci-cd-polyglot`, `docker-polyglot`, `stay-updated-polyglot`.
- `typescript-refactoring`: the missing per-language refactoring skill for JS/TS
  (tsserver renames, `tsc --noEmit` gate, one green step at a time).
- `scripts/check_readme_skills.py` + tests: CI now fails when a skill is missing
  from the README component table or the table references a removed skill.
- CI badge + MIT `LICENSE` file in README (license was declared in plugin.json
  but the file was missing).
- `release-drafter` workflow: auto-drafted release notes from merged PRs,
  categorized and version-resolved from labels.
- Dependabot (weekly) for GitHub Actions versions.
- Knowledge folder `architecture`: layered vs hexagonal vs feature-slice
  architecture per language, dependency direction, per-language module layout,
  and anti-patterns.
- New hook `guard-wip-commit-message` (`guard_commit_message.py`): blocks
  `git commit` with a WIP/DO NOT MERGE subject from `-m` or `-F`. Override:
  `POLYGLOT_WIP_DISABLED=1`. 12 test cases.
- New hook `pre-push-checks` (`prepush_checks.py`): before a plain `git push`,
  runs `scripts/check_readme_skills.py` and the structure test suite; fails
  open when tooling is missing. Override: `POLYGLOT_PREPUSH_DISABLED=1`.
  5 test cases.

## [1.4.0] - 2026-11-27

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
- New hook `guard-secrets-in-git` (`guard_secrets.py`): on `git add`/`git
  commit`, scans staged, unstaged, and untracked content for secret patterns
  (AWS, GitHub, Slack, Stripe, Google keys, private key blocks, generic
  api_key/secret/token assignments) and blocks the command. Override:
  `POLYGLOT_SECRETS_DISABLED=1`. 18 new test cases.
- Cross-references to the `test-automation` and `qa-mcp` plugins added to
  `testing-polyglot`, `debugging-polyglot`, `typescript-testing-advanced`,
  `python-testing-advanced`, and `golang-testing-advanced`.
- Seven skills closing the per-language coverage gaps found in the audit:
  `auth-polyglot` (cross-language auth), `typescript-database`,
  `typescript-graphql`, `python-database`, `python-refactoring`,
  `python-stay-updated`, `golang-web-and-apis`.
- Three more cross-language skills: `accessibility-polyglot` (WCAG 2.2),
  `i18n-polyglot` (locales, plurals, RTL), `events-and-queues-polyglot`
  (brokers, idempotency, DLQ).
- Agents `performance-profiler` and `onboarder`.
- Knowledge folders `security` (OWASP per language + tooling) and `cloud`
  (IAM, core services, Terraform workflow).
- Secrets guard detects npm tokens, GitLab PATs, SendGrid keys, Slack
  webhooks, and JWTs in addition to the existing patterns.
- CI gains a `plugin-schema` job (plugin.json validated against the official
  Agent Plugins 1.0 schema via `scripts/validate_plugin_schema.py`) and a
  `docs-lint` job (markdownlint-cli2 over all markdown).
- Unit tests for `scripts/validate_plugin_schema.py` in `tests/` (schema
  fetch mocked); the CI test step now runs both `tests/` and the plugin
  test suite (143 tests).
- Skill `unit-testing-polyglot`: the unit-test layer per language (Vitest/Jest,
  pytest, Go table-driven) — structure, mocks, determinism, running one test.

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
