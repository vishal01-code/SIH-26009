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

# Production Data
production_query = """
SELECT
    production_date,
    mine_id,
    planned_production,
    actual_production,
    operating_hours,
    downtime_hours,
    blasting_delay_hours
FROM production_records
ORDER BY production_date;
"""

production_data = pd.read_sql_query(
    production_query,
    connection
)


# Weather Data
weather_query = """
SELECT
    observation_date,
    mine_id,
    rainfall_mm,
    soil_moisture,
    land_temperature,
    humidity
FROM weather_data
ORDER BY observation_date;
"""

weather_data = pd.read_sql_query(
    weather_query,
    connection
)


connection.close()


print("Production Data:")
print(production_data)

print()
print("Weather Data:")
print(weather_data)

# Date columns को datetime format में convert करना
production_data["production_date"] = pd.to_datetime(
    production_data["production_date"]
)

weather_data["observation_date"] = pd.to_datetime(
    weather_data["observation_date"]
)


# Production और Weather Data को merge करना
integrated_data = pd.merge(
    production_data,
    weather_data,
    left_on=["production_date", "mine_id"],
    right_on=["observation_date", "mine_id"],
    how="inner"
)


print()
print("Integrated Data:")
print(integrated_data)

# Processed folder का path
project_root = os.path.dirname(os.path.dirname(__file__))

processed_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(processed_folder, exist_ok=True)


# Integrated dataset का output path
output_file = os.path.join(
    processed_folder,
    "integrated_production_weather.csv"
)


# Dataset save करना
integrated_data.to_csv(
    output_file,
    index=False
)

print()
print("Integrated dataset saved successfully!")
print("File:", output_file)