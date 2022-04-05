import pykube

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

    #def _run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
    #    raise NotImplementedError
