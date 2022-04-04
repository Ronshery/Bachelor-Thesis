import datetime
import time

from kopf import Spec

from common.monitoring import handle_monitoring


def handle_benchmarking(name,
                        spec: Spec,
                        stopped,
                        logger,
                        started: datetime.datetime,
                        runtime: datetime.timedelta,
                        **kwargs):

    logger.info(f"{name}: started: {started}, {spec}")

    while not stopped:
        time.sleep(5)

    print(f"{datetime.datetime.utcnow()}: {name}  HAS stopped")

    # TODO: do something with collected metrics
    # get metrics
    benchmark_job_dict = handle_monitoring(name, {}, logger, started, runtime)

    logger.info(f"Deleted {name}")
