import psycopg2
import pandas as pd
import os
from datetime import date


print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.7.3 - Equipment Risk Database Integration")
print("===================================")


# -----------------------------------
# Project Root
# -----------------------------------

project_root = os.path.dirname(os.path.dirname(__file__))


# -----------------------------------
# Input File
# -----------------------------------

input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_risk_reasons.csv"
)


# -----------------------------------
# Load Equipment Risk Data
# -----------------------------------

data = pd.read_csv(input_file)

print()
print("Equipment Risk Data Loaded Successfully!")

print()
print("Total Equipment Records:", len(data))


# -----------------------------------
# Database Connection
# -----------------------------------

try:

    connection = psycopg2.connect(
        host="localhost",
        database="sih_26009",
        user="postgres",
        password="Postgres@12345"
    )

    cursor = connection.cursor()

    print()
    print("Database Connected Successfully!")


    # -----------------------------------
    # Insert Equipment Risk
    # -----------------------------------

    for _, row in data.iterrows():

        equipment_id = int(row["equipment_id"])
        risk_score = float(row["equipment_risk_score"])
        risk_level = row["equipment_risk_level"]
        primary_reason = row["primary_risk_reason"]
        risk_reasons = row["risk_reasons"]

        # Get equipment code
        cursor.execute(
            """
            SELECT equipment_code
            FROM equipment
            WHERE id = %s
            """,
            (equipment_id,)
        )

        equipment_result = cursor.fetchone()

        if equipment_result is None:
            print(
                f"Equipment ID {equipment_id} not found!"
            )
            continue

        equipment_code = equipment_result[0]


        # -----------------------------------
        # Description
        # -----------------------------------

        description = (
            f"Equipment {equipment_code} "
            f"(ID: {equipment_id}) has a "
            f"{risk_level} equipment risk. "
            f"Detected factors: {risk_reasons}."
        )


        # -----------------------------------
        # Insert Risk Assessment
        # -----------------------------------

        cursor.execute(
            """
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
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                1,
                date.today(),
                "Equipment Risk",
                risk_level,
                risk_score,
                primary_reason,
                description
            )
        )


        print(
            f"Equipment {equipment_code} "
            f"risk inserted successfully."
        )


    # -----------------------------------
    # Commit Changes
    # -----------------------------------

    connection.commit()

    print()
    print("All Equipment Risk Records Inserted Successfully!")


    # -----------------------------------
    # Close Database
    # -----------------------------------

    cursor.close()
    connection.close()

    print("Database Connection Closed.")


except Exception as error:

    print()
    print("Database Integration Failed!")
    print("Error:", error)


print()
print("===================================")
print("Step 7.7.3 Completed")
print("===================================")