from fastapi import FastAPI

from . import api_config

app = FastAPI()


@app.get("/version")
async def get_version():
    return {
        "version": api_config.BMAPI_VERSION
    }

