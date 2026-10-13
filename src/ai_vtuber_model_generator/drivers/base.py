from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class OutputDriver(Protocol):
    kind: str

    def __call__(self, ctx: dict[str, Any], params: dict[str, Any]) -> Path: ...


class DriverError(RuntimeError):
    pass