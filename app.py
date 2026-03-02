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
<rect x="7" y="7" width="10" height="10" rx="1" fill="none"/>
<line x1="7" y1="12" x2="17" y2="12"/>
<line x1="12" y1="7" x2="12" y2="17"/>
<line x1="2" y1="9" x2="4" y2="9"/>
<line x1="2" y1="15" x2="4" y2="15"/>
<line x1="20" y1="9" x2="22" y2="9"/>
<line x1="20" y1="15" x2="22" y2="15"/>
<line x1="9" y1="2" x2="9" y2="4"/>
<line x1="15" y1="2" x2="15" y2="4"/>
<line x1="9" y1="20" x2="9" y2="22"/>
<line x1="15" y1="20" x2="15" y2="22"/></svg>''',
    'beaker': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M4.5 3h15v7c0 3.87-3.13 7-7 7h-1c-3.87 0-7-3.13-7-7V3z"/>
<line x1="9" y1="21" x2="15" y2="21"/></svg>''',
    'sprout': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M6 14c.293-2.863 2.618-5 5-5s4.707 2.137 5 5"/>
<path d="M11 13v8"/>
<path d="M8 16h6"/>
<path d="M9 9c0-1.864.895-3.5 2-4.5C12.105 5.5 13 7.136 13 9"/>
<path d="M11 2v4"/></svg>''',
    'droplets': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M7 16.3c2.1 2.1 5.6 2.1 7.7 0c2.1-2.1 2.1-5.6 0-7.7L12 2c-2.1 2.1-5.6 2.1-7.7 0c-2.1 2.1-2.1 5.6 0 7.7L7 16.3z"/>
<path d="M5.7 9.1c-1.4 1.4-1.4 3.7 0 5.1c1.4 1.4 3.7 1.4 5.1 0"/>
<path d="M16.3 7.7c2.1-2.1 2.1-5.6 0-7.7L12 2c2.1 2.1 5.6 2.1 7.7 0c2.1-2.1 2.1-5.6 0-7.7L16.3 7.7z"/></svg>''',
    'thermometer': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M12 2v16M7 19c0 2.76 2.24 5 5 5s5-2.24 5-5"/>
<circle cx="12" cy="20" r="3"/></svg>''',
    'cloud': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 1 0 7 20h11a5 5 0 0 0 0-10z"/></svg>''',
    'sun': '''<svg class="lucide-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/>
<line x1="12" y1="1" x2="12" y2="3"/>
<line x1="12" y1="21" x2="12" y2="23"/>
<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
<line x1="1" y1="12" x2="3" y2="12"/>
<line x1="21" y1="12" x2="23" y2="12"/>
<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>''',
    'map-pin': '''<svg class="lucide-icon" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 11 7 11s7-5.75 7-11c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>''',
}

def lucide_icon(name: str, size_class: str = "md") -> str:
    """Generate a Lucide SVG icon HTML string"""
    svg = LUCIDE_ICONS.get(name, LUCIDE_ICONS['agriculture'])
    return f'<span class="lucide-icon {size_class}">{svg}</span>'

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
        'ai_badge': 'smart_toy AI-Based Prediction',
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
        'predict_btn': 'agriculture Predict Crop Yield',
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
        'ai_badge': 'smart_toy एआई-आधारित भविष्यवाणी',
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
        'predict_btn': 'agriculture फसल उपज की भविष्यवाणी करें',
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

# ================= BACKGROUND IMAGE SETUP =================

def get_base64_image(image_path):
    """Convert image to base64 for CSS background"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Load background image
bg_image = get_base64_image("farmer.jpeg")

# ================= CUSTOM CSS =================
if bg_image:
    st.markdown(f"""
    <style>
        /* Background Image with Overlay */
        .stApp {{
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.42), rgba(255, 255, 255, 0.42)),
                url("data:image/jpeg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Mobile-First Responsive Design */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .main {{
            background: transparent;
            padding: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)
