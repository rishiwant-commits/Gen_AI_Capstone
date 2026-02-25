# 🧪 Sample Test Data for Crop Yield Predictor

## Test Case 1: Rice (High Yield Expected)
```json
{
  "N": 97.0,
  "P": 20.0,
  "K": 40.0,
  "Soil_pH": 6.5,
  "Soil_Moisture": 80.0,
  "Organic_Carbon": 1.2,
  "Temperature": 28.0,
  "Humidity": 85.0,
  "Rainfall": 300.0,
  "Sunlight_Hours": 8.0,
  "Wind_Speed": 3.0,
  "Altitude": 200.0,
  "Fertilizer_Used": 120.0,
  "Pesticide_Used": 30.0,
  "Soil_Type": "Loamy",
  "Region": "South",
  "Season": "Kharif",
  "Crop_Type": "Rice",
  "Irrigation_Type": "Flood"
}
```
**Expected**: 7-9 tons/hectare (High confidence)

---

## Test Case 2: Wheat (Medium Yield)
```json
{
  "N": 80.0,
  "P": 50.0,
  "K": 45.0,
  "Soil_pH": 7.0,
  "Soil_Moisture": 40.0,
  "Organic_Carbon": 0.9,
  "Temperature": 20.0,
  "Humidity": 60.0,
  "Rainfall": 150.0,
  "Sunlight_Hours": 10.0,
  "Wind_Speed": 5.0,
  "Altitude": 300.0,
  "Fertilizer_Used": 100.0,
  "Pesticide_Used": 25.0,
  "Soil_Type": "Clay",
  "Region": "North",
  "Season": "Rabi",
  "Crop_Type": "Wheat",
  "Irrigation_Type": "Sprinkler"
}
```
**Expected**: 4-6 tons/hectare (Medium confidence)

---

## Test Case 3: Maize (Good Conditions)
```json
{
  "N": 90.0,
  "P": 35.0,
  "K": 50.0,
  "Soil_pH": 6.2,
  "Soil_Moisture": 55.0,
  "Organic_Carbon": 1.0,
  "Temperature": 25.0,
  "Humidity": 70.0,
  "Rainfall": 250.0,
  "Sunlight_Hours": 9.0,
  "Wind_Speed": 4.0,
  "Altitude": 250.0,
  "Fertilizer_Used": 110.0,
  "Pesticide_Used": 28.0,
  "Soil_Type": "Loamy",
  "Region": "Central",
  "Season": "Kharif",
  "Crop_Type": "Maize",
  "Irrigation_Type": "Drip"
}
```
**Expected**: 6-8 tons/hectare (High confidence)

---

## Test Case 4: Cotton (Low Rainfall)
```json
{
  "N": 70.0,
  "P": 30.0,
  "K": 35.0,
  "Soil_pH": 7.5,
  "Soil_Moisture": 30.0,
  "Organic_Carbon": 0.7,
  "Temperature": 32.0,
  "Humidity": 50.0,
  "Rainfall": 100.0,
  "Sunlight_Hours": 12.0,
  "Wind_Speed": 6.0,
  "Altitude": 400.0,
  "Fertilizer_Used": 90.0,
  "Pesticide_Used": 35.0,
  "Soil_Type": "Black",
  "Region": "West",
  "Season": "Kharif",
  "Crop_Type": "Cotton",
  "Irrigation_Type": "Drip"
}
```
**Expected**: 2-4 tons/hectare (Medium confidence)

---

## Test Case 5: Sugarcane (Optimal Conditions)
```json
{
  "N": 110.0,
  "P": 40.0,
  "K": 60.0,
  "Soil_pH": 6.8,
  "Soil_Moisture": 70.0,
  "Organic_Carbon": 1.5,
  "Temperature": 30.0,
  "Humidity": 75.0,
  "Rainfall": 350.0,
  "Sunlight_Hours": 10.0,
  "Wind_Speed": 2.0,
  "Altitude": 150.0,
  "Fertilizer_Used": 150.0,
  "Pesticide_Used": 20.0,
  "Soil_Type": "Loamy",
  "Region": "South",
  "Season": "Summer",
  "Crop_Type": "Sugarcane",
  "Irrigation_Type": "Flood"
}
```
**Expected**: 50-70 tons/hectare (High confidence)
*Note: Sugarcane yields are much higher than grain crops*

---

## Test Case 6: Barley (Arid Region)
```json
{
  "N": 65.0,
  "P": 25.0,
  "K": 30.0,
  "Soil_pH": 7.2,
  "Soil_Moisture": 35.0,
  "Organic_Carbon": 0.6,
  "Temperature": 18.0,
  "Humidity": 55.0,
  "Rainfall": 120.0,
  "Sunlight_Hours": 11.0,
  "Wind_Speed": 7.0,
  "Altitude": 500.0,
  "Fertilizer_Used": 80.0,
  "Pesticide_Used": 22.0,
  "Soil_Type": "Sandy",
  "Region": "West",
  "Season": "Rabi",
  "Crop_Type": "Barley",
  "Irrigation_Type": "Sprinkler"
}
```
**Expected**: 3-5 tons/hectare (Medium confidence)

