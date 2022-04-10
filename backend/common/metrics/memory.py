from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class SysbenchMemoryMetrics:
    version: BMMetricField\
        = BMMetricField(r"^sysbench (.*)")

    number_of_threads: BMMetricField\
        = BMMetricField(r"Number of threads: (\d+)")

    block_size: BMMetricField\
        = BMMetricField(r"block size: (.*)")

    total_size: BMMetricField\
        = BMMetricField(r"total size: (.*)")

    operation: BMMetricField\
        = BMMetricField(r"operation: (.*)")

    scope: BMMetricField\
        = BMMetricField(r"scope: (.*)")

    total_time: BMMetricField\
        = BMMetricField(r"total time: (.*)")

    total_number_of_events: BMMetricField\
        = BMMetricField(r"total number of events:\s*(\d+)")

    latency_min: BMMetricField\
        = BMMetricField(r"min:\s*(\d+(\.\d+)?)")

    latency_avg: BMMetricField\
        = BMMetricField(r"avg:\s*(\d+(\.\d+)?)")

    latency_max: BMMetricField\
        = BMMetricField(r"max:\s*(\d+(\.\d+)?)")

    latency_95p: BMMetricField\
        = BMMetricField(r"95th percentile:\s*(\d+(\.\d+)?)")

    latency_sum: BMMetricField\
        = BMMetricField(r"sum:\s*(\d+(\.\d+)?)")

    fairness_events: BMMetricField\
        = BMMetricField(r"events \(avg/stddev\):\s*(\d+(\.\d+)/\d+(\.\d+))")

    fairness_exctime: BMMetricField\
        = BMMetricField(r"execution time \(avg/stddev\):\s*(\d+(\.\d+)/\d+(\.\d+))")
