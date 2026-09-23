import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. Integrated Dataset पढ़ना
# ==========================================

input_path = (
    "../data/features/"
    "integrated_geological_satellite.csv"
)

data = pd.read_csv(input_path)


# ==========================================
# 2. Potential Class के अनुसार Data
# ==========================================

high = data[
    data["integrated_potential_class"] == "HIGH"
]

medium = data[
    data["integrated_potential_class"] == "MEDIUM"
]

low = data[
    data["integrated_potential_class"] == "LOW"
]


# ==========================================
# 3. Potential Map बनाना
# ==========================================

plt.figure(figsize=(10, 8))


# HIGH Potential
plt.scatter(
    high["longitude_x"],
    high["latitude_x"],
    s=120,
    label="HIGH Potential"
)


# MEDIUM Potential
plt.scatter(
    medium["longitude_x"],
    medium["latitude_x"],
    s=100,
    label="MEDIUM Potential"
)


# LOW Potential
plt.scatter(
    low["longitude_x"],
    low["latitude_x"],
    s=100,
    label="LOW Potential"
)


# ==========================================
# 4. Sample Labels
# ==========================================

for _, row in data.iterrows():

    plt.annotate(
        row["sample_code"],
        (
            row["longitude_x"],
            row["latitude_x"]
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )


# ==========================================
# 5. Labels और Title
# ==========================================

plt.xlabel("Longitude")

plt.ylabel("Latitude")

plt.title(
    "Manganese Reserve Potential Map"
)

plt.legend()

plt.grid(True)


# ==========================================
# 6. Map Save करना
# ==========================================

output_path = (
    "../data/features/"
    "manganese_potential_map.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ==========================================
# 7. Summary
# ==========================================

print("\nPotential Map Generated Successfully!")

print(
    f"HIGH Potential Zones: {len(high)}"
)

print(
    f"MEDIUM Potential Zones: {len(medium)}"
)

print(
    f"LOW Potential Zones: {len(low)}"
)

print(
    f"Map saved to: {output_path}"
)