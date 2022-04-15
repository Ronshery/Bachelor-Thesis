from functools import lru_cache

from common.clients.prometheus.client import PrometheusClient


@lru_cache()
def get_prometheus_client():
    return PrometheusClient()
