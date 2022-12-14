from __future__ import annotations
from dataclasses import dataclass
import datetime

from functools import lru_cache
from abc import ABC
import json
from optparse import Option
import re
from statistics import mean
from typing import Any, Dict, List, Optional, TypeVar

import pydantic
from common.benchmarks.base import BenchmarkedResource, BenchmarkedResourceKind

from common.clients.benchmark_history.client import BenchmarkHistoryClient
from common.clients.prometheus import PrometheusClient, get_prometheus_client
from common.clients.k8s import get_k8s_client
from common.clients.k8s.client import K8sClient
from orm.models import Benchmark


class BaseFingerprint(ABC):
    @property
    def node_name(self) -> str:
        raise NotImplementedError

    @property
    def timestamp(self) -> datetime.datetime:
        raise NotImplementedError

    def compare_to(self, ref_fingerprint: BaseFingerprint, for_resource: Optional[BenchmarkedResource] = None,
                   for_kind: Optional[BenchmarkedResourceKind] = None) -> float:
        raise NotImplementedError

    def serialize(self) -> str:
        raise NotImplementedError

    @staticmethod
    def parse(source: str) -> BaseFingerprint:
        raise NotImplementedError

    @staticmethod
    def mean(fingerprints: List[BaseFingerprint]) -> BaseFingerprint:
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

    # disk-fio
    disk_write_iops: float
    disk_write_mibps: float

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

    def compare_to(self, ref_fingerprint: SimpleFingerprint,
                   for_resource: Optional[BenchmarkedResource] = None,
                   for_kind: Optional[BenchmarkedResourceKind] = None) -> float:
        if type(ref_fingerprint) != SimpleFingerprint:
            raise ValueError("SimpleFingerprint can only compare to SimpleFingerprint")

        def safe_div(self_measure: float, ref_measure: float):
            if ref_measure == 0.0:
                ref_measure = 1.0
            
            return self_measure / ref_measure

        if for_resource is not None:
            if for_resource == BenchmarkedResource.CPU:
                vec = (
                    safe_div(self.cpu_events_per_second, ref_fingerprint.cpu_events_per_second),
                    safe_div(self.cpu_latency_95, ref_fingerprint.cpu_latency_95),
                )
            elif for_resource == BenchmarkedResource.DISK:
                vec = (
                    safe_div(self.disk_iops, ref_fingerprint.disk_iops),
                    safe_div(self.disk_latency_avg, ref_fingerprint.disk_latency_avg),
                    safe_div(self.disk_write_iops, ref_fingerprint.disk_write_iops),
                    safe_div(self.disk_write_mibps, ref_fingerprint.disk_write_mibps),
                )
            elif for_resource == BenchmarkedResource.MEMORY:
                vec = (
                    safe_div(self.mem_latency_max, ref_fingerprint.mem_latency_max),
                    safe_div(self.mem_exctime, ref_fingerprint.mem_exctime),
                )
            elif for_resource == BenchmarkedResource.NETWORK:
                vec = (
                    safe_div(self.net_transfer_bitrate, ref_fingerprint.net_transfer_bitrate),
                    safe_div(self.net_tcp_msg_rate, ref_fingerprint.net_tcp_msg_rate),
                    safe_div(self.net_tcp_latency, ref_fingerprint.net_tcp_latency),
                    safe_div(self.net_bw_cpu_usage, ref_fingerprint.net_bw_cpu_usage),
                    safe_div(self.net_lat_cpu_usage, ref_fingerprint.net_lat_cpu_usage),
                )
        elif for_kind is not None:
            if for_kind == BenchmarkedResourceKind.CPU_SYSBENCH:
                vec = (
                    safe_div(self.cpu_events_per_second, ref_fingerprint.cpu_events_per_second),
                    safe_div(self.cpu_latency_95, ref_fingerprint.cpu_latency_95),
                )
            elif for_kind == BenchmarkedResourceKind.DISK_IOPING:
                vec = (
                    safe_div(self.disk_iops, ref_fingerprint.disk_iops),
                    safe_div(self.disk_latency_avg, ref_fingerprint.disk_latency_avg),
                )
            elif for_kind == BenchmarkedResourceKind.DISK_FIO:
                vec = (
                    safe_div(self.disk_write_iops, ref_fingerprint.disk_write_iops),
                    safe_div(self.disk_write_mibps, ref_fingerprint.disk_write_mibps),
                )
            elif for_kind == BenchmarkedResourceKind.MEMORY_SYSBENCH:
                vec = (
                    safe_div(self.mem_latency_max, ref_fingerprint.mem_latency_max),
                    safe_div(self.mem_exctime, ref_fingerprint.mem_exctime),
                )
            elif for_kind == BenchmarkedResourceKind.NETWORK_IPERF3:
                vec = (
                    safe_div(self.net_transfer_bitrate, ref_fingerprint.net_transfer_bitrate),
                )
            elif for_kind == BenchmarkedResourceKind.NETWORK_QPERF:
                vec = (
                    safe_div(self.net_tcp_msg_rate, ref_fingerprint.net_tcp_msg_rate),
                    safe_div(self.net_tcp_latency, ref_fingerprint.net_tcp_latency),
                    safe_div(self.net_bw_cpu_usage, ref_fingerprint.net_bw_cpu_usage),
                    safe_div(self.net_lat_cpu_usage, ref_fingerprint.net_lat_cpu_usage),
                )
        else:
            vec = (
                safe_div(self.cpu_events_per_second, ref_fingerprint.cpu_events_per_second),
                safe_div(self.cpu_latency_95, ref_fingerprint.cpu_latency_95),
                safe_div(self.mem_latency_max, ref_fingerprint.mem_latency_max),
                safe_div(self.mem_exctime, ref_fingerprint.mem_exctime),
                safe_div(self.disk_iops, ref_fingerprint.disk_iops),
                safe_div(self.disk_latency_avg, ref_fingerprint.disk_latency_avg),
                safe_div(self.disk_write_iops, ref_fingerprint.disk_write_iops),
                safe_div(self.disk_write_mibps, ref_fingerprint.disk_write_mibps),
                safe_div(self.net_transfer_bitrate, ref_fingerprint.net_transfer_bitrate),
                safe_div(self.net_tcp_msg_rate, ref_fingerprint.net_tcp_msg_rate),
                safe_div(self.net_tcp_latency, ref_fingerprint.net_tcp_latency),
                safe_div(self.net_bw_cpu_usage, ref_fingerprint.net_bw_cpu_usage),
                safe_div(self.net_lat_cpu_usage, ref_fingerprint.net_lat_cpu_usage),
            )

        return mean(vec)

    def serialize(self) -> str:
        return json.dumps(self.__dict__, default=str)

    @staticmethod
    def parse(source: str) -> SimpleFingerprint:
        return SimpleFingerprint(**json.loads(source))

    @staticmethod
    def mean(fingerprints: List[SimpleFingerprint]) -> SimpleFingerprint:
        return SimpleFingerprint(
            _node_name='+'.join([fp._node_name for fp in fingerprints]),
            _utctimestamp=max([fp._utctimestamp for fp in fingerprints]),
            cpu_events_per_second=mean([fp.cpu_events_per_second for fp in fingerprints]),
            cpu_latency_95=mean([fp.cpu_latency_95 for fp in fingerprints]),
            mem_latency_max=mean([fp.mem_latency_max for fp in fingerprints]),
            mem_exctime=mean([fp.mem_exctime for fp in fingerprints]),
            disk_iops=mean([fp.disk_iops for fp in fingerprints]),
            disk_latency_avg=mean([fp.disk_latency_avg for fp in fingerprints]),
            disk_write_iops=mean([fp.disk_write_iops for fp in fingerprints]),
            disk_write_mibps=mean([fp.disk_write_mibps for fp in fingerprints]),
            net_transfer_bitrate=mean([fp.net_transfer_bitrate for fp in fingerprints]),
            net_tcp_msg_rate=mean([fp.net_tcp_msg_rate for fp in fingerprints]),
            net_bw_cpu_usage=mean([fp.net_bw_cpu_usage for fp in fingerprints]),
            net_lat_cpu_usage=mean([fp.net_lat_cpu_usage for fp in fingerprints]),
            net_tcp_latency=mean([fp.net_tcp_latency for fp in fingerprints]),
        )

