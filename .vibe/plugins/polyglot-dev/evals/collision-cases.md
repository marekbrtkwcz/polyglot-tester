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
| 1 | "Add proper error types and wrapping to this Go service — the callers currently can't tell a missing row from a dead database" | `golang-error-handling` | `error-handling-polyglot` |
| 2 | "Our checkout keeps returning generic 500s — the Go worker and the Python API both swallow errors, tie them together properly" | `error-handling-polyglot` | neither twin alone |
| 3 | "Run the usual npm and pip checks before we ship on Monday — anything known-bad in there?" | `dependency-audit` | `security-polyglot` |
| 4 | "We keep passwords hashed with plain sha256 somewhere — is that the right approach for the API?" | `security-polyglot` | — |
| 5 | "We're seeing N+1 queries from Prisma in the orders endpoint" | `typescript-database` | `database-polyglot` |
| 6 | "Should the new notification service stay on Postgres or move to DynamoDB?" | `database-polyglot` | any `*-database` twin |
| 7 | "Profile the Python ingestion job — it eats 8 GB and takes four minutes, users say it got worse after the last release" | `python-performance` | `performance-polyglot` |

## Testing pair

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 8 | "Write a few quick tests for `calculate_discount` — it's a pure function, edge cases matter" | `unit-testing-polyglot` | `testing-polyglot` |
| 9 | "Nothing runs in CI and we have no idea what's covered — get the test story of this repo under control" | `testing-polyglot` | `unit-testing-polyglot` |

## Logging vs observability

| # | Prompt (as a user would type it) | Winner | Must stay quiet |
| --- | --- | --- | --- |
| 10 | "Thread a request ID through our FastAPI logs so support can trace a ticket" | `python-logging` | `observability-polyglot` |
| 11 | "We need dashboards: latency per endpoint, error rate, and an alert when checkout starts failing" | `observability-polyglot` | `python-logging` |

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

## Known limitation

The per-language twins do not yet name their cross-language sibling, so a
request spanning two languages may still wake the wrong twin. If trials
show that, add the reverse pointer to the twin's description.
