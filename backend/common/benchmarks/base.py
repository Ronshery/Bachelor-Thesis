from __future__ import annotations

import dataclasses
import enum
import os.path
from abc import ABC
from typing import Optional, Type, Dict

import pykube
import yaml
from pykube.objects import APIObject

from common import BaseRun


class BenchmarkedResourceKind(enum.Enum):
    CPU_SYSBENCH = "cpu"
    DISK_FIO = "disk-fio"
    DISK_IOPING = "disk-ioping"
    MEMORY_SYSBENCH = "memory-sysbench"
    NETWORK_IPERF3 = "network-iperf3"
    NETWORK_QPERF = "network-qperf"


class BaseBenchmark(BaseRun, ABC):
    @property
    def config_path(self):
        raise NotImplementedError

    @property
    def resource_kind(self) -> BenchmarkedResourceKind:
        raise NotImplementedError

    @classmethod
    def get_factory(cls, client: pykube.HTTPClient, kind: str) -> Type[APIObject]:
        # use object factory:
        # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
        # - specify 'kind', e.g. 'Sysbench'
        return pykube.object_factory(client, "perf.kubestone.xridge.io/v1alpha1", kind)

    def run(self, client: pykube.HTTPClient, *args, **kwargs) -> BenchmarkStartupResult:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    spec = yaml.safe_load(f)
                    # make sure to execute in 'kubestone' namespace
                    spec = self.merge_dicts(spec, {"metadata": {"namespace": "kubestone"}})
                    # add suffix to 'name', so that they are different and
                    # one can schedule multiple benchmarks of one kind simultaneously
                    spec['metadata']['name'] = f"{spec['metadata'].get('name', None)}-{self.generate_suffix(10)}"
                    # now: run custom logic
                    return self._run(client, spec, *args, **kwargs)
            except Exception as e:
                return BenchmarkStartupResult(success=False, error=str(e))
        else:
            return BenchmarkStartupResult(success=False, error="Job specification configuration file could not be found")

    def _run(self, client: pykube.HTTPClient, spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        node_name: str = args[0].split("@@@")[0]
        spec = self.merge_dicts(spec, {"spec": {"podConfig": {"podScheduling": {"nodeName": node_name}, "podLabels": {"resourceKind": self.resource_kind.value}}}})
        result = self.get_factory(client, self.kind)(client, spec).create()
        return BenchmarkStartupResult(success=True, id=spec['metadata']['name'], benchmark_spec=spec)


@dataclasses.dataclass
class BenchmarkStartupResult:
    success: bool
    id: Optional[str] = None
    benchmark_spec: Optional[Dict] = None
    error: Optional[str] = None
