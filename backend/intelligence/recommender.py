def generate_recommendations(issues):
    recommendations = []

    for issue in issues:
        if "acidic" in issue:
            recommendations.append("Add lime to increase soil pH")

        elif "alkaline" in issue:
            recommendations.append("Use gypsum to reduce soil pH")

        elif "Nitrogen" in issue:
            recommendations.append("Increase nitrogen fertilizer (urea)")

        elif "Phosphorus" in issue:
            recommendations.append("Apply DAP fertilizer")

        elif "Potassium" in issue:
            recommendations.append("Use potash fertilizers")

        elif "rainfall" in issue:
            recommendations.append("Use irrigation methods like drip or sprinkler")

        elif "Temperature" in issue:
            recommendations.append("Use heat-resistant crop varieties")

        elif "organic carbon" in issue:
            recommendations.append("Add compost or organic manure")

    return recommendations