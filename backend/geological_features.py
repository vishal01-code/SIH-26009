import pandas as pd
import psycopg2


# ==========================================
# 1. PostgreSQL से Geological Data पढ़ना
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="sih_26009",
    user="postgres",
    password="Postgres@12345"
)

query = """
SELECT
    id,
    mine_id,
    sample_code,
    sample_date,
    depth_meters,
    manganese_grade,
    rock_type,
    latitude,
    longitude
FROM geological_samples
ORDER BY id;
"""

data = pd.read_sql(query, connection)

connection.close()


# ==========================================
# 2. Manganese Grade को Score में बदलना
# ==========================================

def calculate_grade_score(grade):

    if grade < 25:
        return 20

    elif grade < 35:
        return 40

    elif grade < 45:
        return 70

    else:
        return 100


data["grade_score"] = data["manganese_grade"].apply(
    calculate_grade_score
)


# ==========================================
# 3. Depth को Score में बदलना
# ==========================================

def calculate_depth_score(depth):

    if depth < 15:
        return 40

    elif depth < 25:
        return 60

    elif depth < 35:
        return 80

    else:
        return 100


data["depth_score"] = data["depth_meters"].apply(
    calculate_depth_score
)


# ==========================================
# 4. Rock Type को Score में बदलना
# ==========================================

def calculate_rock_score(rock_type):

    if rock_type == "Manganese Ore":
        return 100

    elif rock_type == "Quartzite":
        return 70

    elif rock_type == "Schist":
        return 50

    elif rock_type == "Laterite":
        return 30

    else:
        return 20


data["rock_score"] = data["rock_type"].apply(
    calculate_rock_score
)


# ==========================================
# 5. Geological Potential Score
# ==========================================

data["geological_potential_score"] = (
    data["grade_score"] * 0.50
    + data["depth_score"] * 0.25
    + data["rock_score"] * 0.25
)


# ==========================================
# 6. Geological Potential Classification
# ==========================================

def classify_potential(score):

    if score >= 75:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    else:
        return "LOW"


data["potential_class"] = data[
    "geological_potential_score"
].apply(
    classify_potential
)


# ==========================================
# 7. Geological Features देखना
# ==========================================

print("\nGeological Feature Engineering:")

print(
    data[
        [
            "sample_code",
            "manganese_grade",
            "grade_score",
            "depth_meters",
            "depth_score",
            "rock_type",
            "rock_score",
            "geological_potential_score",
            "potential_class"
        ]
    ]
)


# ==========================================
# 8. Feature Dataset Save करना
# ==========================================

output_path = "../data/features/geological_features.csv"

data.to_csv(
    output_path,
    index=False
)

print("\nGeological feature dataset created successfully!")
print(f"Saved to: {output_path}")