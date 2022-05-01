from common.benchmarks import BaseBenchmark


class DiskIopingBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Ioping"

    @property
    def config_path(self):
        return "config/disk_ioping.yaml"

    @property
    def name(self):
        return "disk-ioping"


class DiskFioBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Fio"

    @property
    def config_path(self):
        return "config/disk_fio.yaml"

    @property
    def name(self):
        return "disk-fio"
