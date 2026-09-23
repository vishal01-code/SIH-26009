import pandas as pd
import psycopg2


# -----------------------------------
# 1. CSV file load करना
# -----------------------------------

file_path = "../data/features/integrated_geological_satellite.csv"

df = pd.read_csv(file_path)

print("Total records found:", len(df))


# -----------------------------------
# 2. PostgreSQL से connection
# -----------------------------------

connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345"
)

cursor = connection.cursor()

print("Database connected successfully!")


# -----------------------------------
# 3. Database में data insert करना
# -----------------------------------

insert_query = """
INSERT INTO reserve_potential_predictions (
    mine_id,
    sample_code,
    prediction_date,
    geological_potential_score,
    environmental_context_score,
    integrated_potential_score,
    potential_class,
    latitude,
    longitude,
    model_version
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


for _, row in df.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["mine_id"]),
            row["sample_code"],
            row["sample_date"],
            float(row["geological_potential_score"]),
            float(row["environmental_context_score"]),
            float(row["integrated_potential_score"]),
            row["integrated_potential_class"],
            float(row["latitude_x"]),
            float(row["longitude_x"]),
            "prototype-v1"
        )
    )


# -----------------------------------
# 4. Changes save करना
# -----------------------------------

connection.commit()

print("Reserve potential data inserted successfully!")


# -----------------------------------
# 5. Connection close करना
# -----------------------------------

cursor.close()
connection.close()

print("Database connection closed.")