import joblib

from backend.preprocessor import preprocess_input
from backend.predictor import predict_yield

from backend.intelligence.issue_detector import detect_issues
from backend.intelligence.risk_analyzer import analyze_risk
from backend.intelligence.recommender import generate_recommendations
from backend.intelligence.explainer import get_feature_contributions


# ================= LOAD ARTIFACTS (LOAD ONCE) =================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("column.pkl")


def run_pipeline(user_input_dict):
    """
    Main pipeline:
    Input → Preprocess → Predict → Analyze → Explain → Return structured output
    """

    # ================= STEP 1: PREPROCESS =================
    final_input_df = preprocess_input(user_input_dict, columns)

    # ================= STEP 2: PREDICT =================
    prediction = predict_yield(model, scaler, final_input_df)

    # ================= STEP 3: INTELLIGENCE =================
    issues = detect_issues(user_input_dict)
    risk = analyze_risk(prediction)
    recommendations = generate_recommendations(issues)

    # ================= STEP 4: EXPLAINABILITY =================
    contribution_df = get_feature_contributions(
        model=model,
        input_df=final_input_df,
        scaler=scaler,
        columns=final_input_df.columns
    )

    # ================= FINAL OUTPUT =================
    return {
        "prediction": float(prediction),   # ensure JSON-safe
        "risk": risk,
        "issues": issues,
        "recommendations": recommendations,
        "contributions": contribution_df
    }