"""Emit a VRM avatar with ARKit-52 blendshape proxies baked in."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import numpy as np
import structlog

from ai_vtuber_model_generator.drivers.base import DriverError
from ai_vtuber_model_generator.utils.fs import ensure_dir

log = structlog.get_logger(__name__)


def drive_vrm(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    rig = Path(params["rig"])
    src_vrm = rig / "avatar.vrm"
    if not src_vrm.exists():
        raise DriverError(f"avatar.vrm missing under {rig}")
    out = ensure_dir(Path(params.get("out", "outputs")) / f"{rig.name}_vrm")
    shutil.copy2(src_vrm, out / "avatar.vrm")

    bs = rig / "blendshapes" / "arkit52_weights.npy"
    if bs.exists():
        w = np.load(bs)
        np.save(out / "ark