import os
import joblib
import pandas as pd

print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.1 - Shortfall Calculation")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "production_model.pkl"
)

# Load trained production model
model = joblib.load(model_file)

print()
print("Production Model Loaded Successfully!")

# New production input
new_data = pd.DataFrame([{
    "planned_production": 500,
    "operating_hours": 20,
    "downtime_hours": 2,
    "blasting_delay_hours": 1,
    "rainfall_mm": 8,
    "soil_moisture": 35,
    "land_temperature": 32,
    "humidity": 70,
    "equipment_operating_hours": 18,
    "equipment_downtime_hours": 2,
    "average_utilization": 90,
    "average_performance_score": 85,
    "planned_delay_hours": 1,
    "actual_delay_hours": 2,
    "blast_count": 4,
    "downtime_ratio": 0.10,
    "blasting_delay_ratio": 0.05,
    "equipment_downtime_ratio": 0.10,
    "equipment_performance_risk": 15,
    "rainfall_risk": 1
}])

# Get production prediction
prediction = model.predict(new_data)

predicted_production = prediction[0]

# Planned production
planned_production = new_data["planned_production"].iloc[0]

# Calculate shortfall
shortfall = planned_production - predicted_production

# Calculate shortfall percentage
shortfall_percentage = (
    shortfall / planned_production
) * 100

# Prevent negative shortfall
if shortfall < 0:
    shortfall = 0
    shortfall_percentage = 0

print()
print("===================================")
print("PRODUCTION ANALYSIS")
print("===================================")

print(
    "Planned Production:",
    round(planned_production, 2),
    "tonnes/day"
)

print(
    "Predicted Production:",
    round(predicted_production, 2),
    "tonnes/day"
)

print(
    "Production Shortfall:",
    round(shortfall, 2),
    "tonnes/day"
)

print(
    "Shortfall Percentage:",
    round(shortfall_percentage, 2),
    "%"
)

print()
print("===================================")
print("Step 6.1 Completed Successfully")
print("===================================")