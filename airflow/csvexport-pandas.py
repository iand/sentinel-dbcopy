import os
import pathlib
import dask.dataframe as dd
from dask.distributed import Client

from helpers import get_dt, get_output_folder, get_start_end_epocs
import yaml

client = Client(memory_limit="7GB", processes=False)

file_path = pathlib.Path(__file__).parent.absolute()
with open(file_path / "schema.yaml") as f:
    schema = yaml.safe_load(f)


def df_for_table(table_name):
    start_height, stop_height = get_start_end_epocs()
    csv_path = f"{table_name}.csv"
    df = dd.read_csv(csv_path, dtype=str, blocksize="512MB")
    if "height" in schema[table_name]["columns"]:
        df["height"] = df["height"].astype(int)
        df = df.query(f"{start_height} <= height < {stop_height}").drop_duplicates(
            subset=schema[table_name]["pkeys"], keep="last"
        )
    return df


def get_export_filname():
    csv_base_path = os.getenv("CSV_BASE_PATH", "/output")
    dt = get_dt()
    return f"{csv_base_path}/export/{table_name}/{dt}.zip"


if __name__ == "__main__":
    table_name = os.environ["SENTINEL_AIRFLOW_TABLENAME"]
    csv_path = get_output_folder()
    print(f"Running in {csv_path}", flush=True)
    os.chdir(csv_path)
    export_filename = get_export_filname()
    print(f"Slurping up {table_name}.csv", flush=True)
    df = df_for_table(table_name)
    print(f"Writing to {export_filename}", flush=True)
    df.to_csv(
        export_filename,
        index=False,
        header=False,
        compression="gzip",
        single_file=True,
    )
    print(f"DONE", flush=True)
