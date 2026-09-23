print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.2 - Risk Classification")
print("===================================")

# Shortfall percentage
shortfall_percentage = 0.78

# Risk classification
if shortfall_percentage <= 5:
    risk_level = "LOW"

elif shortfall_percentage <= 10:
    risk_level = "MEDIUM"

else:
    risk_level = "HIGH"

print()
print("Shortfall Percentage:", shortfall_percentage, "%")
print("Risk Level:", risk_level)

print()
print("===================================")
print("Step 6.2 Completed Successfully")
print("===================================")