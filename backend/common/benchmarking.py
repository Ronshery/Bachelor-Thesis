import datetime
import time

from common.monitoring import handle_monitoring


def handle_benchmarking(name, spec, stopped, logger,
                        started: datetime.datetime,
                        runtime: datetime.timedelta):
    while not stopped:
        time.sleep(5)

    # TODO: do something with collected metrics
    # get metrics
    benchmark_job_dict = handle_monitoring(name, {}, logger, started, runtime)

    logger.info(f"Deleted {name}")
