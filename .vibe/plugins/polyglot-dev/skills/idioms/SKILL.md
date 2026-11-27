---
name: idioms
description: Load this skill when writing idiomatic code at the language level in JavaScript/TypeScript, Python, or Go — the constructs and small habits that make code read cleanly in each language. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for that language's idioms.
---

# Language Idioms

- Idiomatic means what a fluent reader expects: guard clauses, early returns, the language's own data structures.
- Prefer the standard library's idiom over cleverness; name things the way the ecosystem names them.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | guard clauses and control flow, var vs :=/iota/shadowing, generics, function style, Stringer |
| Python | `references/python.md` | pythonic constructs, EAFP, context managers, dataclasses, f-strings, dunder methods |
| JavaScript/TypeScript | `references/ts.md` | modern syntax, module patterns, array/object idioms, habits that make JS read cleanly |
