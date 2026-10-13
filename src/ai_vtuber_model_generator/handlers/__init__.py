from ai_vtuber_model_generator.core.registry import Registry
from ai_vtuber_model_generator.handlers.live2d_ingest import ingest_live2d
from ai_vtuber_model_generator.handlers.psd_ingest import ingest_psd
from ai_vtuber_model_generator.handlers.vrm_ingest import ingest_vrm


def register_default_handlers(registry: Registry) -> None:
    registry.register("ingest", "live2d", ingest_live2d)
    registry.register("ingest", "vrm", ingest_vrm)
    registry.register("ingest", "psd", ingest_psd)