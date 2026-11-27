---
name: python-typing
description: Load this skill when adding or enforcing type hints in Python: mypy strict, generics, TypeGuard, TypedDict, overloads, and typing the boundaries correctly.
---

# Python Typing

## Start strict, annotate outward

- Public API first, internals after. `mypy --strict` in CI once the core is annotated.
- `disallow_untyped_defs` catches missing annotations; don't silence with `Any` to make it pass.

## The everyday types

```python
from typing import Any, Optional, Union

def find(users: list[User], id: int) -> User | None: ...  # 3.10+ union syntax
```

- `list[T]`, `dict[K, V]`, `tuple[T, ...]` — builtin generics (3.9+), not `typing.List`.
- `X | None` (3.10+) over `Optional[X]`; `X | Y` over `Union`.
- `Any` only at untyped boundaries (JSON in, typed out) — every `Any` is a hole in the net.

## Narrowing

- `TypeGuard` for custom narrowing functions:

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]: ...
```

- `assert isinstance(x, str)` also narrows for mypy — fine in tests and guards.
- `cast(T, x)` when you know better than the checker — comment why.

## Structured shapes

- `TypedDict` for JSON/dict payloads: `class UserDict(TypedDict): id: int; name: str` — `total=False` for partial.
- `Protocol` for structural typing (duck typing with a contract):

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...
```

- `@overload` for functions whose return type depends on argument types.
- `TypeAlias` (3.12) or plain assignment for long type expressions.

## Generics

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...
```

- Constrain with `TypeVar("T", bound=Comparable)` or `TypeVar("T", int, str)`.
- Prefer generics over `Any` when types relate.

## Config (pyproject)

```toml
[tool.mypy]
strict = true
warn_unused_ignores = true
plugins = ["pydantic.mypy"]  # if using pydantic
```

## Rule

Types are documentation that the compiler checks — `mypy --strict` in CI turns them into a contract.

## Related

- Knowledge `python` — Python toolchain and conventions: uv/venv, pyproject.toml, pytest, ruff, mypy, everyday commands.
