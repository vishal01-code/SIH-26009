from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/potential")
def get_reserve_potential():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            mine_id,
            sample_code,
            prediction_date,
            geological_potential_score,
            environmental_context_score,
            integrated_potential_score,
            potential_class,
            latitude,
            longitude,
            model_version
        FROM reserve_potential_predictions
        ORDER BY integrated_potential_score DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    records = []

    for row in rows:
        records.append({
            "id": row[0],
            "mine_id": row[1],
            "sample_code": row[2],
            "prediction_date": row[3].isoformat(),
            "geological_potential_score": row[4],
            "environmental_context_score": row[5],
            "integrated_potential_score": row[6],
            "potential_class": row[7],
            "latitude": row[8],
            "longitude": row[9],
            "model_version": row[10]
        })

    return {
        "status": "ok",
        "records": records
    }