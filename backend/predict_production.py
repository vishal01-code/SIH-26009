import pandas as pd
import os
import joblib

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.10.2 - Prediction Pipeline")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

model_file = os.path.join(
    project_root,
    "ml",
    "production",
    "production_model.pkl"
)

# Load trained model
model = joblib.load(model_file)

print()
print("Production Model Loaded Successfully!")

# Example new production input
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

print()
print("New Production Input:")
print(new_data)

# Make prediction
prediction = model.predict(new_data)

predicted_production = prediction[0]

print()
print("===================================")
print("PRODUCTION PREDICTION")
print("===================================")

print(
    "Predicted Production:",
    round(predicted_production, 2),
    "tonnes/day"
)

print()
print("===================================")
print("Step 5.7.10.2 Completed Successfully")
print("===================================")