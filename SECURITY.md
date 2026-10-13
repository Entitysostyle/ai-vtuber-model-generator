# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.7.x   | yes       |
| 0.6.x   | security fixes only |
| < 0.6   | no        |

## Reporting a vulnerability

Email `security@ai-vtuber-model-generator.dev` with:

- Affected version (`vtuber-gen --version`)
- Windows build (10/11, arch)
- Repro steps or a minimal rig/job file
- Whether the issue is in Python core, the C++ blendshape kernel, the C#
  Unity bridge, or the Java Warudo adapter

We aim to acknowledge within 72 hours.

## Threat model notes

This tool loads third-party rig files (`.moc3`, `.vrm`, `.psd`, `.glb`) and
runs ONNX face-tracking models. Treat all input assets as untrusted:

- `.moc3` parsing goes through the native kernel — fuzz targets live in
  `src/ai_vtuber_model_generator/native/fuzz/`.
- ONNX models are loaded with `onnxruntime` in a subprocess sandbox; do not
  disable this in production.
- The VTS API adapter (`services/vts_client.py`) talks to `localhost:8001`
  by default. Do not point it at a remote host without TLS.
- Never commit a `.env` with a VTS token.

## Out of scope

- Crashes only reproducible with hand-edited binary rigs
- Social engineering of the maintainers
- Anything requiring physical access to the user's machine