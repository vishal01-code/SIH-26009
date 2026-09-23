import pandas as pd
import os

file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "production_data.csv"
)

data = pd.read_csv(file_path)

print(data)