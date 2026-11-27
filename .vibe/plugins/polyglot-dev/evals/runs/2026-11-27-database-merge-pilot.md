# Run: database twin-group merge pilot (progressive disclosure)

Date: 2026-11-27. Scope: merged `database-polyglot` + `golang-database` +
`python-database` + `typescript-database` into a single `database` skill
whose per-language depth lives in `references/go.md`, `references/python.md`,
`references/ts.md` (loaded on demand, Agent Skills pattern). Skill count:
79 → 76; description chars: 18,779 → 18,035 (−744, −4.0%); the group's deferral
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

## Review corrections and keyword hardening (later pass, 2026-11-27)

External review of this pilot found two arithmetic errors, now fixed in
place:

- Description chars were compared apples-to-oranges (with vs without the
  `description: ` prefix): the merge actually went 18,779 → 18,035 chars
  (−744, −4.0%), not 19,806 → 18,035 (−9%). Fixed above and in
  `CHANGELOG.md`.
- Coverage accounting in `evals/activation-cases.md`: A14 and A24 both
  target `database`, so 24 cases cover 23 unique skills of 76 — owed is
  53 (25 twin + 28 non-twin), not 52.

Changes made in this pass:

- `skills/database/SKILL.md` description now names the concrete tools
  (SQL/ORMs, N+1, Prisma, Drizzle, SQLAlchemy, Alembic, sqlc, pgx) —
  313 → 378 chars, collection total 18,035 → 18,100 — so prompts that
  never say "database" still activate the skill. Gated by the must-fire
  cases A14/A24 and the before/after lexical gate below.
- New structure test `test_skill_references_wired_both_ways`
  (`tests/test_plugin_structure.py`): every `references/*.md` must be
  named in SKILL.md, exist, be non-empty and carry no frontmatter; no
  orphans, no dangling names.
- Lexical re-run after the keyword change (same 39 cases, `--top 3`):
  8 agree / 17 abstain / 14 disagree (was 7/18/14). The only verdict that
  moved is collision case C5 ("N+1 queries from Prisma ..."), abstain →
  agree with `database` ranked first; no previously agreeing case flipped.
  `tests/test_eval_skill_matching.py` pins both behaviours.
- Full suite green: 318 tests, ruff (CI rule set) and `ruff format --check`
  clean.

Still NOT run: behavioural scoring with a real model judge, and a live
Vibe session confirming the model reads `references/<lang>.md` after
`database` activates — both remain the gate before merging the other 13
twin groups.

