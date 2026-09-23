import pandas as pd
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.6.10 - Master Dataset Verification")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "production_master_180_days.csv"
)

data = pd.read_csv(input_file)

print()
print("Master Dataset Loaded Successfully!")

print()
print("Rows:", len(data))
print("Columns:", len(data.columns))

print()
print("Date Range:")
print("Start:", data["production_date"].min())
print("End:", data["production_date"].max())

print()
print("Duplicate Dates:",
      data["production_date"].duplicated().sum())

print()
print("Missing Values:")
print(data.isnull().sum())

print()
print("First 5 Rows:")
print(data.head())

print()
print("===================================")
print("Step 5.6.10 Completed")
print("===================================")