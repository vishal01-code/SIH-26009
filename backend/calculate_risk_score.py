print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.5 - Risk Score Calculation")
print("===================================")

# Current values
shortfall_percentage = 0.78
downtime_hours = 2
blasting_delay_hours = 1
rainfall_mm = 8

# -----------------------------------
# Shortfall Risk Score
# -----------------------------------

if shortfall_percentage <= 5:
    shortfall_score = 10

elif shortfall_percentage <= 10:
    shortfall_score = 30

else:
    shortfall_score = 50


# -----------------------------------
# Equipment Downtime Score
# -----------------------------------

if downtime_hours < 2:
    downtime_score = 5

elif downtime_hours <= 4:
    downtime_score = 15

else:
    downtime_score = 25


# -----------------------------------
# Blasting Delay Score
# -----------------------------------

if blasting_delay_hours < 1:
    blasting_score = 5

elif blasting_delay_hours <= 2:
    blasting_score = 10

else:
    blasting_score = 15


# -----------------------------------
# Rainfall Score
# -----------------------------------

if rainfall_mm <= 5:
    rainfall_score = 2

elif rainfall_mm <= 15:
    rainfall_score = 5

else:
    rainfall_score = 10


# -----------------------------------
# Total Risk Score
# -----------------------------------

risk_score = (
    shortfall_score
    + downtime_score
    + blasting_score
    + rainfall_score
)

# Maximum score = 100
if risk_score > 100:
    risk_score = 100


# -----------------------------------
# Risk Level
# -----------------------------------

if risk_score <= 30:
    risk_level = "LOW"

elif risk_score <= 60:
    risk_level = "MEDIUM"

else:
    risk_level = "HIGH"


# -----------------------------------
# Display Result
# -----------------------------------

print()
print("===================================")
print("RISK SCORE ANALYSIS")
print("===================================")

print(
    "Shortfall Score:",
    shortfall_score
)

print(
    "Equipment Downtime Score:",
    downtime_score
)

print(
    "Blasting Delay Score:",
    blasting_score
)

print(
    "Rainfall Score:",
    rainfall_score
)

print()
print(
    "Total Risk Score:",
    risk_score,
    "/ 100"
)

print(
    "Risk Level:",
    risk_level
)

print()
print("===================================")
print("Step 6.5 Completed Successfully")
print("===================================")