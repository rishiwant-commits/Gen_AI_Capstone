def analyze_risk(prediction):
    if prediction < 2:
        return "High"
    elif prediction < 4:
        return "Moderate"
    else:
        return "Low"
