import pendulum
from helpers import get_start_end_epocs, date_to_epoc
import os
import pendulum


def test_epocs():
    os.environ["AIRFLOW_INTERVAL"] = "DAILY"
    os.environ["AIRFLOW_TS"] = "2021-06-16T08:30:00+00:00"
    start, end = get_start_end_epocs()
    assert (end - start) / (2 * 60) == 24
    assert start == date_to_epoc(pendulum.parse("2021-06-16"))
    assert end == date_to_epoc(pendulum.parse("2021-06-17"))
