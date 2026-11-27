# JS/TS Diagnostics Reference

Companion to the `debugging-polyglot` skill: the commands that answer
"where does it break".

## Pin down a failure

| Question | How |
|---|---|
| What exactly failed? | Read the stack bottom-up; first frame in your code = entry point |
| One test only? | `npx vitest run path/to/file.test.ts -t "test name"` |
| Is it types or runtime? | `npx tsc --noEmit` first — half of "runtime bugs" are type bugs |
| What does it print? | `console.log`/`console.trace` at the boundary where data enters |
| Deadlock/never-resolving? | Log each promise before/after await; look for a missing await |

## Tooling

- Debugging: `node --inspect`, Chrome DevTools; Vitest: `--inspect-brk` +
  "attach" launch config.
- Unhandled rejections: run with `--unhandled-rejections=strict` so they
  crash loudly instead of being swallowed.
- Timing: fake timers (`vi.useFakeTimers()`) — never a real `setTimeout` in
  a reproduction.

## Reading a Vitest/Jest failure

1. `AssertionError: expected 5, received 4` — compare actual vs expected
   before opening the test file.
2. `Test timed out` — an unawaited promise or an infinite loop, not a slow
   machine.
3. `Cannot read properties of undefined` — trace where the value is
   *produced*, not where it is *read*.
