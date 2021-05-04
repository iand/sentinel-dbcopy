import pendulum
import subprocess
import os
from helpers import date_to_epoc, epoc_to_date
from pathlib import Path
import socket
from contextlib import closing


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


AIRFLOW_TS = os.environ["AIRFLOW_TS"]
JOB_NAME = os.environ["JOB_NAME"]

free_port = find_free_port()
os.environ["VISOR_PROMETHEUS_PORT"] = f":{free_port}"
eg_execution_time = "2021-03-20T00:00:00"
execution_time = pendulum.parse(AIRFLOW_TS)

start_time = execution_time.subtract(hours=9)
end_time = execution_time.subtract(hours=8)
start_epoc = date_to_epoc(start_time)
end_epoc = date_to_epoc(end_time)

print(execution_time)
print(f"from {start_epoc} to {end_epoc}, total: {end_epoc-start_epoc}")

CSV_PATH = f"/output/{JOB_NAME}/{start_epoc}__{end_epoc}"
Path(CSV_PATH).mkdir(parents=True, exist_ok=True)
for csv_path in Path(CSV_PATH).glob("*.csv"):
    csv_path.unlink()

command = f"/usr/bin/visor run walk --db '' --from {start_epoc} --to {end_epoc} --csv {CSV_PATH}"

print(f"running: {command}", flush=True)

subprocess.run(command, shell=True, check=True)