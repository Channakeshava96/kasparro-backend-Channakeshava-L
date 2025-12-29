from ingestion.transform import transform_csv_record
from datetime import datetime, UTC


def test_incremental_ingestion_skip_old_data():
    record = {
        "coin": "BTC",
        "price_usd": "43000",
        "volume_24h": "120000000",
        "timestamp": "2024-01-01T10:00:00"
    }

    normalized = transform_csv_record(record)

    last_checkpoint = datetime.fromisoformat("2024-01-01T10:00:00").replace(tzinfo=UTC)

    # Simulate incremental logic
    assert normalized.timestamp <= last_checkpoint
