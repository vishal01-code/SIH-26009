import pandas as pd
import psycopg2
import os


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.2 - Insert 180-Day Data")
print("===================================")


# Project root
project_root = os.path.dirname(
    os.path.dirname(__file__)
)


# CSV file location
input_file = os.path.join(
    project_root,
    "data",
    "raw",
    "production_data_180_days.csv"
)


# CSV load
data = pd.read_csv(input_file)


print()
print("CSV Dataset Loaded Successfully!")

print()
print("Rows:", len(data))

print("Columns:", len(data.columns))


# PostgreSQL connection
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


# Insert query
insert_query = """
INSERT INTO production_records
(
    mine_id,
    production_date,
    planned_production,
    actual_production,
    operating_hours,
    downtime_hours,
    blasting_delay_hours
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s
);
"""


# Insert records
for _, row in data.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["mine_id"]),
            row["production_date"],
            float(row["planned_production"]),
            float(row["actual_production"]),
            float(row["operating_hours"]),
            float(row["downtime_hours"]),
            float(row["blasting_delay_hours"])
        )
    )


# Save changes
connection.commit()


print()
print("180 Production Records Inserted Successfully!")


# Close connection
cursor.close()

connection.close()


print()
print("PostgreSQL Connection Closed!")


print()
print("===================================")
print("Step 5.6.2 Completed Successfully")
print("===================================")