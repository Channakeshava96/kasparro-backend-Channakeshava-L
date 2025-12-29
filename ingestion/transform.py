from schemas.price import NormalizedPriceSchema
from datetime import datetime, UTC

def transform_api_record(record: dict):
    return NormalizedPriceSchema(
        coin=record["symbol"],
        price_usd=record["quotes"]["USD"]["price"],
        volume_24h=record["quotes"]["USD"].get("volume_24h"),
        source="coinpaprika",
        timestamp=datetime.fromisoformat(record["last_updated"]).replace(tzinfo=UTC) 
    )

def transform_csv_record(record: dict):
    return NormalizedPriceSchema(
        coin=record["coin"],
        price_usd=float(record["price_usd"]),
        volume_24h=float(record["volume_24h"]),
        source="csv",
        timestamp=datetime.fromisoformat(record["timestamp"]).replace(tzinfo=UTC)
    )
def transform_alt_csv_record(record: dict):
    return NormalizedPriceSchema(
        coin=record["symbol"],
        price_usd=float(record["price"]),
        volume_24h=None,  # missing in this source
        source="csv_alt",
        timestamp=datetime.strptime(
            record["timestamp"],
            "%d-%m-%Y %H:%M"
        ).replace(tzinfo=UTC)
    )