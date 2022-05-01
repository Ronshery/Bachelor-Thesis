from typing import Type

import kopf
import pykube
from pykube.objects import APIObject

from common.clients.k8s import K8sClient, get_k8s_client
from common.executing import handle_running_workload
from common.workloads.flink import FlinkWorkload
from common.workloads.spark import SparkWorkload

k8s_client: K8sClient = get_k8s_client()


@kopf.on.create('peronaworkloads')
def create_workload(namespace, name, logger, body, **kwargs):
    automate: bool = body.get("automate", True)
    spark_spec: dict = body.get("sparkSpec", {})
    SparkWorkload(spark_spec).run(logger, k8s_client, namespace, automate, spark_spec)
    flink_spec: dict = body.get("flinkSpec", {})
    FlinkWorkload(flink_spec).run(logger, k8s_client, namespace, automate, flink_spec)
    # now: delete this wrapper object
    factory_instance: Type[APIObject] = pykube.object_factory(k8s_client.api, "kopf.dev/v1", "PeronaWorkload")
    obj = factory_instance.objects(k8s_client.api, namespace=namespace).get_by_name(name).obj
    factory_instance(k8s_client.api, obj).delete()


@kopf.daemon("sparkapplications")
def handle_spark_workload(namespace, name, logger, started, stopped, body, **_):
    handle_running_workload(namespace, name, logger, started, stopped, body)


@kopf.daemon("flinkdeployments")
def handle_flink_workload(namespace, name, logger, started, stopped, body, **_):
    handle_running_workload(namespace, name, logger, started, stopped, body)


