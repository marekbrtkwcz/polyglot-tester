# polyglot-dev

[![CI](https://github.com/marekbrtkwcz/polyglot-tester/actions/workflows/ci.yml/badge.svg)](https://github.com/marekbrtkwcz/polyglot-tester/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [Vibe](https://mistral.ai) plugin (Agent Plugins 1.0 format) for polyglot
development in JavaScript/TypeScript, Python, and Go: a delivery workflow,
testing and code-review guidance, per-language knowledge, helper subagents,
and a safety hook that blocks destructive shell commands before they run.

## Quickstart

1. **Install** the plugin into your project (see [Install](#install)) and run
   `/reload` in Vibe.
2. **Ask for a change** in plain language — e.g. "add input validation to the
   signup endpoint, test-first". The `feature-workflow` skill drives the whole
   loop: plan → failing test → implementation → verification → review.
3. **Let the right language skill load itself**: when the task touches Go,
   Python, or TypeScript code, the matching `golang-*`, `python-*`, or
   `typescript-*` skill activates on its own — you don't need to name it.
4. **Review before merging**: ask for a review and the `code-review-polyglot`
   checklist plus the `code-reviewer` agent produce a severity-ranked verdict.
5. **Ship it**: `git-workflow-polyglot` for the branch/commit/PR flow,
   `release-and-changelog` for versioning and release notes.

The `guard-destructive-commands` hook is active from the first run — a
mistyped `rm -rf` or force-push is blocked with an explanation, never executed.

## Components

| Component | Name | What it does |
| --- | --- | --- |
| Skill | `polyglot-dev:feature-workflow` | End-to-end delivery loop: understand → plan → test-first implement → verify → review → hand off |
| Skill | `polyglot-dev:testing-polyglot` | Writing and running tests per language: framework detection, structure, deterministic data, coverage |
| Skill | `polyglot-dev:unit-testing-polyglot` | The fast isolated layer per language: Vitest/Jest, pytest, Go table-driven tests, mocks, single-test runs |
| Skill | `polyglot-dev:code-review-polyglot` | Per-language review checklists (JS/TS, Python, Go) with a severity-ranked verdict format |
| Skill | `polyglot-dev:debugging-polyglot` | Failure classification, reproduction loop, and per-language debugging guidance |
| Skill | `polyglot-dev:git-workflow-polyglot` | Day-to-day git: commit conventions, branching, PRs, rebase, bisect, recovery |
| Skill | `polyglot-dev:release-and-changelog` | Semver, Keep a Changelog, tagging, release notes from a diff, rollback plan |
| Skill | `polyglot-dev:dependency-audit` | Vulnerability and outdated-dependency audits per language (npm audit, pip-audit, govulncheck) |
| Skill | `polyglot-dev:database-polyglot` | Store choice, safe queries, transactions, expand/contract migrations, pooling across JS/TS, Python, Go |
| Skill | `polyglot-dev:api-design-polyglot` | Resource modeling, status codes, error envelopes, pagination, versioning, breaking-change policy |
| Skill | `polyglot-dev:auth-polyglot` | Passwords (argon2/bcrypt), sessions, JWT, OAuth2/OIDC+PKCE, authorization, MFA across all three languages |
| Skill | `polyglot-dev:accessibility-polyglot` | WCAG 2.2 AA: semantics, keyboard, screen readers, axe-core per stack, manual sign-off |
| Skill | `polyglot-dev:i18n-polyglot` | Message catalogs, ICU plurals, Intl/Babel/x-text formatting, RTL, pseudo-localization |
| Skill | `polyglot-dev:events-and-queues-polyglot` | Kafka/SQS/RabbitMQ, idempotent consumers, backoff+DLQ, message contracts, async testing |
| Skill | `polyglot-dev:observability-polyglot` | Structured logs, RED/USE metrics, traces, correlation IDs, symptom-based alerting per language |
| Skill | `polyglot-dev:docs-polyglot` | READMEs, docstrings, ADRs, API docs, changelogs — docs a new teammate can follow verbatim |
| Skill | `polyglot-dev:security-polyglot` | Injection, secrets, crypto, HTTP hardening, dependency auditing across JS/TS, Python, Go |
| Skill | `polyglot-dev:performance-polyglot` | Measure-first optimization: profilers, common wins, benchmarks in CI per language |
| Skill | `polyglot-dev:error-handling-polyglot` | Error chaining (`%w` / `raise from` / `cause`), domain error types, log-once discipline |
| Skill | `polyglot-dev:refactoring-polyglot` | Test-first refactoring: one green step at a time, tool-driven renames, no behavior mixing |
| Skill | `polyglot-dev:ci-cd-polyglot` | CI/CD setup per stack: gates, matrices, caching, secrets, merge gating, release automation |
| Skill | `polyglot-dev:docker-polyglot` | Dockerfiles and multi-stage builds per language, compose, rootless Podman, image scanning, tagging |
| Skill | `polyglot-dev:stay-updated-polyglot` | Official sources, EOL schedules, and a safe one-thing-at-a-time upgrade routine per language |
| Skill | `polyglot-dev:golang-error-handling` | Go errors: `%w` wrapping, sentinels, `errors.Is/As`, API error design |
| Skill | `polyglot-dev:golang-concurrency` | Goroutines, channels, errgroup, context, race/leak prevention |
| Skill | `polyglot-dev:golang-testing-advanced` | Table-driven tests, testify, mocks, fuzzing, benchmarks, goleak |
| Skill | `polyglot-dev:golang-security` | Injection, path traversal, secrets, crypto, HTTP hardening, govulncheck |
| Skill | `polyglot-dev:golang-performance` | pprof profiling, allocations, escape analysis, benchmarking discipline |
| Skill | `polyglot-dev:golang-project-structure` | Standard layout, naming, modern Go idioms, gofmt/vet/golangci-lint gate |
| Skill | `polyglot-dev:golang-libraries-and-patterns` | When to pick cobra/viper, gRPC, slog, wire/fx, lo, sqlc, testify |
| Skill | `polyglot-dev:golang-design-and-data` | Structs vs interfaces, composition, common patterns, choosing data structures |
| Skill | `polyglot-dev:golang-refactoring` | Safe refactoring: test-first, small compiling steps, gopls rename |
| Skill | `polyglot-dev:golang-stay-updated` | Toolchain upgrades, go directive, `gopls modernize`, stdlib-first rule |
| Skill | `polyglot-dev:golang-safety` | Panic recovery, nil map/pointer traps, races, overflow, input limits |
| Skill | `polyglot-dev:golang-context` | ctx as first param, cancellation, deadlines, values sparingly |
| Skill | `polyglot-dev:golang-database` | sqlc/sqlx/ORM choice, pooling, transactions, migrations, query safety |
| Skill | `polyglot-dev:golang-graphql` | gqlgen, schema design, dataloader for N+1, errors, depth limits |
| Skill | `polyglot-dev:golang-how-to` | Copy-paste recipes: HTTP server, JSON API, env, files, retry, shutdown |
| Skill | `polyglot-dev:golang-web-and-apis` | net/http vs gin/echo/fiber, handlers, middleware order, graceful shutdown, handler tests |
| Skill | `polyglot-dev:golang-pkg-go-dev` | Evaluating packages on pkg.go.dev, curated library categories |
| Skill | `polyglot-dev:golang-samber-libs` | lo, oops, do, mo, hot, ro — what each is for and when to skip it |
| Skill | `polyglot-dev:golang-language-idioms` | Guard clauses, var vs :=/iota/shadowing, generics, function style, Stringer |
| Skill | `polyglot-dev:golang-logging` | slog in depth, levels, structured attributes, ctx, when zap/zerolog win |
| Skill | `polyglot-dev:python-idioms` | Pythonic constructs, EAFP, context managers, dataclasses, dunder methods |
| Skill | `polyglot-dev:python-typing` | mypy strict, generics, TypeGuard, TypedDict, Protocols, overloads |
| Skill | `polyglot-dev:python-error-handling` | Custom exceptions, `raise from` chaining, traceback reading, error logging |
| Skill | `polyglot-dev:python-concurrency` | asyncio vs threads vs processes, the GIL, cancellation, thread safety |
| Skill | `polyglot-dev:python-context` | contextvars for request-scoped state, context managers, avoiding globals |
| Skill | `polyglot-dev:python-testing-advanced` | pytest fixtures/parametrize, monkeypatch, mocking, hypothesis, coverage |
| Skill | `polyglot-dev:python-security` | Injection (SQL/eval/pickle/YAML), path traversal, secrets, bandit + pip-audit |
| Skill | `polyglot-dev:python-performance` | cProfile, memory_profiler, lru_cache, `__slots__`, when to leave CPython |
| Skill | `polyglot-dev:python-project-structure` | src layout, pyproject, uv, ruff/mypy gates, pre-commit, packaging |
| Skill | `polyglot-dev:python-logging` | logging module, structlog, levels, JSON in prod, correlation IDs |
| Skill | `polyglot-dev:python-web-and-apis` | FastAPI/Django/Flask choice, async SQLAlchemy, Alembic, Strawberry, Celery |
| Skill | `polyglot-dev:python-database` | SQLAlchemy 2.x sync/async, psycopg3/asyncpg, Alembic up/down, pooling, transactions |
| Skill | `polyglot-dev:python-refactoring` | Test-first refactoring: rename/extract/move via jedi/rope, one green step at a time |
| Skill | `polyglot-dev:python-stay-updated` | Python EOL schedule, What's New, deprecation-driven upgrades, dependency bumps |
| Skill | `polyglot-dev:python-data-and-validation` | pydantic v2 vs attrs vs dataclasses, Protocols, boundary validation |
| Skill | `polyglot-dev:python-ecosystem` | Evaluating PyPI packages, curated picks (httpx, typer, polars, respx...) |
| Skill | `polyglot-dev:typescript-idioms` | Modern JS/TS idioms: const/arrow/destructuring, immutable updates, guard clauses |
| Skill | `polyglot-dev:typescript-typing-advanced` | Strict tsconfig, generics, utility types, type guards, branded types, discriminated unions |
| Skill | `polyglot-dev:typescript-async-concurrency` | Event loop, promise pitfalls, Promise.all vs sequential await, AbortController, worker threads |
| Skill | `polyglot-dev:typescript-error-handling` | Error subclasses, `cause` chaining, unhandled rejections, Result type for expected failures |
| Skill | `polyglot-dev:typescript-testing-advanced` | Vitest/Jest, mocking boundaries, fake timers, fast-check, meaningful coverage |
| Skill | `polyglot-dev:typescript-security` | XSS/injection, prototype pollution, schema validation, secrets, npm audit, HTTP headers |
| Skill | `polyglot-dev:typescript-performance` | Profiling, bundle size, memory leaks, Web Vitals, streams in Node |
| Skill | `polyglot-dev:typescript-project-structure` | package.json hygiene, tsconfig, workspaces/Nx/Turborepo, folder conventions, gates |
| Skill | `polyglot-dev:typescript-lint-format-tooling` | Biome vs ESLint+Prettier, type-aware linting, pre-commit hooks, CI gates that can fail |
| Skill | `polyglot-dev:typescript-node-runtime` | Node versions, ESM/CJS, streams/buffers, CLI tools, env validation, graceful shutdown |
| Skill | `polyglot-dev:typescript-web-and-dom` | DOM APIs, fetch + AbortController, storage, events, IntersectionObserver, a11y basics |
| Skill | `polyglot-dev:typescript-database` | Prisma vs Drizzle vs pg, pool sizing, transactions, migrations, N+1 |
| Skill | `polyglot-dev:typescript-graphql` | yoga/Apollo/Pothos, dataloaders, typed errors, depth limits, codegen client |
| Skill | `polyglot-dev:typescript-ecosystem-and-packages` | npm/pnpm/yarn, semver, exports map, publishing with provenance, evaluating dependencies |
| Skill | `polyglot-dev:typescript-build-and-bundling` | tsc vs bundlers, ESM+CJS+d.ts for libs, attw, Vite/esbuild/tsup, code splitting |
| Skill | `polyglot-dev:typescript-stay-updated` | TS/ES/Node release tracking, safe upgrade routine, baseline-wide features, dep hygiene |
| Skill | `polyglot-dev:typescript-refactoring` | Test-first TS refactoring: tsserver renames, `tsc --noEmit` gate, extract/component moves |
| Agent | `polyglot-dev:code-reviewer` | Read-only subagent reviewing diffs for correctness, security, and language-specific pitfalls |
| Agent | `polyglot-dev:test-runner` | Detects the repo's runner, runs tests/lint/type checks, reports pass/fail with evidence |
| Agent | `polyglot-dev:explorer` | Read-only code exploration: structure, call sites, stack detection before planning |
| Agent | `polyglot-dev:planner` | Turns a goal into a concrete plan: files to touch, test level, risks, verification steps |
| Agent | `polyglot-dev:security-auditor` | Read-only security review: injection, access control, secrets, deserialization, supply chain |
| Agent | `polyglot-dev:doc-writer` | Writes READMEs, docstrings, ADRs, changelogs matching the repo's existing docs style |
| Agent | `polyglot-dev:refactorer` | Test-first refactoring in small green steps; never mixes refactor with behavior change |
| Agent | `polyglot-dev:performance-profiler` | Picks the right profiler per stack, reads the output, reports bottlenecks with evidence |
| Agent | `polyglot-dev:onboarder` | Read-only repo explorer producing a newcomer's map: stack, layout, commands, conventions |
| Knowledge | `polyglot-dev:javascript-typescript`, `polyglot-dev:python`, `polyglot-dev:go`, `polyglot-dev:ci-cd`, `polyglot-dev:testing`, `polyglot-dev:docker`, `polyglot-dev:databases`, `polyglot-dev:security`, `polyglot-dev:cloud`, `polyglot-dev:architecture` | Toolchains, conventions, and diagnostics per language plus CI/CD, testing, containers, databases, security, cloud, architecture patterns |
| Hook | `guard-destructive-commands` | Pre-tool guard on every shell tool — `bash`/`git_bash`/`powershell`, background included (see below) |
| Hook | `guard-secrets-in-git` | On `git add`/`git commit`, scans staged/unstaged/untracked content for secret patterns and blocks the command |
| Hook | `guard-wip-commit-message` | Blocks `git commit` with a WIP/DO NOT MERGE subject (see below) |
| Hook | `pre-push-checks` | Before `git push`, runs the README-drift check and structure tests (see below) |

## The destructive-command guard

`guard_destructive.py` runs before every shell tool call — `bash`, `git_bash`, `powershell`, including background `process_start` commands — and blocks:

- `rm` combining recursive + force in **any flag spelling**: `-rf`, `-fr`,
  `-r -f`, `-r dir -f`, `--recursive --force`, inside `sudo`, `xargs`, or a
  command chain (`&&`, `;`)
- `git reset --hard`, `git clean -f`, `git stash drop|clear`
- `git push --force` in any token position — including `--force-with-lease=false`;
  the safe `--force-with-lease` / `--force-with-lease=<ref>:<sha>` forms pass
- `git push` to `main`, `master`, or `release/*`
- `find ... -delete`, `dd ... of=/dev/<device>`, `chmod -R 777` or `chmod -R` on
  an absolute path, `shred`, `truncate -s 0`
- `mkfs` (any filesystem), `wipefs`/`mkswap` on a device, redirects or
  `cp`/`mv`/`tee` onto a block device (`/dev/sd*`, `/dev/nvme*`, `/dev/mmcblk*`,
  `/dev/vd*`, `/dev/xvd*`, `/dev/hd*`)
- `kubectl delete --all` / `--all-namespaces`
- `git push --delete` and the `git push origin :branch` delete-refspec form
- PowerShell equivalents (the `powershell` tool): `Remove-Item` and its
  `rm`/`del`/`erase`/`rd`/`ri` aliases combining `-Recurse` with `-Force`,
  `Format-Volume`, `Clear-Disk -RemoveData`/`-RemoveOEM`

Unrecognized or unreadable payloads always pass through: the guard can never
brick a session. Failures exit non-zero with the reason on stderr.

Deliberate overrides via environment variables:

- `POLYGLOT_GUARD_DISABLED=1` — disables every block
- `POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1` — allows pushing to protected branches

## The secrets guard

`guard_secrets.py` also runs as a `pre_tool` hook on every shell tool
(see the destructive-command guard). When the command
contains `git add` or `git commit`, it scans the staged diff, unstaged diff,
and untracked files (skipping lockfiles and minified bundles) for likely
secrets: AWS keys, GitHub/Slack/Stripe/Google tokens, private key blocks, and
generic `api_key`/`secret`/`token` assignments. Findings are reported masked
(first/last characters only) and the command is blocked.

Override for a deliberate, informed case: `POLYGLOT_SECRETS_DISABLED=1`.

## The WIP commit guard

`guard_commit_message.py` (`pre_tool` on every shell tool) blocks `git commit` whose
subject starts with `WIP`/`[WIP]`/`DO NOT MERGE` — taken from the first
`-m`/`--message` argument or the first line of a `-F` message file. Commits
without inline messages (editor flow) pass. Override: `POLYGLOT_WIP_DISABLED=1`.

## The pre-push checks

`prepush_checks.py` (`pre_tool` on every shell tool) runs fast local checks before a
plain `git push`: the README/skills drift check and the plugin structure
test suite. A failing check blocks the push with the output on stderr;
history-rewriting pushes are left to the destructive-command guard. The hook
fails open when python/pytest are unavailable, and stays a silent no-op when
the plugin is installed in a project other than its own repository.
Override: `POLYGLOT_PREPUSH_DISABLED=1`.

## Install

Project scope (trusted folder only):

```text
<project>/.vibe/plugins/polyglot-dev/   # this directory, minus tests/
```

User global (available in every project):

```text
~/.vibe/plugins/polyglot-dev/
```

The hooks need Python 3.11+ on PATH — `python` or `python3`; every hook
command tries `python` first and falls back to `python3`. With no Python at
all, guarded commands are blocked (fail-closed) rather than silently allowed.

Then run `/reload` in your Vibe session.

## Tests

The guard is the only component with executable logic, and it is tested:

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

197 cases: every blocked flag spelling, allowed near-misses (`rm -r` without
force, `--` end-of-options, flags belonging to a chained command), the git
patterns, commit-message false-positive regressions, end-to-end hook behavior
through stdin/stdout, and a property-based test (hypothesis) that checks
`is_bulk_rm` against a reference model over generated flag combinations.
CI runs the suite on Linux across Python 3.11–3.14 plus a Windows job,
enforces a coverage gate, a ruff lint and format gate, `plugin.json` schema
validation against the official Agent Plugins 1.0 schema, a check that the
component table below lists every skill (`scripts/check_readme_skills.py`),
and a pinned markdownlint pass over all docs — on every push and pull request
(`.github/workflows/ci.yml`).

## Development

- Agent TOML files use **snake_case** keys (`schema_version`, `agent_type`,
  `display_name`, `enabled_tools`, `disabled_tools`) — the plugin validator
  rejects camelCase.
- Add an agent: new TOML under `ai.mistral.vibe/agents/`.

### Adding your own skill

A skill is one folder with one file:

```text
.vibe/plugins/polyglot-dev/skills/<skill-name>/SKILL.md
```

Conventions:

- **Name**: lowercase `kebab-case`, unique across the plugin; prefix it with
  the language when it is language-specific (`golang-`, `python-`,
  `typescript-`) and leave it unprefixed for cross-language topics.
- **Frontmatter** (required, exactly two fields):

  ```yaml
  ---
  name: my-skill
  description: Load this skill when ... — one sentence that tells the agent
    exactly which requests should trigger it.
  ---
  ```

  The `description` is the trigger: write it from the user's point of view
  ("Load this skill when writing idiomatic Python..."), not from the file's.
- **Body**: markdown, imperative and example-driven. Lead with the decision
  the reader must make, then the rules, then copy-paste examples. Keep it
  scannable — bullets over prose, code blocks over explanations.
- **No extra files** unless the skill needs them (reference docs, scripts);
  link them from `SKILL.md`.
- After adding: list the skill in the Components table above and in
  `CHANGELOG.md` under `[Unreleased]`.
- Run tests: `python -m pytest .vibe/plugins/polyglot-dev/tests/ -q`
  (optional `hypothesis` enables the property-based test).
- Lint & format: `python -m ruff check --isolated --select E4,E7,E9,F .vibe/plugins/polyglot-dev/`
  and `python -m ruff format --check .vibe/plugins/polyglot-dev/`
- Release: bump `plugin.json` + `CHANGELOG.md` (Keep a Changelog), commit
  `Release vX.Y.Z`, tag `vX.Y.Z`, push branch and tag.
