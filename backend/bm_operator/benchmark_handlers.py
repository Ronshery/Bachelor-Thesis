# ######################################
# HANDLERS FOR BENCHMARK JOBS ###
# ######################################
import kopf

from common.benchmarking import handle_benchmarking
from common.metrics import SysbenchCpuMetrics, SysbenchMemoryMetrics, NetworkIperf3Metrics


def cpu_sysbench_filter(spec, meta, **_):
    return meta.get("name").startswith("cpu-sysbench")


def memory_sysbench_filter(spec, meta, **_):
    return meta.get("name").startswith("memory-sysbench")


@kopf.daemon("sysbenches", when=cpu_sysbench_filter)
def handle_cpu_sysbench_benchmarking(name, spec, stopped, logger, started, **_):
    handle_benchmarking(name, spec, stopped, logger, started, SysbenchCpuMetrics)


@kopf.daemon("sysbenches", when=memory_sysbench_filter)
def handle_memory_sysbench_benchmarking(name, spec, stopped, logger, started, **_):
    handle_benchmarking(name, spec, stopped, logger, started, SysbenchMemoryMetrics)


@kopf.daemon("fios")
def handle_fio_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("iopings")
def handle_ioping_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("iperf3s")
def handle_iperf3_benchmarking(name, spec, stopped, logger, started, **_):
    # TODO: only use client version for now
    name = "network-iperf3-client"

    handle_benchmarking(name, spec, stopped, logger, started, NetworkIperf3Metrics)


@kopf.daemon("qperves")
def handle_qperf_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)