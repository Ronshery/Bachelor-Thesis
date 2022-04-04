import pykube
import yaml

from bm_api.benchmarks.base import BaseBenchmark, BenchmarkStartupResult


class CpuBenchmark(BaseBenchmark):
    def run(self, pykube_client: pykube.HTTPClient, node_name: str) -> BenchmarkStartupResult:
        with open("config/sysbench_cpu.yaml") as f:
            dpl = yaml.safe_load(f)
            # use object factory:
            # - all kubestone benchmarks use api_version = 'perf.kubestone.xridge.io/v1alpha1'
            # - specify 'kind', here: 'Sysbench'
            factory = pykube.object_factory(pykube_client, "perf.kubestone.xridge.io/v1alpha1", "Sysbench")
            factory(pykube_client, dpl).create()

            # TODO add pod
            return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)

        raise NotImplementedError

    @property
    def name(self):
        return "CPU"

