from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/")
def get_recommendations():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            mine_id,
            recommendation_date,
            recommendation_type,
            action,
            expected_impact,
            priority,
            status
        FROM recommendations
        ORDER BY
            CASE priority
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
                ELSE 4
            END,
            recommendation_date DESC,
            id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    records = []

    for row in rows:
        records.append({
            "id": row[0],
            "mine_id": row[1],
            "recommendation_date": (
                row[2].isoformat()
                if row[2]
                else None
            ),
            "recommendation_type": row[3],
            "action": row[4],
            "expected_impact": row[5],
            "priority": row[6],
            "status": row[7]
        })

    return {
        "status": "ok",
        "records": records
    }