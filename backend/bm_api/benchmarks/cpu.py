import pykube

from base import BaseBenchmark
from bm_api.benchmarks.base import BenchmarkStartupResult


class CpuBenchmark(BaseBenchmark):
    def run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        raise NotImplementedError

    @property
    def name(self):
        return "CPU"

