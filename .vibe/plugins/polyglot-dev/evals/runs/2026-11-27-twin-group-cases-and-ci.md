# Run record: twin-group activation cases + CI eval wiring

- **Date**: 2026-11-27
- **Change**: 12 new must-fire activation cases (A12–A23), one per twin
  group with the language named in the prompt, gating the deferral
  sentences added to the 41 twin descriptions in the previous run.
  Coverage is now 23/79 skills with a must-fire case (9 backbone +
  14 twins); 56 skills still owe one (27 twins, 29 non-twins) — see the
  backlog note in `../activation-cases.md`. The deterministic matcher is
  wired into CI as an advisory `skill-evals` job
  (`continue-on-error: true`, never fails the build) per Stage 2 of the
  ai-quality running-evals guidance.

## Mechanical baseline over all 38 cases (scripts/eval_skill_matching.py --top 3)

- 38 cases parsed (23 activation + 15 collision).
- 8 cases: mechanical top-1 == intended winner — A12, A13, A16, A18, A21,
  A23, collision 8 and 15 (the language-named twin cases share real
  vocabulary with the twin descriptions, as expected).
- 18 cases: matcher abstains (all-zero top-3) — by design, case prompts
  avoid description vocabulary.
- 12 cases: winner ranked but not top-1; the mechanical pick is often
  `unit-testing-polyglot`, which shares generic words with many prompts.
  This is a known weakness of a lexical matcher, recorded here rather than
  hidden: the matcher is a regression tripwire, not a judge.

## What was NOT run

- No behavioural (model) run of the 12 new cases: no external judge is
  available in this environment, and the previous manual protocol was
  selection-only. The new cases are therefore written but unscored; the
  next full suite run (3 trials per case, blind scoring) must score them
  before any further twin-description edit.

## Gate verdict

- Structural gates green: 265 tests (case-count assertions updated to
  23 activation + 15 collision = 38), `check_readme_skills.py`,
  `validate_plugin_schema.py`, ruff check + format, markdownlint.
- Behavioural gate: pending, as recorded above.
