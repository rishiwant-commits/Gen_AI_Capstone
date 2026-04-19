def analyze_risk(prediction):
    if prediction < 2:
        return "High Risk"
    elif prediction < 4:
        return "Moderate Risk"
    else:
        return "Low Risk"