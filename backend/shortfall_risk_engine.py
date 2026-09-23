import os
import joblib
import pandas as pd

print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.4 - Complete Risk Engine")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "production_model.pkl"
)

# Load production model
model = joblib.load(model_file)

print()
print("Production Model Loaded Successfully!")

# Production input
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

# ===================================
# 1. Production Prediction
# ===================================

predicted_production = model.predict(new_data)[0]

planned_production = new_data[
    "planned_production"
].iloc[0]

# ===================================
# 2. Shortfall Calculation
# ===================================

shortfall = planned_production - predicted_production

if shortfall < 0:
    shortfall = 0

shortfall_percentage = (
    shortfall / planned_production
) * 100

# ===================================
# 3. Risk Classification
# ===================================

if shortfall_percentage <= 5:
    risk_level = "LOW"

elif shortfall_percentage <= 10:
    risk_level = "MEDIUM"

else:
    risk_level = "HIGH"

# ===================================
# 4. Reason Analysis
# ===================================

downtime_hours = new_data[
    "downtime_hours"
].iloc[0]

blasting_delay_hours = new_data[
    "blasting_delay_hours"
].iloc[0]

rainfall_mm = new_data[
    "rainfall_mm"
].iloc[0]

reasons = []

if downtime_hours >= 2:
    reasons.append("Equipment Downtime")

if blasting_delay_hours >= 1:
    reasons.append("Blasting Delay")

if rainfall_mm > 5:
    reasons.append("Rainfall")

# Primary reason
if downtime_hours >= 2:
    primary_reason = "Equipment Downtime"

elif blasting_delay_hours >= 1:
    primary_reason = "Blasting Delay"

elif rainfall_mm > 5:
    primary_reason = "Rainfall"

else:
    primary_reason = "No Major Risk Factor"

# ===================================
# FINAL REPORT
# ===================================

print()
print("===================================")
print("FINAL SHORTFALL RISK REPORT")
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

print(
    "Risk Level:",
    risk_level
)

print()
print("Detected Factors:")

for reason in reasons:
    print("-", reason)

print()
print(
    "Primary Reason:",
    primary_reason
)

print()
print("===================================")
print("Step 6.4 Completed Successfully")
print("===================================")