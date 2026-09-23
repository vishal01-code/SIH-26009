import pandas as pd
import numpy as np
import os


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6 - Synthetic Dataset Expansion")
print("===================================")


# Random values को reproducible बनाने के लिए
np.random.seed(42)


# Project root
project_root = os.path.dirname(
    os.path.dirname(__file__)
)


# Output folder
output_folder = os.path.join(
    project_root,
    "data",
    "raw"
)

os.makedirs(
    output_folder,
    exist_ok=True
)


# 180 days का date range
dates = pd.date_range(
    start="2026-01-01",
    periods=180,
    freq="D"
)


records = []


for date in dates:

    # Planned production
    planned_production = 500


    # Weather
    rainfall = np.random.uniform(
        0,
        35
    )

    soil_moisture = (
        28 +
        rainfall * 0.65 +
        np.random.normal(0, 2)
    )

    land_temperature = (
        31 -
        rainfall * 0.10 +
        np.random.normal(0, 1)
    )

    humidity = (
        55 +
        rainfall * 0.9 +
        np.random.normal(0, 3)
    )


    # Equipment
    operating_hours = np.random.uniform(
        16,
        22
    )

    downtime_hours = np.random.uniform(
        0.5,
        5
    )

    blasting_delay_hours = np.random.uniform(
        0,
        3.5
    )


    # Production calculation
    production_loss = (
        downtime_hours * 10
        +
        blasting_delay_hours * 8
        +
        rainfall * 1.2
    )


    actual_production = (
        planned_production
        - production_loss
        + np.random.normal(0, 8)
    )


    # Production को reasonable range में रखना
    actual_production = max(
        350,
        min(
            510,
            actual_production
        )
    )


    records.append({

        "production_date": date,

        "mine_id": 1,

        "planned_production":
            round(
                planned_production,
                2
            ),

        "actual_production":
            round(
                actual_production,
                2
            ),

        "operating_hours":
            round(
                operating_hours,
                2
            ),

        "downtime_hours":
            round(
                downtime_hours,
                2
            ),

        "blasting_delay_hours":
            round(
                blasting_delay_hours,
                2
            ),

        "rainfall_mm":
            round(
                rainfall,
                2
            ),

        "soil_moisture":
            round(
                soil_moisture,
                2
            ),

        "land_temperature":
            round(
                land_temperature,
                2
            ),

        "humidity":
            round(
                humidity,
                2
            )
    })


# DataFrame बनाना
data = pd.DataFrame(
    records
)


print()
print("Dataset Generated Successfully!")


print()
print("Rows:",
      len(data))

print(
    "Columns:",
    len(data.columns)
)


print()
print("First 5 Records:")

print(
    data.head()
)


print()
print("Last 5 Records:")

print(
    data.tail()
)


# File save करना
output_file = os.path.join(
    output_folder,
    "production_data_180_days.csv"
)


data.to_csv(
    output_file,
    index=False
)


print()
print("===================================")
print("Dataset Saved Successfully!")
print("===================================")


print()
print("File Location:")

print(
    output_file
)


print()
print("Final Dataset Shape:")

print(
    data.shape
)


print()
print("===================================")
print("Step 5.6.1 Completed Successfully")
print("===================================")