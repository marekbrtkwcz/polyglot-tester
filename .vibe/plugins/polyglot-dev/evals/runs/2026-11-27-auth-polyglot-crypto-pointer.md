# Eval run: auth-polyglot crypto pointer (before/after on collision case C4)

- **Date:** 2026-11-27
- **Change under test:** `skills/auth-polyglot/SKILL.md` description gains the disambiguation "For reviewing the crypto choices behind credential storage themselves (hashing, KDFs, parameter choices) prefer security-polyglot."
- **Baseline:** `2026-11-27-starter-baseline.md` — C4 fired `security-polyglot` 2/3, `auth-polyglot` 1/3.
- **Model / selector:** same as baseline — the Vibe session model, manual selection, 3 trials per case, fresh pass over all 77 descriptions per trial.

## After-run verdicts

| Case | Prompt (abbrev.) | Intended | T1 | T2 | T3 | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C4 | passwords hashed with plain sha256 — right approach for the API? | `security-polyglot` | security-polyglot | security-polyglot | security-polyglot | pass (was 2/3) |
| C3 | npm and pip checks before ship — anything known-bad? | `dependency-audit` | dependency-audit | dependency-audit | dependency-audit | pass (no leak) |
| R1 (regression probe) | Add Google OAuth2 login to the app | `auth-polyglot` | auth-polyglot | auth-polyglot | auth-polyglot | pass (no regression) |

R1 is an ad-hoc probe added for this edit, not a case-file row: it checks the edited description still fires on its core claim (OAuth2 login).

## Gate verdict

**Green.** C4 now fires the intended winner 3/3 (was 2/3 with `auth-polyglot` winning one trial), the neighbouring collision row C3 is unchanged, and the edited skill still fires on its own core trigger (R1 3/3). No new leaks observed in the re-run set.

## Limitations

- Same limits as the baseline run: single model, manual selection, selection-only (no response-substance scoring), 3 trials per case.
- The full 21-case suite was not re-run; only the collision group the edit touches (C3, C4) plus the regression probe. Per the coverage rule, the full suite re-runs before the next release.
