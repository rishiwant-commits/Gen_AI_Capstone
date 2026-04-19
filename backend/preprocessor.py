import pandas as pd

def preprocess_input(user_input_dict, columns):
    input_df = pd.DataFrame([user_input_dict])

    input_encoded = pd.get_dummies(
        input_df,
        columns=['Soil_Type', 'Region', 'Season', 'Crop_Type', 'Irrigation_Type'],
        drop_first=True
    )

    final_input_df = input_encoded.reindex(columns=columns, fill_value=0)

    return final_input_df