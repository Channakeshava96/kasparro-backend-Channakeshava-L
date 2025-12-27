from sqlalchemy.orm import Session
from core.models import ETLCheckpoint
from datetime import datetime


def get_checkpoint(db: Session, source: str):
    return db.query(ETLCheckpoint).filter_by(source=source).first()


def update_checkpoint(db: Session, source: str, timestamp: datetime):
    checkpoint = get_checkpoint(db, source)

    if checkpoint:
        checkpoint.last_processed_at = timestamp
    else:
        checkpoint = ETLCheckpoint(
            source=source,
            last_processed_at=timestamp
        )
        db.add(checkpoint)

    db.commit()
