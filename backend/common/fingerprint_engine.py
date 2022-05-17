from __future__ import annotations
from dataclasses import dataclass
import datetime

from functools import lru_cache
from abc import ABC
import json
import re
from statistics import mean
from typing import Any, Dict, List, Optional, TypeVar

import pydantic
from common.benchmarks.base import BenchmarkedResourceKind

from common.clients.benchmark_history.client import BenchmarkHistoryClient
from common.clients.prometheus import PrometheusClient, get_prometheus_client
from orm.models import Benchmark


class BaseFingerprint(ABC):
    @property
    def node_name(self) -> str:
        raise NotImplementedError

    @property
    def timestamp(self) -> datetime.datetime:
        raise NotImplementedError

    def compare_to(self, ref_fingerprint: BaseFingerprint) -> float:
        raise NotImplementedError

    def serialize(self) -> str:
        raise NotImplementedError

    @staticmethod
    def parse(source: str) -> BaseFingerprint:
        raise NotImplementedError


@dataclass
class SimpleFingerprint(BaseFingerprint):
    _node_name: str
    _utctimestamp: datetime.datetime

    # cpu-sysbench
    cpu_events_per_second: float
    cpu_latency_95: float

    # memory-sysbench
    mem_latency_max: float
    mem_exctime: float

    # disk-ioping
    disk_iops: float
    disk_latency_avg: float

    # network-iperf3
    net_transfer_bitrate: float

    # network-qperf
    net_tcp_msg_rate: float
    net_tcp_latency: float
    net_bw_cpu_usage: float
    net_lat_cpu_usage: float

    @property
    def node_name(self) -> str:
        return self._node_name

    @property
    def timestamp(self) -> datetime.datetime:
        return self._utctimestamp

    def compare_to(self, ref_fingerprint: SimpleFingerprint) -> float:
        if type(ref_fingerprint) != SimpleFingerprint:
            raise ValueError("SimpleFingerprint can only compare to SimpleFingerprint")
        
        vec = (
            self.cpu_events_per_second / ref_fingerprint.cpu_events_per_second,
            self.cpu_latency_95 / ref_fingerprint.cpu_latency_95,
            self.mem_latency_max / ref_fingerprint.mem_latency_max,
            self.mem_exctime / ref_fingerprint.mem_exctime,
            self.disk_iops / ref_fingerprint.disk_iops,
            self.disk_latency_avg / ref_fingerprint.disk_latency_avg,
            self.net_transfer_bitrate / ref_fingerprint.net_transfer_bitrate,
            self.net_tcp_msg_rate / ref_fingerprint.net_tcp_msg_rate,
            self.net_tcp_latency / ref_fingerprint.net_tcp_latency,
            self.net_bw_cpu_usage / ref_fingerprint.net_bw_cpu_usage,
            self.net_lat_cpu_usage / ref_fingerprint.net_lat_cpu_usage,
        )

        return mean(vec)

    def serialize(self) -> str:
        return json.dumps(self.__dict__, default=str)

    @staticmethod
    def parse(source: str) -> SimpleFingerprint:
        return SimpleFingerprint(**json.loads(source))


class NodeScore(pydantic.BaseModel):
    score: int
    max_score: int = 10    

@dataclass
class NodeScores(pydantic.BaseModel):
    node_name: str

    cpu: NodeScore
    memory: NodeScore
    disk: NodeScore
    network: NodeScore
    

class BaseFingerprintEngine(ABC):
    @property
    def description(self) -> str:
        raise NotImplementedError

    async def get_fingerprint_for_node(self, node_name: str) -> BaseFingerprint:
        raise NotImplementedError

    async def get_scores_for_node(self, node_name: str) -> NodeScores:
        raise NotImplementedError

    async def get_scores(self, *node_names : str) -> Dict[str, NodeScores]:
        return {
            n: await self.get_scores_for_node(n) for n in node_names
        }

    async def get_fingerprints(self, *node_names : str) -> Dict[str, BaseFingerprint]:
        return {
            n: await self.get_fingerprint_for_node(n) for n in node_names
        }


class SimpleFingerprintEngine(BaseFingerprintEngine):
    @property
    def description(self) -> str:
        return "Simple Demo Fingerprint Engine"

    def __init__(self,
                 prometheus_client: PrometheusClient,
                 benchmark_history_client: BenchmarkHistoryClient):
        self.prometheus_client = prometheus_client
        self.benchmark_history_client = benchmark_history_client

    async def get_fingerprint_for_node(self, node_name: str) -> BaseFingerprint:
        recent_bms = self.benchmark_history_client.get_benchmarks_results(node_name)

        bms: Dict[str, Benchmark] = {}
        
        for bm in recent_bms:
            if bm.type not in bms:
                bms[bm.type] = bm
            elif bms[bm.type].started < bm.started:
                bms[bm.type] = bm
        
        def get_metric_value(bm_type: BenchmarkedResourceKind, metric_name: str, default_value: Optional[float]=None) -> Optional[float]:
            if bm_type.value in bms:
                mt = next(filter(lambda m: m.name == metric_name, bms[bm_type.value].metrics), None)
                if mt is not None and mt.value is not None:
                    rm = re.match(r"[\d\.]+", mt.value)
                    if rm is not None:
                        print(mt.value, rm.group(0))
                        return float(rm.group(0))
            
            return default_value

        # TODO correlate with node metrics from prometheus
        fp = SimpleFingerprint(
            node_name,
            datetime.datetime.utcnow(),
            cpu_events_per_second=get_metric_value(BenchmarkedResourceKind.CPU_SYSBENCH, "events_per_second", 0.0),
            cpu_latency_95=get_metric_value(BenchmarkedResourceKind.CPU_SYSBENCH, "latency_95p", 0.0),
            disk_iops=get_metric_value(BenchmarkedResourceKind.DISK_IOPING, "iops", 0.0),
            disk_latency_avg=get_metric_value(BenchmarkedResourceKind.DISK_IOPING, "latency_avg", 0.0),
            mem_exctime=get_metric_value(BenchmarkedResourceKind.MEMORY_SYSBENCH, "fairness_exctime", 0.0),
            mem_latency_max=get_metric_value(BenchmarkedResourceKind.MEMORY_SYSBENCH, "latency_max", 0.0),
            net_bw_cpu_usage=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_bw_send_cpus_used", 0.0),
            net_lat_cpu_usage=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_lat_loc_cpus_used", 0.0),
            net_tcp_latency=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_lat_latency", 0.0),
            net_tcp_msg_rate=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_bw_msg_rate", 0.0),
            net_transfer_bitrate=get_metric_value(BenchmarkedResourceKind.NETWORK_IPERF3, "transfer_bitrate", 0.0)
        )

        return fp


    async def get_scores_for_node(self, node_name: str) -> NodeScores:
        raise NotImplementedError
        # recent_bms = self.benchmark_history_client.get_benchmarks_results(node_name)

        # interval = datetime.timedelta(seconds=60)

        # tf_end = datetime.datetime.now()
        # tf_start = tf_end - interval

        # node_stats = await self.prometheus_client.get_node_metrics(tf_start, tf_end, node_name=node_name)

        # return NodeScores()


@lru_cache()
def get_fingerprint_engine() -> BaseFingerprintEngine:
    return SimpleFingerprintEngine(get_prometheus_client(), BenchmarkHistoryClient())
