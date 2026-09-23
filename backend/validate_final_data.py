import pandas as pd
import os


# Project root का path
project_root = os.path.dirname(os.path.dirname(__file__))


# Final integrated dataset का path
file_path = os.path.join(
    project_root,
    "data",
    "processed",
    "final_integrated_dataset.csv"
)


# Dataset load करना
data = pd.read_csv(file_path)


print("====================================")
print("FINAL DATASET VALIDATION")
print("====================================")


# 1. Dataset Size
print()
print("Dataset Size:")
print("Rows:", len(data))
print("Columns:", len(data.columns))


# 2. Column Names
print()
print("Column Names:")
print(data.columns.tolist())


# 3. Missing Values
print()
print("Missing Values:")
print(data.isnull().sum())


# 4. Duplicate Records
print()
print("Duplicate Records:")
print(data.duplicated().sum())


# 5. Data Types
print()
print("Data Types:")
print(data.dtypes)


# 6. First Records
print()
print("First 3 Records:")
print(data.head(3))


# ====================================
# LOGICAL DATA VALIDATION
# ====================================

print()
print("====================================")
print("LOGICAL DATA VALIDATION")
print("====================================")


# 1. Negative Values Check
print()
print("Negative Values:")

numeric_columns = [
    "planned_production",
    "actual_production",
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
    "average_performance_score"
]

for column in numeric_columns:
    negative_count = (data[column] < 0).sum()
    print(f"{column}: {negative_count}")


# 2. Actual Production > Planned Production Check
print()
print("Production Consistency:")

invalid_production = (
    data["actual_production"] > data["planned_production"]
).sum()

print(
    "Actual Production > Planned Production:",
    invalid_production
)


# 3. Downtime > Operating Hours Check
invalid_downtime = (
    data["downtime_hours"] > data["operating_hours"]
).sum()

print(
    "Downtime > Operating Hours:",
    invalid_downtime
)


# 4. Utilization Range Check
invalid_utilization = (
    (data["average_utilization"] < 0) |
    (data["average_utilization"] > 100)
).sum()

print(
    "Invalid Average Utilization:",
    invalid_utilization
)


# 5. Performance Score Range Check
invalid_performance = (
    (data["average_performance_score"] < 0) |
    