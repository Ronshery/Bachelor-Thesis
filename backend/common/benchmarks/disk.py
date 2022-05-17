from common.benchmarks import BaseBenchmark
from common.benchmarks.base import BenchmarkedResourceKind


class DiskIopingBenchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Ioping"

    @property
    def resource_kind(self) -> BenchmarkedResourceKind:
        return BenchmarkedResourceKind.DISK_IOPING

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
    def resource_kind(self) -> BenchmarkedResourceKind:
        return BenchmarkedResourceKind.DISK_FIO

    @property
    def config_path(self):
        return "config/disk_fio.yaml"

    @property
    def name(self):
        return "disk-fio"
