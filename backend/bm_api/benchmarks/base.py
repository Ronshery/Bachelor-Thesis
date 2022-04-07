from __future__ import annotations

import dataclasses
import os.path
from abc import ABC
from typing import Optional, Type, Dict

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

    def get_factory(self, client: pykube.HTTPClient) -> Type[APIObject]:
        # use object factory:
        # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
        # - specify 'kind', e.g. 'Sysbench'
        return pykube.object_factory(client, "perf.kubestone.xridge.io/v1alpha1", self.kind)

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
                # now: run custom logic
                self._run(client, spec, *args, **kwargs)

    def _run(self, client: pykube.HTTPClient, spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        node_name: str = args[0].split("@@@")[0]
        spec = self.merge_dicts(spec, {"spec": {"podConfig": {"podScheduling": {"nodeName": node_name}}}})
        self.get_factory(client)(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    pod: Optional[str]
    benchmark_spec: BaseBenchmark
