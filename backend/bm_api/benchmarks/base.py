from __future__ import annotations

import dataclasses
import os.path
from abc import ABC
from typing import Optional, Type, Any, Dict

import pykube
import yaml
from pykube.objects import APIObject


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

    @staticmethod
    def merge_dicts(tgt, enhancer):
        for key, val in enhancer.items():
            if key not in tgt:
                tgt[key] = val
                continue

            if isinstance(val, dict):
                if not isinstance(tgt[key], dict):
                    tgt[key] = dict()
                BaseBenchmark.merge_dicts(tgt[key], val)
            else:
                tgt[key] = val
        return tgt

    def run(self, client: pykube.HTTPClient, *args, **kwargs):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                spec = yaml.safe_load(f)
                # make sure to execute in 'kubestone' namespace
                spec = self.merge_dicts(spec, {"metadata": {"namespace": "kubestone"}})
                # use object factory:
                # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
                # - specify 'kind', e.g. 'Sysbench'
                factory: Type[APIObject] = pykube.object_factory(client, "perf.kubestone.xridge.io/v1alpha1", self.kind)
                # now: run custom logic
                try:
                    self._run(client, factory, spec, *args, **kwargs)
                except NotImplementedError:
                    pass

    def _run(self, client: pykube.HTTPClient, factory: Type[APIObject], spec: Dict, *args, **kwargs):
        raise NotImplementedError


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    pod: Optional[str]
    benchmark_spec: BaseBenchmark
