"""Bounded worker pool. CPU-bound blendshape work runs in subprocess pool."""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from contextlib import AbstractContextManager
from typing import Any, Callable

import structlog

log = structlog.get_logger(__name__)


class WorkerPool(AbstractContextManager["WorkerPool"]):
    def __init__(self, size: int = 0, *, max_workers_cap: int = 16) -> None:
        n = size or max(1, (os.cpu_count() or 4) - 1)
        self.size = min(n, max_workers_cap)
        self._exec: ProcessPoolExecutor | None = None

    def __enter__(self) -> "WorkerPool":
        self._exec = ProcessPoolExecutor(max_workers=self.size)
        log.debug("worker_pool.start", size=self.size)
        return self

    def __exit__(self, *exc: object) -> None:
        if self._exec is not None:
            self._exec.shutdown(wait=True, cancel_futures=False)
            self._exec = None

    def map(self, fn: Callable[..., Any], items: list[Any]) -> list[Any]:
        if self._exec is None:
            # synchronous fallback — used by tests and dry runs
            return [fn(x) for x in items]
        return list(self._exec.map(fn, items))