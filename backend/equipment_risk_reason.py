import os
import pandas as pd

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.5 - Equipment Risk Reason Analysis")
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

# Load data
data = pd.read_csv(input_file)

print()
print("Equipment Risk Data Loaded Successfully!")


# -----------------------------------
# Risk Reason Analysis
# -----------------------------------

def analyze_reason(row):

    reasons = []

    downtime = row["downtime_percent"]
    performance = row["average_performance"]
    utilization = row["average_utilization"]

    # Downtime reason
    if downtime >= 15:
        reasons.append("High Downtime")

    # Performance reason
    if performance < 80:
        reasons.append("Low Performance")

    # Utilization reason
    if utilization < 85:
        reasons.append("Low Utilization")

    # If no major factor is detected
    if len(reasons) == 0:
        return "No Major Risk Factor"

    # Combine multiple reasons
    return ", ".join(reasons)


data["risk_reasons"] = data.apply(
    analyze_reason,
    axis=1
)


# -----------------------------------
# Primary Reason
# -----------------------------------

def determine_primary_reason(row):

    downtime = row["downtime_percent"]
    performance = row["average_performance"]
    utilization = row["average_utilization"]

    # Highest priority factor
    if downtime >= 15:
        return "High Downtime"

    elif performance < 80:
        return "Low Performance"

    elif utilization < 85:
        return "Low Utilization"

    else:
        return "No Major Risk Factor"


data["primary_risk_reason"] = data.apply(
    determine_primary_reason,
    axis=1
)


# -----------------------------------
# Display Results
# -----------------------------------

print()
print("===================================")
print("EQUIPMENT RISK REASON ANALYSIS")
print("===================================")

print(
    data[
        [
            "equipment_id",
            "equipment_risk_score",
            "equipment_risk_level",
            "downtime_percent",
            "average_performance",
            "average_utilization",
            "risk_reasons",
            "primary_risk_reason"
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
    "equipment_risk_reasons.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Risk Reasons Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.5 Completed Successfully")
print("===================================")