class NodeScore(pydantic.BaseModel):
    max_score: float = 10.0
    min_score: float = 0.0
    score: float

    @pydantic.validator("score")
    def validate_score(cls, v, values):
        return max(values["min_score"], min(values["max_score"], v))

    # @property
    # def score(self):
    #     return max(self.min_score, min(self.max_score, self._score))


# @dataclass
class NodeScores(pydantic.BaseModel):
    node_name: str

    total: NodeScore

    cpu: NodeScore
    memory: NodeScore
    disk: NodeScore
    network: NodeScore

    details: Optional[Dict[str, NodeScore]] = {}


class BaseFingerprintEngine(ABC):
    @property
    def description(self) -> str:
        raise NotImplementedError

    async def get_fingerprint_for_node(self, node_name: str) -> BaseFingerprint:
        raise NotImplementedError

    async def get_fingerprint_for_cluster(self) -> BaseFingerprint:
        raise NotImplementedError

    async def get_scores_for_node(self, node_name: str, relative_to_cluster: bool) -> NodeScores:
        raise NotImplementedError

    async def get_scores(self, *node_names: str) -> Dict[str, NodeScores]:
        return {
            n: await self.get_scores_for_node(n) for n in node_names
        }

    async def get_fingerprints(self, *node_names: str) -> Dict[str, BaseFingerprint]:
        return {
            n: await self.get_fingerprint_for_node(n) for n in node_names
        }


