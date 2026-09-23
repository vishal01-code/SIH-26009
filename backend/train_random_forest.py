import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
import joblib

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.9.1 - Random Forest Training")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

train_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_train.csv"
)

model_folder = os.path.join(
    project_root,
    "ml",
    "production"
)

os.makedirs(
    model_folder,
    exist_ok=True
)

model_file = os.path.join(
    model_folder,
    "random_forest_model.pkl"
)

# Load training data
train_data = pd.read_csv(train_file)

print()
print("Training Dataset Loaded!")
print("Rows:", len(train_data))
print("Columns:", len(train_data.columns))

# Separate input and target
X_train = train_data.drop(
    columns=["actual_production"]
)

y_train = train_data["actual_production"]

print()
print("Input Features:", X_train.shape)
print("Target:", y_train.shape)

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Train model
model.fit(
    X_train,
    y_train
)

print()
print("Random Forest Training Completed!")

# Save model
joblib.dump(
    model,
    model_file
)

print()
print("Random Forest Model Saved Successfully!")

print()
print("Model File:")
print(model_file)

print()
print("===================================")
print("Step 5.7.9.1 Completed Successfully")
print("===================================")