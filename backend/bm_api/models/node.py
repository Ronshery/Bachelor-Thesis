from typing import Literal, Optional
from pydantic import BaseModel


class NodeLimitations(BaseModel):
    storage_mb: Optional[int]
    memory_mb: Optional[int]
    num_pods: Optional[int] # like this?


class Node(BaseModel):
    id: str
    node_type: Literal["master", "slave"]
    kernel_version: str
    kubernetes_version: str
    num_replicas: int
    limitations: Optional[NodeLimitations]


class NodeMetrics(BaseModel):
    # percentage value sufficient? maybe current value and maximum available would also make sense?

    node_id: str
    cpu_load: float
    memory_usage: float
    storage_usage: float
    network_down: float
    network_up: float
