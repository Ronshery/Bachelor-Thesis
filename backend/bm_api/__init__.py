import datetime
from typing import List, Dict, Type, Optional

from fastapi import FastAPI, HTTPException, responses, Depends
from bm_api.benchmarks.base import BaseBenchmark

from common.clients.k8s import get_k8s_client
from common.clients.k8s.client import K8sClient
from bm_api.models.node import NodeModel, NodeMetricsModel
from common.clients.prometheus.schemes import NodeMetricsModel as PrometheusNodeMetricsModel
from bm_api.models.benchmark import BenchmarkResult

import bm_api.benchmarks
import logging

from common.clients.prometheus import PrometheusClient, get_prometheus_client

from sqlalchemy.orm import Session
from orm import engine
from orm.models import BenchmarkMetric

app = FastAPI()

benchmark_mappings: Dict[str, Type[BaseBenchmark]] = {
    "cpu-sysbench": bm_api.benchmarks.CpuSysbenchBenchmark,
    "memory-sysbench": bm_api.benchmarks.MemorySysbenchBenchmark,
    "network-iperf3": bm_api.benchmarks.NetworkIperf3Benchmark,
    "network-qperf": bm_api.benchmarks.NetworkQperfBenchmark,
    "disk-ioping": bm_api.benchmarks.DiskIopingBenchmark,
    "disk-fio": bm_api.benchmarks.DiskFioBenchmark
}


@app.get("/version")
async def get_version(k8s_client: K8sClient = Depends(get_k8s_client)):
    return {
        "version": k8s_client.api.version
    }


@app.get("/", include_in_schema=False)
async def redirect():
    response = responses.RedirectResponse(url='/docs')
    return response


@app.get("/benchmarks")
async def get_all_benchmarks(k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Benchmarks not found")


@app.get("/benchmarks/kind={bm_type}")
async def get_all_benchmarks_by_kind(bm_type: str, k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()), bm_type=bm_type)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmarks for kind '{bm_type}' not found")


@app.get("/benchmarks/node={node_id}")
async def get_all_benchmarks_by_node(node_id: str, k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()), node_name=node_id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmarks for node '{node_id}' not found")

@app.get("/benchmarks/name={bm_name}/results", response_model=Dict[str, str])
async def get_benchmark_results(bm_name: str, k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        with Session(engine) as session:
            metrics = session \
                .query(BenchmarkMetric) \
                .filter(BenchmarkMetric.benchmark_id == bm_name) \
                .all()
            return {
                m.name: m.value for m in metrics
            }
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmark '{bm_name}' not found")

@app.post("/benchmark/{bm_type}/{node_id}")
async def run_benchmark(bm_type: str, node_id: str, k8s_client: K8sClient = Depends(get_k8s_client)):
    bm_type = bm_type.lower()
    if bm_type in benchmark_mappings:
        bm_cls = benchmark_mappings[bm_type]
        bm = bm_cls()

        startup_result = bm.run(k8s_client.api, node_id)

        if startup_result.success:
            return {
                "id": startup_result.id,
                "spec": startup_result.benchmark_spec
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to start benchmark '{bm_type}': {startup_result.error}")
    else:
        raise HTTPException(status_code=404, detail=f"Benchmark '{bm_type}' not found")


@app.get("/nodes/{node_name}", response_model=NodeModel)
async def get_node(node_name: str, k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        node = k8s_client.get_node_by_name(node_name)
        return node
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/nodes", response_model=List[NodeModel])
async def get_all_nodes(k8s_client: K8sClient = Depends(get_k8s_client)):
    try:
        nodes = k8s_client.get_nodes()
        return nodes
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/metrics/{node_name}/{time_delta}", response_model=NodeMetricsModel)
async def get_node_metrics(node_name: str, time_delta: int,
                           k8s_client: K8sClient = Depends(get_k8s_client),
                           prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        metrics: NodeMetricsModel = next((m for m in await get_all_nodes_metrics(time_delta,
                                                                                 k8s_client,
                                                                                 prometheus_client)
                                          if m.node_name == node_name), None)
        return metrics
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node metrics not found")


@app.get("/metrics/{time_delta}", response_model=List[NodeMetricsModel])
async def get_all_nodes_metrics(time_delta: int,
                                k8s_client: K8sClient = Depends(get_k8s_client),
                                prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        time_delta = max(time_delta, 5)
        now_time: datetime.datetime = datetime.datetime.now()
        prometheus_models: List[PrometheusNodeMetricsModel] = await prometheus_client.get_node_metrics(
            now_time - datetime.timedelta(seconds=time_delta), now_time)

        node_infos: List[Dict[str, str]] = [{ad_obj.type: ad_obj.address for ad_obj in node.status.addresses}
                                            for node in await get_all_nodes(k8s_client)]

        metric_models: List[NodeMetricsModel] = []
        for prom_model in prometheus_models:
            node_info: Dict[str, str] = next((node_info for node_info in node_infos
                                              if prom_model.node_name.startswith(node_info['InternalIP'])), {})
            metric_models.append(NodeMetricsModel(**prom_model.dict(exclude={"node_name"}),
                                                  node_name=node_info.get("Hostname", None)))
        return metric_models

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="No node metrics found")
