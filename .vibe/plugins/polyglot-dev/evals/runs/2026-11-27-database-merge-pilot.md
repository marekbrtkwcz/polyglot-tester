# Run: database twin-group merge pilot (progressive disclosure)

Date: 2026-11-27. Scope: merged `database-polyglot` + `golang-database` +
`python-database` + `typescript-database` into a single `database` skill
whose per-language depth lives in `references/go.md`, `references/python.md`,
`references/ts.md` (loaded on demand, Agent Skills pattern). Skill count:
79 → 76; description chars: 19,806 → 18,035 (−9%); the group's deferral
sentences and twin-collision rows are gone.

## What was run

- `python scripts/eval_skill_matching.py --top 3` over all 39 cases
  (24 activation + 15 collision), lexical baseline only.
- Full pytest suite, ruff (CI rule set), `check_readme_skills.py`,
  `validate_plugin_schema.py` — all green (317 tests).

## Lexical results (39 cases)

- agree with intended winner: 7
- abstain (all-zero, by design on user-style prompts): 18
- disagree: 14

Database-group cases: A24 ranks `database` first (agree); A14, C5, C6, C15
are user-style prompts where the matcher abstains by design (winner outside
the top ranks) — same abstention profile as the pre-merge baseline
(2026-11-27-starter-baseline: 8 agree / 18 abstain / 12 disagree over 38).

## What was NOT run

No behavioural scoring with a real model judge — no external judge is
available in this environment (same limitation as the starter baseline).
The before/after gate from `activation-cases.md` therefore could not be
executed behaviourally; the merge is gated on the lexical baseline plus
structure tests only. Before merging further twin groups, re-run the full
case set on a real model (3 trials per case) and record per-trial verdicts
here — that is the gate for scaling the pilot to the remaining 13 groups.

## Vibe-side verification still owed

Confirm in a live Vibe session that after `database` activates, the model
actually reads `references/<lang>.md` from the skill directory (support
files are read on demand per the skill-creator format) — the lexical
baseline cannot prove that.
