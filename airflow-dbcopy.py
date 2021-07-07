#!/usr/bin/python3

import os
import subprocess
import sys
import time

from helpers import get_output_folder, tables, import_table


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
