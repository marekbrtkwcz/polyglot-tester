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
| Agent | `polyglot-dev:code-reviewer` | Read-only subagent reviewing diffs for correctness, security, and language-specific pitfalls |
| Agent | `polyglot-dev:test-runner` | Detects the repo's runner, runs tests/lint/type checks, reports pass/fail with evidence |
| Knowledge | `polyglot-dev:javascript-typescript`, `polyglot-dev:python`, `polyglot-dev:go` | Toolchains and conventions per language |
| Hook | `guard-destructive-commands` | Pre-tool guard on `bash` (see below) |

## The destructive-command guard

`guard_destructive.py` runs before every `bash` tool call and blocks:

- `rm` combining recursive + force in **any flag spelling**: `-rf`, `-fr`,
  `-r -f`, `-r dir -f`, `--recursive --force`, inside `sudo`, `xargs`, or a
  command chain (`&&`, `;`)
- `git reset --hard`, `git clean -f`, `git stash drop|clear`
- `git push --force` — including `--force-with-lease=false`; the safe
  `--force-with-lease` / `--force-with-lease=<ref>:<sha>` forms pass

Unrecognized or unreadable payloads always pass through: the guard can never
brick a session. Failures exit non-zero with the reason on stderr.

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

34 cases: every blocked flag spelling, allowed near-misses (`rm -r` without
force, `--` end-of-options, flags belonging to a chained command), the git
patterns, and end-to-end hook behavior through stdin/stdout.
