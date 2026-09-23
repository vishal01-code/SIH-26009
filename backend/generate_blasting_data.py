import pandas as pd
import numpy as np
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.7 - Blasting Dataset Generation")
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

records = []

for date in dates:

    # Planned blasting delay
    planned_delay_hours = np.random.uniform(0, 2)

    # Actual delay can be higher or lower
    actual_delay_hours = (
        planned_delay_hours
        + np.random.uniform(0, 2)
    )

    # Number of blasts
    blast_count = np.random.randint(1, 5)

    # Determine blasting status
    if actual_delay_hours <= 1:
        status = "On Time"
    elif actual_delay_hours <= 2.5:
        status = "Delayed"
    else:
        status = "Highly Delayed"

    records.append({
        "mine_id": 1,
        "blast_date": date,
        "planned_delay_hours": round(
            planned_delay_hours, 2
        ),
        "actual_delay_hours": round(
            actual_delay_hours, 2
        ),
        "blast_count": blast_count,
        "status": status
    })

# Create DataFrame
data = pd.DataFrame(records)

# Output file
output_file = os.path.join(
    output_folder,
    "blasting_data_180_days.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Blasting Dataset Generated Successfully!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))

print()
print("Date Range:")
print(
    data["blast_date"].min(),
    "to",
    data["blast_date"].max()
)

print()
print("Status Distribution:")
print(
    data["status"].value_counts()
)

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.6.7 Completed Successfully")
print("===================================")