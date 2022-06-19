import datetime
from typing import List, Dict, Optional, Tuple, Type

from fastapi import FastAPI, HTTPException, responses, Depends
import common.benchmarks as benchmarks
from common.benchmarks import BaseBenchmark
from fastapi.middleware.cors import CORSMiddleware
from common.clients.benchmark_history import get_benchmark_history_client
from common.clients.benchmark_history.client import BenchmarkHistoryClient

from common.clients.k8s import get_k8s_client
from common.clients.k8s.client import K8sClient
from bm_api.models.node import NodeModel, NodeMetricsModel
from bm_api.models.benchmark import BenchmarkResult, BenchmarkResultMetric
from common.clients.prometheus.schemes import NodeMetricsModel as PrometheusNodeMetricsModel
from bm_api.models.benchmark import BenchmarkResult

import logging

from common.clients.prometheus import PrometheusClient, get_prometheus_client

from sqlalchemy.orm import Session

from common.fingerprint.fingerprint_engine import BaseFingerprintEngine, NodeScores, NodeScore, get_fingerprint_engine
from orm import engine
from orm.models import BenchmarkMetric

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

benchmark_mappings: Dict[str, Type[BaseBenchmark]] = {
    "cpu-sysbench": benchmarks.CpuSysbenchBenchmark,
    "memory-sysbench": benchmarks.MemorySysbenchBenchmark,
    "network-iperf3": benchmarks.NetworkIperf3Benchmark,
    "network-qperf": benchmarks.NetworkQperfBenchmark,
    "disk-ioping": benchmarks.DiskIopingBenchmark,
    "disk-fio": benchmarks.DiskFioBenchmark
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


@app.get("/benchmarks/name={bm_name}/results", response_model=BenchmarkResult)
async def get_benchmark_results(bm_name: str, bm_history_client: BenchmarkHistoryClient = Depends(get_benchmark_history_client)):
    try:
        r = bm_history_client.get_benchmark_result(bm_name)
        if r is not None:
            return BenchmarkResult(
                id=r.id,
                type=r.type,
                resource=r.type,
                started=r.started,
                metrics=[BenchmarkResultMetric(name=m.name, value=m.value, unit=m.unit) for m in r.metrics]
            )
        else:
            raise HTTPException(status_code=404, detail=f"Benchmark not found: '{bm_name}'")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmark '{bm_name}' not found: {str(e)}")


@app.get("/benchmarks/node={node_name}/results", response_model=List[BenchmarkResult])
async def get_benchmark_results_for_node(node_name: str, bm_history_client: BenchmarkHistoryClient = Depends(get_benchmark_history_client)):
    try:
        results = bm_history_client.get_benchmarks_results(node_name)
        bm_list = [
            BenchmarkResult(
                id=r.id,
                type=r.type,
                resource=r.type,
                started=r.started,
                metrics=[BenchmarkResultMetric(name=m.name, value=m.value, unit=m.unit) for m in r.metrics]
            ) for r in results
        ]

        return bm_list
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmarks for node '{node_name}' not found")


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


@app.get("/fingerprint/{node_name}")
async def get_node_fingerprint(node_name: str, fingerprint_engine: BaseFingerprintEngine = Depends(get_fingerprint_engine)):
    try:
        fp = await fingerprint_engine.get_fingerprint_for_node(node_name)
        return fp.serialize()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/cluster-fingerprint")
async def get_node_fingerprint(fingerprint_engine: BaseFingerprintEngine = Depends(get_fingerprint_engine)):
    try:
        fp = await fingerprint_engine.get_fingerprint_for_cluster()
        return fp.serialize()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/scores/{node_name}", response_model=NodeScores)
async def get_node_scores(node_name: str, fingerprint_engine: BaseFingerprintEngine = Depends(get_fingerprint_engine)):
    try:
        scores = await fingerprint_engine.get_scores_for_node(node_name, relative_to_cluster=False)
        return scores
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/scores/{node_name}/cluster", response_model=NodeScores)
async def get_node_scores(node_name: str, fingerprint_engine: BaseFingerprintEngine = Depends(get_fingerprint_engine)):
    try:
        scores = await fingerprint_engine.get_scores_for_node(node_name, relative_to_cluster=True)
        return scores
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


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
                           prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        metrics: NodeMetricsModel = next((m for m in await get_all_nodes_metrics(time_delta,
                                                                                 prometheus_client)
                                          if m.node_name == node_name), None)
        return metrics
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node metrics not found")


@app.get("/metrics/{node_name}/{time_from}/{time_to}", response_model=NodeMetricsModel)
async def get_node_metrics_from_to(node_name: str, time_from: datetime.datetime, time_to: datetime.datetime,
                           prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        metrics: NodeMetricsModel = next((m for m in await get_all_nodes_metrics_from_to(time_from, time_to,
                                                                                 prometheus_client)
                                          if m.node_name == node_name), None)
        return metrics
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node metrics not found")


@app.get("/metrics/{time_delta}", response_model=List[NodeMetricsModel])
async def get_all_nodes_metrics(time_delta: int,
                                prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        time_delta = max(time_delta, -1)
        time_delta = time_delta if time_delta > -1 else 60 * 60 * 24 * 1  # max 1 day
        now_time: datetime.datetime = datetime.datetime.now()
        prometheus_models: List[PrometheusNodeMetricsModel] = await prometheus_client.get_node_metrics(
            now_time - datetime.timedelta(seconds=time_delta), now_time)
        return [NodeMetricsModel(**prom_model.dict()) for prom_model in prometheus_models]

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="No node metrics found")


@app.get("/metrics/{time_from}/{time_to}", response_model=List[NodeMetricsModel])
async def get_all_nodes_metrics_from_to(time_from: datetime.datetime,
                                time_to: datetime.datetime,
                                prometheus_client: PrometheusClient = Depends(get_prometheus_client)):
    try:
        prometheus_models: List[PrometheusNodeMetricsModel] = await prometheus_client.get_node_metrics(
            time_from, time_to)
        return [NodeMetricsModel(**prom_model.dict()) for prom_model in prometheus_models]

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="No node metrics found")
