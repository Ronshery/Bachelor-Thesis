from typing import Type, Dict

import pykube
from pykube.objects import APIObject

from bm_api.benchmarks.base import BaseBenchmark, BenchmarkStartupResult


class NetworkIperf3Benchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Iperf3"

    @property
    def config_path(self):
        return "config/network_iperf3.yaml"

    @property
    def name(self):
        return "network-iperf3"

    def _run(self, client: pykube.HTTPClient, spec: Dict,
             *args, **kwargs) -> BenchmarkStartupResult:
        client_node_name, server_node_name = (args[0].split("@@@") + [None, None])[:2]
        spec = self.merge_dicts(spec, {"spec": {
            "clientConfiguration": {"podScheduling": {"nodeName": client_node_name}},
            "serverConfiguration": {"podScheduling": {"nodeName": server_node_name}}
        }})
        self.get_factory(client, self.kind)(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, pod=None, benchmark_spec=self)


class NetworkQperfBenchmark(NetworkIperf3Benchmark):
    @property
    def kind(self):
        return "Qperf"

    @property
    def config_path(self):
        return "config/network_qperf.yaml"

    @property
    def name(self):
        return "network-qperf"
