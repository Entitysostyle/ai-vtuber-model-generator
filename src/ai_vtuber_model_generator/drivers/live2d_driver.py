"""Emit a Live2D-ready bundle: model3.json + moc3 + physics.json + textures."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import structlog

from ai_vtuber_model_generator.drivers.base import DriverError
from ai_vtuber_model_generator.utils.fs import ensure_dir

log = structlog.get_logger(__name__)


def drive_live2d(ctx: dict[str, Any], params: dict[str, Any]) -> Path:
    rig = Path(params["rig"])
    if not rig.exists():
        raise DriverError(f"rig missing: {rig}")
    out = ensure_dir(Path(params.get("out", "outputs")) / f"{rig.name}_live2d")

    for name in ("model.moc3", "model3.json"):
        src = rig / name
        if src.exists():
            shutil.copy2(src, out / name)

    physics = out / "physics.json"
    physics.write_text(json.dumps({"Meta": {"PhysicsSettingCount": 0}, "PhysicsSettings": []},
                                  indent=2), encoding="utf-8")
    log.info("drive.live2d", out=str(out))
    return out