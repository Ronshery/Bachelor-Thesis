from typing import Dict

import pykube

from common.benchmarks.base import BaseBenchmark, BenchmarkStartupResult, BenchmarkedResourceKind


class NetworkIperf3Benchmark(BaseBenchmark):
    @property
    def kind(self):
        return "Iperf3"

    @property
    def resource_kind(self) -> BenchmarkedResourceKind:
        return BenchmarkedResourceKind.NETWORK_IPERF3

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
            "clientConfiguration": {"podScheduling": {"nodeName": client_node_name}, "podLabels": {"resourceKind": self.resource_kind.value}},
            "serverConfiguration": {"podScheduling": {"nodeName": server_node_name}, "podLabels": {"resourceKind": self.resource_kind.value}}
        }})
        self.get_factory(client, self.kind)(client, spec).create()
        # TODO add pod
        return BenchmarkStartupResult(success=True, id=spec['metadata']['name'], benchmark_spec=spec)


class NetworkQperfBenchmark(NetworkIperf3Benchmark):
    @property
    def kind(self):
        return "Qperf"

    @property
    def resource_kind(self) -> BenchmarkedResourceKind:
        return BenchmarkedResourceKind.NETWORK_QPERF

    @property
    def config_path(self):
        return "config/network_qperf.yaml"

    @property
    def name(self):
        return "network-qperf"
