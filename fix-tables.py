import csv
import os
import pprint
import shutil
from datetime import datetime

pp = pprint.pprint


def now():
    now = datetime.utcnow()
    return now.strftime("%Y%m%d-%H%m")


def fix_json(s):
    if s == "null":
        return "null"

    if s == "NULL":
        return "null"

    if s[0] == "[" and s[-1] == "]":
        elements = s[1:-1].split(" ")
        if elements[0][0] == '"':
            return s  # they are already quoted
        quoted = ['"' + item + '"' for item in elements]
        return "[" + ", ".join(quoted) + "]"

    raise RuntimeError(f"Don't know how to fix {s}")


def fix_json_fields(*field_names):
    def fix_row(row):
        for field in field_names:
            row[field] = fix_json(row[field])
        return row

    return fix_row


def backup_visorprocessing():
    shutil.copy(
        "visor_processing_reports.csv", f"visor_processing_reports.csv.{now()}.bak"
    )


def show_miner_infos():
    with open("miner_infos.csv") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            for field in ["control_addresses", "multi_addresses"]:
                value = row[field]
                if value[0] not in ["N", "n"]:
                    print(value)


def process_csv(csv_name, f):
    original_filename = f"{csv_name}.csv"
    if not os.path.isfile(original_filename):
        print(f"Skipping as does not exist: {os.path.abspath(original_filename)}")
        return
    backup_filename = f"{original_filename}.bak.{now()}"
    shutil.move(original_filename, backup_filename)
    with open(backup_filename) as in_file:
        reader = csv.DictReader(in_file)
        with open(original_filename, "w") as out_file:
            print(f"Writing to {os.path.abspath(original_filename)}", end=" ")
            writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                f(row)
                writer.writerow(row)
            print("✓")


# csv_path = f"/mnt/efs/backfill/379000__380000"
# os.chdir(csv_path)
# process_csv("miner_infos", fix_miner_infos)

if __name__ == "__main__":
    for i in range(138000, 380000, 1000):
        csv_path = f"/mnt/efs/backfill/{i}__{i+1000}"
        os.chdir(csv_path)
        # process_csv("miner_infos", fix_json_fields("control_addresses", "multi_addresses"))
        # show_miner_infos()
        backup_visorprocessing()
        # process_csv("multisig_transactions", fix_json_fields("approved"))
