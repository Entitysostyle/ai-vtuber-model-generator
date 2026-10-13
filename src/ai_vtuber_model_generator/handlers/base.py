"""Ingest handler protocol. Every handler takes (ctx, params) -> artifact path."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IngestHandler(Protocol):
    kind: str
    extensions: tuple[str, ...]

    def __call__(self, ctx: dict[str, Any], params: dict[str, Any]) -> Path: ...


class IngestError(RuntimeError):
    pass