import os
import pandas as pd

print("===================================")
print("Phase 7 - Equipment Risk Prediction")
print("Step 7.2 - Equipment Performance Metrics")
print("===================================")

# Project root
project_root = os.path.dirname(os.path.dirname(__file__))

# Input file
input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_summary.csv"
)

# Load equipment summary
data = pd.read_csv(input_file)

print()
print("Equipment Summary Loaded Successfully!")

print()
print("Input Data:")
print(data)

# Calculate total available hours
data["total_available_hours"] = (
    data["total_operating_hours"]
    + data["total_downtime_hours"]
)

# Calculate downtime ratio
data["downtime_ratio"] = (
    data["total_downtime_hours"]
    / data["total_available_hours"]
)

# Convert to percentage
data["downtime_percent"] = (
    data["downtime_ratio"] * 100
)

# Equipment efficiency
data["equipment_efficiency"] = (
    data["average_utilization"]
    * data["average_performance"]
    / 100
)

# Round calculated values
data["downtime_ratio"] = data["downtime_ratio"].round(4)
data["downtime_percent"] = data["downtime_percent"].round(2)
data["equipment_efficiency"] = data["equipment_efficiency"].round(2)

# Performance status
def get_status(row):

    if (
        row["average_utilization"] >= 85
        and row["average_performance"] >= 80
        and row["downtime_percent"] < 15
    ):
        return "GOOD"

    elif (
        row["average_utilization"] >= 80
        and row["average_performance"] >= 70
        and row["downtime_percent"] < 20
    ):
        return "MODERATE"

    else:
        return "POOR"


data["performance_status"] = data.apply(
    get_status,
    axis=1
)

print()
print("===================================")
print("EQUIPMENT PERFORMANCE METRICS")
print("===================================")

print(
    data[
        [
            "equipment_id",
            "total_operating_hours",
            "total_downtime_hours",
            "average_utilization",
            "average_performance",
            "downtime_percent",
            "equipment_efficiency",
            "performance_status"
        ]
    ]
)

# Output file
output_file = os.path.join(
    project_root,
    "data",
    "processed",
    "equipment_metrics.csv"
)

data.to_csv(
    output_file,
    index=False
)

print()
print("Equipment Metrics Saved Successfully!")

print()
print("Output File:")
print(output_file)

print()
print("===================================")
print("Step 7.2 Completed Successfully")
print("===================================")