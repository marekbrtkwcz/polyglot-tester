---
name: typescript-idioms
description: Load this skill when writing idiomatic JavaScript/TypeScript: modern syntax, module patterns, array/object idioms, and the small habits that make JS code read cleanly. If the language is not JavaScript/TypeScript, prefer golang-language-idioms or python-idioms.
---

# TypeScript/JavaScript Idioms

## Modern syntax

- `const` by default; `let` only when reassigned. Never `var`.
- Arrow functions for callbacks and short functions; regular `function` for methods that need their own `this` (rare in modern code).
- Template literals over string concatenation.
- Destructuring: `const { name, age = 18 } = user;` and `const [first, ...rest] = items;`.
- Optional chaining `?.` and nullish coalescing `??` (note: `??` only for null/undefined, not falsy).
- `Array.prototype.flat/flatMap`, `Object.fromEntries`, `Object.groupBy` (ES2024) instead of hand-rolled loops.

## Arrays & objects

- Prefer `map`/`filter`/`reduce`/`find`/`some`/`every` over `for` loops when transforming or searching.
- Don't mutate: use spread (`[...items, x]`, `{ ...obj, key: value }`) instead of `push`/`splice`/direct assignment on shared data.
- Use `Set` for membership checks and `Map` for key-value when keys aren't strings.

## Modules & imports

- Named exports over default exports for anything used in more than one place.
- Import type-only imports with `import type { ... }` (or `verbatimModuleSyntax` in tsconfig) so they are erased at runtime.
- One module per file for anything non-trivial; barrel `index.ts` only when it genuinely helps.

## Async style

- `async/await` over raw `.then()` chains; `Promise.all` / `allSettled` for parallelism.
- Always handle rejections: top-level `try/catch` or `.catch()` — an unhandled rejection crashes modern Node.
- Return early (guard clauses) instead of nesting `if` blocks.

## Misc habits

- `Number.isNaN` / `Number.isInteger` over global `isNaN` (which coerces).
- `structuredClone` for deep copies of plain data (not for class instances/functions).
- `Intl` APIs (`Intl.NumberFormat`, `Intl.DateTimeFormat`) instead of hand-rolled formatting.
- Avoid `any`; reach for `unknown` + type narrowing when the type is genuinely unknown.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
