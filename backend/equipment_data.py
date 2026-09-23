import pandas as pd
import psycopg2
import os

# PostgreSQL Database Connection
connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)


# Equipment Performance Data
query = """
SELECT
    equipment_id,
    record_date,
    operating_hours,
    downtime_hours,
    utilization_percent,
    performance_score
FROM equipment_performance
ORDER BY record_date, equipment_id;
"""


# Database से data Python में load करना
equipment_data = pd.read_sql_query(
    query,
    connection
)


connection.close()


print("Equipment Performance Data:")
print()
print(equipment_data)

print()
print("Rows:", len(equipment_data))
print("Columns:", len(equipment_data.columns))

# Date को datetime format में convert करना
equipment_data["record_date"] = pd.to_datetime(
    equipment_data["record_date"]
)


# हर दिन का Equipment Performance aggregate करना
daily_equipment = (
    equipment_data
    .groupby("record_date")
    .agg(
        total_operating_hours=("operating_hours", "sum"),
        total_downtime_hours=("downtime_hours", "sum"),
        average_utilization=("utilization_percent", "mean"),
        average_performance_score=("performance_score", "mean")
    )
    .reset_index()
)


print()
print("Daily Equipment Summary:")
print(daily_equipment)


# Production + Weather Integrated Dataset load करना
project_root = os.path.dirname(os.path.dirname(__file__))

integrated_file = os.path.join(
    project_root,
    "data",
    "processed",
    "integrated_production_weather.csv"
)

integrated_data = pd.read_csv(integrated_file)


# Date को datetime format में convert करना
integrated_data["production_date"] = pd.to_datetime(
    integrated_data["production_date"]
)


# Equipment Summary की date भी datetime format में
daily_equipment["record_date"] = pd.to_datetime(
    daily_equipment["record_date"]
)


# Production + Weather और Equipment Data को merge करना
final_integrated_data = pd.merge(
    integrated_data,
    daily_equipment,
    left_on="production_date",
    right_on="record_date",
    how="inner"
)


print()
print("Final Integrated Dataset:")
print(final_integrated_data)

print()
print("Rows:", len(final_integrated_data))
print("Columns:", len(final_integrated_data.columns))

# Processed folder का path
project_root = os.path.dirname(os.path.dirname(__file__))

processed_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(processed_folder, exist_ok=True)


# Final integrated dataset का output path
output_file = os.path.join(
    processed_folder,
    "final_integrated_dataset.csv"
)


# Final dataset को CSV में save करना
final_integrated_data.to_csv(
    output_file,
    index=False
)


print()
print("Final Integrated Dataset saved successfully!")
print("File:", output_file)