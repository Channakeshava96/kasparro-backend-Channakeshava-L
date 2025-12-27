from core.database import SessionLocal
from core.models import RawAPIData, RawCSVData, NormalizedPrice, ETLRun
from ingestion.api_ingestion import fetch_coinpaprika_data
from ingestion.csv_ingestion import read_csv_data
from ingestion.transform import transform_api_record, transform_csv_record
from datetime import datetime, UTC
from ingestion.csv_alt_ingestion import read_alt_csv_data
from ingestion.transform import transform_alt_csv_record


def run_etl():
    db = SessionLocal()
    etl_run = ETLRun(status="RUNNING")

    try:
        db.add(etl_run)
        db.commit()

        # --- API INGESTION ---
        api_data = fetch_coinpaprika_data()

        for record in api_data[:5]:  # limit for now
            db.add(RawAPIData(
                source="coinpaprika",
                raw_payload=record
            ))

            normalized = transform_api_record(record)
            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))

        # --- CSV INGESTION ---
        csv_rows = read_csv_data()

        for row in csv_rows:
            db.add(RawCSVData(
                source="csv",
                raw_payload=row
            ))

            normalized = transform_csv_record(row)
            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))
        # --- ALT CSV INGESTION ---
        alt_csv_rows = read_alt_csv_data()

        for row in alt_csv_rows:
            db.add(RawCSVData(
                source="csv_alt",
                raw_payload=row
            ))

            normalized = transform_alt_csv_record(row)

            if not db.query(NormalizedPrice).filter_by(
                coin=normalized.coin,
                source=normalized.source,
                timestamp=normalized.timestamp
            ).first():
                db.add(NormalizedPrice(**normalized.model_dump()))


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
