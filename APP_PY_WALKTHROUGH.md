# `app.py` walkthrough (Smart Crop Yield Predictor)

This document explains the **important blocks** in `app.py` and how the app flows from **frontend inputs** → **model** → **prediction output**.

## Big picture flow

- **App starts** → loads ML artifacts (`model.pkl`, `scaler.pkl`, `column.pkl`)
- **Renders UI** (language toggle, hero header, input form)
- **User fills form** (Streamlit widgets) and clicks **Predict**
- App **builds a single-row feature vector** (DataFrame aligned to `column.pkl`)
- App **scales** it using the trained scaler and **predicts** using the trained model
- App **renders results** (yield + confidence + summary chips + metrics)

The prediction pipeline is fully inside `app.py` (no separate backend service). Streamlit runs Python directly and serves the UI.

---

## 1) Imports and static UI assets (icons)

At the top, the app imports Streamlit + ML/data libraries and defines a dictionary of SVG icons used in the UI.

```1:52:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time
import base64

# ================= LUCIDE SVG ICONS =================
LUCIDE_ICONS = {
    'agriculture': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M4 6l10-4 10 4M4 6v11c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V6M4 6l10 5 10-5M8 10v8M12 10v8M16 10v8"/></svg>''',
    'cpu': '''<svg class="lucide-icon" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/>
...
}

def lucide_icon(name: str, size_class: str = "md") -> str:
    """Generate a Lucide SVG icon HTML string"""
    svg = LUCIDE_ICONS.get(name, LUCIDE_ICONS['agriculture'])
    return f'<span class="lucide-icon {size_class}">{svg}</span>'
```

**Why it matters**

- This block is purely **UI polish**. It doesn’t affect model behavior.

---

## 2) Loading the ML artifacts (model, scaler, columns)

This is where the trained objects are loaded from disk.

```53:56:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= LOAD ARTIFACTS =================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("column.pkl")
```

**What each file is used for**

- **`model.pkl`**: the trained `RandomForestRegressor` (predicts yield)
- **`scaler.pkl`**: the trained `StandardScaler` (normalizes features before prediction)
- **`column.pkl`**: the **expected feature column names/order**. This is critical because your model expects features in the same layout as training time.

---

## 3) Page setup + language state

Streamlit configures the page and initializes the selected language (English/Hindi) in session state.

```58:69:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Crop Yield Predictor | स्मार्ट फसल उपज भविष्यवक्ता",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= SESSION STATE FOR LANGUAGE =================
if 'language' not in st.session_state:
    st.session_state.language = 'en'
```

**How language persists**

- `st.session_state.language` survives reruns within the same browser session.

---

## 4) Translations + helper `t(key)`

Translations live in a dictionary, and `t(key)` returns the string for the current language.

```70:163:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= TRANSLATIONS =================
translations = {
    'en': {
        'title': 'Smart Crop Yield Predictor',
        'subtitle': 'Predict your crop yield with AI-powered precision',
        ...
    },
    'hi': {
        'title': 'स्मार्ट फसल उपज भविष्यवक्ता',
        ...
    }
}

def t(key):
    """Translation helper function"""
    return translations[st.session_state.language].get(key, key)
```

**Where it’s used**

- UI labels like `t('title')`, `t('predict_btn')`, etc.

---

## 5) Background/logo images (base64) + CSS

The app optionally reads `farmer.jpeg` and `image.png`, converts them to base64, and injects custom CSS into the Streamlit page.

```164:222:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
def get_base64_image(image_path):
    """Convert image to base64 for CSS background"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Load background image
bg_image = get_base64_image("farmer.jpeg")
logo_image = get_base64_image("image.png")

# ================= CUSTOM CSS =================
if bg_image:
    st.markdown(f"""
    <style>
        /* Background Image with Overlay */
        .stApp {{
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.42), rgba(255, 255, 255, 0.42)),
                url("data:image/jpeg;base64,{bg_image}");
...
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
...
    """, unsafe_allow_html=True)
```

