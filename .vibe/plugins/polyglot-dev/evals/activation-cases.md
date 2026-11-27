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
| A3 | "I'm on main by accident with two finished commits — move them to a branch without losing anything" | `git-workflow-polyglot` | `refactoring-polyglot` |
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
| A10 | "Our Python GraphQL API runs one query per list item — fix the N+1 and make the schema safe against deeply nested queries" | `python-graphql` | `python-web-and-apis` |
| A11 | "Standardize logging across our Node services so one request ID traces a call through all of them, and make sure tokens never reach the logs" | `typescript-logging` | `observability-polyglot` |

## Per-language twins (language named in the prompt)

One must-fire case per twin group gates the deferral sentences added to
the twin descriptions (2026-11-27): the prompt names a language, the
matching twin must fire, and the cross-language siblings must not
dominate. The graphql and logging groups are already covered by A10/A11.

| # | Prompt (as a user would type it) | Must fire | Must not dominate |
| --- | --- | --- | --- |
| A12 | "Our Go service leaks goroutines on every request — find and fix the leak" | `golang-concurrency` | `python-concurrency`, `typescript-async-concurrency` |
| A13 | "Pass request-scoped values through our Python services without global state" | `python-context` | `golang-context` |
| A14 | "Our Django ORM fires one query per row in the list endpoint" | `database` | `performance-polyglot` |
| A15 | "Callers in our Express app can't tell a 404 from a 500 — give them typed errors" | `typescript-error-handling` | `golang-error-handling`, `python-error-handling` |
| A16 | "Make this TypeScript codebase read idiomatic — modern syntax and small habits" | `typescript-idioms` | `golang-language-idioms`, `python-idioms` |
| A17 | "Our FastAPI endpoint got slower after the last release — profile it and prove the fix" | `python-performance` | `golang-performance`, `typescript-performance` |
| A18 | "Reorganize our Go module into a standard layout with a lint gate" | `golang-project-structure` | `python-project-structure`, `typescript-project-structure` |
| A19 | "Rename this function across our whole Python codebase, safely" | `python-refactoring` | `golang-refactoring`, `typescript-refactoring` |
| A20 | "Audit our Node API for injection and leaked secrets before launch" | `typescript-security` | `golang-security`, `python-security` |
| A21 | "Bump our TypeScript toolchain safely — ES proposals, release notes, Node LTS" | `typescript-stay-updated` | `golang-stay-updated`, `python-stay-updated` |
| A22 | "Add property-based tests and benchmarks to our Go package" | `golang-testing-advanced` | `python-testing-advanced`, `typescript-testing-advanced` |
| A23 | "Build a JSON API in Go with middleware order and graceful shutdown" | `golang-web-and-apis` | `python-web-and-apis`, `typescript-web-and-dom` |
| A24 | "Our Go service opens a new DB connection per request — set up pooling and context-aware queries properly" | `database` | `golang-web-and-apis` |

## Merged groups

The database twin group (`database-polyglot`, `golang-database`,
`python-database`, `typescript-database`) was merged into the single
`database` skill with per-language `references/` files on 2026-11-27
(pilot for progressive disclosure): A14 and A24 gate it. Merging removed
the group's deferral sentences and its twin-collision rows (collision
cases 5, 6, 15 now expect `database`).

## Backlog

Coverage accounting (2026-11-27, after the database merge): 23 of 76
skills have a must-fire case (A1–A24 — `database` is the target of both
A14 and A24, so 24 cases cover 23 unique skills): 10 backbone/umbrella
skills (A1–A9 + `database`) and 13 twin skills. Still owed: 25 twin
skills (the other languages in the 13 remaining twin groups) and 28
non-twin skills — 53 total.
Extend per the coverage rule as skills are edited: one must-fire case
rides along with the edit that needs it — do not batch-write cases nobody
has scored. Behavioural scoring needs a model judge; the deterministic
matcher in `scripts/eval_skill_matching.py` is the CI baseline and abstains
on user-style prompts by design.
