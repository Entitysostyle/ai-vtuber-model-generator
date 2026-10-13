from ai_vtuber_model_generator.core.registry import Registry
from ai_vtuber_model_generator.processors.blendshape_builder import build_blendshapes
from ai_vtuber_model_generator.processors.rig_solver import solve_rig
from ai_vtuber_model_generator.processors.texture_packer import pack_textures


def register_default_processors(registry: Registry) -> None:
    registry.register("process", "blendshape", build_blendshapes)
    registry.register("process", "rig", solve_rig)
    registry.register("process", "texture", pack_textures)