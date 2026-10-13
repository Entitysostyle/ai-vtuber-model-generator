"""Pack layer PNGs into a single atlas + UV map for the output driver."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog
from PIL import Image

from ai_vtuber_model_generator.processors.base import ProcessorError
from ai_vtuber_model_generator.utils.fs import ensure_dir

log = structlog.get_logger(__name__)


def pack_textures(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    layers_dir = Path(params["layers"])
    if not layers_dir.is_dir():
        raise ProcessorError(f"layers dir missing: {layers_dir}")
    pngs = sorted(layers_dir.glob("*.png"))
    if not pngs:
        raise ProcessorError(f"no PNG layers in {layers_dir}")

    imgs = [Image.open(p).convert("RGBA") for p in pngs]
    max_w = max(i.width for i in imgs)
    atlas = Image.new("RGBA", (max_w, sum(i.height for i in imgs)), (0, 0, 0, 0))
    y = 0
    uv_lines: list[str] = []
    for p, im in zip(pngs, imgs, strict=True):
        atlas.paste(im, (0, y))
        uv_lines.append(f"{p.stem} 0 {y} {im.width} {im.height}")
        y += im.height

    out = ensure_dir(layers_dir.parent / "atlas")
    atlas.save(out / "atlas.png")
    (out / "uv.txt").write_text("\n".join(uv_lines), encoding="utf-8")
    log.info("process.texture", layers=len(pngs), out=str(out))
    return out