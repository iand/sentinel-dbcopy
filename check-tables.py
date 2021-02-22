import sys
from pathlib import Path

import datacompy
import humanize
import pandas as pd
import psycopg2

CSV_ROOT = Path("/mnt/efs/backfill")


def csv_file_for(table_name, start_height):
    return CSV_ROOT / f"{start_height}__{start_height + 1000}" / f"{table_name}.csv"


def df_from_csv(table_name, start_height):
    csv_file = csv_file_for(table_name, start_height)
    df = pd.read_csv(csv_file)
    return df.query(f"{start_height} <= height < {start_height + 1000} ")


def connect(db_url):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(db_url)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    # print("Connection successful")
    return conn


def postgresql_to_dataframe(select_query):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    conn = connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    column_names = [desc[0] for desc in cursor.description]
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


def df_from_db(table_name, start_height):
    query = f"SELECT * FROM {table_name} where height >= {start_height} and height < {start_height + 1000}"
    return postgresql_to_dataframe(query)


pkeys = {"miner_sector_infos": ["height", "miner_id", "sector_id", "state_root"]}

for start_height in range(138000, 430000, 1000):
    csv_file = csv_file_for("miner_sector_infos", start_height)
    # if csv_file.is_file():
    #     file_size = csv_file.stat().st_size
    #     print(start_height, humanize.naturalsize(file_size, binary=True))
    # else:
    #     print(start_height, "❌")
    # print(start_height, end=" ")
    print(start_height)

    try:
        csv = df_from_csv("miner_sector_infos", start_height)
        print(f"csv: {len(csv)}")
        db = df_from_db("miner_sector_infos", start_height)
        print(f"db: {len(db)}")
        compare = datacompy.Compare(
            csv,
            db,
            join_columns=pkeys["miner_sector_infos"],
            df1_name="csv",
            df2_name="db",
        )

        if not compare.matches():
            print("❌")
            # print(compare.report())
            # input()
        else:
            print("✓")
    except Exception:
        print("❌")
        pass
