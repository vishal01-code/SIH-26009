import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import joblib

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.5 - Model Training")
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
    "production_model.pkl"
)


# Load training data
train_data = pd.read_csv(train_file)

print()
print("Training Dataset Loaded!")

print("Rows:", len(train_data))
print("Columns:", len(train_data.columns))


# Separate features and target
X_train = train_data.drop(
    columns=["actual_production"]
)

y_train = train_data["actual_production"]


print()
print("Input Features:", X_train.shape)
print("Target:", y_train.shape)


# Create Linear Regression model
model = LinearRegression()


# Train model
model.fit(
    X_train,
    y_train
)


print()
print("Model Training Completed!")


# Save trained model
joblib.dump(
    model,
    model_file
)


print()
print("Model Saved Successfully!")

print()
print("Model File:")
print(model_file)

print()
print("===================================")
print("Step 5.7.5 Completed Successfully")
print("===================================")