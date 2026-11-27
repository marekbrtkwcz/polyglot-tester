# Advanced Testing in JS/TS

## Runner choice

- Vitest for Vite projects and most new projects (fast, ESM-native, Jest-compatible API).
- Jest when already present; Node's built-in `node:test` for zero-dependency library code.
- Playwright Test for E2E/API tests — see the test-automation skills.

## Structure

- Colocate `foo.test.ts` next to `foo.ts`, or mirror in `tests/` — pick one convention per repo.
- One behavior per test; name tests as sentences: `it('rejects expired tokens')`.
- Arrange-Act-Assert; build fixtures with factory functions, not copy-pasted literals.

## Mocking

- Mock at the module boundary (`vi.mock`) for I/O, network, time; avoid mocking what you don't own unless it's flaky.
- `vi.useFakeTimers()` for time; `vi.setSystemTime` for dates; always `vi.useRealTimers()` in cleanup.
- Prefer dependency injection over mocking internals — easier to test, clearer design.

## Property-based testing

- fast-check: define properties (round-trips, invariants, idempotence) and let it generate inputs; shrink failures automatically.
- Pin the seed of a failing case as a regression example.

## Assertions that prove something

- Assert behavior, not implementation: `expect(result).toEqual(...)` over "mock was called".
- No tautologies: `expect(x).toBeDefined()` after `x = something` proves nothing.
- Cover error paths and boundaries (empty, max, off-by-one), not just happy path.

## Coverage

- Measure with Vitest's built-in coverage (v8 or istanbul); gate on changed lines (diff coverage), not global percentage.
- 100% coverage ≠ good tests — mutation testing (Stryker) reveals tests that pass without asserting.

## Related skills in other plugins

- `test-automation:writing-playwright-tests-best-practices`, `test-automation:api-playwright-test-developer` — Playwright UI/API test writing when the repo uses Playwright.
- `test-automation:diagnosing-test-failures`, `test-automation:stabilizing-flaky-tests` — failure classification and flake fixing.
- `qa-mcp` — Playwright MCP + Chrome DevTools MCP for live browser debugging, k6 MCP for load tests.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
