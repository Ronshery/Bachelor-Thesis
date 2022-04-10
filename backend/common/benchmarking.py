import datetime
import time
import uuid
from typing import TypeVar, Type

import pykube
from kopf import Spec
from pykube import Pod
from sqlalchemy.orm import Session

from common.metrics import get_benchmark_metrics, TMetricClass

pk_api = pykube.HTTPClient(pykube.KubeConfig.from_file())


def handle_benchmarking(name,
                        spec: Spec,
                        stopped,
                        logger,
                        started: datetime.datetime,
                        metrics_cls: Type[TMetricClass],
                        **kwargs):
    # from orm import engine
    # from orm.models import Benchmark

    logger.info(f"{name}: started: {started}, {spec}")

    while not stopped:
        pods = pykube.Pod.objects(pk_api, namespace="kubestone")\
            .filter(selector={
                "job-name": name
            }).all()

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

        time.sleep(15)

    logger.info(f"daemon has stopped")
