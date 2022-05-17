from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class NetworkIperf3Metrics:
    transfer_bitrate: BMMetricField\
        = BMMetricField(r".*(\d+\.\d+\s+Gbits\/sec).*sender")
