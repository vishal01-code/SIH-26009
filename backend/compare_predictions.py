import pandas as pd
import os
import joblib

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.7 - Actual vs Predicted")
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


# Separate features and target
X_test = test_data.drop(
    columns=["actual_production"]
)

y_test = test_data["actual_production"]


# Load trained model
model = joblib.load(model_file)

print()
print("Trained Model Loaded Successfully!")


# Prediction
y_pred = model.predict(X_test)


# Create comparison table
comparison = pd.DataFrame({
    "Actual Production": y_test,
    "Predicted Production": y_pred
})

comparison["Error"] = (
    comparison["Actual Production"]
    - comparison["Predicted Production"]
)

comparison["Absolute Error"] = (
    comparison["Error"].abs()
)


print()
print("===================================")
print("ACTUAL VS PREDICTED PRODUCTION")
print("===================================")

print()

print(
    comparison.round(2).to_string(index=False)
)


# Save comparison
output_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = os.path.join(
    output_folder,
    "production_predictions_comparison.csv"
)

comparison.round(2).to_csv(
    output_file,
    index=False
)


print()
print("===================================")
print("Prediction Comparison Saved!")
print("===================================")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.7.7 Completed Successfully")
print("===================================")