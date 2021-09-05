import os
import subprocess
import pathlib
from helpers import get_output_folder, get_epocs_foldername
import yaml


if __name__ == "__main__":
    table_name = os.environ["SENTINEL_AIRFLOW_TABLENAME"]
    csv_path = get_output_folder()
    epocs_foldername = get_epocs_foldername()
    raw_s3_folder = "s3:/sentinel-backfill/raw"
    s3_target = f"{raw_s3_folder}/{epocs_foldername}"
    command = f"rclone copy {csv_path} {s3_target}"
    print(command, flush=True)
    subprocess.run(command, shell=True, check=True)
