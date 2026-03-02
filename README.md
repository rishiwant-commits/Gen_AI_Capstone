# Smart Crop Yield Predictor

A web-based machine learning application designed to help Indian farmers predict crop yield using data-driven insights.

## Project Overview

Agriculture is the backbone of India's economy, yet many farmers struggle with unpredictable crop yields due to various environmental and soil factors. The Smart Crop Yield Predictor addresses this challenge by providing an accessible, AI-powered tool that estimates crop yield based on soil properties, climate conditions, and farming practices.

This application leverages machine learning to analyze key agricultural parameters and deliver accurate yield predictions, enabling farmers to make informed decisions about resource allocation and crop management.

## Features

- AI-powered crop yield prediction using Random Forest Regressor
- Intuitive web interface designed for users with varying digital literacy
- Multilingual support (English and Hindi)
- Comprehensive input parameters including:
  - Soil nutrients (Nitrogen, Phosphorus, Potassium)
  - Soil properties (pH, moisture, organic carbon, type)
  - Climate conditions (temperature, humidity, rainfall, sunlight, wind speed)
  - Crop and management practices (crop type, season, irrigation, region)
- Real-time prediction with confidence indicators
- Mobile-responsive design for accessibility
- Visual result presentation with detailed metrics

## Tech Stack

### Machine Learning
- **Model**: Random Forest Regressor
- **Preprocessing**: StandardScaler for feature normalization
- **Libraries**: scikit-learn, NumPy, pandas

### Frontend & Backend
- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Additional Libraries**: 
  - joblib (model serialization)
  - base64 (image encoding)

### Deployment
- Local deployment with Streamlit server
- Port: 8501 (default)

## Dataset Information

The model was trained on a comprehensive agricultural dataset containing crop yield data from various regions of India. The dataset includes:

- Soil composition and nutrient levels
- Environmental factors (climate and weather data)
- Crop types and seasonal patterns
- Regional variations in farming practices
- Historical yield records

Features were preprocessed and normalized to ensure optimal model performance. The dataset was split into training and testing sets to validate prediction accuracy.

## How It Works

1. **User Input**: Farmer enters agricultural parameters through the web interface
   - Soil nutrients and properties
   - Climate conditions
   - Crop type and farming practices

2. **Data Processing**: Input data is validated and preprocessed
   - Categorical variables are encoded
   - Numerical features are scaled using the trained scaler

3. **Prediction**: The Random Forest model processes the standardized input
   - Model predicts crop yield in tons per hectare
   - Confidence level is calculated based on input quality

4. **Result Display**: The application presents the prediction
   - Estimated yield value
   - Confidence indicator
   - Summary of input parameters
   - Detailed metrics visualization

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. Clone or download the project repository:
   ```bash
   cd Gen_AI_capstone
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure model files are present in the project directory:
   - `model.pkl` (trained Random Forest model)
   - `scaler.pkl` (fitted StandardScaler)
   - `column.pkl` (feature column names)

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Access the application:
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application will load automatically

## Usage

### Basic Workflow

1. **Select Language**: Choose between English or Hindi using the language toggle buttons

2. **Enter Soil Nutrients**:
   - Input Nitrogen (N), Phosphorus (P), and Potassium (K) levels in kg/ha
   - Use sliders or manual input for precision

3. **Specify Soil Properties**:
   - Soil pH (4.0 - 9.0)
   - Soil moisture percentage
   - Organic carbon content
   - Soil type (Loamy, Clay, Sandy, Red, Black)
   - Altitude in meters

4. **Provide Climate Data**:
   - Temperature (degrees Celsius)
   - Humidity percentage
   - Rainfall (mm)
   - Daily sunlight hours
   - Wind speed (km/h)

5. **Select Crop Details**:
   - Crop type (Wheat, Rice, Cotton, Sugarcane, Maize, Barley, Jute)
   - Season (Kharif, Rabi, Zaid, Summer, Winter)
   - Irrigation type (Drip, Sprinkler, Flood, Rainfed)
   - Region (North, South, East, West, Central)
   - Fertilizer and pesticide usage (kg/ha)

6. **Get Prediction**:
   - Click the "Predict" button
   - View the estimated crop yield
   - Review confidence level and detailed metrics

## Project Structure

```
Gen_AI_capstone/
│
├── app.py                  # Main Streamlit application
├── model.pkl              # Trained Random Forest model
├── scaler.pkl             # Fitted StandardScaler for preprocessing
├── column.pkl             # Feature column names for alignment
├── requirements.txt       # Python dependencies
├── farmer.jpeg            # Background image for UI
├── image.png              # Logo image
├── README.md              # Project documentation
└── convert_background.py  # Utility script for image processing
```

### Key Files

- **app.py**: Contains the entire application logic, UI components, and prediction pipeline
- **model.pkl**: Serialized Random Forest Regressor trained on agricultural data
- **scaler.pkl**: Pre-fitted StandardScaler for consistent feature normalization
- **column.pkl**: Stores the expected feature column order for proper model input
- **requirements.txt**: Lists all Python packages needed to run the application

## Team Members

This project was developed as an academic capstone by:

- Aditya Shankar
- Animesh Rai
- Kunal Dev Sahu
- Rishiwant Kumar Maurya

## Future Improvements

### Model Enhancements
- Incorporate deep learning models for improved accuracy
- Add support for more crop varieties
- Include pest and disease prediction capabilities
- Integrate real-time weather API for automatic climate data

### Feature Additions
- Historical yield tracking for farmers
- Crop recommendation system based on soil and climate
- Fertilizer optimization suggestions
- Water usage efficiency calculator
- Multi-crop rotation planning

### Technical Improvements
- Cloud deployment for wider accessibility
- Mobile application (Android/iOS)
- Offline mode for areas with limited connectivity
- Database integration for user data persistence
- Advanced data visualization with interactive charts

### User Experience
- Voice input support for low-literacy users
- Video tutorials in regional languages
- SMS-based predictions for feature phone users
- Community forum for farmer interactions
- Expert consultation integration

## License

This project was developed for educational purposes as part of an academic capstone program.

## Acknowledgments

We thank our academic advisors and the agricultural community for their valuable insights and feedback during the development of this application.
