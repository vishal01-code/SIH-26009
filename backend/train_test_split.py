import pandas as pd
import os

from sklearn.model_selection import train_test_split


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
print("Step 5.2 - Train Test Split")
print("===================================")


print()
print("Dataset loaded successfully!")

print()
print("Total Records:", len(data))


# Input Features

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


# Target

target_column = "actual_production"


X = data[feature_columns]

y = data[target_column]


print()
print("Input Features:", X.shape)

print("Target:", y.shape)


# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print()
print("===================================")
print("Train Test Split Result")
print("===================================")


print()
print("Training Features:", X_train.shape)

print("Testing Features:", X_test.shape)

print("Training Target:", y_train.shape)

print("Testing Target:", y_test.shape)


print()
print("Training Records:")
print(len(X_train))


print()
print("Testing Records:")
print(len(X_test))


print()
print("===================================")
print("Step 5.2 Completed Successfully")
print("===================================")