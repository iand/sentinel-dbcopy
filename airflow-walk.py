import pendulum
import subprocess
import paramiko
import os
from helpers import get_start_end_epocs, set_prometheus_env, get_output_folder
from pathlib import Path


def get_from_s3_for(epoc):
    repos = [471050, 505660, 544858, 598300, 745340, 764950, 778800, 845164]
    for repo_epoc in repos:
        if repo_epoc > epoc:
            return f"s3://sentinel-backfill/repo/mainnet/{repo_epoc}"


set_prometheus_env()


start_epoc, end_epoc = get_start_end_epocs()

if os.getenv("VISOR_LENS") == "lotusrepo":
    s3_repo_path = get_from_s3_for(end_epoc)
    if s3_repo_path:
        print(f"Fetching from {s3_repo_path}")
        subprocess.run("rm -rf /repo/*", shell=True, check=True)
        command = f"s5cmd cp --if-size-differ '{s3_repo_path}/*' /repo/"
    else:
        ssh_key_folder = Path.home() / ".ssh"
        ssh_key_folder.mkdir()
        ssh_key_path = ssh_key_folder / "id_ed25519_snapreader"
        with ssh_key_path.open("w") as ssh_key_file:
            ssh_key_file.write(os.environ["SYNC_SSH_KEY"])
        pk = paramiko.Ed25519Key.from_private_key_file(ssh_key_path)
        host = "172.31.42.56"
        username = "snapreader"
        transport = paramiko.Transport(host)
        transport.connect(username=username, pkey=pk)
        sftp = paramiko.SFTPClient.from_transport(transport)
        folders = sftp.listdir("snapshots")
        folder = sorted(folders)[-1]
        subprocess.run(
            f"rclone config create sftp sftp host {host} user {username} key_file {ssh_key_path}",
            shell=True,
            check=True,
        )
        subprocess.run("rm -rf /repo/*", shell=True, check=True)
        print(f"Fetching from sftp:snapshots/{folder}")
        command = f"rclone copy sftp:snapshots/{folder}/lotus_datadir /repo"
    subprocess.run(
        command,
        shell=True,
        check=True,
    )


CSV_PATH = get_output_folder()
Path(CSV_PATH).mkdir(parents=True, exist_ok=True)
for csv_path in Path(CSV_PATH).glob("*.csv"):
    csv_path.unlink()


command = f"/usr/bin/visor run walk --db '' --from {start_epoc} --to {end_epoc} --csv {CSV_PATH}"

print(f"running: {command}", flush=True)

subprocess.run(command, shell=True, check=True)
