# Python Idioms

## Pythonic constructs

- Comprehensions over map/filter loops when readable: `[x.name for x in users if x.active]`.
- `in` for membership (works on str, list, dict keys, set — O(1) for set/dict).
- Tuple unpacking: `a, b = b, a` (swap), `first, *rest = items`.
- `enumerate` / `zip` / `zip(strict=True)` (3.10+) instead of index loops.
- `any()` / `all()` for boolean reductions.

## EAFP over LBYL

Ask forgiveness, not permission:

```python
# good (EAFP)
try:
    value = mapping[key]
except KeyError:
    value = default

# avoid (LBYL) unless the check is genuinely cheaper
if key in mapping:
    value = mapping[key]
```

## Context managers

- `with` for anything with cleanup: files, locks, DB sessions/transactions, `contextlib.closing`.
- Custom: `__enter__`/`__exit__` or `@contextlib.contextmanager` (yield once).

## Dataclasses & friends

- `@dataclass` for value objects (auto `__init__`/`__repr__`/`__eq__`); `frozen=True` for immutables/hashable; `slots=True` (3.10+) to cut memory.
- `field(default_factory=list)` — never a mutable default argument.
- `NamedTuple` for lightweight records with attribute access; `TypedDict` for JSON-shaped dicts.

## Strings

- f-strings for interpolation: `f"user {user.id} failed"` — not `"%s" % x` or `.format`.
- f-string debug: `f"{value=}"` (3.8+) prints name and value.
- Raw strings `r"..."` for regex/paths on Windows; triple quotes for multi-line.

## Dunder methods worth implementing

- `__repr__` (unambiguous, for devs), `__str__` (for users) — if you write one, write both.
- `__eq__` via dataclass; `__hash__` only when immutable (frozen dataclass does it).
- `__len__`, `__iter__`, `__contains__` to make objects behave like collections.
- `__enter__`/`__exit__` for context managers.

## Anti-patterns

- `type(x) == int` — use `isinstance(x, int)` (subclasses!).
- Mutable default args: `def f(items=[])` — always `None` + assign inside.
- Bare `except:` — always name the exception.
- `return None` vs `return` — pick one style per function.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
