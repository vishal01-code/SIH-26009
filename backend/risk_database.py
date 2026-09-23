import os
import psycopg2
from datetime import date

print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.7 - PostgreSQL Risk Analysis")
print("===================================")

# Risk information
mine_id = 1
risk_score = 40
risk_level = "MEDIUM"

risk_type = "Production Shortfall"

primary_cause = "Equipment Downtime"

description = (
    "Production risk detected due to equipment downtime, "
    "blasting delay, and rainfall."
)

# Recommendations
recommendations = [
    {
        "type": "Equipment",
        "action": "Inspect and maintain high-downtime equipment",
        "impact": 10,
        "priority": "HIGH",
        "status": "Pending"
    },
    {
        "type": "Blasting",
        "action": "Optimize blasting schedule to reduce delays",
        "impact": 8,
        "priority": "MEDIUM",
        "status": "Pending"
    },
    {
        "type": "Weather",
        "action": "Adjust mine operations according to weather conditions",
        "impact": 7,
        "priority": "MEDIUM",
        "status": "Pending"
    }
]

# PostgreSQL connection
connection = psycopg2.connect(
    host="127.0.0.1",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345"
)

cursor = connection.cursor()

print()
print("Connected to PostgreSQL Successfully!")

# Save risk assessment
risk_query = """
INSERT INTO risk_assessments
(
    mine_id,
    assessment_date,
    risk_type,
    risk_level,
    risk_score,
    primary_cause,
    description
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING id;
"""

cursor.execute(
    risk_query,
    (
        mine_id,
        date.today(),
        risk_type,
        risk_level,
        risk_score,
        primary_cause,
        description
    )
)

risk_id = cursor.fetchone()[0]

print("Risk Assessment Saved!")
print("Risk Assessment ID:", risk_id)

# Save recommendations
recommendation_query = """
INSERT INTO recommendations
(
    mine_id,
    recommendation_date,
    recommendation_type,
    action,
    expected_impact,
    priority,
    status
)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

for recommendation in recommendations:

    cursor.execute(
        recommendation_query,
        (
            mine_id,
            date.today(),
            recommendation["type"],
            recommendation["action"],
            recommendation["impact"],
            recommendation["priority"],
            recommendation["status"]
        )
    )

print("Recommendations Saved Successfully!")

# Commit changes
connection.commit()

cursor.close()
connection.close()

print()
print("===================================")
print("DATABASE SAVE COMPLETED")
print("===================================")

print("Risk Score:", risk_score, "/ 100")
print("Risk Level:", risk_level)
print("Primary Cause:", primary_cause)
print("Recommendations Saved:", len(recommendations))

print()
print("===================================")
print("Step 6.7 Completed Successfully")
print("===================================")