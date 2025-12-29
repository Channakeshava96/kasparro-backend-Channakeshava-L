from fastapi import APIRouter
from sqlalchemy import text
from core.database import engine

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_stats():
    stats = {
        "last_run": None,
        "last_success": None,
        "last_failure": None,
        "recent_runs": [],
        "checkpoints": []
    }

    with engine.connect() as conn:
        # Last run
        last_run = conn.execute(
            text("""
            SELECT status, records_processed, started_at, finished_at, error_message
            FROM etl_runs
            ORDER BY id DESC
            LIMIT 1
            """)
        ).fetchone()

        if last_run:
            stats["last_run"] = {
                "status": last_run[0],
                "records_processed": last_run[1],
                "started_at": last_run[2],
                "finished_at": last_run[3],
                "error_message": last_run[4],
            }

        # Last success
        last_success = conn.execute(
            text("""
            SELECT finished_at
            FROM etl_runs
            WHERE status = 'SUCCESS'
            ORDER BY finished_at DESC
            LIMIT 1
            """)
        ).fetchone()

        if last_success:
            stats["last_success"] = last_success[0]

        # Last failure
        last_failure = conn.execute(
            text("""
            SELECT finished_at
            FROM etl_runs
            WHERE status = 'FAILURE'
            ORDER BY finished_at DESC
            LIMIT 1
            """)
        ).fetchone()

        if last_failure:
            stats["last_failure"] = last_failure[0]

        # Recent runs (last 5)
        recent_runs = conn.execute(
            text("""
            SELECT status, records_processed, started_at, finished_at
            FROM etl_runs
            ORDER BY id DESC
            LIMIT 5
            """)
        ).fetchall()

        stats["recent_runs"] = [
            {
                "status": r[0],
                "records_processed": r[1],
                "started_at": r[2],
                "finished_at": r[3],
            }
            for r in recent_runs
        ]

        # Checkpoints
        checkpoints = conn.execute(
            text("""
            SELECT source, last_processed_at
            FROM etl_checkpoints
            """)
        ).fetchall()

        stats["checkpoints"] = [
            {
                "source": c[0],
                "last_processed_at": c[1],
            }
            for c in checkpoints
        ]

    return stats
