import pandas as pd
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.9.2 - Random Forest Evaluation")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

test_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_test.csv"
)

model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "random_forest_model.pkl"
)

# Load test data
test_data = pd.read_csv(test_file)

print()
print("Testing Dataset Loaded!")
print("Rows:", len(test_data))
print("Columns:", len(test_data.columns))

# Separate input and target
X_test = test_data.drop(
    columns=["actual_production"]
)

y_test = test_data["actual_production"]

print()
print("Input Features:", X_test.shape)
print("Target:", y_test.shape)

# Load Random Forest model
model = joblib.load(model_file)

print()
print("Random Forest Model Loaded!")

# Make predictions
predictions = model.predict(X_test)

print()
print("Predictions Generated!")

# Calculate evaluation metrics
mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)

# Display results
print()
print("===================================")
print("Random Forest Evaluation Results")
print("===================================")

print()
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 2))

print()
print("===================================")
print("Step 5.7.9.2 Completed Successfully")
print("===================================")