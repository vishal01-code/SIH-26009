import pandas as pd
import os


# Project root का path
project_root = os.path.dirname(os.path.dirname(__file__))

# Raw dataset का path
file_path = os.path.join(
    project_root,
    "data",
    "production_data.csv"
)

# Dataset load करना
data = pd.read_csv(file_path)

print("Dataset successfully loaded!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))
print()
print("Column Names:")
print(data.columns.tolist())
print()
print("First 5 Records:")
print(data.head())