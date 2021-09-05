import pendulum
import subprocess
import paramiko
import os
import sys
import select
import time
from helpers import (
    get_start_end_epocs,
    set_prometheus_env,
    get_output_folder,
    setup_rclone,
    get_snapshot_folder,
    setup_rclone,
)
from pathlib import Path


def get_from_s3_for(epoc):
    repos = [
        471050,
        505660,
        544858,
        598300,
        745340,
        764950,
        778800,
        845164,
        908400,
        1012080,
        1066800,
        1084080,
    ]
    for repo_epoc in repos:
        if repo_epoc > epoc:
            return f"s3://sentinel-backfill/repo/mainnet/{repo_epoc}"


set_prometheus_env()

start_epoc, end_epoc = get_start_end_epocs()

s3_repo_path = get_from_s3_for(end_epoc)
if s3_repo_path:
    print(f"Fetching from {s3_repo_path}")
    subprocess.run("rm -rf /repo/*", shell=True, check=True)
    command = f"s5cmd cp --if-size-differ '{s3_repo_path}/*' /repo/"
else:
    folder = get_snapshot_folder()
    setup_rclone()
    subprocess.run("rm -rf /repo/*", shell=True, check=True)
    print(f"Fetching from sftp:snapshots/{folder}")
    command = f"rclone copy --ignore-checksum sftp:snapshots/{folder}/lotus_datadir /repo"
subprocess.run(
    command,
    shell=True,
    check=True,
)

Path("/repo/keystore").mkdir(exist_ok=True)

    

CSV_PATH = get_output_folder()
Path(CSV_PATH).mkdir(parents=True, exist_ok=True)
for csv_path in Path(CSV_PATH).glob("*.csv"):
    csv_path.unlink()


config = f"""[Libp2p]
AnnounceAddresses = []

[Pubsub]
RemoteTracer = ""

[Storage]
[Storage.File]
[Storage.File.CSV]
Format = "CSV"
Path = "{CSV_PATH}"
FilePattern = "{{table}}.csv"
OmitHeader = false
"""

with Path("/repo/config.toml").open('w') as config_file:
    config_file.write(config)

task_list = os.environ["LILY_WALK_TASKS"]
daemon_command = "/usr/bin/lily --log-level=error --log-level-named=lily/chain:info,lily/storage:info,lily/schedule:info,lens/util:info daemon --bootstrap=false --repo=/repo"
start_walk_command = f"/usr/bin/lily walk --tasks {task_list} --from {start_epoc} --to {end_epoc} --storage CSV"

print(f"running: {daemon_command}", flush=True)
daemon = subprocess.Popen(
    daemon_command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=0,
)

timeout = time.time() + 60*30

exit_code = os.EX_SOFTWARE
scheduler_started = False
while daemon.poll() is None:
    if time.time() > timeout:
        if not scheduler_started:
            sys.exit(exit_code)
    line = daemon.stderr.readline()
    print(line, end="")
    if "Starting Scheduler" in line:
        scheduler_started = True
        subprocess.run(start_walk_command, shell=True, check=True)
    if "job exited cleanly" in line:
        exit_code = os.EX_OK    
    if "job execution ended" in line:
        sys.exit(exit_code)