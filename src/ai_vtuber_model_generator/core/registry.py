"""Kind -> callable registry. Handlers/processors/drivers self-register."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

CallableImpl = Callable[[dict[str, Any], dict[str, Any]], Any]


class RegistryError(KeyError):
    pass


class Registry:
    def __init__(self) -> None:
        self._impls: dict[tuple[str, str], CallableImpl] = {}

    def register(self, stage: str, kind: str, impl: CallableImpl) -> None:
        key = (stage, kind)
        if key in self._impls:
            raise RegistryError(f"duplicate registration for {stage}:{kind}")
        self._impls[key] = impl

    def resolve(self, stage: str, kind: str) -> CallableImpl:
        try:
            return self._impls[(stage, kind)]
        except KeyError as exc:
            available = sorted(k for (s, k) in self._impls if s == stage)
            raise RegistryError(
                f"no {stage} handler for kind={kind!r}; available={available}"
            ) from exc

    def kinds(self, stage: str) -> list[str]:
        return sorted(k for (s, k) in self._impls if s == stage)