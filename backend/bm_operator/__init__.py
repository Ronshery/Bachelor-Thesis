import time
import kopf

# use config file as desired
from . import operator_config


@kopf.on.login()
def login_fn(logger, **kwargs):
    logger.info("Creating ConnectionInfo from operator_config module")

    return kopf.ConnectionInfo(
        server=operator_config.KUBERNETES_SERVER,
        ca_path=operator_config.KUBERNETES_CA_PATH,
        insecure=True,
        username=operator_config.KUBERNETES_USERNAME,
        scheme=operator_config.KUBERNETES_AUTH_SCHEME,
        token=operator_config.KUBERNETES_TOKEN
    )


@kopf.on.cleanup()
async def cleanup_fn(logger, **kwargs):
    logger.info("Cleaning up kopf resources ...")
    pass


@kopf.on.create('kopfexamples')
async def create_fn(logger, spec, name, meta, status, **kwargs):
    logger.info(f"And here we are! Created {name} with spec: {spec}")


@kopf.daemon('kopfexamples')
async def my_daemon(spec, stopped, logger, **kwargs):
    while not stopped:
        logger.info(f"Object's spec: {spec}")
        time.sleep(1)
