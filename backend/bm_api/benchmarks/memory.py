from bm_api.benchmarks.base import BaseBenchmark


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
