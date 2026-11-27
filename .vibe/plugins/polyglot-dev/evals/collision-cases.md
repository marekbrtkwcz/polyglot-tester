# Skill activation collision cases

Cases for the highest-risk trigger collisions between this collection's
skills. Each case states the intended winner up front; a run scores whether
the right skill fires and the near neighbour stays quiet. Prompts share no
vocabulary with the descriptions on purpose — they are phrased the way a
user would ask.

Run protocol: every prompt, three trials, same model and settings, with
and without the candidate description edit. Record which skill fired per
trial; disagreeing trials are recorded, not discarded.

## Cross-language vs per-language twins

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 1 | "Add proper error types and wrapping to this Go service — the callers currently can't tell a missing row from a dead database" | `error-handling` | — |
| 2 | "Our checkout keeps returning generic 500s — the Go worker and the Python API both swallow errors, tie them together properly" | `error-handling` | — |
| 3 | "Run the usual npm and pip checks before we ship on Monday — anything known-bad in there?" | `dependency-audit` | `security` |
| 4 | "We keep passwords hashed with plain sha256 somewhere — is that the right approach for the API?" | `security` | — |
| 5 | "We're seeing N+1 queries from Prisma in the orders endpoint" | `database` | `performance` |
| 6 | "Should the new notification service stay on Postgres or move to DynamoDB?" | `database` | — |
| 7 | "Profile the Python ingestion job — it eats 8 GB and takes four minutes, users say it got worse after the last release" | `performance` | — |
| 15 | "Our services are written in different languages and every one of them queries the database in a loop — where do we even start?" | `database` | — |

## Testing pair

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 8 | "Write a few quick tests for `calculate_discount` — it's a pure function, edge cases matter" | `unit-testing-polyglot` | `testing` |
| 9 | "Nothing runs in CI and we have no idea what's covered — get the test story of this repo under control" | `testing` | `unit-testing-polyglot` |

## GraphQL depth vs web framework

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 13 | "Design the schema, resolvers and batching for the new GraphQL API our FastAPI service will expose" | `graphql` | `web-and-apis` |

## Logging vs observability

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 10 | "Thread a request ID through our FastAPI logs so support can trace a ticket" | `logging` | `observability-polyglot` |
| 11 | "We need dashboards: latency per endpoint, error rate, and an alert when checkout starts failing" | `observability-polyglot` | `logging` |
| 14 | "Standardize log format across our Express services and trace one request ID through all of them" | `logging` | `observability-polyglot` |

## Review vs workflow

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 12 | "PR is ready — look over the diff before I merge, especially the auth changes" | `code-review-polyglot` | `feature-workflow` |

## Pass criteria

Per case, scored per trial:

- the intended winner's body is actually used — its structure, checklist, or
  named tools appear in the response (substance, not just the skill name)
- the must-stay-quiet skill's specifics do not dominate the response
- for pairs 1–7: the response does not apply another language's tooling
  (e.g. testify in a Python answer, pytest in a Go answer)

## Twin groups merged (2026-11-27)

All 14 per-language twin groups are now merged into single skills with
`references/` (database first as the pilot, then the remaining 13 the
same way), so the deferral sentences ("If the language is not Go,
prefer ...") are gone: a language-ambiguous request wakes the one merged
skill, and the language-specific depth is read from `references/<lang>.md`
on demand. Cases 1–2, 5–7, 10–11, 13–15 now expect the merged skill and
have no twin to stay quiet. If trials still show the wrong skill waking
on a language-ambiguous prompt, re-run this file's cases before editing
the descriptions again.
