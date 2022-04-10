from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class NetworkIperf3Metrics:
    transfer_bitrates: BMMetricField\
        = BMMetricField(r".*(\d+\.\d+\s+Gbits\/sec).*", collect_list=True)
