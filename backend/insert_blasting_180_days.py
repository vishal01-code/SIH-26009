import pandas as pd
import psycopg2
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.8 - Insert Blasting Data")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "raw",
    "blasting_data_180_days.csv"
)

data = pd.read_csv(input_file)

print()
print("Blasting CSV Dataset Loaded Successfully!")
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

# Remove old demo records
cursor.execute(
    "DELETE FROM blasting_records;"
)

print()
print("Old Blasting Records Removed!")

insert_query = """
INSERT INTO blasting_records
(
    mine_id,
    blast_date,
    planned_delay_hours,
    actual_delay_hours,
    blast_count,
    status
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
            int(row["mine_id"]),
            row["blast_date"],
            float(row["planned_delay_hours"]),
            float(row["actual_delay_hours"]),
            int(row["blast_count"]),
            row["status"]
        )
    )

connection.commit()

print()
print("180 Blasting Records Inserted Successfully!")

cursor.close()
connection.close()

print()
print("PostgreSQL Connection Closed!")

print()
print("===================================")
print("Step 5.6.8 Completed Successfully")
print("===================================")