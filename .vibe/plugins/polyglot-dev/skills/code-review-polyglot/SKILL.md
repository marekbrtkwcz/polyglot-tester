---
name: code-review-polyglot
description: Load this skill when reviewing a diff, PR, or snippet in JavaScript, TypeScript, Python, or Go. Provides a per-language review checklist with common pitfalls and a verdict format.
---

# Code Review (Polyglot)

Review in this order: correctness → security → maintainability → performance →
style. Stop at the first blocker-class finding and report it; do not
nitpick past a real defect.

## Universal checklist

- Does the change do what it claims? Trace the behavior, not the comments.
- Arguments, return values, and exceptions consistent at every call site?
- Error paths handled — not swallowed (`except: pass`, `_ = err`, empty
  `catch`).
- No new dependencies without justification; no dead code left behind.
- Tests exist for the changed behavior and can actually fail.

## JavaScript / TypeScript

- No `any` where a type is knowable; no non-null `!` to silence the checker.
- Async: every promise awaited or explicitly handled; no floating promises.
- `==` vs `===`; truthiness on `0`/`""`.
- Mutating shared/module-level state.
- Imported values from untrusted input treated as data, never executed
  (`eval`, `new Function`, dynamic `import(variable)`).

## Python

- Exceptions caught narrowly (`except ValueError`), never bare `except:`.
- Mutable default arguments (`def f(items=[])`).
- Type hints present on public functions; `Optional` handled at boundaries.
- f-strings fine for logs/messages; parameterized queries for SQL, never
  string formatting.
- Resource handling: `with` blocks; no manual `close()` paths.

## Go

- Every error checked; wrap with context (`fmt.Errorf("doing x: %w", err)`).
- No `_ = err`, no ignored returns on functions that can fail.
- `defer` for cleanup inside the acquiring function; loop-variable capture
  in closures (pre-1.22 code).
- Goroutines: who starts them, who stops them? Every channel has a writer
  until close.
- Zero-value misuse: returning `nil` map/slice where an empty one is expected
  by callers iterating.

## Verdict format

Report each finding as `path:line — severity (blocker/major/minor) — issue —
suggested fix`. End with: merge-ready, fix-first, or needs-rework.

## Related

- `security-polyglot` — a security-focused pass when the diff touches auth, input handling, or secrets.
- `feature-workflow` — the delivery loop this review closes.
