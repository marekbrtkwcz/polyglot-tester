# Changelog

All notable changes to the polyglot-dev plugin are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic.

## [Unreleased]

### Added

- Eval coverage and wiring (audit finding 4): 12 new must-fire activation
  cases (A12–A23), one per per-language twin group with the language named,
  gating the twin deferral sentences — coverage is now 23/79 skills
  (backlog accounting in `evals/activation-cases.md`). The deterministic
  matcher `scripts/eval_skill_matching.py` now also runs in CI as an
  advisory `skill-evals` job (`continue-on-error: true`) over all 38 cases;
  behavioural model scoring remains a manual step (run record in
  `evals/runs/2026-11-27-twin-group-cases-and-ci.md`).
- Twin deferral sentences in the 41 per-language skill descriptions across
  the 14 same-topic twin groups (concurrency, context, database,
  error-handling, graphql, idioms, logging, performance, project-structure,
  refactoring, security, stay-updated, testing, web/apis): each now says
  "If the language is not <Lang>, prefer <sibling skills>", so a
  language-ambiguous prompt defers to the right twin instead of waking a
  random one. `evals/collision-cases.md` gains case 15 (language-ambiguous
  prompt, umbrella must win) and the known-limitation note is updated.
- Collection cross-wiring from the qualitative audit: all 55 per-language
  skills (`golang-*`, `python-*`, `typescript-*`) now link their language
  knowledge folder (`go`, `python`, `javascript-typescript`) in a `## Related`
  section, and 7 of 9 agents (`doc-writer`, `test-runner`,
  `performance-profiler`, `refactorer`, `planner`, `explorer`, `onboarder`)
  point at the plugin's own skill or knowledge files as the single source of
  truth instead of carrying a private copy of the checklist — matching the
  pattern `code-reviewer` and `security-auditor` already used.
- Two per-language skills closing the parity gaps: `python-graphql`
  (Strawberry/Ariadne/Graphene, schema design, DataLoader, depth limits) and
  `typescript-logging` (pino vs winston, AsyncLocalStorage correlation IDs,
  redaction). Each ships with its must-fire activation case and collision row
  per the `evals/activation-cases.md` coverage rule; `observability-polyglot`,
  `api-design-polyglot` and `python-web-and-apis` cross-link to them.
- `requirements-dev.txt`: one dependency source for CI and local development
  instead of ad-hoc `pip install` lines in three CI jobs.
- Structure tests: skill descriptions must stay within Vibe's 1024-character
  limit and follow the "Load this skill ..." trigger convention.
- CI hardening: a `windows-latest` test job, a 75% coverage gate over the
  guards and scripts, and a `ruff format --check` gate (the plugin's Python
  files and the Python code blocks inside skills are now formatted).
- Docs lint under pinned `markdownlint-cli2` 0.24.2: bare code fences declare
  a language (MD040), tables use a consistent column style (MD060), bare URLs
  are angle-wrapped (MD034), the unescaped `|safe` table cell is fixed
  (MD056), and MD024 allows the repeated Keep-a-Changelog section headings.
- Release workflow: pushing a `vX.Y.Z` tag runs the tests, verifies the tag
  against `plugin.json`, and attaches `polyglot-dev-<version>.zip` — built
  with `git archive`, `tests/` excluded via `export-ignore` — to the GitHub
  release; the workflow fails if the zip still contains `tests/`.
- Skill collision audit: the 11 descriptions in the highest-risk
  near-neighbour groups (cross-language vs per-language twins, the testing
  pair, logging vs observability, dependency audit vs security, review vs
  workflow) now name the competing skill and say when to prefer it, and
  `evals/collision-cases.md` records the collision cases with intended
  winners for future behavioural runs.

- PowerShell destructive-command patterns for the `powershell` shell tool:
  `Remove-Item` (and its `rm`/`del`/`erase`/`rd`/`ri` aliases) with both
  `-Recurse` and `-Force`, `Format-Volume`, `Clear-Disk -RemoveData`.
  Near-misses keep bash parity: `-Recurse` without `-Force` passes like
  `rm -r`.
