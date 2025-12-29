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
    records_processed = 0
    processed_in_run = set()

    try:
        db.add(etl_run)
        db.commit()

        # Data sources and their processing functions
        sources = {
            "coinpaprika": (fetch_coinpaprika_data, transform_api_record, RawAPIData),
            "csv": (read_csv_data, transform_csv_record, RawCSVData),
            "csv_alt": (read_alt_csv_data, transform_alt_csv_record, RawCSVData),
        }

        for source_name, (fetch_func, transform_func, raw_model) in sources.items():
            checkpoint = get_checkpoint(db, source_name)
            last_ts = checkpoint.last_processed_at if checkpoint else None
            latest_ts = last_ts

            for record in fetch_func():
                normalized = transform_func(record)

                if last_ts and normalized.timestamp <= last_ts:
                    continue

                db.add(raw_model(source=source_name, raw_payload=record))

                record_key = (normalized.coin, normalized.source, normalized.timestamp)
                if record_key in processed_in_run:
                    continue

                if not db.query(NormalizedPrice).filter_by(
                    coin=normalized.coin,
                    source=normalized.source,
                    timestamp=normalized.timestamp
                ).first():
                    db.add(NormalizedPrice(**normalized.model_dump()))
                    records_processed += 1
                    processed_in_run.add(record_key)

                if not latest_ts or normalized.timestamp > latest_ts:
                    latest_ts = normalized.timestamp

            if latest_ts and (not last_ts or latest_ts > last_ts):
                update_checkpoint(db, source_name, latest_ts)

        etl_run.status = "SUCCESS"
        etl_run.records_processed = records_processed
        etl_run.finished_at = datetime.now(UTC)

        db.commit()

        print(f"✅ ETL run completed successfully. {records_processed} records processed.")

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
