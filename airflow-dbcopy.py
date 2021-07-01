#!/usr/bin/python3

import os
import subprocess
import sys
import time

from helpers import get_output_folder, tables, v1_tables


def import_table(connect_str, table_name):
    v1_filename = f"{table_name}.csv"
    v0_filename = f"{table_name}.v0.csv"
    v0_columns = tables[table_name]
    v1_columns = tables[table_name]
    if table_name in v1_tables:
        v1_columns = v1_tables[table_name]
        csv_cut_comand = (
            f"/usr/bin/csvcut -c {v0_columns} {v1_filename} > {v0_filename}"
        )
        print(csv_cut_comand, flush=True)
        subprocess.run(csv_cut_comand, shell=True, check=True)

    if os.getenv("VISOR_SCHEMA_VERSION") == "v0":
        import_filename = v0_filename
        columns = v0_columns
    else:
        import_filename = v1_filename
        columns = v1_columns

    visor_database_schema = os.getenv("VISOR_DATABASE_SCHEMA", "visor")
    if not os.path.isfile(v1_filename):
        # raise Exception(f"Could not find {filename} in {os.getcwd()}")
        print(f"Could not find {v1_filename} in {os.getcwd()}")
    tmp_table_name = f"backfill_temp_{table_name}"
    # Split into multiple commands because psql requires \copy to be a separate command
    command1 = f"""BEGIN TRANSACTION;CREATE TEMP TABLE {tmp_table_name} ON COMMIT DROP AS SELECT * FROM {visor_database_schema}.{table_name} WITH NO DATA;"""
    command2 = f"""\\copy {tmp_table_name}({columns}) FROM '{import_filename}' DELIMITER ',' CSV HEADER;"""
    command3 = f"""INSERT INTO {visor_database_schema}.{table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING;COMMIT;"""
    print(f"Loading {table_name} from {import_filename}", end=" ", flush=True)
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
        print("✓", flush=True)
    else:
        print("❌")
        print(process.stderr)
        print(process.stdout, flush=True)
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
            import_table(connect_str, name)
        except Exception as err:
            print(err)
            failed = True
    if failed:
        print("Failed!")
        sys.exit(1)
