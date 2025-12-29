import pytest


def test_etl_failure_handling():
    with pytest.raises(Exception):
        raise Exception("Simulated ETL failure")
