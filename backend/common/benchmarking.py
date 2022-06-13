import datetime
import time
import re
from typing import Dict, List, Optional, Tuple, TypeVar, Type

import pykube
from pykube import Pod
from pykube.objects import APIObject
from sqlalchemy.orm import Session
from common.metrics.common import BMMetricField

from orm import engine

from common.clients.k8s import get_k8s_client, K8sClient
from common.metrics import get_benchmark_metrics, TMetricClass
from orm.models import Benchmark, BenchmarkMetric


def parse_bm_value(s: Optional[str], default_value: float=0.0, default_unit: str="scalar") -> Tuple[float, str]:

    value = default_value
    unit = default_unit

    if s is not None:
        rx = re.match(r"([\d\.]+)(.*)", s, re.IGNORECASE)

        try:
            value, unit = float(rx.group(1)), (rx.group(2) or default_unit)
        except:
            unit = "(error)"

    return value, unit


# Extracts metrics from a metrics container and converts them to BenchmarkMetric
# entries.
def to_metrics_list(benchmark_id: str, o: any) -> List[BenchmarkMetric]:
    metric_fields: Dict[str, BMMetricField] = {
        k: v for k, v in vars(o).items() if isinstance(v, BMMetricField)
    }

    result = []

    for k, v in metric_fields.items():
        p_value, p_unit = parse_bm_value(v.value)
        result.append(BenchmarkMetric(
            benchmark_id=benchmark_id,
            name=k,
            text_value=v.value,
            value=p_value,
            unit=p_unit
        ))

    return result

def handle_benchmarking(namespace: str,
                        name: str,
                        logger,
                        started: datetime.datetime,
                        stopped,
                        body: dict,
                        job_name: Optional[str] = None,
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

        job_obj = factory_instance.objects(k8s_client.api, namespace=namespace).get_by_name(job_name or name).obj
        job_completed = job_obj.get("status", {}).get("completed", False)

        if job_completed:
            for p in pods:
                pd: Pod = p
                bm_values = get_benchmark_metrics(metrics_cls, p)

                with Session(engine) as session:
                    # assuming pod owner is a job, we use the job's name as benchmark id
                    bm_id = pd.metadata["ownerReferences"][0]["name"]
                    bm_type = pd.labels.get("resourceKind", "unknown")

                    bm = Benchmark(
                        id=bm_id,
                        type=bm_type,
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

            # delete if completed
            factory_instance(k8s_client.api, job_obj).delete()

        time.sleep(15)

    logger.info(f"daemon has stopped")
