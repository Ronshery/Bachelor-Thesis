from abc import ABC
from typing import Optional, List, Type

from pykube.objects import APIObject

from bm_api.models.node import NodeModel
from common import BaseRun
from common.clients.k8s import K8sClient


class BaseWorkload(BaseRun, ABC):
    ALLOC_FRACTION: float = 0.75

    def __init__(self, spec: dict, *args, **kwargs):
        super().__init__()
        self.__workload_name__: str = spec.get("metadata", {}).get("name", None)

    @classmethod
    def infer_configuration(cls, client: K8sClient, automate: bool):
        node_count: Optional[int] = None
        per_node_cpu: Optional[int] = None
        per_node_memory: Optional[int] = None
        if automate:
            nodes: List[NodeModel] = client.get_nodes()
            node_count: int = len(nodes)
            # directly in 'cores' (allocate 75% of allocatable resources)
            per_node_cpu: int = min([int(int(node.status.allocatable["cpu"].__root__) * BaseWorkload.ALLOC_FRACTION)
                                     for node in nodes])
            # in 'Ki' (allocate 75% of allocatable resources)
            per_node_memory: int = min(
                [int(int(node.status.allocatable["memory"].__root__[:-2]) * BaseWorkload.ALLOC_FRACTION)
                 for node in nodes])
        return node_count, per_node_cpu, per_node_memory

    def run(self, logger, client: K8sClient, namespace: str, automate: bool, spec: dict, *args, **kwargs):
        if not len(spec):
            return
        # make sure to execute in 'kubestone' namespace
        spec = self.merge_dicts(spec, {"metadata": {"namespace": namespace}})
        # add suffix to 'name', so that they are different and
        # one can schedule multiple benchmarks of one kind simultaneously
        spec['metadata']['name'] = f"{spec['metadata'].get('name', None)}-{self.generate_suffix(10)}"
        # now: run custom logic
        spec = self._run(client, automate, spec, *args, **kwargs)
        # now create object
        factory_instance: Type[APIObject] = self.get_factory(client.api, self.kind)
        factory_instance(client.api, spec).create()
        logger.info(f"Created object of kind '{self.kind}' in namespace '{namespace}'.")

    def _run(self, client: K8sClient, automate: bool, spec: dict, *args, **kwargs):
        raise NotImplementedError