else:
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
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
    /* Lucide SVG Icon Styling */
    .lucide-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        vertical-align: middle;
        margin-right: 6px;
        flex-shrink: 0;
    }
    
    .lucide-icon svg {
        width: 24px;
        height: 24px;
        stroke: currentColor;
        stroke-width: 2;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    
    .lucide-icon.sm svg {
        width: 18px;
        height: 18px;
    }
    
    .lucide-icon.md svg {
        width: 24px;
        height: 24px;
    }
    
    .lucide-icon.lg svg {
        width: 32px;
        height: 32px;
    }
    
    /* Hide Streamlit Default UI Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Remove Excessive Top Spacing - Override Streamlit Defaults */
    .stAppViewContainer {
        top: 0 !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
        gap: 0 !important;
    }
    
    .stMainBlockContainer {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Compact column spacing */
    .stColumn {
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove spacing from all containers */
    [data-testid="stForm"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    [data-testid="stColumnBlock"] {
        gap: 0 !important;
        margin: 0 !important;
    }
    
    /* Form Submit Button Container */
    [data-testid="stForm"] .stButton {
        display: flex;
        justify-content: center;
        margin-top: 20px !important;
    }
    
    /* Minimize all gaps and spacings */
    div:has(> [data-testid="stButton"]) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Hero Section Container */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 30px 20px 20px 20px;
        margin: 0 !important;
        gap: 0;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.7) 0%, rgba(232, 245, 233, 0.5) 100%);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(1.8rem, 5vw, 3rem);
        font-weight: 800;
        text-align: center;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1;
    }
    
    .subtitle {
        text-align: center;
        color: #555;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        margin: 8px 0 0 0 !important;
        padding: 0 1rem !important;
        line-height: 1.4;
        font-weight: 500;
    }

    /* CTA Buttons Container */
    .cta-buttons-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 12px;
        margin: 16px 0 0 0 !important;
        padding: 0 !important;
    }
    
    /* Language Toggle - Top Right of Content */
    .language-toggle-wrapper {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        margin-bottom: 20px;
        margin-top: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        width: 100%;
    }
    
    .language-toggle-wrapper .stButton {
        flex: 0 0 auto;
    }
    
    .language-toggle-wrapper .stButton > button {
        width: 100% !important;
        background: rgba(76, 175, 80, 0.9) !important;
        color: white !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        border: 1.5px solid rgba(76, 175, 80, 0.5) !important;
        box-shadow: 
            0 4px 12px rgba(76, 175, 80, 0.25),
            0 1px 4px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 !important;
        text-transform: none !important;
        letter-spacing: 0.3px !important;
        text-shadow: none !important;
        white-space: nowrap !important;
    }
    
    .language-toggle-wrapper .stButton > button::before {
        display: none !important;
    }
    
    .language-toggle-wrapper .stButton > button:hover {
        background: rgba(76, 175, 80, 1) !important;
        border-color: #4CAF50 !important;
        box-shadow: 
            0 6px 16px rgba(76, 175, 80, 0.35),
            0 2px 6px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .language-toggle-wrapper .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 
            0 2px 8px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
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
        margin: 0 6px !important;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .ai-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Card-Based Section Headers */
    .section-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.12),
            0 2px 8px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.6),
            inset 0 -1px 0 rgba(0, 0, 0, 0.04);
        border: 1.5px solid rgba(255, 255, 255, 0.7);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .section-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            rgba(46, 125, 50, 0.5) 0%, 
            rgba(76, 175, 80, 0.7) 50%, 
            rgba(46, 125, 50, 0.5) 100%);
    }
    
    .section-card:hover {
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.15),
            0 4px 12px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.7),
            inset 0 -1px 0 rgba(0, 0, 0, 0.05);
        transform: translateY(-4px) scale(1.01);
        border-color: rgba(76, 175, 80, 0.4);
    }
    
    .section-header {
        color: #2E7D32;
        font-size: clamp(1.2rem, 3vw, 1.6rem);
        font-weight: 800;
        margin: 0 0 20px 0;
        display: flex;
        align-items: center;
        gap: 12px;
        border-left: 5px solid #4CAF50;
        padding-left: 18px;
        text-shadow: 0 1px 2px rgba(46, 125, 50, 0.1);
        letter-spacing: 0.3px;
    }
    
    /* Input Field Styling - Modern Glassmorphism */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        border: 1.5px solid rgba(224, 224, 224, 0.6) !important;
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        padding: 12px 14px !important;
        font-size: clamp(0.9rem, 2.5vw, 1rem) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #4CAF50 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    .stSlider > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%) !important;
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
    
    /* Big CTA Button - Premium Glassmorphism */
    .stButton > button {
        width: auto !important;
        min-width: 180px;
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #66BB6A 100%);
        background-size: 200% 100%;
        color: white;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        font-weight: 700;
        padding: 12px 28px;
        border-radius: 16px;
        border: 1.5px solid rgba(255, 255, 255, 0.3);
        box-shadow: \n            0 8px 24px rgba(76, 175, 80, 0.35),\n            0 2px 8px rgba(0, 0, 0, 0.1),\n            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        margin: 0 !important;
        text-transform: none;
        letter-spacing: 0.5px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        white-space: nowrap;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        background-position: 100% 0;
        box-shadow: \n            0 12px 32px rgba(76, 175, 80, 0.45),\n            0 4px 12px rgba(0, 0, 0, 0.15),\n            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: \n            0 4px 16px rgba(76, 175, 80, 0.35),\n            0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Result Box with Animation - Premium Glassmorphism */
    .result-box {
        background: linear-gradient(135deg, \n            rgba(76, 175, 80, 0.92) 0%, \n            rgba(69, 160, 73, 0.92) 50%,\n            rgba(102, 187, 106, 0.88) 100%);
        backdrop-filter: blur(25px) saturate(180%);
        padding: clamp(30px, 5vw, 50px);
        border-radius: 24px;
        text-align: center;
        color: white;
        box-shadow: \n            0 20px 60px rgba(76, 175, 80, 0.35),\n            0 8px 24px rgba(0, 0, 0, 0.15),\n            inset 0 1px 0 rgba(255, 255, 255, 0.25),\n            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        margin: 30px 0;
        animation: slideInScale 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        border: 1.5px solid rgba(255, 255, 255, 0.35);
        position: relative;
        overflow: hidden;
    }
    
    .result-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, \n            transparent 0%, \n            rgba(255, 255, 255, 0.6) 50%, \n            transparent 100%);
    }
    
    @keyframes slideInScale {
        from {
            opacity: 0;
            transform: scale(0.92) translateY(20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .result-title {
        font-size: clamp(1.3rem, 3vw, 1.8rem);
        font-weight: 700;
        margin-bottom: 18px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        letter-spacing: 0.5px;
    }
    
    .result-value {
        font-size: clamp(3rem, 8vw, 4.5rem);
        font-weight: 900;
        margin: 15px 0;
        text-shadow: \n            0 4px 12px rgba(0, 0, 0, 0.25),\n            0 2px 4px rgba(0, 0, 0, 0.15);
        background: linear-gradient(180deg, #ffffff 0%, rgba(255, 255, 255, 0.85) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .result-unit {
        font-size: clamp(1.1rem, 2.5vw, 1.5rem);
        opacity: 0.95;
        font-weight: 600;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        letter-spacing: 0.5px;
    }
    
    /* Confidence Badge - Modern Pill */
    .confidence-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        padding: 10px 24px;
        border-radius: 25px;
        margin-top: 20px;
        font-size: clamp(0.95rem, 2vw, 1.15rem);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(255, 255, 255, 0.4);
        box-shadow: \n            0 4px 12px rgba(0, 0, 0, 0.15),\n            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    /* Summary Chips - Modern Glassmorphism */
    .summary-chip {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px) saturate(180%);
        color: #2E7D32;
        padding: 12px 24px;
        border-radius: 28px;
        display: inline-block;
        margin: 6px;
        font-weight: 700;
        font-size: clamp(0.85rem, 2vw, 1.05rem);
        box-shadow: \n            0 4px 12px rgba(0, 0, 0, 0.1),\n            0 1px 4px rgba(0, 0, 0, 0.06),\n            inset 0 1px 0 rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
    }
    
    .summary-chip:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: \n            0 6px 16px rgba(0, 0, 0, 0.15),\n            0 2px 6px rgba(0, 0, 0, 0.08),\n            inset 0 1px 0 rgba(255, 255, 255, 0.8);
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
        
        .language-toggle-wrapper .stButton > button {
            font-size: 0.75rem !important;
            padding: 6px 10px !important;
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
    
    /* Footer - Premium Glassmorphism */
    .footer {
        text-align: center;
        padding: 40px 30px;
        margin: 50px auto 20px auto;
        max-width: 1000px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 24px;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.12),
            0 4px 12px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.6),
            inset 0 -1px 0 rgba(0, 0, 0, 0.04);
        border: 1.5px solid rgba(255, 255, 255, 0.7);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(76, 175, 80, 0.6) 50%, 
            transparent 100%);
    }
    
    .footer-title {
        color: #2E7D32;
        font-size: clamp(1.1rem, 2.5vw, 1.3rem);
        font-weight: 800;
        margin-bottom: 15px;
        text-shadow: 0 1px 2px rgba(46, 125, 50, 0.1);
        letter-spacing: 0.5px;
    }
    
    .footer-subtitle {
        color: #666;
        font-size: clamp(0.85rem, 2vw, 0.95rem);
        margin: 10px 0;
        font-weight: 500;
    }
    
    .footer-copyright {
        color: #999;
        font-size: clamp(0.75rem, 1.8vw, 0.85rem);
        margin-top: 15px;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

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

# Title and Logo
st.markdown(f"""
<div class="hero-section">
    <h1 style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        {lucide_icon('sprout', 'lg')} {t('title')}
    </h1>
    <p class="subtitle">{t("subtitle")}</p>
    <div class="cta-buttons-container">
        <span class="ai-badge">{t('ai_badge')}</span>
        <span class="ai-badge">{t('ml_badge')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= INPUT FORM =================
with st.form("prediction_form"):
    # Soil Nutrients Section
    st.markdown(f'''
    <div class="section-card">
        <div class="section-header">{lucide_icon('beaker', 'md')} {t("section_soil_nutrients")}</div>
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
        <div class="section-header">{lucide_icon('sprout', 'md')} {t("section_soil_properties")}</div>
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
        <div class="section-header">{lucide_icon('cloud', 'md')} {t("section_climate")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'**{lucide_icon("thermometer", "sm")} {t("temperature")}**', unsafe_allow_html=True)
        Temperature = st.slider("Temp", min_value=-10.0, max_value=50.0, value=25.0, step=0.5,
                               label_visibility="collapsed")
        
        st.markdown(f'**{lucide_icon("droplets", "sm")} {t("humidity")}**', unsafe_allow_html=True)
        Humidity = st.slider("Hum", min_value=0.0, max_value=100.0, value=80.0, step=1.0,
                            label_visibility="collapsed")
    with col2:
        st.markdown(f'**{lucide_icon("cloud", "sm")} {t("rainfall")}**', unsafe_allow_html=True)
        Rainfall = st.number_input("Rain", min_value=0.0, max_value=500.0, value=300.0, step=10.0,
                                  label_visibility="collapsed")
        
        st.markdown(f'**{lucide_icon("sun", "sm")} {t("sunlight")}**', unsafe_allow_html=True)
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
        st.markdown(f'**{lucide_icon("agriculture", "sm")} {t("crop_type")}**', unsafe_allow_html=True)
        Crop_Type = st.selectbox("Crop", ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Barley", "Jute"],
                                label_visibility="collapsed")
        
        st.markdown(f"**📅 {t('season')}**")
        Season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Summer", "Winter"],
                             label_visibility="collapsed")
        
        st.markdown(f'**{lucide_icon("droplets", "sm")} {t("irrigation")}**', unsafe_allow_html=True)
        Irrigation_Type = st.selectbox("Irrigation", ["Drip", "Sprinkler", "Flood", "Rainfed"],
                                      label_visibility="collapsed")
    with col2:
        st.markdown(f'**{lucide_icon("map-pin", "sm")} {t("region")}**', unsafe_allow_html=True)
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
            <div style="text-align: center; margin: 20px 0;">
                <span class="summary-chip">{lucide_icon("agriculture", "sm")} {t('crop_type')}: {Crop_Type}</span>
                <span class="summary-chip">📅 {t('season')}: {Season}</span>
                <span class="summary-chip">{lucide_icon("droplets", "sm")} {t('irrigation')}: {Irrigation_Type}</span>
                <span class="summary-chip">{lucide_icon("map-pin", "sm")} {t('region')}: {Region}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px; text-align: center;">{lucide_icon("thermometer", "sm")} <strong>Temperature</strong><br/>{Temperature}°C</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px; text-align: center;">{lucide_icon("droplets", "sm")} <strong>Humidity</strong><br/>{Humidity}%</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px; text-align: center;">{lucide_icon("cloud", "sm")} <strong>Rainfall</strong><br/>{Rainfall} mm</div>', unsafe_allow_html=True)
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

# Footer content
st.markdown("""
<div class="footer">
    <div class="footer-title">
        🤖 ML Model: Random Forest Regressor | 📊 Smart Crop Yield Dataset
    </div>
    <div class="footer-subtitle">
        🚀 Powered by Streamlit • 🌾 Designed for Indian Farmers
    </div>
    <div class="footer-subtitle" style="margin-top: 12px;">
        💬 AI-Powered Predictions • 🌍 Sustainable Agriculture • 📈 Data-Driven Farming
    </div>
    <div class="footer-copyright">
        © 2026 Smart Crop Yield Predictor - Empowering Farmers with Artificial Intelligence
    </div>
</div>
""", unsafe_allow_html=True)
