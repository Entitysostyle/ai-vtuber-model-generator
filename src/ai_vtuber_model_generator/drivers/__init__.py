from ai_vtuber_model_generator.core.registry import Registry
from ai_vtuber_model_generator.drivers.live2d_driver import drive_live2d
from ai_vtuber_model_generator.drivers.unity_driver import drive_unity
from ai_vtuber_model_generator.drivers.vrm_driver import drive_vrm
from ai_vtuber_model_generator.drivers.vts_driver import drive_vts


def register_default_drivers(registry: Registry) -> None:
    registry.register("drive", "live2d", drive_live2d)
    registry.register("drive", "vrm", drive_vrm)
    registry.register("drive", "unity", drive_unity)
    registry.register("drive", "vts", drive_vts)