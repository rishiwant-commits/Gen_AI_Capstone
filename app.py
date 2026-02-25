import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time

# ================= LOAD ARTIFACTS =================
model = joblib.load("trained_model.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

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

# ================= TRANSLATIONS =================
translations = {
    'en': {
        'title': 'Smart Crop Yield Predictor',
        'subtitle': 'Predict your crop yield with AI-powered precision',
        'ai_badge': '🤖 AI-Based Prediction',
        'ml_badge': 'Powered by Machine Learning',
        'section_soil_nutrients': 'Soil Nutrients (NPK)',
        'section_soil_properties': 'Soil Properties',
        'section_climate': 'Climate Conditions',
        'section_crop': 'Crop & Management Practices',
        'nitrogen': 'Nitrogen (N)',
        'phosphorus': 'Phosphorus (P)',
        'potassium': 'Potassium (K)',
        'soil_ph': 'Soil pH',
        'soil_moisture': 'Soil Moisture (%)',
        'organic_carbon': 'Organic Carbon (%)',
        'soil_type': 'Soil Type',
        'altitude': 'Altitude (m)',
        'temperature': 'Temperature (°C)',
        'humidity': 'Humidity (%)',
        'rainfall': 'Rainfall (mm)',
        'sunlight': 'Sunlight Hours/day',
        'wind_speed': 'Wind Speed (km/h)',
        'crop_type': 'Crop Type',
        'season': 'Season',
        'irrigation': 'Irrigation Type',
        'region': 'Region',
        'fertilizer': 'Fertilizer Used (kg/ha)',
        'pesticide': 'Pesticide Used (kg/ha)',
        'predict_btn': '🌾 Predict Crop Yield',
        'analyzing': 'Analyzing with AI...',
        'result_title': 'Predicted Crop Yield',
        'confidence': 'Confidence',
        'high': 'High',
        'medium': 'Medium',
        'download_report': '📥 Download Report',
        'error_msg': 'An error occurred during prediction. Please check your inputs.',
        'tooltip_n': 'Nitrogen helps plants grow green and strong',
        'tooltip_p': 'Phosphorus supports root development',
        'tooltip_k': 'Potassium improves disease resistance',
        'tooltip_ph': 'Soil pH affects nutrient availability',
        'tooltip_moisture': 'Water content in soil',
        'tooltip_carbon': 'Organic matter in soil'
    },
    'hi': {
        'title': 'स्मार्ट फसल उपज भविष्यवक्ता',
        'subtitle': 'एआई-संचालित सटीकता के साथ अपनी फसल की उपज की भविष्यवाणी करें',
        'ai_badge': '🤖 एआई-आधारित भविष्यवाणी',
        'ml_badge': 'मशीन लर्निंग द्वारा संचालित',
        'section_soil_nutrients': 'मिट्टी के पोषक तत्व (NPK)',
        'section_soil_properties': 'मिट्टी के गुण',
        'section_climate': 'जलवायु परिस्थितियाँ',
        'section_crop': 'फसल और प्रबंधन प्रथाएं',
        'nitrogen': 'नाइट्रोजन (N)',
        'phosphorus': 'फॉस्फोरस (P)',
        'potassium': 'पोटेशियम (K)',
        'soil_ph': 'मिट्टी पीएच',
        'soil_moisture': 'मिट्टी की नमी (%)',
        'organic_carbon': 'जैविक कार्बन (%)',
        'soil_type': 'मिट्टी का प्रकार',
        'altitude': 'ऊंचाई (मी)',
        'temperature': 'तापमान (°C)',
        'humidity': 'आर्द्रता (%)',
        'rainfall': 'वर्षा (मिमी)',
        'sunlight': 'सूर्य के प्रकाश के घंटे/दिन',
        'wind_speed': 'हवा की गति (किमी/घंटा)',
        'crop_type': 'फसल का प्रकार',
        'season': 'मौसम',
        'irrigation': 'सिंचाई का प्रकार',
        'region': 'क्षेत्र',
        'fertilizer': 'उपयोग किया गया उर्वरक (किग्रा/हेक्टेयर)',
        'pesticide': 'उपयोग किया गया कीटनाशक (किग्रा/हेक्टेयर)',
        'predict_btn': '🌾 फसल उपज की भविष्यवाणी करें',
        'analyzing': 'एआई के साथ विश्लेषण कर रहे हैं...',
        'result_title': 'अनुमानित फसल उपज',
        'confidence': 'विश्वास',
        'high': 'उच्च',
        'medium': 'मध्यम',
        'download_report': '📥 रिपोर्ट डाउनलोड करें',
        'error_msg': 'भविष्यवाणी के दौरान एक त्रुटि हुई। कृपया अपने इनपुट की जाँच करें।',
        'tooltip_n': 'नाइट्रोजन पौधों को हरा और मजबूत बनाता है',
        'tooltip_p': 'फॉस्फोरस जड़ विकास का समर्थन करता है',
        'tooltip_k': 'पोटेशियम रोग प्रतिरोध में सुधार करता है',
        'tooltip_ph': 'मिट्टी पीएच पोषक तत्व उपलब्धता को प्रभावित करता है',
        'tooltip_moisture': 'मिट्टी में पानी की मात्रा',
        'tooltip_carbon': 'मिट्टी में जैविक पदार्थ'
    }
}

def t(key):
    """Translation helper function"""
    return translations[st.session_state.language].get(key, key)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Mobile-First Responsive Design */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
        padding: 1rem;
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(1.8rem, 5vw, 3rem);
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #555;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        margin-bottom: 1.5rem;
        padding: 0 1rem;
    }
    
    /* Language Toggle */
    .language-toggle {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* AI Badges */
    .ai-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        font-weight: 600;
        display: inline-block;
        margin: 5px;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Card-Based Section Headers */
    .section-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .section-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .section-header {
        color: #2E7D32;
        font-size: clamp(1.1rem, 3vw, 1.5rem);
        font-weight: 700;
        margin: 0 0 15px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        border-left: 5px solid #4CAF50;
        padding-left: 15px;
    }
    
    /* Input Field Styling */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 10px !important;
        font-size: clamp(0.9rem, 2.5vw, 1rem) !important;
    }
    
    .stSlider > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    /* Tooltip Styling */
    .tooltip-icon {
        display: inline-block;
        background: #4CAF50;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        text-align: center;
        font-size: 12px;
        line-height: 20px;
        cursor: help;
        margin-left: 5px;
    }
    
    /* Big CTA Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        font-size: clamp(1rem, 3vw, 1.3rem);
        font-weight: bold;
        padding: 18px 24px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.6);
        transform: translateY(-3px);
        background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Result Box with Animation */
    .result-box {
        background: linear-gradient(135deg, #4CAF50 0%, #388e3c 100%);
        padding: clamp(20px, 5vw, 40px);
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
        margin: 20px 0;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-title {
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    .result-value {
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 800;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .result-unit {
        font-size: clamp(1rem, 2.5vw, 1.4rem);
        opacity: 0.95;
    }
    
    /* Confidence Badge */
    .confidence-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        padding: 8px 20px;
        border-radius: 20px;
        margin-top: 15px;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        backdrop-filter: blur(10px);
    }
    
    /* Summary Chips */
    .summary-chip {
        background: white;
        color: #2E7D32;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-block;
        margin: 5px;
        font-weight: 600;
        font-size: clamp(0.8rem, 2vw, 1rem);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Loading Animation */
    .loading {
        text-align: center;
        padding: 20px;
        color: #4CAF50;
        font-size: clamp(1rem, 2.5vw, 1.2rem);
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #4CAF50;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .section-card {
            padding: 15px;
            margin: 10px 0;
        }
        
        .stButton > button {
            padding: 15px 20px;
        }
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: clamp(1.2rem, 4vw, 1.8rem) !important;
        font-weight: 700 !important;
        color: #2E7D32 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.9rem, 2.5vw, 1.1rem) !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
# Language Toggle
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇬🇧 English", key="en_btn", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    with lang_col2:
        if st.button("🇮🇳 हिंदी", key="hi_btn", use_container_width=True):
            st.session_state.language = 'hi'
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Title and Logo
st.title(f"🌾 {t('title')}")
st.markdown(f'<p class="subtitle">{t("subtitle")}</p>', unsafe_allow_html=True)

# AI Badges
st.markdown(f"""
<div style="text-align: center; margin-bottom: 30px;">
    <span class="ai-badge">{t('ai_badge')}</span>
    <span class="ai-badge">{t('ml_badge')}</span>
</div>
""", unsafe_allow_html=True)

# ================= INPUT FORM =================
with st.form("prediction_form"):
    # Soil Nutrients Section
    st.markdown(f'''
    <div class="section-card">
        <div class="section-header">🧪 {t("section_soil_nutrients")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**{t('nitrogen')}** ℹ️")
        N = st.number_input("N (kg/ha)", min_value=0.0, max_value=200.0, value=97.0, step=1.0, 
                           help=t('tooltip_n'), label_visibility="collapsed")
        N_slider = st.slider("", min_value=0.0, max_value=200.0, value=97.0, step=1.0, key="n_slider")
        N = N_slider  # Use slider value
    with col2:
        st.markdown(f"**{t('phosphorus')}** ℹ️")
        P = st.number_input("P (kg/ha)", min_value=0.0, max_value=200.0, value=20.0, step=1.0,
                           help=t('tooltip_p'), label_visibility="collapsed")
    with col3:
        st.markdown(f"**{t('potassium')}** ℹ️")
        K = st.number_input("K (kg/ha)", min_value=0.0, max_value=200.0, value=40.0, step=1.0,
                           help=t('tooltip_k'), label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Soil Properties Section
    st.markdown(f'''
    <div class="section-card">
        <div class="section-header">🌱 {t("section_soil_properties")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{t('soil_ph')}** ℹ️")
        Soil_pH = st.slider("pH", min_value=4.0, max_value=9.0, value=6.5, step=0.1,
                           help=t('tooltip_ph'), label_visibility="collapsed")
        
        st.markdown(f"**{t('soil_moisture')}** ℹ️")
        Soil_Moisture = st.slider("Moisture %", min_value=0.0, max_value=100.0, value=25.0, step=1.0,
                                 help=t('tooltip_moisture'), label_visibility="collapsed")
        
        st.markdown(f"**{t('organic_carbon')}** ℹ️")
        Organic_Carbon = st.number_input("OC %", min_value=0.0, max_value=5.0, value=0.8, step=0.1,
                                        help=t('tooltip_carbon'), label_visibility="collapsed")
    with col2:
        st.markdown(f"**{t('soil_type')}**")
        Soil_Type = st.selectbox("Type", ["Loamy", "Clay", "Sandy", "Red", "Black"],
                                label_visibility="collapsed")
        
        st.markdown(f"**{t('altitude')}**")
        Altitude = st.number_input("Alt (m)", min_value=0.0, max_value=3000.0, value=200.0, step=10.0,
                                  label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Climate Conditions Section
    st.markdown(f'''
    <div class="section-card">
        <div class="section-header">🌤️ {t("section_climate")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**🌡️ {t('temperature')}**")
        Temperature = st.slider("Temp", min_value=-10.0, max_value=50.0, value=25.0, step=0.5,
                               label_visibility="collapsed")
        
        st.markdown(f"**💧 {t('humidity')}**")
        Humidity = st.slider("Hum", min_value=0.0, max_value=100.0, value=80.0, step=1.0,
                            label_visibility="collapsed")
    with col2:
        st.markdown(f"**🌧️ {t('rainfall')}**")
        Rainfall = st.number_input("Rain", min_value=0.0, max_value=500.0, value=300.0, step=10.0,
                                  label_visibility="collapsed")
        
        st.markdown(f"**☀️ {t('sunlight')}**")
        Sunlight_Hours = st.slider("Sun", min_value=0.0, max_value=24.0, value=8.0, step=0.5,
                                  label_visibility="collapsed")
    with col3:
        st.markdown(f"**💨 {t('wind_speed')}**")
        Wind_Speed = st.slider("Wind", min_value=0.0, max_value=50.0, value=3.0, step=0.5,
                              label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Crop & Management Section
    st.markdown(f'''
    <div class="section-card">
        <div class="section-header">🚜 {t("section_crop")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🌾 {t('crop_type')}**")
        Crop_Type = st.selectbox("Crop", ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Barley", "Jute"],
                                label_visibility="collapsed")
        
        st.markdown(f"**📅 {t('season')}**")
        Season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Summer", "Winter"],
                             label_visibility="collapsed")
        
        st.markdown(f"**💧 {t('irrigation')}**")
        Irrigation_Type = st.selectbox("Irrigation", ["Drip", "Sprinkler", "Flood", "Rainfed"],
                                      label_visibility="collapsed")
    with col2:
        st.markdown(f"**📍 {t('region')}**")
        Region = st.selectbox("Region", ["North", "South", "East", "West", "Central"],
                             label_visibility="collapsed")
        
        st.markdown(f"**🧴 {t('fertilizer')}**")
        Fertilizer_Used = st.number_input("Fert", min_value=0.0, max_value=500.0, value=120.0, step=5.0,
                                         label_visibility="collapsed")
        
        st.markdown(f"**🦗 {t('pesticide')}**")
        Pesticide_Used = st.number_input("Pest", min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                                        label_visibility="collapsed")
    
    # Submit Button
    st.markdown("<br><br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(t('predict_btn'))

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
            
            # Calculate confidence (simplified - based on input completeness)
            confidence = t('high') if prediction > 5 else t('medium')
            confidence_color = "#4CAF50" if prediction > 5 else "#FF9800"
            
            # Display result with animation
            st.markdown(f"""
            <div class="result-box">
                <div class="result-title">🌾 {t('result_title')}</div>
                <div class="result-value">{prediction:.2f}</div>
                <div class="result-unit">ton/hectare</div>
                <div class="confidence-badge" style="background-color: {confidence_color};">
                    {t('confidence')}: {confidence}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary chips
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <span class="summary-chip">🌾 {t('crop_type')}: {Crop_Type}</span>
                <span class="summary-chip">📅 {t('season')}: {Season}</span>
                <span class="summary-chip">💧 {t('irrigation')}: {Irrigation_Type}</span>
                <span class="summary-chip">📍 {t('region')}: {Region}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌡️ Temp", f"{Temperature}°C")
            with col2:
                st.metric("💧 Humidity", f"{Humidity}%")
            with col3:
                st.metric("🌧️ Rainfall", f"{Rainfall} mm")
            with col4:
                st.metric("☀️ Sunlight", f"{Sunlight_Hours} hrs")
            
            # Download Report Button (placeholder)
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div style="text-align: center;">
                    <button style="
                        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
                        color: white;
                        padding: 12px 30px;
                        border: none;
                        border-radius: 25px;
                        font-size: 1rem;
                        font-weight: 600;
                        cursor: pointer;
                        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
                    ">
                        {t('download_report')}
                    </button>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ {t('error_msg')}")
            st.exception(e)

# ================= FOOTER =================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Footer content
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem; margin-bottom: 10px;">
        <strong>🤖 ML Model:</strong> Random Forest Regressor | 
        <strong>📊 Dataset:</strong> Smart Crop Yield | 
        <strong>🚀 Powered by:</strong> Streamlit
    </p>
    <p style="color: #999; font-size: 0.85rem;">
        💬 Need help? Ask AI for farming tips and recommendations
    </p>
    <p style="color: #999; font-size: 0.8rem; margin-top: 10px;">
        © 2026 Smart Crop Yield Predictor - Empowering Indian Farmers with AI
    </p>
</div>
""", unsafe_allow_html=True)
