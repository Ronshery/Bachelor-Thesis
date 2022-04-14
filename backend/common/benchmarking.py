import datetime
import time
import uuid
from typing import Type, Optional

import pykube
from pykube import Pod
from pykube.objects import APIObject
from sqlalchemy.orm import Session

from common.clients.k8s import get_k8s_client, K8sClient
from common.metrics import get_benchmark_metrics, TMetricClass


def handle_benchmarking(namespace: str,
                        name: str,
                        logger,
                        started: datetime.datetime,
                        stopped,
                        body: dict,
                        metrics_cls: Optional[Type[TMetricClass]] = None,  # make this later no longer optional
                        **_):
    # from orm import engine
    # from orm.models import Benchmark

    logger.info(f"{name}: started: {started}, {body['spec']}")

    k8s_client: K8sClient = get_k8s_client()

    kind: str = body["kind"]
    factory_instance: Type[APIObject] = pykube.object_factory(k8s_client.api, "perf.kubestone.xridge.io/v1alpha1", kind)

    while not stopped:
        pods = pykube.Pod.objects(k8s_client.api, namespace=namespace) \
            .filter(selector={"job-name": name}).all()

        logger.info(f"{name}: Found {len(pods)} pods")

        for p in pods:
            pd: Pod = p
            bm_values = get_benchmark_metrics(metrics_cls, p)

            print(pd.metadata)

            # TODO - find information as needed
            # with Session(engine) as session:
            #     bm = Benchmark(
            #         id=str(uuid.uuid4()),
            #         node_id=pd.metadata["nodeName"],
            #         pod_id="unknown",
            #         started=pd.status.startTime,
            #         duration=0,
            #         image=spec["image"],
            #         options=spec["options"],
            #         logs=p.logs()
            #     )
            #
            #     session.add(bm)
            #     session.commit()

            logger.info(bm_values)

            # TODO: after storing its metrics, delete the pod
            # p.delete()

        obj = factory_instance.objects(k8s_client.api, namespace=namespace).get_by_name(name).obj

        # delete if completed
        if obj["status"]["completed"]:
            factory_instance(k8s_client.api, obj).delete()

        time.sleep(15)

    logger.info(f"daemon has stopped")
