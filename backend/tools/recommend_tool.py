def recommend_tool(state):
    mapping = {
        "nitrogen":      ("Apply urea fertilizer to boost nitrogen levels", "high"),
        "phosphorus":    ("Apply DAP fertilizer to improve phosphorus content", "high"),
        "potassium":     ("Use potash fertilizers to restore potassium levels", "medium"),
        "rainfall":      ("Install drip or sprinkler irrigation system", "medium"),
        "soil_fertility": ("Add compost or organic manure to improve soil fertility", "medium"),
        "soil_acidic":   ("Apply lime to raise soil pH to optimal range", "medium"),
        "soil_alkaline": ("Use gypsum or sulfur to lower soil pH", "medium"),
        "heat_stress":   ("Switch to heat-resistant crop varieties and increase irrigation", "high"),
    }

    recs = []
    for issue in state["issues"]:
        entry = mapping.get(issue["type"])
        if entry:
            recs.append({
                "action": entry[0],
                "priority": issue["severity"]
            })

    state["recommendations"] = recs
    return state
