import pandas as pd
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.4 - Time-Based Train/Test Split")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_ml_dataset_180_days.csv"
)

output_folder = os.path.join(
    project_root,
    "data",
    "features"
)

train_file = os.path.join(
    output_folder,
    "production_train.csv"
)

test_file = os.path.join(
    output_folder,
    "production_test.csv"
)

data = pd.read_csv(input_file)

# Make sure data is sorted by date
# Date is not used as an ML feature,
# but it is needed for correct time ordering.
original_data = pd.read_csv(
    os.path.join(
        project_root,
        "data",
        "processed",
        "production_master_180_days.csv"
    )
)

original_data["production_date"] = pd.to_datetime(
    original_data["production_date"]
)

data["production_date"] = original_data[
    "production_date"
].values

data = data.sort_values(
    "production_date"
).reset_index(drop=True)

# 80% training, 20% testing
split_index = int(len(data) * 0.80)

train_data = data.iloc[:split_index].copy()
test_data = data.iloc[split_index:].copy()

# Remove date before saving ML datasets
train_data = train_data.drop(
    columns=["production_date"]
)

test_data = test_data.drop(
    columns=["production_date"]
)

train_data.to_csv(
    train_file,
    index=False
)

test_data.to_csv(
    test_file,
    index=False
)

print()
print("Dataset Split Successfully!")

print()
print("Total Rows:", len(data))

print()
print("Training Data:")
print("Rows:", len(train_data))
print("Columns:", len(train_data.columns))

print()
print("Testing Data:")
print("Rows:", len(test_data))
print("Columns:", len(test_data.columns))

print()
print("Training File:")
print(train_file)

print()
print("Testing File:")
print(test_file)

print()
print("===================================")
print("Step 5.7.4 Completed Successfully")
print("===================================")