class SimpleFingerprintEngine(BaseFingerprintEngine):
    @property
    def description(self) -> str:
        return "Simple Demo Fingerprint Engine"

    def __init__(self,
                 prometheus_client: PrometheusClient,
                 benchmark_history_client: BenchmarkHistoryClient,
                 k8s_client: K8sClient):
        self.prometheus_client = prometheus_client
        self.benchmark_history_client = benchmark_history_client
        self.k8s_client = k8s_client

    async def get_fingerprint_for_node(self, node_name: str) -> BaseFingerprint:
        recent_bms = self.benchmark_history_client.get_benchmarks_results(node_name)

        bms: Dict[str, Benchmark] = {}

        for bm in recent_bms:
            if bm.type not in bms:
                bms[bm.type] = bm
            elif bms[bm.type].started < bm.started:
                bms[bm.type] = bm

        def get_metric_value(bm_type: BenchmarkedResourceKind, metric_name: str, default_value: Optional[float] = None,
                             normalize: bool = True) -> Optional[float]:
            if bm_type.value in bms:
                bm_ts_start = bms[bm_type.value].started
                bm_ts_end = bms[bm_type.value].started + datetime.timedelta(seconds=bms[bm_type.value].duration)
                metrics_timeframe = datetime.timedelta(seconds=10)

                node_metrics = self.benchmark_history_client.get_node_metrics(node_name,
                                                                              bm_ts_start - metrics_timeframe,
                                                                              bm_ts_end + metrics_timeframe)

                def get_metric_avg(metric_name: str) -> float:
                    values = [float(nm.value) for nm in node_metrics if nm.metric == metric_name]
                    return mean(values)

                cpu_busy_avg: float = get_metric_avg("cpu_busy") / 100.0
                # memory_used_avg: float = get_metric_avg("memory_used") / 100.0 # useless
                disk_io_util_avg: float = get_metric_avg("disk_io_util") / 100.0

                mt = next(filter(lambda m: m.name == metric_name and m.value is not None, bms[bm_type.value].metrics),
                          None)
                if mt is not None and mt.value is not None:
                    value = mt.value
                    if normalize:
                        if bm_type == BenchmarkedResourceKind.CPU_SYSBENCH and cpu_busy_avg > 0:
                            value /= cpu_busy_avg
                        elif bm_type in (BenchmarkedResourceKind.DISK_FIO,
                                         BenchmarkedResourceKind.DISK_IOPING) and disk_io_util_avg > 0:
                            value /= disk_io_util_avg

                    return value

            return default_value

        fp = SimpleFingerprint(
            node_name,
            datetime.datetime.utcnow(),
            cpu_events_per_second=get_metric_value(BenchmarkedResourceKind.CPU_SYSBENCH, "events_per_second", 0.0),
            cpu_latency_95=get_metric_value(BenchmarkedResourceKind.CPU_SYSBENCH, "latency_95p", 0.0),
            disk_iops=get_metric_value(BenchmarkedResourceKind.DISK_IOPING, "iops", 0.0),
            disk_latency_avg=get_metric_value(BenchmarkedResourceKind.DISK_IOPING, "latency_avg", 0.0),
            disk_write_iops=get_metric_value(BenchmarkedResourceKind.DISK_FIO, "write_iops", 0.0),
            disk_write_mibps=get_metric_value(BenchmarkedResourceKind.DISK_FIO, "write_mibps", 0.0),
            mem_exctime=get_metric_value(BenchmarkedResourceKind.MEMORY_SYSBENCH, "fairness_exctime", 0.0),
            mem_latency_max=get_metric_value(BenchmarkedResourceKind.MEMORY_SYSBENCH, "latency_max", 0.0),
            net_bw_cpu_usage=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_bw_send_cpus_used", 0.0),
            net_lat_cpu_usage=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_lat_loc_cpus_used", 0.0),
            net_tcp_latency=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_lat_latency", 0.0),
            net_tcp_msg_rate=get_metric_value(BenchmarkedResourceKind.NETWORK_QPERF, "tcp_bw_msg_rate", 0.0),
            net_transfer_bitrate=get_metric_value(BenchmarkedResourceKind.NETWORK_IPERF3, "transfer_bitrate", 0.0)
        )

        return fp

    async def get_fingerprint_for_cluster(self) -> SimpleFingerprint:
        nodes = self.k8s_client.get_nodes()
        if nodes is not None:
            fps: List[SimpleFingerprint] = []
            for n in nodes:
                n_fp = await self.get_fingerprint_for_node(n.metadata.name)
                fps.append(n_fp)

            return SimpleFingerprint.mean(fps)
            

    async def get_scores_for_node(self, node_name: str, relative_to_cluster: bool=False) -> NodeScores:
        fp = await self.get_fingerprint_for_node(node_name)

        if relative_to_cluster:
            ref_fingerprint = await self.get_fingerprint_for_cluster()
        else:
            # TODO: global reference fingerprint
            ref_fingerprint = SimpleFingerprint(
                _node_name=node_name,
                _utctimestamp=datetime.datetime(2022, 5, 25, 18, 47, 00),
                cpu_events_per_second=73834.30137412282,
                cpu_latency_95=0.7090241200365385,
                mem_latency_max=52.53,
                mem_exctime=8.4504,
                disk_iops=869.149952244506,
                disk_latency_avg=6.566380133715361,
                disk_write_iops=5000,
                disk_write_mibps=18000,
                net_transfer_bitrate=2.5,
                net_tcp_msg_rate=63.6,
                net_tcp_latency=15.7,
                net_bw_cpu_usage=565.0,
                net_lat_cpu_usage=264.0
            )

        return NodeScores(
            node_name=node_name,
            total=NodeScore(score=fp.compare_to(ref_fingerprint) * 10),
            cpu=NodeScore(score=fp.compare_to(ref_fingerprint, for_resource=BenchmarkedResource.CPU) * 10),
            memory=NodeScore(score=fp.compare_to(ref_fingerprint, for_resource=BenchmarkedResource.MEMORY) * 10),
            disk=NodeScore(score=fp.compare_to(ref_fingerprint, for_resource=BenchmarkedResource.DISK) * 10),
            network=NodeScore(score=fp.compare_to(ref_fingerprint, for_resource=BenchmarkedResource.NETWORK) * 10),
            details={brk.name: NodeScore(score=fp.compare_to(ref_fingerprint, for_kind=brk) * 10)
                     for brk in BenchmarkedResourceKind}
        )


@lru_cache()
def get_fingerprint_engine() -> BaseFingerprintEngine:
    return SimpleFingerprintEngine(get_prometheus_client(), BenchmarkHistoryClient(), get_k8s_client())
