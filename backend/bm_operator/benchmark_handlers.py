# ######################################
# HANDLERS FOR BENCHMARK JOBS ###
# ######################################
import kopf

from common.benchmarking import handle_benchmarking


def sysbench_cpu_filter(spec, meta, **_):
    return meta.get("name") == "sysbench-cpu"


@kopf.daemon("sysbenches", when=sysbench_cpu_filter)
def handle_cpu_sysbench_benchmarking(spec, stopped, logger, started, runtime, **_):
    handle_benchmarking("sysbench-cpu", spec, stopped, logger, started, runtime)


@kopf.daemon("fios")
def handle_fio_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("iopings")
def handle_ioping_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("iperf3s")
def handle_iperf3_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("qperves")
def handle_qperf_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)