from typing import List, Dict, Type

import pykube
from fastapi import FastAPI, HTTPException, responses


from . import api_config
from bm_api.k8s_client import K8sClient
from bm_api.models.node import NodeModel, NodeMetricsModel
from bm_api.models.benchmark import BenchmarkResult

import bm_api.benchmarks
import logging

app = FastAPI()
k8s_client = K8sClient()


benchmark_mappings: Dict[str, Type[bm_api.benchmarks.BaseBenchmark]] = {
    "cpu-sysbench": bm_api.benchmarks.CpuSysbenchBenchmark,
    "memory-sysbench": bm_api.benchmarks.MemorySysbenchBenchmark,
    "network-iperf3": bm_api.benchmarks.NetworkIperf3Benchmark,
    "network-qperf": bm_api.benchmarks.NetworkQperfBenchmark,
    "disk-ioping": bm_api.benchmarks.DiskIopingBenchmark,
    "disk-fio": bm_api.benchmarks.DiskFioBenchmark
}


@app.get("/version")
async def get_version():
    return {
        "version": api_config.BMAPI_VERSION
    }


@app.get("/", include_in_schema=False)
async def redirect():
    response = responses.RedirectResponse(url='/docs')
    return response


@app.get("/benchmarks")
async def get_all_benchmarks():
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Benchmarks not found")


@app.get("/benchmarks/kind={bm_type}")
async def get_all_benchmarks_by_kind(bm_type: str):
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()), bm_type=bm_type)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmarks for kind '{bm_type}' not found")


@app.get("/benchmarks/node={node_id}")
async def get_all_benchmarks_by_node(node_id: str):
    try:
        return k8s_client.get_benchmarks(list(benchmark_mappings.values()), node_name=node_id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail=f"Benchmarks for node '{node_id}' not found")


@app.post("/benchmark/{bm_type}/{node_id}", response_model=BenchmarkResult)
async def run_benchmark(bm_type: str, node_id: str):
    bm_type = bm_type.lower()
    if bm_type in benchmark_mappings:
        # TODO: centrally initialize pykube client
        pk_api = pykube.HTTPClient(pykube.KubeConfig.from_env())

        bm_cls = benchmark_mappings[bm_type]
        bm = bm_cls()

        startup_result = bm.run(pk_api, node_id)

        return startup_result
    else:
        raise HTTPException(status_code=404, detail=f"Benchmark '{bm_type}' not found")


@app.get("/nodes/{node_name}", response_model=NodeModel)
async def get_node(node_name: str):
    try:
        node = k8s_client.get_node_by_name(node_name)
        return node
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/nodes", response_model=List[NodeModel])
async def get_all_nodes():
    try:
        nodes = k8s_client.get_nodes()
        return nodes
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/metrics/{node_name}", response_model=NodeMetricsModel)
async def get_node_metrics(node_name: str):
    try:
        metrics: NodeMetricsModel = k8s_client.get_node_metrics_by_name(node_name)
        return metrics
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Node metrics not found")


@app.get("/metrics", response_model=List[NodeMetricsModel])
async def get_all_nodes_metrics():
    try:
        metrics_list: List[NodeMetricsModel] = k8s_client.get_node_metrics()
        return metrics_list
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="No node metrics found")
