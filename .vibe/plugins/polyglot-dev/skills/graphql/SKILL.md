---
name: graphql
description: Load this skill when building or consuming GraphQL APIs in JavaScript/TypeScript, Python, or Go — server library choice, schema design, resolvers, dataloaders for N+1, typed errors, and depth/complexity limits. Once the language is known, also read the matching references/ file (go.md, python.md, ts.md) for library-specific depth.
---

# GraphQL

- Schema-first: design types and resolvers before codegen and clients.
- Batch N+1 with dataloaders — never resolve per row in a loop.
- Cap depth/complexity and return typed, safe errors.

## Per-language deep dives

The rules above apply in every language. For tool-specific depth, read the
file for the language in use (relative to this skill's directory):

| Language | File | Covers |
| --- | --- | --- |
| Go | `references/go.md` | server library choice (gqlgen et al.), schema design, resolvers, dataloaders, errors |
| Python | `references/python.md` | Strawberry/Ariadne/Graphene choice, resolvers, DataLoader for N+1, typed errors, depth limits, testing |
| JavaScript/TypeScript | `references/ts.md` | graphql-yoga/Apollo/Pothos, resolvers, dataloaders, errors, depth limits, codegen client |
