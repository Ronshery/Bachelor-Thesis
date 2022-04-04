import pykube
import logging
from bm_api.models.node import NodeModel, NodeMetricsModel

from . import api_config


class NodeMetrics(pykube.objects.APIObject):
    version = "metrics.k8s.io/v1beta1"
    endpoint = "nodes"
    kind = "NodeMetrics"


class K8sClient:
    api: pykube.HTTPClient

    def __init__(self):
        try:
            # either use in-cluster config or local ~/.kube/config
            self.api = pykube.HTTPClient(pykube.KubeConfig.from_env())
        except Exception as e:
            logging.error("Could not connect to the Kubernetes cluster")

    def get_node_metrics(self):
        metrics = NodeMetrics.objects(self.api)
        metrics_list = []
        for node in metrics:
            metrics_dict = {
                'name': node.name,
                'usage': node.obj.get("usage", {})
            }
            metrics_list.append(NodeMetricsModel(**metrics_dict))
        return metrics_list

    def get_node_metrics_by_name(self, node_name: str):
        metrics: NodeMetrics = NodeMetrics.objects(self.api).get(name=node_name)
        metrics_dict = {
            'name': metrics.name,
            'usage': metrics.obj.get("usage", {})
        }
        return NodeMetricsModel(**metrics_dict)

    def get_nodes(self):
        nodes = pykube.Node.objects(self.api)
        if nodes:
            return [NodeModel(cluster=api_config.CLUSTER_NAME, **n.obj) for n in nodes]

    def get_node_by_name(self, node_name: str):
        node: pykube.objects.Node = pykube.Node.objects(self.api).get(name=node_name)
        return NodeModel(cluster=api_config.CLUSTER_NAME, **node.obj)
