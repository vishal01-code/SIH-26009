import pandas as pd
import os


project_root = os.path.dirname(
    os.path.dirname(__file__)
)


input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "ml_ready_production.csv"
)


data = pd.read_csv(input_file)


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.1 - ML Dataset Check")
print("===================================")


print()
print("Dataset loaded successfully!")


print()
print("Rows:", len(data))
print("Columns:", len(data.columns))


print()
print("Dataset Columns:")

for column in data.columns:
    print("-", column)


print()
print("Input Features:")

feature_columns = [
    "mine_id",
    "planned_production",
    "operating_hours",
    "downtime_hours",
    "blasting_delay_hours",
    "rainfall_mm",
    "soil_moisture",
    "land_temperature",
    "humidity",
    "total_operating_hours",
    "total_downtime_hours",
    "average_utilization",
    "average_performance_score",
    "downtime_ratio",
    "blasting_delay_ratio",
    "equipment_downtime_ratio",
    "equipment_performance_risk",
    "rainfall_risk",
    "year",
    "month",
    "day",
    "day_of_week"
]


for feature in feature_columns:
    print("-", feature)


print()
print("Number of Input Features:",
      len(feature_columns))


target_column = "actual_production"


print()
print("Target Column:")
print(target_column)


print()
print("Target Values:")

print(data[target_column])


print()
print("===================================")
print("Step 5.1 Completed Successfully")
print("===================================")