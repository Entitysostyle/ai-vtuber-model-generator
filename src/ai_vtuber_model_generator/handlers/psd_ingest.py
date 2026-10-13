"""Ingest a layered PSD (VTuber art source) and split into layer PNGs."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog
from PIL import Image

from ai_vtuber_model_generator.handlers.base import IngestError
from ai_vtuber_model_generator.utils.fs import ensure_dir
from ai_vtuber_model_generator.utils.hashing import sha256_file

log = structlog.get_logger(__name__)


def ingest_psd(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    src = Path(params["source"])
    if src.suffix.lower() != ".psd":
        raise IngestError(f"expected .psd, got {src.suffix}")
    try:
        psd = Image.open(src)
    except Exception as exc:  # noqa: BLE001
        raise IngestError(f"cannot open PSD: {exc}") from exc

    out = ensure_dir(Path(params.get("out", "rigs_cache")) / sha256_file(src)[:12] / "layers")
    # PSD layers are exposed as separate frames by Pillow's PsdImagePlugin.
    n = getattr(psd, "n_frames", 1)
    for i in range(n):
        psd.seek(i)
        name = (psd.info.get("layer_name") or f"layer_{i:03d}").replace("/", "_")
        psd.convert("RGBA").save(out / f"{i:03d}_{name}.png")
    log.info("ingest.psd", src=str(src), layers=n, out=str(out))
    return out.parent