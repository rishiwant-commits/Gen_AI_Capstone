import streamlit as st
import numpy as np
import pandas as pd
import joblib

# ================= LOAD ARTIFACTS =================
model = joblib.load("trained_model.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")  # list of training columns

# ================= STREAMLIT UI =================
st.set_page_config(page_title="Smart Crop Yield Predictor", layout="centered")

st.title("🌾 Smart Crop Yield Prediction")
st.markdown(
    "Enter crop, soil, and environment details in **key=value** format separated by commas."
)

example_input = """N=90, P=40, K=40,
Soil_pH=6.5,
Soil_Moisture=25,
Organic_Carbon=0.8,
Temperature=25,
Humidity=80,
Rainfall=200,
Sunlight_Hours=8,
Wind_Speed=3,
Altitude=200,
Fertilizer_Used=120,
Pesticide_Used=30,
Soil_Type=Loamy,
Region=North,
Season=Kharif,
Crop_Type=Wheat,
Irrigation_Type=Drip
"""

user_input = st.text_area(
    "📥 Input Data",
    height=260,
    placeholder=example_input
)

# ================= HELPER FUNCTION =================
def parse_input(text):
    data = {}
    pairs = text.split(",")

    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=")
            data[key.strip()] = value.strip()

    return data

# ================= PREDICTION =================
if st.button("🔮 Predict Crop Yield"):
    try:
        parsed = parse_input(user_input)

        # Create empty row with all columns = 0
        input_df = pd.DataFrame(
            np.zeros((1, len(columns))),
            columns=columns
        )

        # Fill numeric values
        for key, value in parsed.items():
            if key in input_df.columns:
                input_df[key] = float(value)

        # Handle one-hot categorical columns
        categorical_prefixes = [
            "Soil_Type_", "Region_", "Season_", "Crop_Type_", "Irrigation_Type_"
        ]

        for key, value in parsed.items():
            col_name = f"{key}_{value}"
            if col_name in input_df.columns:
                input_df[col_name] = 1

        # Scale
        input_scaled = scaler.transform(input_df)

        # Predict
        prediction = model.predict(input_scaled)[0]

        # Output
        st.success(f"🌱 Predicted Crop Yield: **{prediction:.2f} ton/hectare**")

    except Exception as e:
        st.error("❌ Invalid input format. Please check values and try again.")
        st.exception(e)

# ================= FOOTER =================
st.markdown("---")
st.caption("ML Model: Random Forest Regressor | Dataset: Smart Crop Yield")