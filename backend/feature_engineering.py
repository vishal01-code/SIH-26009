import pandas as pd
import os


# Project root का path
project_root = os.path.dirname(os.path.dirname(__file__))


# Input dataset का path
input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "final_integrated_dataset.csv"
)


# Dataset को Python में load करना
data = pd.read_csv(input_file)

print("Dataset successfully loaded!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))


# Production Gap Feature बनाना
data["production_gap"] = (
    data["planned_production"] - data["actual_production"]
)


# Production Gap को देखना
print()
print("Production Gap Feature:")
print(
    data[
        [
            "production_date",
            "planned_production",
            "actual_production",
            "production_gap"
        ]
    ]
)


# Production Gap का summary
print()
print("Production Gap Summary:")
print("Minimum Gap:", data["production_gap"].min())
print("Maximum Gap:", data["production_gap"].max())
print("Average Gap:", data["production_gap"].mean())


data["downtime_ratio"] = (
    data["downtime_hours"] / data["operating_hours"]
)

print()
print("Downtime Ratio Feature:")
print(
    data[
        [
            "production_date",
            "operating_hours",
            "downtime_hours",
            "downtime_ratio"
        ]
    ]
)


data["blasting_delay_ratio"] = (
    data["blasting_delay_hours"] / data["operating_hours"]
)

print()
print("Blasting Delay Ratio Feature:")
print(
    data[
        [
            "production_date",
            "operating_hours",
            "blasting_delay_hours",
            "blasting_delay_ratio"
        ]
    ]
)


# Features folder का path
features_folder = os.path.join(
    project_root,
    "data",
    "features"
)


# अगर folder मौजूद नहीं है तो बनाना
os.makedirs(
    features_folder,
    exist_ok=True
)


# Output file का path
output_file = os.path.join(
    features_folder,
    "feature_engineered_data.csv"
)


# Feature engineered dataset save करना
data.to_csv(
    output_file,
    index=False
)

# Step 8.4: Equipment Features

data["equipment_downtime_ratio"] = (
    data["total_downtime_hours"] /
    data["total_operating_hours"]
)

data["equipment_performance_risk"] = (
    100 - data["average_performance_score"]
)

print()
print("Equipment Features:")
print(
    data[
        [
            "production_date",
            "total_operating_hours",
            "total_downtime_hours",
            "average_utilization",
            "average_performance_score",
            "equipment_downtime_ratio",
            "equipment_performance_risk"
        ]
    ]
)

# Step 8.5: Weather Features

data["rainfall_risk"] = pd.cut(
    data["rainfall_mm"],
    bins=[-1, 5, 15, float("inf")],
    labels=[0, 1, 2]
).astype(int)

print()
print("Weather Features:")
print(
    data[
        [
            "production_date",
            "rainfall_mm",
            "soil_moisture",
            "land_temperature",
            "humidity",
            "rainfall_risk"
        ]
    ]
)


# Step 8.6: Final Feature Validation

print()
print("Final Feature Validation")
print("------------------------")

required_features = [
    "production_gap",
    "downtime_ratio",
    "blasting_delay_ratio",
    "equipment_downtime_ratio",
    "equipment_performance_risk",
    "rainfall_risk"
]

print("Required Features:")

for feature in required_features:
    if feature in data.columns:
        print(f"{feature}: OK")
    else:
        print(f"{feature}: MISSING")


print()
print("Missing Values in Features:")

print(
    data[required_features].isnull().sum()
)


print()
print("Final Dataset Shape:")
print("Rows:", len(data))
print("Columns:", len(data.columns))


final_output_file = os.path.join(
    features_folder,
    "final_feature_dataset.csv"
)

data.to_csv(
    final_output_file,
    index=False
)

print()
print("Final Feature Dataset saved successfully!")
print("File:", final_output_file)

print()
print("Feature engineered dataset saved successfully!")
print("File:", output_file)