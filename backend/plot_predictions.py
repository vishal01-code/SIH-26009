import pandas as pd
import os
import matplotlib.pyplot as plt

print("===================================")
print("Phase 5 - Production Prediction")
print("Step 5.7.8 - Prediction Visualization")
print("===================================")

project_root = os.path.dirname(os.path.dirname(__file__))

input_file = os.path.join(
    project_root,
    "data",
    "processed",
    "production_predictions_comparison.csv"
)

output_folder = os.path.join(
    project_root,
    "data",
    "processed"
)

output_file = os.path.join(
    output_folder,
    "actual_vs_predicted.png"
)


# Load prediction comparison
data = pd.read_csv(input_file)

print()
print("Prediction Data Loaded!")

print("Rows:", len(data))


# Create day numbers
data["Day"] = range(1, len(data) + 1)


# Create graph
plt.figure(figsize=(12, 6))

plt.plot(
    data["Day"],
    data["Actual Production"],
    label="Actual Production",
    marker="o"
)

plt.plot(
    data["Day"],
    data["Predicted Production"],
    label="Predicted Production",
    marker="o"
)

plt.title(
    "Actual vs Predicted Production"
)

plt.xlabel("Testing Day")

plt.ylabel("Production")

plt.legend()

plt.grid(True)

plt.tight_layout()


# Save graph
plt.savefig(output_file)

plt.show()


print()
print("Graph Created Successfully!")

print()
print("Graph File:")
print(output_file)

print()
print("===================================")
print("Step 5.7.8 Completed Successfully")
print("===================================")