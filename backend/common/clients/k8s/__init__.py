from functools import lru_cache

from common.clients.k8s.client import K8sClient


@lru_cache()
def get_k8s_client():
    return K8sClient()
