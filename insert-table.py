#!/usr/bin/python3

import os
import pendulum

from helpers import import_table, get_output_folder


if __name__ == "__main__":
    print("STARTING")
    connect_str = os.environ["DATABASE_URL"]
    table_name = os.environ["TABLE_NAME"]
    os.environ["AIRFLOW_INTERVAL"] = "DAILY"
    os.environ["JOB_NAME"] = "airflow-backfill-csvonly"

    start = pendulum.parse("2020-09-18")
    end = pendulum.parse("2021-06-30")

    for day in pendulum.period(start, end).range("days"):
        os.environ["AIRFLOW_TS"] = str(day)
        csv_path = get_output_folder()
        print(f"Running in {csv_path}")
        os.chdir(csv_path)
        import_table(connect_str, table_name)
