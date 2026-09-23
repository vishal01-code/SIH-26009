from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/")
def get_production():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            mine_id,
            production_date,
            planned_production,
            actual_production,
            operating_hours,
            downtime_hours,
            blasting_delay_hours
        FROM production_records
        ORDER BY production_date DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    records = []

    for row in rows:
        records.append({
            "id": row[0],
            "mine_id": row[1],
            "production_date": row[2].isoformat(),
            "planned_production": row[3],
            "actual_production": row[4],
            "operating_hours": row[5],
            "downtime_hours": row[6],
            "blasting_delay_hours": row[7]
        })

    return {
        "status": "ok",
        "records": records
    }