import pykube

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

    def _run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        # TODO add pod
        return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)

