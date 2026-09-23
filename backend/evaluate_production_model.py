import pandas as pd
import os
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.6 - Model Evaluation")
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
    "production_model.pkl"
)


# Load testing data
test_data = pd.read_csv(test_file)

print()
print("Testing Dataset Loaded!")

print("Rows:", len(test_data))
print("Columns:", len(test_data.columns))


# Separate features and target
X_test = test_data.drop(
    columns=["actual_production"]
)

y_test = test_data["actual_production"]


# Load trained model
model = joblib.load(model_file)

print()
print("Trained Model Loaded Successfully!")


# Make predictions
y_pred = model.predict(X_test)


print()
print("Prediction Completed!")


# Calculate evaluation metrics
mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print()
print("===================================")
print("MODEL PERFORMANCE")
print("===================================")

print()
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))


print()
print("===================================")
print("Step 5.7.6 Completed Successfully")
print("===================================")