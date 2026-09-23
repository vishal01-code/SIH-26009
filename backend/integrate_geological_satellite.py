import pandas as pd


# ==========================================
# 1. Geological Features पढ़ना
# ==========================================

geological_path = "../data/features/geological_features.csv"

geological_data = pd.read_csv(
    geological_path
)


# ==========================================
# 2. Satellite Features पढ़ना
# ==========================================

satellite_path = "../data/features/satellite_features.csv"

satellite_data = pd.read_csv(
    satellite_path
)


# ==========================================
# 3. Date को datetime में बदलना
# ==========================================

geological_data["sample_date"] = pd.to_datetime(
    geological_data["sample_date"]
)

satellite_data["observation_date"] = pd.to_datetime(
    satellite_data["observation_date"]
)


# ==========================================
# 4. Location + Date के आधार पर
#    सबसे नज़दीकी Satellite Observation
#    ढूँढना
# ==========================================

geological_data = geological_data.sort_values(
    "sample_date"
)

satellite_data = satellite_data.sort_values(
    "observation_date"
)


integrated_data = pd.merge_asof(
    geological_data,
    satellite_data,
    left_on="sample_date",
    right_on="observation_date",
    by="mine_id",
    direction="nearest"
)


# ==========================================
# 5. Integrated Potential Score
# ==========================================

integrated_data["integrated_potential_score"] = (
    integrated_data["geological_potential_score"] * 0.70
    + integrated_data["environmental_context_score"] * 0.30
)


# ==========================================
# 6. Integrated Potential Classification
# ==========================================

def classify_integrated_potential(score):

    if score >= 75:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    else:
        return "LOW"


integrated_data["integrated_potential_class"] = (
    integrated_data[
        "integrated_potential_score"
    ].apply(
        classify_integrated_potential
    )
)


# ==========================================
# 7. Important Results देखना
# ==========================================

print("\nGeological + Satellite Integrated Data:")

print(
    integrated_data[
        [
            "sample_code",
            "manganese_grade",
            "geological_potential_score",
            "ndvi",
            "soil_moisture",
            "land_surface_temperature",
            "cloud_cover",
            "environmental_context_score",
            "integrated_potential_score",
            "integrated_potential_class"
        ]
    ]
)


# ==========================================
# 8. Integrated Dataset Save करना
# ==========================================

output_path = (
    "../data/features/"
    "integrated_geological_satellite.csv"
)

integrated_data.to_csv(
    output_path,
    index=False
)


# ==========================================
# 9. Summary
# ==========================================

print(
    "\nIntegrated dataset created successfully!"
)

print(
    f"Total records: {len(integrated_data)}"
)

print(
    f"Saved to: {output_path}"
)