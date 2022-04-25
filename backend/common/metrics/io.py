from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class FiosMetrics:
    version: BMMetricField\
        = BMMetricField(r"(fio\-.+)")

    number_of_processes: BMMetricField\
        = BMMetricField(r".*Starting (\d+) process.*")

    write_iops: BMMetricField\
        = BMMetricField(r".*write: IOPS=(\d+).*")

    write_mibps: BMMetricField\
        = BMMetricField(r".*write: BW=(\d+)MiB/s.*")


@dataclasses.dataclass
class IopingsMetrics:
    number_of_requests: BMMetricField\
        = BMMetricField(r"(\d+) requests completed.*")

    total_duration: BMMetricField\
        = BMMetricField(r".*requests completed in ([\d\w\s\.]+)?")

    iops: BMMetricField\
        = BMMetricField(r".*requests completed.*,([\d\w\s\.]+) iops,")

    transfer_bitrate: BMMetricField\
        = BMMetricField(r".*requests completed.*, ([\d\.]+ [\w\/]+)")

    latency_min: BMMetricField\
        = BMMetricField(r"min\/avg\/max\/mdev = ([\d\.]+ \w+)")

    latency_avg: BMMetricField\
        = BMMetricField(r"min\/avg\/max\/mdev = .+?\/ ([\d\.]+ \w+)")

    latency_max: BMMetricField\
        = BMMetricField(r"min\/avg\/max\/mdev = .+?\/ .+?\/ ([\d\.]+ \w+)")

    latency_mdev: BMMetricField\
        = BMMetricField(r"min\/avg\/max\/mdev = .+?\/ .+?\/ .+?\/ ([\d\.]+ \w+)")
