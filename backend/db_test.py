import psycopg2


# PostgreSQL database से connection
connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345",
    port="5432"
)

print("Database connection successful!")

connection.close()

print("Database connection closed.")