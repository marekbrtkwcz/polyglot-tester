"""Mutation score gate for the guard scripts.

Reads mutmut's .mutmut-cache sqlite DB, prints the outcome split, and exits
non-zero when the mutation score is below the threshold or the run is
incomplete (untested mutants must fail the gate, never score a partial run).

Caught = ok_killed + bad_timeout + ok_suspicious; not caught = bad_survived;
skipped mutants are excluded from the denominator.
"""

import argparse
import sqlite3
import sys

CAUGHT = ("ok_killed", "bad_timeout", "ok_suspicious")
NOT_CAUGHT = ("bad_survived",)
EXCLUDED = ("skipped",)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "cache", nargs="?", default=".mutmut-cache", help="mutmut sqlite cache"
    )
    parser.add_argument(
        "--min-score", type=float, default=0.80, help="minimum mutation score (0-1)"
    )
    args = parser.parse_args()

    conn = sqlite3.connect(args.cache)
    try:
        rows = dict(conn.execute("SELECT status, COUNT(*) FROM Mutant GROUP BY status"))
    finally:
        conn.close()

    counts = {status: rows.get(status, 0) for status in CAUGHT + NOT_CAUGHT + EXCLUDED}
    untested = rows.get("untested", 0)
    caught = sum(counts[s] for s in CAUGHT)
    survived = sum(counts[s] for s in NOT_CAUGHT)
    scored = caught + survived

    print(
        f"mutation outcomes: killed/timeout/suspicious {caught}, survived {survived}, "
        f"skipped {counts['skipped']}, untested {untested}"
    )

    if scored == 0:
        print(
            "no scored mutants found — is the cache from a finished run?",
            file=sys.stderr,
        )
        return 1
    if untested:
        print(f"run incomplete: {untested} mutants untested", file=sys.stderr)
        return 1

    score = caught / scored
    print(f"mutation score: {caught}/{scored} = {score:.1%}")
    if score < args.min_score:
        print(f"mutation score below gate ({args.min_score:.0%})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
