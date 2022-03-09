import datetime
from typing import Dict

from common.clients.prometheus.client import PrometheusClient

prometheus_client: PrometheusClient = PrometheusClient()


def handle_monitoring(name: str, benchmark_job_dict: Dict[str, dict], logger,
                      started: datetime.datetime,
                      runtime: datetime.timedelta):
    logger.info(f"Monitoring {name}")
    nodes: Dict[str, dict] = {}

    try:
        nodes = prometheus_client.get_node_metrics(started, started + runtime)
    except Exception as e:
        logger.warning("Failed to query metrics! {}".format(e))

    benchmark_job_dict[name] = nodes
    return benchmark_job_dict
