"""DAG pipeline: ingest -> process -> drive. Jobs are TOML-described."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import structlog

from ai_vtuber_model_generator.core.job_graph import JobGraph, load_job
from ai_vtuber_model_generator.core.registry import Registry
from ai_vtuber_model_generator.core.worker_pool import WorkerPool

log = structlog.get_logger(__name__)

STAGE_ORDER = ("ingest", "process", "drive")


@dataclass(slots=True)
class PipelineResult:
    ok: bool
    stages_run: list[str] = field(default_factory=list)
    artifacts: dict[str, Path] = field(default_factory=dict)
    elapsed_ms: float = 0.0
    error: str | None = None


class Pipeline:
    """Executes a job graph. Each node resolves to a registered callable."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def execute(self, job_path: Path, *, pool: WorkerPool, dry_run: bool = False) -> PipelineResult:
        t0 = time.perf_counter()
        result = PipelineResult(ok=True)
        try:
            graph: JobGraph = load_job(job_path)
        except Exception as exc:  # noqa: BLE001 - surface as pipeline error
            return PipelineResult(ok=False, error=f"job load failed: {exc}",
                                  elapsed_ms=(time.perf_counter() - t0) * 1000)

        ctx: dict[str, Any] = {"job_path": job_path, "artifacts": {}}
        for stage in STAGE_ORDER:
            nodes = graph.nodes_for(stage)
            if not nodes:
                continue
            log.info("pipeline.stage", stage=stage, nodes=[n.id for n in nodes])
            if dry_run:
                result.stages_run.append(stage)
                continue
            for node in nodes:
                impl = self._registry.resolve(stage, node.kind)
                out = impl(ctx, node.params)
                if out is not None:
                    ctx["artifacts"][node.id] = out
            result.stages_run.append(stage)

        result.artifacts = {k: Path(v) for k, v in ctx["artifacts"].items()}
        result.elapsed_ms = (time.perf_counter() - t0) * 1000
        return result