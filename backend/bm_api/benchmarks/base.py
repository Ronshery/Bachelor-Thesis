from __future__ import annotations

import dataclasses
import os.path
import string
from abc import ABC
import random
from typing import Optional, Type, Dict

import pykube
import yaml
from pykube.objects import APIObject


def generate_suffix(length: int):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))


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
    def get_factory(client: pykube.HTTPClient, kind: str) -> Type[APIObject]:
        # use object factory:
        # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
        # - specify 'kind', e.g. 'Sysbench'
        return pykube.object_factory(client, "perf.kubestone.xridge.io/v1alpha1", kind)

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

    def run(self, client: pykube.HTTPClient, *args, **kwargs) -> BenchmarkStartupResult:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    spec = yaml.safe_load(f)
                    # make sure to execute in 'kubestone' namespace
                    spec = self.merge_dicts(spec, {"metadata": {"namespace": "kubestone"}})
                    # add suffix to 'name', so that they are different and
                    # one can schedule multiple benchmarks of one kind simultaneously
                    spec['metadata']['name'] = f"{spec['metadata'].get('name', None)}-{generate_suffix(10)}"
                    # now: run custom logic
                    return self._run(client, spec, *args, **kwargs)
            except Exception as e:
                return BenchmarkStartupResult(success=False, error=str(e))
        else:
            return BenchmarkStartupResult(success=False, error="Job specification configuration file could not be found")

    def _run(self, client: pykube.HTTPClient, spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        node_name: str = args[0].split("@@@")[0]
        spec = self.merge_dicts(spec, {"spec": {"podConfig": {"podScheduling": {"nodeName": node_name}}}})
        result = self.get_factory(client, self.kind)(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, id=spec['metadata']['name'], benchmark_spec=spec)


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    id: Optional[str] = None
    benchmark_spec: Optional[Dict] = None
    error: Optional[str] = None
