"""Single-process entrypoint for all polyglot-dev pre-tool guards.

hooks.toml used to run four separate `python x.py || python3 x.py`
processes on every shell tool call; this module reads the payload ONCE and
runs every check in one interpreter, cutting the startup cost to a single
process per shell call. write_file/edit payloads are routed to
guard_secrets.py by their own hook, and even if one arrives here,
extract_command never mistakes file content for a shell command.

Checks run in the same order the separate hooks used to run, and the first
blocking check wins. Each guard module keeps its own script and env
disable switch; this entrypoint only shares the payload read.

Fail-open on anything unreadable: the guards must never brick a session.
One deliberate exception: an EMPTY stdin fails closed — the hook runner
always sends a JSON payload, so empty stdin means this process is the
fallback interpreter in a `python guard_all.py || python3 guard_all.py`
chain whose first run already consumed the payload.
"""

import sys

try:
    from guard_destructive import EMPTY, read_payload
    import guard_commit_message
    import guard_destructive
    import guard_secrets
    import prepush_checks
except ImportError:  # pragma: no cover - hook always runs from the plugin dir
    import os

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from guard_destructive import EMPTY, read_payload
    import guard_commit_message
    import guard_destructive
    import guard_secrets
    import prepush_checks

CHECKS = (
    guard_destructive.run_payload,
    guard_secrets.run_payload,
    guard_commit_message.run_payload,
    prepush_checks.run_payload,
)


def main():
    payload = read_payload()
    if payload is EMPTY:
        sys.stderr.write(
            "blocked by polyglot-dev guard: empty stdin, no payload to inspect "
            "(fail-closed)\n"
        )
        return 1
    if payload is None:
        return 0  # never block on a payload we cannot read
    for run in CHECKS:
        if run(payload):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
