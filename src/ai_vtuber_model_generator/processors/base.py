from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Processor(Protocol):
    kind: str

    def __call__(self, ctx: dict[str, Any], params: dict[str, Any]) -> Path: ...


class ProcessorError(RuntimeError):
    pass