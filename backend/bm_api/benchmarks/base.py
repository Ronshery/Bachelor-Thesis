from __future__ import annotations

import dataclasses
import os.path
from abc import ABC
from typing import Optional

import pykube
import yaml


class BaseBenchmark(ABC):
    @property
    def name(self):
        raise NotImplementedError

    @property
    def kind(self):
        raise NotImplementedError

    @property
    def config_path(self):
        raise NotImplementedError

    def run(self, pykube_client: pykube.HTTPClient, *args, **kwargs):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                spec = yaml.safe_load(f)
                # use object factory:
                # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
                # - specify 'kind', e.g. 'Sysbench'
                factory = pykube.object_factory(pykube_client, "perf.kubestone.xridge.io/v1alpha1", self.kind)
                factory(pykube_client, spec).create()
                # now: run custom logic, if any
                if callable(getattr(self, "_run", None)):
                    self._run(pykube_client, *args, **kwargs)

    def _run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        raise NotImplementedError


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    pod: Optional[str]
    benchmark_spec: BaseBenchmark
