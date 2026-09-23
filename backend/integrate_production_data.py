import pandas as pd
import psycopg2
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.9 - Data Integration")
print("===================================")

# -----------------------------------
# PostgreSQL Connection
# -----------------------------------

connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)

print()
print("PostgreSQL Connection Successful!")

# -----------------------------------
# 1. Production Data
# -----------------------------------

production_query = """
SELECT
    mine_id,
    production_date,
    planned_production,
    actual_production,
    operating_hours,
    downtime_hours,
    blasting_delay_hours
FROM production_records
ORDER BY production_date;
"""

production = pd.read_sql_query(
    production_query,
    connection
)

print()
print("Production Data:", production.shape)

# -----------------------------------
# 2. Weather Data
# -----------------------------------

weather_query = """
SELECT
    mine_id,
    observation_date,
    rainfall_mm,
    soil_moisture,
    land_temperature,
    humidity
FROM weather_data
ORDER BY observation_date;
"""

weather = pd.read_sql_query(
    weather_query,
    connection
)

print("Weather Data:", weather.shape)

# -----------------------------------
# 3. Equipment Performance
# -----------------------------------

equipment_query = """
SELECT
    equipment_id,
    record_date,
    operating_hours,
    downtime_hours,
    utilization_percent,
    performance_score
FROM equipment_performance
ORDER BY record_date;
"""

equipment = pd.read_sql_query(
    equipment_query,
    connection
)

print("Equipment Data:", equipment.shape)

# -----------------------------------
# 4. Aggregate Equipment by Date
# -----------------------------------

equipment_daily = (
    equipment
    .groupby("record_date")
    .agg(
        equipment_operating_hours=(
            "operating_hours",
            "mean"
        ),
        equipment_downtime_hours=(
            "downtime_hours",
            "sum"
        ),
        average_utilization=(
            "utilization_percent",
            "mean"
        ),
        average_performance_score=(
            "performance_score",
            "mean"
        )
    )
    .reset_index()
)

print(
    "Daily Equipment Data:",
    equipment_daily.shape
)

# -----------------------------------
# 5. Blasting Data
# -----------------------------------

blasting_query = """
SELECT
    mine_id,
    blast_date,
    planned_delay_hours,
    actual_delay_hours,
    blast_count,
    status
FROM blasting_records
ORDER BY blast_date;
"""

blasting = pd.read_sql_query(
    blasting_query,
    connection
)

print("Blasting Data:", blasting.shape)

# -----------------------------------
# 6. Rename Date Columns
# -----------------------------------

production["production_date"] = pd.to_datetime(
    production["production_date"]
)

weather["observation_date"] = pd.to_datetime(
    weather["observation_date"]
)

equipment_daily["record_date"] = pd.to_datetime(
    equipment_daily["record_date"]
)

blasting["blast_date"] = pd.to_datetime(
    blasting["blast_date"]
)

# -----------------------------------
# 7. Merge Production + Weather
# -----------------------------------

integrated = pd.merge(
    production,
    weather,
    left_on=["mine_id", "production_date"],
    right_on=["mine_id", "observation_date"],
    how="left"
)

# Remove duplicate date column
integrated = integrated.drop(
    columns=["observation_date"]
)

print()
print(
    "After Production + Weather:",
    integrated.shape
)

# -----------------------------------
# 8. Merge Equipment
# -----------------------------------

integrated = pd.merge(
    integrated,
    equipment_daily,
    left_on="production_date",
    right_on="record_date",
    how="left"
)

integrated = integrated.drop(
    columns=["record_date"]
)

print(
    "After Equipment Integration:",
    integrated.shape
)

# -----------------------------------
# 9. Merge Blasting
# -----------------------------------

integrated = pd.merge(
    integrated,
    blasting,
    left_on=["mine_id", "production_date"],
    right_on=["mine_id", "blast_date"],
    how="left"
)

integrated = integrated.drop(
    columns=["blast_date"]
)

print(
    "After Blasting Integration:",
    integrated.shape
)

# -----------------------------------
# 10. Missing Value Check
# -----------------------------------

print()
print("Missing Values:")
print(
    integrated.isnull().sum()
)

# -----------------------------------
# 11. Save Integrated Dataset
# -----------------------------------

project_root = os.path.dirname(
    os.path.dirname(__file__)
)

output_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = os.path.join(
    output_folder,
    "production_master_180_days.csv"
)

integrated.to_csv(
    output_file,
    index=False
)

# -----------------------------------
# 12. Final Information
# -----------------------------------

print()
print("===================================")
print("MASTER DATASET CREATED")
print("===================================")

print()
print("Rows:", len(integrated))
print("Columns:", len(integrated.columns))

print()
print("Columns:")
for column in integrated.columns:
    print("-", column)

print()
print("Output File:")
print(output_file)

connection.close()

print()
print("PostgreSQL Connection Closed!")

print()
print("===================================")
print("Step 5.6.9 Completed Successfully")
print("===================================")