# Contributing to ai-vtuber-model-generator

Thanks for wanting to push the pipeline forward. This repo is a Windows-first
desktop tool that ingests VTuber source assets (Live2D `.moc3` rigs, VRM
avatars, PSD layer stacks, webcam face-tracking streams), runs them through a
job pipeline, and emits driver-ready outputs for OBS, VTube Studio, Warudo,
and Unity/Unreal.

## Repo shape

```
src/ai_vtuber_model_generator/
  bootstrap/     # entrypoints, DI wiring, config load
  core/          # pipeline scheduler, job graph, worker pool
  handlers/      # ingest handlers (one per source format)
  processors/    # blendshape, rig, texture, tracking processors
  drivers/       # output drivers (Live2D, VRM, Unity, OBS, VTS)
  services/      # external service adapters (VTS API, ONNX runtime)
  models/        # pydantic schemas + dataclasses
  utils/         # fs, logging, hashing, image, math
  config/        # default TOML + schema
  native/        # C++ blendshape kernel (pybind11)
  dotnet/        # C# Unity bridge shim
  java/          # Java Warudo plugin adapter
tests/
```

## Local dev

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,live2d,vrm,unity]"
pytest -q
ruff check src tests
```

Native kernel:
```powershell
pip install pybind11
python src/ai_vtuber_model_generator/native/setup.py build_ext --inplace
```

## Pipeline contract

Every handler implements `IngestHandler` (see `handlers/base.py`).
Every processor implements `Processor` (see `processors/base.py`).
Every driver implements `OutputDriver` (see `drivers/base.py`).

Jobs are DAGs. A job is a list of `(stage, node_id)` edges. Stages run in
this fixed order: `ingest -> process -> drive`. Do not add stages without an
RFC issue.

## Style

- `ruff` line length 100, target py311.
- Type hints mandatory on public functions.
- No `print()` — use `structlog` via `utils/logging_setup.py`.
- Native code: C++20, `-Wall -Wextra -Werror` on MSVC.
- C# shim: net8.0, nullable enabled.
- Java adapter: Java 17, no reflection on Warudo internals unless guarded.

## PR checklist

- [ ] Tests pass locally on Windows 11 + Python 3.11
- [ ] New handler/processor/driver has a unit test under `tests/`
- [ ] Public API changes noted in `docs/CHANGELOG.md`
- [ ] No generated rigs or model weights committed

## Community

We hang out in the `#rigging` and `#tracking` channels. Be decent. Ship code.