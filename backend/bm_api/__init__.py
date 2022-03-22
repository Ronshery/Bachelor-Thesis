from typing import List

from fastapi import FastAPI, HTTPException
import pykube

from . import api_config
from bm_api.k8s_client import K8sClient
from bm_api.models.node import NodeModel, NodeMetricsModel
from bm_api.models.benchmark import BenchmarkResult


app = FastAPI()
k8s_client = K8sClient()

@app.get("/version")
async def get_version():
    return {
        "version": api_config.BMAPI_VERSION
    }


@app.post("/benchmark/{type}/{node_id}", response_model=BenchmarkResult)
async def run_benchmark(type: str, node_id: str):
    # TODO
    raise NotImplementedError


@app.get("/nodes/{node_name}", response_model=NodeModel)
async def get_node(node_name: str):
    try:
        node = k8s_client.get_node_by_name(node_name)
        return node
    except Exception:
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/nodes", response_model=List[NodeModel])
async def get_all_nodes():
    try:
        nodes = k8s_client.get_nodes()
        return nodes
    except Exception:
        raise HTTPException(status_code=404, detail="Node not found")


@app.get("/metrics/{node_name}", response_model=NodeMetricsModel)
async def get_node_metrics(node_name: str):
    try:
        metrics: NodeMetricsModel = k8s_client.get_node_metrics_by_name(node_name)
        return metrics
    except Exception:
        raise HTTPException(status_code=404, detail="Node metrics not found")


@app.get("/metrics", response_model=List[NodeMetricsModel])
async def get_all_nodes_metrics():
    try:
        metrics_list: List[NodeMetricsModel] = k8s_client.get_node_metrics()
        return metrics_list
    except Exception:
        raise HTTPException(status_code=404, detail="No node metrics found")
