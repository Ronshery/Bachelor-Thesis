# ######################################
# HANDLERS FOR BENCHMARK JOBS ###
# ######################################
import kopf

from common.benchmarking import handle_benchmarking


def cpu_sysbench_filter(spec, meta, **_):
    return meta.get("name").startswith("cpu-sysbench")


@kopf.daemon("sysbenches", when=cpu_sysbench_filter)
def handle_cpu_sysbench_benchmarking(spec, stopped, logger, started, runtime, **_):
    handle_benchmarking("cpu-sysbench", spec, stopped, logger, started, runtime)


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