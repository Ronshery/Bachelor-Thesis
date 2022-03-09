import asyncio

import kopf

# use config file as desired
from . import operator_config


@kopf.on.startup()
async def startup(logger, **_):
    logger.info('Starting Operator in 5s...')
    await asyncio.sleep(5)


@kopf.on.login()
async def login(logger, **_):
    logger.info("Creating ConnectionInfo from operator_config module")

    return kopf.ConnectionInfo(
        server=operator_config.KUBERNETES_SERVER,
        ca_path=operator_config.KUBERNETES_CA_PATH,
        insecure=True,
        username=operator_config.KUBERNETES_USERNAME,
        scheme=operator_config.KUBERNETES_AUTH_SCHEME,
        token=operator_config.KUBERNETES_TOKEN
    )
