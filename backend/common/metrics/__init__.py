from typing import Type

from pykube import Pod

from .common import TMetricClass, read_benchmark_metrics
from .cpu import SysbenchCpuMetrics
from .memory import SysbenchMemoryMetrics
from .network import NetworkIperf3Metrics


def get_benchmark_metrics(cls: Type[TMetricClass], pod: Pod) -> TMetricClass:
    lgs = pod.logs().splitlines(keepends=False)
    values = read_benchmark_metrics(cls, lgs)
    return values
