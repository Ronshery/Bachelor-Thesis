from typing import Literal, Optional, Dict
from pydantic import BaseModel
from bm_api.models.k8s.io.k8s.api.core.v1 import Node


class NodeLimitations(BaseModel):
    storage_mb: Optional[int]
    memory_mb: Optional[int]
    num_pods: Optional[int] # like this?


# inherits from k8s OpenAPI specs and can be extended
# with custom fields, i.e. the name of the current cluster
class NodeModel(Node):
    cluster: Optional[str] = None  # name of current k8s cluster


# based on the metrics-server API
# https://github.com/kubernetes-sigs/metrics-server
class NodeMetricsModel(BaseModel):
    name: str
    usage: Dict[str, str]
