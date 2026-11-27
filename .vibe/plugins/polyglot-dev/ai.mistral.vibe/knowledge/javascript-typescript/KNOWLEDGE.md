---
name: javascript-typescript
description: Toolchain and conventions for JavaScript and TypeScript projects: package managers, Biome linting, tsconfig strictness, and everyday commands.
display_name: JavaScript & TypeScript
icon: code
---

# JavaScript & TypeScript Reference

## Toolchain

- Runtime/manager: detect from lockfiles — `package-lock.json` (npm),
  `pnpm-lock.yaml`, `bun.lockb` (bun). Use what the repo already uses.
- Lint/format: **Biome** (`biome check .` writes fixes with `--write`;
  `biome format`, `biome lint`). ESLint+Prettier in older repos — do not
  migrate unasked.
- Types: `tsc --noEmit` as the gate. `strict: true` is the baseline.

## tsconfig essentials

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "verbatimModuleSyntax": true,
    "moduleResolution": "bundler",
    "isolatedModules": true
  }
}
```

## Conventions

- Prefer `type` for unions/intersections, `interface` for object shapes open
  to extension — pick one per file and stay consistent.
- Discriminated unions over boolean flags for state.
- `import type` for types when `verbatimModuleSyntax` is on.
- Errors: throw `Error` subclasses with context; never throw strings.
- Env access via a validated config module, not scattered
  `process.env.FOO`.

## Everyday commands

| Task | npm | bun |
|---|---|---|
| install | `npm ci` | `bun install` |
| test | `npm test` | `bun test` |
| typecheck | `npx tsc --noEmit` | `bunx tsc --noEmit` |
| lint+fix | `npx biome check --write .` | `bunx biome check --write .` |

## Gotchas

- `Array.prototype.sort` mutates — copy first (`[...xs].sort()`).
- Object spread is shallow; nested objects need structured cloning.
- `parseInt` without radix; `0.1 + 0.2 !== 0.3` — use integer cents for money.
- `JSON.parse` of untrusted input inside try/catch, never `eval`.

## Official sources

- https://www.typescriptlang.org — handbook, playground, release notes.
- https://www.typescriptlang.org/docs/ — TS Handbook + reference (start here).
- https://nodejs.org/en — Node.js downloads, API docs, release schedule.
- https://nodejs.org/api/ — full Node API reference.
- https://developer.mozilla.org (MDN) — JS language reference and web APIs.
- https://tc39.es/ecma262/ — the ECMAScript specification.
- https://www.npmjs.com — package registry (evaluate packages: maintenance, types, dep tree).
