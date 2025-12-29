import pytest
from ingestion.transform import transform_alt_csv_record


def test_schema_mismatch_missing_field():
    bad_record = {
        "symbol": "BTC",
        # "price" missing
        "timestamp": "01-01-2024 10:05"
    }

    with pytest.raises(KeyError):
        transform_alt_csv_record(bad_record)
