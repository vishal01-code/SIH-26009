
from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/what-if")
def what_if_simulation(downtime_reduction: float = 30):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            planned_production,
            actual_production,
            downtime_hours
        FROM production_records
        ORDER BY production_date DESC, id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return {
            "status": "error",
            "message": "No production record found."
        }

    planned_production = float(row[0])
    actual_production = float(row[1])
    downtime_hours = float(row[2])

    # Reduction must stay between 0 and 100
    downtime_reduction = max(
        0,
        min(downtime_reduction, 100)
    )

    # Calculate new downtime
    new_downtime = downtime_hours * (
        1 - downtime_reduction / 100
    )

    # Estimate recovered production
    recovered_production = (
        downtime_hours - new_downtime
    ) * 10

    # Calculate new production
    new_production = min(
        actual_production + recovered_production,
        planned_production
    )

    # Calculate remaining shortfall
    remaining_shortfall = max(
        planned_production - new_production,
        0
    )

    return {
        "status": "ok",
        "downtime_reduction_percent": downtime_reduction,
        "original_downtime_hours": round(
            downtime_hours, 2
        ),
        "new_downtime_hours": round(
            new_downtime, 2
        ),
        "original_production": round(
            actual_production, 2
        ),
        "new_production": round(
            new_production, 2
        ),
        "planned_production": round(
            planned_production, 2
        ),
        "remaining_shortfall": round(
            remaining_shortfall, 2
        )
    }