**Why it matters**

- Purely frontend styling. No effect on predictions.

---

## 6) Frontend: language toggle buttons

This is the top-right “English / हिंदी” toggle. Clicking a button sets session state and triggers `st.rerun()` (Streamlit reruns the script to re-render UI in the new language).

```967:981:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= HEADER =================
# Language Toggle - Top Right Corner
col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

with col4:
    col_en, col_hi = st.columns(2)
    with col_en:
        if st.button("English", key="en_btn"):
            st.session_state.language = 'en'
            st.rerun()
    with col_hi:
        if st.button("हिंदी", key="hi_btn"):
            st.session_state.language = 'hi'
            st.rerun()
```

---

## 7) Frontend: hero header (title + badges)

This uses HTML/CSS to create a hero section and show the logo.

```982:995:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# Title and Logo
logo_html = f'<img src="data:image/png;base64,{logo_image}" style="width: 48px; height: 48px; object-fit: contain;">' if logo_image else lucide_icon('sprout', 'lg')
st.markdown(f"""
<div class="hero-section">
    <h1 style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        {logo_html} {t('title')}
    </h1>
    <p class="subtitle">{t("subtitle")}</p>
    <div class="cta-buttons-container">
        <span class="ai-badge">{t('ai_badge')}</span>
        <span class="ai-badge">{t('ml_badge')}</span>
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## 8) Frontend: the input form (where inputs come from)

All user inputs are created inside a Streamlit form:

```1000:1123:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= INPUT FORM =================
with st.form("prediction_form"):
    # Soil Nutrients Section
    ...
    N = st.number_input("N (kg/ha)", min_value=0.0, max_value=200.0, value=97.0, step=1.0, 
                       help=t('tooltip_n'), label_visibility="collapsed")
    P = st.number_input("P (kg/ha)", min_value=0.0, max_value=200.0, value=20.0, step=1.0,
                       help=t('tooltip_p'), label_visibility="collapsed")
    K = st.number_input("K (kg/ha)", min_value=0.0, max_value=200.0, value=40.0, step=1.0,
                       help=t('tooltip_k'), label_visibility="collapsed")
    ...
    Soil_pH = st.slider("pH", min_value=4.0, max_value=9.0, value=6.5, step=0.1,
                       help=t('tooltip_ph'), label_visibility="collapsed")
    Soil_Moisture = st.slider("Moisture %", min_value=0.0, max_value=100.0, value=25.0, step=1.0,
                             help=t('tooltip_moisture'), label_visibility="collapsed")
    Organic_Carbon = st.number_input("OC %", min_value=0.0, max_value=5.0, value=0.8, step=0.1,
                                    help=t('tooltip_carbon'), label_visibility="collapsed")
    ...
    Soil_Type = st.selectbox("Type", ["Loamy", "Clay", "Sandy", "Red", "Black"],
                            label_visibility="collapsed")
    Altitude = st.number_input("Alt (m)", min_value=0.0, max_value=3000.0, value=200.0, step=10.0,
                              label_visibility="collapsed")
    ...
    Temperature = st.slider("Temp", min_value=-10.0, max_value=50.0, value=25.0, step=0.5,
                           label_visibility="collapsed")
    Humidity = st.slider("Hum", min_value=0.0, max_value=100.0, value=80.0, step=1.0,
                        label_visibility="collapsed")
    Rainfall = st.number_input("Rain", min_value=0.0, max_value=500.0, value=300.0, step=10.0,
                              label_visibility="collapsed")
    Sunlight_Hours = st.slider("Sun", min_value=0.0, max_value=24.0, value=8.0, step=0.5,
                              label_visibility="collapsed")
    Wind_Speed = st.slider("Wind", min_value=0.0, max_value=50.0, value=3.0, step=0.5,
                          label_visibility="collapsed")
    ...
    Crop_Type = st.selectbox("Crop", ["Wheat", "Rice", "Maize", "Barley", "Jute"],
                            label_visibility="collapsed")
    Season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Summer", "Winter"],
                         label_visibility="collapsed")
    Irrigation_Type = st.selectbox("Irrigation", ["Drip", "Sprinkler", "Flood", "Rainfed"],
                                  label_visibility="collapsed")
    Region = st.selectbox("Region", ["North", "South", "East", "West", "Central"],
                         label_visibility="collapsed")
    Fertilizer_Used = st.number_input("Fert", min_value=0.0, max_value=500.0, value=120.0, step=5.0,
                                     label_visibility="collapsed")
    Pesticide_Used = st.number_input("Pest", min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                                    label_visibility="collapsed")
    ...
    submit_button = st.form_submit_button(t('predict_btn'))
