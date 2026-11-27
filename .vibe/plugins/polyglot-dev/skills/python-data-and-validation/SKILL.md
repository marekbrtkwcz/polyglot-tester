---
name: python-data-and-validation
description: Load this skill when modeling and validating data in Python: pydantic vs attrs vs dataclasses, Protocols for structural types, and validating at system boundaries.
---

# Python Data Modeling & Validation

## Choose the model

| Tool | When |
|---|---|
| `@dataclass` | Internal value objects, no validation needed |
| **pydantic** (v2) | Boundary data: API payloads, config, env — validation + parsing + JSON schema |
| attrs | Performance-sensitive models, `slots` by default, mature ecosystem |
| TypedDict / NamedTuple | JSON-shaped dicts / lightweight records |

## pydantic v2 essentials

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class Signup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12)
    age: int = Field(ge=18)

    @field_validator("password")
    @classmethod
    def no_common(cls, v: str) -> str:
        if v.lower() in {"password", "123456789012"}: raise ValueError("too common")
        return v

user = Signup.model_validate(payload)   # raises ValidationError with all errors
json_str = user.model_dump_json()
```

- Validate **at the boundary** (input, config, env via `BaseSettings`/pydantic-settings), trust inside.
- `model_validate` on dicts, `model_validate_json` on raw JSON; catch `ValidationError` and map to 400 with field errors.
- `model_config = ConfigDict(strict=True)` when you want no coercion (`"1"` → int rejected).

## Structural typing: Protocol

```python
from typing import Protocol
class Repository(Protocol):
    def get(self, id: int) -> User | None: ...
    def save(self, user: User) -> None: ...
```

- "Accept interfaces, return concrete" — the Go rule applies: code against the Protocol, instantiate the real class.

## Enums & literals

- `enum.Enum`/`StrEnum` (3.11+) for closed sets — better than magic strings (typed, exhaustiveness-checkable).
- `Literal["a", "b"]` for small fixed sets in signatures.

## Rules

- One validation layer, at the edge; internal functions can assume valid data (assert in debug if needed).
- Never validate the same thing twice (framework + handler) — pick the layer.
- Error messages for humans: which field, what constraint, what was received.
