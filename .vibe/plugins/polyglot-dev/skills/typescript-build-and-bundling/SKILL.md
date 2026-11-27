---
name: typescript-build-and-bundling
description: Load this skill for building and bundling JS/TS: tsc vs bundlers, ESM/CJS output, declaration files, Vite/Rollup/esbuild/tsup choices, and library packaging.
---

# Build & Bundling

## tsc vs bundler

- `tsc` for type checking and simple transpile (`tsc --noEmit` in CI; emit only for libs).
- Bundlers (Vite, Rollup, esbuild, webpack, tsup, rspack) resolve imports, transpile, and bundle for apps/libs.
- Rule of thumb: apps → bundler; libraries → `tsup`/`tsc` + `arethetypeswrong` check; never ship raw TS to consumers.

## Library packaging

- Emit ESM + CJS + `.d.ts` (tsup does all three); `exports` map with `types` first.
- Check with `arethetypeswrong` (attw) — catches broken `exports`/`types` resolution per consumer.
- Mark side-effect-free (`sideEffects: false`) so bundlers can tree-shake; keep CSS imports out of `sideEffects: false` packages unless listed.

## App bundling

- Vite for most apps (dev server + Rollup build); esbuild for speed-critical builds; webpack/rspack when ecosystem plugins are needed.
- Code-split by route; dynamic `import()` for heavy, rarely used modules.
- Source maps in production only as `hidden` (upload to error tracker, don't serve publicly) or omit.

## Declarations

- `declaration: true` + `declarationMap` for libs; `stripInternal` with `/** @internal */` for non-public API.
- Keep public types stable — d.ts is your API contract.

## Environments

- Define env vars at build time only for truly static config (`import.meta.env.MODE`, `define` in Vite); runtime config belongs to env/fetch, not build.
- Target modern output (`ES2022`+) unless you must support old browsers; let `browserslist`/Vite `build.target` handle transpile level.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
