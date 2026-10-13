"""Job graph: TOML-described DAG of (stage, kind, id, params) nodes."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True, frozen=True)
class JobNode:
    id: str
    stage: str
    kind: str
    params: dict[str, Any]


@dataclass(slots=True)
class JobGraph:
    name: str
    nodes: list[JobNode]

    def nodes_for(self, stage: str) -> list[JobNode]:
        return [n for n in self.nodes if n.stage == stage]


def load_job(path: Path) -> JobGraph:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    name = raw.get("job", {}).get("name", path.stem)
    nodes: list[JobNode] = []
    for entry in raw.get("nodes", []):
        nodes.append(
            JobNode(
                id=entry["id"],
                stage=entry["stage"],
                kind=entry["kind"],
                params=entry.get("params", {}),
            )
        )
    if not nodes:
        raise ValueError(f"job {path} has no [[nodes]]")
    return JobGraph(name=name, nodes=nodes)