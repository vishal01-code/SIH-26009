from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/risk")
def get_equipment_risk():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT ON (e.id)
            e.id,
            e.equipment_code,
            e.equipment_type,
            e.model,
            e.status,
            ep.record_date,
            ep.operating_hours,
            ep.downtime_hours,
            ep.utilization_percent,
            ep.performance_score
        FROM equipment e
        JOIN equipment_performance ep
            ON e.id = ep.equipment_id
        ORDER BY e.id, ep.record_date DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    records = []

    for row in rows:

        performance_score = row[9]

        if performance_score >= 85:
            risk_level = "LOW"
        elif performance_score >= 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        records.append({
            "id": row[0],
            "equipment_code": row[1],
            "equipment_type": row[2],
            "model": row[3],
            "status": row[4],
            "record_date": row[5].isoformat(),
            "operating_hours": row[6],
            "downtime_hours": row[7],
            "utilization_percent": row[8],
            "performance_score": performance_score,
            "risk_level": risk_level
        })

    return {
        "status": "ok",
        "records": records
    }