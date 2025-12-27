from fastapi import APIRouter, Query
from core.database import SessionLocal
from core.models import NormalizedPrice
from sqlalchemy.orm import Session

router = APIRouter(prefix="/data", tags=["data"])


@router.get("")
def get_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    coin: str | None = None,
    source: str | None = None,
):
    db: Session = SessionLocal()

    try:
        query = db.query(NormalizedPrice)

        if coin:
            query = query.filter(NormalizedPrice.coin == coin)

        if source:
            query = query.filter(NormalizedPrice.source == source)

        total = query.count()

        results = (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        data = [
            {
                "coin": r.coin,
                "price_usd": r.price_usd,
                "volume_24h": r.volume_24h,
                "source": r.source,
                "timestamp": r.timestamp,
            }
            for r in results
        ]

        return {
            "page": page,
            "page_size": page_size,
            "total_records": total,
            "data": data,
        }

    finally:
        db.close()
