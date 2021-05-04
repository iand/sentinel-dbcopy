#!/usr/bin/python3

import os
import pathlib
import subprocess
import sys
import time

from helpers import tables


def import_table(connect_str, table_name, columns):
    filename = f"{table_name}.csv"
    if not os.path.isfile(filename):
        print(f"Could not find {filename} in {os.getcwd()}")
        return
    tmp_table_name = f"backfill_temp_{table_name}"
    # Split into multiple commands because psql requires \copy to be a separate command
    command1 = f"""BEGIN TRANSACTION;CREATE TEMP TABLE {tmp_table_name} ON COMMIT DROP AS SELECT * FROM public.{table_name} WITH NO DATA;"""
    command2 = f"""\\copy {tmp_table_name}({columns}) FROM '{filename}' DELIMITER ',' CSV HEADER;"""
    command3 = f"""INSERT INTO public.{table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING;COMMIT;"""
    # print(f"Loading {table_name}")
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


if __name__ == "__main__":
    print("STARTING")
    connect_str = os.environ["DATABASE_URL"]
    table_name = os.environ["TABLE_NAME"]
    from_height = os.environ["VISOR_HEIGHT_FROM"]
    to_height = os.environ["VISOR_HEIGHT_TO"]
    step = int(os.environ.get("VISOR_BACKFILL_STEP", 1000))
    csv_path_base = os.environ["CSV_PATH"]
    for i in range(int(from_height), int(to_height), step):
        csv_path = f"{csv_path_base}/{i}__{i+step}"
        # print(csv_path)
        os.chdir(csv_path)
        print(i, end=" ")
        import_table(connect_str, table_name, tables[table_name])
