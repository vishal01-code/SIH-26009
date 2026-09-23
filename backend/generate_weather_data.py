import pandas as pd
import numpy as np
import os


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.3 - Weather Dataset Generation")
print("===================================")


np.random.seed(42)


project_root = os.path.dirname(
    os.path.dirname(__file__)
)


output_folder = os.path.join(
    project_root,
    "data",
    "raw"
)

os.makedirs(
    output_folder,
    exist_ok=True
)


dates = pd.date_range(
    start="2026-01-01",
    periods=180,
    freq="D"
)


records = []


for date in dates:

    rainfall = np.random.uniform(
        0,
        35
    )

    soil_moisture = (
        28
        + rainfall * 0.65
        + np.random.normal(0, 2)
    )

    land_temperature = (
        31
        - rainfall * 0.10
        + np.random.normal(0, 1)
    )

    humidity = (
        55
        + rainfall * 0.9
        + np.random.normal(0, 3)
    )

    records.append({
        "observation_date": date,
        "mine_id": 1,
        "rainfall_mm": round(rainfall, 2),
        "soil_moisture": round(soil_moisture, 2),
        "land_temperature": round(land_temperature, 2),
        "humidity": round(humidity, 2)
    })


data = pd.DataFrame(records)


print()
print("Weather Dataset Generated Successfully!")

print()
print("Rows:", len(data))

print("Columns:", len(data.columns))


print()
print("First 5 Records:")

print(data.head())


print()
print("Last 5 Records:")

print(data.tail())


output_file = os.path.join(
    output_folder,
    "weather_data_180_days.csv"
)


data.to_csv(
    output_file,
    index=False
)


print()
print("===================================")
print("Weather Dataset Saved Successfully!")
print("===================================")

print()
print("File Location:")

print(output_file)

print()
print("Final Dataset Shape:")

print(data.shape)


print()
print("===================================")
print("Step 5.6.3 Completed Successfully")
print("===================================")