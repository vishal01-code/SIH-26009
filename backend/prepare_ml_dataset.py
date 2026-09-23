import pandas as pd
import os

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.3 - ML Dataset Preparation")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_features_180_days.csv"
)

output_folder = os.path.join(
    project_root,
    "data",
    "features"
)

output_file = os.path.join(
    output_folder,
    "production_ml_dataset_180_days.csv"
)

data = pd.read_csv(input_file)

print()
print("Feature Dataset Loaded!")

print("Rows:", len(data))
print("Columns:", len(data.columns))


# Target
target = "actual_production"


# Columns that should not be used as ML features
columns_to_remove = [
    "mine_id",
    "production_date",
    "status",
    "actual_production"
]


# Create X
X = data.drop(
    columns=columns_to_remove
)


# Create y
y = data[target]


print()
print("ML Features (X):")
for column in X.columns:
    print("-", column)


print()
print("Target (y):")
print("-", target)


print()
print("X Shape:", X.shape)
print("y Shape:", y.shape)


# Combine X and y for final ML dataset
ml_dataset = X.copy()

ml_dataset[target] = y

ml_dataset.to_csv(
    output_file,
    index=False
)


print()
print("ML Dataset Created Successfully!")

print()
print("Final ML Dataset:")
print("Rows:", len(ml_dataset))
print("Columns:", len(ml_dataset.columns))

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.7.3 Completed Successfully")
print("===================================")