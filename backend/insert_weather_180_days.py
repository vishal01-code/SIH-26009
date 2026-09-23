import pandas as pd
import psycopg2
import os


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.4 - Insert 180-Day Weather Data")
print("===================================")


project_root = os.path.dirname(
    os.path.dirname(__file__)
)


input_file = os.path.join(
    project_root,
    "data",
    "raw",
    "weather_data_180_days.csv"
)


data = pd.read_csv(input_file)


print()
print("Weather CSV Dataset Loaded Successfully!")

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


insert_query = """
INSERT INTO weather_data
(
    mine_id,
    observation_date,
    rainfall_mm,
    soil_moisture,
    land_temperature,
    humidity
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
            row["observation_date"],
            float(row["rainfall_mm"]),
            float(row["soil_moisture"]),
            float(row["land_temperature"]),
            float(row["humidity"])
        )
    )


connection.commit()


print()
print("180 Weather Records Inserted Successfully!")


cursor.close()

connection.close()


print()
print("PostgreSQL Connection Closed!")


print()
print("===================================")
print("Step 5.6.4 Completed Successfully")
print("===================================")