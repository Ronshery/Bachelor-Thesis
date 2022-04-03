from typing import List, Optional, Iterable

import pykube

from bm_api.models.k8s.io.k8s.api.core.v1 import NodeSpec, NodeStatus
from bm_api.models.k8s.io.k8s.apimachinery.pkg.apis.meta.v1 import ObjectMeta
from bm_api.models.node import NodeModel, NodeMetricsModel


class K8sClient(object):
    pk_api: pykube.HTTPClient

    def __init__(self):
        # TODO: centrally initialize pykube client
        self.pk_api = pykube.HTTPClient(pykube.KubeConfig.from_file())

    def get_node_by_name(self, node_name: str) -> Optional[NodeModel]:
        node: Optional[pykube.objects.Node] = pykube.Node.objects(self.pk_api).get_by_name(node_name)

        if node is not None:
            return NodeModel.from_pykube(node)

    def get_nodes(self) -> List[NodeModel]:
        nodes: Iterable[pykube.objects.Node] = pykube.Node.objects(self.pk_api)

        return [NodeModel.from_pykube(n) for n in nodes]

    def get_node_metrics_by_name(self, node_name: str) -> Optional[NodeMetricsModel]:
        pass

    def get_node_metrics(self) -> List[NodeMetricsModel]:
        pass

