import psycopg2
import pandas as pd


# PostgreSQL से connection
connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)

# PostgreSQL से production data पढ़ना
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

# SQL query को Pandas DataFrame में load करना
data = pd.read_sql_query(query, connection)

# Connection बंद करना
connection.close()


print("Data loaded from PostgreSQL successfully!")
print()
print("Rows:", len(data))
print("Columns:", len(data.columns))
print()
print(data)