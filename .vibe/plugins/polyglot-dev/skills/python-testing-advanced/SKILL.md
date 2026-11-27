---
name: python-testing-advanced
description: Load this skill when writing serious pytest suites: fixtures and scopes, parametrize, monkeypatch, mocking strategy, hypothesis property tests, and coverage discipline.
---

# Python Testing (Advanced)

## Fixtures

```python
import pytest

@pytest.fixture(scope="module")  # function < class < module < session
def db():
    engine = create_engine(TEST_URL)
    yield engine
    engine.dispose()
```

- `yield` fixtures = setup/teardown in one; teardown runs even on test failure.
- Built-ins: `tmp_path`, `monkeypatch`, `capsys`, `caplog`, `request` — prefer them over hand-rolled versions.
- `conftest.py` for shared fixtures; scope wider than needed wastes time, narrower causes flakes.

## Parametrize

```python
@pytest.mark.parametrize("raw,expected", [
    ("1", 1),
    ("-5", -5),
    pytest.param("abc", None, marks=pytest.mark.xfail),
])
def test_parse(raw, expected): ...
```

- IDs: `ids=["positive", "negative"]` for readable output.

## Mocking strategy

- `unittest.mock.patch` / `monkeypatch.setattr` for replacing dependencies — patch **where it's used**, not where it's defined (`app.service.client`, not `client.library`).
- `mocker` (pytest-mock) for cleaner syntax; stdlib `mock` works without plugins.
- Prefer fakes over mocks for complex behavior; assert on **outcomes**, not on which methods were called (mock-only tests prove nothing).

## Property-based: hypothesis

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)
```

- `settings(max_examples=...)` to bound runtime; `@example(...)` to pin a regression case.
- hypothesis shrinks failures to the minimal input — read the shrunk case in the report.

## Running & coverage

- `pytest -q`, `-k expr`, `--lf` (last failed), `-x`, `--pdb` on failure.
- `pytest --cov=mypkg --cov-report=term-missing --cov-fail-under=80` in CI.
- Coverage measures execution, not correctness — pair with mutation testing (mutmut) for critical logic.

## Rules

- One behavior per test; name describes the outcome (`test_refund_fails_when_amount_negative`).
- Deterministic: fixed data, `freezegun` for time, no network (respx/httpx mock transport).
- Tests must be able to fail — an assertion that can't fail is decoration.
