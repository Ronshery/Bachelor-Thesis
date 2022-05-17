from common.benchmarks.base import BaseBenchmark, BenchmarkedResourceKind


class CpuSysbenchBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Sysbench"

    @property
    def resource_kind(self) -> BenchmarkedResourceKind:
        return BenchmarkedResourceKind.CPU_SYSBENCH

    @property
    def config_path(self):
        return "config/cpu_sysbench.yaml"

    @property
    def name(self):
        return "cpu-sysbench"

