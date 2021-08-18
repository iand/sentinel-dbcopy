#!/usr/bin/python3
import yaml
import os
import pendulum
import pathlib
import subprocess
from helpers import get_output_folder, get_export_filename, tables

file_path = pathlib.Path(__file__).parent.absolute()
with open(file_path / "schema.yaml") as f:
    schema = yaml.safe_load(f)

if __name__ == "__main__":
    print("STARTING")
    os.environ["AIRFLOW_INTERVAL"] = "DAILY"
    os.environ["JOB_NAME"] = "airflow-backfill-csvonly"

    # start = pendulum.parse("2020-08-24")
    start = pendulum.parse("2021-07-12")
    end = pendulum.parse("2021-08-15")
    table_name = os.environ["TABLE_NAME"]
    for day in pendulum.period(start, end).range("days"):
        os.environ["AIRFLOW_TS"] = str(day)
        csv_path = get_output_folder()
        os.chdir(csv_path)

        export_filename = get_export_filename(table_name)
        command = f"tail -n +2  {table_name}.csv | gzip > {export_filename}"
        print(
            f"{day}: Compressing {table_name}.csv to {export_filename}",
            flush=True,
            end=" ",
        )
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            print("✓", flush=True)
        else:
            print("❌")
            print(process.stderr)
            print(process.stdout, flush=True)
