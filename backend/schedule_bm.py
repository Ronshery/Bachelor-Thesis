import sys
import time
import requests
import datetime

bm_type: str = sys.argv[1] if len(sys.argv) > 1 else "cpu-sysbench"
bm_delay: int = int(sys.argv[2]) if len(sys.argv) > 2 else 40
bm_node: str = sys.argv[3] if len(sys.argv) > 3 else "benchmark-operator-worker"

print(f"{bm_node=}, {bm_type=}, {bm_delay=}")

api_endpoint = "http://localhost:8004"

def apiclient_get(path: str):
    return requests.get(f"{api_endpoint}{path}").json()

def apiclient_post(path: str):
    return requests.post(f"{api_endpoint}{path}").json()

while True:
    try:
        rsp = apiclient_post(f"/benchmark/{bm_type}/{bm_node}")
        print(f"Benchmark {bm_type} started as '{rsp['id']}'")
        print(rsp, end="\n\n")
    except KeyboardInterrupt as e:
        break
        
    time.sleep(bm_delay)
