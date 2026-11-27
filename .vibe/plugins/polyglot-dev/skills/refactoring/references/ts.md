# Safe Refactoring (JS/TS)

## Process

1. Read the target module **and its importers** (`git grep` for the symbol, check barrel files `index.ts`).
2. Confirm vitest/jest, `tsc --noEmit`, and eslint/biome are green BEFORE touching anything. Missing coverage on the target? Add characterization tests first.
3. One transformation per step, each step green: rename → extract → move → change signature.
4. Never mix a refactor with a behavior change in one commit; never weaken a test to make the refactor pass.

## Mechanical tools

- **Rename/move**: IDE (tsserver) "Rename Symbol" / "Move to file" — updates all imports across the project. Verify with `git grep <oldName>` afterwards.
- After each step: `tsc --noEmit` catches signature drift, eslint/biome (`--select F401`-style unused-import rules) catches dead imports, tests catch behavior drift.
- Type the boundaries first: a well-typed module makes `tsc` the safety net for the refactor.

## Common safe moves

- **Extract function** with explicit params and return type — no closure over mutable module state.
- **Extract component/hook** when a block of JSX/logic has a name-able purpose (React); keep props typed.
- **Parameter object** when a function grows past ~4 params — an options object with an interface.
- **Replace conditional chains** with a `Record<string, Handler>` dispatch when the branch list grows.
- **Move files by feature**, not by kind (`features/user/` not `components/` + `hooks/` + `types/`); update barrel exports and deprecate old paths if public.
- Enable strict flags incrementally (`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`) — they surface real bugs during the refactor; fix them as part of the step.

## Behavior preservation

- `tsc --noEmit` before and after should show the same (zero) errors.
- Run the full test suite after every step, not just at the end.
- Delete dead code completely — no commented-out blocks, no `// eslint-disable` left behind by the move.

## When to stop

- If a step breaks the build and the fix isn't obvious in minutes, revert that step (`git checkout -- <file>` is safe here — only your uncommitted step is lost) and report the state.
- Right before a release, or without tests on the moved code — don't refactor then.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
