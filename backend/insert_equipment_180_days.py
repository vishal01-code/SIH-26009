import pandas as pd
import psycopg2
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.6 - Insert Equipment Data")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "raw",
    "equipment_performance_180_days.csv"
)

data = pd.read_csv(input_file)

print()
print("Equipment CSV Dataset Loaded Successfully!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))

connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)

cursor = connection.cursor()

print()
print("PostgreSQL Connection Successful!")

# Remove old demo equipment-performance records
cursor.execute(
    "DELETE FROM equipment_performance;"
)

print()
print("Old Equipment Performance Records Removed!")

insert_query = """
INSERT INTO equipment_performance
(
    equipment_id,
    record_date,
    operating_hours,
    downtime_hours,
    utilization_percent,
    performance_score
)
VALUES
(
    %s, %s, %s, %s, %s, %s
);
"""

for _, row in data.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["equipment_id"]),
            row["record_date"],
            float(row["operating_hours"]),
            float(row["downtime_hours"]),
            float(row["utilization_percent"]),
            float(row["performance_score"])
        )
    )

connection.commit()

print()
print("900 Equipment Performance Records Inserted Successfully!")

cursor.close()
connection.close()

print()
print("PostgreSQL Connection Closed!")

print()
print("===================================")
print("Step 5.6.6 Completed Successfully")
print("===================================")