import os
import pandas as pd

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.4 - Equipment Risk Classification")
print("===================================")

# Project root
project_root = os.path.dirname(os.path.dirname(__file__))

# Input file
input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_risk_scores.csv"
)

# Load risk scores
data = pd.read_csv(input_file)

print()
print("Equipment Risk Scores Loaded Successfully!")


# -----------------------------------
# Risk Classification
# -----------------------------------

def classify_equipment_risk(score):

    if score <= 30:
        return "LOW"

    elif score <= 60:
        return "MEDIUM"

    else:
        return "HIGH"


data["risk_level"] = data[
    "equipment_risk_score"
].apply(classify_equipment_risk)


# -----------------------------------
# Risk Priority
# -----------------------------------

def determine_priority(risk_level):

    if risk_level == "HIGH":
        return "IMMEDIATE ACTION"

    elif risk_level == "MEDIUM":
        return "MONITOR"

    else:
        return "NORMAL"


data["risk_priority"] = data[
    "risk_level"
].apply(determine_priority)


# -----------------------------------
# Display Results
# -----------------------------------

print()
print("===================================")
print("EQUIPMENT RISK CLASSIFICATION")
print("===================================")

print(
    data[
        [
            "equipment_id",
            "equipment_risk_score",
            "risk_level",
            "risk_priority"
        ]
    ]
)


# -----------------------------------
# Save Output
# -----------------------------------

output_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_risk_classification.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Risk Classification Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.4 Completed Successfully")
print("===================================")