# Eval run: starter baseline (activation + collision cases)

- **Date:** 2026-11-27
- **Model / selector:** the Mistral Vibe session model running this eval, manual selection protocol — the model read all 77 skill frontmatter descriptions from `skills/*/SKILL.md` and picked the skill it would load, per trial, in a fresh pass over the descriptions. No external judge, no second model instance.
- **Cases:** 9 activation cases (`../activation-cases.md`) + 12 collision cases (`../collision-cases.md`), 3 trials each = 63 selections.
- **Mechanical baseline:** `scripts/eval_skill_matching.py` (lexical token-overlap ranking). It cannot score these cases — the prompts deliberately avoid description vocabulary — and only catches language-name signals; recorded here as reproducibility tooling, not as a verdict.

## Context cost measured

Total frontmatter description size across the 77 skills: **14 719 chars** (avg 191, min 135, max 381 `security-polyglot`). This is what every session loads before the first user message.

## Per-case verdicts

Verdicts: `T1/T2/T3` = skill the selector would load on each trial.

| Case | Intended winner | T1 | T2 | T3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| A1 | `feature-workflow` | feature-workflow | feature-workflow | feature-workflow | pass |
| A2 | `debugging-polyglot` | debugging-polyglot | debugging-polyglot | debugging-polyglot | pass |
| A3 | `git-workflow-polyglot` | git-workflow-polyglot | git-workflow-polyglot | git-workflow-polyglot | pass |
| A4 | `release-and-changelog` | release-and-changelog | release-and-changelog | release-and-changelog | pass |
| A5 | `docs-polyglot` | docs-polyglot | docs-polyglot | docs-polyglot | pass |
| A6 | `ci-cd-polyglot` | ci-cd-polyglot | ci-cd-polyglot | ci-cd-polyglot | pass |
| A7 | `i18n-polyglot` | i18n-polyglot | i18n-polyglot | i18n-polyglot | pass |
| A8 | `accessibility-polyglot` | accessibility-polyglot | accessibility-polyglot | accessibility-polyglot | pass |
| A9 | `ai-integration-polyglot` | ai-integration-polyglot | ai-integration-polyglot | ai-integration-polyglot | pass |
| C1 | `golang-error-handling` | golang-error-handling | golang-error-handling | golang-error-handling | pass |
| C2 | `error-handling-polyglot` | error-handling-polyglot | error-handling-polyglot | error-handling-polyglot | pass |
| C3 | `dependency-audit` | dependency-audit | dependency-audit | dependency-audit | pass |
| C4 | `security-polyglot` | security-polyglot | **auth-polyglot** | security-polyglot | **fail — collision** |
| C5 | `typescript-database` | typescript-database | typescript-database | typescript-database | pass |
| C6 | `database-polyglot` | database-polyglot | database-polyglot | database-polyglot | pass |
| C7 | `python-performance` | python-performance | python-performance | python-performance | pass |
| C8 | `unit-testing-polyglot` | unit-testing-polyglot | unit-testing-polyglot | unit-testing-polyglot | pass |
| C9 | `testing-polyglot` | testing-polyglot | testing-polyglot | testing-polyglot | pass |
| C10 | `python-logging` | python-logging | python-logging | python-logging | pass |
| C11 | `observability-polyglot` | observability-polyglot | observability-polyglot | observability-polyglot | pass |
| C12 | `code-review-polyglot` | code-review-polyglot | code-review-polyglot | code-review-polyglot | pass |

## Findings

1. **C4 collision (P2 finding):** "passwords hashed with plain sha256 — is that the right approach for the API?" woke `auth-polyglot` on 1 of 3 trials. `auth-polyglot` claims "passwords" while `security-polyglot` claims "crypto"; neither description disambiguates credential-storage crypto review. Fixed in `2026-11-27-auth-polyglot-crypto-pointer.md`.
2. All other 20 cases: intended winner on 3/3 trials, must-stay-quiet skill quiet on 3/3. The umbrella→twin pointers ("when the task names one language prefer its … twin") carry the collision cases C1–C3, C5–C11 as designed.

## Gate verdict

**Red on C4** (one unintended winner in three trials); green on the other 20 cases. This run is the baseline: no description was edited before it.

## Limitations (what this run does not prove)

- Single model, single session, manual selection — not a blind-scored response eval. The substance criteria in the case files (winner's body actually used in the response) need full task runs with responses; this pass measured activation/selection only.
- 21 starter cases cover the workflow backbone, not all 77 skills; the coverage rule in `../activation-cases.md` still applies (one must-fire case per edited skill).
- Trials were independent re-selections by the same model; there is no inter-rater or inter-model variance measured.