---

## Edge Cases to Test

### Minimum Values (Poor Conditions)
```json
{
  "N": 10.0,
  "P": 5.0,
  "K": 10.0,
  "Soil_pH": 5.0,
  "Soil_Moisture": 15.0,
  "Organic_Carbon": 0.2,
  "Temperature": 10.0,
  "Humidity": 30.0,
  "Rainfall": 50.0,
  "Sunlight_Hours": 4.0,
  "Wind_Speed": 15.0,
  "Altitude": 1000.0,
  "Fertilizer_Used": 20.0,
  "Pesticide_Used": 5.0,
  "Soil_Type": "Sandy",
  "Region": "North",
  "Season": "Winter",
  "Crop_Type": "Wheat",
  "Irrigation_Type": "Rainfed"
}
```
**Expected**: Very low yield (Low confidence)

---

### Maximum Values (Ideal Conditions)
```json
{
  "N": 150.0,
  "P": 80.0,
  "K": 70.0,
  "Soil_pH": 7.0,
  "Soil_Moisture": 60.0,
  "Organic_Carbon": 2.0,
  "Temperature": 28.0,
  "Humidity": 70.0,
  "Rainfall": 350.0,
  "Sunlight_Hours": 12.0,
  "Wind_Speed": 3.0,
  "Altitude": 200.0,
  "Fertilizer_Used": 200.0,
  "Pesticide_Used": 15.0,
  "Soil_Type": "Loamy",
  "Region": "South",
  "Season": "Kharif",
  "Crop_Type": "Rice",
  "Irrigation_Type": "Drip"
}
```
**Expected**: Maximum possible yield (High confidence)

---

## Regional Variations

### North India (Wheat Belt)
- **Crops**: Wheat, Barley
- **Season**: Rabi (Winter)
- **Temp**: 15-25°C
- **Rainfall**: 100-200mm
- **Soil**: Clay, Loamy

### South India (Rice Bowl)
- **Crops**: Rice, Sugarcane
- **Season**: Kharif (Monsoon)
- **Temp**: 25-35°C
- **Rainfall**: 250-400mm
- **Soil**: Loamy, Red

### Central India (Cotton Region)
- **Crops**: Cotton, Maize
- **Season**: Kharif
- **Temp**: 28-35°C
- **Rainfall**: 150-300mm
- **Soil**: Black, Red

### East India (Jute & Rice)
- **Crops**: Rice, Jute
- **Season**: Kharif
- **Temp**: 25-32°C
- **Rainfall**: 300-500mm
- **Soil**: Loamy, Alluvial

### West India (Arid Region)
- **Crops**: Cotton, Wheat
- **Season**: Mixed
- **Temp**: 20-35°C
- **Rainfall**: 80-200mm
- **Soil**: Sandy, Black

---

## Quick Test Values (Copy-Paste)

### Good Rice Yield
```
N: 97, P: 20, K: 40
pH: 6.5, Moisture: 80%, Carbon: 1.2%
Temp: 28°C, Humidity: 85%, Rain: 300mm
Sun: 8h, Wind: 3km/h
Altitude: 200m, Fertilizer: 120, Pesticide: 30
Type: Loamy, Region: South, Season: Kharif
Crop: Rice, Irrigation: Flood
```

### Good Wheat Yield
```
N: 80, P: 50, K: 45
pH: 7.0, Moisture: 40%, Carbon: 0.9%
Temp: 20°C, Humidity: 60%, Rain: 150mm
Sun: 10h, Wind: 5km/h
Altitude: 300m, Fertilizer: 100, Pesticide: 25
Type: Clay, Region: North, Season: Rabi
Crop: Wheat, Irrigation: Sprinkler
```

---

## Mobile Testing Tips

1. **Start with defaults** - Just change crop type and predict
2. **Use sliders first** - Easier on mobile than typing
3. **Test language toggle** - Switch between EN/HI
4. **Check responsiveness** - Rotate device
5. **Verify tooltips** - Tap the ℹ️ icons
6. **Test validation** - Try invalid values
7. **Check loading animation** - Watch the spinner
8. **Review result display** - Is it readable?

---

## Expected Yield Ranges by Crop

| Crop      | Low    | Medium | High   | Unit        |
|-----------|--------|--------|--------|-------------|
| Wheat     | 2-3    | 4-5    | 6-7    | ton/ha      |
| Rice      | 3-4    | 5-7    | 8-10   | ton/ha      |
| Maize     | 2-3    | 4-6    | 7-9    | ton/ha      |
| Cotton    | 1-2    | 2-3    | 4-5    | ton/ha      |
| Sugarcane | 30-40  | 50-60  | 70-90  | ton/ha      |
| Barley    | 2-3    | 3-4    | 5-6    | ton/ha      |
| Jute      | 1-2    | 2-3    | 3-4    | ton/ha      |

---

**Note**: Actual predictions will vary based on the trained model. These are approximate ranges for validation purposes.
