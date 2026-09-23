import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


project_root = os.path.dirname(
    os.path.dirname(__file__)
)


input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "ml_ready_production.csv"
)


data = pd.read_csv(input_file)


print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.3 - Baseline Model")
print("===================================")


print()
print("Dataset loaded successfully!")

print()
print("Total Records:", len(data))


feature_columns = [
    "mine_id",
    "planned_production",
    "operating_hours",
    "downtime_hours",
    "blasting_delay_hours",
    "rainfall_mm",
    "soil_moisture",
    "land_temperature",
    "humidity",
    "total_operating_hours",
    "total_downtime_hours",
    "average_utilization",
    "average_performance_score",
    "downtime_ratio",
    "blasting_delay_ratio",
    "equipment_downtime_ratio",
    "equipment_performance_risk",
    "rainfall_risk",
    "year",
    "month",
    "day",
    "day_of_week"
]


target_column = "actual_production"


X = data[feature_columns]

y = data[target_column]


print()
print("Input Features:", X.shape)

print("Target:", y.shape)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print()
print("Training Data:", X_train.shape)

print("Testing Data:", X_test.shape)


model = LinearRegression()


print()
print("Linear Regression Model Created Successfully!")


model.fit(
    X_train,
    y_train
)


print()
print("Model Training Completed Successfully!")


print()
print("===================================")
print("Step 5.3 Completed Successfully")
print("===================================")

print()
print("===================================")
print("Step 5.4 - Production Prediction")
print("===================================")


predictions = model.predict(X_test)


print()
print("Predicted Production:")

for prediction in predictions:
    print(round(prediction, 2))


print()
print("Actual Production:")

for actual in y_test:
    print(actual)


print()
print("===================================")
print("Prediction Completed Successfully")
print("===================================")

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


print()
print("===================================")
print("Step 5.5 - Model Evaluation")
print("===================================")


mae = mean_absolute_error(
    y_test,
    predictions
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)


r2 = r2_score(
    y_test,
    predictions
)


print()
print("MAE:", round(mae, 2))

print("RMSE:", round(rmse, 2))

print("R2 Score:", round(r2, 2))


print()
print("===================================")
print("Model Evaluation Completed Successfully")
print("===================================")