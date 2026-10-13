"""Console entrypoint: `vtuber-gen`."""
from __future__ import annotations

import sys

from ai_vtuber_model_generator.bootstrap.app import build_app
from ai_vtuber_model_generator.utils.logging_setup import configure_logging


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    configure_logging()
    app = build_app()
    return app.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())