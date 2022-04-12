import ast
from typing import List, Type, Dict, Optional, Callable

import pykube
import logging
from bm_api.models.node import NodeModel, NodeMetricsModel

from . import api_config
from .benchmarks import BaseBenchmark


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

    def get_benchmarks(self, classes: List[Type[BaseBenchmark]],
                       bm_type: Optional[str] = None,
                       node_name: Optional[str] = None):
        res_list: List[Dict] = []
        for cls in classes:
            cls_instance = cls()
            json_result = cls_instance.get_factory(self.api, cls_instance.kind).objects(self.api).filter(namespace="kubestone").execute().json()
            for idx in range(len(json_result["items"])):
                json_result["items"][idx]["metadata"].pop("managedFields", None)
            res_list += json_result["items"]

        def _get_value(extractor_func: Callable, target_dict: Dict, search_value: str):
            try:
                return extractor_func(target_dict).startswith(search_value.lower())
            except Exception:
                return False

        unique_elements = [ast.literal_eval(el) for el in list(set([str(el) for el in res_list]))]
        if bm_type is not None:
            unique_elements = [el for el in unique_elements
                               if _get_value(lambda d: d["metadata"]["name"], el, bm_type)]
        if node_name is not None:
            unique_elements = [el for el in unique_elements
                               if any([
                    _get_value(lambda d: d["spec"]["podConfig"]["podScheduling"]["nodeName"], el, node_name),
                    _get_value(lambda d: d["spec"]["clientConfiguration"]["podScheduling"]["nodeName"], el, node_name),
                    _get_value(lambda d: d["spec"]["serverConfiguration"]["podScheduling"]["nodeName"], el, node_name),
                ])]
        return unique_elements

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
