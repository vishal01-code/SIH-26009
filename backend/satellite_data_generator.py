import pandas as pd
import psycopg2
import random
from datetime import timedelta


# ==========================================
# 1. PostgreSQL से Geological Locations पढ़ना
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345"
)

query = """
SELECT
    id,
    mine_id,
    sample_date,
    latitude,
    longitude
FROM geological_samples
ORDER BY id;
"""

geological_data = pd.read_sql(query, connection)


# ==========================================
# 2. Synthetic Satellite Data Generate करना
# ==========================================

satellite_records = []

for _, row in geological_data.iterrows():

    ndvi = round(random.uniform(0.20, 0.75), 2)

    land_temperature = round(
        random.uniform(28.0, 42.0), 2
    )

    soil_moisture = round(
        random.uniform(0.20, 0.80), 2
    )

    cloud_cover = round(
        random.uniform(5.0, 90.0), 2
    )

    satellite_records.append({
        "mine_id": int(row["mine_id"]),
        "observation_date": row["sample_date"],
        "ndvi": ndvi,
        "land_surface_temperature": land_temperature,
        "soil_moisture": soil_moisture,
        "cloud_cover": cloud_cover,
        "latitude": row["latitude"],
        "longitude": row["longitude"]
    })


satellite_data = pd.DataFrame(satellite_records)


# ==========================================
# 3. Satellite Data PostgreSQL में Insert करना
# ==========================================

insert_query = """
INSERT INTO satellite_observations (
    mine_id,
    observation_date,
    ndvi,
    land_surface_temperature,
    soil_moisture,
    cloud_cover,
    latitude,
    longitude
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""


cursor = connection.cursor()

for _, row in satellite_data.iterrows():

    cursor.execute(
        insert_query,
        (
            row["mine_id"],
            row["observation_date"],
            row["ndvi"],
            row["land_surface_temperature"],
            row["soil_moisture"],
            row["cloud_cover"],
            row["latitude"],
            row["longitude"]
        )
    )


connection.commit()

cursor.close()
connection.close()


# ==========================================
# 4. Generated Data दिखाना
# ==========================================

print("\nSynthetic Satellite Data Generated:")

print(
    satellite_data[
        [
            "mine_id",
            "observation_date",
            "ndvi",
            "land_surface_temperature",
            "soil_moisture",
            "cloud_cover",
            "latitude",
            "longitude"
        ]
    ]
)


print("\nTotal Satellite Records:", len(satellite_data))

print("\nSatellite data inserted successfully!")