- `reference.md` companions for the six knowledge folders that lacked
  them (architecture, cloud, databases, docker, security, testing) —
  diagnostics commands, lookup tables, and failure triage in the style of
  the existing ci-cd, go, javascript-typescript, and python references,
  so every knowledge folder now has a quick-reference companion.
- `evals/activation-cases.md`: must-fire cases and a before/after gate for
  edited skills — a description edit must not silence a case that fired
  or wake one that stayed quiet (unless that was the stated intent, and
  then the collision cases re-run); body-only edits gate on substance.
  Ships with starter cases for the workflow backbone and a coverage rule
  that ties every future description edit to its case.
- Cross-link sections in the umbrella skills: thirteen skills that had no
  links to their per-language twins or the knowledge folders now carry a
  `## Related` section (api-design, auth, code-review, database,
  dependency-audit, events-and-queues, git-workflow, observability,
  release-and-changelog, unit-testing), and security-polyglot,
  refactoring-polyglot, and testing-polyglot gained knowledge-folder
  pointers in their existing sections.
- `guard-secrets-in-files` hook: `write_file` and `edit` payloads are
  scanned for the same secret patterns before the text lands in a file —
  a secret is caught at write time (inside or outside a git repository),
  not only at the next `git add`. An edit that *removes* a secret passes,
  lockfile paths are skipped, and the structure test now enforces that a
  hook guarding a tool class covers every variant of that class.
- New skill `ai-integration-polyglot`: integrating LLM APIs in JS/TS,
  Python, and Go — provider/SDK choice behind one adapter, prompt
  structure, structured output, embeddings and vector search, RAG
  basics, token budgets and cost/latency control, prompt-injection
  safety, and testing LLM-backed features. Ships with its must-fire
  activation case (A9) in `evals/activation-cases.md` per the coverage
  rule.

### Changed

- All four pre-tool hooks now match `re:bash|git_bash|powershell|process_start`:
  commands the agent starts in the background or through the Windows managed
  shell tools no longer bypass the destructive-command, secrets, WIP-commit,
  and pre-push guards.
- Hook commands try `python` and fall back to `python3`, so on macOS and
  modern Linux (which ship `python3` only) the guards keep working instead
  of denying every guarded shell call under `strict = true`.
- The four read-only agents (`explorer`, `planner`, `code-reviewer`,
  `security-auditor`) can run read-only search commands (`grep`/`rg`,
  `find`, `git log`/`git blame`) through `bash`: every command still needs
  user approval (`permission = "ask"`), and a denylist blocks
  state-changing git commands plus `rm -rf`, so finding call sites no
  longer depends on guessing file paths with `read_file` alone.
- The `code-reviewer` and `security-auditor` instructions now read their
  per-language checklist from the plugin's own
  `skills/code-review-polyglot/SKILL.md` and
  `skills/security-polyglot/SKILL.md` instead of duplicating it, so the
  agent instructions and the skills cannot drift apart; a one-line
  fallback covers the review order when the skill file is not found.
- `test-runner` can now run just the tests related to the changed files
  (mapped by naming convention and package) before the full suite, and it
  reports the runner's coverage summary when the repo already supports
  coverage without adding any new dependency.
- The five pre-tool hooks are consolidated into ONE hook
  (`polyglot-dev-guards`) whose new `guard_all.py` entrypoint reads the
  payload once and runs the destructive-command, secrets, WIP-commit, and
  pre-push checks in a single Python process per tool call (previously up
  to five interpreter startups per shell command). Each guard module keeps
  its own script, its `run_payload(payload)` entry, and its env disable
  switch; empty stdin still fails closed in the `|| python3` fallback.

### Fixed

- Regression from the hook consolidation: `write_file`/`edit` payloads no
  longer reach the shell guards. `hooks.toml` again routes file writes to
  their own hook (`polyglot-dev-secrets-in-files` → `guard_secrets.py`),
  and `extract_command` now skips file-content keys (`content`,
  `new_string`, `old_string`, `path`, `file_path`) at every nesting level,
  so a document mentioning `rm -rf` or `git push origin main` is never
  parsed as a shell command.
