
# ============================================
# SIH 26009 - Recommendation Engine
# Phase 9
# ============================================


# ============================================
# 1. Calculate Recommendation Priority
# ============================================

def calculate_priority(cause, risk_score):

    if cause in [
        "Production Shortfall",
        "Equipment Downtime"
    ] and risk_score >= 30:

        return "HIGH"

    elif cause in [
        "Blasting Delay",
        "Rainfall",
        "Low Equipment Performance",
        "Low Equipment Utilization"
    ]:

        return "MEDIUM"

    else:

        return "LOW"


# ============================================
# 2. Calculate Risk Level
# ============================================

def calculate_risk_level(risk_score):

    if risk_score >= 60:

        return "HIGH"

    elif risk_score >= 30:

        return "MEDIUM"

    else:

        return "LOW"


# ============================================
# 3. Calculate Expected Impact
# ============================================

def calculate_expected_impact(
    cause,
    shortfall,
    downtime_hours,
    blasting_delay_hours
):

    # No shortfall means no recovery is required.

    if shortfall <= 0:

        return 0.0


    # Production Schedule Adjustment

    if cause == "Production Shortfall":

        impact = shortfall * 0.20


    # Equipment Downtime

    elif cause == "Equipment Downtime":

        impact = downtime_hours * 20


    # Blasting Delay

    elif cause == "Blasting Delay":

        impact = blasting_delay_hours * 20


    # Equipment Performance

    elif cause == "Low Equipment Performance":

        impact = shortfall * 0.15


    # Equipment Utilization

    elif cause == "Low Equipment Utilization":

        impact = shortfall * 0.10


    # Rainfall

    elif cause == "Rainfall":

        impact = shortfall * 0.10


    # Default

    else:

        impact = 0


    # Do not allow one recommendation
    # to claim more recovery than the
    # actual shortfall.

    impact = min(impact, shortfall)


    return round(impact, 2)


# ============================================
# 4. Generate Recommendation
# ============================================

def generate_recommendation(
    risk_score,
    shortfall,
    downtime_hours,
    blasting_delay_hours,
    rainfall,
    equipment_performance,
    equipment_utilization
):

    recommendations = []

    causes = []


    # ========================================
    # 4.1 Identify Causes
    # ========================================

    if downtime_hours >= 2:

        causes.append("Equipment Downtime")


    if blasting_delay_hours >= 1:

        causes.append("Blasting Delay")


    if rainfall > 5:

        causes.append("Rainfall")


    if equipment_performance < 80:

        causes.append("Low Equipment Performance")


    if equipment_utilization < 85:

        causes.append("Low Equipment Utilization")


    # ========================================
    # 4.2 Identify Primary Cause
    # ========================================

    if downtime_hours >= 2:

        primary_cause = "Equipment Downtime"

    elif blasting_delay_hours >= 1:

        primary_cause = "Blasting Delay"

    elif rainfall > 5:

        primary_cause = "Rainfall"

    elif equipment_performance < 80:

        primary_cause = "Low Equipment Performance"

    elif equipment_utilization < 85:

        primary_cause = "Low Equipment Utilization"

    else:

        primary_cause = "No Major Cause Detected"


    # ========================================
    # 4.3 Risk Level
    # ========================================

    risk_level = calculate_risk_level(risk_score)


    # ========================================
    # 4.4 Production Recommendation
    # ========================================

    if shortfall > 0:

        cause = "Production Shortfall"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Production",

            "cause": cause,

            "reason":
                "Predicted production is below the planned production target.",

            "action":
                "Adjust mine production schedule to reduce the predicted shortfall.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.5 Equipment Downtime
    # ========================================

    if downtime_hours >= 2:

        cause = "Equipment Downtime"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Equipment",

            "cause": cause,

            "reason":
                "High equipment downtime may reduce available operating capacity.",

            "action":
                "Inspect high-downtime equipment and perform preventive maintenance.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.6 Equipment Performance
    # ========================================

    if equipment_performance < 80:

        cause = "Low Equipment Performance"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Equipment",

            "cause": cause,

            "reason":
                "Low performance score indicates reduced equipment effectiveness.",

            "action":
                "Perform equipment performance diagnostics and maintenance.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.7 Equipment Utilization
    # ========================================

    if equipment_utilization < 85:

        cause = "Low Equipment Utilization"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Equipment",

            "cause": cause,

            "reason":
                "Low utilization indicates that equipment capacity may not be fully utilized.",

            "action":
                "Optimize equipment deployment and operating schedule.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.8 Blasting Delay
    # ========================================

    if blasting_delay_hours >= 1:

        cause = "Blasting Delay"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Blasting",

            "cause": cause,

            "reason":
                "Blasting delays can reduce available production operating time.",

            "action":
                "Optimize blasting schedule to reduce operational delays.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.9 Weather
    # ========================================

    if rainfall > 5:

        cause = "Rainfall"

        impact = calculate_expected_impact(
            cause,
            shortfall,
            downtime_hours,
            blasting_delay_hours
        )

        recommendations.append({

            "type": "Weather",

            "cause": cause,

            "reason":
                "Rainfall may affect mining operations and production continuity.",

            "action":
                "Adjust mine operations according to weather conditions.",

            "priority":
                calculate_priority(cause, risk_score),

            "expected_impact":
                impact

        })


    # ========================================
    # 4.10 Final Result
    # ========================================

    return {

        "risk_score": risk_score,

        "risk_level": risk_level,

        "primary_cause": primary_cause,

        "causes": causes,

        "recommendations": recommendations

    }