```

**How Streamlit “frontend” works here**

- Widgets like `st.slider(...)` and `st.selectbox(...)` are the **frontend inputs**.
- Each widget returns a Python value (float/int/str) to the variable you assign (`N`, `Soil_Type`, etc.).
- When the user clicks the form submit button, Streamlit returns `submit_button = True` for that run, which triggers the prediction block.

---

## 9) Backend logic: “Predict” click → build feature vector → scale → model predict

This is the most important part. It runs only when `submit_button` is `True`.

```1124:1177:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= PREDICTION =================
if submit_button:
    # Show loading animation
    with st.spinner(t('analyzing')):
        time.sleep(1.5)  # Simulate AI processing
        
        try:
            # Collect all inputs
            input_data = {
                'N': N, 'P': P, 'K': K,
                'Soil_pH': Soil_pH,
                'Soil_Moisture': Soil_Moisture,
                'Organic_Carbon': Organic_Carbon,
                'Temperature': Temperature,
                'Humidity': Humidity,
                'Rainfall': Rainfall,
                'Sunlight_Hours': Sunlight_Hours,
                'Wind_Speed': Wind_Speed,
                'Altitude': Altitude,
                'Fertilizer_Used': Fertilizer_Used,
                'Pesticide_Used': Pesticide_Used,
                'Soil_Type': Soil_Type,
                'Region': Region,
                'Season': Season,
                'Crop_Type': Crop_Type,
                'Irrigation_Type': Irrigation_Type
            }
            
            # Create DataFrame with all columns initialized to 0
            input_df = pd.DataFrame(np.zeros((1, len(columns))), columns=columns)
            
            # Fill numeric values
            for key, value in input_data.items():
                if key in input_df.columns:
                    input_df[key] = float(value)
            
            # Handle one-hot encoded categorical columns
            categorical_fields = {
                'Soil_Type': Soil_Type,
                'Region': Region,
                'Season': Season,
                'Crop_Type': Crop_Type,
                'Irrigation_Type': Irrigation_Type
            }
            
            for field, value in categorical_fields.items():
                col_name = f"{field}_{value}"
                if col_name in input_df.columns:
                    input_df[col_name] = 1
            
            # Scale and predict
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
```

### 9.1 Where the input is “taken from the frontend”

The “frontend” values are the variables defined in the form:

- Numeric: `N`, `P`, `K`, `Soil_pH`, `Temperature`, …
- Categorical: `Soil_Type`, `Region`, `Season`, `Crop_Type`, `Irrigation_Type`

Those are collected into the dictionary `input_data`.

### 9.2 How the model input is constructed (the DataFrame trick)

The app creates a DataFrame with **exactly the same columns as the training pipeline**:

- `input_df = DataFrame(zeros, columns=columns)`
- then it fills numeric fields directly
- then it sets one-hot columns like `Soil_Type_Loamy = 1` (if such columns exist in `column.pkl`)

This avoids “column mismatch” errors and ensures consistent feature ordering.

### 9.3 Where scaling happens

- `input_scaled = scaler.transform(input_df)`

This must match training time preprocessing. If you trained the model on scaled features, you must scale at inference time too.

### 9.4 Where model prediction happens

```1175:1177:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
input_scaled = scaler.transform(input_df)
prediction = model.predict(input_scaled)[0]
```

---

## 10) Confidence label (simple heuristic)

Confidence is not a true probability. It’s a simple label based on prediction magnitude.

```1178:1181:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# Calculate confidence (simplified - based on input completeness)
confidence = t('high') if prediction > 5 else t('medium')
confidence_color = "#4CAF50" if prediction > 5 else "#FF9800"
```

---

## 11) Frontend output: result rendering

After prediction, the app displays:

- predicted yield value
- confidence badge
- summary chips (crop, season, irrigation, region)
- metric cards (temperature, humidity, rainfall, sunlight)

```1182:1215:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# Display result with animation
st.markdown(f"""
<div class="result-box">
    <div class="result-title">{lucide_icon("agriculture", "lg")} {t('result_title')}</div>
    <div class="result-value">{prediction:.2f}</div>
    <div class="result-unit">ton/hectare</div>
    <div class="confidence-badge" style="background-color: {confidence_color};">
        {t('confidence')}: {confidence}
    </div>
</div>
""", unsafe_allow_html=True)

