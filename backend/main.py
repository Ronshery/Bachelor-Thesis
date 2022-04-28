import asyncio
import contextlib
import threading
from typing import Optional, Any

import kopf
import uvicorn
import uvloop
from uvloop.loop import Loop
from bm_api import app

import argparse

# this thread will start kopf, i.e. our custom kubernetes operator that listens to kubernetes events, acts accordingly
def kopf_thread(stop_me: threading.Event) -> None:
    try:
        # import needed to active kopf operator
        import bm_operator
        
        kopf_loop = uvloop.new_event_loop()
        asyncio.set_event_loop(kopf_loop)

        with contextlib.closing(kopf_loop):
            kopf.configure(verbose=True)
            kopf_loop.run_until_complete(kopf.operator(stop_flag=stop_me, clusterwide=True))  # for graceful termination
    finally:
        stop_me.set()


# this thread will start a fastapi-backend, which can process requests from the frontend
def api_thread(stop_me: threading.Event, host: str, port: int) -> None:
    api_loop: Optional[Loop] = None
    pending: Any = None
    try:
        api_loop = uvloop.new_event_loop()
        asyncio.set_event_loop(api_loop)

        # monitor the flag and stop it somehow. here, disgracefully.
        with contextlib.closing(api_loop):
            config = uvicorn.Config(app=app, loop=api_loop, host=host, port=port)
            server = uvicorn.Server(config)
            server_task = asyncio.gather(server.serve())
            waiter_task = asyncio.gather(api_loop.run_in_executor(None, stop_me.wait))
            done, pending = api_loop.run_until_complete(
                asyncio.wait({server_task, waiter_task}, return_when=asyncio.FIRST_COMPLETED))
    finally:
        stop_me.set()

        if pending is not None:
            for task in pending:
                task.cancel()
        if api_loop is not None and pending is not None:
            api_loop.run_until_complete(asyncio.gather(pending))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Benchmarking Framework HTTP API server")
    parser.add_argument("--host", dest="host", action="store", type=str, default="0.0.0.0")
    parser.add_argument("--port", dest="port", action="store", type=int, default=8000)

    cli_namespace = parser.parse_args()

    api_host = cli_namespace.host
    api_port = cli_namespace.port

    import orm
    orm.create_tables()

    stop_me_event: threading.Event = threading.Event()
    t_kopf: threading.Thread = threading.Thread(target=kopf_thread, args=(stop_me_event,))
    t_api: threading.Thread = threading.Thread(target=api_thread, args=(stop_me_event,), kwargs={
        "host": api_host,
        "port": api_port
    })

    t_kopf.start()
    t_api.start()

    try:
        t_api.join()
        t_kopf.join()
    except KeyboardInterrupt:
        stop_me_event.set()

        t_api.join()
        t_kopf.join()
    finally:
        print("benchmarking-framework: Backend has shut down.")
