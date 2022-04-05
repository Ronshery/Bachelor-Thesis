from typing import Type, Dict

import pykube
from pykube.objects import APIObject

from bm_api.benchmarks.base import BaseBenchmark, BenchmarkStartupResult


class MemorySysbenchBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Sysbench"

    @property
    def config_path(self):
        return "config/memory_sysbench.yaml"

    @property
    def name(self):
        return "memory-sysbench"

    def _run(self, client: pykube.HTTPClient, factory: Type[APIObject], spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        node_name: str = args[0]
        spec = self.merge_dicts(spec, {"spec": {"podConfig": {"podScheduling": {"nodeName": node_name}}}})
        factory(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)
