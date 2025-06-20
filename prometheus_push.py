import requests
import os

def push_metric(url, is_up):
    gateway_url = os.getenv("PUSHGATEWAY_URL", "http://localhost:9091")
    stream_name = url.split("/")[-1]
    metric = f'stream_up{{stream=\"{stream_name}\"}} {1 if is_up else 0}\n'

    requests.post(
        f"{gateway_url}/metrics/job/lofi_monitor/instance/{stream_name}",
        data=metric,
        headers={"Content-Type": "text/plain"}
    )
