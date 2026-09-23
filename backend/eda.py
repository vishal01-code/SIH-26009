import pandas as pd
import os


# Project root directory
project_root = os.path.dirname(os.path.dirname(__file__))


# Final feature dataset का path
input_file = os.path.join(
    project_root,
    "data",
    "features",
    "final_feature_dataset.csv"
)


# Dataset load करना
data = pd.read_csv(input_file)


print("===================================")
print("EDA - Dataset Overview")
print("===================================")

print()
print("Dataset successfully loaded!")

print()
print("Rows:", len(data))
print("Columns:", len(data.columns))


# Column names
print()
print("Column Names:")
print(data.columns.tolist())


# Data types
print()
print("Data Types:")
print(data.dtypes)


# Statistical Summary
print()
print("Statistical Summary:")
print(data.describe())


# Step 9.2: Production Analysis

print()
print("===================================")
print("Production Analysis")
print("===================================")


# Average Planned Production
average_planned = data["planned_production"].mean()

# Average Actual Production
average_actual = data["actual_production"].mean()

# Total Production Gap
total_gap = data["production_gap"].sum()

# Average Production Gap
average_gap = data["production_gap"].mean()


print()
print("Average Planned Production:", average_planned)
print("Average Actual Production:", average_actual)
print("Total Production Gap:", total_gap)
print("Average Production Gap:", average_gap)


# Minimum Production
minimum_production = data["actual_production"].min()

# Maximum Production
maximum_production = data["actual_production"].max()


print()
print("Minimum Actual Production:", minimum_production)
print("Maximum Actual Production:", maximum_production)


# Day with minimum production
minimum_day = data.loc[
    data["actual_production"].idxmin(),
    "production_date"
]

# Day with maximum production
maximum_day = data.loc[
    data["actual_production"].idxmax(),
    "production_date"
]


print()
print("Lowest Production Date:", minimum_day)
print("Highest Production Date:", maximum_day)


# Step 9.3: Production Gap vs Downtime Analysis

print()
print("===================================")
print("Production Gap vs Downtime Analysis")
print("===================================")


# Production Gap और Downtime Ratio का correlation
downtime_correlation = data[
    "production_gap"
].corr(
    data["downtime_ratio"]
)


print()
print(
    "Correlation between Production Gap and Downtime Ratio:",
    round(downtime_correlation, 3)
)


# Important columns को एक साथ display करना
print()
print("Production Gap and Downtime Details:")

print(
    data[
        [
            "production_date",
            "actual_production",
            "production_gap",
            "downtime_hours",
            "downtime_ratio"
        ]
    ]
)


# Highest production gap वाले records
print()
print("Highest Production Gap Records:")

highest_gap = data.sort_values(
    by="production_gap",
    ascending=False
)

print(
    highest_gap[
        [
            "production_date",
            "production_gap",
            "downtime_hours",
            "downtime_ratio"
        ]
    ].head(5)
)


# Step 9.4: Production vs Weather Analysis

print()
print("===================================")
print("Production vs Weather Analysis")
print("===================================")


# Rainfall और Production Gap का correlation
rainfall_correlation = data[
    "production_gap"
].corr(
    data["rainfall_mm"]
)


print()
print(
    "Correlation between Production Gap and Rainfall:",
    round(rainfall_correlation, 3)
)


# Rainfall Risk और Production Gap का correlation
rainfall_risk_correlation = data[
    "production_gap"
].corr(
    data["rainfall_risk"]
)


print()
print(
    "Correlation between Production Gap and Rainfall Risk:",
    round(rainfall_risk_correlation, 3)
)


# Weather और Production की details
print()
print("Weather and Production Details:")

print(
    data[
        [
            "production_date",
            "actual_production",
            "production_gap",
            "rainfall_mm",
            "soil_moisture",
            "humidity",
            "rainfall_risk"
        ]
    ]
)


# Highest rainfall records
print()
print("Highest Rainfall Records:")

highest_rainfall = data.sort_values(
    by="rainfall_mm",
    ascending=False
)

print(
    highest_rainfall[
        [
            "production_date",
            "rainfall_mm",
            "rainfall_risk",
            "actual_production",
            "production_gap"
        ]
    ].head(5)
)


# Step 9.5: Blasting Delay + Equipment Performance Analysis

print()
print("===================================")
print("Blasting Delay + Equipment Performance Analysis")
print("===================================")


# Blasting Delay और Production Gap का correlation
blasting_correlation = data[
    "production_gap"
].corr(
    data["blasting_delay_ratio"]
)


print()
print(
    "Correlation between Production Gap and Blasting Delay:",
    round(blasting_correlation, 3)
)


# Equipment Performance Risk और Production Gap का correlation
equipment_risk_correlation = data[
    "production_gap"
].corr(
    data["equipment_performance_risk"]
)


print()
print(
    "Correlation between Production Gap and Equipment Performance Risk:",
    round(equipment_risk_correlation, 3)
)


# Important operational factors
print()
print("Operational Factors and Production:")

print(
    data[
        [
            "production_date",
            "actual_production",
            "production_gap",
            "blasting_delay_hours",
            "blasting_delay_ratio",
            "average_performance_score",
            "equipment_performance_risk"
        ]
    ]
)


# Highest blasting delay records
print()
print("Highest Blasting Delay Records:")

highest_blasting_delay = data.sort_values(
    by="blasting_delay_hours",
    ascending=False
)

print(
    highest_blasting_delay[
        [
            "production_date",
            "blasting_delay_hours",
            "production_gap",
            "actual_production"
        ]
    ].head(5)
)


# Highest equipment risk records
print()
print("Highest Equipment Risk Records:")

highest_equipment_risk = data.sort_values(
    by="equipment_performance_risk",
    ascending=False
)

print(
    highest_equipment_risk[
        [
            "production_date",
            "equipment_performance_risk",
            "production_gap",
            "actual_production"
        ]
    ].head(5)
)


# Step 9.6: Overall EDA Correlation Analysis

print()
print("===================================")
print("Overall EDA Correlation Analysis")
print("===================================")


# Important features
important_features = [
    "production_gap",
    "downtime_ratio",
    "blasting_delay_ratio",
    "equipment_downtime_ratio",
    "equipment_performance_risk",
    "rainfall_mm",
    "rainfall_risk",
    "soil_moisture",
    "humidity",
    "average_utilization",
    "average_performance_score"
]


# Correlation Matrix
correlation_matrix = data[
    important_features
].corr()


print()
print("Correlation Matrix:")

print(
    correlation_matrix.round(3)
)


# Production Gap के साथ correlation
production_gap_correlation = (
    correlation_matrix["production_gap"]
    .drop("production_gap")
    .sort_values(
        ascending=False
    )
)


print()
print("Features Correlated with Production Gap:")
print(
    production_gap_correlation.round(3)
)


# Strongest factors
print()
print("Strongest Factors Affecting Production Gap:")

print(
    production_gap_correlation.head(5).round(3)
)