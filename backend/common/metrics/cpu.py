from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class SysbenchCpuMetrics:
    version: BMMetricField\
        = BMMetricField(r"^sysbench (.*)")

    num_threads: BMMetricField\
        = BMMetricField(r"^Number of threads: (\d+)")

    prime_numbers_limit: BMMetricField\
        = BMMetricField(r"Prime numbers limit: (\d+)")

    events_per_second: BMMetricField\
        = BMMetricField(r"events per second: (\d+(\.\d+)?)")

    total_time: BMMetricField\
        = BMMetricField(r"total time:\s*(\d+(\.\d+)s)")

    total_number_of_events: BMMetricField\
        = BMMetricField(r"total number of events:\s*(\d+)")

    latency_min: BMMetricField\
        = BMMetricField(r"min:\s*(\d+(\.\d+))")

    latency_avg: BMMetricField\
        = BMMetricField(r"avg:\s*(\d+(\.\d+))")

    latency_max: BMMetricField\
        = BMMetricField(r"max:\s*(\d+(\.\d+))")

    latency_95p: BMMetricField\
        = BMMetricField(r"95th percentile:\s*(\d+(\.\d+))")

    latency_sum: BMMetricField\
        = BMMetricField(r"sum:\s*(\d+(\.\d+))")

    fairness_events: BMMetricField\
        = BMMetricField(r"events \(avg/stddev\):\s*(\d+(\.\d+)/\d+(\.\d+))")

    fairness_exctime: BMMetricField\
        = BMMetricField(r"execution time \(avg/stddev\):\s*(\d+(\.\d+)/\d+(\.\d+))")