# Summary chips
st.markdown(f"""
<div style="text-align: center; margin: 20px auto; max-width: 900px;">
    <span class="summary-chip">{lucide_icon("agriculture", "sm")} {t('crop_type')}: {Crop_Type}</span>
    <span class="summary-chip">📅 {t('season')}: {Season}</span>
    <span class="summary-chip">{lucide_icon("droplets", "sm")} {t('irrigation')}: {Irrigation_Type}</span>
    <span class="summary-chip">{lucide_icon("map-pin", "sm")} {t('region')}: {Region}</span>
</div>
""", unsafe_allow_html=True)

# Detailed metrics
st.markdown('<div style="max-width: 1000px; margin: 0 auto;">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card">{lucide_icon("thermometer", "sm")} <strong>Temperature</strong><div class="metric-card-value">{Temperature}°C</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">{lucide_icon("droplets", "sm")} <strong>Humidity</strong><div class="metric-card-value">{Humidity}%</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card">{lucide_icon("cloud", "sm")} <strong>Rainfall</strong><div class="metric-card-value">{Rainfall} mm</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card">{lucide_icon("sun", "sm")} <strong>Sunlight</strong><div class="metric-card-value">{Sunlight_Hours} hrs</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
```

---

## 12) Error handling

If anything goes wrong during dataframe construction, scaling, or prediction, the app shows an error message and prints the exception (useful for debugging).

```1217:1220:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
except Exception as e:
    st.error(f"❌ {t('error_msg')}")
    st.exception(e)
```

---

## 13) Footer

Static footer with team member names.

```1221:1236:/Users/rishiwantmaurya/Desktop/Gen_AI_Capstone/app.py
# ================= FOOTER =================
st.markdown("<br>", unsafe_allow_html=True)

# Footer content
st.markdown("""
<div class="footer">
    <div class="footer-title">Team Members</div>
    <div class="team-members">
        Aditya Shankar • Animesh Rai • Kunal Dev Sahu • Rishiwant Kumar Maurya
    </div>
    <div class="footer-copyright">
        © 2026 Smart Crop Yield Predictor
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## Common confusion points (quick clarifications)

- **“Where is the backend?”**  
  In Streamlit, the Python script *is* the backend. Widgets send values to Python on each rerun.

- **“Where do we call the model?”**  
  At `model.predict(input_scaled)` in the prediction block.

- **“Why do we use `column.pkl`?”**  
  To guarantee the inference-time dataframe uses the **same feature columns** as training time, including one-hot columns.

- **“Are categorical values scaled?”**  
  They become one-hot columns (0/1) in `input_df`, and then the entire feature vector is passed into `scaler.transform(...)` (exactly as training likely did).

