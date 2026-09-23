import pandas as pd
import os


# Project root directory
project_root = os.path.dirname(
    os.path.dirname(__file__)
)


# Final feature dataset का path
input_file = os.path.join(
    project_root,
    "data",
    "features",
    "final_feature_dataset.csv"
)


# Dataset load करना
data = pd.read_csv(input_file)


print("===================================")
print("ML-Ready Dataset Preparation")
print("===================================")


print()
print("Dataset successfully loaded!")

print()
print("Original Rows:", len(data))
print("Original Columns:", len(data.columns))


print()
print("Original Columns:")

print(
    data.columns.tolist()
)


print()
print("===================================")
print("Step 10.1 - Removing Unnecessary Columns")
print("===================================")

columns_to_remove = [
    "observation_date",
    "record_date",
    "production_gap"
]

data = data.drop(
    columns=columns_to_remove
)

print()
print("Removed Columns:")
print(columns_to_remove)

print()
print("Remaining Columns:")
print(data.columns.tolist())

print()
print("Remaining Rows:", len(data))
print("Remaining Columns:", len(data.columns))


print()
print("===================================")
print("Step 10.2 - Date Feature Engineering")
print("===================================")

# Convert production_date into datetime format

data["production_date"] = pd.to_datetime(
    data["production_date"]
)

# Extract useful date features

data["year"] = data["production_date"].dt.year

data["month"] = data["production_date"].dt.month

data["day"] = data["production_date"].dt.day

data["day_of_week"] = data["production_date"].dt.dayofweek

print()
print("Date Features Created:")

print(
    data[
        [
            "production_date",
            "year",
            "month",
            "day",
            "day_of_week"
        ]
    ]
)

print()
print("Date Feature Engineering completed successfully!")


print()
print("===================================")
print("Step 10.3 - Input Features and Target")
print("===================================")

# Input features for the ML model

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

# Target variable

target_column = "actual_production"

X = data[feature_columns]

y = data[target_column]

print()
print("Input Features:")
print(X.columns.tolist())

print()
print("Number of Input Features:", len(X.columns))

print()
print("Target:")
print(target_column)

print()
print("Feature Dataset Shape:")
print(X.shape)

print()
print("Target Dataset Shape:")
print(y.shape)

print()
print("===================================")
print("Step 10.4 - Creating ML-Ready Dataset")
print("===================================")

# Create a copy of input features

ml_data = X.copy()

# Add target column

ml_data["actual_production"] = y

print()
print("ML-Ready Dataset:")

print(ml_data)

print()
print("ML-Ready Dataset Shape:")

print("Rows:", len(ml_data))

print("Columns:", len(ml_data.columns))

print()
print("ML-Ready Dataset Columns:")

print(ml_data.columns.tolist())

print()
print("===================================")
print("Step 10.5 - Final ML Dataset Validation")
print("===================================")

print()
print("1. Checking Missing Values:")

missing_values = ml_data.isnull().sum()

print(missing_values)

print()
print("Total Missing Values:",
      ml_data.isnull().sum().sum())


print()
print("2. Checking Duplicate Records:")

duplicate_count = ml_data.duplicated().sum()

print("Duplicate Records:", duplicate_count)


print()
print("3. Checking Negative Values:")

numeric_columns = ml_data.select_dtypes(
    include="number"
).columns

negative_values = (
    ml_data[numeric_columns] < 0
).sum()

print(negative_values)


print()
print("4. Checking Required Features:")

required_columns = feature_columns + [
    "actual_production"
]

for column in required_columns:

    if column in ml_data.columns:
        print(f"{column}: OK")
    else:
        print(f"{column}: MISSING")


print()
print("5. Checking Feature and Target Rows:")

print("Input Feature Rows:", len(X))

print("Target Rows:", len(y))


if len(X) == len(y):

    print("Feature and Target row count: OK")

else:

    print("Feature and Target row count: ERROR")


print()
print("===================================")
print("Final ML Dataset Validation Completed")
print("===================================")

print()
print("===================================")
print("Step 10.6 - Saving ML-Ready Dataset")
print("===================================")

# Project root folder
project_root = os.path.dirname(
    os.path.dirname(__file__)
)

# Processed data folder
processed_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

# Make sure folder exists
os.makedirs(
    processed_folder,
    exist_ok=True
)

# Output file path
output_file = os.path.join(
    processed_folder,
    "ml_ready_production.csv"
)

# Save ML-ready dataset
ml_data.to_csv(
    output_file,
    index=False
)

print()
print("ML-Ready Dataset saved successfully!")

print()
print("File Location:")
print(output_file)

print()
print("Final Dataset Shape:")
print("Rows:", len(ml_data))
print("Columns:", len(ml_data.columns))

print()
print("===================================")
print("Step 10.6 Completed Successfully")
print("===================================")