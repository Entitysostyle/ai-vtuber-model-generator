"""Top-level app wiring: config -> registry -> pipeline -> CLI dispatch."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import structlog

from ai_vtuber_model_generator.config.loader import load_config
from ai_vtuber_model_generator.core.pipeline import Pipeline
from ai_vtuber_model_generator.core.registry import Registry
from ai_vtuber_model_generator.core.worker_pool import WorkerPool
from ai_vtuber_model_generator.drivers import register_default_drivers
from ai_vtuber_model_generator.handlers import register_default_handlers
from ai_vtuber_model_generator.processors import register_default_processors

log = structlog.get_logger(__name__)


@dataclass(slots=True)
class App:
    pipeline: Pipeline
    registry: Registry

    def run(self, argv: list[str]) -> int:
        parser = argparse.ArgumentParser(
            prog="vtuber-gen",
            description="AI VTuber model generator — ingest, process, drive.",
        )
        parser.add_argument("job", type=Path, help="Path to a .job.toml pipeline file")
        parser.add_argument("--config", type=Path, default=None)
        parser.add_argument("--workers", type=int, default=0, help="0 = auto")
        parser.add_argument("--dry-run", action="store_true")
        args = parser.parse_args(argv)

        cfg = load_config(args.config)
        workers = args.workers or cfg.workers
        pool = WorkerPool(size=workers)

        log.info("app.start", job=str(args.job), workers=workers, dry=args.dry_run)
        result = self.pipeline.execute(args.job, pool=pool, dry_run=args.dry_run)
        log.info("app.done", ok=result.ok, stages=result.stages_run, elapsed_ms=result.elapsed_ms)
        return 0 if result.ok else 1


def build_app() -> App:
    registry = Registry()
    register_default_handlers(registry)
    register_default_processors(registry)
    register_default_drivers(registry)
    pipeline = Pipeline(registry=registry)
    return App(pipeline=pipeline, registry=registry)