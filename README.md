# polyglot-dev

A [Vibe](https://mistral.ai) plugin (Agent Plugins 1.0 format) for polyglot
development in JavaScript/TypeScript, Python, and Go: a delivery workflow,
testing and code-review guidance, per-language knowledge, helper subagents,
and a safety hook that blocks destructive shell commands before they run.

## Components

| Component | Name | What it does |
|---|---|---|
| Skill | `polyglot-dev:feature-workflow` | End-to-end delivery loop: understand → plan → test-first implement → verify → review → hand off |
| Skill | `polyglot-dev:testing-polyglot` | Writing and running tests per language: framework detection, structure, deterministic data, coverage |
| Skill | `polyglot-dev:code-review-polyglot` | Per-language review checklists (JS/TS, Python, Go) with a severity-ranked verdict format |
| Skill | `polyglot-dev:debugging-polyglot` | Failure classification, reproduction loop, and per-language debugging guidance |
| Skill | `polyglot-dev:git-workflow-polyglot` | Day-to-day git: commit conventions, branching, PRs, rebase, bisect, recovery |
| Skill | `polyglot-dev:release-and-changelog` | Semver, Keep a Changelog, tagging, release notes from a diff, rollback plan |
| Skill | `polyglot-dev:dependency-audit` | Vulnerability and outdated-dependency audits per language (npm audit, pip-audit, govulncheck) |
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
| Skill | `polyglot-dev:typescript-ecosystem-and-packages` | npm/pnpm/yarn, semver, exports map, publishing with provenance, evaluating dependencies |
| Skill | `polyglot-dev:typescript-build-and-bundling` | tsc vs bundlers, ESM+CJS+d.ts for libs, attw, Vite/esbuild/tsup, code splitting |
| Skill | `polyglot-dev:typescript-stay-updated` | TS/ES/Node release tracking, safe upgrade routine, baseline-wide features, dep hygiene |
| Agent | `polyglot-dev:code-reviewer` | Read-only subagent reviewing diffs for correctness, security, and language-specific pitfalls |
| Agent | `polyglot-dev:test-runner` | Detects the repo's runner, runs tests/lint/type checks, reports pass/fail with evidence |
| Agent | `polyglot-dev:explorer` | Read-only code exploration: structure, call sites, stack detection before planning |
| Agent | `polyglot-dev:planner` | Turns a goal into a concrete plan: files to touch, test level, risks, verification steps |
| Knowledge | `polyglot-dev:javascript-typescript`, `polyglot-dev:python`, `polyglot-dev:go`, `polyglot-dev:ci-cd` | Toolchains, conventions, and diagnostics per language plus GitHub Actions |
| Hook | `guard-destructive-commands` | Pre-tool guard on `bash` (see below) |

## The destructive-command guard

`guard_destructive.py` runs before every `bash` tool call and blocks:

- `rm` combining recursive + force in **any flag spelling**: `-rf`, `-fr`,
  `-r -f`, `-r dir -f`, `--recursive --force`, inside `sudo`, `xargs`, or a
  command chain (`&&`, `;`)
- `git reset --hard`, `git clean -f`, `git stash drop|clear`
- `git push --force` in any token position — including `--force-with-lease=false`;
  the safe `--force-with-lease` / `--force-with-lease=<ref>:<sha>` forms pass
- `git push` to `main`, `master`, or `release/*`
- `find ... -delete`, `dd ... of=/dev/<device>`, `chmod -R 777` or `chmod -R` on
  an absolute path, `shred`, `truncate -s 0`

Unrecognized or unreadable payloads always pass through: the guard can never
brick a session. Failures exit non-zero with the reason on stderr.

Deliberate overrides via environment variables:

- `POLYGLOT_GUARD_DISABLED=1` — disables every block
- `POLYGLOT_GUARD_ALLOW_PROTECTED_PUSH=1` — allows pushing to protected branches

## Install

Project scope (trusted folder only):

```
<project>/.vibe/plugins/polyglot-dev/   # this directory, minus tests/
```

User global (available in every project):

```
~/.vibe/plugins/polyglot-dev/
```

Then run `/reload` in your Vibe session.

## Tests

The guard is the only component with executable logic, and it is tested:

```
pip install pytest
python -m pytest tests/ -q
```

80+ cases: every blocked flag spelling, allowed near-misses (`rm -r` without
force, `--` end-of-options, flags belonging to a chained command), the git
patterns, commit-message false-positive regressions, end-to-end hook behavior
through stdin/stdout, and a property-based test (hypothesis) that checks
`is_bulk_rm` against a reference model over generated flag combinations.
CI runs the suite on Python 3.11–3.14 plus a ruff lint gate on every push and
pull request (`.github/workflows/ci.yml`).

## Development

- Agent TOML files use **snake_case** keys (`schema_version`, `agent_type`,
  `display_name`, `enabled_tools`, `disabled_tools`) — the plugin validator
  rejects camelCase.
- Add a skill: new folder under `skills/<name>/SKILL.md` with frontmatter
  (`name`, `description`).
- Add an agent: new TOML under `ai.mistral.vibe/agents/`.
- Run tests: `python -m pytest .vibe/plugins/polyglot-dev/tests/ -q`
  (optional `hypothesis` enables the property-based test).
- Lint: `python -m ruff check --isolated --select E4,E7,E9,F .vibe/plugins/polyglot-dev/`
- Release: bump `plugin.json` + `CHANGELOG.md` (Keep a Changelog), commit
  `Release vX.Y.Z`, tag `vX.Y.Z`, push branch and tag.
