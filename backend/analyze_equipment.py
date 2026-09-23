import os
import pandas as pd
import psycopg2

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.1 - Equipment Data Analysis")
print("===================================")

# PostgreSQL connection
conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345"
)

print()
print("Connected to PostgreSQL Successfully!")

# SQL query
query = """
SELECT
    equipment_id,
    operating_hours,
    downtime_hours,
    utilization_percent,
    performance_score
FROM equipment_performance
ORDER BY equipment_id, record_date;
"""

# Load data
data = pd.read_sql(query, conn)

conn.close()

print()
print("Equipment Data Loaded Successfully!")

print("Total Records:", len(data))
print("Total Columns:", len(data.columns))

print()
print("Equipment Data Columns:")
print(data.columns.tolist())

# Equipment performance summary
summary = data.groupby("equipment_id").agg(
    total_operating_hours=("operating_hours", "sum"),
    total_downtime_hours=("downtime_hours", "sum"),
    average_utilization=("utilization_percent", "mean"),
    average_performance=("performance_score", "mean")
).reset_index()

print()
print("===================================")
print("EQUIPMENT PERFORMANCE SUMMARY")
print("===================================")

print(summary)

# Project root
project_root = os.path.dirname(os.path.dirname(__file__))

# Output folder
output_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

# Output file
output_file = os.path.join(
    output_folder,
    "equipment_summary.csv"
)

# Save summary
summary.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Summary Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.1 Completed Successfully")
print("===================================")