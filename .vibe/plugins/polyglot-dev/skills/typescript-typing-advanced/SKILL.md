---
name: typescript-typing-advanced
description: Load this skill for advanced TypeScript typing: strict tsconfig, generics, utility types, type guards, branded/nominal types, discriminated unions, and avoiding `any` without losing ergonomics.
---

# Advanced TypeScript Typing

## Strictness baseline

- `strict: true` always; add `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and `noImplicitOverride` when the codebase is ready.
- `verbatimModuleSyntax: true` to make type-only imports explicit.
- Never silence the compiler with `as any` or `@ts-expect-error` without a comment explaining why.

## Generics

- Constrain generics: `<T extends object>` or `<K extends string>` instead of unconstrained `<T>`.
- Prefer generic functions over generic classes unless state is involved.
- Use `infer` in conditional types for extracting types: `type Awaited<T> = T extends Promise<infer U> ? U : T`.

## Utility types

- `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`, `ReturnType`, `Parameters`.
- Write your own when needed: `type DeepReadonly<T> = { readonly [K in keyof T]: ... }`.

## Type narrowing

- Discriminated unions: `{ kind: 'a', ... } | { kind: 'b', ... }` — switch on the discriminant.
- Type guards: `function isUser(x: unknown): x is User { ... }`; `Array.filter(isUser)` narrows automatically.
- `in` operator and `typeof` for primitives; `instanceof` only for classes you control (breaks across realms/versions).

## Nominal (branded) types

```ts
type UserId = string & { readonly __brand: 'UserId' };
function makeUserId(id: string): UserId { return id as UserId; }
```

Prevents mixing up `UserId` and `OrderId` at compile time.

## Function typing

- `type Fn = (a: string) => number` over interfaces with call signatures when simple.
- `overload` signatures for functions with several call shapes; implementation signature stays loose.
- `satisfies` (TS 4.9+) to check a value against a type without widening it: `const cfg = { ... } satisfies Config;`.

## Escape hatches

- `unknown` + narrowing beats `any`; `any` disables checking for everything it touches.
- For untyped third-party code, write a minimal `.d.ts` instead of `any`.
