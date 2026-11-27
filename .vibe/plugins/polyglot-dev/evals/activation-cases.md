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

## Backlog

The starter set covers the workflow backbone only. Extend per the
coverage rule as skills are edited: one must-fire case rides along with
the edit that needs it — do not batch-write cases nobody has scored.
