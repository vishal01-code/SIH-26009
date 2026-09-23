import pandas as pd
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.2 - Feature Engineering")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "production_master_180_days.csv"
)

output_folder = os.path.join(
    project_root,
    "data",
    "features"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = os.path.join(
    output_folder,
    "production_features_180_days.csv"
)

data = pd.read_csv(input_file)

print()
print("Master Dataset Loaded!")
print("Rows:", len(data))
print("Columns:", len(data.columns))


# 1. Downtime Ratio
data["downtime_ratio"] = (
    data["downtime_hours"] /
    data["operating_hours"]
)


# 2. Blasting Delay Ratio
data["blasting_delay_ratio"] = (
    data["blasting_delay_hours"] /
    data["operating_hours"]
)


# 3. Equipment Downtime Ratio
data["equipment_downtime_ratio"] = (
    data["equipment_downtime_hours"] /
    (
        data["equipment_operating_hours"]
        + data["equipment_downtime_hours"]
    )
)


# 4. Equipment Performance Risk
data["equipment_performance_risk"] = (
    100 -
    data["average_performance_score"]
)


# 5. Rainfall Risk
data["rainfall_risk"] = 0

data.loc[
    data["rainfall_mm"] > 5,
    "rainfall_risk"
] = 1

data.loc[
    data["rainfall_mm"] > 15,
    "rainfall_risk"
] = 2


# Save Feature Dataset
data.to_csv(
    output_file,
    index=False
)

print()
print("Feature Engineering Completed!")

print()
print("New Features:")

print("- downtime_ratio")
print("- blasting_delay_ratio")
print("- equipment_downtime_ratio")
print("- equipment_performance_risk")
print("- rainfall_risk")

print()
print("Rows:", len(data))
print("Columns:", len(data.columns))

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.7.2 Completed Successfully")
print("===================================")