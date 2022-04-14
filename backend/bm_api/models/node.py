from __future__ import annotations

from typing import Optional, Dict

import pykube
from pydantic import BaseModel
from bm_api.models.k8s.io.k8s.api.core.v1 import Node
from bm_api.models.k8s.io.k8s.apimachinery.pkg.apis.meta.v1 import ObjectMeta


class NodeLimitations(BaseModel):
    storage_mb: Optional[int]
    memory_mb: Optional[int]
    num_pods: Optional[int]  # like this?


# inherits from k8s OpenAPI specs and can be extended
# with custom fields, i.e. the name of the current cluster
class NodeModel(Node):
    @staticmethod
    def from_pykube(n: pykube.objects.Node) -> NodeModel:
        return NodeModel(
            apiVersion=n.version,
            metadata=ObjectMeta(
                **n.metadata
            )
        )


# based on the metrics-server API
# https://github.com/kubernetes-sigs/metrics-server
class NodeMetricsModel(BaseModel):
    name: str
    usage: Dict[str, str]
