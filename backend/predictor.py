def predict_yield(model, scaler, final_input_df):
    scaled_input = scaler.transform(final_input_df)
    prediction = model.predict(scaled_input)[0]
    return prediction