- `guard_all.py` imports its sibling guard modules inside the
  `try/except ImportError` path fallback, so importing it from outside the
  plugin directory no longer raises `ModuleNotFoundError` before the
  `sys.path` fix runs.
- `guard_all.py` added to `--paths-to-mutate` in the mutation workflow.
- `ai-integration-polyglot` now names the official Mistral SDKs per language
  (`mistralai` for Python, `@mistralai/mistralai` for JS/TS,
  `mistralai/client-go` for Go, key in `MISTRAL_API_KEY`) alongside the
  other providers.

- `pre-push-checks` is now a silent no-op when the plugin is installed in a
  project other than its own repository: it no longer prints `skipped` noise
  on every push there, and a missing pytest there no longer blocks the push.
  In its own repository it resolves the repo root from the hook payload's
  `cwd`, so the checks also run when Vibe executes the hook from its
  read-only plugin snapshot.
- `rm` flag detection in the destructive-command guard is now
  case-insensitive: the GNU uppercase spelling `rm -Rf` and the capitalized
  PowerShell `-Recurse`/`-Force` parameters no longer bypass it.
- Secrets guard no longer blocks a fix commit that REMOVES a leaked key:
  the git diff is scanned for added (`+`) lines only, so `-` lines never
  match. A plain `git commit` also no longer scans the unstaged diff (it
  stages nothing from the worktree); the unstaged diff is still scanned
  for `git add` and `git commit -a`, and untracked files for `git add`.
- `SKIP_PATHS` in the secrets guard now also excludes `uv.lock`,
  `poetry.lock`, `bun.lock`/`bun.lockb`, and `*.map` source maps; the
  pattern list gained OpenAI (`sk-proj-`/`sk-svcacct-`/legacy `sk-`),
  Anthropic (`sk-ant-`), and HuggingFace (`hf_`) keys.
- `is_bulk_rm` treats any single-dash token made only of GNU rm short-flag
  letters as an option cluster, so 4+-letter clusters like `rm -irfv` or
  `rm -dvrf` are blocked too (long parameters such as `-Confirm` still
  pass).
- Protected-push detection is token-based now: refspec destinations count
  (`git push origin HEAD:main`, `refs/heads/main`, `HEAD:release/1.0` are
  blocked; `main:feature/x` is not), and `--dry-run` pushes are never
  treated as protected.
- The WIP-commit guard only reads `-m`/`--message`/`-F` inside the
  `git commit` segment of the command, so `pytest -m wip && git commit -m
  "fix"` no longer false-positives; a WIP subject in ANY commit of a
  chain still blocks.
- Force-push detection now catches `+`-prefixed refspecs (`git push origin
  +main`, `+HEAD:main`) — in git the `+` prefix means force without
  `--force`. Protected-push detection strips the `+` too, treats the short
  `-n` flag like `--dry-run` (never protected), and `segment_after` is now
  quote-aware, so `git commit -m "WIP: foo; bar"` can no longer slip past
  the WIP guard through a quoted separator. The WIP subject regex also
  accepts `(wip)` parentheses, as its docstring always claimed.
- `is_bulk_rm` also knows the BSD `-x` flag: `rm -rfx build` is blocked.
- Secrets guard: the diff-header exclusion is now `+++ ` (with space), so
  an added code line starting with `++` (e.g. `++i;`) is still scanned;
  `commit_stages_worktree` strips quoted `-m` payloads first, so
  `git commit -m "fix -a flag"` no longer triggers an unstaged scan.
- README test count updated to 282.
- `segment_after` is escape-aware inside quotes: `\"` no longer closes the
  string, so `git commit -m "WIP: \"a; b"` can no longer slip past the WIP
  guard through a separator after an escaped quote.
- The dry-run check in `is_protected_push` uses a full short-flag match
  (`-n` clusters only), so option values like `-o=no-ci` are no longer
  misread as `--dry-run`.
- README no longer hardcodes the exact test count ("280+ cases"), so it
  does not drift on every PR that adds cases.

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
