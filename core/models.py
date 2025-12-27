from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    func,
    UniqueConstraint
)

from core.database import Base


# -------------------------
# RAW API DATA
# -------------------------
class RawAPIData(Base):
    __tablename__ = "raw_api_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    raw_payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())


# -------------------------
# RAW CSV DATA
# -------------------------
class RawCSVData(Base):
    __tablename__ = "raw_csv_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    raw_payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())


# -------------------------
# NORMALIZED DATA
# -------------------------
class NormalizedPrice(Base):
    __tablename__ = "normalized_prices"

    id = Column(Integer, primary_key=True, index=True)
    coin = Column(String, nullable=False)
    price_usd = Column(Float, nullable=False)
    volume_24h = Column(Float, nullable=True)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "coin", "source", "timestamp",
            name="uq_coin_source_timestamp"
        ),
    )

# -------------------------
# ETL RUN METADATA
# -------------------------
class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)  # SUCCESS / FAILURE
    records_processed = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)
class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False, unique=True)
    last_processed_at = Column(DateTime(timezone=True), nullable=True)

