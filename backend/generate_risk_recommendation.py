print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.6 - Risk Recommendation")
print("===================================")

# Current risk information
risk_score = 40
risk_level = "MEDIUM"

downtime_hours = 2
blasting_delay_hours = 1
rainfall_mm = 8

# -----------------------------------
# Detect Factors
# -----------------------------------

factors = []

if downtime_hours >= 2:
    factors.append("Equipment Downtime")

if blasting_delay_hours >= 1:
    factors.append("Blasting Delay")

if rainfall_mm > 5:
    factors.append("Rainfall")


# -----------------------------------
# Generate Recommendation
# -----------------------------------

recommendations = []

if downtime_hours >= 2:
    recommendations.append(
        "Inspect and maintain high-downtime equipment"
    )

if blasting_delay_hours >= 1:
    recommendations.append(
        "Optimize blasting schedule to reduce delays"
    )

if rainfall_mm > 5:
    recommendations.append(
        "Adjust mine operations according to weather conditions"
    )


# -----------------------------------
# Display Final Result
# -----------------------------------

print()
print("===================================")
print("RISK & RECOMMENDATION REPORT")
print("===================================")

print("Risk Score:", risk_score, "/ 100")
print("Risk Level:", risk_level)

print()
print("Detected Factors:")

for factor in factors:
    print("-", factor)

print()
print("Recommended Actions:")

for recommendation in recommendations:
    print("-", recommendation)

print()
print("===================================")
print("Step 6.6 Completed Successfully")
print("===================================")