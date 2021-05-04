#!/usr/bin/python3

import os
import subprocess
import sys
import time

from helpers import get_output_folder, tables


def import_table(connect_str, table_name, columns):
    filename = f"{table_name}.csv"
    if not os.path.isfile(filename):
        # raise Exception(f"Could not find {filename} in {os.getcwd()}")
        print(f"Could not find {filename} in {os.getcwd()}")
    tmp_table_name = f"backfill_temp_{table_name}"
    # Split into multiple commands because psql requires \copy to be a separate command
    command1 = f"""BEGIN TRANSACTION;CREATE TEMP TABLE {tmp_table_name} ON COMMIT DROP AS SELECT * FROM public.{table_name} WITH NO DATA;"""
    command2 = f"""\\copy {tmp_table_name}({columns}) FROM '{filename}' DELIMITER ',' CSV HEADER;"""
    command3 = f"""INSERT INTO public.{table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING;COMMIT;"""
    print(f"Loading {table_name}", end=" ")
    process = subprocess.run(
        [
            "psql",
            "-q",
            "-a",
            "-X",
            "-t",
            "-d",
            connect_str,
            "-c",
            command1,
            "-c",
            command2,
            "-c",
            command3,
        ],
        capture_output=True,
        text=True,
    )
    if process.returncode == 0:
        print("✓")
    else:
        print("❌")
        print(process.stderr)
        print(process.stdout)
        raise Exception(f"Could not import {table_name}")


if __name__ == "__main__":
    failed = False
    connect_str = os.environ["DATABASE_URL"]
    csv_path = get_output_folder()
    print(f"Running in {csv_path}")
    os.chdir(csv_path)
    if not os.path.isfile("visor_processing_reports.csv"):
        print("Could not find visor_processing_reports")
        # We should do more than just check it exists, it needs to have entries for each task/epoc
        sys.exit(1)
    for name in tables:
        try:
            import_table(connect_str, name, tables[name])
        except Exception as err:
            print(err)
            failed = True
    if failed:
        print("Failed!")
        sys.exit(1)