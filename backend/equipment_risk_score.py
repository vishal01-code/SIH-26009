import os
import pandas as pd

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.3 - Equipment Risk Score")
print("===================================")

# Project root
project_root = os.path.dirname(os.path.dirname(__file__))

# Input file
input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_metrics.csv"
)

# Load equipment metrics
data = pd.read_csv(input_file)

print()
print("Equipment Metrics Loaded Successfully!")

print()
print("Input Data:")
print(data)

# -----------------------------------
# 1. Downtime Risk Score
# -----------------------------------

def calculate_downtime_risk(downtime_percent):

    if downtime_percent < 10:
        return 10

    elif downtime_percent < 15:
        return 20

    elif downtime_percent < 20:
        return 35

    elif downtime_percent < 30:
        return 50

    else:
        return 70


data["downtime_risk_score"] = data[
    "downtime_percent"
].apply(calculate_downtime_risk)


# -----------------------------------
# 2. Performance Risk Score
# -----------------------------------

def calculate_performance_risk(performance):

    if performance >= 90:
        return 5

    elif performance >= 80:
        return 15

    elif performance >= 70:
        return 30

    elif performance >= 60:
        return 50

    else:
        return 70


data["performance_risk_score"] = data[
    "average_performance"
].apply(calculate_performance_risk)


# -----------------------------------
# 3. Utilization Risk Score
# -----------------------------------

def calculate_utilization_risk(utilization):

    if utilization >= 90:
        return 5

    elif utilization >= 85:
        return 15

    elif utilization >= 80:
        return 30

    elif utilization >= 70:
        return 50

    else:
        return 70


data["utilization_risk_score"] = data[
    "average_utilization"
].apply(calculate_utilization_risk)


# -----------------------------------
# 4. Final Equipment Risk Score
# -----------------------------------

data["equipment_risk_score"] = (
    data["downtime_risk_score"] * 0.40
    + data["performance_risk_score"] * 0.35
    + data["utilization_risk_score"] * 0.25
)

data["equipment_risk_score"] = (
    data["equipment_risk_score"].round(2)
)


# -----------------------------------
# 5. Risk Classification
# -----------------------------------

def classify_risk(score):

    if score <= 30:
        return "LOW"

    elif score <= 60:
        return "MEDIUM"

    else:
        return "HIGH"


data["equipment_risk_level"] = data[
    "equipment_risk_score"
].apply(classify_risk)


# -----------------------------------
# Display Results
# -----------------------------------

print()
print("===================================")
print("EQUIPMENT RISK SCORE")
print("===================================")

print(
    data[
        [
            "equipment_id",
            "downtime_percent",
            "average_performance",
            "average_utilization",
            "downtime_risk_score",
            "performance_risk_score",
            "utilization_risk_score",
            "equipment_risk_score",
            "equipment_risk_level"
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
    "equipment_risk_scores.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Risk Scores Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.3 Completed Successfully")
print("===================================")