# Run record: twin deferral sentences in per-language descriptions

- **Date**: 2026-11-27
- **Change**: appended one deferral sentence ("If the language is not
  <Lang>, prefer <siblings>.") to the `description` frontmatter of 41
  per-language skills in the 14 same-topic twin groups. No body edits; no
  skill added or removed (still 79).
- **Gate context**: the before/after gate in `../activation-cases.md`
  requires a must-fire case per skill before its description is edited;
  only 11 of 79 skills have one (recorded backlog). These edits touch only
  twin-group descriptions, so the gate runs on the affected groups.

## What was run

- Lexical baseline (`scripts/eval_skill_matching.py --top 1`): the matcher
  abstains (all-zero) on all 26 case prompts by design, so it cannot score
  this change; it still ranks `golang-error-handling` first on a
  vocabulary-sharing probe ("error handling in Go: wrapping with sentinel
  errors"), and the unit tests pinning that behaviour pass.
- Manual model re-selection was **not** re-run for this change (same
  limitation as the starter baseline: selection-only, no external judge, no
  response-substance scoring). Honest verdict: deferral sentences are
  unverified behaviourally; case 15 in `../collision-cases.md` is the
  must-pass case for the next full suite run.

## Gate verdict

- Structure/lint gates green: 265 tests, description length limit (max now
  394 chars, limit 1024), `check_readme_skills.py`, `validate_plugin_schema.py`,
  ruff (including the Python code blocks inside skills), markdownlint.
- Behavioural gate: **not run** — recorded as the open follow-up together
  with the per-skill must-fire case backlog.
