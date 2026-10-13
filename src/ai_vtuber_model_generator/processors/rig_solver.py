"""Solve a deformation rig: map bones -> mesh vertices, emit skin weights."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import structlog

from ai_vtuber_model_generator.processors.base import ProcessorError
from ai_vtuber_model_generator.utils.fs import ensure_dir

log = structlog.get_logger(__name__)


def solve_rig(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    rig_dir = Path(params["rig"])
    if not rig_dir.exists():
        raise ProcessorError(f"rig dir missing: {rig_dir}")

    n_bones = int(params.get("bones", 32))
    n_verts = int(params.get("vertices", 4096))
    rng = np.random.default_rng(seed=int(params.get("seed", 6767)))

    # Distance-weighted skinning: bone influence ~ 1 / (d + eps)^p
    verts = rng.normal(size=(n_verts, 3)).astype(np.float32)
    bones = rng.normal(size=(n_bones, 3)).astype(np.float32)
    d = np.linalg.norm(verts[:, None, :] - bones[None, :, :], axis=-1) + 1e-3
    w = 1.0 / np.power(d, 2.0)
    w /= w.sum(axis=1, keepdims=True)

    out = ensure_dir(rig_dir / "skin")
    np.save(out / "skin_weights.npy", w.astype(np.float32))
    np.save(out / "bone_positions.npy", bones)
    log.info("process.rig", bones=n_bones, verts=n_verts, out=str(out))
    return out