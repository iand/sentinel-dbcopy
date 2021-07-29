import os
import subprocess
import pathlib
from helpers import get_output_folder, get_export_filename
import yaml


file_path = pathlib.Path(__file__).parent.absolute()
with open(file_path / "schema.yaml") as f:
    schema = yaml.safe_load(f)


if __name__ == "__main__":
    table_name = os.environ["SENTINEL_AIRFLOW_TABLENAME"]
    csv_path = get_output_folder()
    print(f"Running in {csv_path}", flush=True)
    os.chdir(csv_path)
    export_filename = get_export_filename(table_name)
    command = f"tail -n +2  {table_name}.csv | gzip > {export_filename}"
    print(f"Compressing {table_name}.csv to {export_filename}", flush=True)
    subprocess.run(command, shell=True, check=True)
