from bm_api.benchmarks.base import BaseBenchmark


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

