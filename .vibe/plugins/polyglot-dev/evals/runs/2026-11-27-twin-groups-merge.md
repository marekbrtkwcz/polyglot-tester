# Run: merge the remaining 13 twin groups (scale-up of the database pilot)

Date: 2026-11-27. Scope: merged the 13 remaining twin groups into single
skills with per-language `references/` files, exactly the pattern of the
database pilot (`2026-11-27-database-merge-pilot.md`):

- umbrella groups (former `*-polyglot` + 3 twins): `error-handling`,
  `performance`, `refactoring`, `security`, `stay-updated`, `testing`
- twin-only groups: `concurrency` (incl. `typescript-async-concurrency`),
  `context` (Go/Python only), `graphql`, `idioms` (incl.
  `golang-language-idioms`), `logging`, `project-structure`, `web-and-apis`
  (TS twin was `typescript-web-and-dom` — browser DOM/fetch depth lives in
  its `references/ts.md`)

Skill count: 76 → 45. Description chars: 18,100 → 10,934 (−7,166, −39.6%).
Every group's deferral sentences ("If the language is not Go,
prefer ...") and twin-pointer sections are gone; each merged SKILL.md names
its `references/*.md` in the description and in a "Per-language deep dives"
table. Twin bodies moved unchanged (frontmatter stripped).

## What was run

- Full pytest suite (repo `tests/` + plugin `tests/`): 318 passed —
  includes `test_skill_references_wired_both_ways` over all 14 merged skills.
- `python -m ruff check --isolated --select E4,E7,E9,F` and
  `ruff format --check` (CI rule set): clean.
- `python scripts/check_readme_skills.py`: all 45 skills documented, no
  stale entries.
- `python scripts/validate_plugin_schema.py`: plugin.json valid.
- markdownlint-cli2 0.24.2 over README/CHANGELOG/plugin docs (CI command):
  0 issues in 116 files.
- `python scripts/eval_skill_matching.py --top 3` over all 39 cases
  (24 activation + 15 collision), lexical baseline only.

## Lexical results (39 cases)

- agree with intended winner: 13
- abstain (all-zero, by design on user-style prompts): 19
- disagree: 7 (A3, A11, A15, C2, C3, C7, C14)

Baseline comparison: post-pilot run was 8 agree / 17 abstain / 14 disagree
over the same 39 cases — agreeing cases went up, disagreements down; no
case that agreed after the pilot flipped. The disagreements are the usual
lexical-baseline noise (e.g. C3 "npm and pip checks" ranks `security`
over `dependency-audit` on shared tokens; A15 "404 vs 500 typed errors"
shares "errors" with `graphql`'s "typed errors"). The pinned matcher test
still has `database` first on the N+1/Prisma prompt and `error-handling`
first on the Go sentinel-errors prompt.

## Eval case updates

- `activation-cases.md`: A10–A23 winners are the merged skills; must-not
  cells now name a surviving near neighbour (e.g. A15 `error-handling` must
  not be dominated by `api-design-polyglot`); "Merged groups" and backlog
  accounting updated (24 cases cover 23 of 45 skills; 22 owed).
- `collision-cases.md`: cases 1–4, 7–11, 13–14 expect merged skills and
  have no twin to stay quiet; the deferral note now describes the merged
  state.
- `tests/test_eval_skill_matching.py`: skill count 76 → 45, collision case
  1 winner and the Go error-handling rank expectation updated.
- README component table: 38 twin rows removed, 6 umbrella rows renamed,
  7 rows added for the twin-only groups; intro point 3 now describes
  references/ on-demand loading. Agent TOMLs (`performance-profiler`,
  `refactorer`, `security-auditor`, `test-runner`) and knowledge
  cross-references point at the merged skill paths.

## What was NOT run

No behavioural scoring with a real model judge — no external judge is
available in this environment (same limitation as the pilot). The
before/after gate from `activation-cases.md` therefore remains lexical +
structure tests only.

## Vibe-side verification (live session, updated 2026-11-27)

The activation → on-demand read hop is now observed end to end in a live
Vibe session: `skill polyglot-dev:database` resolved the merged skill, its
body shows the "Per-language deep dives" table, the loader advertises
`references/go.md`, `references/python.md`, `references/ts.md` in
`<skill_files>`, and a live `read_file` of the activated skill's
`references/ts.md` returned the real TS database content (Prisma vs Drizzle
vs pg, pooling). The mechanism is supported per `vibe:skill-creator`
(support files read with `read_file` on demand) and the wiring is enforced
by `test_skill_references_wired_both_ways` over all 14 merged skills.

Caveat: a running session serves a startup snapshot of the skill registry —
this session (started after the database pilot, before a1b96b4) sees
`database` but not the 13 groups merged in a1b96b4 (`skill
polyglot-dev:error-handling` is rejected mid-session; new skill
directories are not picked up until restart). So the last confirmation is
one prompt in a fresh Vibe session after this commit — e.g. "N+1 queries
from Prisma" should activate `database` + read `references/ts.md`, and "Go
error wrapping with sentinels" should activate `error-handling` + read
`references/go.md`. The disk state they load is committed and
structure-tested, and the lexical matcher already ranks both merged skills
first on those prompts.

## Gate verdict

Lexical baseline improved (8/17/14 → 13/19/7), structure and CI checks
green, README/schema/lint clean. Merging scaled as intended. Behavioural
model-judge scoring and the fresh-session activation observation remain
the owed next step before relying on activation behaviour end to end.
