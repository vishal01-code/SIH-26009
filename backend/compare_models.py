import pandas as pd
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.9.3 - Model Comparison")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

test_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_test.csv"
)

linear_model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "production_model.pkl"
)

random_forest_file = os.path.join(
    project_root,
    "ml",
    "production",
    "random_forest_model.pkl"
)

# Load test data
test_data = pd.read_csv(test_file)

X_test = test_data.drop(
    columns=["actual_production"]
)

y_test = test_data["actual_production"]

print()
print("Testing Dataset Loaded!")
print("Rows:", len(test_data))

# Load models
linear_model = joblib.load(linear_model_file)
random_forest_model = joblib.load(random_forest_file)

print()
print("Both Models Loaded Successfully!")

# Predictions
linear_predictions = linear_model.predict(X_test)
random_forest_predictions = random_forest_model.predict(X_test)

# Linear Regression metrics
linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

linear_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        linear_predictions
    )
)

linear_r2 = r2_score(
    y_test,
    linear_predictions
)

# Random Forest metrics
rf_mae = mean_absolute_error(
    y_test,
    random_forest_predictions
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        random_forest_predictions
    )
)

rf_r2 = r2_score(
    y_test,
    random_forest_predictions
)

# Display comparison
print()
print("===================================")
print("MODEL COMPARISON")
print("===================================")

print()
print("Linear Regression")
print("MAE :", round(linear_mae, 2))
print("RMSE:", round(linear_rmse, 2))
print("R2  :", round(linear_r2, 2))

print()
print("Random Forest")
print("MAE :", round(rf_mae, 2))
print("RMSE:", round(rf_rmse, 2))
print("R2  :", round(rf_r2, 2))

# Select best model using R2
if rf_r2 > linear_r2:
    best_model = "Random Forest"
else:
    best_model = "Linear Regression"

print()
print("===================================")
print("BEST MODEL")
print("===================================")

print()
print("Best Model:", best_model)

print()
print("===================================")
print("Step 5.7.9.3 Completed Successfully")
print("===================================")