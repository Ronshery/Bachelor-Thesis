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
    return kopf.login_with_kubeconfig(**_)
