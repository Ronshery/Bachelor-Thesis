# ######################################
# HANDLERS FOR BENCHMARK JOBS ###
# ######################################
import kopf

from common.benchmarking import handle_benchmarking
from common.metrics import \
    SysbenchCpuMetrics, \
    SysbenchMemoryMetrics, \
    NetworkIperf3Metrics, \
    FiosMetrics, \
    IopingsMetrics, \
    QpervesMetrics


def cpu_sysbench_filter(spec, meta, **_):
    return meta.get("name").startswith("cpu-sysbench")


def memory_sysbench_filter(spec, meta, **_):
    return meta.get("name").startswith("memory-sysbench")


@kopf.daemon("sysbenches", when=cpu_sysbench_filter)
def handle_cpu_sysbench_benchmarking(namespace, name, logger, started, stopped, body, **_):
    handle_benchmarking(namespace, name, logger, started, stopped, body, metrics_cls=SysbenchCpuMetrics)


@kopf.daemon("sysbenches", when=memory_sysbench_filter)
def handle_memory_sysbench_benchmarking(namespace, name, logger, started, stopped, body, **_):
    handle_benchmarking(namespace, name, logger, started, stopped, body, metrics_cls=SysbenchMemoryMetrics)


@kopf.daemon("fios")
def handle_fio_benchmarking(namespace, name, logger, started, stopped, body, **_):
    handle_benchmarking(namespace, name, logger, started, stopped, body, metrics_cls=FiosMetrics)


@kopf.daemon("iopings")
def handle_ioping_benchmarking(namespace, name, logger, started, stopped, body, **_):
    handle_benchmarking(namespace, name, logger, started, stopped, body, metrics_cls=IopingsMetrics)


@kopf.daemon("iperf3s")
def handle_iperf3_benchmarking(namespace, name, logger, started, stopped, body, **_):
    # TODO: only use client version for now
    handle_benchmarking(namespace, f"{name}-client", logger, started, stopped, body, job_name=name, metrics_cls=NetworkIperf3Metrics)


@kopf.daemon("qperves")
def handle_qperf_benchmarking(namespace, name, logger, started, stopped, body, **_):
    # TODO: only use client version for now
    handle_benchmarking(namespace, f"{name}-client", logger, started, stopped, body, job_name=name, metrics_cls=QpervesMetrics)
