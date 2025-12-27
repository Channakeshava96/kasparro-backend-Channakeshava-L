from core.database import SessionLocal
from core.models import RawAPIData, RawCSVData, NormalizedPrice, ETLRun
from ingestion.api_ingestion import fetch_coinpaprika_data
from ingestion.csv_ingestion import read_csv_data
from ingestion.transform import transform_api_record, transform_csv_record
from datetime import datetime, UTC
from ingestion.csv_alt_ingestion import read_alt_csv_data
from ingestion.transform import transform_alt_csv_record
from services.checkpoint_service import get_checkpoint, update_checkpoint


def run_etl():
    db = SessionLocal()
    etl_run = ETLRun(status="RUNNING")

    try:
        db.add(etl_run)
        db.commit()

        # --- API INGESTION ---
        api_checkpoint = get_checkpoint(db, "coinpaprika")
        last_api_ts = api_checkpoint.last_processed_at if api_checkpoint else None

        api_data = fetch_coinpaprika_data()

        latest_ts = last_api_ts

        for record in api_data[:5]:  # limit for now
            normalized = transform_api_record(record)

            if last_api_ts and normalized.timestamp <= last_api_ts:
                continue

            db.add(RawAPIData(
                source="coinpaprika",
                raw_payload=record
            ))

            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))

            if not latest_ts or normalized.timestamp > latest_ts:
                latest_ts = normalized.timestamp

        if latest_ts and (not last_api_ts or latest_ts > last_api_ts):
            update_checkpoint(db, "coinpaprika", latest_ts)

        # --- CSV INGESTION ---
        csv_checkpoint = get_checkpoint(db, "csv")
        last_csv_ts = csv_checkpoint.last_processed_at if csv_checkpoint else None

        csv_rows = read_csv_data()

        latest_csv_ts = last_csv_ts

        for row in csv_rows:
            normalized = transform_csv_record(row)

            if last_csv_ts and normalized.timestamp <= last_csv_ts:
                continue

            db.add(RawCSVData(
                source="csv",
                raw_payload=row
            ))

            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))

            if not latest_csv_ts or normalized.timestamp > latest_csv_ts:
                latest_csv_ts = normalized.timestamp

        if latest_csv_ts and (not last_csv_ts or latest_csv_ts > last_csv_ts):
            update_checkpoint(db, "csv", latest_csv_ts)
        # --- ALT CSV INGESTION ---
        alt_csv_checkpoint = get_checkpoint(db, "csv_alt")
        last_alt_csv_ts = alt_csv_checkpoint.last_processed_at if alt_csv_checkpoint else None

        alt_csv_rows = read_alt_csv_data()

        latest_alt_csv_ts = last_alt_csv_ts

        for row in alt_csv_rows:
            normalized = transform_alt_csv_record(row)

            if last_alt_csv_ts and normalized.timestamp <= last_alt_csv_ts:
                continue

            db.add(RawCSVData(
                source="csv_alt",
                raw_payload=row
            ))

            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))

            if not latest_alt_csv_ts or normalized.timestamp > latest_alt_csv_ts:
                latest_alt_csv_ts = normalized.timestamp

        if latest_alt_csv_ts and (not last_alt_csv_ts or latest_alt_csv_ts > last_alt_csv_ts):
            update_checkpoint(db, "csv_alt", latest_alt_csv_ts)


        etl_run.status = "SUCCESS"
        etl_run.records_processed = len(api_data[:5]) + len(csv_rows) + len(alt_csv_rows)
        etl_run.finished_at = datetime.now(UTC)

        db.commit()

        print("✅ ETL run completed successfully")

    except Exception as e:
        db.rollback()
        etl_run.status = "FAILURE"
        etl_run.error_message = str(e)
        etl_run.finished_at = datetime.now(UTC)
        db.commit()
        print("❌ ETL failed:", e)

    finally:
        db.close()

if __name__ == "__main__":
    run_etl()
