import string
from abc import ABC
import random
from typing import Type

import pykube
from pykube.objects import APIObject


class BaseRun(ABC):
    @property
    def name(self):
        raise NotImplementedError

    @property
    def kind(self):
        raise NotImplementedError

    @classmethod
    def get_factory(cls, client: pykube.HTTPClient, kind: str) -> Type[APIObject]:
        raise NotImplementedError

    @classmethod
    def generate_suffix(cls, length: int):
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

    @classmethod
    def merge_dicts(cls, tgt, enhancer):
        for key, val in enhancer.items():
            if key not in tgt:
                tgt[key] = val
                continue

            if isinstance(val, dict):
                if not isinstance(tgt[key], dict):
                    tgt[key] = dict()
                BaseRun.merge_dicts(tgt[key], val)
            else:
                tgt[key] = val
        return tgt
