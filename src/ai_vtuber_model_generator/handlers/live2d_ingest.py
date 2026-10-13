"""Ingest a Live2D .moc3 + model3.json pair into a normalized rig bundle."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import structlog

from ai_vtuber_model_generator.handlers.base import IngestError
from ai_vtuber_model_generator.utils.fs import ensure_dir
from ai_vtuber_model_generator.utils.hashing import sha256_file

log = structlog.get_logger(__name__)


def ingest_live2d(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    src = Path(params["source"])
    if not src.exists():
        raise IngestError(f"live2d source missing: {src}")
    model3 = src if src.suffix == ".json" else src / "model3.json"
    if not model3.exists():
        raise IngestError(f"model3.json not found next to {src}")

    meta = json.loads(model3.read_text(encoding="utf-8"))
    moc3 = model3.parent / meta["FileReferences"]["Moc"]
    if not moc3.exists():
        raise IngestError(f"moc3 referenced but missing: {moc3}")

    out = ensure_dir(Path(params.get("out", "rigs_cache")) / sha256_file(moc3)[:12])
    shutil.copy2(moc3, out / "model.moc3")
    shutil.copy2(model3, out / "model3.json")
    (out / "source.txt").write_text(str(src), encoding="utf-8")
    log.info("ingest.live2d", moc3=str(moc3), out=str(out))
    return out