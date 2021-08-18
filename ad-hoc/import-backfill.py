#!/usr/bin/python3

import os
import subprocess
import sys
import time

from helpers import tables, import_table

if __name__ == "__main__":
    connect_str = os.environ["DATABASE_URL"]
    csv_path = os.environ["CSV_PATH"]
    os.chdir(csv_path)
    for tablename in tables:
        import_table(connect_str, tablename)
