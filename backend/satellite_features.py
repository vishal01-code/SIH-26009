import pandas as pd
import psycopg2


# ==========================================
# 1. PostgreSQL से Satellite Data पढ़ना
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
    observation_date,
    ndvi,
    land_surface_temperature,
    soil_moisture,
    cloud_cover,
    latitude,
    longitude
FROM satellite_observations
ORDER BY id;
"""

data = pd.read_sql(query, connection)

connection.close()


# ==========================================
# 2. NDVI Score
# ==========================================

def calculate_ndvi_score(ndvi):

    if ndvi < 0.30:
        return 30

    elif ndvi < 0.50:
        return 50

    elif ndvi < 0.70:
        return 75

    else:
        return 100


data["ndvi_score"] = data["ndvi"].apply(
    calculate_ndvi_score
)


# ==========================================
# 3. Soil Moisture Score
# ==========================================

def calculate_soil_moisture_score(moisture):

    if moisture < 0.30:
        return 30

    elif moisture < 0.50:
        return 50

    elif moisture < 0.70:
        return 75

    else:
        return 100


data["soil_moisture_score"] = data[
    "soil_moisture"
].apply(
    calculate_soil_moisture_score
)


# ==========================================
# 4. Land Surface Temperature Score
# ==========================================

def calculate_temperature_score(temperature):

    if temperature < 30:
        return 100

    elif temperature < 35:
        return 75

    elif temperature < 40:
        return 50

    else:
        return 30


data["temperature_score"] = data[
    "land_surface_temperature"
].apply(
    calculate_temperature_score
)


# ==========================================
# 5. Cloud Cover Score
# ==========================================

def calculate_cloud_score(cloud_cover):

    if cloud_cover < 20:
        return 100

    elif cloud_cover < 50:
        return 75

    elif cloud_cover < 75:
        return 50

    else:
        return 30


data["cloud_score"] = data[
    "cloud_cover"
].apply(
    calculate_cloud_score
)


# ==========================================
# 6. Environmental Context Score
# ==========================================

data["environmental_context_score"] = (
    data["ndvi_score"] * 0.25
    + data["soil_moisture_score"] * 0.25
    + data["temperature_score"] * 0.25
    + data["cloud_score"] * 0.25
)


# ==========================================
# 7. Satellite Features देखना
# ==========================================

print("\nSatellite Feature Engineering:")

print(
    data[
        [
            "observation_date",
            "ndvi",
            "ndvi_score",
            "soil_moisture",
            "soil_moisture_score",
            "land_surface_temperature",
            "temperature_score",
            "cloud_cover",
            "cloud_score",
            "environmental_context_score"
        ]
    ]
)


# ==========================================
# 8. Feature Dataset Save करना
# ==========================================

output_path = "../data/features/satellite_features.csv"

data.to_csv(
    output_path,
    index=False
)

print("\nSatellite feature dataset created successfully!")
print(f"Saved to: {output_path}")