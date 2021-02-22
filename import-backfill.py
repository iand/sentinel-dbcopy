#!/usr/bin/python3

import os
import subprocess
import sys
import time

from shared import now, tables


def import_table(connect_str, table_name, columns):
    filename = f"{table_name}.csv"
    if not os.path.isfile(filename):
        print(f"Could not find {filename} in {os.getcwd()}")
        # sys.exit(1)
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


if __name__ == "__main__":
    connect_str = os.environ["DATABASE_URL"]
    csv_path = os.environ["CSV_PATH"]
    os.chdir(csv_path)
    for name in tables:
        import_table(connect_str, name, tables[name])
