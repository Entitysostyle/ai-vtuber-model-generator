"""Ingest a VRM 0.x/1.0 avatar via pygltflib, normalize to internal rig."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import structlog

from ai_vtuber_model_generator.handlers.base import IngestError
from ai_vtuber_model_generator.utils.fs import ensure_dir
from ai_vtuber_model_generator.utils.hashing import sha256_file

log = structlog.get_logger(__name__)


def ingest_vrm(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    src = Path(params["source"])
    if src.suffix.lower() != ".vrm":
        raise IngestError(f"expected .vrm, got {src.suffix}")
    try:
        import pygltflib  # type: ignore[import-not-found]
    except ImportError as exc:
        raise IngestError("install extras: pip install -e '.[vrm]'") from exc

    gltf = pygltflib.GLTF2().load(str(src))
    ext = gltf.extensions or {}
    vrm_ext = ext.get("VRM") or ext.get("VRMC_vrm")
    if not vrm_ext:
        raise IngestError("no VRM extension found in glTF")

    out = ensure_dir(Path(params.get("out", "rigs_cache")) / sha256_file(src)[:12])
    shutil.copy2(src, out / "avatar.vrm")
    (out / "source.txt").write_text(str(src), encoding="utf-8")
    log.info("ingest.vrm", src=str(src), out=str(out))
    return out