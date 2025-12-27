from pydantic import BaseModel
from datetime import datetime

class NormalizedPriceSchema(BaseModel):
    coin: str
    price_usd: float
    volume_24h: float | None
    source: str
    timestamp: datetime
