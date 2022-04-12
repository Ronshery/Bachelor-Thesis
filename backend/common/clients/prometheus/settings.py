from typing import Optional
from pydantic import BaseSettings


class PrometheusQuery:
    # percentage values, i.e. 0 <= x <= 100
    MEMORY_USED: str = '100 - ((avg_over_time(k8s_node_node_memory_MemAvailable_bytes[30s]) / avg_over_time(' \
                  'k8s_node_node_memory_MemTotal_bytes[30s])) * 100) '
    CPU_BUSY: str = '100 - (avg by (instance) (rate(k8s_node_node_cpu_seconds_total{mode="idle"}[30s])) * 100)'
    DISK_IO_UTIL: str = '100 * (sum by (instance) (rate(k8s_node_node_disk_io_time_seconds_total[30s])))'


class PrometheusSettings(BaseSettings):
    prometheus_endpoint: Optional[str] = "http://prometheus-kube-prometheus-prometheus.prometheus.svc.cluster.local:9090"
    prometheus_query_step_width: Optional[int] = 5  # in seconds

