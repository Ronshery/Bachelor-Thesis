import pykube
import yaml

from bm_api.benchmarks.base import BaseBenchmark, BenchmarkStartupResult


class CpuBenchmark(BaseBenchmark):
    def run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        with open("config/bmfw_sysbench.yaml") as f:
            dpl = yaml.safe_load(f)
            pykube.Deployment(pykube_client, dpl).create()

            # TODO add pod
            return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)

        raise NotImplementedError

    @property
    def name(self):
        return "CPU"

