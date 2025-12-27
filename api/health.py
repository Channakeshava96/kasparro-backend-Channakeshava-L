from fastapi import APIRouter
from core.database import engine
from core.models import ETLRun
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    status = {
        "database": "unknown",
        "last_etl_run": None,
    }

    # Check DB connectivity
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status["database"] = "connected"
    except Exception:
        status["database"] = "disconnected"

    # Check last ETL run
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT status, finished_at
                FROM etl_runs
                ORDER BY id DESC
                LIMIT 1
                """)
            ).fetchone()

            if result:
                status["last_etl_run"] = {
                    "status": result[0],
                    "finished_at": result[1],
                }
    except Exception:
        pass

    return status
