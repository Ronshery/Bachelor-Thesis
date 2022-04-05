from typing import Type, Dict

import pykube
from pykube.objects import APIObject

from bm_api.benchmarks.base import BaseBenchmark, BenchmarkStartupResult


class CpuSysbenchBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Sysbench"

    @property
    def config_path(self):
        return "config/cpu_sysbench.yaml"

    @property
    def name(self):
        return "cpu-sysbench"

    def _run(self, client: pykube.HTTPClient, factory: Type[APIObject], spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        node_name: str = args[0]
        spec = self.merge_dicts(spec, {"spec": {"podConfig": {"podScheduling": {"nodeName": node_name}}}})
        factory(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)

