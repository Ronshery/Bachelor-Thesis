import asyncio
import kopf

# needed to load kopf operators for benchmark handling
from . import benchmark_handlers


@kopf.on.startup()
async def startup(logger, **_):
    logger.info('Starting Operator in 1s...')
    await asyncio.sleep(1)


@kopf.on.login()
async def login(logger, **_):
    return kopf.login_via_pykube(logger=logger)
