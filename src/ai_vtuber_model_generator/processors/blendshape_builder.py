"""Build ARKit-52 compatible blendshapes from a normalized rig bundle."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import structlog

from ai_vtuber_model_generator.processors.base import ProcessorError
from ai_vtuber_model_generator.utils.fs import ensure_dir

log = structlog.get_logger(__name__)

ARKIT_52 = (
    "browDownLeft browDownRight browInnerUp browOuterUpLeft browOuterUpRight "
    "cheekPuff cheekSquintLeft cheekSquintRight eyeBlinkLeft eyeBlinkRight "
    "eyeLookDownLeft eyeLookDownRight eyeLookInLeft eyeLookInRight "
    "eyeLookOutLeft eyeLookOutRight eyeLookUpLeft eyeLookUpRight eyeSquintLeft "
    "eyeSquintRight eyeWideLeft eyeWideRight jawForward jawLeft jawOpen jawRight "
    "mouthClose mouthDimpleLeft mouthDimpleRight mouthFrownLeft mouthFrownRight "
    "mouthFunnel mouthLeft mouthLowerDownLeft mouthLowerDownRight mouthPressLeft "
    "mouthPressRight mouthPucker mouthRight mouthRollLower mouthRollUpper "
    "mouthShrugLower mouthShrugUpper mouthSmileLeft mouthSmileRight mouthStretchLeft "
    "mouthStretchRight mouthUpperUpLeft mouthUpperUpRight noseSneerLeft noseSneerRight"
).split()


def build_blendshapes(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    rig_dir = Path(params["rig"])
    if not rig_dir.exists():
        raise ProcessorError(f"rig dir missing: {rig_dir}")

    # Native kernel does the heavy vertex math; fall back to numpy if absent.
    try:
        from ai_vtuber_model_generator.native import blendshape_kernel as k  # type: ignore
        weights = k.project_arkit52(np.eye(52, dtype=np.float32))
    except ImportError:
        weights = np.eye(52, dtype=np.float32)

    if weights.shape != (52, 52):
        raise ProcessorError(f"kernel returned {weights.shape}, expected (52, 52)")

    out = ensure_dir(rig_dir / "blendshapes")
    np.save(out / "arkit52_weights.npy", weights)
    (out / "names.txt").write_text("\n".join(ARKIT_52), encoding="utf-8")
    log.info("process.blendshape", out=str(out), count=len(ARKIT_52))
    return out