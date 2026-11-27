---
name: typescript-stay-updated
description: Load this skill to stay current with JavaScript/TypeScript: ECMAScript proposals, TS release notes, Node LTS schedule, and a safe upgrade routine for tooling and dependencies. If the language is not JavaScript/TypeScript, prefer golang-stay-updated or python-stay-updated.
---

# Staying Updated (JS/TS)

## Official sources

- TypeScript release notes: typescriptlang.org/docs/handbook/release-notes (and the TS blog for beta announcements).
- ECMAScript proposals: tc39.es/proposals — finished (stage 4) proposals land in the next ES version; check kangax compat tables for engine support.
- Node releases: nodejs.org/en/about/previous-releases — LTS schedule (even versions → LTS in October).
- MDN (developer.mozilla.org) for web platform APIs; web.dev for platform changes and Web Vitals.

## Safe upgrade routine

1. Read the changelog/migration notes for the major bump before upgrading.
2. Upgrade one thing at a time (runtime, then compiler, then linter, then deps) so failures are attributable.
3. Run full typecheck + tests + lint after each step; fix deprecations flagged by the compiler (`--deprecation` in tsc 5.x).
4. Update CI matrix to supported versions; drop EOL versions.

## Adopting new features

- Wait for stage 4 / shipped-in-major-browsers before relying on a JS feature in production; polyfill or transpile otherwise.
- TS: enable new strictness flags incrementally (`noUncheckedIndexedAccess` etc.) — they surface real bugs.
- Prefer platform APIs over polyfills; remove polyfills when baseline support allows (baselinewidelyavailable.dev).

## Dependency hygiene

- Monthly: `npm outdated`, Dependabot/Renovate PRs reviewed, `npm audit fix` for safe fixes.
- Major dep bumps: check migration guides, run E2E tests, watch error tracker after deploy.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
