from __future__ import annotations

import dataclasses
from abc import ABC
from typing import Optional

import pykube


class BaseBenchmark(ABC):
    @property
    def name(self):
        raise NotImplementedError

    def run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        raise NotImplementedError


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    pod: Optional[str]
    benchmark_spec: BaseBenchmark
