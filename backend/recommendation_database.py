
# ============================================
# SIH 26009 - Recommendation Database
# Phase 9.7
# ============================================

import psycopg2

from recommendation_engine import generate_recommendation


# ============================================
# 1. Database Configuration
# ============================================

DB_CONFIG = {

    "host": "localhost",

    "database": "sih_26009",

    "user": "postgres",

    "password": "Postgres@12345",

    "port": "5432"

}


# ============================================
# 2. Generate Recommendations
# ============================================

result = generate_recommendation(

    risk_score=40,

    shortfall=3.89,

    downtime_hours=2.5,

    blasting_delay_hours=1.2,

    rainfall=12,

    equipment_performance=78,

    equipment_utilization=84

)


# ============================================
# 3. Connect to PostgreSQL
# ============================================

try:

    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()

    print("\nDatabase connected successfully!")


    # ========================================
    # 4. Insert Recommendations
    # ========================================

    inserted_count = 0


    for recommendation in result["recommendations"]:

        query = """
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
        VALUES
        (
            %s,
            CURRENT_DATE,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (

            1,

            recommendation["type"],

            recommendation["action"],

            recommendation["expected_impact"],

            recommendation["priority"],

            "Pending"

        )


        cursor.execute(
            query,
            values
        )


        inserted_count += 1


    # ========================================
    # 5. Save Changes
    # ========================================

    connection.commit()


    print(
        f"{inserted_count} recommendations inserted successfully!"
    )


# ============================================
# 6. Error Handling
# ============================================

except Exception as error:

    print("\nDatabase Error:")

    print(error)


# ============================================
# 7. Close Database
# ============================================

finally:

    if "cursor" in locals():

        cursor.close()


    if "connection" in locals():

        connection.close()


    print("Database connection closed.")

