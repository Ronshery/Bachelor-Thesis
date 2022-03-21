from typing import List

from fastapi import FastAPI

from . import api_config
from bm_api.models.node import Node, NodeMetrics
from bm_api.models.benchmark import BenchmarkResult

app = FastAPI()


@app.get("/version")
async def get_version():
    return {
        "version": api_config.BMAPI_VERSION
    }


@app.post("/benchmark/{type}/{node_id}", response_model=BenchmarkResult)
async def run_benchmark(type: str, node_id: str):
    # TODO
    raise NotImplementedError


@app.get("/nodes/{node_id}", response_model=Node)
async def get_node(node_id: str):
    # TODO
    raise NotImplementedError


@app.get("/nodes", response_model=List[Node])
async def get_all_nodes():
    # TODO
    raise NotImplementedError


@app.get("/metrics/{node_id}", response_model=NodeMetrics)
async def get_node_metrics(node_id: str):
    # TODO
    raise NotImplementedError


@app.get("/metrics", response_model=List[NodeMetrics])
async def get_all_nodes_metrics():
    # TODO
    raise NotImplementedError
