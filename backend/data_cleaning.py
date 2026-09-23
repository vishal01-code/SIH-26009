import pandas as pd
import psycopg2
import os


# PostgreSQL से connection
connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)


# Production data की SQL query
query = """
SELECT
    production_date,
    mine_id,
    planned_production,
    actual_production,
    operating_hours,
    downtime_hours,
    blasting_delay_hours
FROM production_records
ORDER BY production_date;
"""


# Database से data Pandas DataFrame में load करना
data = pd.read_sql_query(query, connection)

connection.close()


# Missing values की जानकारी
print("Missing Values Analysis")
print("-----------------------")

print(data.isnull().sum())



# Duplicate records की जाँच
print()
print("Duplicate Records Analysis")
print("---------------------------")

duplicate_count = data.duplicated().sum()

print("Duplicate Records:", duplicate_count)


# Invalid Values की जाँच
print()
print("Invalid Values Analysis")
print("-----------------------")

print("Negative Planned Production:",
      (data["planned_production"] < 0).sum())

print("Negative Actual Production:",
      (data["actual_production"] < 0).sum())

print("Negative Operating Hours:",
      (data["operating_hours"] < 0).sum())

print("Negative Downtime Hours:",
      (data["downtime_hours"] < 0).sum())

print("Negative Blasting Delay Hours:",
      (data["blasting_delay_hours"] < 0).sum())


# Logical Consistency Check
print()
print("Logical Consistency Check")
print("-------------------------")

# Downtime operating hours से ज्यादा नहीं होना चाहिए
invalid_downtime = (
    data["downtime_hours"] > data["operating_hours"]
).sum()

print("Downtime > Operating Hours:", invalid_downtime)

# Actual production planned production से बहुत अधिक तो नहीं
invalid_production = (
    data["actual_production"] > data["planned_production"] * 1.5
).sum()

print("Unusually High Production:", invalid_production)

project_root = os.path.dirname(os.path.dirname(__file__))

# Project root का path
project_root = os.path.dirname(os.path.dirname(__file__))


# Cleaned dataset को processed folder में save करना
processed_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

os.makedirs(processed_folder, exist_ok=True)

output_file = os.path.join(
    processed_folder,
    "cleaned_production_data.csv"
)

data.to_csv(output_file, index=False)

print()
print("Cleaned dataset saved successfully!")
print("File:", output_file)


# Missing और Invalid Values को Handle करना
print()
print("Data Cleaning Rules")
print("-------------------")

# Numeric columns
numeric_columns = [
    "planned_production",
    "actual_production",
    "operating_hours",
    "downtime_hours",
    "blasting_delay_hours"
]

# Missing numeric values को median से भरना
for column in numeric_columns:
    if data[column].isnull().any():
        data[column] = data[column].fillna(data[column].median())

# Negative values को 0 से replace करना
for column in numeric_columns:
    data.loc[data[column] < 0, column] = 0

print("Missing values handled successfully.")
print("Invalid negative values handled successfully.")

print()
print("Final Missing Values:")
print(data.isnull().sum())