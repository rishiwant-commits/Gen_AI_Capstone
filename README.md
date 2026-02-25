# 🌾 Smart Crop Yield Predictor

A mobile-first, multilingual web application designed for Indian farmers to predict crop yield using AI-powered machine learning.

## 🎯 Features

- **Mobile-First Design**: Optimized for smartphones and tablets
- **Multilingual Support**: English (🇬🇧) and Hindi (🇮🇳)
- **AI-Powered Predictions**: Uses Random Forest Regressor for accurate yield forecasting
- **Farmer-Friendly UI**: Simple icons, sliders, and minimal text
- **Visual Design**: Card-based layout with green earth tones
- **Interactive Elements**: 
  - Tooltips for guidance
  - Loading animations
  - Confidence indicators
  - Responsive sliders and inputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd Gen_AI_capstone
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically open in your default browser

## 📱 How to Use

### Step 1: Select Language
- Choose between English (🇬🇧) or Hindi (🇮🇳) using the language toggle

### Step 2: Enter Soil Nutrients (NPK)
- **Nitrogen (N)**: Use slider or input (0-200 kg/ha)
- **Phosphorus (P)**: Enter value (0-200 kg/ha)
- **Potassium (K)**: Enter value (0-200 kg/ha)
- ℹ️ Hover over info icons for tips

### Step 3: Soil Properties
- **Soil pH**: Adjust slider (4.0-9.0)
- **Soil Moisture**: Set percentage (0-100%)
- **Organic Carbon**: Enter percentage (0-5%)
- **Soil Type**: Select from dropdown (Loamy, Clay, Sandy, Red, Black)
- **Altitude**: Enter in meters (0-3000m)

### Step 4: Climate Conditions
- 🌡️ **Temperature**: -10°C to 50°C
- 💧 **Humidity**: 0-100%
- 🌧️ **Rainfall**: Enter in mm
- ☀️ **Sunlight Hours**: 0-24 hours/day
- 💨 **Wind Speed**: 0-50 km/h

### Step 5: Crop & Management
- 🌾 **Crop Type**: Rice, Wheat, Maize, etc.
- 📅 **Season**: Kharif, Rabi, Zaid
- 💧 **Irrigation Type**: Drip, Sprinkler, Flood
- 📍 **Region**: North, South, East, West
- 🧴 **Fertilizer Used**: kg/hectare
- 🦗 **Pesticide Used**: kg/hectare

### Step 6: Get Prediction
- Click the **🌾 Predict Crop Yield** button
- Wait for AI analysis (1-2 seconds)
- View your predicted yield in **tons/hectare**
- See confidence level (High/Medium)
- Review summary chips with your inputs

## 🎨 Design Highlights

### Color Palette
- **Primary Green**: `#4CAF50` (Agriculture, growth)
- **Earth Brown**: `#795548` (Soil, land)
- **Sky Blue**: `#2196F3` (Water, weather)
- **Background**: Soft gradient from `#f5f7fa` to `#e8f5e9`

### Typography
- **Font**: Poppins (rounded, highly readable)
- **Mobile-responsive**: Font sizes scale from `clamp(0.9rem, 2.5vw, 1rem)`

### Components
- **Card-based sections**: White cards with shadows
- **Big rounded buttons**: Easy tap targets for mobile
- **Slider controls**: Accessible for low-literacy users
- **Icon-heavy interface**: Reduces text dependency

## 🧠 AI Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 18 input parameters
- **Output**: Crop yield in tons/hectare
- **Preprocessing**: StandardScaler normalization
- **Encoding**: One-hot encoding for categorical variables

## 📊 Dataset Features

### Numeric Features (14)
- N, P, K (NPK nutrients)
- Soil pH, Moisture, Organic Carbon
- Temperature, Humidity, Rainfall
- Sunlight Hours, Wind Speed
- Altitude
- Fertilizer Used, Pesticide Used

### Categorical Features (5)
- Soil Type
- Region
- Season
- Crop Type
- Irrigation Type

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **ML Model**: scikit-learn Random Forest
- **Data Processing**: pandas, numpy
- **Model Persistence**: joblib
- **Styling**: Custom CSS with mobile-first approach

## 📱 Mobile Optimization

- Responsive breakpoints for tablets and phones
- Touch-friendly input controls
- Reduced data entry with sliders
- Simplified navigation (no sidebar)
- Fast loading times
- Offline-friendly design

## 🌐 Multilingual Support

Currently supports:
- **English** (Default)
- **Hindi** (हिंदी)

Translations are managed through a centralized dictionary that can be easily extended to support additional Indian languages like:
- Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam

## 🔮 Future Enhancements

- [ ] Voice input for farmers
- [ ] Image-based soil analysis
- [ ] WhatsApp integration
- [ ] SMS-based predictions
- [ ] Weather API integration
- [ ] Historical yield tracking
- [ ] PDF report generation
- [ ] Crop recommendation system
- [ ] Pest and disease detection
- [ ] Market price predictions

## 🤝 Contributing

This project is designed to help Indian farmers. Contributions are welcome!

## 📄 License

Open source - free to use for agricultural and educational purposes.

## 👨‍💻 Support

For issues or questions:
- Check input values are within valid ranges
- Ensure model files (`trained_model.pkl`, `scaler.pkl`, `columns.pkl`) are present
- Verify Python and package versions

## 🌾 About

Built with ❤️ for Indian farmers to make AI-powered agricultural predictions accessible to everyone, regardless of technical literacy.

---

**🤖 Powered by Machine Learning | 🌱 Empowering Farmers | 🇮🇳 Made in India**
