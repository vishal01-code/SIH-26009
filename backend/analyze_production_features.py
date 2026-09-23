import pandas as pd
import os
import joblib

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.10.1 - Feature Analysis")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

train_file = os.path.join(
    project_root,
    "data",
    "features",
    "production_train.csv"
)

model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "production_model.pkl"
)

# Load training data
train_data = pd.read_csv(train_file)

print()
print("Training Dataset Loaded!")
print("Rows:", len(train_data))

# Separate features
X_train = train_data.drop(
    columns=["actual_production"]
)

# Load trained Linear Regression model
model = joblib.load(model_file)

print()
print("Linear Regression Model Loaded!")

# Get feature coefficients
feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Coefficient": model.coef_
})

# Calculate absolute importance
feature_importance["Absolute Importance"] = (
    feature_importance["Coefficient"].abs()
)

# Sort by importance
feature_importance = feature_importance.sort_values(
    by="Absolute Importance",
    ascending=False
)

print()
print("===================================")
print("FEATURE IMPORTANCE")
print("===================================")

print(
    feature_importance[
        ["Feature", "Coefficient", "Absolute Importance"]
    ].to_string(index=False)
)

# Save results
output_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

output_file = os.path.join(
    output_folder,
    "production_feature_importance.csv"
)

feature_importance.to_csv(
    output_file,
    index=False
)

print()
print("Feature Analysis Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 5.7.10.1 Completed Successfully")
print("===================================")