from typing import Optional
from pydantic import BaseSettings


class PrometheusQuery:
    # percentage values, i.e. 0 <= x <= 100
    MEMORY_USED: str = '100 - ((avg_over_time(node_memory_MemAvailable_bytes[1m]) / ' \
                       'avg_over_time(node_memory_MemTotal_bytes[1m])) * 100)'
    CPU_BUSY: str = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    DISK_IO_UTIL: str = '100 * (sum by (instance) (rate(node_disk_io_time_seconds_total[1m])))'


class PrometheusSettings(BaseSettings):
    prometheus_endpoint: Optional[str] = "http://localhost:9090"
    prometheus_query_step_width: Optional[int] = 10  # in seconds

