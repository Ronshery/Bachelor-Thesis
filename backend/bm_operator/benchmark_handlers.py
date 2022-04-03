# ######################################
# HANDLERS FOR BENCHMARK JOBS ###
# ######################################
import kopf

from common.benchmarking import handle_benchmarking


def bmfw_filter(spec, meta, **_):
    return meta.get("name") == "sysbench-bmfw"


@kopf.daemon("sysbenches", when=bmfw_filter)
def handle_cpu_sysbench_benchmarking(spec, stopped, logger, started, runtime, **_):
    print(f"HANDLING BENCHMARKING SYSBENCH: {_['meta']['name']}")
    handle_benchmarking("cpu-sysbench", spec, stopped, logger, started, runtime)


@kopf.daemon("fios")
def handle_fio_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("iopings")
def handle_ioping_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("sysbenchs", __name="memory-sysbench")
def handle_memory_sysbench_benchmarking(spec, stopped, logger, started, runtime, **_):
    handle_benchmarking("memory-sysbench", spec, stopped, logger, started, runtime)


@kopf.daemon("iperf3s")
def handle_iperf3_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)


@kopf.daemon("qperfs")
def handle_qperf_benchmarking(name, spec, stopped, logger, started, runtime, **_):
    handle_benchmarking(name, spec, stopped, logger, started, runtime)