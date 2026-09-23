print("===================================")
print("Phase 6 - Production Shortfall & Risk")
print("Step 6.3 - Shortfall Reason Analysis")
print("===================================")

# Current production factors
downtime_hours = 2
blasting_delay_hours = 1
rainfall_mm = 8

# Analyze the reasons
reasons = []

if downtime_hours >= 2:
    reasons.append("Equipment Downtime")

if blasting_delay_hours >= 1:
    reasons.append("Blasting Delay")

if rainfall_mm > 5:
    reasons.append("Rainfall")

print()
print("Detected Factors:")

if reasons:
    for reason in reasons:
        print("-", reason)

else:
    print("- No Major Risk Factor")

print()
print("Primary Reason:")

if downtime_hours >= 2:
    print("Equipment Downtime")

elif blasting_delay_hours >= 1:
    print("Blasting Delay")

elif rainfall_mm > 5:
    print("Rainfall")

else:
    print("No Major Risk Factor")

print()
print("===================================")
print("Step 6.3 Completed Successfully")
print("===================================")