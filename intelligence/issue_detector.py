def detect_issues(input_data):
    issues = []

    # --- Soil pH ---
    if input_data["Soil_pH"] < 5.5:
        issues.append("Soil is too acidic")
    elif input_data["Soil_pH"] > 7.5:
        issues.append("Soil is too alkaline")

    # --- Organic Carbon ---
    if input_data["Organic_Carbon"] < 0.5:
        issues.append("Low organic carbon (poor soil fertility)")

    # --- Nutrients ---
    if input_data["N"] < 50:
        issues.append("Low Nitrogen")
    if input_data["P"] < 40:
        issues.append("Low Phosphorus")
    if input_data["K"] < 40:
        issues.append("Low Potassium")

    # --- Climate ---
    if input_data["Rainfall"] < 500:
        issues.append("Insufficient rainfall")
    if input_data["Temperature"] > 38:
        issues.append("Temperature too high")

    return issues