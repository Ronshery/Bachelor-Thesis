from abc import ABC
from typing import Type

import pykube
from pykube.objects import APIObject

from common.clients.k8s import K8sClient
from common.workloads.base import BaseWorkload


class SparkWorkload(BaseWorkload, ABC):

    @property
    def kind(self):
        return "SparkApplication"

    @property
    def name(self):
        return self.__workload_name__

    @classmethod
    def get_factory(cls, client: pykube.HTTPClient, kind: str) -> Type[APIObject]:
        return pykube.object_factory(client, "sparkoperator.k8s.io/v1beta2", kind)

    def _run(self, client: K8sClient, automate: bool, spec: dict, *args, **kwargs):
        # set / override some fields
        spec = self.merge_dicts(spec, {"metadata": {"namespace": "spark-operator"}, "spec": {
            "image": "mcd01/spark:v3.1.1-servlet",
            "sparkConf": {
                # metric monitoring + k8s monitoring
                "spark.metrics.conf": "/etc/metrics/conf/metrics.properties",
                "spark.ui.prometheus.enabled": "true",
                "spark.metrics.appStatusSource.enabled": "true",
                "spark.sql.streaming.metricsEnabled": "true",
                "spark.metrics.staticSources.enabled": "true",
                "spark.metrics.executorMetricsSource.enabled": "true",
                "spark.executor.processTreeMetrics.enabled": "true",
                # annotations below are useless for prometheus-operator, but
                # we add them nevertheless for scenarios where different monitoring solution is used
                "spark.kubernetes.driver.annotation.prometheus.io/scrape": "true",
                "spark.kubernetes.driver.annotation.prometheus.io/path": "/metrics/prometheus/ | /metrics/executors/prometheus/",
                "spark.kubernetes.driver.annotation.prometheus.io/port": "4040"
            }
        }})
        if automate:
            node_count, per_node_cpu, per_node_memory = self.infer_configuration(client, automate)
            spec = self.merge_dicts(spec, {"spec": {
                "driver": {"cores": per_node_cpu,
                           "memory": f"{int(per_node_memory / 1000)}m"},
                "executor": {"cores": per_node_cpu,
                             "memory": f"{int(per_node_memory / 1000)}m",
                             "instances": node_count - 1},
            }})
        return spec

