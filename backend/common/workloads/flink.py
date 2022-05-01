from abc import ABC
from typing import Type

import pykube
from pykube.objects import APIObject

from common.clients.k8s import K8sClient
from common.workloads.base import BaseWorkload


class FlinkWorkload(BaseWorkload, ABC):

    @property
    def kind(self):
        return "FlinkDeployment"

    @property
    def name(self):
        return self.__workload_name__

    @classmethod
    def get_factory(cls, client: pykube.HTTPClient, kind: str) -> Type[APIObject]:
        return pykube.object_factory(client, "flink.apache.org/v1alpha1", kind)

    def _run(self, client: K8sClient, automate: bool, spec: dict, *args, **kwargs):
        # set / override some fields
        spec = self.merge_dicts(spec, {"metadata": {"namespace": "flink-operator"}, "spec": {
            "image": "flink:1.14",
            "flinkVersion": "v1_14",
            # https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/operations/metrics-logging/
            "flinkConfiguration": {
                "kubernetes.rest-service.exposed.type": "ClusterIP",
                "metrics.reporters": "prom",
                "metrics.reporter.prom.class": "org.apache.flink.metrics.prometheus.PrometheusReporter",
                "metrics.reporter.prom.port": "9999",
                # annotations below are useless for prometheus-operator, but
                # we add them nevertheless for scenarios where different monitoring solution is used
                "kubernetes.jobmanager.annotations": "prometheus.io/scrape:true,prometheus.io/port:9999",
                "kubernetes.jobmanager.labels": "component:jobmanager",
                "kubernetes.taskmanager.annotations": "prometheus.io/scrape:true,prometheus.io/port:9999",
                "kubernetes.taskmanager.labels": "component:taskmanager"
            },
            # make sure the port can be used
            "podTemplate": {
                "spec": {
                    "containers": [{
                        "name": "flink-main-container",
                        "ports": [{
                            "containerPort": 9999,
                            "name": "metrics"
                        }]
                    }]
                }
            }
        }})
        if automate:
            node_count, per_node_cpu, per_node_memory = self.infer_configuration(client, automate)
            spec = self.merge_dicts(spec, {"spec": {
                "flinkConfiguration": {"taskmanager.numberOfTaskSlots:": str(node_count - 1)},
                "jobManager": {"replicas": 1, "resource": {
                    "cpu": per_node_cpu,
                    "memory": f"{int(per_node_memory / 1000)}m"}},
                "taskManager": {"resource": {
                    "cpu": per_node_cpu,
                    "memory": f"{int(per_node_memory / 1000)}m"}},
                "job": {"parallelism": node_count - 1}
            }})
        return spec

