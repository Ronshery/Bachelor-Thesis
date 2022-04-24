import datetime
import time
import uuid
from typing import Dict, List, Optional, TypeVar, Type

import pykube
from pykube import Pod
from pykube.objects import APIObject
from sqlalchemy.orm import Session
from common.metrics.common import BMMetricField

from orm import engine

from common.clients.k8s import get_k8s_client, K8sClient
from common.metrics import get_benchmark_metrics, TMetricClass
from orm.models import Benchmark, BenchmarkMetric

# Extracts metrics from a metrics container and converts them to BenchmarkMetric
# entries.
def to_metrics_list(benchmark_id: str, o: any) -> List[BenchmarkMetric]:
    metric_fields: Dict[str, BMMetricField] = {
        k: v for k, v in vars(o).items() if isinstance(v, BMMetricField)
    }

    result = []

    for k, v in metric_fields.items():
        result.append(BenchmarkMetric(
            benchmark_id=benchmark_id,
            name=k,
            value=v.value
        ))

    return result

def handle_benchmarking(namespace: str,
                        name: str,
                        logger,
                        started: datetime.datetime,
                        stopped,
                        body: dict,
                        metrics_cls: Optional[Type[TMetricClass]] = None,  # make this later no longer optional
                        **_):

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

            with Session(engine) as session:
                # assuming pod owner is a job, we use the job's name as benchmark id
                bm_id = pd.metadata["ownerReferences"][0]["name"]

                bm = Benchmark(
                    id=bm_id,
                    node_id=pd.obj["spec"]["nodeName"],
                    pod_id=pd.name,
                    started=datetime.datetime.strptime(pd.obj["status"]["startTime"], "%Y-%m-%dT%H:%M:%S%z"),
                    duration=0,
                    image=pd.obj["spec"]["containers"][0]["image"],
                    options=' '.join(pd.obj["spec"]["containers"][0]["args"]),
                    logs=pd.logs()
                )

                bm_metric_list = to_metrics_list(bm_id, bm_values)
            
                session.merge(bm)

                for bm_metric in bm_metric_list:
                    session.merge(bm_metric)
                
                session.commit()

        obj = factory_instance.objects(k8s_client.api, namespace=namespace).get_by_name(name).obj

        # delete if completed
        if "status" in obj and obj["status"]["completed"]:
            factory_instance(k8s_client.api, obj).delete()

        time.sleep(15)

    logger.info(f"daemon has stopped")
