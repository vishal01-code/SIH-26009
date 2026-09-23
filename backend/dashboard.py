from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()


@router.get("/summary")
def dashboard_summary():

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Latest production prediction
    cursor.execute("""
        SELECT predicted_value
        FROM predictions
        WHERE prediction_type = 'Production'
        ORDER BY prediction_date DESC, id DESC
        LIMIT 1
    """)

    prediction_row = cursor.fetchone()

    predicted_production = (
        prediction_row[0]
        if prediction_row
        else None
    )

    # 2. Latest risk assessment
    cursor.execute("""
        SELECT
            risk_level,
            risk_score,
            primary_cause
        FROM risk_assessments
        ORDER BY assessment_date DESC, id DESC
        LIMIT 1
    """)

    risk_row = cursor.fetchone()

    if risk_row:
        risk_level = risk_row[0]
        risk_score = risk_row[1]
        primary_cause = risk_row[2]
    else:
        risk_level = None
        risk_score = None
        primary_cause = None

    # 3. Count high-potential reserve zones
    cursor.execute("""
        SELECT COUNT(*)
        FROM reserve_potential_predictions
        WHERE potential_class = 'HIGH'
    """)

    high_potential_zones = cursor.fetchone()[0]

    # Close database connection
    cursor.close()
    conn.close()

    # Return dashboard summary
    return {
        "status": "ok",
        "predicted_production": predicted_production,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "primary_cause": primary_cause,
        "high_potential_zones": high_potential_zones
    }