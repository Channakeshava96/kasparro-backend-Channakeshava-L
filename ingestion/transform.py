from schemas.price import NormalizedPriceSchema
from datetime import datetime, UTC

def transform_api_record(record: dict):
    return NormalizedPriceSchema(
        coin=record["symbol"],
        price_usd=record["quotes"]["USD"]["price"],
        volume_24h=record["quotes"]["USD"].get("volume_24h"),
        source="coinpaprika",
        timestamp=datetime.fromisoformat(record["last_updated"]) 
    )

def transform_csv_record(record: dict):
    return NormalizedPriceSchema(
        coin=record["coin"],
        price_usd=float(record["price_usd"]),
        volume_24h=float(record["volume_24h"]),
        source="csv",
        timestamp=datetime.fromisoformat(record["timestamp"])
    )
