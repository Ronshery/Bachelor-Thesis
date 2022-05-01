import time
from typing import List, Tuple, Type, Optional
import datetime
import pykube
from pykube.objects import APIObject

from common.clients.k8s import K8sClient, get_k8s_client


def handle_running_workload(namespace: str,
                            name: str,
                            logger,
                            started: datetime.datetime,
                            stopped,
                            body: dict,
                            **_):

    logger.info(f"{name}: started: {started}, {body['spec']}")

    k8s_client: K8sClient = get_k8s_client()

    kind: str = body["kind"]
    factory_instance: Type[APIObject] = pykube.object_factory(k8s_client.api,
                                                              "flink.apache.org/v1alpha1" if "Flink" in kind
                                                              else "sparkoperator.k8s.io/v1beta2",
                                                              kind)

    while not stopped:
        obj = factory_instance.objects(k8s_client.api, namespace=namespace).get_by_name(name).obj

        # TODO: do something, persist metrics etc
        logger.info("Still running, no real action yet defined...")

        # delete if completed
        if obj.get("status", {}).get("applicationState", {}).get("state", "") == "COMPLETED":
            factory_instance(k8s_client.api, obj).delete()

        time.sleep(15)

    logger.info(f"daemon has stopped")