# ============================================
# 5. What-if Simulation
# ============================================

def simulate_downtime_reduction(
    predicted_production,
    planned_production,
    downtime_hours,
    reduction_percent
):

    # ----------------------------------------
    # Calculate downtime reduction
    # ----------------------------------------

    downtime_reduction = (
        downtime_hours * reduction_percent / 100
    )


    # ----------------------------------------
    # Calculate new downtime
    # ----------------------------------------

    new_downtime = (
        downtime_hours - downtime_reduction
    )


    # ----------------------------------------
    # Estimate production recovery
    # ----------------------------------------
    #
    # Prototype assumption:
    #
    # 1 hour reduction in downtime
    # = approximately 20 tonnes
    # potential production recovery.
    #
    # This is an illustrative prototype
    # assumption and must be calibrated
    # using real operational data later.
    #
    # ----------------------------------------

    recovery = downtime_reduction * 20


    # ----------------------------------------
    # Calculate new production
    # ----------------------------------------

    new_production = (
        predicted_production + recovery
    )


    # ----------------------------------------
    # Production cannot exceed plan
    # ----------------------------------------

    new_production = min(
        new_production,
        planned_production
    )


    # ----------------------------------------
    # Calculate new shortfall
    # ----------------------------------------

    new_shortfall = (
        planned_production - new_production
    )


    # ----------------------------------------
    # Final simulation result
    # ----------------------------------------

    return {

        "current_production":
            round(predicted_production, 2),

        "planned_production":
            round(planned_production, 2),

        "current_shortfall":
            round(
                planned_production - predicted_production,
                2
            ),

        "current_downtime":
            round(downtime_hours, 2),

        "reduction_percent":
            reduction_percent,

        "downtime_reduction":
            round(downtime_reduction, 2),

        "new_downtime":
            round(new_downtime, 2),

        "estimated_recovery":
            round(recovery, 2),

        "new_production":
            round(new_production, 2),

        "new_shortfall":
            round(new_shortfall, 2)

    }


# ============================================
# 6. Recommendation Engine Test
# ============================================

result = generate_recommendation(

    risk_score=40,

    shortfall=3.89,

    downtime_hours=2.5,

    blasting_delay_hours=1.2,

    rainfall=12,

    equipment_performance=78,

    equipment_utilization=84

)


# ============================================
# 7. Display Recommendation Result
# ============================================

print("\n========================================")

print("       RECOMMENDATION ENGINE")

print("========================================")


print("\nRisk Score:")

print(result["risk_score"])


print("\nRisk Level:")

print(result["risk_level"])


print("\nPrimary Cause:")

print(result["primary_cause"])


print("\nAll Causes:")

for cause in result["causes"]:

    print("-", cause)


print("\nRecommendations:")


for recommendation in result["recommendations"]:

    print("\n----------------------------------------")

    print("Type:",
          recommendation["type"])

    print("Cause:",
          recommendation["cause"])

    print("Reason:",
          recommendation["reason"])

    print("Action:",
          recommendation["action"])

    print("Priority:",
          recommendation["priority"])

    print("Expected Impact:",
          recommendation["expected_impact"],
          "tonnes")


# ============================================
# 8. What-if Test
# ============================================

what_if = simulate_downtime_reduction(

    predicted_production=496.11,

    planned_production=500,

    downtime_hours=2.5,

    reduction_percent=30

)


print("\n========================================")

print("        WHAT-IF SIMULATION")

print("========================================")


print("\nCurrent Production:",
      what_if["current_production"],
      "tonnes")


print("Planned Production:",
      what_if["planned_production"],
      "tonnes")


print("Current Shortfall:",
      what_if["current_shortfall"],
      "tonnes")


print("\nCurrent Downtime:",
      what_if["current_downtime"],
      "hours")


print("Downtime Reduction:",
      what_if["reduction_percent"],
      "%")


print("Downtime Reduced By:",
      what_if["downtime_reduction"],
      "hours")


print("New Downtime:",
      what_if["new_downtime"],
      "hours")


print("\nEstimated Production Recovery:",
      what_if["estimated_recovery"],
      "tonnes")


print("New Predicted Production:",
      what_if["new_production"],
      "tonnes")


print("Remaining Shortfall:",
      what_if["new_shortfall"],
      "tonnes")


print("\n========================================")

print("Recommendation and What-if testing completed.")

print("========================================")

