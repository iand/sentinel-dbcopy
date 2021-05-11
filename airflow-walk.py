import pendulum
import subprocess
import os
from helpers import get_start_end_epocs, set_prometheus_env, get_output_folder
from pathlib import Path


set_prometheus_env()


CSV_PATH = get_output_folder()
Path(CSV_PATH).mkdir(parents=True, exist_ok=True)
for csv_path in Path(CSV_PATH).glob("*.csv"):
    csv_path.unlink()

start_epoc, end_epoc = get_start_end_epocs()

command = f"/usr/bin/visor run walk --db '' --from {start_epoc} --to {end_epoc} --csv {CSV_PATH}"

print(f"running: {command}", flush=True)

subprocess.run(command, shell=True, check=True)
