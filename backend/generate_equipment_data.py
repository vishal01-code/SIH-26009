import pandas as pd
import numpy as np
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.5 - Equipment Dataset Generation")
print("===================================")

np.random.seed(42)

project_root = os.path.dirname(os.path.dirname(__file__))

output_folder = os.path.join(
    project_root,
    "data",
    "raw"
)

os.makedirs(output_folder, exist_ok=True)

# 180 days
dates = pd.date_range(
    start="2026-01-01",
    periods=180,
    freq="D"
)

# 5 equipment
equipment_ids = [1, 2, 3, 4, 5]

records = []

for equipment_id in equipment_ids:

    for date in dates:

        operating_hours = np.random.uniform(14, 22)

        downtime_hours = np.random.uniform(0.5, 6)

        # Equipment utilization
        utilization_percent = (
            operating_hours /
            (operating_hours + downtime_hours)
        ) * 100

        # Performance score
        performance_score = (
            utilization_percent
            - downtime_hours * 2
            + np.random.normal(0, 3)
        )

        # Keep values within sensible range
        utilization_percent = max(
            40,
            min(100, utilization_percent)
        )

        performance_score = max(
            0,
            min(100, performance_score)
        )

        records.append({
            "equipment_id": equipment_id,
            "record_date": date,
            "operating_hours": round(
                operating_hours, 2
            ),
            "downtime_hours": round(
                downtime_hours, 2
            ),
            "utilization_percent": round(
                utilization_percent, 2
            ),
            "performance_score": round(
                performance_score, 2
            )
        })

# Create DataFrame
data = pd.DataFrame(records)

# Output file
output_file = os.path.join(
    output_folder,
    "equipment_performance_180_days.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Dataset Generated Successfully!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))

print()
print("Equipment Count:", data["equipment_id"].nunique())

print()
print("Date Range:")
print(
    data["record_date"].min(),
    "to",
    data["record_date"].max()
)

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.6.5 Completed Successfully")
print("===================================")