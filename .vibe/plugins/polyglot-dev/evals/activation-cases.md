# Skill activation cases

Companion to `collision-cases.md`: that file proves the *right* skill wins
a near-neighbour collision; this one proves a skill fires at all when it
should — and that editing it does not silently change who fires. Every
case states the intended winner up front. Prompts avoid the skill's
description vocabulary on purpose — they are phrased the way a user would
ask.

## Coverage rule

- Every skill must have at least one must-fire case before its description
  is edited; until then its activation is unverified.
- Skills in near-neighbour groups additionally answer their group's rows in
  `collision-cases.md`.
- A new skill ships together with its must-fire case (and, when it has a
  near neighbour, its collision row) in the same change.

## Run protocol

Every prompt, three trials, same model and settings. Run the case set
twice around an edit: once on the current tree (baseline), once with the
edit applied. Record which skill fired per trial; disagreeing trials are
recorded, not discarded. Results land in
`evals/runs/YYYY-MM-DD-<skill-or-change>.md`: date, model, per-case trial
verdicts (fired skill / stayed quiet / substance held), and the gate
verdict.

## The before/after gate

Compare the two runs case by case:

- **Regression**: fired before, silent after — the edit broke activation.
  Fix the description or revert; the gate is red.
- **Leak**: quiet before, fires after — allowed only when waking that
  skill was the edit's stated intent, and then every collision group the
  skill belongs to re-runs. Otherwise the gate is red.
- **Substance**: firing is not passing — for cases that fire in both runs,
  the pass criteria must hold in the after-run.
- **Body-only edits** (description untouched) skip the baseline: activation
  is unchanged; gate on substance only.
- Gate green: every must-fire case fires, no unintended leak, on all three
  trials, in both runs.

## Pass criteria

Per case, scored per trial (same as the collision cases):

- the intended winner's body is actually used — its structure, checklist,
  or named tools appear in the response (substance, not just the name)
- no other skill's specifics dominate the response

## Starter cases — the workflow backbone

| # | Prompt (as a user would type it) | Must fire | Must not dominate |
| --- | --- | --- | --- |
| A1 | "We need the checkout endpoint to reject negative quantities — take it all the way to a fix you can prove works" | `feature-workflow` | `unit-testing-polyglot` |
| A2 | "Checkout returns 500 with nothing in the logs — find out why it dies" | `debugging-polyglot` | `feature-workflow` |
| A3 | "I'm on main by accident with two finished commits — move them to a branch without losing anything" | `git-workflow-polyglot` | `refactoring` |
| A4 | "We ship 2.0 on Friday — what should users read about what changed?" | `release-and-changelog` | `docs-polyglot` |
| A5 | "The getting-started guide at the repo root hasn't worked for months — make it match reality" | `docs-polyglot` | `feature-workflow` |
| A6 | "Every PR rebuilds everything and takes 25 minutes — run only what the diff can break" | `ci-cd-polyglot` | `feature-workflow` |
| A7 | "The app ships in Polish and German; where do we stand for Arabic?" | `i18n-polyglot` | `feature-workflow` |
| A8 | "A blind employee cannot place an order in the dashboard — find out where the UI blocks them" | `accessibility-polyglot` | `debugging-polyglot` |

## AI integration

| # | Prompt (as a user would type it) | Must fire | Must not dominate |
| --- | --- | --- | --- |
| A9 | "Our support bot invents refund rules that don't exist — plug it into a real model and make it answer only from our own docs" | `ai-integration-polyglot` | `debugging-polyglot` |

## Language-specific depth

| # | Prompt (as a user would type it) | Must fire | Must not dominate |
| --- | --- | --- | --- |
| A10 | "Our Python GraphQL API runs one query per list item — fix the N+1 and make the schema safe against deeply nested queries" | `graphql` | `web-and-apis` |
| A11 | "Standardize logging across our Node services so one request ID traces a call through all of them, and make sure tokens never reach the logs" | `logging` | `observability-polyglot` |

## Merged twin groups (language named in the prompt)

One must-fire case per merged group gates the `references/` wiring added
on 2026-11-27: the prompt names a language, the merged skill must fire
(and read the matching `references/<lang>.md`), and near neighbours must
not dominate. The graphql and logging groups are covered by A10/A11.

| # | Prompt (as a user would type it) | Must fire | Must not dominate |
| --- | --- | --- | --- |
| A12 | "Our Go service leaks goroutines on every request — find and fix the leak" | `concurrency` | `performance` |
| A13 | "Pass request-scoped values through our Python services without global state" | `context` | `concurrency` |
| A14 | "Our Django ORM fires one query per row in the list endpoint" | `database` | `performance` |
| A15 | "Callers in our Express app can't tell a 404 from a 500 — give them typed errors" | `error-handling` | `api-design-polyglot` |
| A16 | "Make this TypeScript codebase read idiomatic — modern syntax and small habits" | `idioms` | `refactoring` |
| A17 | "Our FastAPI endpoint got slower after the last release — profile it and prove the fix" | `performance` | `observability-polyglot` |
| A18 | "Reorganize our Go module into a standard layout with a lint gate" | `project-structure` | `refactoring` |
| A19 | "Rename this function across our whole Python codebase, safely" | `refactoring` | `project-structure` |
| A20 | "Audit our Node API for injection and leaked secrets before launch" | `security` | `dependency-audit` |
| A21 | "Bump our TypeScript toolchain safely — ES proposals, release notes, Node LTS" | `stay-updated` | `dependency-audit` |
| A22 | "Add property-based tests and benchmarks to our Go package" | `testing` | `unit-testing-polyglot` |
| A23 | "Build a JSON API in Go with middleware order and graceful shutdown" | `web-and-apis` | `api-design-polyglot` |
| A24 | "Our Go service opens a new DB connection per request — set up pooling and context-aware queries properly" | `database` | `web-and-apis` |

## Merged groups

All 14 twin groups were merged into single skills with per-language
`references/` files (progressive disclosure): `database` on 2026-11-27
(pilot: `database-polyglot` + `golang-database` + `python-database` +
`typescript-database`, gated by A14/A24 and collision cases 5/6/15), and
the remaining 13 groups on 2026-11-27 the same way — `error-handling`,
`performance`, `refactoring`, `security`, `stay-updated`, `testing`,
`concurrency`, `context`, `graphql`, `idioms`, `logging`,
`project-structure`, `web-and-apis` — gated by A10–A23. Merging removed
every group's deferral sentences and twin-collision rows.

## Backlog

Coverage accounting (2026-11-27, after merging all 14 twin groups): 23
of 45 skills have a must-fire case (A1–A24 — `database` is the target of
both A14 and A24, so 24 cases cover 23 unique skills): 10
backbone/umbrella skills (A1–A9 + `database`) and 13 merged topic
skills. Still owed: 22 non-covered skills.
Extend per the coverage rule as skills are edited: one must-fire case
rides along with the edit that needs it — do not batch-write cases nobody
has scored. Behavioural scoring needs a model judge; the deterministic
matcher in `scripts/eval_skill_matching.py` is the CI baseline and abstains
on user-style prompts by design.
