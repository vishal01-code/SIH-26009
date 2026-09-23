import os
import pandas as pd

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.6 - Equipment Recommendation")
print("===================================")


# -----------------------------------
# Project Root
# -----------------------------------

project_root = os.path.dirname(os.path.dirname(__file__))


# -----------------------------------
# Input File
# -----------------------------------

input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_risk_reasons.csv"
)


# -----------------------------------
# Load Data
# -----------------------------------

data = pd.read_csv(input_file)

print()
print("Equipment Risk Reason Data Loaded Successfully!")


# -----------------------------------
# Generate Recommendations
# -----------------------------------

def generate_recommendation(row):

    recommendations = []

    reasons = row["risk_reasons"]

    # High Downtime
    if "High Downtime" in reasons:
        recommendations.append(
            "Inspect equipment and perform preventive maintenance"
        )

    # Low Performance
    if "Low Performance" in reasons:
        recommendations.append(
            "Perform equipment performance diagnostics and maintenance"
        )

    # Low Utilization
    if "Low Utilization" in reasons:
        recommendations.append(
            "Optimize equipment deployment and operating schedule"
        )

    # No major risk
    if len(recommendations) == 0:
        recommendations.append(
            "Continue normal equipment monitoring"
        )

    return "; ".join(recommendations)


data["recommendation"] = data.apply(
    generate_recommendation,
    axis=1
)


# -----------------------------------
# Recommendation Priority
# -----------------------------------

def determine_priority(row):

    risk_level = row["equipment_risk_level"]

    if risk_level == "HIGH":
        return "HIGH"

    elif risk_level == "MEDIUM":
        return "MEDIUM"

    else:
        return "LOW"


data["recommendation_priority"] = data.apply(
    determine_priority,
    axis=1
)


# -----------------------------------
# Display Results
# -----------------------------------

print()
print("===================================")
print("EQUIPMENT RECOMMENDATIONS")
print("===================================")

print(
    data[
        [
            "equipment_id",
            "equipment_risk_score",
            "equipment_risk_level",
            "risk_reasons",
            "primary_risk_reason",
            "recommendation",
            "recommendation_priority"
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
    "equipment_recommendations.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Recommendations Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.6 Completed Successfully")
print("===================================")